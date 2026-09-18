from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.campaign_metrics import CampaignMetric

def get_campaign_metrics(db: Session, campaign_id: int):
    rows = db.query(CampaignMetric).filter(CampaignMetric.campaign_id == campaign_id).all()
    result = []
    for r in rows:
        ctr = r.clicks / r.impressions if r.impressions else 0
        cvr = r.conversions / r.clicks if r.clicks else 0
        cpc = r.spend / r.clicks if r.clicks else 0
        roas = r.revenue / r.spend if r.spend else 0
        result.append({
            "date": r.date, "ctr": round(ctr, 4), "cvr": round(cvr, 4),
            "cpc": round(cpc, 2), "roas": round(roas, 2),
            "impressions": r.impressions, "clicks": r.clicks,
            "spend": r.spend, "conversions": r.conversions, "revenue": r.revenue
        })
    return result