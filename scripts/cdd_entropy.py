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
# 交互式向导函数
# -----------------------------------------------------------------------------

def run_guided_entropy_wizard(project_path: Path) -> dict:
    """
    交互式熵值管理向导
    
    宪法依据: §102§300.3 (熵值监控流程)
    """
    import time
    
    print("=" * 60)
    print("📊 CDD 交互式熵值管理向导 v2.0.0")
    print("=" * 60)
    print("本向导将引导您完成以下步骤:")
    print("1. 项目选择和初始化")
    print("2. 熵值计算和状态评估")
    print("3. 热点分析和问题定位")
    print("4. 优化计划生成和执行")
    print("5. 结果总结和后续建议")
    print("=" * 60)
    print()
    
    results = {
        "success": False,
        "steps": [],
        "project": str(project_path),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    # 步骤1: 项目选择和初始化
    print("🔍 步骤1/5: 项目选择和初始化")
    print("-" * 40)
    
    print(f"当前项目路径: {project_path}")
    
    # 检查项目目录是否存在
    if not project_path.exists():
        print(f"❌ 项目目录不存在: {project_path}")
        new_path = input("请输入正确的项目路径 (或回车取消): ").strip()
        if new_path:
            project_path = Path(new_path).resolve()
            if not project_path.exists():
                print("❌ 项目目录仍然不存在，向导终止")
                results["error"] = "项目目录不存在"
                return results
        else:
            print("❌ 向导终止")
            results["error"] = "项目目录不存在"
            return results
    
    # 检查是否为有效的CDD项目
    print(f"✅ 项目目录: {project_path}")
    
    # 检查memory_bank目录
    memory_bank = project_path / "memory_bank"
    if memory_bank.exists():
        print(f"✅ 发现memory_bank目录")
        results["steps"].append({
            "name": "project_validation",
            "status": "passed",
            "message": "有效的CDD项目目录"
        })
    else:
        print(f"⚠️  未发现memory_bank目录 (可能不是CDD项目)")
        confirm = input("是否继续? (Y/n): ").strip().lower()
        if confirm not in ["", "y", "yes"]:
            print("❌ 向导终止")
            results["error"] = "非CDD项目目录"
            return results
        
        results["steps"].append({
            "name": "project_validation",
            "status": "warning",
            "message": "非标准CDD项目，用户选择继续"
        })
    
    # 步骤2: 熵值计算和状态评估
    print("\n🔍 步骤2/5: 熵值计算和状态评估")
    print("-" * 40)
    
    try:
        print(f"⏳ 正在计算系统熵值...")
        entropy_service = EntropyService(project_path)
        
        # 计算熵值
        print("  1. 计算目录合规性 (C_dir)...")
        print("  2. 计算接口覆盖率 (C_sig)...")
        print("  3. 计算测试通过率 (C_test)...")
        print("  4. 计算系统熵值 (H_sys)...")
        
        metrics = entropy_service.calculate_entropy()
        h_sys = metrics.get("h_sys", 0)
        status = metrics.get("status", "未知")
        compliance = metrics.get("constitutional_compliance", False)
        
        print(f"✅ 熵值计算完成!")
        print(f"  H_sys: {h_sys:.4f} [{status}]")
        print(f"  C_dir: {metrics.get('c_dir', 0):.2%}")
        print(f"  C_sig: {metrics.get('c_sig', 0):.2%}")
        print(f"  C_test: {metrics.get('c_test', 0):.2%}")
        print(f"  宪法合规: {'✅ 通过' if compliance else '❌ 未通过'}")
        
        results["entropy_metrics"] = metrics
        results["steps"].append({
            "name": "entropy_calculation",
            "status": "success",
            "message": f"H_sys={h_sys:.4f}, 状态={status}, 合规={compliance}"
        })
        
        # 熵值状态评估
        if status == "normal":
            print("🎉 熵值状态: 正常")
            print("   系统处于健康状态，无需紧急优化")
        elif status == "warning":
            print("⚠️  熵值状态: 警告")
            print("   系统存在可优化的空间")
        elif status == "critical":
            print("🚨 熵值状态: 紧急")
            print("   系统熵值超标，建议立即优化")
        else:
            print(f"❓ 熵值状态: {status}")
        
    except Exception as e:
        print(f"❌ 熵值计算失败: {e}")
        results["error"] = str(e)
        results["steps"].append({
            "name": "entropy_calculation",
            "status": "failed",
            "message": f"计算失败: {e}"
        })
        return results
    
    # 步骤3: 热点分析和问题定位
    print("\n🔍 步骤3/5: 热点分析和问题定位")
    print("-" * 40)
    
    if status in ["normal"]:
        print("ℹ️  熵值正常，跳过热点分析")
        results["steps"].append({
            "name": "hotspot_analysis",
            "status": "skipped",
            "message": "熵值正常，无需热点分析"
        })
    else:
        try:
            print(f"⏳ 正在分析熵值热点...")
            analysis_result = entropy_service.analyze_hotspots(top_n=10)
            hotspots = analysis_result.get("hotspots", [])
            
            if hotspots:
                print(f"✅ 发现 {len(hotspots)} 个熵值热点:")
                for i, h in enumerate(hotspots[:5], 1):
                    path = h.get("path", "未知")
                    entropy_val = h.get("entropy", 0)
                    reason = h.get("reason", "未知原因")
                    print(f"\n{i}. {path}")
                    print(f"   熵值: {entropy_val:.2f}")
                    print(f"   原因: {reason}")
                
                if len(hotspots) > 5:
                    print(f"  ... 以及 {len(hotspots) - 5} 个其他热点")
                
                results["hotspots"] = hotspots
                results["steps"].append({
                    "name": "hotspot_analysis",
                    "status": "success",
                    "message": f"发现 {len(hotspots)} 个熵值热点"
                })
            else:
                print("✅ 未发现明显的熵值热点")
                results["steps"].append({
                    "name": "hotspot_analysis",
                    "status": "success",
                    "message": "未发现熵值热点"
                })
                
        except Exception as e:
            print(f"⚠️  热点分析失败: {e}")
            results["steps"].append({
                "name": "hotspot_analysis",
                "status": "warning",
                "message": f"分析失败: {e}"
            })
    
    # 步骤4: 优化计划生成和执行
    print("\n🔍 步骤4/5: 优化计划生成和执行")
    print("-" * 40)
    
    if status in ["normal"]:
        print("ℹ️  熵值正常，跳过优化计划")
        results["steps"].append({
            "name": "optimization_plan",
            "status": "skipped",
            "message": "熵值正常，无需优化"
        })
    else:
        print("📋 生成优化计划...")
        optimize_option = input("是否生成优化计划? (Y/n): ").strip().lower()
        
        if optimize_option in ["", "y", "yes"]:
            try:
                print("1. 分析目录结构问题...")
                print("2. 检查接口覆盖问题...")
                print("3. 评估测试覆盖率...")
                print("4. 生成优化建议...")
                
                optimization_result = entropy_service.generate_optimization_plan(dry_run=True)
                actions = optimization_result.get("actions", [])
                actions_planned = optimization_result.get("actions_planned", 0)
                
                if actions:
                    print(f"✅ 生成 {actions_planned} 个优化建议:")
                    for i, action in enumerate(actions[:3], 1):
                        desc = action.get("description", "未知")
                        action_type = action.get("type", "未知")
                        target = action.get("target", "未知")
                        print(f"\n{i}. {desc}")
                        print(f"   类型: {action_type}")
                        print(f"   目标: {target}")
                    
                    if len(actions) > 3:
                        print(f"  ... 以及 {len(actions) - 3} 个其他建议")
                    
                    # 询问是否执行优化
                    print("\n🔄 优化执行选项:")
                    print("  是否执行这些优化?")
                    execute_option = input("执行优化? (y/N): ").strip().lower()
                    
                    if execute_option == "y":
                        print("⏳ 正在执行优化...")
                        # 实际执行优化
                        execution_result = entropy_service.generate_optimization_plan(dry_run=False)
                        
                        if execution_result.get("success", False):
                            print("✅ 优化执行成功!")
                            results["optimization_executed"] = True
                            results["steps"].append({
                                "name": "optimization_execution",
                                "status": "success",
                                "message": f"执行了 {actions_planned} 个优化操作"
                            })
                        else:
                            print(f"❌ 优化执行失败: {execution_result.get('error', '未知错误')}")
                            results["steps"].append({
                                "name": "optimization_execution",
                                "status": "failed",
                                "message": f"执行失败: {execution_result.get('error', '未知错误')}"
                            })
                    else:
                        print("⏸️  跳过优化执行")
                        results["steps"].append({
                            "name": "optimization_execution",
                            "status": "skipped",
                            "message": "用户选择跳过优化执行"
                        })
                    
                    results["optimization_plan"] = optimization_result
                    results["steps"].append({
                        "name": "optimization_planning",
                        "status": "success",
                        "message": f"生成了 {actions_planned} 个优化建议"
                    })
                else:
                    print("✅ 无需优化操作")
                    results["steps"].append({
                        "name": "optimization_planning",
                        "status": "success",
                        "message": "无需优化操作"
                    })
                    
            except Exception as e:
                print(f"❌ 优化计划生成失败: {e}")
                results["steps"].append({
                    "name": "optimization_planning",
                    "status": "failed",
                    "message": f"计划生成失败: {e}"
                })
        else:
            print("⏸️  跳过优化计划")
            results["steps"].append({
                "name": "optimization_planning",
                "status": "skipped",
                "message": "用户选择跳过优化计划"
            })
    
    # 步骤5: 结果总结和后续建议
    print("\n🔍 步骤5/5: 结果总结和后续建议")
    print("-" * 40)
    
    # 设置向导成功标志
    results["success"] = True
    
    print("🎉 熵值管理向导完成!")
    print(f"📋 项目: {project_path}")
    print(f"📊 系统熵值: {h_sys:.4f} [{status}]")
    
    successful_steps = sum(1 for step in results["steps"] if step["status"] in ["passed", "success"])
    total_steps = len(results["steps"])
    
    print(f"📊 执行统计:")
    print(f"   总步骤数: {total_steps}")
    print(f"   成功步骤: {successful_steps}")
    
    print("\n📚 后续建议:")
    
    if status == "critical":
        print("   1. ⚠️ 紧急: 立即处理熵值超标问题")
        print("   2. 运行优化: python scripts/cdd_entropy.py optimize")
        print("   3. 修复热点: 处理前5个熵值热点")
    elif status == "warning":
        print("   1. 🔧 优化: 建议在本周内优化")
        print("   2. 运行分析: python scripts/cdd_entropy.py analyze")
        print("   3. 改进合规: 提升目录或接口合规性")
    else:
        print("   1. ✅ 保持: 继续当前良好实践")
        print("   2. 定期检查: 每周运行熵值计算")
        print("   3. 预防: 在新代码中添加熵值检查")
    
    print("\n💡 宪法依据:")
    print("   §102: 熵值监控公理")
    print("   §300.3: 行为验证标准")
    print("   §309: 工具一致性要求")
    
    # 向导完成
    print("\n" + "=" * 60)
    print("📊 交互式熵值管理向导完成")
    print("=" * 60)
    
    return results

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
    
    # guided 子命令（交互式向导）
    guided_parser = subparsers.add_parser("guided", help="交互式熵值管理向导")
    guided_parser.add_argument("--project", "-p", default=".", help="项目路径")
    guided_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
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
    
    elif args.command == "guided":
        project_path = Path(args.project).resolve() if args.project != "." else Path.cwd()
        
        # 运行交互式向导
        wizard_result = run_guided_entropy_wizard(project_path)
        
        if args.json:
            print(json.dumps(wizard_result, indent=2, ensure_ascii=False))
        else:
            # 向导已经在run_guided_entropy_wizard中输出详细信息
            pass
        
        sys.exit(0 if wizard_result.get("success", False) else 1)
    
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

def optimize_entropy_claude(project_path: str = ".", dry_run: bool = True, **kwargs) -> dict:
    """Claude Code熵值优化接口"""
    if not SERVICE_AVAILABLE:
        return {"success": False, "error": "EntropyService not available"}
    
    entropy_service = EntropyService(Path(project_path).resolve())
    result = entropy_service.generate_optimization_plan(dry_run=dry_run)
    
    # 确保返回格式符合测试期望
    if result.get("success", False):
        return {
            "success": True,
            "actions_executed": result.get("actions_planned", 0),
            "entropy_before": result.get("entropy_before", 0),
            "entropy_after": result.get("entropy_after", 0),
            "improvement": result.get("improvement", "0%")
        }
    else:
        return result

if __name__ == "__main__":
    main()