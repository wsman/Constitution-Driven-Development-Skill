#!/usr/bin/env python3
"""
CDD Asset Tool (cdd_asset_tool.py) v2.0.0
=========================================
Claude Code技术资产管理工具API层，调用services/asset_service.py。

宪法依据: §101单一真理源原则、§102熵减原则、§103文档优先公理

使用场景:
1. State A→B阶段：强制搜索现有技术资产
2. 资产审计阶段：定期检查资产质量和复用率
3. 资产贡献阶段：标准化资产入库流程
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

try:
    from claude_tools.tool_registry import BaseTool, cdd_tool
except ImportError:
    from tool_registry import BaseTool, cdd_tool

# 导入新的服务层
try:
    from core.asset_service import AssetService
    SERVICE_AVAILABLE = True
except ImportError as e:
    SERVICE_AVAILABLE = False
    AssetService = None
    print(f"⚠️  AssetService import error: {e}")


@cdd_tool(name="cdd_asset", description="CDD技术资产管理工具")
class CDDAssetTool(BaseTool):
    """CDD技术资产管理工具API层"""
    
    name = "cdd_asset"
    description = "技术资产库的扫描、搜索、验证和管理"
    version = "2.0.0"
    constitutional_basis = ["§101", "§102", "§103", "§309"]
    
    def execute(self, command: str = "scan", **kwargs) -> Dict[str, Any]:
        """
        执行资产管理命令
        
        Args:
            command: 命令类型 (scan, search, validate, suggest, stats, report)
            **kwargs: 其他参数，根据命令类型不同
            
        Returns:
            Dict[str, Any]: 执行结果
        """
        try:
            if not SERVICE_AVAILABLE:
                return self.create_response(
                    success=False,
                    error="AssetService not available. Please ensure asset_service.py is in core/ directory."
                )
            
            # 根据命令类型调用相应方法
            if command == "scan":
                return self.scan_assets(**kwargs)
            elif command == "search":
                return self.search_assets(**kwargs)
            elif command == "validate":
                return self.validate_asset(**kwargs)
            elif command == "suggest":
                return self.suggest_reuse(**kwargs)
            elif command == "stats":
                return self.get_stats(**kwargs)
            elif command == "report":
                return self.generate_report(**kwargs)
            else:
                return self.create_response(
                    success=False,
                    error=f"Unknown command: {command}",
                    available_commands=["scan", "search", "validate", "suggest", "stats", "report"]
                )
                
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Asset tool execution failed: {str(e)}"
            )
    
    def scan_assets(self, verbose: bool = False, **kwargs) -> Dict[str, Any]:
        """
        扫描技术资产库
        
        Args:
            verbose: 详细输出模式
            
        Returns:
            Dict[str, Any]: 扫描结果
        """
        try:
            asset_service = AssetService()
            result = asset_service.scan_assets(verbose=verbose)
            
            # 添加工具版本信息
            result["tool_version"] = self.version
            result["command"] = "scan"
            
            return result
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Asset scan failed: {str(e)}"
            )
    
    def search_assets(self, query: str, asset_type: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        搜索资产
        
        Args:
            query: 搜索查询词
            asset_type: 资产类型过滤
            
        Returns:
            Dict[str, Any]: 搜索结果
        """
        try:
            asset_service = AssetService()
            result = asset_service.search(query=query, asset_type=asset_type)
            
            result["tool_version"] = self.version
            result["command"] = "search"
            
            return result
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Asset search failed: {str(e)}"
            )
    
    def validate_asset(self, file_path: str, content: str = "", **kwargs) -> Dict[str, Any]:
        """
        验证新资产
        
        Args:
            file_path: 资产文件路径
            content: 资产内容（如不指定则从文件读取）
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            asset_service = AssetService()
            
            # 如果没有提供内容，尝试从文件读取
            if not content:
                file_path_obj = Path(file_path)
                if not file_path_obj.exists():
                    return self.create_response(
                        success=False,
                        error=f"File not found: {file_path}"
                    )
                
                try:
                    content = file_path_obj.read_text(encoding='utf-8')
                except Exception as e:
                    return self.create_response(
                        success=False,
                        error=f"Failed to read file: {e}"
                    )
            
            result = asset_service.validate(asset_path=file_path, content=content)
            
            result["tool_version"] = self.version
            result["command"] = "validate"
            
            return result
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Asset validation failed: {str(e)}"
            )
    
    def suggest_reuse(self, project_path: str, **kwargs) -> Dict[str, Any]:
        """
        生成资产复用建议
        
        Args:
            project_path: 项目路径
            
        Returns:
            Dict[str, Any]: 复用建议
        """
        try:
            asset_service = AssetService()
            result = asset_service.suggest_reuse(project_path=project_path)
            
            result["tool_version"] = self.version
            result["command"] = "suggest"
            
            return result
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Reuse suggestion failed: {str(e)}"
            )
    
    def get_stats(self, **kwargs) -> Dict[str, Any]:
        """
        获取资产统计
        
        Returns:
            Dict[str, Any]: 统计结果
        """
        try:
            asset_service = AssetService()
            result = asset_service.generate_report(format="json")
            
            result["tool_version"] = self.version
            result["command"] = "stats"
            
            return result
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Asset statistics failed: {str(e)}"
            )
    
    def generate_report(self, format: str = "json", **kwargs) -> Dict[str, Any]:
        """
        生成资产报告
        
        Args:
            format: 报告格式（json/text）
            
        Returns:
            Dict[str, Any]: 报告结果
        """
        try:
            asset_service = AssetService()
            result = asset_service.generate_report(format=format)
            
            result["tool_version"] = self.version
            result["command"] = "report"
            result["format"] = format
            
            return result
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Report generation failed: {str(e)}"
            )
    
    def get_asset_info(self, asset_name: str, **kwargs) -> Dict[str, Any]:
        """
        获取特定资产信息
        
        Args:
            asset_name: 资产名称
            
        Returns:
            Dict[str, Any]: 资产信息
        """
        try:
            asset_service = AssetService()
            
            # 使用搜索功能查找资产
            result = asset_service.search(query=asset_name)
            
            if not result.get("success", False):
                return result
            
            # 查找匹配的资产
            assets = result.get("results", [])
            matching_assets = [asset for asset in assets if asset["name"] == asset_name]
            
            if not matching_assets:
                return {
                    "success": False,
                    "error": f"Asset not found: {asset_name}",
                    "similar_assets": [asset["name"] for asset in assets[:5]]
                }
            
            return {
                "success": True,
                "command": "info",
                "tool_version": self.version,
                "asset": matching_assets[0],
                "found_exact_match": len(matching_assets) > 0
            }
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Asset info retrieval failed: {str(e)}"
            )
    
    def check_constitutional_compliance(self, **kwargs) -> Dict[str, Any]:
        """
        检查资产库宪法合规性
        
        Returns:
            Dict[str, Any]: 合规性检查结果
        """
        try:
            asset_service = AssetService()
            result = asset_service.scan_assets()
            
            if not result.get("success", False):
                return result
            
            metrics = result.get("metrics", {})
            compliance_rate = metrics.get("constitutional_compliance", 0)
            
            compliance_status = {
                "constitutional_compliance": compliance_rate,
                "status": "excellent" if compliance_rate >= 0.9 else 
                          "good" if compliance_rate >= 0.7 else
                          "warning" if compliance_rate >= 0.5 else
                          "danger",
                "recommendations": []
            }
            
            if compliance_rate < 0.9:
                compliance_status["recommendations"].append(
                    "Add §101 (Single Source of Truth) and §102 (Entropy Reduction) references to assets"
                )
            
            if compliance_rate < 0.7:
                compliance_status["recommendations"].append(
                    "Perform asset audit and update missing constitutional references"
                )
            
            return {
                "success": True,
                "command": "compliance",
                "tool_version": self.version,
                "compliance": compliance_status,
                "metrics": metrics
            }
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Compliance check failed: {str(e)}"
            )


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CDD Asset Tool CLI")
    
    parser.add_argument("--scan", "-s", action="store_true", help="Scan asset library")
    parser.add_argument("--search", "-q", help="Search assets (query)")
    parser.add_argument("--type", "-t", help="Asset type filter (component, pattern, hook, etc.)")
    parser.add_argument("--validate", "-v", help="Validate asset file")
    parser.add_argument("--content", "-c", help="Asset content for validation")
    parser.add_argument("--suggest", help="Generate reuse suggestions for project path")
    parser.add_argument("--stats", action="store_true", help="Show asset statistics")
    parser.add_argument("--report", action="store_true", help="Generate asset report")
    parser.add_argument("--format", "-f", choices=["json", "text"], default="json", help="Report format")
    parser.add_argument("--info", "-i", help="Get asset information")
    parser.add_argument("--compliance", action="store_true", help="Check constitutional compliance")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    tool = CDDAssetTool()
    result = None
    
    # 根据参数执行相应命令
    if args.scan:
        result = tool.scan_assets(verbose=args.verbose)
    elif args.search:
        result = tool.search_assets(query=args.search, asset_type=args.type)
    elif args.validate:
        result = tool.validate_asset(file_path=args.validate, content=args.content or "")
    elif args.suggest:
        result = tool.suggest_reuse(project_path=args.suggest)
    elif args.stats:
        result = tool.get_stats()
    elif args.report:
        result = tool.generate_report(format=args.format)
    elif args.info:
        result = tool.get_asset_info(asset_name=args.info)
    elif args.compliance:
        result = tool.check_constitutional_compliance()
    else:
        parser.print_help()
        return 0
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.format == "json":
                json.dump(result, f, indent=2, ensure_ascii=False)
            else:
                f.write(_format_text_result(result, args))
        print(f"✅ Result saved to: {args.output}")
    else:
        if args.format == "json" or args.stats or args.report:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(_format_text_result(result, args))
    
    return 0 if result.get("success", False) else 1

def _format_text_result(result: Dict[str, Any], args) -> str:
    """格式化文本输出结果"""
    if not result.get("success", False):
        return f"❌ Error: {result.get('error', 'Unknown error')}"
    
    output_lines = []
    command = result.get("command", "unknown")
    
    if command == "scan":
        output_lines.append("📊 Asset Library Scan Results")
        output_lines.append(f"Library: {result.get('library_root', 'N/A')}")
        output_lines.append(f"Assets Found: {result.get('assets_found', 0)}")
        
        metrics = result.get("metrics", {})
        if metrics:
            output_lines.append("\n📈 Key Metrics:")
            output_lines.append(f"  • Constitutional Compliance: {metrics.get('constitutional_compliance', 0)*100:.1f}%")
            output_lines.append(f"  • Documentation Completeness: {metrics.get('documentation_completeness', 0)*100:.1f}%")
            output_lines.append(f"  • Type Coverage: {metrics.get('coverage', 0)*100:.1f}%")
        
        asset_types = result.get("asset_types", {})
        if asset_types:
            output_lines.append("\n📂 Asset Type Distribution:")
            for asset_type, count in sorted(asset_types.items()):
                output_lines.append(f"  • {asset_type}: {count}")
    
    elif command == "search":
        output_lines.append("🔍 Asset Search Results")
        output_lines.append(f"Query: {result.get('query', 'N/A')}")
        output_lines.append(f"Asset Type Filter: {result.get('asset_type', 'all')}")
        output_lines.append(f"Results Found: {result.get('results_found', 0)}")
        
        results = result.get("results", [])
        if results:
            output_lines.append("\n📄 Matching Assets:")
            for i, item in enumerate(results[:10], 1):
                output_lines.append(f"\n  {i}. {item.get('name', 'Unknown')}")
                output_lines.append(f"      Type: {item.get('asset_type', 'unknown')}")
                output_lines.append(f"      Path: {item.get('path', 'N/A')}")
                output_lines.append(f"      File Type: {item.get('file_type', 'N/A')}")
                
                refs = item.get("constitutional_refs", [])
                if refs:
                    output_lines.append(f"      Constitutional Refs: {', '.join(refs[:3])}")
                    if len(refs) > 3:
                        output_lines.append(f"                      ... +{len(refs)-3} more")
                
                output_lines.append(f"      Compliance: {'✅' if item.get('has_constitutional_compliance', False) else '❌'}")
                output_lines.append(f"      Theme: {'✅' if item.get('is_theme_compliant', True) else '❌'}")
            
            if len(results) > 10:
                output_lines.append(f"\n  ... and {len(results) - 10} more results")
    
    elif command == "validate":
        output_lines.append("✅ Asset Validation Results")
        
        validation = result.get("validation", {})
        if validation.get("valid", False):
            output_lines.append("Status: ✅ Valid")
        else:
            output_lines.append("Status: ❌ Invalid")
        
        errors = validation.get("errors", [])
        if errors:
            output_lines.append("\n❌ Errors:")
            for error in errors:
                output_lines.append(f"  - {error}")
        
        warnings = validation.get("warnings", [])
        if warnings:
            output_lines.append("\n⚠️ Warnings:")
            for warning in warnings:
                output_lines.append(f"  - {warning}")
        
        suggestions = validation.get("suggestions", [])
        if suggestions:
            output_lines.append("\n💡 Suggestions:")
            for suggestion in suggestions:
                output_lines.append(f"  - {suggestion}")
        
        if result.get("compliance_required", False):
            output_lines.append("\n📋 Constitutional Requirements:")
            output_lines.append("  • §101 Single Source of Truth reference")
            output_lines.append("  • §102 Entropy Reduction Principle reference")
        
        if result.get("theme_compliance_required", False):
            output_lines.append("  • §119 Theme-Driven Development reference")
            output_lines.append("  • No hardcoded color values")
    
    elif command == "suggest":
        output_lines.append("💡 Asset Reuse Suggestions")
        output_lines.append(f"Project: {result.get('project_path', 'N/A')}")
        output_lines.append(f"Assets Scanned: {result.get('assets_scanned', 0)}")
        output_lines.append(f"Suggestions Generated: {result.get('suggestions_found', 0)}")
        
        suggestions = result.get("suggestions", [])
        if suggestions:
            output_lines.append("\n📋 Suggestions:")
            for i, suggestion in enumerate(suggestions[:5], 1):
                output_lines.append(f"\n  {i}. {suggestion.get('asset', 'Unknown')}")
                output_lines.append(f"      Type: {suggestion.get('type', 'unknown')}")
                output_lines.append(f"      Path: {suggestion.get('path', 'N/A')}")
                output_lines.append(f"      Reason: {suggestion.get('reason', '')}")
                output_lines.append(f"      Suggestion: {suggestion.get('suggestion', '')}")
            
            if len(suggestions) > 5:
                output_lines.append(f"\n  ... and {len(suggestions) - 5} more suggestions")
    
    elif command in ["stats", "report"]:
        # 对于统计和报告，使用JSON输出更好
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    elif command == "compliance":
        output_lines.append("⚖️ Constitutional Compliance Check")
        
        compliance = result.get("compliance", {})
        compliance_rate = compliance.get("constitutional_compliance", 0)
        status = compliance.get("status", "unknown")
        
        status_emoji = {
            "excellent": "🟢",
            "good": "🟡",
            "warning": "🟠",
            "danger": "🔴"
        }
        
        output_lines.append(f"Compliance Rate: {compliance_rate*100:.1f}% {status_emoji.get(status, '')}")
        output_lines.append(f"Status: {status.upper()}")
        
        recommendations = compliance.get("recommendations", [])
        if recommendations:
            output_lines.append("\n📋 Recommendations:")
            for rec in recommendations:
                output_lines.append(f"  • {rec}")
    
    output_lines.append(f"\n🔧 Tool Version: {result.get('tool_version', 'N/A')}")
    return "\n".join(output_lines)

if __name__ == "__main__":
    sys.exit(main())