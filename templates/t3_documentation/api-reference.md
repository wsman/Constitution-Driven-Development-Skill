# {{PROJECT_NAME}} API 参考文档

> **版本**: 1.0.0  
> **最后更新**: {{TIMESTAMP}}  
> **类别**: API 文档  
> **目标读者**: API 消费者、开发者

## 📚 API 概览

{{PROJECT_NAME}} 提供 RESTful API 接口，支持 JSON 格式的数据交换。

### 基础信息
- **Base URL**: `https://api.example.com/v1` (生产环境)
- **开发环境**: `http://localhost:8000/v1`
- **内容类型**: `application/json`
- **认证方式**: Bearer Token / API Key

### 状态码
| 状态码 | 描述 | 说明 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 认证失败 |
| 403 | Forbidden | 权限不足 |
| 404 | Not Found | 资源不存在 |
| 429 | Too Many Requests | 请求频率限制 |
| 500 | Internal Server Error | 服务器内部错误 |

## 🔐 认证与授权

### 获取访问令牌
```http
POST /auth/token
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**响应**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "def50200aecc12a..."
}
```

### 使用 API Key
```http
GET /api/resource
Authorization: Api-Key your-api-key-here
```

## 📋 API 端点

### 用户管理

#### 获取用户列表
```http
GET /users
Authorization: Bearer <token>
```

**查询参数**:
| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| page | integer | 否 | 页码，默认 1 |
| limit | integer | 否 | 每页数量，默认 20 |
| sort | string | 否 | 排序字段 |
| order | string | 否 | 排序方向 (asc/desc) |

**响应**:
```json
{
  "data": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

#### 创建用户
```http
POST /users
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "new_user",
  "email": "user@example.com",
  "password": "secure_password"
}
```

#### 获取单个用户
```http
GET /users/{id}
Authorization: Bearer <token>
```

#### 更新用户
```http
PUT /users/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "updated@example.com"
}
```

#### 删除用户
```http
DELETE /users/{id}
Authorization: Bearer <token>
```

### 产品管理

#### 获取产品列表
```http
GET /products
```

#### 创建产品
```http
POST /products
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "产品名称",
  "description": "产品描述",
  "price": 99.99,
  "stock": 100
}
```

### 订单管理

#### 创建订单
```http
POST /orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2,
  "shipping_address": "收货地址"
}
```

#### 获取订单状态
```http
GET /orders/{id}/status
Authorization: Bearer <token>
```

## 🔄 WebSocket 端点

### 实时通知
```javascript
// 连接 WebSocket
const ws = new WebSocket('wss://api.example.com/ws/notifications');

// 发送认证消息
ws.onopen = () => {
  ws.send(JSON.stringify({
    "type": "auth",
    "token": "your_jwt_token"
  }));
};

// 接收消息
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('收到通知:', data);
};
```

### 事件类型
| 事件类型 | 描述 | 数据格式 |
|----------|------|----------|
| notification | 系统通知 | `{type: "notification", data: {...}}` |
| order_update | 订单更新 | `{type: "order_update", order_id: 123, status: "shipped"}` |
| chat_message | 聊天消息 | `{type: "chat_message", from: "user1", message: "hello"}` |

## 📊 数据模型

### 用户模型
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "status": "string (active/inactive)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 产品模型
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "price": "decimal",
  "stock": "integer",
  "category_id": "integer",
  "created_at": "datetime"
}
```

### 订单模型
```json
{
  "id": "integer",
  "user_id": "integer",
  "total_amount": "decimal",
  "status": "string (pending/paid/shipped/delivered/cancelled)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🛡️ 速率限制

### 限制规则
| 端点 | 限制 | 周期 |
|------|------|------|
| 认证端点 | 10 次 | 每分钟 |
| 公开 API | 100 次 | 每小时 |
| 认证用户 | 1000 次 | 每天 |
| 管理员 | 5000 次 | 每天 |

### 响应头信息
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1640995200
```

## 🔧 错误处理

### 错误响应格式
```json
{
  "error": {
    "code": "validation_error",
    "message": "输入验证失败",
    "details": {
      "email": ["邮箱格式不正确"],
      "password": ["密码长度至少8位"]
    },
    "timestamp": "2024-01-01T00:00:00Z",
    "request_id": "req_123456789"
  }
}
```

### 常见错误码
| 错误码 | 描述 | 解决方案 |
|--------|------|----------|
| invalid_token | 令牌无效 | 重新获取访问令牌 |
| insufficient_permission | 权限不足 | 检查用户角色和权限 |
| resource_not_found | 资源不存在 | 检查资源ID是否正确 |
| validation_error | 验证失败 | 检查请求参数格式 |

## 📝 代码示例

### Python 示例
```python
import requests

# 获取访问令牌
response = requests.post(
    "https://api.example.com/auth/token",
    json={"username": "user", "password": "pass"}
)
token = response.json()["access_token"]

# 调用 API
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("https://api.example.com/api/users", headers=headers)
users = response.json()
```

### JavaScript 示例
```javascript
// 使用 fetch API
const response = await fetch('https://api.example.com/api/products', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});
const products = await response.json();
```

### cURL 示例
```bash
# 获取令牌
curl -X POST https://api.example.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'

# 调用 API
curl -H "Authorization: Bearer <token>" \
  https://api.example.com/api/users
```

## 🧪 测试端点

### 健康检查
```http
GET /health
```

**响应**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "cache": "connected",
    "queue": "connected"
  }
}
```

### 版本信息
```http
GET /version
```

## 🔗 相关资源

- **Swagger UI**: `/docs` (开发环境)
- **ReDoc**: `/redoc` (开发环境)
- **OpenAPI 规范**: `/openapi.json`
- **API 状态页面**: https://status.example.com

## 📋 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | {{TIMESTAMP}} | 初始 API 版本 |

---

**API 版本**: v1.0.0  
**认证方式**: Bearer Token / API Key  
**速率限制**: 已启用  
**文档状态**: ✅ 完整

*文档版本: v1.0.0 | 更新日期: {{TIMESTAMP}}*
