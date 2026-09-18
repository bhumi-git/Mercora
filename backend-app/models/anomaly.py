from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    metric_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    expected_value = Column(Float, nullable=False)
    actual_value = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    ai_explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())