# Behavior Context (行为上下文)

**项目**: hello-cdd  
**类型**: T1 公理层  
**用途**: 定义测试场景和行为不变量

---

## 🧪 测试场景

### 场景1: 问候功能

```python
# tests/test_hello.py

def test_greet_with_name():
    """测试带名字的问候"""
    from src.hello import greet
    result = greet("World")
    assert "World" in result
    assert len(result) > 0

def test_greet_empty_name():
    """测试空名字的边界情况"""
    from src.hello import greet
    result = greet("")
    assert len(result) > 0  # 应返回默认问候
```

### 场景2: 版本获取

```python
def test_get_version():
    """测试版本号格式"""
    from src.hello import get_version
    version = get_version()
    # 版本格式: X.Y.Z
    parts = version.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)
```

---

## 📋 行为不变量

| ID | 不变量 | 描述 |
|----|--------|------|
| INV-001 | `greet(name)` 总返回非空字符串 | 即使 name 为空 |
| INV-002 | `get_version()` 返回语义版本格式 | X.Y.Z |
| INV-003 | 所有公共函数可调用 | 无异常抛出 |

---

## ✅ Tier 3 验证标准

验证行为是否符合本文档定义：

```bash
# 运行行为验证
pytest tests/ -v

# 预期结果: 所有测试通过
```

---

**宪法依据**: §300.3