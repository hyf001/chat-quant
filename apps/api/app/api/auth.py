"""
用户授权管理 API 接口
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import logging

from app.api.deps import get_db, verify_user_authorization, get_current_cert_fingerprint
from app.models.authorized_users import AuthorizedUser

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])


# Pydantic 模型定义
class AuthorizedUserCreate(BaseModel):
    """添加授权用户的请求体"""
    cert_fingerprint: str = Field(..., description="证书指纹（32位大写MD5哈希）", min_length=32, max_length=32)
    user_name: Optional[str] = Field(None, description="用户名称")
    user_email: Optional[str] = Field(None, description="用户邮箱")
    remark: Optional[str] = Field(None, description="备注信息")

    class Config:
        json_schema_extra = {
            "example": {
                "cert_fingerprint": "8E0A8FC9011CEFE1AFD0B41FA60175FF",
                "user_name": "张三",
                "user_email": "zhangsan@example.com",
                "remark": "测试用户"
            }
        }


class AuthorizedUserUpdate(BaseModel):
    """更新授权用户的请求体"""
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    is_active: Optional[bool] = None
    remark: Optional[str] = None


class AuthorizedUserResponse(BaseModel):
    """授权用户响应"""
    cert_fingerprint: str
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    is_active: bool
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AuthCheckResponse(BaseModel):
    """权限检查响应"""
    authorized: bool
    cert_fingerprint: Optional[str] = None
    user_name: Optional[str] = None
    message: str


# API 路由
@router.post("/users", response_model=AuthorizedUserResponse, status_code=201)
async def add_authorized_user(
    body: AuthorizedUserCreate,
    db: Session = Depends(get_db)
):
    """
    添加授权用户

    传入证书指纹并存储到数据库中
    """
    # 验证证书指纹格式（32位大写十六进制）
    cert_fingerprint = body.cert_fingerprint.upper()
    if not all(c in '0123456789ABCDEF' for c in cert_fingerprint):
        raise HTTPException(
            status_code=400,
            detail="证书指纹格式无效，必须是32位十六进制字符串"
        )

    # 检查是否已存在
    existing_user = db.query(AuthorizedUser).filter(
        AuthorizedUser.cert_fingerprint == cert_fingerprint
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail=f"该证书指纹已存在: {cert_fingerprint}"
        )

    # 创建新的授权用户
    try:
        new_user = AuthorizedUser(
            cert_fingerprint=cert_fingerprint,
            user_name=body.user_name,
            user_email=body.user_email,
            remark=body.remark,
            is_active=True
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"Added authorized user: {cert_fingerprint} ({body.user_name})")

        return new_user

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add authorized user: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"添加授权用户失败: {str(e)}"
        )


@router.get("/check", response_model=AuthCheckResponse)
async def check_user_permission(
    cert_fingerprint: str = Depends(get_current_cert_fingerprint),
    db: Session = Depends(get_db)
):
    """
    检查当前用户是否有权限使用系统

    从请求头 kyc_client_cert 中获取证书并验证权限
    """
    # 如果没有提供证书
    if not cert_fingerprint:
        return AuthCheckResponse(
            authorized=False,
            cert_fingerprint=None,
            user_name=None,
            message="未提供客户端证书"
        )

    # 查询数据库
    authorized_user = db.query(AuthorizedUser).filter(
        AuthorizedUser.cert_fingerprint == cert_fingerprint,
        AuthorizedUser.is_active == True
    ).first()

    if authorized_user:
        return AuthCheckResponse(
            authorized=True,
            cert_fingerprint=cert_fingerprint,
            user_name=authorized_user.user_name,
            message="用户已授权"
        )
    else:
        return AuthCheckResponse(
            authorized=False,
            cert_fingerprint=cert_fingerprint,
            user_name=None,
            message="用户未授权或已被禁用"
        )


@router.get("/users", response_model=List[AuthorizedUserResponse])
async def list_authorized_users(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    获取授权用户列表

    支持分页和按状态过滤
    """
    query = db.query(AuthorizedUser)

    if is_active is not None:
        query = query.filter(AuthorizedUser.is_active == is_active)

    users = query.offset(skip).limit(limit).all()
    return users


@router.get("/users/{cert_fingerprint}", response_model=AuthorizedUserResponse)
async def get_authorized_user(
    cert_fingerprint: str,
    db: Session = Depends(get_db)
):
    """
    获取指定授权用户信息
    """
    user = db.query(AuthorizedUser).filter(
        AuthorizedUser.cert_fingerprint == cert_fingerprint
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"未找到证书指纹为 {cert_fingerprint} 的授权用户"
        )

    return user


@router.patch("/users/{cert_fingerprint}", response_model=AuthorizedUserResponse)
async def update_authorized_user(
    cert_fingerprint: str,
    body: AuthorizedUserUpdate,
    db: Session = Depends(get_db)
):
    """
    更新授权用户信息
    """
    user = db.query(AuthorizedUser).filter(
        AuthorizedUser.cert_fingerprint == cert_fingerprint
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"未找到证书指纹为 {cert_fingerprint} 的授权用户"
        )

    # 更新字段
    try:
        if body.user_name is not None:
            user.user_name = body.user_name
        if body.user_email is not None:
            user.user_email = body.user_email
        if body.is_active is not None:
            user.is_active = body.is_active
        if body.remark is not None:
            user.remark = body.remark

        db.commit()
        db.refresh(user)

        logger.info(f"Updated authorized user: {cert_fingerprint}")

        return user

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update authorized user: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"更新授权用户失败: {str(e)}"
        )


@router.delete("/users/{cert_fingerprint}", status_code=204)
async def delete_authorized_user(
    cert_fingerprint: str,
    db: Session = Depends(get_db)
):
    """
    删除授权用户
    """
    user = db.query(AuthorizedUser).filter(
        AuthorizedUser.cert_fingerprint == cert_fingerprint
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"未找到证书指纹为 {cert_fingerprint} 的授权用户"
        )

    try:
        db.delete(user)
        db.commit()

        logger.info(f"Deleted authorized user: {cert_fingerprint}")

        return None

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete authorized user: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"删除授权用户失败: {str(e)}"
        )
