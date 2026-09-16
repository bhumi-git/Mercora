import os
from urllib import response
from google import genai
from sqlalchemy.orm import Session
from app.models.anomaly import Anomaly

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_explanation(anomaly: Anomaly) -> str:
    prompt = f"""A marketing campaign showed an anomaly:
Metric: {anomaly.metric_name}
Expected value: {anomaly.expected_value}
Actual value: {anomaly.actual_value}
Severity: {anomaly.severity}

In 2-3 sentences, explain a likely cause for this and suggest one next investigation step. Be concise and practical."""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

def generate_explanations_for_anomalies(db: Session, anomalies: list[Anomaly]):
    for a in anomalies:
        a.ai_explanation = generate_explanation(a)
    db.commit()