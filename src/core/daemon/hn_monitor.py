import time
from core.hn_analyzer import HNAnalyzer
from datetime import datetime

class HNDaemon:
    def __init__(self, interval: int = 3600):
        self.analyzer = HNAnalyzer()
        self.interval = interval

    def run(self):
        while True:
            try:
                report = self.analyzer.generate_daily_report()
                self._save_report(report)
            except Exception as e:
                print(f"[ERROR] {datetime.now()}: {str(e)}")
            time.sleep(self.interval)

    def _save_report(self, content: str):
        filename = f"hn_report_{datetime.now().date()}.md"
        with open(f"reports/{filename}", "w") as f:
            f.write(content)
        print(f"[INFO] 报告已保存至 {filename}")

if __name__ == "__main__":
    daemon = HNDaemon()
    daemon.run()  # 每小时自动生成报告
