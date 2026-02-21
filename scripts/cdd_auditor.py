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