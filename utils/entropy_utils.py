"""
Entropy Utilities

熵值计算的工具函数。

宪法依据: §102
"""

import re
from pathlib import Path
from typing import Dict, Any, List

from core.constants import (
    REQUIRED_DIRS_PROJECT, REQUIRED_DIRS_SKILL, OPTIONAL_DIRS,
    W_DIR, W_SIG, W_TEST, THRESHOLD_WARNING
)
from core.exceptions import EntropyThresholdExceeded


def calculate_simple_entropy(project_path: Path) -> Dict[str, Any]:
    """
    简单的熵值计算
    
    Args:
        project_path: 项目路径
        
    Returns:
        Dict[str, Any]: 熵值结果
    """
    # 检查是否为CDD技能库本身
    is_cdd_skill = (project_path / "scripts" / "cdd_entropy.py").exists()
    
    # 计算目录合规率
    if is_cdd_skill:
        required_dirs = REQUIRED_DIRS_SKILL
    else:
        required_dirs = REQUIRED_DIRS_PROJECT
    
    c_dir = _calculate_directory_compliance(project_path, required_dirs, OPTIONAL_DIRS)
    
    # 简化计算接口覆盖率和测试通过率
    c_sig = 0.7  # 默认值
    c_test = 0.5  # 默认值
    
    # 计算综合熵值
    compliance_score = W_DIR * c_dir + W_SIG * c_sig + W_TEST * c_test
    h_sys = 1.0 - compliance_score
    
    # 状态评估
    if h_sys <= 0.3:
        status = "🟢 优秀"
    elif h_sys <= 0.5:
        status = "🟡 良好"
    elif h_sys <= THRESHOLD_WARNING:
        status = "🟠 警告"
    else:
        status = "🔴 危险"
    
    return {
        "h_sys": h_sys,
        "c_dir": c_dir,
        "c_sig": c_sig,
        "c_test": c_test,
        "compliance_score": compliance_score,
        "status": status,
        "threshold_exceeded": h_sys > THRESHOLD_WARNING
    }


def quick_entropy_estimate(project_path: Path) -> Dict[str, Any]:
    """
    快速熵值估算
    
    Args:
        project_path: 项目路径
        
    Returns:
        Dict[str, Any]: 快速估算结果
    """
    # 只检查关键目录
    critical_dirs = ["src", "tests", "memory_bank", "specs"]
    existing_dirs = [d for d in critical_dirs if (project_path / d).exists()]
    
    dir_score = len(existing_dirs) / len(critical_dirs) if critical_dirs else 0.5
    h_sys = 1.0 - dir_score
    
    if h_sys <= 0.3:
        status = "🟢 优秀"
    elif h_sys <= 0.5:
        status = "🟡 良好"
    elif h_sys <= THRESHOLD_WARNING:
        status = "🟠 警告"
    else:
        status = "🔴 危险"
    
    return {
        "h_sys_estimate": h_sys,
        "directory_score": dir_score,
        "critical_dirs_found": existing_dirs,
        "critical_dirs_missing": [d for d in critical_dirs if d not in existing_dirs],
        "status": status
    }


def _calculate_directory_compliance(
    project_path: Path, 
    required_dirs: List[str], 
    optional_dirs: List[str]
) -> float:
    """计算目录合规率"""
    score = 0.0
    total_weight = 0.0
    
    for d in required_dirs:
        total_weight += 1.0
        if (project_path / d).exists():
            score += 1.0
    
    for d in optional_dirs:
        total_weight += 0.5
        if (project_path / d).exists():
            score += 0.5
    
    return score / total_weight if total_weight > 0 else 0.5


def find_entropy_hotspots(project_path: Path, top_n: int = 10) -> List[Dict[str, Any]]:
    """查找熵值热点"""
    hotspots = []
    
    # 检查大文件
    for f in project_path.rglob("*"):
        if f.is_file() and not _should_skip(f):
            try:
                size = f.stat().st_size
                if size > 100000:  # 大于100KB
                    hotspots.append({
                        "path": str(f.relative_to(project_path)),
                        "entropy": 0.3,
                        "reason": f"Large file ({size // 1024}KB)",
                        "suggestions": ["Consider splitting into smaller files"]
                    })
            except Exception:
                pass
    
    # 检查深层目录
    for d in project_path.rglob("*"):
        if d.is_dir() and not _should_skip(d):
            depth = len(d.relative_to(project_path).parts)
            if depth > 5:
                hotspots.append({
                    "path": str(d.relative_to(project_path)),
                    "entropy": 0.2,
                    "reason": f"Deep nesting (depth: {depth})",
                    "suggestions": ["Consider flattening directory structure"]
                })
    
    # 按熵值排序
    hotspots.sort(key=lambda x: x["entropy"], reverse=True)
    return hotspots[:top_n]


def _should_skip(path: Path) -> bool:
    """判断是否跳过该路径"""
    skip_patterns = ['__pycache__', '.git', 'node_modules', '.entropy_cache', '.venv']
    return any(p in str(path) for p in skip_patterns)