import json
from utils.config_loader import load_config
from utils.logger import Logger

class BehaviorAnalyzer:
    def __init__(self, rule_path):
        self.config = load_config()
        self.logger = Logger(self.config['paths']['log_file'])
        self.rules = self._load_rules(rule_path)
        self.normal_baseline = self._load_baseline()

    def _load_rules(self, path):
        """加载预定义攻击规则库"""
        with open(path, 'r') as f:
            return json.load(f).get('rules', [])

    def analyze(self, device, data_packets):
        """多维度行为分析"""
        results = []
        # 规则匹配检测
        for rule in self.rules:
            if self._match_rule(data_packets, rule):
                results.append(rule['type'])
        # 阈值检测（如键盘频率）
        if self._check_keyboard_rate(data_packets):
            results.append("高频键盘输入攻击")
        return results

    def _match_rule(self, data, rule):
        """匹配预定义特征规则"""
        # 示例：检测HID协议异常指令
        if rule['field'] == 'hid_command' and data.get('hid') == rule['value']:
            return True
        return False

    def _check_keyboard_rate(self, data):
        """动态阈值检测"""
        rate = data.get('input_rate', 0)
        return rate > self.config['thresholds']['keyboard_input_rate']