import statistics
from sqlalchemy.orm import Session
from app.models.campaign_metrics import CampaignMetric
from app.models.anomaly import Anomaly

def detect_anomalies(db: Session, campaign_id: int, z_threshold: float = 1.0):
    rows = db.query(CampaignMetric).filter(
        CampaignMetric.campaign_id == campaign_id
    ).order_by(CampaignMetric.date).all()

    if len(rows) < 3:
        return []

    cvr_values = [r.conversions / r.clicks if r.clicks else 0 for r in rows]
    mean = statistics.mean(cvr_values)
    stdev = statistics.stdev(cvr_values) if len(cvr_values) > 1 else 0

    found = []
    for r, cvr in zip(rows, cvr_values):
        if stdev == 0:
            continue
        z = (cvr - mean) / stdev
        if abs(z) > z_threshold:
            existing = db.query(Anomaly).filter(
                Anomaly.campaign_id == campaign_id,
                Anomaly.metric_name == "cvr",
                Anomaly.date == r.date
            ).first()
            if existing:
                continue

            severity = "severe" if abs(z) > 2.5 else "moderate" if abs(z) > 2 else "mild"
            anomaly = Anomaly(
                campaign_id=campaign_id, metric_name="cvr", date=r.date,
                expected_value=round(mean, 4), actual_value=round(cvr, 4),
                severity=severity
            )
            db.add(anomaly)
            found.append(anomaly)

    db.commit()
    return found