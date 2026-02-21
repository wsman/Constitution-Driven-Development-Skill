#!/usr/bin/env python3
"""
CDD Asset Manager CLI (cdd_asset_manager.py) v2.0.0
==================================================
技术资产管理CLI工具，调用services/asset_service.py核心业务逻辑。

宪法依据: §101单一真理源原则、§102熵减原则、§103文档优先公理

使用场景:
1. State A→B阶段：强制搜索现有技术资产
2. 资产审计阶段：定期检查资产质量和复用率
3. 资产贡献阶段：标准化资产入库流程

Usage:
    python scripts/cdd_asset_manager.py scan [--verbose] [--json]
    python scripts/cdd_asset_manager.py report [--format json|text] [--output FILE]
    python scripts/cdd_asset_manager.py search <query> [--type TYPE] [--json]
    python scripts/cdd_asset_manager.py validate <file> [--content CONTENT] [--json]
    python scripts/cdd_asset_manager.py suggest <project_path> [--json]
    python scripts/cdd_asset_manager.py stats [--json]
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import Optional

# 添加项目根目录到Python路径，确保可以导入services
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入服务层
try:
    from core.asset_service import AssetService
    SERVICE_AVAILABLE = True
except ImportError as e:
    SERVICE_AVAILABLE = False
    print(f"❌ 无法导入asset_service: {e}")
    print("请确保services目录存在且包含asset_service.py")

VERSION = "2.0.0"

# -----------------------------------------------------------------------------
# 环境检查函数
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

def format_scan_result(result: dict) -> str:
    """格式化扫描输出"""
    if not result.get("success", False):
        return f"❌ 扫描失败: {result.get('error', 'Unknown error')}"
    
    output = ["📊 资产库扫描完成"]
    output.append(f"📁 资产库目录: {result.get('library_root', 'N/A')}")
    output.append(f"🔍 发现资产: {result.get('assets_found', 0)} 个")
    
    metrics = result.get("metrics", {})
    if metrics:
        output.append("\n📈 资产指标:")
        output.append(f"  • 资产类型覆盖: {metrics.get('coverage', 0)*100:.1f}%")
        output.append(f"  • 宪法合规性: {metrics.get('constitutional_compliance', 0)*100:.1f}%")
        output.append(f"  • 文档完整性: {metrics.get('documentation_completeness', 0)*100:.1f}%")
    
    asset_types = result.get("asset_types", {})
    if asset_types:
        output.append("\n📂 资产类型分布:")
        for asset_type, count in sorted(asset_types.items()):
            output.append(f"  • {asset_type}: {count} 个")
    
    suggestions = result.get("suggestions", [])
    if suggestions:
        output.append("\n💡 建议:")
        for suggestion in suggestions[:3]:  # 只显示前3个建议
            output.append(f"  - {suggestion}")
    
    return "\n".join(output)

def format_report_result(result: dict) -> str:
    """格式化报告输出"""
    if not result.get("success", False):
        return f"❌ 报告生成失败: {result.get('error', 'Unknown error')}"
    
    report = result.get("report", {})
    if not report:
        return "⚠️  报告内容为空"
    
    output = ["📋 技术资产库报告"]
    output.append(f"📅 生成时间: {report.get('timestamp', 'N/A')}")
    output.append(f"📁 资产库目录: {report.get('library_root', 'N/A')}")
    
    summary = report.get("summary", {})
    if summary:
        output.append(f"\n📊 资产概要:")
        output.append(f"  • 总资产数: {summary.get('total_assets', 0)} 个")
        output.append(f"  • 资产类型数: {summary.get('asset_types', 0)} 种")
        output.append(f"  • 宪法合规率: {summary.get('constitutional_compliance', 0)*100:.1f}%")
        output.append(f"  • 文档完整率: {summary.get('documentation_completeness', 0)*100:.1f}%")
    
    metrics = report.get("metrics", {})
    if metrics:
        output.append(f"\n📈 详细指标:")
        output.append(f"  • 平均文件大小: {metrics.get('avg_file_size', 0):.2f} bytes")
        output.append(f"  • 复用率: {metrics.get('reuse_rate', 0)*100:.1f}%")
        output.append(f"  • 覆盖率: {metrics.get('coverage', 0)*100:.1f}%")
    
    # 显示部分资产（最多5个）
    assets = report.get("assets", [])
    if assets:
        output.append(f"\n📂 资产列表 (前5个，共{len(assets)}个):")
        for i, asset in enumerate(assets[:5], 1):
            output.append(f"\n  {i}. {asset.get('name', 'Unknown')}")
            output.append(f"     类型: {asset.get('asset_type', 'unknown')}")
            output.append(f"     路径: {asset.get('path', 'N/A')}")
            output.append(f"     合规: {'✅' if asset.get('has_constitutional_compliance', False) else '❌'}")
            output.append(f"     主题: {'✅' if asset.get('is_theme_compliant', True) else '❌'}")
        
        if len(assets) > 5:
            output.append(f"\n  ... 以及 {len(assets) - 5} 个其他资产")
    
    return "\n".join(output)

def format_search_result(result: dict) -> str:
    """格式化搜索输出"""
    if not result.get("success", False):
        return f"❌ 搜索失败: {result.get('error', 'Unknown error')}"
    
    output = ["🔍 资产搜索结果"]
    output.append(f"查询词: {result.get('query', 'N/A')}")
    output.append(f"资产类型过滤: {result.get('asset_type', '全部')}")
    output.append(f"找到结果: {result.get('results_found', 0)} 个")
    
    results = result.get("results", [])
    if results:
        output.append("\n📄 搜索结果:")
        for i, item in enumerate(results, 1):
            output.append(f"\n  {i}. {item.get('name', 'Unknown')}")
            output.append(f"     类型: {item.get('asset_type', 'unknown')}")
            output.append(f"     路径: {item.get('path', 'N/A')}")
            output.append(f"     文件类型: {item.get('file_type', 'N/A')}")
            output.append(f"     大小: {item.get('size', 0)} bytes")
            
            # 显示宪法引用
            refs = item.get("constitutional_refs", [])
            if refs:
                output.append(f"     宪法引用: {', '.join(refs[:3])}")
                if len(refs) > 3:
                    output.append(f"               ... 等 {len(refs)} 个引用")
    
    return "\n".join(output)

def format_validate_result(result: dict) -> str:
    """格式化验证输出"""
    if not result.get("success", False):
        return f"❌ 验证失败: {result.get('error', 'Unknown error')}"
    
    validation = result.get("validation", {})
    if not validation:
        return "⚠️  验证结果为空"
    
    output = ["✅ 资产验证结果"]
    
    if validation.get("valid", False):
        output.append("状态: ✅ 验证通过")
    else:
        output.append("状态: ❌ 验证失败")
    
    errors = validation.get("errors", [])
    if errors:
        output.append("\n❌ 错误:")
        for error in errors:
            output.append(f"  - {error}")
    
    warnings = validation.get("warnings", [])
    if warnings:
        output.append("\n⚠️  警告:")
        for warning in warnings:
            output.append(f"  - {warning}")
    
    suggestions = validation.get("suggestions", [])
    if suggestions:
        output.append("\n💡 改进建议:")
        for suggestion in suggestions:
            output.append(f"  - {suggestion}")
    
    # 合规要求说明
    if result.get("compliance_required", False):
        output.append("\n📋 合规要求:")
        output.append("  • §101单一真理源原则引用")
        output.append("  • §102熵减原则引用")
    
    if result.get("theme_compliance_required", False):
        output.append("  • §119主题驱动开发公理引用")
        output.append("  • 禁止硬编码颜色值")
    
    return "\n".join(output)

def format_suggest_result(result: dict) -> str:
    """格式化复用建议输出"""
    if not result.get("success", False):
        return f"❌ 复用建议生成失败: {result.get('error', 'Unknown error')}"
    
    output = ["💡 资产复用建议"]
    output.append(f"📁 项目路径: {result.get('project_path', 'N/A')}")
    output.append(f"🔍 扫描资产数: {result.get('assets_scanned', 0)} 个")
    output.append(f"💡 生成建议数: {result.get('suggestions_found', 0)} 个")
    
    suggestions = result.get("suggestions", [])
    if suggestions:
        output.append("\n📋 复用建议:")
        for i, suggestion in enumerate(suggestions[:5], 1):  # 只显示前5个
            output.append(f"\n  {i}. {suggestion.get('asset', 'Unknown')}")
            output.append(f"     类型: {suggestion.get('type', 'unknown')}")
            output.append(f"     路径: {suggestion.get('path', 'N/A')}")
            output.append(f"     建议: {suggestion.get('suggestion', '')}")
            output.append(f"     原因: {suggestion.get('reason', '')}")
        
        if len(suggestions) > 5:
            output.append(f"\n  ... 以及 {len(suggestions) - 5} 个其他建议")
    
    recommendations = result.get("recommendations", [])
    if recommendations:
        output.append("\n🎯 推荐行动:")
        for recommendation in recommendations:
            output.append(f"  • {recommendation}")
    
    return "\n".join(output)

def format_stats_result(result: dict) -> str:
    """格式化统计输出"""
    if not result.get("success", False):
        return f"❌ 统计失败: {result.get('error', 'Unknown error')}"
    
    output = ["📊 资产库统计"]
    output.append(f"📁 资产库目录: {result.get('library_root', 'N/A')}")
    output.append(f"📅 生成时间: {result.get('timestamp', 'N/A')}")
    
    metrics = result.get("metrics", {})
    if metrics:
        output.append("\n📈 关键指标:")
        output.append(f"  • 总资产数: {metrics.get('total_assets', 0)} 个")
        
        asset_types = metrics.get("by_type", {})
        if asset_types:
            output.append(f"  • 资产类型分布:")
            for asset_type, count in sorted(asset_types.items()):
                percentage = (count / metrics.get('total_assets', 1)) * 100
                output.append(f"    - {asset_type}: {count} 个 ({percentage:.1f}%)")
        
        output.append(f"  • 平均文件大小: {metrics.get('avg_file_size', 0):.2f} bytes")
        output.append(f"  • 类型覆盖率: {metrics.get('coverage', 0)*100:.1f}%")
        output.append(f"  • 宪法合规率: {metrics.get('constitutional_compliance', 0)*100:.1f}%")
        output.append(f"  • 文档完整率: {metrics.get('documentation_completeness', 0)*100:.1f}%")
    
    summary = result.get("summary", {})
    if summary:
        output.append("\n📋 概要:")
        output.append(f"  • 合规状态: {'✅ 良好' if summary.get('constitutional_compliance', 0) > 0.8 else '⚠️ 需改进'}")
        output.append(f"  • 文档状态: {'✅ 良好' if summary.get('documentation_completeness', 0) > 0.7 else '⚠️ 需改进'}")
        output.append(f"  • 资产多样性: {'✅ 丰富' if len(metrics.get('by_type', {})) > 5 else '⚠️ 有限'}")
    
    return "\n".join(output)

# -----------------------------------------------------------------------------
# 主函数
# -----------------------------------------------------------------------------

def main():
    if not SERVICE_AVAILABLE:
        print("❌ 资产服务不可用")
        sys.exit(1)
    
    # 环境检查
    if not check_environment_integration():
        sys.exit(2)
    
    parser = argparse.ArgumentParser(
        description=f"CDD Asset Manager CLI v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/cdd_asset_manager.py scan --verbose       # 扫描资产库
  python scripts/cdd_asset_manager.py report --format text # 生成报告
  python scripts/cdd_asset_manager.py search "button"      # 搜索资产
  python scripts/cdd_asset_manager.py validate my_component.jsx  # 验证资产
  python scripts/cdd_asset_manager.py suggest ./my_project # 生成复用建议
  python scripts/cdd_asset_manager.py stats                # 查看统计
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # scan 子命令
    scan_parser = subparsers.add_parser("scan", help="扫描技术资产库")
    scan_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出模式")
    scan_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # report 子命令
    report_parser = subparsers.add_parser("report", help="生成资产报告")
    report_parser.add_argument("--format", "-f", choices=["json", "text"], default="text", help="报告格式")
    report_parser.add_argument("--output", "-o", help="输出文件路径")
    report_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式（快捷方式）")
    
    # search 子命令
    search_parser = subparsers.add_parser("search", help="搜索资产")
    search_parser.add_argument("query", help="搜索查询词")
    search_parser.add_argument("--type", "-t", help="资产类型过滤")
    search_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # validate 子命令
    validate_parser = subparsers.add_parser("validate", help="验证新资产")
    validate_parser.add_argument("file", help="资产文件路径")
    validate_parser.add_argument("--content", "-c", help="资产内容（如不指定则从文件读取）")
    validate_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # suggest 子命令
    suggest_parser = subparsers.add_parser("suggest", help="生成资产复用建议")
    suggest_parser.add_argument("project_path", help="项目路径")
    suggest_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # stats 子命令
    stats_parser = subparsers.add_parser("stats", help="查看资产统计")
    stats_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 初始化资产服务
    asset_service = AssetService()
    
    # 执行命令
    try:
        if args.command == "scan":
            result = asset_service.scan_assets(verbose=args.verbose)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"🔧 CDD Asset Manager v{VERSION}")
                print()
                print(format_scan_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
        
        elif args.command == "report":
            # 确定输出格式
            format_type = "json" if args.json else args.format
            
            result = asset_service.generate_report(format=format_type)
            
            # 输出到文件或控制台
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    if format_type == "json":
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    else:
                        f.write(format_report_result(result))
                print(f"✅ 报告已保存到: {args.output}")
            else:
                if format_type == "json":
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print(f"📋 CDD Asset Report v{VERSION}")
                    print()
                    print(format_report_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
        
        elif args.command == "search":
            result = asset_service.search(query=args.query, asset_type=args.type)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"🔍 CDD Asset Search v{VERSION}")
                print()
                print(format_search_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
        
        elif args.command == "validate":
            # 读取资产内容
            file_path = Path(args.file)
            if args.content:
                content = args.content
            else:
                if not file_path.exists():
                    print(f"❌ 文件不存在: {file_path}")
                    sys.exit(1)
                try:
                    content = file_path.read_text(encoding='utf-8')
                except Exception as e:
                    print(f"❌ 无法读取文件: {e}")
                    sys.exit(1)
            
            result = asset_service.validate(file_path=str(file_path), content=content)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"✅ CDD Asset Validator v{VERSION}")
                print(f"   文件: {file_path}")
                print()
                print(format_validate_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
        
        elif args.command == "suggest":
            result = asset_service.suggest_reuse(project_path=args.project_path)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"💡 CDD Reuse Suggester v{VERSION}")
                print()
                print(format_suggest_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
        
        elif args.command == "stats":
            # 使用报告功能生成统计
            result = asset_service.generate_report(format="json")
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"📊 CDD Asset Statistics v{VERSION}")
                print()
                print(format_stats_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  操作被用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        sys.exit(1)

# -----------------------------------------------------------------------------
# Claude Code桥梁接口
# -----------------------------------------------------------------------------

def scan_assets_claude(verbose: bool = False, **kwargs) -> dict:
    """Claude Code资产扫描接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "AssetService not available"}
    
    asset_service = AssetService()
    return asset_service.scan_assets(verbose=verbose)

def search_assets_claude(query: str, asset_type: Optional[str] = None, **kwargs) -> dict:
    """Claude Code资产搜索接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "AssetService not available"}
    
    asset_service = AssetService()
    return asset_service.search(query=query, asset_type=asset_type)

def validate_asset_claude(file_path: str, content: str = "", **kwargs) -> dict:
    """Claude Code资产验证接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "AssetService not available"}
    
    asset_service = AssetService()
    
    # 如果没有提供内容，尝试从文件读取
    if not content:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"无法读取文件: {e}",
                "file_path": file_path
            }
    
    return asset_service.validate(asset_path=file_path, content=content)

def suggest_reuse_claude(project_path: str, **kwargs) -> dict:
    """Claude Code资产复用建议接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "AssetService not available"}
    
    asset_service = AssetService()
    return asset_service.suggest_reuse(project_path=project_path)

if __name__ == "__main__":
    main()