#!/usr/bin/env python3
"""
CDD Unified Auditor (cdd_auditor.py) v2.0.0
===========================================
整合审计功能：Gate 1-5宪法审计 + Claude Code桥梁接口

重要变更：
- 已重构为使用core/audit_service.py作为唯一业务逻辑层
- 支持通过 --target 参数审计外部项目
- Gate 2 在pytest未安装时优雅降级

遵循§101§106.1

宪法依据: §101§102§309§106.1

Usage:
    python scripts/cdd_auditor.py --gate all                    # 审计CDD技能自身
    python scripts/cdd_auditor.py --gate all --target /path     # 审计外部项目
    python scripts/cdd_auditor.py --gate 1 --fix               # 自动修复版本漂移
    python scripts/cdd_auditor.py --format json --ai-hint      # JSON格式输出
"""

import sys
import os
import argparse
import json
from pathlib import Path

# 添加项目根目录到Python路径，确保可以导入core
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SKILL_ROOT))

# 导入core层
try:
    from core.audit_service import AuditService, VersionChecker
    from core.audit_service import EC_SUCCESS, EC_GATE_1_FAIL, EC_GATE_2_FAIL, EC_GATE_3_FAIL, EC_GATE_4_FAIL, EC_GATE_5_FAIL
    from utils.spore_utils import check_spore_isolation
    SERVICE_AVAILABLE = True
except ImportError as e:
    SERVICE_AVAILABLE = False
    print(f"无法导入core层: {e}")
    print("请确保core目录存在且包含audit_service.py")
    print(f"Python路径: {sys.path}")

VERSION = "2.0.0"

# -----------------------------------------------------------------------------
# 交互式向导函数
# -----------------------------------------------------------------------------

