from typing import Dict, List
from core.models import Alert
from core.channels import ChannelType
from .llm import LLMAnalyzer

class SentinelAnalyzer:
    def __init__(self):
        self.llm = LLMAnalyzer()
        self.system_prompt = """
        # Role: Security Sentinel
        输出要求：
        1. 按风险等级分组
        2. 包含原始链接
        3. 提供缓解建议
        """

    def generate_report(self, alerts: List[Alert]) -> str:
        grouped = self._group_alerts(alerts)
        return self.llm.analyze(
            system_prompt=self.system_prompt,
            user_content=str(grouped)
        )

    def _group_alerts(self, alerts: List[Alert]) -> Dict[int, List[Alert]]:
        return {
            level: [a for a in alerts if a.severity == level]
            for level in range(1, 6)
        }
