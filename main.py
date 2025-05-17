from queue import Queue
import time
from core.device_monitor import USBMonitor
from core.behavior_analyzer import BehaviorAnalyzer
from core.alert_manager import AlertManager

def main():
    event_queue = Queue()
    monitor = USBMonitor(event_queue)
    analyzer = BehaviorAnalyzer()
    alert_manager = AlertManager()

    monitor.start()

    try:
        while True:
            if not event_queue.empty():
                event_type, data = event_queue.get()
                if event_type == 'insert':
                    # 模拟采集数据（实际需实现USB数据捕获）
                    test_data = {'hid.input_rate': 35, 'device.vendor_id': '0x1234'}
                    alerts = analyzer.analyze(data, test_data)
                    for alert in alerts:
                        alert_manager.trigger_alert(alert)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[INFO] 监控已停止")

if __name__ == "__main__":
    main()