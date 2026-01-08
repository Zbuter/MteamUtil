import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import datetime
from pathlib import Path
import config


class LoggerUtil:
    """日志工具类"""

    def __init__(self, name='mteam', log_file='mteam.log', level=logging.INFO,
                 max_bytes=1*1024*1024, backup_count=10):
        """
        初始化日志工具

        Args:
            name: 日志记录器名称
            log_file: 日志文件路径
            level: 日志级别
            max_bytes: 单个日志文件最大大小（字节）
            backup_count: 保留的备份文件数量
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers(log_file, max_bytes, backup_count)

    def _setup_handlers(self, log_file, max_bytes, backup_count):
        """设置日志处理器"""
        # 创建日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
        )

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 文件处理器 - 按大小轮转
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message):
        """记录信息级别日志"""
        self.logger.info(message)

    def warning(self, message):
        """记录警告级别日志"""
        self.logger.warning(message)

    def error(self, message, exc_info=False):
        """记录错误级别日志"""
        self.logger.error(message, exc_info=exc_info)

    def debug(self, message):
        """记录调试级别日志"""
        self.logger.debug(message)


# 创建全局日志实例
logger = LoggerUtil(log_file=config.LOG_PATH).logger
