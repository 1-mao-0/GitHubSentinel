import pytest
from core.channels.hackernews import HackerNewsChannel
from unittest.mock import patch

@patch("requests.get")
def test_hn_channel(mock_get):
    mock_get.return_value.json.return_value = {
        "hits": [{
            "title": "Test Alert",
            "points": 150,
            "url": "http://example.com",
            "created_at_i": 1234567890
        }]
    }
    
    chan = HackerNewsChannel({"min_points": 100})
    alerts = chan.fetch_alerts()
    
    assert len(alerts) == 1
    assert alerts[0].severity == 3  # 150/50 +1
