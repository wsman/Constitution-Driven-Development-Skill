#!/usr/bin/env python3
"""
CDD Environment Check (cdd_check_env.py) v2.0.0
===============================================
检查 CDD 技能运行环境是否符合要求

宪法依据: §100.3, §101, §102

Usage:
    python scripts/cdd_check_env.py                # 基本检查
    python scripts/cdd_check_env.py --verbose      # 详细输出
    python scripts/cdd_check_env.py --essential    # 仅检查必需依赖
    python scripts/cdd_check_env.py --json         # JSON格式输出
    python scripts/cdd_check_env.py --fix          # 尝试自动修复
"""

import sys
import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import importlib.util

# 添加项目根目录到Python路径
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SKILL_ROOT))

try:
    from utils.spore_utils import check_spore_isolation
    SPORE_UTILS_AVAILABLE = True
except ImportError:
    SPORE_UTILS_AVAILABLE = False

VERSION = "2.0.0"

# -----------------------------------------------------------------------------
# 依赖定义
# -----------------------------------------------------------------------------

class Dependency:
    """依赖项定义"""
    
    def __init__(self, name: str, required: bool, description: str, 
                 check_fn=None, install_cmd: Optional[str] = None,
                 min_version: Optional[str] = None):
        self.name = name
        self.required = required
        self.description = description
        self.check_fn = check_fn or (lambda: self._default_check())
        self.install_cmd = install_cmd
        self.min_version = min_version
        self.installed = False
        self.version = None
        self.error = None
        self.fix_suggestion = None
    
    def _default_check(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """默认检查函数"""
        # 检查命令是否存在
        if shutil.which(self.name):
            self.installed = True
            return True, self._get_version(), None
        return False, None, f"Command '{self.name}' not found in PATH"
    
    def _get_version(self) -> Optional[str]:
        """获取版本号"""
        try:
            if self.name == "python3":
                return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            elif self.name == "pytest":
                import pytest
                return pytest.__version__
            elif self.name == "tree":
                result = subprocess.run(["tree", "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip().split()[-1]
            elif self.name == "PyYAML":
                import yaml
                return yaml.__version__
        except Exception as e:
            return f"Unknown (error: {e})"
        return None
    
    def check(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """执行检查"""
        try:
            return self.check_fn()
        except Exception as e:
            return False, None, f"Check failed: {e}"
    
    def get_status_icon(self) -> str:
        """获取状态图标"""
        if self.installed:
            return "✅" if self.required else "ℹ️"
        return "❌" if self.required else "⚠️"

# -----------------------------------------------------------------------------
# 依赖检查函数
# -----------------------------------------------------------------------------

def check_python() -> Tuple[bool, Optional[str], Optional[str]]:
    """检查 Python 版本"""
    min_version = (3, 8)
    current_version = (sys.version_info.major, sys.version_info.minor)
    
    if current_version >= min_version:
        version_str = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        return True, version_str, None
    
    version_str = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    return False, version_str, f"Python {min_version[0]}.{min_version[1]}+ required, found {version_str}"

def check_pytest() -> Tuple[bool, Optional[str], Optional[str]]:
    """检查 pytest"""
    try:
        import pytest
        version = pytest.__version__
        # 解析版本号
        import re
        match = re.search(r'(\d+)\.(\d+)\.(\d+)', version)
        if match:
            major = int(match.group(1))
            if major >= 6:
                return True, version, None
        return True, version, f"pytest 6.0+ recommended, found {version}"
    except ImportError:
        return False, None, "pytest not installed"

def check_pyyaml() -> Tuple[bool, Optional[str], Optional[str]]:
    """检查 PyYAML"""
    try:
        import yaml
        return True, yaml.__version__, None
    except ImportError:
        return False, None, "PyYAML not installed"

def check_tree() -> Tuple[bool, Optional[str], Optional[str]]:
    """检查 tree 命令"""
    if shutil.which("tree"):
        try:
            result = subprocess.run(["tree", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip().split()[-1]
                return True, version, None
        except Exception:
            pass
        return True, "unknown", None
    return False, None, "tree command not found (optional for directory visualization)"

def check_git() -> Tuple[bool, Optional[str], Optional[str]]:
    """检查 git"""
    if shutil.which("git"):
        try:
            result = subprocess.run(["git", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.split()[2]
                return True, version, None
        except Exception:
            pass
        return True, "unknown", None
    return False, None, "git not found (optional for version control)"

def check_deepseek_api() -> Tuple[bool, Optional[str], Optional[str]]:
    """检查 DeepSeek API 配置"""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if api_key:
        return True, "configured", None
    return False, None, "DEEPSEEK_API_KEY not set (optional for Gate 4 external audit)"

# -----------------------------------------------------------------------------
# 依赖列表
# -----------------------------------------------------------------------------

DEPENDENCIES = [
    Dependency(
        name="python3",
        required=True,
        description="Python 3.8+",
        check_fn=check_python,
        install_cmd=None,  # 系统级依赖
        min_version="3.8"
    ),
    Dependency(
        name="pytest",
        required=True,
        description="pytest 6.0+ (behavior verification)",
        check_fn=check_pytest,
        install_cmd="pip install pytest",
        min_version="6.0"
    ),
    Dependency(
        name="PyYAML",
        required=True,
        description="PyYAML (configuration parsing)",
        check_fn=check_pyyaml,
        install_cmd="pip install pyyaml",
        min_version="6.0"
    ),
    Dependency(
        name="tree",
        required=False,
        description="tree command (directory visualization)",
        check_fn=check_tree,
        install_cmd="apt install tree  # Ubuntu/Debian\nbrew install tree  # macOS",
        min_version=None
    ),
    Dependency(
        name="git",
        required=False,
        description="Git (version control)",
        check_fn=check_git,
        install_cmd="apt install git  # Ubuntu/Debian\nbrew install git  # macOS",
        min_version=None
    ),
    Dependency(
        name="deepseek-api",
        required=False,
        description="DeepSeek API key (Gate 4 external audit)",
        check_fn=check_deepseek_api,
        install_cmd="export DEEPSEEK_API_KEY='your-key-here'",
        min_version=None
    ),
]

# -----------------------------------------------------------------------------
# 输出格式化
# -----------------------------------------------------------------------------

def format_tree_output(results: List[Dict[str, Any]], essential_only: bool = False) -> str:
    """树状格式化输出"""
    lines = [f"🔍 CDD 环境检查 v{VERSION}"]
    
    required_passed = 0
    required_total = 0
    optional_passed = 0
    optional_total = 0
    
    for i, dep in enumerate(results):
        if essential_only and not dep["required"]:
            continue
        
        if dep["required"]:
            required_total += 1
            if dep["installed"]:
                required_passed += 1
        else:
            optional_total += 1
            if dep["installed"]:
                optional_passed += 1
        
        prefix = "├── " if i < len(results) - 1 else "└── "
        icon = dep["icon"]
        name = dep["name"]
        version_info = f" ({dep['version']})" if dep["version"] else ""
        
        lines.append(f"{prefix}{icon} {name}{version_info} ... {dep['description']}")
        
        if dep["error"] and not dep["installed"]:
            indent = "    " if i < len(results) - 1 else "    "
            lines.append(f"{indent}  ❗ {dep['error']}")
            if dep["fix_suggestion"]:
                lines.append(f"{indent}  💡 修复建议: {dep['fix_suggestion']}")
    
    # 汇总信息
    total_passed = required_passed + optional_passed
    total_checked = required_total + optional_total
    
    summary = []
    if required_total > 0:
        summary.append(f"{required_passed}/{required_total} 必需依赖")
    if optional_total > 0 and not essential_only:
        summary.append(f"{optional_passed}/{optional_total} 可选依赖")
    
    status_icon = "✅" if required_passed == required_total else "⚠️"
    lines.append(f"\n{status_icon} 环境检查完成: {'，'.join(summary)}")
    
    if required_passed < required_total:
        lines.append(f"❌ 必需依赖不满足，请使用 --fix 尝试修复")
    
    return "\n".join(lines)

def format_json_output(results: List[Dict[str, Any]]) -> str:
    """JSON格式化输出"""
    output = {
        "version": VERSION,
        "timestamp": subprocess.run(["date", "-Iseconds"], 
                                   capture_output=True, text=True).stdout.strip(),
        "summary": {
            "required_passed": sum(1 for d in results if d["required"] and d["installed"]),
            "required_total": sum(1 for d in results if d["required"]),
            "optional_passed": sum(1 for d in results if not d["required"] and d["installed"]),
            "optional_total": sum(1 for d in results if not d["required"]),
            "all_passed": all(d["installed"] for d in results if d["required"]),
        },
        "dependencies": results,
        "environment": {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": sys.platform,
            "cdd_skill_root": str(SKILL_ROOT),
        }
    }
    return json.dumps(output, indent=2, ensure_ascii=False)

# -----------------------------------------------------------------------------
# 修复函数
# -----------------------------------------------------------------------------

def attempt_fix(dep: Dependency, verbose: bool = False) -> Tuple[bool, str]:
    """尝试修复依赖"""
    if not dep.install_cmd:
        return False, "No automatic fix available (system dependency)"
    
    if verbose:
        print(f"尝试修复: {dep.name} ({dep.description})")
        print(f"命令: {dep.install_cmd}")
    
    try:
        # 处理多行命令
        commands = dep.install_cmd.split('\n')
        for cmd in commands:
            cmd = cmd.strip()
            if not cmd or cmd.startswith('#'):
                continue
            
            # 如果是导出命令，设置环境变量
            if cmd.startswith('export '):
                parts = cmd[7:].split('=', 1)
                if len(parts) == 2:
                    var_name = parts[0].strip()
                    var_value = parts[1].strip().strip("'\"")
                    os.environ[var_name] = var_value
                    if verbose:
                        print(f"设置环境变量: {var_name}=***")
                continue
            
            # 执行安装命令
            if verbose:
                print(f"执行: {cmd}")
            
            result = subprocess.run(cmd, shell=True, 
                                   capture_output=True, text=True,
                                   timeout=60)
            
            if result.returncode != 0:
                if verbose:
                    print(f"失败: {result.stderr[:200]}")
                return False, f"Installation failed: {result.stderr[:100]}"
        
        return True, "Installation attempted"
    
    except subprocess.TimeoutExpired:
        return False, "Installation timeout"
    except Exception as e:
        return False, f"Installation error: {e}"

# -----------------------------------------------------------------------------
# 主函数
# -----------------------------------------------------------------------------

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description=f"CDD Environment Check v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/cdd_check_env.py           # 基本检查
  python scripts/cdd_check_env.py --fix     # 尝试自动修复
  python scripts/cdd_check_env.py --json    # JSON格式输出
  python scripts/cdd_check_env.py --quiet   # 仅显示错误
        
宪法依据: §100.3, §101, §102
        """
    )
    
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="详细输出模式")
    parser.add_argument("--quiet", "-q", action="store_true", 
                       help="安静模式（仅显示错误）")
    parser.add_argument("--essential", "-e", action="store_true", 
                       help="仅检查必需依赖")
    parser.add_argument("--json", "-j", action="store_true", 
                       help="JSON格式输出")
    parser.add_argument("--fix", "-f", action="store_true", 
                       help="尝试自动修复缺失依赖")
    parser.add_argument("--list", "-l", action="store_true", 
                       help="列出所有依赖项")
    
    args = parser.parse_args()
    
    if args.list:
        print(f"CDD 环境依赖列表 (v{VERSION})")
        print("=" * 50)
        for dep in DEPENDENCIES:
            req = "✅ 必需" if dep.required else "ℹ️  可选"
            print(f"{req}: {dep.name} - {dep.description}")
            if dep.min_version:
                print(f"     最低版本: {dep.min_version}")
            if dep.install_cmd:
                print(f"     安装命令: {dep.install_cmd.split()[0]}...")
            print()
        return
    
    # 执行检查
    results = []
    fixes_attempted = 0
    fixes_succeeded = 0
    
    for dep in DEPENDENCIES:
        if args.essential and not dep.required:
            continue
        
        # 执行检查
        installed, version, error = dep.check()
        dep.installed = installed
        dep.version = version
        dep.error = error
        
        # 如果检查失败且启用了修复，尝试修复
        fix_result = None
        if not installed and dep.required and args.fix:
            fix_success, fix_msg = attempt_fix(dep, args.verbose)
            fixes_attempted += 1
            if fix_success:
                fixes_succeeded += 1
                # 重新检查
                installed, version, error = dep.check()
                dep.installed = installed
                dep.version = version
                dep.error = error
            fix_result = fix_msg
        
        # 生成修复建议
        fix_suggestion = None
        if not installed and dep.install_cmd:
            fix_suggestion = dep.install_cmd.split('\n')[0]
        
        results.append({
            "name": dep.name,
            "description": dep.description,
            "required": dep.required,
            "installed": dep.installed,
            "version": version,
            "error": error,
            "fix_suggestion": fix_suggestion,
            "fix_attempted": fix_result is not None,
            "fix_result": fix_result,
            "icon": dep.get_status_icon(),
        })
    
    # 输出结果
    if args.json:
        print(format_json_output(results))
    else:
        if not args.quiet:
            print(format_tree_output(results, args.essential))
        
        # 如果需要，显示修复摘要
        if args.fix and fixes_attempted > 0:
            print(f"\n🔧 修复摘要:")
            print(f"   尝试修复: {fixes_attempted}")
            print(f"   成功修复: {fixes_succeeded}")
            print(f"   失败修复: {fixes_attempted - fixes_succeeded}")
    
    # 设置退出码
    required_deps = [d for d in results if d["required"]]
    all_required_met = all(d["installed"] for d in required_deps)
    
    sys.exit(0 if all_required_met else 1)

# -----------------------------------------------------------------------------
# Claude Code 集成接口
# -----------------------------------------------------------------------------

def check_environment_claude(**kwargs) -> Dict[str, Any]:
    """
    Claude Code 环境检查接口
    
    Returns:
        Dict[str, Any]: 检查结果
    """
    results = []
    
    for dep in DEPENDENCIES:
        if kwargs.get("essential_only") and not dep.required:
            continue
        
        installed, version, error = dep.check()
        dep.installed = installed
        dep.version = version
        dep.error = error
        
        results.append({
            "name": dep.name,
            "description": dep.description,
            "required": dep.required,
            "installed": installed,
            "version": version,
            "error": error,
            "status": "passed" if installed else "failed",
        })
    
    required_deps = [d for d in results if d["required"]]
    all_required_met = all(d["installed"] for d in required_deps)
    
    return {
        "success": all_required_met,
        "all_required_met": all_required_met,
        "required_passed": sum(1 for d in required_deps if d["installed"]),
        "required_total": len(required_deps),
        "results": results,
        "environment_info": {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": sys.platform,
            "cdd_skill_root": str(SKILL_ROOT),
        }
    }

if __name__ == "__main__":
    main()