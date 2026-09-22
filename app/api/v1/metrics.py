from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.metrics import get_campaign_metrics
from app.models.campaign import Campaign
from sqlalchemy import func
from fastapi import HTTPException
from app.models.anomaly import Anomaly
from app.models.campaign_metrics import CampaignMetric
from app.core.auth import verify_api_key
router = APIRouter()

@router.get("/metrics/{campaign_id}")
def read_metrics(campaign_id: int, db: Session = Depends(get_db)):
    return get_campaign_metrics(db, campaign_id)

@router.get("/campaigns")
def list_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).all()
    return [{"id": c.id, "name": c.name, "channel": c.channel, "status": c.status} for c in campaigns]

@router.get("/metrics/{campaign_id}/trend")
def get_trend(campaign_id: int, db: Session = Depends(get_db)):
    rows = db.query(CampaignMetric).filter(
        CampaignMetric.campaign_id == campaign_id
    ).order_by(CampaignMetric.date).all()
    return [
        {
            "date": str(r.date), "impressions": r.impressions, "clicks": r.clicks,
            "conversions": r.conversions, "spend": r.spend, "revenue": r.revenue,
            "cvr": round(r.conversions / r.clicks, 4) if r.clicks else 0,
            "ctr": round(r.clicks / r.impressions, 4) if r.impressions else 0,
        }
        for r in rows
    ]

from app.models.anomaly import Anomaly

@router.get("/summary")
def get_summary(campaign_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(CampaignMetric)
    if campaign_id:
        query = query.filter(CampaignMetric.campaign_id == campaign_id)
    metrics = query.all()

    if campaign_id:
        campaigns_count = 1
        anomalies_count = db.query(Anomaly).filter(Anomaly.campaign_id == campaign_id).count()
    else:
        campaigns_count = db.query(Campaign).count()
        anomalies_count = db.query(Anomaly).count()

    total_impressions = sum(m.impressions for m in metrics)
    total_clicks = sum(m.clicks for m in metrics)
    total_conversions = sum(m.conversions for m in metrics)
    total_spend = sum(m.spend for m in metrics)
    total_revenue = sum(m.revenue for m in metrics)

    return {
        "total_impressions": total_impressions,
        "conversion_rate": round(total_conversions / total_clicks, 4) if total_clicks else 0,
        "revenue": round(total_revenue, 2),
        "cost_per_acquisition": round(total_spend / total_conversions, 2) if total_conversions else 0,
        "active_campaigns": campaigns_count,
        "anomalies_detected": anomalies_count,
    }


@router.delete("/campaigns/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db), _: None = Depends(verify_api_key)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.query(Anomaly).filter(Anomaly.campaign_id == campaign_id).delete()
    db.query(CampaignMetric).filter(CampaignMetric.campaign_id == campaign_id).delete()
    db.delete(campaign)
    db.commit()
    return {"deleted": campaign_id}

@router.delete("/reset")
def reset_all_data(db: Session = Depends(get_db), _: None = Depends(verify_api_key)):
    db.query(Anomaly).delete()
    db.query(CampaignMetric).delete()
    db.query(Campaign).delete()
    db.commit()
    return {"status": "all data cleared"}