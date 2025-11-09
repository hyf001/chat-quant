"""
证书工具函数
用于解析和验证客户端证书指纹
"""
import base64
import hashlib
import logging

logger = logging.getLogger(__name__)


def get_md5_cert(cert: str | None) -> str | None:
    """
    获取证书指纹（MD5哈希值）
    与 CRM 统计平台保持一致的实现

    Args:
        cert: 证书字符串（PEM 格式）

    Returns:
        证书的 MD5 指纹（32位大写十六进制字符串），如果输入为空则返回 None

    Example:
        >>> cert = "-----BEGIN CERTIFICATE-----\\nMIID...\\n-----END CERTIFICATE-----"
        >>> fingerprint = get_md5_cert(cert)
        >>> print(fingerprint)  # 输出: "A1B2C3D4E5F6..."
    """
    if cert is None:
        return None

    try:
        # 清理证书字符串
        # 处理转义的换行符（HTTP 头部中可能使用 \\n）
        cert = cert.replace("\\n", "\n")
        # 去除真实的换行符
        cert = cert.replace("\n", "")
        # 去除 PEM 格式的开始和结束标记
        cert = cert.replace("-----BEGIN CERTIFICATE-----", "")
        cert = cert.replace("-----END CERTIFICATE-----", "")
        # 去除空格
        cert = cert.strip().replace(" ", "")

        # Base64 解码
        client_cert_bytes = base64.b64decode(cert)

        # 计算 MD5 指纹
        fingerprint = _cert_md5(client_cert_bytes)

        return fingerprint.upper()

    except Exception as e:
        logger.error(f"Failed to parse certificate: {e}")
        return None


def _cert_md5(cert_bytes: bytes) -> str:
    """
    计算证书字节数据的 MD5 哈希值

    Args:
        cert_bytes: 证书的字节数据

    Returns:
        MD5 哈希值的十六进制字符串
    """
    try:
        md5_hash = hashlib.md5()
        md5_hash.update(cert_bytes)

        # 将 MD5 摘要转换为十六进制字符串
        digest = md5_hash.digest()
        hex_string = ''.join(f'{b:02x}' for b in digest)

        return hex_string

    except Exception as e:
        logger.error(f"Failed to calculate MD5: {e}")
        return ""


def validate_cert_format(cert: str) -> bool:
    """
    验证证书格式是否正确

    Args:
        cert: 证书字符串

    Returns:
        True 如果格式正确，否则 False
    """
    if not cert:
        return False

    # 检查是否包含 PEM 格式的标记
    has_begin = "-----BEGIN CERTIFICATE-----" in cert
    has_end = "-----END CERTIFICATE-----" in cert

    return has_begin and has_end
