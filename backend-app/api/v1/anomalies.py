from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.anomaly_detection import detect_anomalies
from app.services.ai_insight import generate_explanations_for_anomalies
from app.models.anomaly import Anomaly

router = APIRouter()

@router.post("/anomalies/{campaign_id}/detect")
def run_detection(campaign_id: int, db: Session = Depends(get_db)):
    anomalies = detect_anomalies(db, campaign_id)
    generate_explanations_for_anomalies(db, anomalies)
    return {"detected": len(anomalies), "anomalies": [
        {"date": str(a.date), "metric": a.metric_name, "expected": a.expected_value,
         "actual": a.actual_value, "severity": a.severity, "explanation": a.ai_explanation}
        for a in anomalies
    ]}

@router.get("/anomalies/{campaign_id}")
def list_anomalies(campaign_id: int, db: Session = Depends(get_db)):
    anomalies = db.query(Anomaly).filter(Anomaly.campaign_id == campaign_id).all()
    return [
        {"date": str(a.date), "metric": a.metric_name, "expected": a.expected_value,
         "actual": a.actual_value, "severity": a.severity, "explanation": a.ai_explanation}
        for a in anomalies
    ]
@router.get("/anomalies")
def list_all_anomalies(db: Session = Depends(get_db)):
    anomalies = db.query(Anomaly).order_by(Anomaly.created_at.desc()).all()
    return [
        {"id": a.id, "campaign_id": a.campaign_id, "date": str(a.date), "metric": a.metric_name,
         "expected": a.expected_value, "actual": a.actual_value, "severity": a.severity,
         "explanation": a.ai_explanation, "created_at": str(a.created_at)}
        for a in anomalies
    ]