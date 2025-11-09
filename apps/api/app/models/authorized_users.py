from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base


class AuthorizedUser(Base):
    """授权用户模型 - 存储有权限使用系统的用户证书指纹"""
    __tablename__ = "authorized_users"

    # 证书指纹作为主键 (32位MD5哈希值的大写字符串)
    cert_fingerprint: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)

    # 用户标识信息（可选）
    user_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # 是否启用
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # 备注信息
    remark: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<AuthorizedUser(cert_fingerprint={self.cert_fingerprint!r}, user_name={self.user_name!r}, is_active={self.is_active})>"
