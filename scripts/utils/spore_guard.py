"""
Spore Guard Utility (孢子卫士)
=============================
实现了 CDD 宪法 §300.1 (孢子协议) 的核心隔离逻辑。
防止 CDD 工具链对自己进行操作（递归污染）。

数学原理：∀T ∈ S_target, T ∉ S_tool
其中 S_tool = {SKILL_ROOT}, S_target 是目标项目集合
"""

import sys
from pathlib import Path

# 计算 SKILL_ROOT (此文件位于 scripts/utils/ 下)
# scripts/utils/spore_guard.py -> scripts/utils -> scripts -> SKILL_ROOT
SKILL_ROOT = Path(__file__).resolve().parent.parent.parent

def check_spore_isolation(target_path: Path, tool_name: str):
    """
    执行孢子隔离检查。
    
    :param target_path: 用户指定的操作目标路径
    :param tool_name: 当前运行的工具名称 (用于报错信息)
    """
    resolved_target = target_path.resolve()
    
    # 集合重叠检测
    if resolved_target == SKILL_ROOT:
        print(f"\n⛔  **SECURITY ERROR: Spore Isolation Violation [{tool_name}]**")
        print(f"    Target path collision detected: {resolved_target}")
        print(f"    You are attempting to run '{tool_name}' on the CDD Skill Root itself.")
        print("\n    The CDD Skill is a tool (The Spore), not the target soil.")
        print("    Please specify an external target project path explicitly.")
        print(f"\n    Example: python scripts/{tool_name} ... --target ../your-project\n")
        sys.exit(100)  # Exit Code 100 for Isolation Violation