from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class ChannelType(Enum):
    GITHUB = "github"
    HACKERNEWS = "hackernews"
    CUSTOM_RSS = "rss"

@dataclass
class Alert:
    title: str
    content: str
    severity: int  # 1-5
    source: ChannelType
    timestamp: datetime
