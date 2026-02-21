"""
CDD Constants (constants.py)
============================
全局常量定义。

宪法依据: §101§102
"""

from pathlib import Path
from typing import List, Dict, Any, Final

# ==================== 基本常量 ====================
SKILL_ROOT: Final[Path] = Path(__file__).parent.parent.resolve()
VERSION: Final[str] = "2.0.0"

DEFAULT_ENCODING: Final[str] = "utf-8"

# ==================== 目录结构常量 ====================
REQUIRED_DIRS_PROJECT: Final[List[str]] = ["memory_bank", "src", "tests"]
REQUIRED_DIRS_SKILL: Final[List[str]] = ["claude", "scripts", "tests", "templates", "reference"]
OPTIONAL_DIRS: Final[List[str]] = ["examples", "utils"]

# ==================== 熵值计算常量 ====================
#
# 系统熵值计算公式 (§102, §300.5):
#
#   compliance_score = W_DIR * C_dir + W_SIG * C_sig + W_TEST * C_test
#   H_sys = 1.0 - compliance_score
#
# 三个合规率指标:
#   C_dir  = 目录结构合规率 (权重 0.4) - 检查目录结构是否符合CDD规范
#   C_sig  = 接口签名覆盖率 (权重 0.3) - 检查接口文档覆盖程度
#   C_test = 测试通过率     (权重 0.3) - 检查单元测试通过情况
#
# 熵值评估标准 (H_sys = 1.0 - compliance_score):
#   ≤ 0.3 : 优秀 🟢 (compliance_score ≥ 0.7)
#   ≤ 0.5 : 良好 🟡 (compliance_score ≥ 0.5)
#   ≤ 0.7 : 警告 🟠 (compliance_score ≥ 0.3)
#   > 0.7 : 危险 🔴 (compliance_score < 0.3)

# 权重配置 (总和 = 1.0)
W_DIR: Final[float] = 0.4   # 目录结构合规率权重
W_SIG: Final[float] = 0.3   # 接口签名覆盖率权重
W_TEST: Final[float] = 0.3  # 测试通过率权重

# 熵值阈值 (§300.5)
THRESHOLD_EXCELLENT: Final[float] = 0.3  # 优秀阈值
THRESHOLD_GOOD: Final[float] = 0.5       # 良好阈值
THRESHOLD_WARNING: Final[float] = 0.7    # 警告阈值
THRESHOLD_DANGER: Final[float] = 0.9     # 危险阈值

# ==================== 缓存配置 ====================
CACHE_DIR_NAME: Final[str] = ".entropy_cache"
CACHE_FILE: Final[str] = "entropy.json"
CACHE_TTL: Final[int] = 3600  # 缓存有效期（秒）

# ==================== 工具定义常量 ====================
TOOL_PREFIX: Final[str] = "cdd_"
TOOL_CATEGORIES: Final[List[str]] = ["audit", "feature", "entropy", "project", "transition", "constitution"]

# ==================== 宪法引用格式 ====================
CONSTITUTION_SECTION_PATTERN: Final[str] = r"§(\d{3}(?:\.\d+)?)"
CONSTITUTION_REFERENCE_FORMAT: Final[str] = "§{section}"

# 从统一的宪法模块导入条款列表
# 注意: 详细定义请参考 core/constitution_core.py
try:
    from core.constitution_core import CONSTITUTION_CORE_ARTICLES_LIST as CONSTITUTION_ARTICLES
except ImportError:
    # 回退到硬编码列表（保持向后兼容）
    CONSTITUTION_ARTICLES: List[str] = [
        # T0 核心层 (基本法)
        "§100", "§100.3", "§101", "§102", "§103", "§104", "§105", "§119", "§148",
        # T1 技术层 (技术法)
        "§106.1", "§200", "§201", "§202", "§267", "§268", "§269",
        # T2 协议层 (程序法)
        "§300", "§300.3", "§300.5", "§301", "§302", "§303", "§304", "§305",
        # T3 文档层
        "§309", "§310", "§311", "§312", "§350"
    ]

# 宪法引用格式规范
CONSTITUTION_REF_PATTERNS: Final[Dict[str, str]] = {
    "valid": r"§\d{3}(?:\.\d+)?",  # 有效格式: §100.3
    "invalid_with_name": r"§\d{3}(?:\.\d+)?\s+\S+",  # 无效格式: §100.3 同步公理
}

# ==================== 状态常量 ====================
STATE_ACTIVE: Final[str] = "active"
STATE_SUSPENDED: Final[str] = "suspended"
STATE_ARCHIVED: Final[str] = "archived"

# ==================== 错误级别常量 ====================
ERROR_LEVEL_INFO: Final[str] = "info"
ERROR_LEVEL_WARNING: Final[str] = "warning"
ERROR_LEVEL_ERROR: Final[str] = "error"
ERROR_LEVEL_CRITICAL: Final[str] = "critical"

# ==================== 审计门禁常量 ====================
GATES: Final[Dict[str, Dict[str, Any]]] = {
    "1": {
        "name": "版本一致性检查",
        "description": "检查所有文件的版本信息一致性",
        "constitutional_basis": ["§100.3"]
    },
    "2": {
        "name": "行为验证检查",
        "description": "验证行为符合宪法要求",
        "constitutional_basis": ["§300.3"]
    },
    "3": {
        "name": "熵值监控检查",
        "description": "监控系统熵值状态",
        "constitutional_basis": ["§102"]
    },
    "4": {
        "name": "语义审计检查",
        "description": "检查宪法引用和语义一致性",
        "constitutional_basis": ["§101", "§300.5"]
    },
    "5": {
        "name": "宪法引用完整性检查",
        "description": "验证所有宪法引用格式正确且引用的条款存在",
        "constitutional_basis": ["§305"]
    }
}