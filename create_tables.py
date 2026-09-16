from app.core.database import Base, engine
from app.models.campaign import Campaign
from app.models.campaign_metrics import CampaignMetric
from app.models.anomaly import Anomaly
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")