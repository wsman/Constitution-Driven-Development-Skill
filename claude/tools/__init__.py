"""
CDD Claude Tools Package v2.0.0

Claude Code工具集成包，提供CDD技能的MCP工具接口。

宪法依据: §309§304
"""

__version__ = "2.0.0"
__author__ = "CDD技术部"
__license__ = "Apache-2.0"

# 导出核心工具类
from .tool_registry import CDDToolRegistry
from .cdd_audit_tool import CDDAuditTool
from .measure_entropy_tool import MeasureEntropyTool
from .cdd_feature_tool import CDDFeatureTool
from .cdd_project_init_tool import CDDProjectInitTool
from .cdd_state_transition_tool import CDDStateTransitionTool

# 导出工具函数
from .tool_registry import register_tools, get_tool, list_tools

__all__ = [
    "CDDToolRegistry",
    "CDDAuditTool",
    "MeasureEntropyTool",
    "CDDFeatureTool",
    "CDDProjectInitTool",
    "CDDStateTransitionTool",
    "register_tools",
    "get_tool",
    "list_tools",
]