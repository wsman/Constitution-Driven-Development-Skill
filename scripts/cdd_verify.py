#!/usr/bin/env python3
"""
CDD Skill Verification Tool (cdd_verify.py) v2.0.0
==================================================
验证CDD技能的完整性，包括文件、依赖、模板和配置检查。

宪法依据: §100.3, §101, §106.1

Usage:
    python scripts/cdd_verify.py                    # 基本验证
    python scripts/cdd_verify.py --full             # 完整验证
    python scripts/cdd_verify.py --fix              # 尝试自动修复
    python scripts/cdd_verify.py --json             # JSON格式输出
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

# 添加项目根目录到Python路径
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SKILL_ROOT))

VERSION = "2.0.0"

# -----------------------------------------------------------------------------
# 核心文件列表
# -----------------------------------------------------------------------------

CORE_FILES = {
    "root": [
        "README.md",
        "SKILL.md",
        "QUICK_START.md",
        "reference.md",
        "pyproject.toml",
        "requirements.txt",
        "pytest.ini",
        "Makefile",
    ],
    "scripts": [
        "scripts/cdd_check_env.py",
        "scripts/cdd_feature.py",
        "scripts/cdd_auditor.py",
        "scripts/cdd_entropy.py",
        "scripts/cdd_claude_bridge.py",
        "scripts/cdd_utils.py",
    ],
    "core": [
        "core/__init__.py",
        "core/constitution_core.py",
        "core/constants.py",
        "core/exceptions.py",
        "core/audit_service.py",
        "core/entropy_service.py",
        "core/feature_service.py",
        "core/state_transition_service.py",
        "core/state_validation_service.py",
    ],
    "utils": [
        "utils/__init__.py",
        "utils/cache_manager.py",
        "utils/entropy_utils.py",
        "utils/file_utils.py",
        "utils/logger.py",
        "utils/spore_utils.py",
        "utils/version_utils.py",
    ],
    "templates_t0": [
        "templates/t0_core/active_context.md",
        "templates/t0_core/knowledge_graph.md",
        "templates/t0_core/basic_law_index.md",
        "templates/t0_core/operational_law_index.md",
    ],
    "templates_t1": [
        "templates/t1_axioms/system_patterns.md",
        "templates/t1_axioms/tech_context.md",
        "templates/t1_axioms/behavior_context.md",
    ],
    "templates_t2_protocols": [
        "templates/t2_protocols/WF-001_clarify_workflow.md",
        "templates/t2_protocols/WF-201_cdd_workflow.md",
        "templates/t2_protocols/WF-206_refactor_protocol.md",
    ],
    "templates_t2_standards": [
        "templates/t2_standards/DS-007_context_management.md",
        "templates/t2_standards/DS-039_tool_bridge.md",
        "templates/t2_standards/DS-050_feature_specification.md",
        "templates/t2_standards/DS-051_implementation_plan.md",
        "templates/t2_standards/DS-052_atomic_tasks.md",
        "templates/t2_standards/DS-053_quality_checklist.md",
        "templates/t2_standards/DS-054_environment_hardening.md",
        "templates/t2_standards/DS-055_entropy_optimizer_spec.md",
        "templates/t2_standards/DS-060_code_review.md",
    ],
}

# -----------------------------------------------------------------------------
# 依赖列表
# -----------------------------------------------------------------------------

DEPENDENCIES = {
    "python": {
        "min_version": (3, 8),
        "check_fn": lambda: check_python_version(),
        "install_cmd": None,
        "required": True,
    },
    "pytest": {
        "min_version": (6, 0),
        "check_fn": lambda: check_pytest_version(),
        "install_cmd": "pip install pytest",
        "required": True,
    },
    "pyyaml": {
        "min_version": (6, 0),
        "check_fn": lambda: check_pyyaml_version(),
        "install_cmd": "pip install pyyaml",
        "required": True,
    },
}

# -----------------------------------------------------------------------------
# 检查函数
# -----------------------------------------------------------------------------

def check_python_version() -> Tuple[bool, str, Optional[str]]:
    """检查Python版本"""
    min_version = (3, 8)
    current_version = (sys.version_info.major, sys.version_info.minor)
    
    if current_version >= min_version:
        version_str = f"{current_version[0]}.{current_version[1]}.{sys.version_info.micro}"
        return True, version_str, None
    
    version_str = f"{current_version[0]}.{current_version[1]}.{sys.version_info.micro}"
    return False, version_str, f"Python {min_version[0]}.{min_version[1]}+ required"

def check_pytest_version() -> Tuple[bool, str, Optional[str]]:
    """检查pytest版本"""
    try:
        import pytest
        version = pytest.__version__
        import re
        match = re.search(r'(\d+)\.(\d+)\.(\d+)', version)
        if match:
            major = int(match.group(1))
            if major >= 6:
                return True, version, None
        return True, version, f"pytest 6.0+ recommended"
    except ImportError:
        return False, None, "pytest not installed"

def check_pyyaml_version() -> Tuple[bool, str, Optional[str]]:
    """检查PyYAML版本"""
    try:
        import yaml
        return True, yaml.__version__, None
    except ImportError:
        return False, None, "PyYAML not installed"

def check_file_exists(file_path: Path) -> Tuple[bool, Optional[str]]:
    """检查文件是否存在"""
    if file_path.exists():
        return True, None
    return False, f"文件不存在: {file_path.relative_to(SKILL_ROOT)}"

def check_file_readable(file_path: Path) -> Tuple[bool, Optional[str]]:
    """检查文件是否可读"""
    if not file_path.exists():
        return False, f"文件不存在: {file_path}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)  # 读取前1KB验证
        return True, None
    except Exception as e:
        return False, f"文件不可读: {file_path} - {e}"

# -----------------------------------------------------------------------------
# 验证函数
# -----------------------------------------------------------------------------

def verify_core_files(full: bool = False) -> Dict[str, Any]:
    """验证核心文件完整性"""
    results = {
        "category": "core_files",
        "description": "核心文件完整性",
        "status": "passed",
        "files_checked": 0,
        "files_passed": 0,
        "issues": []
    }
    
    categories_to_check = ["root", "scripts", "core", "utils"]
    if full:
        categories_to_check.extend(["templates_t0", "templates_t1", 
                                   "templates_t2_protocols", "templates_t2_standards"])
    
    for category in categories_to_check:
        if category not in CORE_FILES:
            continue
        
        for file_path_str in CORE_FILES[category]:
            file_path = SKILL_ROOT / file_path_str
            results["files_checked"] += 1
            
            passed, error = check_file_exists(file_path)
            if not passed:
                results["status"] = "failed"
                results["issues"].append({"file": file_path_str, "error": error})
                continue
            
            if full:
                passed, error = check_file_readable(file_path)
                if not passed:
                    results["status"] = "failed"
                    results["issues"].append({"file": file_path_str, "error": error})
                    continue
            
            results["files_passed"] += 1
    
    return results

def verify_dependencies(full: bool = False) -> Dict[str, Any]:
    """验证依赖完整性"""
    results = {
        "category": "dependencies",
        "description": "依赖完整性",
        "status": "passed",
        "deps_checked": 0,
        "deps_passed": 0,
        "issues": []
    }
    
    for dep_name, dep_config in DEPENDENCIES.items():
        results["deps_checked"] += 1
        
        installed, version, error = dep_config["check_fn"]()
        
        if not installed:
            results["status"] = "failed"
            results["issues"].append({
                "dependency": dep_name,
                "error": error,
                "install_cmd": dep_config.get("install_cmd"),
                "required": dep_config.get("required", False)
            })
            continue
        
        results["deps_passed"] += 1
    
    # 检查Python模块导入
    if full:
        modules_to_check = [
            ("core.constitution_core", "core/constitution_core.py"),
            ("core.audit_service", "core/audit_service.py"),
            ("core.entropy_service", "core/entropy_service.py"),
            ("core.feature_service", "core/feature_service.py"),
            ("utils.spore_utils", "utils/spore_utils.py"),
        ]
        
        for module_name, file_path in modules_to_check:
            try:
                __import__(module_name)
            except ImportError as e:
                results["status"] = "failed"
                results["issues"].append({
                    "module": module_name,
                    "error": f"导入失败: {e}",
                    "file": file_path
                })
    
    return results

def verify_config_files() -> Dict[str, Any]:
    """验证配置文件完整性"""
    results = {
        "category": "config_files",
        "description": "配置文件完整性",
        "status": "passed",
        "files_checked": 0,
        "files_passed": 0,
        "issues": []
    }
    
    config_files = [
        "pytest.ini",
        "pyproject.toml",
        "requirements.txt",
    ]
    
    for file_name in config_files:
        file_path = SKILL_ROOT / file_name
        results["files_checked"] += 1
        
        passed, error = check_file_exists(file_path)
        if not passed:
            results["status"] = "failed"
            results["issues"].append({"file": file_name, "error": error})
            continue
        
        # 验证YAML配置文件（如果存在）
        if file_name.endswith('.yaml') or file_name.endswith('.yml'):
            try:
                import yaml
                with open(file_path, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
            except Exception as e:
                results["status"] = "failed"
                results["issues"].append({
                    "file": file_name,
                    "error": f"YAML解析失败: {e}"
                })
                continue
        
        results["files_passed"] += 1
    
    return results

def verify_structure() -> Dict[str, Any]:
    """验证目录结构"""
    results = {
        "category": "structure",
        "description": "目录结构",
        "status": "passed",
        "directories_checked": 0,
        "directories_passed": 0,
        "issues": []
    }
    
    required_dirs = [
        "core",
        "scripts",
        "templates",
        "utils",
        "reference",
        "claude",
    ]
    
    for dir_name in required_dirs:
        dir_path = SKILL_ROOT / dir_name
        results["directories_checked"] += 1
        
        if not dir_path.exists() or not dir_path.is_dir():
            results["status"] = "failed"
            results["issues"].append({
                "directory": dir_name,
                "error": "目录不存在"
            })
            continue
        
        results["directories_passed"] += 1
    
    return results


# -----------------------------------------------------------------------------
# 模板必需文件
# -----------------------------------------------------------------------------

REQUIRED_TEMPLATES = {
    "t0_core": [
        "templates/t0_core/active_context.md",
        "templates/t0_core/knowledge_graph.md",
        "templates/t0_core/basic_law_index.md",
        "templates/t0_core/operational_law_index.md",
        "templates/t0_core/tools_law_index.md",
    ],
    "t1_axioms": [
        "templates/t1_axioms/behavior_context.md",
        "templates/t1_axioms/system_patterns.md",
        "templates/t1_axioms/tech_context.md",
    ],
    "t2_protocols": [
        "templates/t2_protocols/WF-001_clarify_workflow.md",
        "templates/t2_protocols/WF-201_cdd_workflow.md",
        "templates/t2_protocols/WF-206_refactor_protocol.md",
    ],
    "t2_standards": [
        "templates/t2_standards/DS-007_context_management.md",
        "templates/t2_standards/DS-039_tool_bridge.md",
        "templates/t2_standards/DS-050_feature_specification.md",
        "templates/t2_standards/DS-051_implementation_plan.md",
        "templates/t2_standards/DS-052_atomic_tasks.md",
        "templates/t2_standards/DS-053_quality_checklist.md",
    ],
    "t3_documentation": [
        "templates/t3_documentation/unified_docs.md",
    ],
}


def verify_templates(full: bool = False) -> Dict[str, Any]:
    """验证模板完整性"""
    results = {
        "category": "templates",
        "description": "模板完整性",
        "status": "passed",
        "templates_checked": 0,
        "templates_passed": 0,
        "issues": [],
        "details": {}
    }
    
    for group_name, templates in REQUIRED_TEMPLATES.items():
        group_passed = 0
        group_total = len(templates)
        
        for template_path_str in templates:
            template_path = SKILL_ROOT / template_path_str
            results["templates_checked"] += 1
            
            if not template_path.exists():
                results["status"] = "failed"
                results["issues"].append({
                    "template": template_path_str,
                    "group": group_name,
                    "error": "模板文件不存在"
                })
                continue
            
            # 检查模板文件是否有内容
            if full:
                try:
                    content = template_path.read_text(encoding='utf-8')
                    if len(content.strip()) < 50:  # 模板至少要有50字符
                        results["status"] = "warning"
                        results["issues"].append({
                            "template": template_path_str,
                            "group": group_name,
                            "error": "模板内容过短，可能是空模板"
                        })
                        continue
                    
                    # 检查是否包含未解析的模板变量
                    import re
                    unresolved_vars = re.findall(r'\{\{[A-Z_]+\}\}', content)
                    # 注意：模板文件中包含模板变量是正常的
                    
                except Exception as e:
                    results["status"] = "failed"
                    results["issues"].append({
                        "template": template_path_str,
                        "group": group_name,
                        "error": f"无法读取模板: {e}"
                    })
                    continue
            
            results["templates_passed"] += 1
            group_passed += 1
        
        results["details"][group_name] = {
            "total": group_total,
            "passed": group_passed
        }
    
    return results

# -----------------------------------------------------------------------------
# 修复函数
# -----------------------------------------------------------------------------

def attempt_fix(issue: Dict[str, Any], verbose: bool = False) -> Tuple[bool, str]:
    """尝试修复问题"""
    issue_type = issue.get("type", "unknown")
    
    if issue_type == "dependency":
        install_cmd = issue.get("install_cmd")
        if not install_cmd:
            return False, "无自动修复方案"
        
        if verbose:
            print(f"尝试安装: {issue.get('dependency')}")
            print(f"命令: {install_cmd}")
        
        try:
            result = subprocess.run(install_cmd, shell=True,
                                   capture_output=True, text=True,
                                   timeout=60)
            
            if result.returncode != 0:
                return False, f"安装失败: {result.stderr[:100]}"
            
            return True, "安装成功"
        except Exception as e:
            return False, f"安装错误: {e}"
    
    return False, "无法自动修复"

# -----------------------------------------------------------------------------
# 输出格式化
# -----------------------------------------------------------------------------

def format_text_output(results: List[Dict[str, Any]], show_details: bool = False) -> str:
    """文本格式输出"""
    lines = [f"🔍 CDD技能验证 v{VERSION}"]
    lines.append(f"{'='*50}")
    
    overall_status = "✅ 通过" if all(r["status"] == "passed" for r in results) else "❌ 失败"
    lines.append(f"总体状态: {overall_status}\n")
    
    for result in results:
        icon = "✅" if result["status"] == "passed" else "❌"
        lines.append(f"{icon} {result['description']}")
        
        if result["status"] == "passed":
            if "files_checked" in result:
                lines.append(f"   文件: {result['files_passed']}/{result['files_checked']}")
            if "deps_checked" in result:
                lines.append(f"   依赖: {result['deps_passed']}/{result['deps_checked']}")
            if "directories_checked" in result:
                lines.append(f"   目录: {result['directories_passed']}/{result['directories_checked']}")
        else:
            lines.append(f"   ❌ 发现 {len(result.get('issues', []))} 个问题")
            
            if show_details:
                for issue in result.get("issues", []):
                    lines.append(f"      • {issue.get('error', 'Unknown error')}")
                    if "install_cmd" in issue:
                        lines.append(f"        修复: {issue['install_cmd']}")
        
        lines.append("")
    
    # 汇总信息
    total_issues = sum(len(r.get("issues", [])) for r in results)
    if total_issues > 0:
        lines.append(f"📊 总计发现 {total_issues} 个问题")
        lines.append(f"💡 运行 'python scripts/cdd_verify.py --fix' 尝试自动修复")
    
    return "\n".join(lines)

def format_json_output(results: List[Dict[str, Any]]) -> str:
    """JSON格式输出"""
    output = {
        "version": VERSION,
        "timestamp": subprocess.run(["date", "-Iseconds"],
                                   capture_output=True, text=True).stdout.strip(),
        "overall_status": "passed" if all(r["status"] == "passed" for r in results) else "failed",
        "results": results,
        "summary": {
            "categories_checked": len(results),
            "categories_passed": sum(1 for r in results if r["status"] == "passed"),
            "total_issues": sum(len(r.get("issues", [])) for r in results),
        }
    }
    return json.dumps(output, indent=2, ensure_ascii=False)

# -----------------------------------------------------------------------------
# 主函数
# -----------------------------------------------------------------------------

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description=f"CDD Skill Verification v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/cdd_verify.py              # 基本验证
  python scripts/cdd_verify.py --full       # 完整验证
  python scripts/cdd_verify.py --fix        # 尝试自动修复
  python scripts/cdd_verify.py --json       # JSON格式输出
        """
    )
    
    parser.add_argument("--full", "-f", action="store_true",
                       help="完整验证（包括模板和模块导入）")
    parser.add_argument("--fix", action="store_true",
                       help="尝试自动修复问题")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="详细输出")
    parser.add_argument("--json", "-j", action="store_true",
                       help="JSON格式输出")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="安静模式（仅显示错误）")
    
    args = parser.parse_args()
    
    # 执行验证
    results = []
    
    # 1. 验证目录结构
    results.append(verify_structure())
    
    # 2. 验证核心文件
    results.append(verify_core_files(full=args.full))
    
    # 3. 验证依赖
    results.append(verify_dependencies(full=args.full))
    
    # 4. 验证配置文件
    results.append(verify_config_files())
    
    # 5. 验证模板（完整模式下）
    if args.full:
        results.append(verify_templates(full=True))
    
    # 尝试修复
    if args.fix:
        fixes_attempted = 0
        fixes_succeeded = 0
        
        for result in results:
            if result["status"] == "failed":
                for issue in result.get("issues", []):
                    if "install_cmd" in issue:
                        fix_issue = issue.copy()
                        fix_issue["type"] = "dependency"
                        
                        success, msg = attempt_fix(fix_issue, args.verbose)
                        fixes_attempted += 1
                        
                        if success:
                            fixes_succeeded += 1
                            # 重新验证
                            if result["category"] == "dependencies":
                                new_result = verify_dependencies(full=args.full)
                                result["deps_checked"] = new_result["deps_checked"]
                                result["deps_passed"] = new_result["deps_passed"]
                                result["issues"] = new_result["issues"]
                                result["status"] = new_result["status"]
        
        if not args.quiet and fixes_attempted > 0:
            print(f"\n🔧 修复摘要:")
            print(f"   尝试修复: {fixes_attempted}")
            print(f"   成功修复: {fixes_succeeded}")
            print(f"   失败修复: {fixes_attempted - fixes_succeeded}")
            print()
    
    # 输出结果
    if args.json:
        print(format_json_output(results))
    else:
        if not args.quiet:
            print(format_text_output(results, show_details=args.verbose))
        else:
            # 仅显示失败信息
            failed_results = [r for r in results if r["status"] == "failed"]
            if failed_results:
                for result in failed_results:
                    print(f"❌ {result['description']}")
                    for issue in result.get("issues", []):
                        print(f"   • {issue.get('error', 'Unknown error')}")
    
    # 设置退出码
    overall_passed = all(r["status"] == "passed" for r in results)
    sys.exit(0 if overall_passed else 1)

if __name__ == "__main__":
    main()