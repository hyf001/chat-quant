"""
HTTPS双向认证(mTLS)客户端工具类

支持使用客户端证书进行HTTPS双向认证,兼容.p12和.pem格式证书。
主要用于调用需要客户端证书认证的API接口。

特性:
- 支持 .p12 (PKCS#12) 证书自动转换
- 支持 .pem 证书直接使用
- 异步HTTP请求(GET, POST, PUT, DELETE等)
- 自动重试机制
- 连接池管理
- 详细的错误处理

作者: Claude Code
日期: 2025-10-15
"""

import os
import ssl
import tempfile
import asyncio
from typing import Dict, Any, Optional, Union
from pathlib import Path

import aiohttp
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    Encoding,
    PrivateFormat,
    NoEncryption,
    pkcs12
)


class HttpsMtlsClient:
    """
    HTTPS双向认证客户端

    支持使用客户端证书进行SSL/TLS双向认证的HTTP客户端。
    自动处理.p12证书转换和SSL上下文配置。

    使用示例:
        ```python
        # 使用.p12证书
        client = HttpsMtlsClient(
            cert_path="D:/AppData/user@example.com.p12",
            cert_password="password123"
        )

        # 发起请求
        response = await client.get("https://api.example.com/v1/user/info")
        print(response)

        # 关闭客户端
        await client.close()
        ```
    """

    def __init__(
        self,
        cert_path: str,
        cert_password: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        verify_ssl: bool = True
    ):
        """
        初始化HTTPS双向认证客户端

        Args:
            cert_path: 证书文件路径,支持.p12或.pem格式
            cert_password: 证书密码
            base_url: 基础URL,如 "https://api.example.com"
            timeout: 请求超时时间(秒),默认30秒
            max_retries: 最大重试次数,默认3次
            verify_ssl: 是否验证服务器SSL证书,默认True
        """
        self.cert_path = Path(cert_path)
        self.cert_password = cert_password
        self.base_url = base_url.rstrip('/') if base_url else None
        self.timeout = timeout
        self.max_retries = max_retries
        self.verify_ssl = verify_ssl

        # 临时文件存储转换后的证书
        self.temp_cert_file = None
        self.temp_key_file = None

        # SSL上下文
        self.ssl_context = None

        # aiohttp session
        self.session: Optional[aiohttp.ClientSession] = None

        # 初始化SSL上下文
        self._init_ssl_context()

    def _init_ssl_context(self):
        """初始化SSL上下文"""
        # 检查证书文件是否存在
        if not self.cert_path.exists():
            raise FileNotFoundError(f"证书文件不存在: {self.cert_path}")

        # 根据证书类型进行处理
        if self.cert_path.suffix.lower() == '.p12':
            self._convert_p12_to_pem()
        elif self.cert_path.suffix.lower() in ['.pem', '.crt']:
            # PEM格式证书直接使用
            self.temp_cert_file = str(self.cert_path)
            # 假设私钥在同一个文件中,如果分开需要额外指定
            self.temp_key_file = str(self.cert_path)
        else:
            raise ValueError(f"不支持的证书格式: {self.cert_path.suffix}")

        # 创建SSL上下文
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

        # 降低安全级别以支持旧证书
        # SECLEVEL=0 允许使用弱密钥和弱哈希算法(MD5, SHA1等)
        # 这对于一些旧的企业证书是必要的
        try:
            self.ssl_context.set_ciphers('DEFAULT@SECLEVEL=0')
        except:
            # 如果设置失败,尝试使用默认密码套件
            try:
                self.ssl_context.set_ciphers('DEFAULT')
            except:
                pass

        # 默认验证模式
        self.ssl_context.check_hostname = True
        self.ssl_context.verify_mode = ssl.CERT_REQUIRED

        # 加载默认CA证书
        try:
            self.ssl_context.load_default_certs()
        except:
            pass

        # 加载客户端证书和私钥
        try:
            self.ssl_context.load_cert_chain(
                certfile=self.temp_cert_file,
                keyfile=self.temp_key_file
            )
        except Exception as e:
            raise RuntimeError(f"加载证书失败: {str(e)}")

        # 配置SSL验证
        if not self.verify_ssl:
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE

    def _convert_p12_to_pem(self):
        """
        将.p12证书转换为PEM格式

        使用cryptography库将PKCS#12格式的证书转换为PEM格式,
        分别提取公钥证书和私钥,保存到临时文件中。
        """
        try:
            # 读取.p12文件
            with open(self.cert_path, 'rb') as f:
                p12_data = f.read()

            # 解析.p12证书
            private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
                p12_data,
                self.cert_password.encode()
            )

            # 转换为PEM格式
            cert_pem = certificate.public_bytes(Encoding.PEM)
            key_pem = private_key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.PKCS8,
                encryption_algorithm=NoEncryption()
            )

            # 创建临时文件保存PEM证书
            cert_fd, cert_path = tempfile.mkstemp(suffix='.pem', prefix='cert_')
            key_fd, key_path = tempfile.mkstemp(suffix='.pem', prefix='key_')

            # 写入证书
            os.write(cert_fd, cert_pem)
            os.close(cert_fd)

            # 写入私钥
            os.write(key_fd, key_pem)
            os.close(key_fd)

            self.temp_cert_file = cert_path
            self.temp_key_file = key_path

        except Exception as e:
            raise RuntimeError(f"转换.p12证书失败: {str(e)}")

    async def _ensure_session(self):
        """确保session已创建"""
        if self.session is None or self.session.closed:
            # 创建TCP连接器
            connector = aiohttp.TCPConnector(
                ssl=self.ssl_context,
                limit=100,  # 连接池大小
                limit_per_host=30,
                ttl_dns_cache=300
            )

            # 创建session
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            )

    def _build_url(self, path: str) -> str:
        """
        构建完整URL

        Args:
            path: 路径或完整URL

        Returns:
            完整URL
        """
        if path.startswith('http://') or path.startswith('https://'):
            return path

        if self.base_url:
            # 确保路径以/开头
            if not path.startswith('/'):
                path = '/' + path
            return f"{self.base_url}{path}"

        raise ValueError("必须提供完整URL或设置base_url")

    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送HTTP请求

        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE等)
            url: 请求URL或路径
            headers: 请求头
            params: URL查询参数
            json: JSON请求体
            data: 表单数据或原始数据
            **kwargs: 其他aiohttp参数

        Returns:
            响应数据字典,包含status, headers, body等

        Raises:
            aiohttp.ClientError: 请求失败
        """
        await self._ensure_session()

        full_url = self._build_url(url)

        # 重试逻辑
        last_error = None
        for attempt in range(self.max_retries):
            try:
                async with self.session.request(
                    method=method,
                    url=full_url,
                    headers=headers,
                    params=params,
                    json=json,
                    data=data,
                    ssl=self.ssl_context,
                    **kwargs
                ) as response:
                    # 读取响应
                    response_body = await response.text()

                    # 尝试解析为JSON
                    try:
                        response_json = await response.json()
                    except:
                        response_json = None

                    return {
                        'status': response.status,
                        'status_text': response.reason,
                        'headers': dict(response.headers),
                        'body': response_body,
                        'json': response_json,
                        'ok': 200 <= response.status < 300,
                        'url': str(response.url)
                    }

            except aiohttp.ClientError as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    # 等待后重试
                    await asyncio.sleep(2 ** attempt)  # 指数退避
                    continue
                break

        # 所有重试都失败
        raise last_error or Exception("请求失败")

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送GET请求

        Args:
            url: 请求URL或路径
            headers: 请求头
            params: URL查询参数
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        return await self.request('GET', url, headers=headers, params=params, **kwargs)

    async def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送POST请求

        Args:
            url: 请求URL或路径
            headers: 请求头
            params: URL查询参数
            json: JSON请求体
            data: 表单数据
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        return await self.request('POST', url, headers=headers, params=params, json=json, data=data, **kwargs)

    async def put(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送PUT请求

        Args:
            url: 请求URL或路径
            headers: 请求头
            params: URL查询参数
            json: JSON请求体
            data: 表单数据
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        return await self.request('PUT', url, headers=headers, params=params, json=json, data=data, **kwargs)

    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送DELETE请求

        Args:
            url: 请求URL或路径
            headers: 请求头
            params: URL查询参数
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        return await self.request('DELETE', url, headers=headers, params=params, **kwargs)

    async def close(self):
        """关闭客户端并清理资源"""
        # 关闭session
        if self.session and not self.session.closed:
            await self.session.close()
            # 等待底层连接关闭
            await asyncio.sleep(0.250)

        # 删除临时证书文件
        if self.cert_path.suffix.lower() == '.p12':
            if self.temp_cert_file and os.path.exists(self.temp_cert_file):
                try:
                    os.remove(self.temp_cert_file)
                except:
                    pass

            if self.temp_key_file and os.path.exists(self.temp_key_file):
                try:
                    os.remove(self.temp_key_file)
                except:
                    pass

    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.close()


# ======================== 便捷函数 ========================

async def create_mtls_client(
    cert_path: str,
    cert_password: str,
    base_url: Optional[str] = None,
    **kwargs
) -> HttpsMtlsClient:
    """
    创建HTTPS双向认证客户端的便捷函数

    Args:
        cert_path: 证书文件路径
        cert_password: 证书密码
        base_url: 基础URL
        **kwargs: 其他配置参数

    Returns:
        配置好的HttpsMtlsClient实例
    """
    client = HttpsMtlsClient(
        cert_path=cert_path,
        cert_password=cert_password,
        base_url=base_url,
        **kwargs
    )
    await client._ensure_session()
    return client
