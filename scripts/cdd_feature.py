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