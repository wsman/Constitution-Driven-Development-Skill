"""
Spore Isolation Utilities

孢子隔离工具函数，确保工具不会意外修改CDD技能库自身。

宪法依据: §200
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Tuple

from core.constants import SKILL_ROOT, VERSION
from core.exceptions import SporeIsolationViolation


def check_spore_isolation(
    target_root: Path, 
    tool_name: str,
    allow_skill_root: bool = False,
    strict_mode: bool = True
) -> Tuple[bool, str]:
    """
    孢子隔离检查
    
    确保工具不会意外修改CDD技能库自身
    
    Args:
        target_root: 目标目录
        tool_name: 工具名称
        allow_skill_root: 是否允许操作技能库
        strict_mode: 是否严格模式（默认True，检查部署标志）
        
    Returns:
        Tuple[bool, str]: (是否通过, 消息)
    """
    target_root = Path(target_root).resolve()
    
    # 1. 检查部署模式
    if not strict_mode or is_deployment_mode(target_root):
        return True, "Deployment mode detected, spore isolation bypassed"
    
    # 2. 检查是否是技能库本身
    if target_root == SKILL_ROOT:
        if allow_skill_root:
            return True, "Self-modification allowed"
        else:
            return False, f"""
⛔ **SPORE ISOLATION VIOLATION [{tool_name}]**
    Target directory is CDD Skill Root: {SKILL_ROOT}
    CDD Skill is a tool, not a target project.
    Please specify a different target: --target /path/to/project
"""
    
    # 3. 检查是否在技能库内（子目录）
    try:
        target_root.relative_to(SKILL_ROOT)
        if strict_mode:
            return False, f"""
⛔ **SPORE ISOLATION VIOLATION [{tool_name}]**
    Target directory is inside CDD Skill Root: {target_root}
    Cannot operate on CDD skill subdirectories.
    Please specify a different target: --target /path/to/independent/project
"""
        else:
            return True, "Warning: Target is inside CDD Skill Root"
    except ValueError:
        pass  # 不在SKILL_ROOT内，安全
    
    return True, "Spore isolation check passed"


def create_deployment_flag(skill_root: Path, deployed_dir: Path):
    """
    创建部署标志
    
    标记已部署的工具处于部署模式
    """
    flag_file = deployed_dir / ".cdd_deployed"
    
    flag_content = {
        "source_skill": str(skill_root),
        "deployed_at": datetime.now().isoformat(),
        "version": VERSION
    }
    
    flag_file.write_text(json.dumps(flag_content, indent=2))


def is_deployment_mode(script_dir: Path) -> bool:
    """检查是否处于部署模式"""
    flag_file = script_dir / ".cdd_deployed"
    return flag_file.exists()