def run_audit_interactive(target_root: Path) -> dict:
    """
    交互式宪法审计向导
    
    宪法依据: §101§102§300.3 (宪法审计流程)
    """
    import time
    
    print("=" * 60)
    print("🔍 CDD 交互式宪法审计向导 v2.0.0")
    print("=" * 60)
    print("本向导将引导您完成以下步骤:")
    print("1. 选择要审计的Gate")
    print("2. 配置审计选项")
    print("3. 执行审计")
    print("4. 查看结果并提供修复建议")
    print("=" * 60)
    print()
    
    results = {
        "success": False,
        "steps": [],
        "target": str(target_root),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    # 步骤1: 选择要审计的Gate
    print("🔍 步骤1/4: 选择要审计的Gate")
    print("-" * 40)
    print("可用的Gate:")
    print("  [1] Gate 1: 版本一致性检查")
    print("  [2] Gate 2: 行为验证检查 (测试)")
    print("  [3] Gate 3: 熵值监控检查")
    print("  [4] Gate 4: 语义审计检查")
    print("  [5] Gate 5: 宪法引用完整性检查")
    print("  [A] All: 所有Gate")
    print()
    
    gate_choice = ""
    valid_choices = ['1', '2', '3', '4', '5', 'a', 'A', 'all', 'All']
    while gate_choice not in valid_choices:
        gate_choice = input("请选择要审计的Gate (1-5, A/all): ").strip()
        if gate_choice not in valid_choices:
            print("❌ 无效选择，请重试")
    
    # 映射选择到gate参数
    gate_map = {
        '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
        'a': 'all', 'A': 'all', 'all': 'all', 'All': 'all'
    }
    selected_gate = gate_map.get(gate_choice, 'all')
    
    print(f"✅ 已选择: Gate {selected_gate}")
    results["steps"].append({
        "name": "gate_selection",
        "status": "selected",
        "message": f"用户选择了 Gate {selected_gate}"
    })
    
    # 步骤2: 配置审计选项
    print("\n🔍 步骤2/4: 配置审计选项")
    print("-" * 40)
    
    print("自动修复选项:")
    print("  如果发现版本不一致 (Gate 1)，是否自动修复?")
    fix_choice = input("是否启用自动修复? (Y/n): ").strip().lower()
    enable_fix = fix_choice in ["", "y", "yes"]
    
    print("\n详细输出选项:")
    print("  是否显示详细的审计信息?")
    verbose_choice = input("是否启用详细输出? (Y/n): ").strip().lower()
    enable_verbose = verbose_choice in ["", "y", "yes"]
    
    print("\n🔧 配置摘要:")
    print(f"   目标目录: {target_root}")
    print(f"   审计的Gate: {selected_gate}")
    print(f"   自动修复: {'✅ 启用' if enable_fix else '❌ 禁用'}")
    print(f"   详细输出: {'✅ 启用' if enable_verbose else '❌ 禁用'}")
    
    confirm = input("\n✅ 确认以上配置并开始审计? (Y/n): ").strip().lower()
    if confirm not in ["", "y", "yes"]:
        print("❌ 向导终止")
        results["error"] = "用户取消"
        return results
    
    results["steps"].append({
        "name": "configuration",
        "status": "confirmed",
        "message": f"Gate: {selected_gate}, 修复: {enable_fix}, 详细: {enable_verbose}"
    })
    
    # 步骤3: 执行审计
    print("\n🔍 步骤3/4: 执行宪法审计")
    print("-" * 40)
    
    try:
        print(f"⏳ 正在运行Gate {selected_gate} 审计...")
        audit_service = AuditService(target_root)
        audit_result = audit_service.audit_gates(
            gates=selected_gate,
            fix=enable_fix,
            verbose=enable_verbose
        )
        
        results["audit_result"] = audit_result
        
        if audit_result.get("success", False):
            gate_results = audit_result.get("results", [])
            all_passed = all(gate.get("passed", False) for gate in gate_results)
            
            if all_passed:
                print("✅ 所有审计通过!")
                results["success"] = True
                results["steps"].append({
                    "name": "audit_execution",
                    "status": "success",
                    "message": "所有Gate通过审计"
                })
            else:
                print("⚠️  审计发现问题:")
                for gate in gate_results:
                    gate_id = gate.get("gate", "?")
                    gate_name = gate.get("name", "Unknown")
                    passed = gate.get("passed", False)
                    
                    if passed:
                        print(f"  ✅ Gate {gate_id}: {gate_name} - 通过")
                    else:
                        print(f"  ❌ Gate {gate_id}: {gate_name} - 失败")
                        
                        # 显示失败详情
                        if enable_verbose and "details" in gate:
                            details = gate["details"]
                            if isinstance(details, dict):
                                for key, value in details.items():
                                    if key not in ["files", "found_articles", "required_articles"] and value:
                                        print(f"      {key}: {value}")
                
                results["success"] = False
                results["steps"].append({
                    "name": "audit_execution",
                    "status": "warning",
                    "message": f"发现 {len([g for g in gate_results if not g.get('passed', False)])} 个Gate失败"
                })
        else:
            error_msg = audit_result.get("error", "未知错误")
            print(f"❌ 审计执行失败: {error_msg}")
            results["error"] = error_msg
            results["steps"].append({
                "name": "audit_execution",
                "status": "failed",
                "message": f"审计失败: {error_msg}"
            })
    
    except Exception as e:
        print(f"❌ 审计过程中出现异常: {e}")
        results["error"] = str(e)
        results["steps"].append({
            "name": "audit_execution",
            "status": "error",
            "message": f"异常: {e}"
        })
    
    # 步骤4: 结果分析和建议
    print("\n🔍 步骤4/4: 结果分析和建议")
    print("-" * 40)
    
    if results.get("success", False):
        print("🎉 审计完成!")
        print("📋 结果: 所有Gate通过，项目符合宪法要求")
        print("\n📚 下一步建议:")
        print("   1. 继续开发新特性")
        print("   2. 定期运行审计以确保合规")
        print("   3. 更新文档以反映当前状态")
    else:
        audit_result = results.get("audit_result", {})
        gate_results = audit_result.get("results", [])
        
        failed_gates = [g for g in gate_results if not g.get("passed", False)]
        if failed_gates:
            print("🔧 修复建议:")
            for gate in failed_gates:
                gate_id = gate.get("gate", "?")
                
                if gate_id == 1:
                    print(f"  Gate {gate_id} 失败 - 版本不一致:")
                    print("    修复命令: python scripts/cdd_auditor.py --gate 1 --fix")
                    print("    宪法依据: §100.3")
                
                elif gate_id == 2:
                    print(f"  Gate {gate_id} 失败 - 测试未通过:")
                    print("    修复命令: pytest tests/ -v")
                    print("    宪法依据: §300.3")
                
                elif gate_id == 3:
                    print(f"  Gate {gate_id} 失败 - 熵值超标:")
                    print("    修复命令: python scripts/cdd_entropy.py optimize")
                    print("    宪法依据: §102")
                
                elif gate_id == 4:
                    print(f"  Gate {gate_id} 失败 - 宪法引用不足:")
                    print("    修复命令: 添加适当的宪法引用")
                    print("    宪法依据: §101, §300.5")
                
                elif gate_id == 5:
                    print(f"  Gate {gate_id} 失败 - 引用格式错误:")
                    print("    修复命令: 修复宪法引用格式 (格式: §100.3)")
                    print("    宪法依据: §305")
        
        print("\n💡 综合修复建议:")
        print("   1. 运行综合诊断: python scripts/cdd_diagnose.py --fix")
        print("   2. 查看详细错误: python scripts/cdd_auditor.py --gate all --verbose")
        print("   3. 寻求帮助: 查看文档或社区支持")
    
    # 向导完成
    print("\n" + "=" * 60)
    print("🔍 交互式宪法审计向导完成")
    print("=" * 60)
    
    successful_steps = sum(1 for step in results["steps"] if step["status"] in ["selected", "confirmed", "success"])
    total_steps = len(results["steps"])
    
    print(f"📊 执行统计:")
    print(f"   总步骤数: {total_steps}")
    print(f"   成功步骤: {successful_steps}")
    print(f"   完成状态: {'✅ 成功' if results['success'] else '❌ 失败'}")
    
    return results

# -----------------------------------------------------------------------------
# CLI入口点
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=f"CDD Unified Auditor v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/cdd_auditor.py --gate all                    # 审计CDD技能自身
  python scripts/cdd_auditor.py --gate all --target ../myapp  # 审计外部项目
  python scripts/cdd_auditor.py --gate 1 --fix               # 自动修复版本漂移
  python scripts/cdd_auditor.py --gate 2                     # 仅运行Gate 2行为验证
  python scripts/cdd_auditor.py --clean                      # 清理临时目录
        """
    )
    
    # Modes
    parser.add_argument("--gate", choices=['1', '2', '3', '4', '5', 'all'], 
                        default='all', help="Gate to run (default: all)")
    parser.add_argument("--fix", action="store_true", help="Auto-fix violations")
    parser.add_argument("--clean", action="store_true", help="Clean temporary directories")
    
    # Target
    parser.add_argument("--target", "-t", default=None, 
                        help="Target project directory (default: CDD skill root)")
    
    # Options
    parser.add_argument("--force", action="store_true", help="Skip confirmation")
    parser.add_argument("--format", choices=['text', 'json'], default='text', 
                        help="Output format (default: text)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress non-error output")
    parser.add_argument("--ai-hint", action="store_true", help="AI remediation hints")
    parser.add_argument("--interactive", "-i", action="store_true", 
                        help="交互式向导模式")
    
    args = parser.parse_args()
    
    if not SERVICE_AVAILABLE:
        print("审计服务不可用")
        sys.exit(1)
    
    # 确定目标目录
    if args.target:
        target_root = Path(args.target).resolve()
        
        # 孢子隔离检查：审计外部项目时允许
        passed, message = check_spore_isolation(target_root, "cdd_auditor.py", allow_skill_root=True)
        if not passed:
            print(f"\n孢子隔离违例: {message}")
            sys.exit(100)
        
        if not args.quiet:
            print(f"CDD Auditor v{VERSION}")
            print(f"目标目录: {target_root}")
    else:
        # 默认审计CDD技能自身
        target_root = SKILL_ROOT
        if not args.quiet:
            print(f"CDD Auditor v{VERSION}")
            print(f"目标目录: {target_root} (CDD技能自身)")
    
    try:
        # 创建审计服务实例
        audit_service = AuditService(target_root)
        
        if args.clean:
            # 清理临时目录
            result = audit_service.cleanup_temporary_directories(force=args.force)
            if args.format == 'json':
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"清理完成: {result.get('cleaned', 0)} 个目录")
            return
        
        # 检查是否需要运行交互式向导
        if args.interactive:
            # 运行交互式向导
            wizard_result = run_audit_interactive(target_root)
            
            if args.format == 'json':
                print(json.dumps(wizard_result, indent=2, ensure_ascii=False))
            else:
                # 向导已经在run_audit_interactive中输出详细信息
                pass
            
            sys.exit(0 if wizard_result.get("success", False) else 1)
        
        # 执行审计
        result = audit_service.audit_gates(
            gates=args.gate,
            fix=args.fix,
            verbose=args.verbose
        )
        
        if args.format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # 文本格式输出
            if result.get("success", False):
                print("\n审计完成")
                results = result.get("results", [])
                for gate_result in results:
                    icon = "✅" if gate_result.get("passed", False) else "❌"
                    gate_id = gate_result.get('gate', '?')
                    gate_name = gate_result.get('name', 'Unknown')
                    print(f"  {icon} Gate {gate_id}: {gate_name}")
                    
                    # 显示详细信息
                    if args.verbose and "details" in gate_result:
                        details = gate_result["details"]
                        if isinstance(details, dict):
                            for key, value in details.items():
                                if key not in ["files", "found_articles", "required_articles"]:
                                    print(f"      {key}: {value}")
            else:
                error_msg = result.get('error', 'Unknown error')
                print(f"\n审计失败: {error_msg}")
                
                # 显示已完成的门禁结果
                results = result.get("results", [])
                if results:
                    print("\n已完成的门禁:")
                    for gate_result in results:
                        icon = "✅" if gate_result.get("passed", False) else "❌"
                        gate_id = gate_result.get('gate', '?')
                        gate_name = gate_result.get('name', 'Unknown')
                        print(f"  {icon} Gate {gate_id}: {gate_name}")
        
        # 确定退出码
        exit_code = EC_SUCCESS
        if not result.get("success", False):
            exit_code = 1
        else:
            results = result.get("results", [])
            for gate_result in results:
                if not gate_result.get("passed", False):
                    gate_id = gate_result.get("gate", 0)
                    if gate_id == 1:
                        exit_code = EC_GATE_1_FAIL
                    elif gate_id == 2:
                        exit_code = EC_GATE_2_FAIL
                    elif gate_id == 3:
                        exit_code = EC_GATE_3_FAIL
                    elif gate_id == 4:
                        exit_code = EC_GATE_4_FAIL
                    elif gate_id == 5:
                        exit_code = EC_GATE_5_FAIL
                    break
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n审计被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n内部错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

# -----------------------------------------------------------------------------
# Claude Code桥梁接口 (保持向后兼容)
# -----------------------------------------------------------------------------

def audit_gates_claude(gates: str = "all", fix: bool = False, target: str = None, **kwargs) -> dict:
    """Claude Code审计桥梁接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "Audit service not available"}
    
    target_root = Path(target).resolve() if target else SKILL_ROOT
    audit_service = AuditService(target_root)
    return audit_service.audit_gates(gates=gates, fix=fix, verbose=kwargs.get("verbose", False))

def verify_versions_claude(fix: bool = False, target: str = None, **kwargs) -> dict:
    """Claude Code版本验证接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "Audit service not available"}
    
    target_root = Path(target).resolve() if target else SKILL_ROOT
    audit_service = AuditService(target_root)
    return audit_service.verify_versions(fix=fix)

if __name__ == "__main__":
    main()