import onnxruntime as ort
import numpy as np
from .rule_engine import RuleEngine

class HybridAnalyzer:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.ml_model = ort.InferenceSession("ml_models/detection.onnx")
        
    def analyze(self, usb_data):
        # 规则匹配
        rule_alerts = self.rule_engine.check(usb_data)
        if rule_alerts:
            return rule_alerts
            
        # 机器学习检测
        input_data = self._preprocess(usb_data)
        pred = self.ml_model.run(None, {'input': input_data})
        if pred[0][0] > 0.8:  # 阈值可配置
            return [{"type": "ml_anomaly", "score": float(pred[0][0])}]
        return []

    def _preprocess(self, data):
        # 将USB数据转换为模型输入格式
        return np.array([data['packet_size'], data['interval']], dtype=np.float32)