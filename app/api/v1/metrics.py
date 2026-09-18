from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.campaign_metrics import CampaignMetric
from app.services.metrics import get_campaign_metrics
from app.models.campaign import Campaign
from sqlalchemy import func
from app.models.anomaly import Anomaly

router = APIRouter()

@router.get("/metrics/{campaign_id}")
def read_metrics(campaign_id: int, db: Session = Depends(get_db)):
    return get_campaign_metrics(db, campaign_id)

@router.get("/campaigns")
def list_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).all()
    return [{"id": c.id, "name": c.name, "channel": c.channel} for c in campaigns]

@router.get("/metrics/{campaign_id}/trend")
def get_trend(campaign_id: int, db: Session = Depends(get_db)):
    rows = db.query(CampaignMetric).filter(
        CampaignMetric.campaign_id == campaign_id
    ).order_by(CampaignMetric.date).all()

    result = []
    prev_cvr = None
    for r in rows:
        cvr = round(r.conversions / r.clicks, 4) if r.clicks else 0
        delta = round(cvr - prev_cvr, 4) if prev_cvr is not None else None
        result.append({"date": str(r.date), "cvr": cvr, "cvr_change_from_prev_day": delta})
        prev_cvr = cvr
    return result

from app.models.anomaly import Anomaly

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    metrics = db.query(CampaignMetric).all()
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