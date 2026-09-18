from pydantic import BaseModel
from datetime import date

class CampaignMetricRow(BaseModel):
    campaign_name: str
    channel: str
    date: date
    impressions: int
    clicks: int
    spend: float
    conversions: int
    revenue: float