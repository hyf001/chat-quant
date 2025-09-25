"""
日志工具模块
提供统一的日志管理功能，支持多种输出格式和级别控制
"""

import os
import sys
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum


class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class Logger:
    """统一日志管理器"""

    _instance = None
    _loggers: Dict[str, logging.Logger] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.log_dir = Path("logs")
            self.log_dir.mkdir(exist_ok=True)
            self.default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            self.default_date_format = '%Y-%m-%d %H:%M:%S'

    def get_logger(
        self,
        name: str = "chat-quant",
        level: LogLevel = LogLevel.INFO,
        console_output: bool = True,
        file_output: bool = True,
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        file_prefix: str = None
    ) -> logging.Logger:
        """
        获取或创建logger实例

        Args:
            name: logger名称（显示在日志内容中）
            level: 日志级别
            console_output: 是否输出到控制台
            file_output: 是否输出到文件
            max_file_size: 单个日志文件最大大小（字节）
            backup_count: 日志文件备份数量
            file_prefix: 日志文件名前缀，如果不指定则使用name

        Returns:
            logging.Logger: 配置好的logger实例
        """
        if name in self._loggers:
            return self._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(level.value)
        logger.handlers.clear()
        # 防止日志向上级logger传播，避免重复输出
        logger.propagate = False

        formatter = logging.Formatter(
            self.default_format,
            datefmt=self.default_date_format
        )

        # 控制台输出
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level.value)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # 文件输出
        if file_output:
            # 普通日志文件 - 使用TimedRotatingFileHandler按日期归档
            file_name_prefix = file_prefix or name
            log_file = self.log_dir / f"{file_name_prefix}.log"
            file_handler = logging.handlers.TimedRotatingFileHandler(
                log_file,
                when='midnight',
                interval=1,
                backupCount=backup_count,
                encoding='utf-8'
            )
            # 设置归档文件后缀格式为 -YYYY-MM-DD
            file_handler.suffix = "-%Y-%m-%d"
            file_handler.setLevel(level.value)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # 错误日志文件（只记录ERROR及以上级别）- 同样按日期归档
            error_log_file = self.log_dir / f"{file_name_prefix}_error.log"
            error_handler = logging.handlers.TimedRotatingFileHandler(
                error_log_file,
                when='midnight',
                interval=1,
                backupCount=backup_count,
                encoding='utf-8'
            )
            # 设置归档文件后缀格式为 -YYYY-MM-DD
            error_handler.suffix = "-%Y-%m-%d"
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            logger.addHandler(error_handler)

        self._loggers[name] = logger
        return logger

    def set_level(self, name: str, level: LogLevel):
        """设置指定logger的日志级别"""
        if name in self._loggers:
            self._loggers[name].setLevel(level.value)
            for handler in self._loggers[name].handlers:
                if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.handlers.RotatingFileHandler):
                    handler.setLevel(level.value)
                elif isinstance(handler, logging.handlers.RotatingFileHandler) and 'error' not in str(handler.baseFilename):
                    handler.setLevel(level.value)

    def add_json_handler(self, name: str, json_log_file: Optional[str] = None):
        """为指定logger添加JSON格式处理器"""
        if name not in self._loggers:
            return

        import json

        logger = self._loggers[name]

        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_entry = {
                    'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                    'level': record.levelname,
                    'logger': record.name,
                    'message': record.getMessage(),
                    'module': record.module,
                    'function': record.funcName,
                    'line': record.lineno
                }

                if record.exc_info:
                    log_entry['exception'] = self.formatException(record.exc_info)

                return json.dumps(log_entry, ensure_ascii=False)

        json_file = json_log_file or str(self.log_dir / f"{name}_json.log")
        json_handler = logging.handlers.TimedRotatingFileHandler(
            json_file,
            when='midnight',
            interval=1,
            backupCount=5,
            encoding='utf-8'
        )
        # 设置归档文件后缀格式为 -YYYY-MM-DD
        json_handler.suffix = "-%Y-%m-%d"
        json_handler.setFormatter(JSONFormatter())
        logger.addHandler(json_handler)


class LoggerMixin:
    """日志混入类，为其他类提供日志功能"""

    @property
    def logger(self) -> logging.Logger:
        """获取当前类的logger"""
        if not hasattr(self, '_logger'):
            class_name = self.__class__.__name__.lower()
            self._logger = get_logger(class_name)
        return self._logger


def get_logger(
    name: str ,
    level: LogLevel = LogLevel.INFO,
    console_output: bool = True,
    file_output: bool = True,
    file_prefix: str = "chat-quant"
) -> logging.Logger:
    """
    便捷函数：获取logger实例

    Args:
        name: logger名称（显示在日志内容中）
        level: 日志级别
        console_output: 是否输出到控制台
        file_output: 是否输出到文件
        file_prefix: 日志文件名前缀，如果不指定则使用name

    Returns:
        logging.Logger: 配置好的logger实例
    """
    logger_manager = Logger()
    return logger_manager.get_logger(name, level, console_output, file_output, file_prefix=file_prefix)


def set_global_level(level: LogLevel):
    """设置全局日志级别"""
    logging.getLogger().setLevel(level.value)


def log_function_call(func):
    """函数调用日志装饰器"""
    def wrapper(*args, **kwargs):
        func_logger = get_logger(f"function.{func.__name__}")
        func_logger.debug(f"调用函数 {func.__name__}, args: {args}, kwargs: {kwargs}")

        try:
            result = func(*args, **kwargs)
            func_logger.debug(f"函数 {func.__name__} 执行成功")
            return result
        except Exception as e:
            func_logger.error(f"函数 {func.__name__} 执行失败: {str(e)}", exc_info=True)
            raise

    return wrapper


def log_execution_time(func):
    """执行时间日志装饰器"""
    import time

    def wrapper(*args, **kwargs):
        func_logger = get_logger(f"performance.{func.__name__}")
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            func_logger.info(f"函数 {func.__name__} 执行时间: {execution_time:.4f}秒")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            func_logger.error(f"函数 {func.__name__} 执行失败 (耗时: {execution_time:.4f}秒): {str(e)}")
            raise

    return wrapper


class ContextLogger:
    """上下文日志记录器"""

    def __init__(self, logger_name: str, context: str):
        self.logger = get_logger(logger_name)
        self.context = context

    def __enter__(self):
        self.logger.info(f"开始 {self.context}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.logger.info(f"完成 {self.context}")
        else:
            self.logger.error(f"执行 {self.context} 时出错: {exc_val}", exc_info=True)

    def info(self, message: str):
        self.logger.info(f"[{self.context}] {message}")

    def debug(self, message: str):
        self.logger.debug(f"[{self.context}] {message}")

    def warning(self, message: str):
        self.logger.warning(f"[{self.context}] {message}")

    def error(self, message: str):
        self.logger.error(f"[{self.context}] {message}")


def create_context_logger(logger_name: str, context: str) -> ContextLogger:
    """创建上下文日志记录器"""
    return ContextLogger(logger_name, context)