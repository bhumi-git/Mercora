from datetime import date, timedelta
from app.models.campaign import Campaign
from app.models.campaign_metrics import CampaignMetric
from app.services.anomaly_detection import detect_anomalies

def test_detects_clear_anomaly(db_session):
    campaign = Campaign(name="Anomaly Test", channel="Google Ads", status="active", start_date=date(2026, 8, 1))
    db_session.add(campaign)
    db_session.commit()
    db_session.refresh(campaign)

    base_date = date(2026, 8, 1)
    normal_days = [(100, 10) for _ in range(5)]
    for i, (clicks, conversions) in enumerate(normal_days):
        db_session.add(CampaignMetric(
            campaign_id=campaign.id, date=base_date + timedelta(days=i),
            impressions=1000, clicks=clicks, spend=100.0, conversions=conversions, revenue=500.0,
        ))
    db_session.add(CampaignMetric(
        campaign_id=campaign.id, date=base_date + timedelta(days=5),
        impressions=1000, clicks=100, spend=100.0, conversions=1, revenue=50.0,
    ))
    db_session.commit()

    anomalies = detect_anomalies(db_session, campaign.id, z_threshold=1.0)
    assert len(anomalies) >= 1
    assert anomalies[0].metric_name == "cvr"

def test_no_anomaly_with_insufficient_data(db_session):
    campaign = Campaign(name="Sparse Test", channel="Meta Ads", status="active", start_date=date(2026, 8, 1))
    db_session.add(campaign)
    db_session.commit()
    db_session.refresh(campaign)

    db_session.add(CampaignMetric(
        campaign_id=campaign.id, date=date(2026, 8, 1),
        impressions=1000, clicks=100, spend=100.0, conversions=10, revenue=500.0,
    ))
    db_session.commit()

    anomalies = detect_anomalies(db_session, campaign.id)
    assert anomalies == []