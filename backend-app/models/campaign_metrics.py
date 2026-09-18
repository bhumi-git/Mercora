from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class CampaignMetric(Base):
    __tablename__ = "campaign_metrics"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    date = Column(Date, nullable=False)
    impressions = Column(Integer, nullable=False, default=0)
    clicks = Column(Integer, nullable=False, default=0)
    spend = Column(Float, nullable=False, default=0.0)
    conversions = Column(Integer, nullable=False, default=0)
    revenue = Column(Float, nullable=False, default=0.0)

    campaign = relationship("Campaign", backref="metrics")