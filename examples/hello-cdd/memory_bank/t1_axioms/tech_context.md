# Tech Context (技术上下文)

**项目**: hello-cdd  
**类型**: T1 公理层  
**用途**: 定义技术栈和接口签名

---

## 🛠️ 技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 主要开发语言 |
| pytest | 7.x | 测试框架 |
| Markdown | - | 文档格式 |

---

## 📋 接口签名

### hello 模块

```python
# src/hello.py

def greet(name: str) -> str:
    """
    返回问候语
    
    Args:
        name: 用户名
        
    Returns:
        问候字符串
    """
    pass

def get_version() -> str:
    """
    返回版本号
    
    Returns:
        版本字符串 (如 "0.1.0")
    """
    pass
```

---

## ✅ Tier 2 验证标准

验证代码接口是否符合本文档定义：

```python
# 验证接口存在
from src.hello import greet, get_version

# 验证签名
assert callable(greet)
assert callable(get_version)
```

---

**宪法依据**: §300.3