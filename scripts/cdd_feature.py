#!/usr/bin/env python3
"""
CDD Feature CLI Wrapper (cdd_feature.py) v2.0.0
===============================================
简化CLI包装层，调用services/feature_service.py核心业务逻辑。

宪法依据: §101§102§200§309

Usage:
    python scripts/cdd_feature.py create "Feature Name" "Description"
    python scripts/cdd_feature.py deploy "Project Name" --target /path
    python scripts/cdd_feature.py list --target /path
"""

import sys
import os
import argparse
import json
from pathlib import Path

# 添加项目根目录到Python路径，确保可以导入services
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入服务层
try:
    from core.feature_service import FeatureService
    from utils.spore_utils import check_spore_isolation
    SERVICE_AVAILABLE = True
except ImportError as e:
    SERVICE_AVAILABLE = False
    print(f"❌ 无法导入services层: {e}")
    print("请确保services目录存在且包含feature_service.py")

VERSION = "2.0.0"

# -----------------------------------------------------------------------------
# 环境检查函数（P1改进）
# -----------------------------------------------------------------------------

def check_environment_integration():
    """
    集成环境检查到主要工具中
    
    Returns:
        bool: 环境是否通过检查
    """
    try:
        # 尝试导入环境检查函数
        check_env_path = SCRIPT_DIR / "cdd_check_env.py"
        if check_env_path.exists():
            import importlib.util
            spec = importlib.util.spec_from_file_location("cdd_check_env", check_env_path)
            if spec and spec.loader:
                check_env_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(check_env_module)
                
                # 静默模式检查
                if hasattr(check_env_module, "check_environment_claude"):
                    env_check = check_env_module.check_environment_claude()
                    
                    if not env_check.get("success", False):
                        print("⚠️  环境检查失败:")
                        missing = [d["name"] for d in env_check.get("results", []) 
                                  if d["required"] and not d["installed"]]
                        for dep in missing:
                            print(f"  - 缺少必需依赖: {dep}")
                        print("\n💡 请运行以下命令修复:")
                        print(f"   python {check_env_path} --fix")
                        return False
        return True
    except Exception as e:
        # 如果环境检查失败，继续执行（避免阻止有效使用）
        return True

# -----------------------------------------------------------------------------
# CLI输出格式化
# -----------------------------------------------------------------------------

def format_feature_list_result(result: dict) -> str:
    """格式化特性列表输出"""
    if not result.get("success", False):
        return f"❌ 错误: {result.get('error', 'Unknown error')}"
    
    features = result.get("features", [])
    if not features:
        return f"📁 目标目录: {result.get('target', 'Unknown')}\n未找到特性"
    
    output = [f"📁 目标目录: {result.get('target', 'Unknown')}"]
    output.append(f"找到 {result.get('count', 0)} 个特性:")
    
    for i, feature in enumerate(features, 1):
        output.append(f"\n  {i}. {feature.get('name', 'Unknown')}")
        output.append(f"     路径: {feature.get('path', 'N/A')}")
        files = feature.get("files", [])
        if files:
            output.append(f"     文件: {len(files)} 个")
    
    return "\n".join(output)

def format_feature_create_result(result: dict, dry_run: bool = False) -> str:
    """格式化特性创建输出"""
    if not result.get("success", False):
        return f"❌ 创建失败: {result.get('error', 'Unknown error')}"
    
    if result.get("dry_run", False) or dry_run:
        prefix = "🔍 模拟运行结果:"
    else:
        prefix = "✅ 特性创建成功:"
    
    output = [prefix]
    output.append(f"名称: {result.get('feature_name', 'N/A')}")
    output.append(f"ID: {result.get('feature_id', 'N/A')}")
    output.append(f"目录: {result.get('feature_dir', 'N/A')}")
    
    files = result.get("generated_files", [])
    if files:
        output.append(f"生成文件 ({len(files)} 个):")
        for f in files:
            output.append(f"  - {f}")
    
    return "\n".join(output)

