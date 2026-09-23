import os
import time
from google import genai
from sqlalchemy.orm import Session
from app.models.campaign import Campaign
from app.models.campaign_metrics import CampaignMetric
from app.models.anomaly import Anomaly

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_FALLBACKS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3.6-flash"]

def build_context(db: Session) -> str:
    campaigns = db.query(Campaign).all()
    anomalies = db.query(Anomaly).order_by(Anomaly.created_at.desc()).limit(10).all()

    lines = ["Current campaigns:"]
    for c in campaigns:
        metrics = db.query(CampaignMetric).filter(CampaignMetric.campaign_id == c.id).all()
        total_spend = sum(m.spend for m in metrics)
        total_revenue = sum(m.revenue for m in metrics)
        total_clicks = sum(m.clicks for m in metrics)
        total_conversions = sum(m.conversions for m in metrics)
        roas = round(total_revenue / total_spend, 2) if total_spend else 0
        cvr = round(total_conversions / total_clicks, 4) if total_clicks else 0
        lines.append(f"- {c.name} ({c.channel}, {c.status}): spend ${total_spend}, ROAS {roas}x, CVR {cvr*100}%")

    lines.append("\nRecent anomalies:")
    for a in anomalies:
        lines.append(f"- {a.metric_name} anomaly on {a.date}, severity {a.severity}: expected {a.expected_value}, actual {a.actual_value}")

    return "\n".join(lines)

def ask(db: Session, question: str) -> str:
    context = build_context(db)
    prompt = f"""You are an AI assistant embedded in Mercora, a commerce/campaign intelligence platform.
Answer the user's question using ONLY the data below. Be specific, cite real numbers, and keep it concise (3-5 sentences).
If the data doesn't answer the question, say so honestly rather than guessing.

DATA:
{context}

QUESTION: {question}"""

    for model_name in MODEL_FALLBACKS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(model=model_name, contents=prompt)
                return response.text
            except Exception as e:
                print(f"{model_name} attempt {attempt + 1} failed: {e}")
                time.sleep(1.5)
    return "I'm having trouble reaching the AI service right now. Please try again in a moment."