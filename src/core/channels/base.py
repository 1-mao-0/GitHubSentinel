from abc import ABC, abstractmethod
from typing import List
from core.models import Alert

class BaseChannel(ABC):
    @abstractmethod
    def fetch_alerts(self) -> List[Alert]:
        pass

    @staticmethod
    def validate_config(config: dict) -> bool:
        """验证渠道配置"""
        return True
