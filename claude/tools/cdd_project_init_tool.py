#!/usr/bin/env python3
"""
CDD Project Init Tool (cdd_project_init_tool.py) v2.0.0
=======================================================
Claude Code项目初始化工具，提供CDD Memory Bank部署功能。

宪法依据: §101§102§200§309
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from .tool_registry import BaseTool, cdd_tool

@cdd_tool(name="cdd_project_init", description="CDD项目初始化工具")
class CDDProjectInitTool(BaseTool):
    """CDD项目初始化工具"""
    
    name = "cdd_project_init"
    description = "部署CDD Memory Bank结构和配置"
    version = "2.0.0"
    constitutional_basis = ["§101", "§102", "§200", "§309"]
    
    def execute(self, project_name: str, target: str = ".", force: bool = False, 
                minimal: bool = False, **kwargs) -> Dict[str, Any]:
        """
        初始化CDD项目
        
        Args:
            project_name: 项目名称
            target: 目标项目路径（默认为当前目录）
            force: 是否覆盖现有文件
            minimal: 是否使用最小化部署（仅核心文件）
            
        Returns:
            Dict[str, Any]: 初始化结果
        """
        try:
            path = Path(target).resolve()
            
            # 孢子隔离检查
            isolation_check = self._check_spore_isolation(path)
            if not isolation_check["passed"]:
                return self.create_response(
                    success=False,
                    error=f"Spore isolation check failed: {isolation_check['reason']}"
                )
            
            # 导入CDD部署引擎
            from core.feature_service import deploy_project_claude
            
            # 执行项目部署
            deploy_result = deploy_project_claude(
                project_name=project_name,
                target=str(path),
                force=force
            )
            
            # 准备响应
            response = {
                "success": deploy_result.get("success", False),
                "project_name": deploy_result.get("project_name", ""),
                "target_dir": deploy_result.get("target_dir", ""),
                "memory_bank": deploy_result.get("memory_bank", ""),
                "deployed_files": deploy_result.get("deployed_files", []),
                "operation": "deploy"
            }
            
            # 添加最小化部署信息
            if minimal:
                response["deployment_mode"] = "minimal"
                response["files_deployed"] = len(response["deployed_files"])
            
            # 验证部署完整性
            response["deployment_validation"] = self._validate_deployment(path)
            
            return response
            
        except ImportError as e:
            return self.create_response(
                success=False,
                error=f"Failed to import deployment modules: {str(e)}",
                suggestion="Ensure cdd_feature.py is available in scripts directory"
            )
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Project initialization failed: {str(e)}"
            )
    
    def validate_project_structure(self, target: str = ".") -> Dict[str, Any]:
        """
        验证项目结构
        
        Args:
            target: 目标项目路径
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            path = Path(target).resolve()
            
            # 定义必需目录和文件
            required_dirs = [
                "memory_bank/t0_core",
                "memory_bank/t1_axioms",
                "memory_bank/t2_protocols",
                "memory_bank/t2_standards",
                "memory_bank/t3_documentation",
                "specs",
                "src",
                "tests"
            ]
            
            required_files = [
                "memory_bank/t0_core/active_context.md",
                "memory_bank/t1_axioms/system_patterns.md",
                "memory_bank/t2_standards/DS-050_feature_specification.md",
                "cdd_config.yaml",
                "Makefile",
                "pytest.ini"
            ]
            
            # 检查必需目录
            missing_dirs = []
            existing_dirs = []
            for d in required_dirs:
                dir_path = path / d
                if dir_path.exists():
                    existing_dirs.append(d)
                else:
                    missing_dirs.append(d)
            
            # 检查必需文件
            missing_files = []
            existing_files = []
            for f in required_files:
                file_path = path / f
                if file_path.exists():
                    existing_files.append(f)
                else:
                    missing_files.append(f)
            
            # 计算合规率
            dir_compliance = len(existing_dirs) / len(required_dirs) if required_dirs else 1.0
            file_compliance = len(existing_files) / len(required_files) if required_files else 1.0
            total_compliance = (dir_compliance + file_compliance) / 2.0
            
            return {
                "success": True,
                "target": str(path),
                "required_dirs": len(required_dirs),
                "existing_dirs": len(existing_dirs),
                "missing_dirs": missing_dirs,
                "required_files": len(required_files),
                "existing_files": len(existing_files),
                "missing_files": missing_files,
                "compliance_rate": total_compliance,
                "status": self._get_compliance_status(total_compliance)
            }
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Failed to validate project structure: {str(e)}"
            )
    
    def get_project_info(self, target: str = ".") -> Dict[str, Any]:
        """
        获取项目信息
        
        Args:
            target: 目标项目路径
            
        Returns:
            Dict[str, Any]: 项目信息
        """
        try:
            path = Path(target).resolve()
            
            # 检查是否为CDD项目
            cdd_config = path / "cdd_config.yaml"
            memory_bank = path / "memory_bank"
            
            is_cdd_project = cdd_config.exists() and memory_bank.exists()
            
            info = {
                "name": path.name,
                "path": str(path),
                "is_cdd_project": is_cdd_project,
                "has_memory_bank": memory_bank.exists(),
                "has_cdd_config": cdd_config.exists(),
                "directories": [],
                "features_count": 0,
                "entropy_level": "unknown"
            }
            
            # 统计目录
            if path.exists():
                for item in path.iterdir():
                    if item.is_dir():
                        info["directories"].append(item.name)
            
            # 统计特性
            specs_dir = path / "specs"
            if specs_dir.exists():
                feature_dirs = [d for d in specs_dir.iterdir() if d.is_dir()]
                info["features_count"] = len(feature_dirs)
            
            # 估算熵值水平
            if is_cdd_project:
                entropy_estimate = self._estimate_entropy_level(path)
                info["entropy_level"] = entropy_estimate
            
            return {
                "success": True,
                "project": info
            }
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Failed to get project info: {str(e)}"
            )
    
    def create_minimal_project(self, project_name: str, target: str = ".") -> Dict[str, Any]:
        """
        创建最小化CDD项目
        
        Args:
            project_name: 项目名称
            target: 目标项目路径
            
        Returns:
            Dict[str, Any]: 创建结果
        """
        try:
            path = Path(target).resolve()
            
            # 孢子隔离检查
            isolation_check = self._check_spore_isolation(path)
            if not isolation_check["passed"]:
                return self.create_response(
                    success=False,
                    error=f"Spore isolation check failed: {isolation_check['reason']}"
                )
            
            # 创建基础目录
            base_dirs = ["memory_bank/t0_core", "src", "tests", "specs"]
            for d in base_dirs:
                dir_path = path / d
                dir_path.mkdir(parents=True, exist_ok=True)
            
            # 创建核心文件
            core_files = {
                "memory_bank/t0_core/active_context.md": self._create_active_context(project_name),
                "cdd_config.yaml": self._create_minimal_config(project_name),
                "Makefile": self._create_minimal_makefile(),
                "README.md": self._create_readme(project_name)
            }
            
            deployed_files = []
            for file_path, content in core_files.items():
                full_path = path / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                deployed_files.append(file_path)
            
            return {
                "success": True,
                "project_name": project_name,
                "target_dir": str(path),
                "deployment_mode": "minimal",
                "deployed_files": deployed_files,
                "operation": "create_minimal"
            }
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Failed to create minimal project: {str(e)}"
            )
    
    def _check_spore_isolation(self, target_path: Path) -> Dict[str, Any]:
        """
        检查孢子隔离
        
        Args:
            target_path: 目标路径
            
        Returns:
            Dict[str, Any]: 检查结果
        """
        from cdd_utils import SKILL_ROOT
        
        try:
            # 检查是否是CDD技能库本身
            if target_path.resolve() == SKILL_ROOT:
                return {
                    "passed": False,
                    "reason": "Target is CDD skill root directory"
                }
            
            # 检查是否在CDD技能库内
            try:
                target_path.resolve().relative_to(SKILL_ROOT)
                return {
                    "passed": False,
                    "reason": "Target is inside CDD skill directory"
                }
            except ValueError:
                pass  # 不在技能库内，安全
            
            # 检查部署标志
            deployment_flag = target_path / ".cdd_deployment"
            if deployment_flag.exists():
                return {
                    "passed": True,
                    "reason": "Deployment mode detected",
                    "deployment_mode": True
                }
            
            return {
                "passed": True,
                "reason": "Spore isolation check passed"
            }
            
        except Exception as e:
            return {
                "passed": False,
                "reason": f"Spore isolation check error: {str(e)}"
            }
    
    def _validate_deployment(self, target_path: Path) -> Dict[str, Any]:
        """验证部署完整性"""
        validation = {
            "required_directories": [],
            "required_files": [],
            "passed": False
        }
        
        # 检查核心目录
        core_dirs = ["memory_bank/t0_core", "memory_bank/t1_axioms"]
        for d in core_dirs:
            dir_path = target_path / d
            status = "exists" if dir_path.exists() else "missing"
            validation["required_directories"].append({
                "path": d,
                "status": status
            })
        
        # 检查核心文件
        core_files = [
            "memory_bank/t0_core/active_context.md",
            "cdd_config.yaml"
        ]
        for f in core_files:
            file_path = target_path / f
            status = "exists" if file_path.exists() else "missing"
            validation["required_files"].append({
                "path": f,
                "status": status
            })
        
        # 判断是否通过
        all_items = validation["required_directories"] + validation["required_files"]
        passed_items = [i for i in all_items if i["status"] == "exists"]
        validation["passed"] = len(passed_items) >= len(all_items) * 0.8
        
        return validation
    
    def _estimate_entropy_level(self, project_path: Path) -> str:
        """估算熵值水平"""
        try:
            # 简化熵值估算
            required_items = [
                "memory_bank/t0_core/active_context.md",
                "memory_bank/t1_axioms/system_patterns.md",
                "memory_bank/t2_standards/DS-050_feature_specification.md",
                "src/",
                "tests/"
            ]
            
            existing_items = []
            for item in required_items:
                item_path = project_path / item
                if item_path.exists():
                    existing_items.append(item)
            
            compliance_rate = len(existing_items) / len(required_items)
            
            if compliance_rate >= 0.8:
                return "low"
            elif compliance_rate >= 0.5:
                return "medium"
            else:
                return "high"
                
        except Exception:
            return "unknown"
    
    def _get_compliance_status(self, compliance_rate: float) -> str:
        """获取合规状态"""
        if compliance_rate >= 0.9:
            return "🟢 优秀"
        elif compliance_rate >= 0.7:
            return "🟡 良好"
        elif compliance_rate >= 0.5:
            return "🟠 警告"
        else:
            return "🔴 危险"
    
    def _create_active_context(self, project_name: str) -> str:
        """创建active_context.md模板"""
        return f"""# Active Context - {project_name}

## 引导加载状态

| 维度 | 状态 | 上次更新 |
|------|------|----------|
| **工作流状态** | State A (Ingest) | {self._get_timestamp()} |
| **熵值状态** | H_sys = 0.0 (优秀) | {self._get_timestamp()} |
| **验证状态** | Tier 1/2/3 全部通过 | {self._get_timestamp()} |

## 项目概览
- **项目名称**: {project_name}
- **创建时间**: {self._get_timestamp()}
- **CDD版本**: 2.0.0
- **宪法依据**: §101, §102, §200, §309

## 最近宪法事件
1. 项目初始化完成 ({self._get_timestamp()})
"""

    def _create_minimal_config(self, project_name: str) -> str:
        """创建最小化配置"""
        return f"""# CDD Configuration
# 项目: {project_name}
# 创建时间: {self._get_timestamp()}

name: {project_name}
version: 1.0.0
type: cdd-project
constitutional_basis:
  - "§101: 单一真理源原则"
  - "§102: 熵减原则"
  - "§200: 孢子隔离原则"
  - "§309: 自动化任务原则"

memory_bank:
  t0_core:
    active_context: "memory_bank/t0_core/active_context.md"
    knowledge_graph: "memory_bank/t0_core/knowledge_graph.md"
  
  t1_axioms:
    system_patterns: "memory_bank/t1_axioms/system_patterns.md"
    tech_context: "memory_bank/t1_axioms/tech_context.md"
    behavior_context: "memory_bank/t1_axioms/behavior_context.md"

workflow:
  state: "A"
  enable_audit: true
  entropy_threshold: 0.7
"""

    def _create_minimal_makefile(self) -> str:
        """创建最小化Makefile"""
        return """# CDD Makefile

.PHONY: audit gate1 gate2 gate3 fix-versions clean

audit:
\tpython -m scripts.cdd_auditor --gate all

gate1:
\tpython -m scripts.cdd_auditor --gate 1

gate2:
\tpython -m scripts.cdd_auditor --gate 2

gate3:
\tpython -m scripts.cdd_auditor --gate 3

fix-versions:
\tpython -m scripts.cdd_auditor --gate 1 --fix

clean:
\tpython -m scripts.cdd_auditor --clean
"""

    def _create_readme(self, project_name: str) -> str:
        """创建README.md"""
        return f"""# {project_name}

基于CDD (Constitution-Driven Development) 开发的项目。

## 项目结构
```
{project_name}/
├── memory_bank/          # Memory Bank (T0-T3文档)
│   ├── t0_core/         # 核心层文档
│   ├── t1_axioms/       # 公理层文档
│   ├── t2_protocols/    # 工作流协议
│   ├── t2_standards/    # 实现标准
│   └── t3_documentation/ # 用户文档
├── src/                 # 源代码
├── tests/               # 测试代码
├── specs/               # 特性规格
├── cdd_config.yaml     # CDD配置
└── Makefile            # 构建命令
```

## 使用说明
1. **环境自检**: `make audit`
2. **创建特性**: `python scripts/cdd_feature.py create "特性名称"`
3. **测量熵值**: `python scripts/cdd_entropy.py calculate`

## 宪法依据
- §101: 单一真理源原则
- §102: 熵减原则
- §200: 孢子隔离原则
- §309: 自动化任务原则

---

**创建时间**: {self._get_timestamp()}
**CDD版本**: 2.0.0
"""

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CDD Project Init Tool CLI")
    
    parser.add_argument("--name", "-n", help="Project name")
    parser.add_argument("--target", "-t", default=".", help="Target directory")
    parser.add_argument("--force", "-f", action="store_true", help="Force overwrite")
    parser.add_argument("--minimal", "-m", action="store_true", help="Minimal deployment")
    parser.add_argument("--validate", action="store_true", help="Validate project structure")
    parser.add_argument("--info", action="store_true", help="Get project info")
    parser.add_argument("--create-minimal", action="store_true", help="Create minimal project")
    
    args = parser.parse_args()
    
    tool = CDDProjectInitTool()
    
    if args.validate:
        result = tool.validate_project_structure(target=args.target)
        output_format = "text"
    elif args.info:
        result = tool.get_project_info(target=args.target)
        output_format = "text"
    elif args.create_minimal:
        if not args.name:
            print("❌ Error: Project name required for minimal creation")
            return 1
        result = tool.create_minimal_project(project_name=args.name, target=args.target)
        output_format = "json"
    elif args.name:
        result = tool.execute(
            project_name=args.name,
            target=args.target,
            force=args.force,
            minimal=args.minimal
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
    
    if args.validate:
        print("📊 CDD 项目结构验证报告")
        print(f"目标路径: {result.get('target', 'N/A')}")
        print(f"合规率: {result.get('compliance_rate', 0):.2%}")
        print(f"状态: {result.get('status', 'N/A')}")
        
        missing_dirs = result.get("missing_dirs", [])
        if missing_dirs:
            print(f"\n📁 缺失目录 ({len(missing_dirs)}):")
            for d in missing_dirs:
                print(f"  - {d}")
        
        missing_files = result.get("missing_files", [])
        if missing_files:
            print(f"\n📄 缺失文件 ({len(missing_files)}):")
            for f in missing_files:
                print(f"  - {f}")
    
    elif args.info:
        project = result.get("project", {})
        if project:
            print("📋 项目信息")
            print(f"名称: {project.get('name', 'N/A')}")
            print(f"路径: {project.get('path', 'N/A')}")
            print(f"CDD项目: {'✅' if project.get('is_cdd_project', False) else '❌'}")
            print(f"Memory Bank: {'✅' if project.get('has_memory_bank', False) else '❌'}")
            print(f"CDD配置: {'✅' if project.get('has_cdd_config', False) else '❌'}")
            print(f"特性数量: {project.get('features_count', 0)}")
            print(f"熵值水平: {project.get('entropy_level', 'unknown')}")

if __name__ == "__main__":
    sys.exit(main())