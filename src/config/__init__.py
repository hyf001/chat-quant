"""
配置模块初始化
"""

# AKShare 相关功能已移动到 src.akshare 模块
from src.akshare import get_akshare_invoker, InterfaceDetail, InterfaceParameter

__all__ = ['InterfaceDetail', 'InterfaceParameter', 'get_akshare_invoker']