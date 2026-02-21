# Technical Context (技术上下文)

**类型**: T1 (System Axioms)
**版本**: v1.8.0
**用途**: 定义核心接口签名与技术栈约束 (Tier 2 验证依据)

---

## 1. 技术栈清单 (Tech Stack)

| 层级 | 技术选型 | 约束说明 |
|------|----------|----------|
| **Language** | Python 3.10+ / TypeScript 5.0+ | 禁止使用实验性特性 |
| **Backend** | FastAPI 0.109+ / Node.js 20+ | 必须启用类型检查 |
| **Frontend** | React 18+ / Vue 3+ | 使用函数式组件 |
| **Database** | PostgreSQL 15+ / Redis 7+ | 禁止直接拼接 SQL |
| **ORM** | SQLAlchemy 2.0 / Prisma | 使用异步查询 |
| **Testing** | pytest 8.0+ / Jest 29+ | 覆盖率 > 80% |

---

## 2. 核心接口签名 (Core Interfaces)

**Tier 2 验证规则**: 代码中的实现必须包含以下签名。

### 2.1 用户模块

```python
from typing import Protocol, Optional
from datetime import datetime
import uuid

class IUserRepository(Protocol):
    """用户数据访问接口"""
    def find_by_id(self, user_id: uuid.UUID) -> Optional['User']: ...
    def find_by_email(self, email: str) -> Optional['User']: ...
    def create(self, user: 'UserCreate') -> 'User': ...
    def update(self, user_id: uuid.UUID, data: dict) -> 'User': ...
    def delete(self, user_id: uuid.UUID) -> bool: ...

class IUserService(Protocol):
    """用户业务服务接口"""
    def get_user(self, user_id: uuid.UUID) -> Optional['User']: ...
    def create_user(self, user: 'UserCreate') -> 'User': ...
    def authenticate(self, email: str, password: str) -> Optional['User']: ...
    def update_profile(self, user_id: uuid.UUID, profile: 'ProfileUpdate') -> 'User': ...

```

### 2.2 订单模块

```typescript
interface IOrderService {
  // 创建订单
  createOrder(order: OrderCreate): Promise<OrderResult>;
  
  // 验证库存
  validateInventory(items: Item[]): Promise<boolean>;
  
  // 计算总价
  calculateTotal(items: Item[], coupon?: Coupon): Promise<decimal>;
  
  // 订单状态流转
  updateStatus(orderId: string, newStatus: OrderStatus): Promise<Order>;
}

interface IPaymentService {
  // 发起支付
  initiatePayment(orderId: string, amount: decimal): Promise<PaymentResult>;
  
  // 验证支付
  verifyPayment(paymentId: string): Promise<boolean>;
  
  // 退款
  refund(paymentId: string, reason: string): Promise<RefundResult>;
}

```

---

## 3. 数据契约 (Data Contracts)

### 3.1 核心实体定义

```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class User(BaseModel):
    """用户核心实体"""
    id: uuid.UUID
    email: EmailStr
    username: str
    role: 'UserRole'
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    """用户创建请求"""
    email: EmailStr
    username: str
    password: str  # 最小8位，包含字母数字
    role: Optional['UserRole'] = 'USER'

class Order(BaseModel):
    """订单核心实体"""
    id: uuid.UUID
    user_id: uuid.UUID
    total: float
    status: 'OrderStatus'
    items: list['OrderItem']
    created_at: datetime
    paid_at: Optional[datetime]
```

### 3.2 枚举定义

```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    GUEST = "GUEST"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
```

---

## 4. API 规范 (REST API)

### 4.1 响应格式标准

```typescript
// 统一 API 响应格式
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
  meta?: {
    timestamp: string;
    request_id: string;
  };
}

// 分页响应
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
```

### 4.2 错误码规范

| 错误码 | 说明 | HTTP状态码 |
|--------|------|------------|
| ERR_001 | 参数验证失败 | 400 |
| ERR_002 | 资源不存在 | 404 |
| ERR_003 | 权限不足 | 403 |
| ERR_004 | 认证失败 | 401 |
| ERR_005 | 系统内部错误 | 500 |

---

## 5. Tier 2 验证检查清单

```bash
# 验证命令: 检查接口实现完整性
grep -r "def.*(" src/ --include="*.py" | \
  grep -v "test_" | \
  grep -v "__" > impl_signatures.txt
  
# 手动对比 impl_signatures.txt 与 techContext.md 中的接口定义
```

| 检查项 | 验证方法 | 通过标准 |
|--------|----------|----------|
| 接口实现 | 代码扫描 | 每个接口方法都有对应实现 |
| 签名一致 | 手动对比 | 参数类型、返回值类型完全匹配 |
| 数据契约 | JSON Schema 验证 | 字段类型完全一致 |

---

**宪法依据**: §103§105
**最后更新**: {{TIMESTAMP}}
**版本**: v1.8.0