def format_deploy_result(result: dict) -> str:
    """格式化部署输出"""
    if not result.get("success", False):
        return f"❌ 部署失败: {result.get('error', 'Unknown error')}"
    
    output = ["🌱 CDD部署成功"]
    output.append(f"项目: {result.get('project_name', 'N/A')}")
    output.append(f"目标目录: {result.get('target_dir', 'N/A')}")
    output.append(f"Memory Bank: {result.get('memory_bank', 'N/A')}")
    
    files = result.get("deployed_files", [])
    if files:
        output.append(f"部署文件 ({len(files)} 个):")
        for f in files[:5]:  # 只显示前5个文件
            output.append(f"  - {f}")
        if len(files) > 5:
            output.append(f"  ... 以及 {len(files) - 5} 个其他文件")
    
    return "\n".join(output)

# -----------------------------------------------------------------------------
# Wizard交互函数
# -----------------------------------------------------------------------------

def run_wizard_interactive(target: str = ".", skip_checks: bool = False) -> dict:
    """
    交互式向导模式 - 引导用户完成特性创建
    
    宪法依据: §101§102§103 (上下文管理, 文档优先)
    """
    import time
    
    print("=" * 60)
    print("🎯 CDD 交互式向导 v2.0.0")
    print("=" * 60)
    print("本向导将引导您完成以下步骤:")
    print("1. 环境检查")
    print("2. 孢子隔离验证")
    print("3. 特性信息收集")
    print("4. 配置确认")
    print("5. 执行创建")
    print("=" * 60)
    print()
    
    results = {
        "success": False,
        "steps": [],
        "target": target,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    # 步骤1: 环境检查
    if not skip_checks:
        print("🔍 步骤1/5: 环境检查")
        print("-" * 40)
        
        try:
            check_result = check_environment_integration()
            if check_result:
                print("✅ 环境检查通过")
                results["steps"].append({
                    "name": "environment_check",
                    "status": "passed",
                    "message": "环境依赖检查通过"
                })
            else:
                print("❌ 环境检查失败，建议运行:")
                print("   python scripts/cdd_check_env.py --fix")
                
                confirm = input("是否继续? (y/N): ").strip().lower()
                if confirm != "y":
                    print("❌ 向导终止")
                    return results
                
                results["steps"].append({
                    "name": "environment_check",
                    "status": "warning",
                    "message": "环境检查失败，用户选择继续"
                })
        except Exception as e:
            print(f"⚠️  环境检查异常: {e}")
            results["steps"].append({
                "name": "environment_check",
                "status": "warning",
                "message": f"环境检查异常: {e}"
            })
    
    # 步骤2: 孢子隔离检查
    print("\n🔍 步骤2/5: 孢子隔离检查")
    print("-" * 40)
    
    target_root = Path(target).resolve()
    try:
        passed, message = check_spore_isolation(target_root, "cdd_feature.py")
        if passed:
            print(f"✅ 孢子隔离检查通过")
            print(f"   目标目录: {target_root}")
            results["steps"].append({
                "name": "spore_isolation",
                "status": "passed",
                "message": message
            })
        else:
            print(f"❌ 孢子隔离违例: {message}")
            print("\n💡 解决方案:")
            print("   1. 确保在项目目录中运行向导")
            print("   2. 不要修改CDD技能库自身")
            print("   3. 使用 --target 参数指定正确目录")
            
            new_target = input(f"请输入正确的目标目录 (当前: {target}): ").strip()
            if new_target:
                target = new_target
                target_root = Path(target).resolve()
                
                # 重新检查
                passed, message = check_spore_isolation(target_root, "cdd_feature.py")
                if passed:
                    print(f"✅ 修正后孢子隔离检查通过")
                    results["steps"].append({
                        "name": "spore_isolation",
                        "status": "corrected",
                        "message": f"修正后通过: {message}"
                    })
                else:
                    print("❌ 孢子隔离检查仍然失败，向导终止")
                    results["error"] = "孢子隔离违例"
                    return results
            else:
                print("❌ 向导终止")
                results["error"] = "孢子隔离违例"
                return results
    except Exception as e:
        print(f"⚠️  孢子隔离检查异常: {e}")
        results["steps"].append({
            "name": "spore_isolation",
            "status": "error",
            "message": f"检查异常: {e}"
        })
    
    # 步骤3: 收集特性信息
    print("\n🔍 步骤3/5: 特性信息收集")
    print("-" * 40)
    
    feature_name = ""
    while not feature_name.strip():
        feature_name = input("请输入特性名称 (必填): ").strip()
        if not feature_name:
            print("❌ 特性名称不能为空")
    
    description = input("请输入特性描述 (可选，回车跳过): ").strip()
    
    # 名称验证
    print(f"\n🔍 验证特性名称: {feature_name}")
    try:
        feature_service = FeatureService()
        validate_result = feature_service.validate_feature_name(feature_name)
        
        if validate_result.get("valid", False):
            print(f"✅ 特性名称有效")
            reason = validate_result.get("reason", "")
            if reason:
                print(f"   原因: {reason}")
            
            warning = validate_result.get("warning", "")
            if warning:
                print(f"   ⚠️ 警告: {warning}")
            
            results["steps"].append({
                "name": "feature_validation",
                "status": "passed",
                "message": validate_result.get("reason", "")
            })
        else:
            print(f"❌ 特性名称无效")
            print(f"   原因: {validate_result.get('reason', '未知')}")
            
            confirm = input("是否继续使用此名称? (y/N): ").strip().lower()
            if confirm != "y":
                print("❌ 向导终止")
                results["error"] = "特性名称无效"
                return results
            
            results["steps"].append({
                "name": "feature_validation",
                "status": "warning",
                "message": f"名称无效但用户选择继续: {validate_result.get('reason', '')}"
            })
    except Exception as e:
        print(f"⚠️  名称验证异常: {e}")
        results["steps"].append({
            "name": "feature_validation",
            "status": "warning",
            "message": f"验证异常: {e}"
        })
    
    # 步骤4: 配置确认
    print("\n🔍 步骤4/5: 配置确认")
    print("-" * 40)
    
    print("📋 配置摘要:")
    print(f"   特性名称: {feature_name}")
    print(f"   特性描述: {description or '(无)'}")
    print(f"   目标目录: {target}")
    print(f"   目标路径: {target_root}")
    print()
    
    print("📋 向导将为您生成以下内容:")
    print("   1. 特性规格文档 (specs/XXX-特性名/DS-050_feature_specification.md)")
    print("   2. 实现标准文档 (specs/XXX-特性名/DS-051_implementation_plan.md)")
    print("   3. 原子任务文档 (specs/XXX-特性名/DS-052_atomic_tasks.md)")
    print("   4. 质量检查表 (specs/XXX-特性名/DS-053_quality_checklist.md)")
    print("   5. 熵值优化器规格 (specs/XXX-特性名/DS-055_entropy_optimizer_spec.md)")
    
    confirm = input("\n✅ 确认以上配置并创建特性? (Y/n): ").strip().lower()
    if confirm in ["", "y", "yes"]:
        print("✅ 配置已确认")
        results["steps"].append({
            "name": "configuration_confirmation",
            "status": "confirmed",
            "message": "用户确认配置"
        })
    else:
        print("❌ 向导终止")
        results["error"] = "用户取消"
        return results
    
    # 步骤5: 执行创建
    print("\n🔍 步骤5/5: 执行创建")
    print("-" * 40)
    
    try:
        print(f"⏳ 正在创建特性 '{feature_name}'...")
        feature_service = FeatureService()
        create_result = feature_service.create_feature(
            name=feature_name,
            description=description,
            target=target,
            create_branch=True
        )
        
        if create_result.get("success", False):
            print("✅ 特性创建成功!")
            print(f"   特性ID: {create_result.get('feature_id', 'N/A')}")
            print(f"   特性目录: {create_result.get('feature_dir', 'N/A')}")
            
            files = create_result.get("generated_files", [])
            if files:
                print(f"   生成文件 ({len(files)} 个):")
                for f in files[:3]:
                    print(f"      - {f}")
                if len(files) > 3:
                    print(f"      ... 以及 {len(files) - 3} 个其他文件")
            
            results["success"] = True
            results["feature_result"] = create_result
            results["steps"].append({
                "name": "feature_creation",
                "status": "success",
                "message": "特性创建成功"
            })
        else:
            print(f"❌ 特性创建失败")
            error_msg = create_result.get("error", "未知错误")
            print(f"   错误: {error_msg}")
            
            results["error"] = error_msg
            results["steps"].append({
                "name": "feature_creation",
                "status": "failed",
                "message": f"创建失败: {error_msg}"
            })
    except Exception as e:
        print(f"❌ 创建过程中出现异常: {e}")
        results["error"] = str(e)
        results["steps"].append({
            "name": "feature_creation",
            "status": "error",
            "message": f"异常: {e}"
        })
    
    # 向导完成
    print("\n" + "=" * 60)
    print("🎯 交互式向导完成")
    print("=" * 60)
    
    # 统计步骤结果
    successful_steps = sum(1 for step in results["steps"] if step["status"] in ["passed", "confirmed", "success", "corrected"])
    total_steps = len(results["steps"])
    
    print(f"📊 执行统计:")
    print(f"   总步骤数: {total_steps}")
    print(f"   成功步骤: {successful_steps}")
    print(f"   完成状态: {'✅ 成功' if results['success'] else '❌ 失败'}")
    
    if results["success"]:
        print("\n🎉 特性创建完成!")
        print("📚 下一步建议:")
        print("   1. 查看生成的规格文档")
        print("   2. 在State B等待规格批准")
        print("   3. 批准后在State C开始编码")
    else:
        print("\n💡 故障排除建议:")
        print("   1. 检查错误信息")
        print("   2. 运行诊断: python scripts/cdd_diagnose.py --fix")
        print("   3. 查看帮助文档")
    
    return results

# -----------------------------------------------------------------------------
# 主函数
# -----------------------------------------------------------------------------

def main():
    if not SERVICE_AVAILABLE:
        print("❌ 特征服务不可用")
        sys.exit(1)
    
    # 环境检查（P1改进）
    if not check_environment_integration():
        sys.exit(2)
    
    parser = argparse.ArgumentParser(description=f"CDD Feature CLI v{VERSION}")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # create 子命令
    create_parser = subparsers.add_parser("create", help="创建新特性")
    create_parser.add_argument("name", help="特性名称")
    create_parser.add_argument("description", nargs="?", default="", help="特性描述")
    create_parser.add_argument("--target", default=".", help="目标项目目录")
    create_parser.add_argument("--no-branch", action="store_true", help="跳过git分支创建")
    create_parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    create_parser.add_argument("--json", action="store_true", help="JSON输出格式")
    
    # deploy 子命令
    deploy_parser = subparsers.add_parser("deploy", help="部署CDD结构到项目")
    deploy_parser.add_argument("name", help="项目名称")
    deploy_parser.add_argument("--target", default=".", help="目标目录")
    deploy_parser.add_argument("--force", action="store_true", help="覆盖现有文件")
    deploy_parser.add_argument("--json", action="store_true", help="JSON输出格式")
    
    # list 子命令
    list_parser = subparsers.add_parser("list", help="列出所有特性")
    list_parser.add_argument("--target", default=".", help="目标目录")
    list_parser.add_argument("--json", action="store_true", help="JSON输出格式")
    
    # validate 子命令
    validate_parser = subparsers.add_parser("validate", help="验证特性名称")
    validate_parser.add_argument("name", help="特性名称")
    validate_parser.add_argument("--json", action="store_true", help="JSON输出格式")
    
    # wizard 子命令（交互式向导）
    wizard_parser = subparsers.add_parser("wizard", help="交互式向导模式")
    wizard_parser.add_argument("--target", default=".", help="目标项目目录")
    wizard_parser.add_argument("--skip-checks", action="store_true", help="跳过环境检查")
    wizard_parser.add_argument("--json", action="store_true", help="JSON输出格式")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行命令
    if args.command == "create":
        target_root = Path(args.target).resolve()
        
        # 孢子隔离检查
        passed, message = check_spore_isolation(target_root, "cdd_feature.py")
        if not passed:
            print(f"\n❌ 孢子隔离违例: {message}")
            sys.exit(100)
        
        feature_service = FeatureService()
        
        if args.dry_run:
            result = {
                "success": True,
                "dry_run": True,
                "feature_name": args.name,
                "feature_id": "000",  # 模拟ID
                "feature_dir": str(target_root / "specs" / f"000-{args.name.lower().replace(' ', '-')}"),
                "generated_files": ["模拟文件1", "模拟文件2"]
            }
        else:
            result = feature_service.create_feature(
                name=args.name,
                description=args.description,
                target=args.target,
                create_branch=not args.no_branch
            )
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"🔧 CDD Feature CLI v{VERSION}")
            print(f"   目标: {target_root}")
            print()
            print(format_feature_create_result(result, args.dry_run))
        
        sys.exit(0 if result.get("success", False) else 1)
    
    elif args.command == "deploy":
        target_root = Path(args.target).resolve()
        
        # 孢子隔离检查
        passed, message = check_spore_isolation(target_root, "cdd_feature.py")
        if not passed:
            print(f"\n❌ 孢子隔离违例: {message}")
            sys.exit(100)
        
        feature_service = FeatureService()
        result = feature_service.deploy_project(
            project_name=args.name,
            target=args.target,
            force=args.force
        )
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"🌱 CDD Deployer v{VERSION}")
            print(f"   项目: {args.name}")
            print(f"   目标: {target_root}")
            print()
            print(format_deploy_result(result))
        
        sys.exit(0 if result.get("success", False) else 1)
    
    elif args.command == "list":
        feature_service = FeatureService()
        result = feature_service.list_features(target=args.target)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"📁 CDD Feature List v{VERSION}")
            print()
            print(format_feature_list_result(result))
        
        sys.exit(0 if result.get("success", False) else 1)
    
    elif args.command == "validate":
        feature_service = FeatureService()
        result = feature_service.validate_feature_name(args.name)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if result.get("valid", False):
                print(f"✅ 特性名称有效: {args.name}")
                print(f"   原因: {result.get('reason', 'N/A')}")
                if "warning" in result:
                    print(f"   ⚠️ 警告: {result.get('warning', '')}")
            else:
                print(f"❌ 特性名称无效: {args.name}")
                print(f"   原因: {result.get('reason', 'Unknown')}")
        
        sys.exit(0 if result.get("valid", False) else 1)
    
    elif args.command == "wizard":
        target_root = Path(args.target).resolve()
        
        # 孢子隔离检查
        passed, message = check_spore_isolation(target_root, "cdd_feature.py")
        if not passed:
            print(f"\n❌ 孢子隔离违例: {message}")
            sys.exit(100)
        
        # 运行交互式向导
        wizard_result = run_wizard_interactive(
            target=args.target,
            skip_checks=args.skip_checks
        )
        
        if args.json:
            print(json.dumps(wizard_result, indent=2, ensure_ascii=False))
        else:
            # 向导已经在run_wizard_interactive中输出详细信息
            # 这里只添加JSON格式支持
            pass
        
        sys.exit(0 if wizard_result.get("success", False) else 1)
    
    else:
        print(f"❌ 未知命令: {args.command}")
        parser.print_help()
        sys.exit(1)

# -----------------------------------------------------------------------------
# Claude Code桥梁接口 (保持向后兼容)
# -----------------------------------------------------------------------------

def create_feature_claude(name: str, description: str = "", 
                          target: str = ".", **kwargs) -> dict:
    """Claude Code特性创建接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "FeatureService not available"}
    
    feature_service = FeatureService()
    return feature_service.create_feature(
        name=name,
        description=description,
        target=target,
        create_branch=kwargs.get("create_branch", True)
    )

def deploy_project_claude(project_name: str, target: str = ".", 
                          force: bool = False, **kwargs) -> dict:
    """Claude Code项目部署接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "FeatureService not available"}
    
    feature_service = FeatureService()
    return feature_service.deploy_project(
        project_name=project_name,
        target=target,
        force=force
    )

if __name__ == "__main__":
    main()