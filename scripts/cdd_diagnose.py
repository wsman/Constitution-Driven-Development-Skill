#!/usr/bin/env python3
"""
CDD 综合诊断工具 (cdd_diagnose.py) v2.0.0
=========================================
运行所有CDD检查的综合诊断工具：环境检查、技能验证、宪法审计。

宪法依据: §100.3, §101, §102, §106.1

Usage:
    python scripts/cdd_diagnose.py                    # 基本诊断
    python scripts/cdd_diagnose.py --fix              # 尝试自动修复
    python scripts/cdd_diagnose.py --json             # JSON格式输出
    python scripts/cdd_diagnose.py --target /path     # 诊断外部项目
    python scripts/cdd_diagnose.py --summary          # 仅显示摘要
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import argparse

# 添加项目根目录到Python路径
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SKILL_ROOT))

VERSION = "2.0.0"

# -----------------------------------------------------------------------------
# 诊断检查定义
# -----------------------------------------------------------------------------

class DiagnosticCheck:
    """诊断检查基类"""
    
    def __init__(self, name: str, description: str, command: str, 
                 required: bool = True, timeout: int = 120):
        self.name = name
        self.description = description
        self.command = command
        self.required = required
        self.timeout = timeout
        self.result: Optional[Dict[str, Any]] = None
        self.duration: float = 0.0
    
    def run(self, verbose: bool = False) -> Dict[str, Any]:
        """运行检查"""
        start_time = time.time()
        
        try:
            if verbose:
                print(f"🔍 运行检查: {self.name}")
            
            # 执行命令
            result = subprocess.run(
                self.command,
                shell=True,
                cwd=SKILL_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=self.timeout
            )
            
            self.duration = time.time() - start_time
            
            # 解析输出
            return self._parse_result(result, verbose)
            
        except subprocess.TimeoutExpired:
            self.duration = time.time() - start_time
            return {
                "status": "timeout",
                "exit_code": 1,
                "message": f"检查超时 ({self.timeout}秒)",
                "stdout": "",
                "stderr": f"Timeout after {self.timeout}s",
                "duration": self.duration,
                "suggestions": ["增加超时时间", "检查系统负载"]
            }
        except Exception as e:
            self.duration = time.time() - start_time
            return {
                "status": "error",
                "exit_code": 1,
                "message": f"检查失败: {e}",
                "stdout": "",
                "stderr": str(e),
                "duration": self.duration,
                "suggestions": ["检查命令语法", "确保依赖项已安装"]
            }
    
    def _parse_result(self, result: subprocess.CompletedProcess, verbose: bool) -> Dict[str, Any]:
        """解析命令结果"""
        status = "passed" if result.returncode == 0 else "failed"
        
        # 尝试解析JSON输出
        json_output = None
        if result.stdout.strip() and result.stdout.strip().startswith("{"):
            try:
                json_output = json.loads(result.stdout)
            except json.JSONDecodeError:
                pass
        
        return {
            "status": status,
            "exit_code": result.returncode,
            "message": f"退出码: {result.returncode}" if status == "failed" else "检查完成",
            "stdout": result.stdout[:500] if not json_output else "JSON output parsed",
            "stderr": result.stderr[:500] if result.stderr else "",
            "json_output": json_output,
            "duration": self.duration,
            "parsed_successfully": json_output is not None
        }

# -----------------------------------------------------------------------------
# 检查列表
# -----------------------------------------------------------------------------

DIAGNOSTIC_CHECKS = [
    DiagnosticCheck(
        name="environment_check",
        description="环境依赖检查",
        command="python3 scripts/cdd_check_env.py --json --quiet",
        required=True,
        timeout=60
    ),
    DiagnosticCheck(
        name="skill_verification",
        description="技能完整性验证",
        command="python3 scripts/cdd_verify.py --json --quiet",
        required=True,
        timeout=60
    ),
    DiagnosticCheck(
        name="constitution_audit",
        description="宪法审计 (Gate 1-5)",
        command="python3 scripts/cdd_auditor.py --gate all --format json --quiet",
        required=True,
        timeout=180
    ),
    DiagnosticCheck(
        name="entropy_calculation",
        description="系统熵值计算",
        command="python3 scripts/cdd_entropy.py calculate --json",
        required=False,
        timeout=60
    ),
    DiagnosticCheck(
        name="claude_bridge_status",
        description="Claude Code桥接状态",
        command="python3 scripts/cdd_claude_bridge.py --status",
        required=False,
        timeout=30
    ),
    DiagnosticCheck(
        name="feature_management",
        description="特性管理功能",
        command="python3 scripts/cdd_feature.py list --json",
        required=False,
        timeout=60
    ),
]

# -----------------------------------------------------------------------------
# 输出格式化
# -----------------------------------------------------------------------------

def format_check_result(check: DiagnosticCheck, result: Dict[str, Any], 
                        show_details: bool = False) -> str:
    """格式化单个检查结果"""
    status_icons = {
        "passed": "✅",
        "failed": "❌",
        "timeout": "⏱️",
        "error": "⚠️"
    }
    
    icon = status_icons.get(result["status"], "❓")
    duration = f" ({result['duration']:.2f}s)" if result.get("duration") else ""
    
    lines = []
    lines.append(f"{icon} {check.name}: {check.description}{duration}")
    
    if result["status"] != "passed" or show_details:
        if result["message"]:
            lines.append(f"   消息: {result['message']}")
        
        if result["exit_code"] != 0:
            lines.append(f"   退出码: {result['exit_code']}")
        
        # 显示建议
        suggestions = result.get("suggestions", [])
        if suggestions:
            lines.append(f"   建议:")
            for suggestion in suggestions:
                lines.append(f"      • {suggestion}")
    
    return "\n".join(lines)

def format_summary_report(results: List[Tuple[DiagnosticCheck, Dict[str, Any]]]) -> str:
    """生成摘要报告"""
    total_checks = len(results)
    passed_checks = sum(1 for _, r in results if r["status"] == "passed")
    failed_checks = total_checks - passed_checks
    
    lines = []
    lines.append(f"📊 CDD 综合诊断摘要 (v{VERSION})")
    lines.append(f"{'='*50}")
    lines.append(f"📋 检查总数: {total_checks}")
    lines.append(f"✅ 通过检查: {passed_checks}")
    lines.append(f"❌ 失败检查: {failed_checks}")
    
    if failed_checks > 0:
        lines.append(f"\n🔍 失败检查:")
        for check, result in results:
            if result["status"] != "passed":
                icon = "❌" if result["status"] == "failed" else "⚠️"
                lines.append(f"  {icon} {check.name}: {check.description}")
    
    # 总体状态
    if failed_checks == 0:
        lines.append(f"\n🎉 所有诊断检查通过！CDD系统状态正常。")
    elif failed_checks == 1:
        lines.append(f"\n⚠️  发现1个问题，建议修复。")
    else:
        lines.append(f"\n🚨 发现{failed_checks}个问题，需要立即关注。")
    
    return "\n".join(lines)

def format_detailed_report(results: List[Tuple[DiagnosticCheck, Dict[str, Any]]]) -> str:
    """生成详细报告"""
    lines = []
    lines.append(f"🔍 CDD 综合诊断详细报告 (v{VERSION})")
    lines.append(f"{'='*50}")
    
    for check, result in results:
        lines.append("")
        lines.append(format_check_result(check, result, show_details=True))
    
    lines.append("")
    lines.append(format_summary_report(results))
    
    return "\n".join(lines)

def format_json_report(results: List[Tuple[DiagnosticCheck, Dict[str, Any]]]) -> str:
    """生成JSON报告"""
    report = {
        "version": VERSION,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "project_root": str(SKILL_ROOT),
        "checks": [],
        "summary": {
            "total_checks": len(results),
            "passed_checks": sum(1 for _, r in results if r["status"] == "passed"),
            "failed_checks": sum(1 for _, r in results if r["status"] != "passed"),
            "required_passed": sum(1 for check, r in results if check.required and r["status"] == "passed"),
            "required_total": sum(1 for check in DIAGNOSTIC_CHECKS if check.required),
            "overall_status": "passed" if all(r["status"] == "passed" for _, r in results) else "failed"
        }
    }
    
    for check, result in results:
        check_info = {
            "name": check.name,
            "description": check.description,
            "required": check.required,
            "command": check.command,
            "result": result
        }
        report["checks"].append(check_info)
    
    return json.dumps(report, indent=2, ensure_ascii=False)

# -----------------------------------------------------------------------------
# 文件操作事务管理器
# -----------------------------------------------------------------------------

class FileTransactionManager:
    """文件操作事务管理器"""
    
    def __init__(self):
        self.backup_dir: Optional[Path] = None
        self.backup_files: Dict[str, Tuple[str, str]] = {}
        self.active = False
    
    def begin_transaction(self, transaction_name: str) -> bool:
        """开始事务"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            self.backup_dir = SKILL_ROOT / ".cdd_backups" / f"{transaction_name}_{timestamp}"
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            self.active = True
            return True
        except Exception as e:
            print(f"事务开始失败: {e}")
            return False
    
    def backup_file(self, file_path: Path) -> bool:
        """备份文件"""
        if not self.active:
            return False
        
        try:
            if not file_path.exists():
                return False
            
            backup_path = self.backup_dir / file_path.relative_to(SKILL_ROOT)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.backup_files[str(file_path)] = (str(backup_path), content)
            return True
        except Exception as e:
            print(f"文件备份失败 {file_path}: {e}")
            return False
    
    def commit_transaction(self) -> bool:
        """提交事务（清理备份）"""
        if not self.active:
            return False
        
        try:
            # 删除备份目录
            import shutil
            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)
            
            self.backup_dir = None
            self.backup_files.clear()
            self.active = False
            return True
        except Exception as e:
            print(f"事务提交失败: {e}")
            return False
    
    def rollback_transaction(self) -> bool:
        """回滚事务（恢复所有备份）"""
        if not self.active:
            return False
        
        success = True
        
        try:
            # 恢复所有备份文件
            for original_path, (backup_path, content) in self.backup_files.items():
                try:
                    with open(original_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    print(f"文件恢复失败 {original_path}: {e}")
                    success = False
            
            # 清理备份目录
            if self.backup_dir and self.backup_dir.exists():
                import shutil
                shutil.rmtree(self.backup_dir)
            
            self.backup_dir = None
            self.backup_files.clear()
            self.active = False
            return success
        except Exception as e:
            print(f"事务回滚失败: {e}")
            return False

# -----------------------------------------------------------------------------
# 修复函数 - 增强版
# -----------------------------------------------------------------------------

def attempt_auto_fix_with_checkpoint(check: DiagnosticCheck, result: Dict[str, Any], verbose: bool = False) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """尝试自动修复失败的检查（带检查点）"""
    import shutil
    
    # 为安全起见，创建检查点
    try:
        from cdd_claude_bridge import get_bridge
        bridge = get_bridge()
        checkpoint_result = bridge.create_checkpoint(f"before_fix_{check.name}", {
            "check": check.name,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        })
        
        if not checkpoint_result.get("success", False):
            print("⚠️  检查点创建失败，继续执行修复")
    except ImportError:
        # 如果桥接器不可用，跳过检查点
        pass
    
    # 创建文件事务管理器
    transaction = FileTransactionManager()
    transaction_used = False
    
    try:
        if check.name == "environment_check":
            if verbose:
                print(f"尝试修复环境依赖...")
            
            transaction_used = transaction.begin_transaction("env_check_fix")
            
            fix_result = subprocess.run(
                "python3 scripts/cdd_check_env.py --fix --quiet",
                shell=True,
                cwd=SKILL_ROOT,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if fix_result.returncode == 0:
                if transaction_used:
                    transaction.commit_transaction()
                return True, "环境依赖修复成功", None
            else:
                if transaction_used:
                    transaction.rollback_transaction()
                return False, f"环境依赖修复失败: {fix_result.stderr[:100]}", None
        
        elif check.name == "skill_verification":
            if verbose:
                print(f"尝试修复技能完整性...")
            
            transaction_used = transaction.begin_transaction("skill_verify_fix")
            
            # 首先备份关键文件
            key_files = [
                SKILL_ROOT / "SKILL.md",
                SKILL_ROOT / "README.md",
                SKILL_ROOT / "pyproject.toml",
                SKILL_ROOT / "requirements.txt"
            ]
            
            for file_path in key_files:
                if file_path.exists():
                    transaction.backup_file(file_path)
            
            fix_result = subprocess.run(
                "python3 scripts/cdd_verify.py --fix --quiet",
                shell=True,
                cwd=SKILL_ROOT,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if fix_result.returncode == 0:
                if transaction_used:
                    transaction.commit_transaction()
                return True, "技能完整性修复成功", None
            else:
                if transaction_used:
                    transaction.rollback_transaction()
                return False, f"技能完整性修复失败: {fix_result.stderr[:100]}", None
        
        elif check.name == "constitution_audit":
            # Gate 1版本不一致可以尝试修复
            if "Version mismatch" in str(result.get("stderr", "")) or \
               (result.get("json_output") and "gate_1_failed" in str(result["json_output"])):
                
                if verbose:
                    print(f"尝试修复版本不一致...")
                
                transaction_used = transaction.begin_transaction("version_fix")
                
                # 备份版本相关文件
                version_files = [
                    SKILL_ROOT / "pyproject.toml",
                    SKILL_ROOT / "scripts" / "cdd_auditor.py",
                    SKILL_ROOT / "scripts" / "cdd_diagnose.py"
                ]
                
                for file_path in version_files:
                    if file_path.exists():
                        transaction.backup_file(file_path)
                
                fix_result = subprocess.run(
                    "python3 scripts/cdd_auditor.py --gate 1 --fix --quiet",
                    shell=True,
                    cwd=SKILL_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if fix_result.returncode == 0:
                    if transaction_used:
                        transaction.commit_transaction()
                    return True, "版本一致性修复成功", None
        
        elif check.name == "entropy_calculation":
            # 熵值超标优化
            if result.get("json_output") and "critical" in str(result["json_output"]):
                if verbose:
                    print(f"尝试优化熵值超标...")
                
                transaction_used = transaction.begin_transaction("entropy_optimize")
                
                fix_result = subprocess.run(
                    "python3 scripts/cdd_entropy.py optimize --dry-run --json",
                    shell=True,
                    cwd=SKILL_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=180
                )
                
                if fix_result.returncode == 0:
                    # 分析优化建议
                    optimization_result = None
                    try:
                        optimization_result = json.loads(fix_result.stdout)
                    except:
                        pass
                    
                    if verbose:
                        print(f"生成优化建议，是否执行？")
                    
                    return True, "熵值优化建议已生成", optimization_result
        
        return False, "无自动修复方案", None
        
    except Exception as e:
        # 异常时回滚
        if transaction_used:
            transaction.rollback_transaction()
        
        # 尝试恢复检查点
        try:
            from cdd_claude_bridge import get_bridge
            bridge = get_bridge()
            restore_result = bridge.restore_checkpoint()
            if restore_result.get("success", False):
                return False, f"修复过程中发生异常并恢复检查点: {e}", None
        except:
            pass
        
        return False, f"修复过程中发生异常: {e}", None

def get_intelligent_suggestions(check: DiagnosticCheck, result: Dict[str, Any]) -> List[str]:
    """获取智能修复建议"""
    suggestions = []
    
    if check.name == "environment_check":
        suggestions.append("运行: python scripts/cdd_check_env.py --fix")
        
        # 检查特定错误
        error_text = result.get("stderr", "")
        if "pip not found" in error_text:
            suggestions.append("请安装python-pip包: sudo apt install python3-pip")
        elif "pytest not found" in error_text:
            suggestions.append("请安装pytest: pip install pytest")
        elif "git not found" in error_text:
            suggestions.append("请安装git: sudo apt install git")
    
    elif check.name == "skill_verification":
        suggestions.append("运行: python scripts/cdd_verify.py --fix")
        suggestions.append("检查文件完整性: git status")
        
        # 检查可能的问题
        json_output = result.get("json_output")
        if json_output:
            if "missing_files" in str(json_output):
                suggestions.append("检查缺失的文件，可能需要从模板恢复")
            elif "version_mismatch" in str(json_output):
                suggestions.append("更新版本信息: 运行python scripts/cdd_verify.py --sync-versions")
    
    elif check.name == "constitution_audit":
        suggestions.append("运行: python scripts/cdd_auditor.py --gate all --verbose 查看详细信息")
        
        error_text = result.get("stderr", "") + result.get("stdout", "")
        if "Gate 1" in error_text:
            suggestions.append("版本不一致: 运行python scripts/cdd_auditor.py --gate 1 --fix")
        if "Gate 2" in error_text:
            suggestions.append("测试失败: 运行pytest tests/ -v 查看详细错误")
        if "Gate 3" in error_text:
            suggestions.append("熵值超标: 运行python scripts/cdd_entropy.py analyze")
        if "Gate 4" in error_text:
            suggestions.append("宪法引用不足: 在代码中添加§格式的宪法引用")
        if "Gate 5" in error_text:
            suggestions.append("引用格式错误: 确保宪法引用格式正确（如§100.3）")
    
    elif check.name == "entropy_calculation":
        suggestions.append("运行: python scripts/cdd_entropy.py analyze 查看熵值热点")
        suggestions.append("优化: python scripts/cdd_entropy.py optimize (dry-run模式)")
        
        json_output = result.get("json_output")
        if json_output:
            if "critical" in str(json_output):
                suggestions.append("⚠️ 紧急: 立即处理熵值超标问题")
            elif "warning" in str(json_output):
                suggestions.append("建议在本周内进行优化")
    
    # 通用建议
    suggestions.append("查看详细日志: 添加 --verbose 参数")
    suggestions.append("宪法依据: §100.3 (环境要求), §101 (审计), §102 (熵值)")
    
    return suggestions

# -----------------------------------------------------------------------------
# 修复函数 - 兼容旧版本
# -----------------------------------------------------------------------------

def attempt_auto_fix(check: DiagnosticCheck, result: Dict[str, Any], verbose: bool = False) -> Tuple[bool, str]:
    """尝试自动修复失败的检查（兼容版本）"""
    success, message, _ = attempt_auto_fix_with_checkpoint(check, result, verbose)
    return success, message

# -----------------------------------------------------------------------------
# 主函数
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=f"CDD 综合诊断工具 v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/cdd_diagnose.py              # 基本诊断
  python scripts/cdd_diagnose.py --fix        # 尝试自动修复
  python scripts/cdd_diagnose.py --json       # JSON格式输出
  python scripts/cdd_diagnose.py --summary    # 仅显示摘要
  python scripts/cdd_diagnose.py --verbose    # 详细输出
        
宪法依据: §100.3, §101, §102, §106.1
        """
    )
    
    parser.add_argument("--fix", "-f", action="store_true",
                       help="尝试自动修复失败项")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="详细输出模式")
    parser.add_argument("--json", "-j", action="store_true",
                       help="JSON格式输出")
    parser.add_argument("--summary", "-s", action="store_true",
                       help="仅显示摘要")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="安静模式（仅显示错误）")
    parser.add_argument("--target", "-t", default=None,
                       help="目标项目目录（默认：CDD技能自身）")
    
    args = parser.parse_args()
    
    if not args.quiet:
        print(f"🔍 开始CDD综合诊断...")
        print(f"版本: v{VERSION}")
        print(f"项目根目录: {SKILL_ROOT}")
        if args.target:
            print(f"目标目录: {args.target}")
        print()
    
    # 运行所有检查
    results = []
    fixes_attempted = 0
    fixes_succeeded = 0
    
    for check in DIAGNOSTIC_CHECKS:
        # 如果指定了目标，调整命令
        if args.target and "scripts/cdd_" in check.command:
            # 对于外部项目，调整命令
            adjusted_cmd = check.command.replace("--quiet", f"--target {args.target} --quiet")
        else:
            adjusted_cmd = check.command
        
        check.command = adjusted_cmd
        
        result = check.run(verbose=args.verbose)
        results.append((check, result))
        
        # 如果检查失败且启用了修复，尝试自动修复
        if result["status"] != "passed" and args.fix and check.required:
            if args.verbose:
                print(f"尝试修复失败的检查: {check.name}")
            
            fix_success, fix_message = attempt_auto_fix(check, result, args.verbose)
            fixes_attempted += 1
            
            if fix_success:
                fixes_succeeded += 1
                # 重新运行检查
                if args.verbose:
                    print(f"重新运行检查: {check.name}")
                
                result = check.run(verbose=args.verbose)
                results[-1] = (check, result)  # 更新结果
    
    # 输出结果
    if args.json:
        print(format_json_report(results))
    elif args.summary:
        print(format_summary_report(results))
    else:
        if not args.quiet:
            print(format_detailed_report(results))
        else:
            # 仅显示失败项
            failed_results = [(c, r) for c, r in results if r["status"] != "passed"]
            if failed_results:
                print("❌ 诊断失败项:")
                for check, result in failed_results:
                    print(f"  {check.name}: {result.get('message', '未知错误')}")
    
    # 显示修复摘要
    if args.fix and fixes_attempted > 0:
        if not args.quiet:
            print(f"\n🔧 修复摘要:")
            print(f"   尝试修复: {fixes_attempted}")
            print(f"   成功修复: {fixes_succeeded}")
            print(f"   失败修复: {fixes_attempted - fixes_succeeded}")
    
    # 设置退出码
    all_passed = all(r["status"] == "passed" for _, r in results)
    sys.exit(0 if all_passed else 1)

# -----------------------------------------------------------------------------
# Claude Code 集成接口
# -----------------------------------------------------------------------------

def run_diagnostic_claude(**kwargs) -> Dict[str, Any]:
    """Claude Code诊断接口"""
    results = []
    
    for check in DIAGNOSTIC_CHECKS:
        result = check.run(verbose=kwargs.get("verbose", False))
        results.append({
            "name": check.name,
            "description": check.description,
            "result": result
        })
    
    all_passed = all(item["result"]["status"] == "passed" for item in results)
    
    return {
        "success": all_passed,
        "all_passed": all_passed,
        "checks": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for item in results if item["result"]["status"] == "passed"),
            "failed": sum(1 for item in results if item["result"]["status"] != "passed")
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

if __name__ == "__main__":
    main()