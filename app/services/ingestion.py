import pandas as pd
from sqlalchemy.orm import Session
from app.models.campaign import Campaign
from app.models.campaign_metrics import CampaignMetric
from app.schemas.campaign import CampaignMetricRow
from app.services.anomaly_detection import detect_anomalies
from app.services.ai_insight import generate_explanations_for_anomalies

def read_file(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        return pd.read_json(file_path)
    elif file_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type")

def ingest_dataframe(df: pd.DataFrame, db: Session):
    inserted, skipped, failed = 0, 0, []
    touched_campaign_ids = set()

    for idx, row in df.iterrows():
        try:
            validated = CampaignMetricRow(**row.to_dict())
        except Exception as e:
            failed.append({"row": idx, "error": str(e)})
            continue

        campaign = db.query(Campaign).filter(Campaign.name == validated.campaign_name).first()
        if not campaign:
            campaign = Campaign(
                name=validated.campaign_name,
                channel=validated.channel,
                start_date=validated.date,
                status="active",
            )
            db.add(campaign)
            db.commit()
            db.refresh(campaign)

        touched_campaign_ids.add(campaign.id)

        existing = db.query(CampaignMetric).filter(
            CampaignMetric.campaign_id == campaign.id,
            CampaignMetric.date == validated.date
        ).first()
        if existing:
            skipped += 1
            continue

        metric = CampaignMetric(
            campaign_id=campaign.id,
            date=validated.date,
            impressions=validated.impressions,
            clicks=validated.clicks,
            spend=validated.spend,
            conversions=validated.conversions,
            revenue=validated.revenue,
        )
        db.add(metric)
        inserted += 1

    db.commit()

    total_new_anomalies = 0
    for campaign_id in touched_campaign_ids:
        anomalies = detect_anomalies(db, campaign_id)
        generate_explanations_for_anomalies(db, anomalies)
        total_new_anomalies += len(anomalies)

    return {
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
        "campaigns_processed": len(touched_campaign_ids),
        "new_anomalies_detected": total_new_anomalies,
    }