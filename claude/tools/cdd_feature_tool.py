#!/usr/bin/env python3
"""
CDD Feature Tool (cdd_feature_tool.py) v2.0.0
=============================================
Claude Code特性管理工具API层，调用services/feature_service.py。

宪法依据: §101§102§309
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from .tool_registry import BaseTool, cdd_tool

# 导入新的服务层
try:
    from core.feature_service import FeatureService
    SERVICE_AVAILABLE = True
except ImportError:
    SERVICE_AVAILABLE = False
    FeatureService = None


@cdd_tool(name="cdd_feature", description="CDD特性脚手架工具")
class CDDFeatureTool(BaseTool):
    """CDD特性创建工具API层"""
    
    name = "cdd_feature"
    description = "创建CDD特性规格脚手架"
    version = "2.0.0"
    constitutional_basis = ["§101", "§102", "§309"]
    
    def execute(self, name: str, description: str = "", target: str = ".", 
                create_branch: bool = True, dry_run: bool = False, **kwargs) -> Dict[str, Any]:
        """
        创建新特性
        
        Args:
            name: 特性名称
            description: 特性描述
            target: 目标项目路径（默认为当前目录）
            create_branch: 是否创建Git分支
            dry_run: 模拟运行，不实际创建文件
            
        Returns:
            Dict[str, Any]: 创建结果
        """
        try:
            if not SERVICE_AVAILABLE:
                return self.create_response(
                    success=False,
                    error="FeatureService not available. Please check services/ directory."
                )
            
            if dry_run:
                return {
                    "success": True,
                    "dry_run": True,
                    "simulation": f"Would create feature '{name}' in {target}",
                    "target": target,
                    "operation": "create"
                }
            
            # 创建特性服务实例
            feature_service = FeatureService()
            
            # 执行特性创建
            result = feature_service.create_feature(
                name=name,
                description=description,
                target=target,
                create_branch=create_branch
            )
            
            # 添加工具版本信息
            result["tool_version"] = self.version
            
            return result
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Feature creation failed: {str(e)}"
            )
    
    def list_features(self, target: str = ".") -> Dict[str, Any]:
        """
        列出所有特性
        
        Args:
            target: 目标项目路径
            
        Returns:
            Dict[str, Any]: 特性列表
        """
        try:
            if not SERVICE_AVAILABLE:
                return {
                    "success": False,
                    "error": "FeatureService not available. Please check services/ directory."
                }
            
            feature_service = FeatureService()
            return feature_service.list_features(target=target)
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Failed to list features: {str(e)}"
            )
    
    def get_feature_info(self, feature_id: str, target: str = ".") -> Dict[str, Any]:
        """
        获取特性详细信息
        
        Args:
            feature_id: 特性ID（如001-login）
            target: 目标项目路径
            
        Returns:
            Dict[str, Any]: 特性信息
        """
        try:
            path = Path(target).resolve()
            specs_dir = path / "specs"
            
            if not specs_dir.exists():
                return {
                    "success": False,
                    "error": f"Specs directory not found: {specs_dir}"
                }
            
            # 查找特性目录
            feature_dir = None
            for item in specs_dir.iterdir():
                if item.is_dir() and item.name.startswith(feature_id):
                    feature_dir = item
                    break
            
            if not feature_dir:
                return {
                    "success": False,
                    "error": f"Feature not found: {feature_id}",
                    "available_features": [d.name for d in specs_dir.iterdir() if d.is_dir()]
                }
            
            # 收集特性信息
            feature_info = {
                "name": feature_dir.name,
                "path": str(feature_dir.relative_to(path)),
                "full_path": str(feature_dir),
                "files": [],
                "specifications": []
            }
            
            for file_item in feature_dir.iterdir():
                if file_item.is_file():
                    file_info = {
                        "name": file_item.name,
                        "size": file_item.stat().st_size,
                        "modified": file_item.stat().st_mtime
                    }
                    feature_info["files"].append(file_info)
                    
                    # 检查是否为规范文件
                    if file_item.suffix == ".md" and "spec" in file_item.name.lower():
                        feature_info["specifications"].append(file_item.name)
            
            return {
                "success": True,
                "feature": feature_info
            }
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Failed to get feature info: {str(e)}"
            )
    
    def validate_feature_name(self, name: str) -> Dict[str, Any]:
        """
        验证特性名称
        
        Args:
            name: 特性名称
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            if not SERVICE_AVAILABLE:
                return {
                    "valid": False,
                    "reason": "FeatureService not available"
                }
            
            feature_service = FeatureService()
            return feature_service.validate_feature_name(name)
            
        except Exception as e:
            return {
                "valid": False,
                "reason": f"Validation failed: {str(e)}"
            }


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CDD Feature Tool CLI")
    
    parser.add_argument("--name", "-n", help="Feature name")
    parser.add_argument("--description", "-d", default="", help="Feature description")
    parser.add_argument("--target", "-t", default=".", help="Target project path")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--list", "-l", action="store_true", help="List all features")
    parser.add_argument("--info", "-i", help="Get feature info (feature ID)")
    parser.add_argument("--validate", action="store_true", help="Validate feature name")
    parser.add_argument("--create-branch", action="store_true", default=True, help="Create Git branch")
    parser.add_argument("--no-branch", action="store_false", dest="create_branch", help="Skip Git branch")
    parser.add_argument("--deploy", metavar="PROJECT_NAME", help="Deploy CDD structure to project")
    parser.add_argument("--force", action="store_true", help="Force overwrite when deploying")
    
    args = parser.parse_args()
    
    tool = CDDFeatureTool()
    
    if args.deploy:
        if not SERVICE_AVAILABLE:
            print("❌ Error: FeatureService not available")
            return 1
        
        feature_service = FeatureService()
        result = feature_service.deploy_project(
            project_name=args.deploy,
            target=args.target,
            force=args.force
        )
        output_format = "json"
    
    elif args.list:
        result = tool.list_features(target=args.target)
        output_format = "text"
    elif args.info:
        result = tool.get_feature_info(args.info, target=args.target)
        output_format = "text"
    elif args.validate:
        if not args.name:
            print("❌ Error: Feature name required for validation")
            return 1
        result = tool.validate_feature_name(args.name)
        output_format = "text"
    elif args.name:
        result = tool.execute(
            name=args.name,
            description=args.description,
            target=args.target,
            create_branch=args.create_branch,
            dry_run=args.dry_run
        )
        output_format = "json"
    else:
        parser.print_help()
        return 0
    
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
    
    if hasattr(args, 'deploy') and args.deploy:
        print(f"✅ CDD Structure Deployed")
        print(f"Project: {result.get('project_name', 'N/A')}")
        print(f"Target: {result.get('target_dir', 'N/A')}")
        print(f"Memory Bank: {result.get('memory_bank', 'N/A')}")
        if result.get('deployed_files'):
            print(f"Files Deployed: {len(result.get('deployed_files', []))}")
    
    elif args.list:
        features = result.get("features", [])
        if not features:
            print("📁 No features found")
            print(f"Specs directory: {result.get('specs_dir', 'N/A')}")
        else:
            print(f"📁 Found {result.get('count', 0)} features")
            for i, feature in enumerate(features, 1):
                print(f"\n  {i}. {feature.get('name', 'Unknown')}")
                print(f"     Path: {feature.get('path', 'N/A')}")
                print(f"     Files: {len(feature.get('files', []))}")
    
    elif args.info:
        feature = result.get("feature", {})
        if feature:
            print(f"📋 Feature Information")
            print(f"Name: {feature.get('name', 'Unknown')}")
            print(f"Path: {feature.get('path', 'N/A')}")
            
            files = feature.get("files", [])
            if files:
                print(f"\n📄 Files ({len(files)}):")
                for f in files:
                    print(f"  - {f.get('name', 'Unknown')} ({f.get('size', 0)} bytes)")
            
            specs = feature.get("specifications", [])
            if specs:
                print(f"\n📝 Specifications:")
                for s in specs:
                    print(f"  - {s}")
    
    elif args.validate:
        if result.get("valid", False):
            print(f"✅ Feature name is valid")
            print(f"   Reason: {result.get('reason', 'N/A')}")
            if "warning" in result:
                print(f"   ⚠️ Warning: {result.get('warning', '')}")
        else:
            print(f"❌ Feature name is invalid")
            print(f"   Reason: {result.get('reason', 'Invalid')}")
    
    elif args.name:
        # 特性创建结果
        if result.get("dry_run", False):
            print("🔍 Dry Run Results:")
        else:
            print("✅ Feature Created:")
        
        print(f"Name: {result.get('feature_name', 'N/A')}")
        print(f"ID: {result.get('feature_id', 'N/A')}")
        print(f"Directory: {result.get('feature_dir', 'N/A')}")
        
        files = result.get("generated_files", [])
        if files:
            print(f"Files Generated ({len(files)}):")
            for f in files:
                print(f"  - {f}")

if __name__ == "__main__":
    sys.exit(main())