import time
import logging
from multiprocessing import Process
from core.channels import ChannelType
from core.analyzer import SentinelAnalyzer

class SentinelDaemon:
    def __init__(self, config: dict):
        self.interval = config["interval"]
        self.channels = self._init_channels(config["channels"])
        self.analyzer = SentinelAnalyzer()

    def run(self):
        while True:
            try:
                alerts = []
                for chan in self.channels:
                    alerts.extend(chan.fetch_alerts())
                
                report = self.analyzer.generate_report(alerts)
                self._save_report(report)
                
            except Exception as e:
                logging.exception("Daemon error")
            finally:
                time.sleep(self.interval)
