import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, log_path):
        self.logger = logging.getLogger('USBGuardian')
        self.logger.setLevel(logging.DEBUG)
        
        # 文件日志（自动轮换）
        file_handler = RotatingFileHandler(
            log_path, maxBytes=5*1024*1024, backupCount=3
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # 控制台日志
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def log(self, message, level='INFO'):
        getattr(self.logger, level.lower())(message)