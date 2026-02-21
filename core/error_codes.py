"""
CDD Error Codes Module (error_codes.py) v2.0.0
================================================
统一错误代码定义，确保所有工具返回一致的错误信息。

宪法依据: §104 (错误处理规范)

使用方式:
    from core.error_codes import ErrorCodes, ErrorCode
    
    # 获取错误信息
    error = ErrorCodes.get(ErrorCode.C001_ENTROPY_EXCEEDED)
    print(error.message)  # "熵值超标"
    print(error.recovery) # "运行 cdd_entropy.py optimize"
"""

from dataclasses import dataclass
from typing import Dict, Optional, List, Any
from enum import Enum


class ErrorCode(Enum):
    """错误代码枚举"""
    # C0xx - 系统级错误 (100-109)
    C001_ENTROPY_EXCEEDED = "C001"
    C002_VERSION_MISMATCH = "C002"
    C003_SPORE_ISOLATION = "C003"
    C004_TEST_FAILURE = "C004"
    C005_SPEC_NOT_APPROVED = "C005"
    C006_SEMANTIC_AUDIT_FAILED = "C006"
    C007_INVALID_CONSTITUTION_REF = "C007"
    C008_TEMPLATE_NOT_FOUND = "C008"
    C009_CONFIG_INVALID = "C009"
    C010_DEPENDENCY_MISSING = "C010"
    
    # C1xx - 工具执行错误 (110-119)
    C110_TOOL_EXECUTION_ERROR = "C110"
    C111_GIT_OPERATION_FAILED = "C111"
    C112_FILE_OPERATION_FAILED = "C112"
    C113_PERMISSION_DENIED = "C113"
    C114_TIMEOUT = "C114"
    
    # C2xx - 状态转换错误 (120-129)
    C120_INVALID_STATE_TRANSITION = "C120"
    C121_STATE_VALIDATION_FAILED = "C121"
    C122_MISSING_PREREQUISITE = "C122"
    
    # ENVxx - 环境错误
    ENV_PYTHON_VERSION = "ENV001"
    ENV_PIP_NOT_FOUND = "ENV002"
    ENV_GIT_NOT_FOUND = "ENV003"
    ENV_VIRTUAL_ENV = "ENV004"


@dataclass
class ErrorInfo:
    """错误信息数据类"""
    code: str
    message: str
    constitution_ref: str
    recovery: str
    severity: str  # "critical", "warning", "info"
    related_gates: List[int]  # 相关的审计门禁


