from sqlalchemy.orm import Session
from fastapi import Header, HTTPException, Depends, Request
from typing import Annotated
import logging

from app.db.session import SessionLocal
from app.models.authorized_users import AuthorizedUser
from app.utils.cert_utils import get_md5_cert

logger = logging.getLogger(__name__)


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def verify_user_authorization(
    request: Request,
    db: Session = Depends(get_db)
) -> str:
    """
    验证用户是否有权限访问系统
    从请求头中获取证书并验证
    支持以下请求头格式：
    - kyc-client-cert (推荐，HTTP标准)
    - kyc_client_cert (兼容格式)
    - Kyc-Client-Cert (大小写不敏感)

    Args:
        request: FastAPI 请求对象
        db: 数据库会话

    Returns:
        证书指纹（如果验证通过）

    Raises:
        HTTPException: 如果证书无效或用户未授权
    """
    # 尝试从不同格式的请求头中获取证书
    # HTTP 标准使用连字符，但有些中间件可能使用下划线
    kyc_client_cert = (
        request.headers.get("kyc-client-cert") or
        request.headers.get("kyc_client_cert") or
        request.headers.get("Kyc-Client-Cert")
    )

    # 检查证书是否存在
    if not kyc_client_cert:
        logger.warning("Request without kyc_client_cert header")
        raise HTTPException(
            status_code=401,
            detail="客户端证书缺失，请提供有效的证书"
        )

    # 解析证书指纹
    cert_fingerprint = get_md5_cert(kyc_client_cert)

    if not cert_fingerprint:
        logger.warning("Failed to parse certificate")
        raise HTTPException(
            status_code=401,
            detail="证书格式无效，无法解析"
        )

    # 查询数据库验证权限
    authorized_user = db.query(AuthorizedUser).filter(
        AuthorizedUser.cert_fingerprint == cert_fingerprint,
        AuthorizedUser.is_active == True
    ).first()

    if not authorized_user:
        logger.warning(f"Unauthorized access attempt with fingerprint: {cert_fingerprint}")
        raise HTTPException(
            status_code=403,
            detail="您没有权限访问此系统，请联系管理员"
        )

    logger.info(f"User authorized: {authorized_user.user_name or cert_fingerprint}")
    return cert_fingerprint


async def get_current_cert_fingerprint(
    request: Request
) -> str | None:
    """
    获取当前请求的证书指纹（不验证权限）
    用于管理接口等不需要权限验证的场景
    支持以下请求头格式：
    - kyc-client-cert (推荐，HTTP标准)
    - kyc_client_cert (兼容格式)
    - Kyc-Client-Cert (大小写不敏感)

    Args:
        request: FastAPI 请求对象

    Returns:
        证书指纹，如果证书不存在或解析失败则返回 None
    """
    # 尝试从不同格式的请求头中获取证书
    kyc_client_cert = (
        request.headers.get("kyc-client-cert") or
        request.headers.get("kyc_client_cert") or
        request.headers.get("Kyc-Client-Cert")
    )

    if not kyc_client_cert:
        return None

    return get_md5_cert(kyc_client_cert)
