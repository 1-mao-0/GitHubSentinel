import pytest
from daemon.sentinel_d import SentinelDaemon
from unittest.mock import MagicMock

def test_daemon_loop():
    mock_channel = MagicMock()
    mock_channel.fetch_alerts.return_value = []
    
    daemon = SentinelDaemon({
        "interval": 10,
        "channels": [mock_channel]
    })
    
    # 测试单次循环
    daemon.run_once()  
    mock_channel.fetch_alerts.assert_called_once()
