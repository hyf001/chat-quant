"""
AKShare 模块
提供 AKShare 接口文档加载和查询功能
"""

from .akshare_interface import AKShareInterfaceLoader, AKShareInvoker, InterfaceDetail, InterfaceParameter

__all__ = ['AKShareInterfaceLoader', 'InterfaceDetail', 'InterfaceParameter', 'get_akshare_loader']

_akshare_loader = None
_akshare_invoker = None


def get_akshare_loader() -> AKShareInterfaceLoader:
    """获取 AKShare 接口加载器单例"""
    global _akshare_loader
    if _akshare_loader is None:
        import os
        akshare_dir = os.path.dirname(__file__)
        md_path = os.path.join(akshare_dir, 'ak_share.md')
        _akshare_loader = AKShareInterfaceLoader(md_path)
    return _akshare_loader

def get_akshare_invoker() -> AKShareInvoker:
    """获取 AKShare invoker 加载器单例"""
    global _akshare_invoker
    if _akshare_invoker is None:
        _akshare_invoker = AKShareInvoker(get_akshare_loader())
    return _akshare_invoker