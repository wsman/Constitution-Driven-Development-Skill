# Behavior Context (行为上下文)

**类型**: T1 (System Axioms)
**版本**: v1.8.0
**用途**: 定义系统的运行时行为与业务断言 (Tier 3 验证依据)

---

## 1. 业务不变量 (Business Invariants)

> **公理 1**: 用户的余额不能为负数。
> **公理 2**: 已完成的订单不能被修改。
> **公理 3**: 每个订单必须有至少一个商品。
> **公理 4**: 订单金额必须与商品价格一致。

### 1.1 不变量验证规则

```python
class BusinessInvariantError(Exception):
    """业务不变量违反异常"""
    def __init__(self, invariant: str, details: str):
        self.invariant = invariant
        self.details = details
        super().__init__(f"业务不变量违反 [{invariant}]: {details}")

def require_invariant(condition: bool, invariant: str, details: str):
    """不变量检查装饰器"""
    if not condition:
        raise BusinessInvariantError(invariant, details)
```

---

## 2. 关键测试用例 (Test Scenarios)

| ID | 场景 | 输入 | 预期输出 | 对应测试文件 | 优先级 |
|----|------|------|----------|--------------|--------|
| TC-01 | 用户注册 | 有效邮箱+密码 | 创建成功, 返回UID | `tests/auth/test_register.py` | P0 |
| TC-02 | 用户登录 | 正确凭证 | 返回JWT Token | `tests/auth/test_login.py` | P0 |
| TC-03 | 余额查询 | 用户ID | 返回正确余额 | `tests/wallet/test_balance.py` | P0 |
| TC-04 | 余额扣除 | 余额 < 金额 | 抛出 `InsufficientFunds` | `tests/wallet/test_debit.py` | P0 |
| TC-05 | 订单创建 | 有效商品列表 | 创建成功 | `tests/order/test_create.py` | P0 |
| TC-06 | 订单状态变更 | 已完成订单 | 拒绝修改 | `tests/order/test_status.py` | P0 |
| TC-07 | 支付成功 | 有效订单+支付方式 | 状态更新为PAID | `tests/payment/test_process.py` | P0 |
| TC-08 | 库存校验 | 超量商品 | 校验失败 | `tests/inventory/test_validate.py` | P1 |

---

## 3. 行为断言 (Behavioral Assertions)

### 3.1 Python 断言模板

```python
# tests/conftest.py
import pytest
from src.core.user import User, UserRole

@pytest.fixture
def sample_user():
    return User(
        id="test-uuid",
        email="test@example.com",
        username="testuser",
        role=UserRole.USER
    )

# tests/user/test_user_service.py
class TestUserService:
    def test_create_user_success(self, user_service, user_repo):
        """用户创建成功测试"""
        result = user_service.create_user(
            email="new@example.com",
            username="newuser",
            password="SecurePass123"
        )
        
        # 断言
        assert result.id is not None
        assert result.email == "new@example.com"
        assert result.role == UserRole.USER
        assert user_repo.save.called_once()

    def test_create_user_duplicate_email(self, user_service, user_repo):
        """重复邮箱测试"""
        user_repo.find_by_email.return_value = User(...)
        
        with pytest.raises(DuplicateEmailError):
            user_service.create_user(email="existing@example.com", ...)
```

### 3.2 TypeScript 断言模板

```typescript
// tests/order/order.service.spec.ts
describe('OrderService', () => {
  it('should create order successfully', async () => {
    const order = await orderService.createOrder({
      userId: 'user-123',
      items: [{ productId: 'prod-1', quantity: 2 }]
    });
    
    expect(order.id).toBeDefined();
    expect(order.status).toBe(OrderStatus.PENDING);
    expect(order.total).toBeGreaterThan(0);
  });

  it('should reject order with empty items', async () => {
    await expect(orderService.createOrder({
      userId: 'user-123',
      items: []
    })).rejects.toThrow(InvalidOrderError);
  });
});
```

---

## 4. 性能约束 (SLA)

| 指标 | 目标 (P95) | 目标 (P99) | 监控位置 |
|------|------------|------------|----------|
| API 响应时间 | < 200ms | < 500ms | API Gateway |
| 数据库查询 | < 50ms | < 100ms | Slow Query Log |
| 页面加载 | < 1s | < 2s | Frontend Performance |
| 支付处理 | < 3s | < 5s | Payment Service |

---

## 5. 异常处理规范

### 5.1 异常分类

```python
class AppException(Exception):
    """应用异常基类"""
    def __init__(self, code: str, message: str, status_code: int = 500):
        self.code = code
        self.message = message
        self.status_code = status_code

class ValidationError(AppException):
    """参数验证错误"""
    def __init__(self, field: str, reason: str):
        super().__init__(
            code="ERR_001",
            message=f"参数验证失败 [{field}]: {reason}",
            status_code=400
        )

class NotFoundError(AppException):
    """资源不存在"""
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            code="ERR_002",
            message=f"{resource} 不存在: {identifier}",
            status_code=404
        )

class AuthorizationError(AppException):
    """权限不足"""
    def __init__(self, action: str):
        super().__init__(
            code="ERR_003",
            message=f"权限不足: {action}",
            status_code=403
        )
```

### 5.2 全局异常处理

```python
# FastAPI 全局异常处理器
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )
```

---

## 6. Tier 3 验证检查清单

```bash
# 运行所有测试
pytest tests/ -v --tb=short --cov=src

# 通过标准: 
# - 测试覆盖率 > 80%
# - 所有 P0 测试通过
# - 无运行时错误
```

| 检查项 | 验证方法 | 通过标准 |
|--------|----------|----------|
| 单元测试 | `pytest tests/unit/` | 覆盖率 > 80%, 全部通过 |
| 集成测试 | `pytest tests/integration/` | 关键流程全部通过 |
| 业务不变量 | 运行时监控 | 违反次数 = 0 |
| 性能约束 | 性能测试 | P95 达标 |

---

**宪法依据**: §102
**最后更新**: {{TIMESTAMP}}
**版本**: v1.8.0
