import requests
import json
from datetime import datetime

class SplunkLogger:
    def __init__(self, token: str, host: str = "splunk.example.com"):
        self.url = f"https://{host}:8088/services/collector"
        self.headers = {
            "Authorization": f"Splunk {token}",
            "Content-Type": "application/json"
        }
    
    def send_event(self, event: dict):
        payload = {
            "event": event,
            "sourcetype": "_json",
            "source": "USBGuardian",
            "time": datetime.now().timestamp()
        }
        resp = requests.post(self.url, headers=self.headers, json=payload, verify=False)
        resp.raise_for_status()