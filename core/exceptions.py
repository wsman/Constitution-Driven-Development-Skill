"""
CDD Exceptions (exceptions.py)
==============================
自定义异常类。

宪法依据: §310§300.5
"""

class CDDError(Exception):
    """CDD基础异常类"""
    def __init__(self, message: str, constitutional_violation: str = ""):
        super().__init__(message)
        self.constitutional_violation = constitutional_violation
        self.message = message
    
    def __str__(self):
        if self.constitutional_violation:
            return f"{self.message} (违反: {self.constitutional_violation})"
        return self.message


class SporeIsolationViolation(CDDError):
    """孢子隔离违例"""
    def __init__(self, message: str = "Spore isolation violation"):
        super().__init__(message, "§200")


class EntropyThresholdExceeded(CDDError):
    """熵值阈值超过"""
    def __init__(self, h_sys: float, threshold: float):
        message = f"熵值超标: H_sys={h_sys:.3f} > 阈值={threshold:.3f}"
        super().__init__(message, "§102")


class ToolExecutionError(CDDError):
    """工具执行错误"""
    def __init__(self, tool_name: str, error_msg: str):
        message = f"工具'{tool_name}'执行失败: {error_msg}"
        super().__init__(message, "§309")


class CacheError(CDDError):
    """缓存错误"""
    def __init__(self, operation: str, error_msg: str):
        message = f"缓存操作'{operation}'失败: {error_msg}"
        super().__init__(message, "§102")


class ConstitutionViolation(CDDError):
    """宪法违例"""
    def __init__(self, section: str, violation: str):
        message = f"宪法违例 §{section}: {violation}"
        super().__init__(message, f"§{section}")


class VersionDriftError(CDDError):
    """版本漂移错误"""
    def __init__(self, expected: str, actual: str):
        message = f"版本漂移: 期望={expected}, 实际={actual}"
        super().__init__(message, "§100.3")


class DependencyError(CDDError):
    """依赖关系错误"""
    def __init__(self, dependency: str, reason: str):
        message = f"依赖关系错误: {dependency} - {reason}"
        super().__init__(message, "§309")


class ServiceUnavailableError(CDDError):
    """服务不可用错误"""
    def __init__(self, service_name: str):
        message = f"服务不可用: {service_name}"
        super().__init__(message, "§309")


class ConfigurationError(CDDError):
    """配置错误"""
    def __init__(self, config_key: str, reason: str):
        message = f"配置错误 '{config_key}': {reason}"
        super().__init__(message, "§101")


class ValidationError(CDDError):
    """验证错误"""
    def __init__(self, field: str, reason: str):
        message = f"验证错误 '{field}': {reason}"
        super().__init__(message, "§300.3")


class AuditGateFailed(CDDError):
    """审计门禁失败"""
    def __init__(self, gate_id: int, reason: str):
        message = f"Gate {gate_id} failed: {reason}"
        super().__init__(message, f"§{300 + gate_id} 相关审计条款")