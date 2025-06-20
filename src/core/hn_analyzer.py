import requests
from datetime import datetime, timedelta
from typing import List, Dict
from core.llm import LLMAnalyzer  # 复用原有LLM

class HNAnalyzer:
    HN_API = "https://hn.algolia.com/api/v1/search"

    def __init__(self):
        self.llm = LLMAnalyzer()
        self.system_prompt = """
        # Role: Hacker News 趋势分析师
        输出要求：
        1. 按技术领域分类（AI/区块链/安全等）
        2. 标注热度指标（🔥xN）
        3. 包含专家短评
        """

    def fetch_top_stories(self, hours: int = 24) -> List[Dict]:
        """获取最近N小时的热门故事"""
        params = {
            "tags": "story",
            "numericFilters": f"created_at_i>{int((datetime.now() - timedelta(hours=hours)).timestamp()}",
            "hitsPerPage": 50
        }
        resp = requests.get(self.HN_API, params=params)
        return sorted(resp.json()["hits"], key=lambda x: -x["points"])

    def generate_daily_report(self) -> str:
        """生成每日趋势报告"""
        stories = self.fetch_top_stories()
        report = self.llm.analyze(
            system_prompt=self.system_prompt,
            user_content="分析以下HN故事趋势：\n" + "\n".join(
                f"- {s['title']} (🔥{s['points']})" 
                for s in stories[:10]
            )
        )
        return f"# Hacker News 每日报告\n{report}"
