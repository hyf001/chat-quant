# 用户授权 API 文档

## 目录

- [概述](#概述)
- [核心功能](#核心功能)
- [API 端点摘要](#api-端点摘要)
- [API 端点详情](#api-端点详情)
  - [1. 添加授权用户](#1-添加授权用户)
  - [2. 检查用户权限](#2-检查用户权限)
  - [3. 获取授权用户列表](#3-获取授权用户列表)
  - [4. 获取单个授权用户](#4-获取单个授权用户)
  - [5. 更新授权用户](#5-更新授权用户)
  - [6. 删除授权用户](#6-删除授权用户)
- [依赖函数](#依赖函数)
- [数据库模型](#数据库模型)
- [证书格式说明](#证书格式说明)
- [测试](#测试)
- [实现文件](#实现文件)
- [快速开始](#快速开始)
- [常见问题 (FAQ)](#常见问题-faq)
- [注意事项](#注意事项)

---

## 概述

本文档描述了用户授权管理系统的 API 接口。系统通过客户端证书（从请求头 `kyc_client_cert` 获取）来验证用户权限。

## 核心功能

1. **证书指纹解析**：从客户端证书中提取 MD5 指纹
2. **权限验证**：验证用户是否有权限访问系统
3. **授权用户管理**：增删改查授权用户信息

## API 端点摘要

| 方法 | 端点 | 描述 | 需要授权 |
|------|------|------|----------|
| POST | `/api/auth/users` | 添加授权用户 | 否 |
| GET | `/api/auth/check` | 检查用户权限 | 否 |
| GET | `/api/auth/users` | 获取授权用户列表 | 否 |
| GET | `/api/auth/users/{cert_fingerprint}` | 获取单个授权用户 | 否 |
| PATCH | `/api/auth/users/{cert_fingerprint}` | 更新授权用户信息 | 否 |
| DELETE | `/api/auth/users/{cert_fingerprint}` | 删除授权用户 | 否 |

**注意**: 这些接口本身不需要授权，因为它们用于管理授权用户。在生产环境中，建议添加管理员权限验证。

---

## API 端点详情

### 1. 添加授权用户

**端点**: `POST /api/auth/users`

**描述**: 添加新的授权用户，传入证书指纹并存储到数据库

**请求体**:
```json
{
  "cert_fingerprint": "8E0A8FC9011CEFE1AFD0B41FA60175FF",
  "user_name": "张三",
  "user_email": "zhangsan@example.com",
  "remark": "测试用户"
}
```

**字段说明**:
- `cert_fingerprint` (必填): 证书指纹，32位大写MD5哈希值
- `user_name` (可选): 用户名称
- `user_email` (可选): 用户邮箱
- `remark` (可选): 备注信息

**响应** (201 Created):
```json
{
  "cert_fingerprint": "8E0A8FC9011CEFE1AFD0B41FA60175FF",
  "user_name": "张三",
  "user_email": "zhangsan@example.com",
  "is_active": true,
  "remark": "测试用户",
  "created_at": "2025-10-21T09:30:01.828246",
  "updated_at": "2025-10-21T09:30:01.828255"
}
```

**错误响应**:
- `400 Bad Request`: 证书指纹格式无效（必须是32位十六进制字符串）
- `409 Conflict`: 证书指纹已存在
- `500 Internal Server Error`: 数据库操作失败

---

### 2. 检查用户权限

**端点**: `GET /api/auth/check`

**描述**: 检查当前用户是否有权限使用系统

**请求头**:
```
kyc_client_cert: -----BEGIN CERTIFICATE-----\nMIID...\n-----END CERTIFICATE-----
```

**注意**:
- 证书可以使用 `\n` 转义换行符，或者直接去掉换行符
- 两种格式都支持：
  - `-----BEGIN CERTIFICATE-----\nMIID...\n-----END CERTIFICATE-----`
  - `-----BEGIN CERTIFICATE-----MIID...-----END CERTIFICATE-----`

**响应** (200 OK):
```json
{
  "authorized": true,
  "cert_fingerprint": "973C8B9F079CB848216D0537950F35C3",
  "user_name": "张三",
  "message": "用户已授权"
}
```

**未授权响应**:
```json
{
  "authorized": false,
  "cert_fingerprint": "ABCD1234...",
  "user_name": null,
  "message": "用户未授权或已被禁用"
}
```

---

### 3. 获取授权用户列表

**端点**: `GET /api/auth/users`

**描述**: 获取所有授权用户列表（支持分页和过滤）

**查询参数**:
- `skip` (int, 可选): 跳过的记录数，默认 0
- `limit` (int, 可选): 返回的记录数，默认 100
- `is_active` (bool, 可选): 过滤激活状态

**示例**: `GET /api/auth/users?is_active=true&limit=10`

**响应** (200 OK):
```json
[
  {
    "cert_fingerprint": "973C8B9F079CB848216D0537950F35C3",
    "user_name": "张三",
    "user_email": "zhangsan@example.com",
    "is_active": true,
    "remark": "测试用户",
    "created_at": "2025-10-21T09:30:01.828246",
    "updated_at": "2025-10-21T09:30:01.828255"
  }
]
```

---

### 4. 获取单个授权用户

**端点**: `GET /api/auth/users/{cert_fingerprint}`

**描述**: 根据证书指纹获取单个授权用户信息

**路径参数**:
- `cert_fingerprint` (string): 证书指纹（32位大写十六进制字符串）

**示例**: `GET /api/auth/users/973C8B9F079CB848216D0537950F35C3`

**响应** (200 OK):
```json
{
  "cert_fingerprint": "973C8B9F079CB848216D0537950F35C3",
  "user_name": "张三",
  "user_email": "zhangsan@example.com",
  "is_active": true,
  "remark": "测试用户",
  "created_at": "2025-10-21T09:30:01.828246",
  "updated_at": "2025-10-21T09:30:01.828255"
}
```

**错误响应**:
- `404 Not Found`: 用户不存在

---

### 5. 更新授权用户

**端点**: `PATCH /api/auth/users/{cert_fingerprint}`

**描述**: 更新授权用户信息

**路径参数**:
- `cert_fingerprint` (string): 证书指纹

**请求体** (所有字段可选):
```json
{
  "user_name": "更新后的名称",
  "user_email": "newemail@example.com",
  "is_active": false,
  "remark": "已更新"
}
```

**响应** (200 OK):
```json
{
  "cert_fingerprint": "973C8B9F079CB848216D0537950F35C3",
  "user_name": "更新后的名称",
  "user_email": "newemail@example.com",
  "is_active": false,
  "remark": "已更新",
  "created_at": "2025-10-21T09:30:01.828246",
  "updated_at": "2025-10-21T09:45:00.123456"
}
```

**错误响应**:
- `404 Not Found`: 用户不存在
- `500 Internal Server Error`: 数据库操作失败

---

### 6. 删除授权用户

**端点**: `DELETE /api/auth/users/{cert_fingerprint}`

**描述**: 删除授权用户

**路径参数**:
- `cert_fingerprint` (string): 证书指纹

**响应**: `204 No Content`

**错误响应**:
- `404 Not Found`: 用户不存在
- `500 Internal Server Error`: 数据库操作失败

---

## 依赖函数

### verify_user_authorization

用于保护需要权限验证的接口。

**使用示例**:
```python
from fastapi import Depends
from app.api.deps import verify_user_authorization

@router.get("/protected")
async def protected_endpoint(
    cert_fingerprint: str = Depends(verify_user_authorization)
):
    return {"message": "访问成功", "fingerprint": cert_fingerprint}
```

**功能**:
- 从请求头 `kyc_client_cert` 获取证书
- 解析证书指纹
- 验证用户是否在授权列表中
- 验证用户是否处于激活状态

**异常**:
- `401 Unauthorized`: 证书缺失或格式无效
- `403 Forbidden`: 用户未授权

---

## 数据库模型

### AuthorizedUser

**表名**: `authorized_users`

**字段**:
- `cert_fingerprint` (String, PK): 证书指纹（32位大写 MD5 哈希）
- `user_name` (String, 可空): 用户名称
- `user_email` (String, 可空): 用户邮箱
- `is_active` (Boolean): 是否启用
- `remark` (String, 可空): 备注信息
- `created_at` (DateTime): 创建时间
- `updated_at` (DateTime): 更新时间

---

## 证书格式说明

### 标准 PEM 格式
```
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAKJ5CqF5gvQGMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMjAwMTAxMDAwMDAwWhcNMzAwMTAxMDAwMDAwWjBF
MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50
ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAw5zJQKJ7LQaXFGXPgHvvR6xE+gMH3Y7FZ7mKRXx5bBHxGcXVvyEqZxYV
2KqLbR3dVQZWHSVkKJNXQdvmEEv3RpwqCJhEcw0H9fLVlV+VpPSMYWmXQNvmJC0L
-----END CERTIFICATE-----
```

### HTTP 头部格式（使用 \n 转义）
```
kyc_client_cert: -----BEGIN CERTIFICATE-----\nMIIDXTC...\n-----END CERTIFICATE-----
```

### HTTP 头部格式（去掉换行符）
```
kyc_client_cert: -----BEGIN CERTIFICATE-----MIIDXTC...-----END CERTIFICATE-----
```

---

## 测试

使用提供的测试脚本验证接口：

```bash
# 运行完整测试
python test_auth_api.py

# 运行调试测试
python debug_test.py
```

---

## 实现文件

- **模型**: `apps/api/app/models/authorized_users.py`
- **工具函数**: `apps/api/app/utils/cert_utils.py`
- **依赖**: `apps/api/app/api/deps.py`
- **路由**: `apps/api/app/api/auth.py`
- **主应用**: `apps/api/app/main.py`

---

## 快速开始

### 1. 添加授权用户

```bash
curl -X POST http://localhost:8080/api/auth/users \
  -H "Content-Type: application/json" \
  -d '{
    "cert_fingerprint": "8E0A8FC9011CEFE1AFD0B41FA60175FF",
    "user_name": "测试用户",
    "user_email": "test@example.com",
    "remark": "开发测试"
  }'
```

### 2. 检查权限

```bash
curl -X GET http://localhost:8080/api/auth/check \
  -H "kyc_client_cert: -----BEGIN CERTIFICATE-----\nMIID...\n-----END CERTIFICATE-----"
```

### 3. 查看所有授权用户

```bash
curl -X GET http://localhost:8080/api/auth/users
```

### 4. 更新用户状态（禁用用户）

```bash
curl -X PATCH http://localhost:8080/api/auth/users/8E0A8FC9011CEFE1AFD0B41FA60175FF \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

---

## 常见问题 (FAQ)

### Q1: 如何获取证书指纹？

使用工具函数 `get_md5_cert()` 从完整证书中提取指纹：

```python
from app.utils.cert_utils import get_md5_cert

cert_pem = """-----BEGIN CERTIFICATE-----
MIID...
-----END CERTIFICATE-----"""

fingerprint = get_md5_cert(cert_pem)
print(fingerprint)  # 输出: 8E0A8FC9011CEFE1AFD0B41FA60175FF
```

或使用 OpenSSL 命令行：

```bash
openssl x509 -in certificate.pem -noout -fingerprint -md5 | \
  sed 's/://g' | \
  awk -F= '{print toupper($2)}'
```

### Q2: 为什么权限检查返回 "用户未授权"？

可能的原因：
1. 证书指纹不在授权列表中
2. 用户被禁用 (`is_active=false`)
3. 证书格式解析失败
4. 请求头名称错误（应该是 `kyc_client_cert`）

### Q3: 如何在其他接口中使用权限验证？

使用 `verify_user_authorization` 依赖：

```python
from fastapi import APIRouter, Depends
from app.api.deps import verify_user_authorization

router = APIRouter()

@router.get("/protected")
async def protected_route(
    cert_fingerprint: str = Depends(verify_user_authorization)
):
    return {"message": "访问成功", "user": cert_fingerprint}
```

### Q4: 生产环境如何部署？

1. 使用 PostgreSQL 替代 SQLite
2. 配置环境变量 `DATABASE_URL`
3. 使用 HTTPS 协议
4. 配置反向代理（Nginx）处理证书认证
5. 设置适当的 CORS 策略

---

## 注意事项

1. **证书指纹计算**：使用 MD5 哈希算法，与 CRM 统计平台保持一致
2. **HTTP 头部名称**：使用 `kyc_client_cert`（连字符），不是 `kyc_client_cert`（下划线）
3. **证书格式兼容性**：支持带换行符和不带换行符两种格式
4. **权限验证**：只有 `is_active=true` 的用户才能通过权限验证
5. **数据库**：开发环境使用 SQLite，生产环境可使用 PostgreSQL
6. **安全性**：建议在生产环境使用 HTTPS 和真实的 SSL/TLS 客户端证书认证
