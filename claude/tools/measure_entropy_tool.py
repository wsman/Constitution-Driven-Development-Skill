#!/usr/bin/env python3
"""
Measure Entropy Tool (measure_entropy_tool.py) v2.0.0
=====================================================
Claude Code熵值测量工具API层，调用services/entropy_service.py。

宪法依据: §102§309
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from .tool_registry import BaseTool, cdd_tool

# 导入新的服务层
try:
    from core.entropy_service import EntropyService
    SERVICE_AVAILABLE = True
except ImportError:
    SERVICE_AVAILABLE = False
    EntropyService = None


@cdd_tool(name="measure_entropy", description="CDD系统熵值测量工具")
class MeasureEntropyTool(BaseTool):
    """CDD熵值测量工具API层"""
    
    name = "measure_entropy"
    description = "测量和分析系统熵值 (H_sys)"
    version = "2.0.0"
    constitutional_basis = ["§102", "§309"]
    
    def execute(self, project_path: str = ".", analyze: bool = False, 
                optimize: bool = False, top_n: int = 10, **kwargs) -> Dict[str, Any]:
        """
        测量系统熵值
        
        Args:
            project_path: 项目路径（默认为当前目录）
            analyze: 是否进行熵值热点分析
            optimize: 是否生成优化建议（仅分析不执行）
            top_n: 显示前N个热点（分析模式）
            
        Returns:
            Dict[str, Any]: 熵值测量结果
        """
        try:
            if not SERVICE_AVAILABLE:
                return self.create_response(
                    success=False,
                    error="EntropyService not available. Please check services/ directory."
                )
            
            path = Path(project_path).resolve()
            entropy_service = EntropyService(path)
            
            # 测量熵值
            entropy_result = entropy_service.calculate_entropy()
            
            # 准备基础响应
            response = {
                "success": True,
                "project_path": str(path),
                "entropy_metrics": entropy_result,
                "constitutional_compliance": entropy_result.get("constitutional_compliance", False),
                "status": entropy_result.get("status", "未知"),
                "tool_version": self.version
            }
            
            # 如果需要分析热点
            if analyze:
                analysis_result = entropy_service.analyze_hotspots(top_n=top_n)
                response["hotspots"] = analysis_result.get("hotspots", [])
                response["hotspots_count"] = len(response["hotspots"])
                
                # 计算熵值统计
                if response["hotspots"]:
                    max_entropy = max(h["entropy"] for h in response["hotspots"])
                    avg_entropy = sum(h["entropy"] for h in response["hotspots"]) / len(response["hotspots"])
                    response["hotspot_statistics"] = {
                        "max_entropy": max_entropy,
                        "average_entropy": avg_entropy,
                        "critical_hotspots": len([h for h in response["hotspots"] if h["entropy"] > 0.5])
                    }
            
            # 如果需要生成优化建议
            if optimize:
                optimization_result = entropy_service.generate_optimization_plan(dry_run=True)
                
                response["optimization_plan"] = {
                    "dry_run": True,
                    "actions_planned": optimization_result.get("actions_planned", 0),
                    "actions": optimization_result.get("actions", [])
                }
                response["optimization_suggestions"] = self._generate_optimization_suggestions(
                    entropy_result,
                    response.get("hotspots", [])
                )
            
            # 添加熵值评估
            response["entropy_assessment"] = entropy_service.assess_entropy_level(
                entropy_result.get("h_sys", 1.0)
            )
            
            return response
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Entropy measurement failed: {str(e)}"
            )
    
    def _generate_optimization_suggestions(self, metrics: Dict[str, Any], 
                                          hotspots: List[Dict[str, Any]]) -> List[str]:
        """生成优化建议"""
        suggestions = []
        h_sys = metrics.get("h_sys", 1.0)
        
        # 基于熵值水平的建议
        if h_sys > 0.7:
            suggestions.append("🟥 **紧急**: 系统熵值过高，需要立即重构")
            suggestions.append("优先处理高熵值热点，减少认知复杂度")
        elif h_sys > 0.5:
            suggestions.append("🟧 **重要**: 系统熵值较高，建议进行优化")
            suggestions.append("关注目录结构和接口覆盖率的改进")
        elif h_sys > 0.3:
            suggestions.append("🟨 **建议**: 系统熵值正常，可以保持或微调")
            suggestions.append("定期监控熵值变化，防止熵增")
        else:
            suggestions.append("🟩 **优秀**: 系统熵值很低，保持现状")
            suggestions.append("继续遵循CDD最佳实践")
        
        # 基于热点的具体建议
        if hotspots:
            critical_hotspots = [h for h in hotspots if h.get("entropy", 0) > 0.5]
            if critical_hotspots:
                suggestions.append(f"**发现 {len(critical_hotspots)} 个高熵值热点**:")
                for h in critical_hotspots[:3]:  # 显示前3个
                    suggestions.append(f"  - {h.get('path', 'Unknown')}: {h.get('reason', 'No reason')}")
        
        # 基于组件熵值的建议
        c_dir = metrics.get("c_dir", 0)
        c_sig = metrics.get("c_sig", 0)
        c_test = metrics.get("c_test", 0)
        
        if c_dir < 0.5:
            suggestions.append("📁 **目录结构**: 改善目录组织结构，确保必要目录存在")
        if c_sig < 0.5:
            suggestions.append("🔧 **接口签名**: 增加类型注解和接口定义")
        if c_test < 0.5:
            suggestions.append("✅ **测试覆盖**: 增加测试用例，提高测试覆盖率")
        
        return suggestions
    
    def get_entropy_thresholds(self) -> Dict[str, Any]:
        """获取熵值阈值配置"""
        try:
            if not SERVICE_AVAILABLE:
                return {
                    "error": "EntropyService not available",
                    "tool_version": self.version
                }
            
            entropy_service = EntropyService()
            return {
                **entropy_service.get_entropy_thresholds(),
                "tool_version": self.version
            }
        except Exception:
            # 回退到默认阈值
            return {
                "excellent": {
                    "max": 0.3,
                    "description": "🟢 优秀 - 熵值控制良好"
                },
                "good": {
                    "min": 0.3,
                    "max": 0.5,
                    "description": "🟡 良好 - 熵值在可控范围"
                },
                "warning": {
                    "min": 0.5,
                    "max": 0.7,
                    "description": "🟠 警告 - 熵值较高，建议优化"
                },
                "danger": {
                    "min": 0.7,
                    "description": "🔴 危险 - 熵值过高，需要立即重构"
                },
                "tool_version": self.version
            }
    
    def calculate_quick_entropy(self, project_path: str = ".") -> Dict[str, Any]:
        """
        快速熵值计算（轻量级）
        
        Args:
            project_path: 项目路径
            
        Returns:
            Dict[str, Any]: 快速熵值估算
        """
        try:
            if not SERVICE_AVAILABLE:
                return self.create_response(
                    success=False,
                    error="EntropyService not available"
                )
            
            path = Path(project_path).resolve()
            entropy_service = EntropyService(path)
            
            quick_result = entropy_service.calculate_quick_estimate()
            quick_result["tool_version"] = self.version
            
            return quick_result
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Quick entropy calculation failed: {str(e)}"
            )


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CDD Entropy Measurement Tool CLI")
    
    parser.add_argument("--project", "-p", default=".", help="Project path")
    parser.add_argument("--analyze", "-a", action="store_true", help="Analyze entropy hotspots")
    parser.add_argument("--optimize", "-o", action="store_true", help="Generate optimization suggestions")
    parser.add_argument("--top-n", type=int, default=10, help="Top N hotspots for analysis")
    parser.add_argument("--quick", "-q", action="store_true", help="Quick entropy estimate")
    parser.add_argument("--thresholds", action="store_true", help="Show entropy thresholds")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    tool = MeasureEntropyTool()
    
    if args.thresholds:
        result = tool.get_entropy_thresholds()
        output_format = args.format
    elif args.quick:
        result = tool.calculate_quick_entropy(project_path=args.project)
        output_format = args.format
    else:
        result = tool.execute(
            project_path=args.project,
            analyze=args.analyze,
            optimize=args.optimize,
            top_n=args.top_n
        )
        output_format = args.format
    
    # 输出结果
    if output_format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        _print_text_result(result, args)
    
    return 0 if result.get("success", False) else 1


def _print_text_result(result: Dict[str, Any], args):
    """打印文本格式结果"""
    if not result.get("success", False):
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        return
    
    if args.thresholds:
        print("📊 CDD 熵值阈值配置")
        thresholds = result
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
        if "tool_version" in thresholds:
            print(f"\n工具版本: {thresholds['tool_version']}")
        return
    
    print(f"\n📊 CDD 熵值测量报告")
    print(f"项目路径: {result.get('project_path', 'Unknown')}")
    
    metrics = result.get("entropy_metrics", {})
    if metrics:
        print(f"\n📈 熵值指标:")
        print(f"  H_sys (系统熵值): {metrics.get('h_sys', 0):.4f} [{metrics.get('status', 'Unknown')}]")
        print(f"  C_dir (目录合规): {metrics.get('c_dir', 0):.2%}")
        print(f"  C_sig (接口覆盖): {metrics.get('c_sig', 0):.2%}")
        print(f"  C_test (测试通过): {metrics.get('c_test', 0):.2%}")
    
    assessment = result.get("entropy_assessment", {})
    if assessment:
        print(f"\n📋 熵值评估: {assessment.get('color', '')} {assessment.get('description', '')}")
        print(f"  当前熵值: {assessment.get('current', 0):.4f}")
        print(f"  警告阈值: {assessment.get('threshold', 0.7)}")
    
    hotspots = result.get("hotspots", [])
    if hotspots:
        print(f"\n🔥 熵值热点分析 (前{len(hotspots)}个):")
        for i, h in enumerate(hotspots, 1):
            print(f"  {i}. {h.get('path', 'Unknown')}")
            print(f"     熵值: {h.get('entropy', 0):.2f} - {h.get('reason', 'No reason')}")
    
    suggestions = result.get("optimization_suggestions", [])
    if suggestions:
        print(f"\n💡 优化建议:")
        for s in suggestions:
            print(f"  {s}")
    
    if result.get("h_sys_estimate") is not None or result.get("quick_estimate", False):
        print(f"\n⚡ 快速估算结果:")
        print(f"  目录合规率: {result.get('directory_score', 0):.2%}")
        print(f"  发现目录: {', '.join(result.get('critical_dirs_found', []))}")
        if result.get('critical_dirs_missing', []):
            print(f"  缺失目录: {', '.join(result.get('critical_dirs_missing', []))}")
    
    if "tool_version" in result:
        print(f"\n🔧 工具版本: {result['tool_version']}")


if __name__ == "__main__":
    sys.exit(main())