"""
CDD Core Module v2.0.0
=====================
核心模块：常量定义、异常类、宪法和服务层。

宪法依据: §101

模块结构:
- constants.py: 全局常量
- constitution.py: 宪法定义
- exceptions.py: 异常类
- audit_service.py: 审计服务
- entropy_service.py: 熵值服务
- feature_service.py: 特性服务
- state_transition_service.py: 状态转换服务
- state_validation_service.py: 状态验证服务
"""

from .constants import *
from .exceptions import *

# 服务层模块（延迟导入）
__services__ = [
    "audit_service",
    "entropy_service", 
    "feature_service",
    "state_transition_service",
    "state_validation_service"
]

__all__ = [
    # 常量
    "SKILL_ROOT", "VERSION", "DEFAULT_ENCODING",
    "REQUIRED_DIRS_PROJECT", "REQUIRED_DIRS_SKILL", "OPTIONAL_DIRS",
    "W_DIR", "W_SIG", "W_TEST", "THRESHOLD_WARNING", "THRESHOLD_DANGER",
    "CACHE_DIR_NAME", "CACHE_FILE", "CACHE_TTL",
    "TOOL_PREFIX", "TOOL_CATEGORIES",
    "CONSTITUTION_SECTION_PATTERN", "CONSTITUTION_REFERENCE_FORMAT",
    "STATE_ACTIVE", "STATE_SUSPENDED", "STATE_ARCHIVED",
    "ERROR_LEVEL_INFO", "ERROR_LEVEL_WARNING", "ERROR_LEVEL_ERROR", "ERROR_LEVEL_CRITICAL",
    "GATES",
    # 异常
    "CDDError", "SporeIsolationViolation", "EntropyThresholdExceeded", "ToolExecutionError",
    "CacheError", "ConstitutionViolation", "VersionDriftError", "DependencyError",
    "ServiceUnavailableError", "ConfigurationError", "ValidationError",
    # 服务模块
    "__services__"
]


def get_service(name: str):
    """
    获取服务模块（延迟导入）
    
    Args:
        name: 服务名称 (audit, entropy, feature, state_transition, state_validation)
        
    Returns:
        对应的服务模块
    """
    import importlib
    module_name = f"{name}_service"
    if module_name not in __services__:
        raise ImportError(f"Unknown service: {name}")
    return importlib.import_module(f".{module_name}", package="core")