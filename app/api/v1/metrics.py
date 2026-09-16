from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.campaign_metrics import CampaignMetric
from app.services.metrics import get_campaign_metrics
from app.models.campaign import Campaign
from sqlalchemy import func

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