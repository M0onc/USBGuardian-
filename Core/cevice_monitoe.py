import usb.core
import usb.util
from threading import Thread
from queue import Queue
from utils.logger import Logger
from utils.config_loader import load_config

class USBMonitor(Thread):
    def __init__(self, event_queue):
        super().__init__(daemon=True)
        self.event_queue = event_queue  # 异步事件队列
        self.config = load_config()
        self.logger = Logger(self.config['paths']['log_file'])
        self.active_devices = {}

    def run(self):
        """异步监控USB设备插拔事件"""
        while True:
            self._detect_devices()
            time.sleep(1)  # 降低CPU占用

    def _detect_devices(self):
        current_devices = {dev.idVendor: dev for dev in usb.core.find(find_all=True)}
        # 检测新设备插入
        for vid, dev in current_devices.items():
            if vid not in self.active_devices:
                self._handle_new_device(dev)
        # 检测设备移除
        for vid in list(self.active_devices.keys()):
            if vid not in current_devices:
                self._handle_device_removal(vid)

    def _handle_new_device(self, device):
        """处理新设备插入事件"""
        device_info = {
            "vendor_id": hex(device.idVendor),
            "product_id": hex(device.idProduct),
            "insert_time": datetime.now().isoformat()
        }
        self.active_devices[device.idVendor] = device_info
        self.event_queue.put(('insert', device_info))  # 推送事件到队列
        self.logger.log(f"新设备接入: {device_info}")

    def _handle_device_removal(self, vendor_id):
        """处理设备移除事件"""
        device_info = self.active_devices.pop(vendor_id, None)
        if device_info:
            self.event_queue.put(('remove', device_info))
            self.logger.log(f"设备移除: {device_info}")