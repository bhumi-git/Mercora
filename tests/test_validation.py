import pytest
from pydantic import ValidationError
from app.schemas.campaign import CampaignMetricRow

def test_valid_row_passes():
    row = CampaignMetricRow(
        campaign_name="Test Campaign", channel="Google Ads", date="2026-08-01",
        impressions=1000, clicks=50, spend=100.0, conversions=5, revenue=500.0,
    )
    assert row.campaign_name == "Test Campaign"
    assert row.clicks == 50

def test_missing_required_field_fails():
    with pytest.raises(ValidationError):
        CampaignMetricRow(
            campaign_name="Test Campaign", channel="Google Ads", date="2026-08-01",
            clicks=50, spend=100.0, conversions=5, revenue=500.0,
        )

def test_wrong_type_fails():
    with pytest.raises(ValidationError):
        CampaignMetricRow(
            campaign_name="Test Campaign", channel="Google Ads", date="2026-08-01",
            impressions="not a number", clicks=50, spend=100.0, conversions=5, revenue=500.0,
        )