class ErrorCodes:
    """统一错误代码管理"""
    
    _registry: Dict[str, ErrorInfo] = {
        # C0xx - 系统级错误
        ErrorCode.C001_ENTROPY_EXCEEDED.value: ErrorInfo(
            code="C001",
            message="熵值超标",
            constitution_ref="§102",
            recovery="运行 `cdd_entropy.py optimize` 优化熵值，然后重新检查",
            severity="critical",
            related_gates=[3]
        ),
        ErrorCode.C002_VERSION_MISMATCH.value: ErrorInfo(
            code="C002",
            message="版本不一致",
            constitution_ref="§100.3",
            recovery="运行 `cdd_auditor.py --gate 1 --fix` 自动修复版本漂移",
            severity="warning",
            related_gates=[1]
        ),
        ErrorCode.C003_SPORE_ISOLATION.value: ErrorInfo(
            code="C003",
            message="孢子隔离违例",
            constitution_ref="§106.1",
            recovery="在项目目录调用工具，而不是在CDD技能目录中",
            severity="critical",
            related_gates=[]
        ),
        ErrorCode.C004_TEST_FAILURE.value: ErrorInfo(
            code="C004",
            message="测试失败",
            constitution_ref="§300.3",
            recovery="运行 `pytest tests/ -v` 查看详细错误，修复失败的测试",
            severity="critical",
            related_gates=[2]
        ),
        ErrorCode.C005_SPEC_NOT_APPROVED.value: ErrorInfo(
            code="C005",
            message="规格文档未批准",
            constitution_ref="§103",
            recovery="等待规格文档(DS-050)获得明确批准后再开始编码",
            severity="critical",
            related_gates=[]
        ),
        ErrorCode.C006_SEMANTIC_AUDIT_FAILED.value: ErrorInfo(
            code="C006",
            message="语义审计失败",
            constitution_ref="§101",
            recovery="确保文档中包含足够的宪法引用，覆盖率需达到80%",
            severity="warning",
            related_gates=[4]
        ),
        ErrorCode.C007_INVALID_CONSTITUTION_REF.value: ErrorInfo(
            code="C007",
            message="无效的宪法引用",
            constitution_ref="§104",
            recovery="检查宪法引用格式，确保使用有效的条款编号(如§101)",
            severity="warning",
            related_gates=[5]
        ),
        ErrorCode.C008_TEMPLATE_NOT_FOUND.value: ErrorInfo(
            code="C008",
            message="模板文件未找到",
            constitution_ref="§202",
            recovery="验证CDD技能完整性: `python scripts/cdd_verify.py`",
            severity="warning",
            related_gates=[]
        ),
        ErrorCode.C009_CONFIG_INVALID.value: ErrorInfo(
            code="C009",
            message="配置文件无效",
            constitution_ref="§201",
            recovery="检查cdd_config.yaml格式是否正确",
            severity="warning",
            related_gates=[]
        ),
        ErrorCode.C010_DEPENDENCY_MISSING.value: ErrorInfo(
            code="C010",
            message="依赖缺失",
            constitution_ref="§200",
            recovery="运行 `pip install -r requirements.txt` 安装依赖",
            severity="warning",
            related_gates=[]
        ),
        
        # C1xx - 工具执行错误
        ErrorCode.C110_TOOL_EXECUTION_ERROR.value: ErrorInfo(
            code="C110",
            message="工具执行错误",
            constitution_ref="§300.5",
            recovery="检查工具参数是否正确，使用 --help 获取帮助",
            severity="critical",
            related_gates=[]
        ),
        ErrorCode.C111_GIT_OPERATION_FAILED.value: ErrorInfo(
            code="C111",
            message="Git操作失败",
            constitution_ref="§300.2",
            recovery="检查Git仓库状态，确保有正确的权限",
            severity="warning",
            related_gates=[]
        ),
        ErrorCode.C112_FILE_OPERATION_FAILED.value: ErrorInfo(
            code="C112",
            message="文件操作失败",
            constitution_ref="§200",
            recovery="检查文件权限和磁盘空间",
            severity="critical",
            related_gates=[]
        ),
        ErrorCode.C113_PERMISSION_DENIED.value: ErrorInfo(
            code="C113",
            message="权限被拒绝",
            constitution_ref="§200",
            recovery="检查文件/目录权限，可能需要sudo或修改权限",
            severity="critical",
            related_gates=[]
        ),
        ErrorCode.C114_TIMEOUT.value: ErrorInfo(
            code="C114",
            message="操作超时",
            constitution_ref="§300.5",
            recovery="增加超时时间或检查系统负载",
            severity="warning",
            related_gates=[]
        ),
        
        # C2xx - 状态转换错误
        ErrorCode.C120_INVALID_STATE_TRANSITION.value: ErrorInfo(
            code="C120",
            message="无效的状态转换",
            constitution_ref="§104",
            recovery="检查当前状态，确保遵循5状态工作流(A→B→C→D→E)",
            severity="critical",
            related_gates=[]
        ),
        ErrorCode.C121_STATE_VALIDATION_FAILED.value: ErrorInfo(
            code="C121",
            message="状态验证失败",
            constitution_ref="§104",
            recovery="检查memory_bank/t0_core/active_context.md中的状态",
            severity="warning",
            related_gates=[]
        ),
        ErrorCode.C122_MISSING_PREREQUISITE.value: ErrorInfo(
            code="C122",
            message="缺少前置条件",
            constitution_ref="§103",
            recovery="确保满足当前操作的所有前置条件",
            severity="warning",
            related_gates=[]
        ),
        
        # ENVxx - 环境错误
        ErrorCode.ENV_PYTHON_VERSION.value: ErrorInfo(
            code="ENV001",
            message="Python版本不兼容",
            constitution_ref="§200",
            recovery="安装Python 3.8或更高版本",
            severity="critical",
            related_gates=[]
        ),
        ErrorCode.ENV_PIP_NOT_FOUND.value: ErrorInfo(
            code="ENV002",
            message="pip未找到",
            constitution_ref="§200",
            recovery="安装pip: `python -m ensurepip --upgrade`",
            severity="critical",
            related_gates=[]
        ),
        ErrorCode.ENV_GIT_NOT_FOUND.value: ErrorInfo(
            code="ENV003",
            message="Git未找到",
            constitution_ref="§300.2",
            recovery="安装Git: `apt install git` 或 `brew install git`",
            severity="warning",
            related_gates=[]
        ),
        ErrorCode.ENV_VIRTUAL_ENV.value: ErrorInfo(
            code="ENV004",
            message="虚拟环境问题",
            constitution_ref="§200",
            recovery="重新创建虚拟环境: `python -m venv .venv && source .venv/bin/activate`",
            severity="warning",
            related_gates=[]
        ),
    }
    
    @classmethod
    def get(cls, code: str) -> Optional[ErrorInfo]:
        """
        获取错误信息
        
        Args:
            code: 错误代码 (如 "C001")
            
        Returns:
            ErrorInfo或None
        """
        return cls._registry.get(code)
    
    @classmethod
    def get_message(cls, code: str) -> str:
        """获取错误消息"""
        info = cls.get(code)
        if info:
            return info.message
        return f"未知错误: {code}"
    
    @classmethod
    def get_recovery(cls, code: str) -> str:
        """获取恢复建议"""
        info = cls.get(code)
        if info:
            return info.recovery
        return "无可用恢复建议"
    
    @classmethod
    def format_error(cls, code: str, context: str = "") -> str:
        """
        格式化错误信息为完整报告
        
        Args:
            code: 错误代码
            context: 额外上下文
            
        Returns:
            格式化的错误报告
        """
        info = cls.get(code)
        if not info:
            return f"❌ 未知错误: {code}"
        
        lines = [
            f"❌ {info.code}: {info.message}",
            f"   宪法依据: {info.constitution_ref}",
            f"   严重程度: {info.severity}",
            "",
            f"🔧 恢复建议:",
            f"   {info.recovery}",
        ]
        
        if context:
            lines.extend([
                "",
                f"📝 上下文:",
                f"   {context}"
            ])
        
        if info.related_gates:
            gates_str = ", ".join(f"Gate {g}" for g in info.related_gates)
            lines.extend([
                "",
                f"🔍 相关门禁: {gates_str}"
            ])
        
        return "\n".join(lines)
    
    @classmethod
    def list_all(cls, severity: str = None) -> List[ErrorInfo]:
        """
        列出所有错误
        
        Args:
            severity: 按严重程度过滤 ("critical", "warning", "info")
            
        Returns:
            ErrorInfo列表
        """
        errors = list(cls._registry.values())
        if severity:
            errors = [e for e in errors if e.severity == severity]
        return errors
    
    @classmethod
    def get_gate_errors(cls, gate_id: int) -> List[ErrorInfo]:
        """
        获取与特定门禁相关的错误
        
        Args:
            gate_id: 门禁ID (1-5)
            
        Returns:
            相关的ErrorInfo列表
        """
        return [e for e in cls._registry.values() if gate_id in e.related_gates]


