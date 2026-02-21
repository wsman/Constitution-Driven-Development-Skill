#!/usr/bin/env python3
"""
CDD Entropy CLI Wrapper (cdd_entropy.py) v2.0.0
===============================================
简化CLI包装层，调用services/entropy_service.py核心业务逻辑。

宪法依据: §102§309

Usage:
    python scripts/cdd_entropy.py calculate [--project /path]
    python scripts/cdd_entropy.py analyze [--project /path] [--top-n 20]
    python scripts/cdd_entropy.py optimize [--project /path] [--dry-run]
    python scripts/cdd_entropy.py cache [--clear|--info]
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
    from core.entropy_service import EntropyService
    from utils.cache_manager import CacheManager
    SERVICE_AVAILABLE = True
except ImportError as e:
    SERVICE_AVAILABLE = False
    print(f"❌ 无法导入services层: {e}")
    print("请确保services目录存在且包含entropy_service.py")

VERSION = "2.0.0"

# -----------------------------------------------------------------------------
# CLI输出格式化
# -----------------------------------------------------------------------------

def format_entropy_result(result: dict) -> str:
    """格式化熵值计算结果"""
    if not result.get("success", False):
        return f"❌ 错误: {result.get('error', 'Unknown error')}"
    
    metrics = result.get("entropy_metrics", {})
    if not metrics:
        return "⚠️ 未找到熵值指标"
    
    output = [f"📊 CDD 熵值报告 (v{VERSION})"]
    
    h_sys = metrics.get("h_sys", 0)
    status = metrics.get("status", "未知")
    
    output.append(f"H_sys (系统熵值): {h_sys:.4f} [{status}]")
    output.append(f"C_dir (目录合规): {metrics.get('c_dir', 0):.2%}")
    output.append(f"C_sig (接口覆盖): {metrics.get('c_sig', 0):.2%}")
    output.append(f"C_test (测试通过): {metrics.get('c_test', 0):.2%}")
    
    compliance = result.get("constitutional_compliance", False)
    output.append(f"宪法合规: {'✅ 通过' if compliance else '❌ 未通过'}")
    
    return "\n".join(output)

def format_analysis_result(result: dict, top_n: int = 10) -> str:
    """格式化热点分析结果"""
    if not result.get("success", False):
        return f"❌ 错误: {result.get('error', 'Unknown error')}"
    
    hotspots = result.get("hotspots", [])
    if not hotspots:
        return "✅ 未发现明显的熵值热点"
    
    output = [f"🔥 熵值热点分析 (前{len(hotspots)}个):"]
    
    for i, h in enumerate(hotspots, 1):
        output.append(f"\n{i}. {h.get('path', 'Unknown')}")
        output.append(f"   熵值: {h.get('entropy', 0):.2f}")
        output.append(f"   原因: {h.get('reason', 'No reason')}")
        suggestions = h.get("suggestions", [])
        if suggestions:
            output.append(f"   建议: {', '.join(suggestions)}")
    
    return "\n".join(output)

def format_optimization_result(result: dict) -> str:
    """格式化优化计划结果"""
    if not result.get("success", False):
        return f"❌ 错误: {result.get('error', 'Unknown error')}"
    
    dry_run = result.get("dry_run", True)
    actions_planned = result.get("actions_planned", 0)
    actions = result.get("actions", [])
    
    output = [f"⚡ 熵值优化 {'(模拟运行)' if dry_run else ''}"]
    output.append(f"计划操作数: {actions_planned}")
    
    if actions:
        for i, action in enumerate(actions, 1):
            output.append(f"\n{i}. {action.get('description', 'Unknown')}")
            output.append(f"   类型: {action.get('type', 'unknown')}")
            output.append(f"   目标: {action.get('target', 'N/A')}")
    
    if not actions:
        output.append("✅ 当前无需优化操作")
    
    return "\n".join(output)

def format_cache_info(info: dict) -> str:
    """格式化缓存信息"""
    if not info.get("exists", False):
        return "📁 无缓存文件"
    
    output = ["📁 熵值缓存信息:"]
    output.append(f"键数量: {len(info.get('keys', []))}")
    output.append(f"缓存大小: {info.get('size', 0)} 字节")
    
    keys = info.get("keys", [])
    if keys:
        output.append(f"缓存键: {', '.join(keys[:5])}")
        if len(keys) > 5:
            output.append(f"  ... 以及 {len(keys) - 5} 个其他键")
    
    return "\n".join(output)

# -----------------------------------------------------------------------------
# 主函数
# -----------------------------------------------------------------------------

def main():
    if not SERVICE_AVAILABLE:
        print("❌ 熵值服务不可用")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description=f"CDD Entropy CLI v{VERSION}")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # calculate 子命令
    calc_parser = subparsers.add_parser("calculate", help="计算系统熵值")
    calc_parser.add_argument("--project", "-p", default=".", help="项目路径")
    calc_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    calc_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    calc_parser.add_argument("--force", action="store_true", help="强制重新计算")
    
    # analyze 子命令
    analyze_parser = subparsers.add_parser("analyze", help="分析熵值热点")
    analyze_parser.add_argument("--project", "-p", default=".", help="项目路径")
    analyze_parser.add_argument("--top-n", type=int, default=10, help="显示前N个热点")
    analyze_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # optimize 子命令
    optimize_parser = subparsers.add_parser("optimize", help="熵值优化")
    optimize_parser.add_argument("--project", "-p", default=".", help="项目路径")
    optimize_parser.add_argument("--dry-run", action="store_true", help="模拟运行模式")
    optimize_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # cache 子命令
    cache_parser = subparsers.add_parser("cache", help="缓存管理")
    cache_parser.add_argument("--project", "-p", default=".", help="项目路径")
    cache_parser.add_argument("--clear", action="store_true", help="清除缓存")
    cache_parser.add_argument("--info", action="store_true", help="显示缓存信息")
    cache_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # thresholds 子命令
    thresholds_parser = subparsers.add_parser("thresholds", help="显示熵值阈值")
    thresholds_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行命令
    if args.command == "calculate":
        project_path = Path(args.project).resolve() if args.project != "." else Path.cwd()
        entropy_service = EntropyService(project_path)
        
        try:
            # 服务层返回原始指标字典
            metrics = entropy_service.calculate_entropy()
            result = {
                "success": True,
                "entropy_metrics": metrics,
                "constitutional_compliance": metrics.get("constitutional_compliance", False)
            }
        except Exception as e:
            result = {
                "success": False,
                "error": str(e)
            }
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"🔧 CDD Entropy CLI v{VERSION}")
            print(f"   目标: {project_path}")
            print()
            print(format_entropy_result(result))
        
        sys.exit(0 if result.get("success", True) else 1)
    
    elif args.command == "analyze":
        project_path = Path(args.project).resolve() if args.project != "." else Path.cwd()
        entropy_service = EntropyService(project_path)
        result = entropy_service.analyze_hotspots(top_n=args.top_n)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"🔍 CDD Entropy Analyzer v{VERSION}")
            print(f"   目标: {project_path}")
            print()
            print(format_analysis_result(result, args.top_n))
        
        sys.exit(0 if result.get("success", False) else 1)
    
    elif args.command == "optimize":
        project_path = Path(args.project).resolve() if args.project != "." else Path.cwd()
        entropy_service = EntropyService(project_path)
        result = entropy_service.generate_optimization_plan(dry_run=args.dry_run)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"⚡ CDD Entropy Optimizer v{VERSION}")
            print(f"   目标: {project_path}")
            print()
            print(format_optimization_result(result))
        
        sys.exit(0)
    
    elif args.command == "cache":
        project_path = Path(args.project).resolve() if args.project != "." else Path.cwd()
        cache = CacheManager(project_path)
        
        if args.clear:
            cache.clear_cache()
            result = {"success": True, "action": "clear", "message": "缓存已清除"}
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("✅ 熵值缓存已清除")
        
        elif args.info:
            info = cache.get_cache_info()
            if args.json:
                print(json.dumps(info, indent=2))
            else:
                print(format_cache_info(info))
        
        else:
            print("请指定 --clear 或 --info")
            sys.exit(1)
    
    elif args.command == "thresholds":
        entropy_service = EntropyService()
        thresholds = entropy_service.get_entropy_thresholds()
        
        if args.json:
            print(json.dumps(thresholds, indent=2, ensure_ascii=False))
        else:
            print("📊 CDD 熵值阈值配置")
            for level, config in thresholds.items():
                if level == "tool_version":
                    continue
                if isinstance(config, dict):
                    desc = config.get("description", "N/A")
                    if "max" in config:
                        print(f"  {desc} (≤ {config['max']})")
                    elif "min" in config:
                        min_val = config.get("min", "?")
                        max_val = config.get("max", "")
                        if max_val:
                            print(f"  {desc} ({min_val} - {max_val})")
                        else:
                            print(f"  {desc} (≥ {min_val})")
    
    else:
        parser.print_help()

# -----------------------------------------------------------------------------
# Claude Code桥梁接口 (保持向后兼容)
# -----------------------------------------------------------------------------

def measure_entropy_claude(project_path: str = ".", **kwargs) -> dict:
    """Claude Code熵值测量接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "EntropyService not available"}
    
    entropy_service = EntropyService(Path(project_path).resolve())
    result = entropy_service.calculate_entropy()
    return {
        "success": True,
        "metrics": result.get("entropy_metrics", {}),
        "constitutional_compliance": result.get("constitutional_compliance", False)
    }

def analyze_entropy_claude(project_path: str = ".", top_n: int = 10, **kwargs) -> dict:
    """Claude Code熵值分析接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "EntropyService not available"}
    
    entropy_service = EntropyService(Path(project_path).resolve())
    result = entropy_service.analyze_hotspots(top_n=top_n)
    return result

def get_entropy_thresholds_claude(**kwargs) -> dict:
    """Claude Code熵值阈值接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "EntropyService not available"}
    
    entropy_service = EntropyService()
    return {
        "success": True,
        "thresholds": entropy_service.get_entropy_thresholds()
    }

if __name__ == "__main__":
    main()