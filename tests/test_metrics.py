from datetime import date
from app.models.campaign import Campaign
from app.models.campaign_metrics import CampaignMetric
from app.services.metrics import get_campaign_metrics

def test_metrics_calculation(db_session):
    campaign = Campaign(name="Test", channel="Google Ads", status="active", start_date=date(2026, 8, 1))
    db_session.add(campaign)
    db_session.commit()
    db_session.refresh(campaign)

    metric = CampaignMetric(
        campaign_id=campaign.id, date=date(2026, 8, 1),
        impressions=1000, clicks=100, spend=200.0, conversions=10, revenue=1000.0,
    )
    db_session.add(metric)
    db_session.commit()

    result = get_campaign_metrics(db_session, campaign.id)
    assert len(result) == 1
    assert result[0]["ctr"] == 0.1
    assert result[0]["cvr"] == 0.1
    assert result[0]["cpc"] == 2.0
    assert result[0]["roas"] == 5.0

def test_metrics_zero_division_safe(db_session):
    campaign = Campaign(name="Zero Test", channel="Meta Ads", status="active", start_date=date(2026, 8, 1))
    db_session.add(campaign)
    db_session.commit()
    db_session.refresh(campaign)

    metric = CampaignMetric(
        campaign_id=campaign.id, date=date(2026, 8, 1),
        impressions=0, clicks=0, spend=0.0, conversions=0, revenue=0.0,
    )
    db_session.add(metric)
    db_session.commit()

    result = get_campaign_metrics(db_session, campaign.id)
    assert result[0]["ctr"] == 0
    assert result[0]["cvr"] == 0