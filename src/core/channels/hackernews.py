import requests
from core.channels.base import BaseChannel
from core.models import Alert, ChannelType
from datetime import datetime

class HackerNewsChannel(BaseChannel):
    def __init__(self, config: dict):
        self.min_points = config.get("min_points", 100)
        self.api_url = "https://hn.algolia.com/api/v1/search"

    def fetch_alerts(self) -> List[Alert]:
        resp = requests.get(self.api_url, params={
            "tags": "story",
            "hitsPerPage": 20,
            "numericFilters": [f"points>{self.min_points}"]
        })
        return [
            Alert(
                title=item["title"],
                content=f"Points: {item['points']} | {item['url']}",
                severity=self._calc_severity(item["points"]),
                source=ChannelType.HACKERNEWS,
                timestamp=datetime.fromtimestamp(item["created_at_i"])
            ) for item in resp.json()["hits"]
        ]

    def _calc_severity(self, points: int) -> int:
        return min(points // 50 + 1, 5)  # 每50点增加1级严重度
