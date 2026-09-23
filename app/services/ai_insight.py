import os
import time
from google import genai
from sqlalchemy.orm import Session
from app.models.anomaly import Anomaly

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_FALLBACKS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3.6-flash"]

def generate_explanation(anomaly: Anomaly) -> str | None:
    prompt = f"""A marketing campaign showed an anomaly:
Metric: {anomaly.metric_name}
Expected value: {anomaly.expected_value}
Actual value: {anomaly.actual_value}
Severity: {anomaly.severity}

In 2-3 sentences, explain a likely cause for this and suggest one next investigation step. Be concise and practical."""

    for model_name in MODEL_FALLBACKS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(model=model_name, contents=prompt)
                return response.text
            except Exception as e:
                print(f"{model_name} attempt {attempt + 1} failed for anomaly {anomaly.id}: {e}")
                time.sleep(1.5)
    return None

def generate_explanations_for_anomalies(db: Session, anomalies: list[Anomaly]):
    for a in anomalies:
        a.ai_explanation = generate_explanation(a)
        time.sleep(1)
    db.commit()