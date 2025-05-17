from utils.logger import Logger
from utils.config_loader import load_config

class AlertManager:
    def __init__(self):
        self.config = load_config()
        self.logger = Logger(self.config['paths']['log_file'])

    def trigger_alert(self, alert_data):
        message = f"ALERT - Rule {alert_data['rule_id']} triggered. Risk: {alert_data['risk_level']}"
        self.logger.log(message, level='WARNING')
        # 此处可扩展邮件/短信通知
        print(f"\033[91m{message}\033[0m")  # 控制台红色输出