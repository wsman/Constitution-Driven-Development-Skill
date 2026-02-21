"""
CDD Utilities Module

通用工具函数和辅助类。

宪法依据: §102§309
"""

from .cache_manager import CacheManager
from .entropy_utils import calculate_simple_entropy, quick_entropy_estimate
from .file_utils import (
    run_command, run_command_safe, ensure_dir, read_json, write_json, 
    read_file, write_file, file_matches_patterns
)
from .spore_utils import check_spore_isolation, create_deployment_flag, is_deployment_mode
from .logger import Logger
from .version_utils import parse_version, compare_version

__all__ = [
    "CacheManager",
    "calculate_simple_entropy", "quick_entropy_estimate",
    "run_command", "run_command_safe", "ensure_dir", "read_json", "write_json",
    "read_file", "write_file", "file_matches_patterns",
    "check_spore_isolation", "create_deployment_flag", "is_deployment_mode",
    "Logger", 
    "parse_version", "compare_version"
]