# 便捷函数
def get_error(code: str) -> Optional[ErrorInfo]:
    """获取错误信息的便捷函数"""
    return ErrorCodes.get(code)


def format_error(code: str, context: str = "") -> str:
    """格式化错误的便捷函数"""
    return ErrorCodes.format_error(code, context)


# 熵值阈值常量
ENTROPY_THRESHOLDS = {
    "excellent": {"max": 0.3, "color": "🟢", "action": "正常开发"},
    "good": {"min": 0.3, "max": 0.5, "color": "🟡", "action": "监控技术债务"},
    "warning": {"min": 0.5, "max": 0.7, "color": "🟠", "action": "优先修复"},
    "danger": {"min": 0.7, "color": "🔴", "action": "立即重构"}
}


def assess_entropy(h_sys: float) -> Dict[str, Any]:
    """
    评估熵值水平
    
    Args:
        h_sys: 系统熵值 (0.0-1.0)
        
    Returns:
        包含评估结果的字典
    """
    if h_sys <= 0.3:
        level = "excellent"
    elif h_sys <= 0.5:
        level = "good"
    elif h_sys <= 0.7:
        level = "warning"
    else:
        level = "danger"
    
    threshold = ENTROPY_THRESHOLDS[level]
    
    from typing import Any, Dict
    
    return {
        "level": level,
        "color": threshold["color"],
        "action": threshold["action"],
        "value": h_sys,
        "threshold": threshold.get("max", 1.0)
    }