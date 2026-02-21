"""
Version Utilities

版本相关工具函数。

宪法依据: §100.3
"""

import re
from typing import Optional, Tuple


def parse_version(version_str: str) -> Tuple[int, int, int, Optional[str]]:
    """
    解析版本字符串
    
    Args:
        version_str: 版本字符串，如 "2.1.0", "v1.2.3-beta"
        
    Returns:
        Tuple[主要版本, 次要版本, 修订版本, 预发布标签]
    """
    # 移除可能的v前缀
    clean_str = version_str.strip().lstrip('vV')
    
    # 匹配主要.次要.修订[.构建][-预发布]
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:\.\d+)?(-[a-zA-Z0-9.]+)?$', clean_str)
    
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3))
        prerelease = match.group(4)[1:] if match.group(4) else None
        
        return major, minor, patch, prerelease
    else:
        # 简化的版本格式
        parts = clean_str.split('.')
        major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
        minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        patch = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        
        return major, minor, patch, None


def compare_version(version_a: str, version_b: str) -> int:
    """
    比较两个版本号
    
    Args:
        version_a: 版本A
        version_b: 版本B
        
    Returns:
        -1: A < B
         0: A == B
         1: A > B
    """
    maj_a, min_a, pat_a, pre_a = parse_version(version_a)
    maj_b, min_b, pat_b, pre_b = parse_version(version_b)
    
    # 比较主要版本
    if maj_a < maj_b:
        return -1
    elif maj_a > maj_b:
        return 1
    
    # 比较次要版本
    if min_a < min_b:
        return -1
    elif min_a > min_b:
        return 1
    
    # 比较修订版本
    if pat_a < pat_b:
        return -1
    elif pat_a > pat_b:
        return 1
    
    # 比较预发布版本（如果有）
    if pre_a is None and pre_b is not None:
        return 1  # 正式版本 > 预发布版本
    elif pre_a is not None and pre_b is None:
        return -1  # 预发布版本 < 正式版本
    elif pre_a is not None and pre_b is not None:
        # 简单的预发布版本比较
        if pre_a < pre_b:
            return -1
        elif pre_a > pre_b:
            return 1
    
    return 0


def is_compatible(version_a: str, version_b: str, strict: bool = False) -> bool:
    """
    检查版本是否兼容
    
    Args:
        version_a: 版本A
        version_b: 版本B
        strict: 是否严格模式（完全相同才兼容）
        
    Returns:
        bool: 是否兼容
    """
    if strict:
        return compare_version(version_a, version_b) == 0
    
    maj_a, min_a, _, _ = parse_version(version_a)
    maj_b, min_b, _, _ = parse_version(version_b)
    
    # 主要版本必须相同
    if maj_a != maj_b:
        return False
    
    # 次要版本差异 <= 1 视为兼容
    return abs(min_a - min_b) <= 1


def validate_version(version_str: str) -> bool:
    """
    验证版本字符串格式
    
    Args:
        version_str: 版本字符串
        
    Returns:
        bool: 是否有效
    """
    try:
        parse_version(version_str)
        return True
    except (ValueError, TypeError):
        return False


def normalize_version(version_str: str) -> str:
    """
    标准化版本字符串
    
    Args:
        version_str: 原始版本字符串
        
    Returns:
        标准化版本字符串
    """
    maj, min, pat, pre = parse_version(version_str)
    
    if pre:
        return f"{maj}.{min}.{pat}-{pre}"
    else:
        return f"{maj}.{min}.{pat}"