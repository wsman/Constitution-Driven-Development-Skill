"""
CDD Feature Service (feature_service.py) v2.0.0
================================================
特性服务的核心业务逻辑，整合自scripts/cdd_feature.py和claude_tools/cdd_feature_tool.py。

宪法依据: §101§102§200§309
"""

import re
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from core.constants import SKILL_ROOT, VERSION, DEFAULT_ENCODING
from core.exceptions import SporeIsolationViolation, ToolExecutionError
from utils.spore_utils import check_spore_isolation
from utils.file_utils import run_command


class TemplateEngine:
    """模板引擎"""
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
    
    def load_template(self, template_path: str) -> str:
        """加载模板文件
        
        Args:
            template_path: 模板路径，可以是相对路径或绝对路径
            
        Returns:
            模板内容字符串，如果模板不存在则返回占位符内容
            
        查找顺序:
        1. 在templates_dir目录中查找
        2. 在SKILL_ROOT中查找原始路径
        """
        # 处理路径：移除可能的前缀
        path_str = template_path
        
        # 如果路径以 templates/ 开头，移除它（因为 templates_dir 已经是 templates 目录）
        if path_str.startswith("templates/"):
            path_str = path_str[len("templates/"):]
        
        # 首先在templates_dir中查找
        full_path = self.templates_dir / path_str
        
        # 如果在templates_dir中没找到，尝试在SKILL_ROOT中查找原始路径
        if not full_path.exists():
            original_path = SKILL_ROOT / template_path
            if original_path.exists():
                full_path = original_path
        
        if not full_path.exists():
            # 返回更详细的错误信息，帮助调试模板路径问题
            error_msg = (
                f"# Template: {{{{ feature_name }}}}\n\n"
                f"> ⚠️ 模板未找到: {template_path}\n\n"
                f"**调试信息**:\n"
                f"- 查找的路径: {full_path}\n"
                f"- 模板目录: {self.templates_dir}\n"
                f"- 原始路径: {SKILL_ROOT / template_path if template_path else 'N/A'}\n\n"
                f"**可能的解决方案**:\n"
                f"1. 确保模板文件存在于 `templates/` 目录中\n"
                f"2. 检查模板路径是否正确\n"
                f"3. 验证CDD技能库完整性: `python scripts/cdd_verify.py`\n"
            )
            return error_msg
        
        return full_path.read_text(encoding=DEFAULT_ENCODING)
    
    def render(self, content: str, context: Dict[str, Any]) -> str:
        """渲染模板"""
        result = content
        for key, value in context.items():
            pattern = r"\{\{\s*" + re.escape(key) + r"\s*\}\}"
            result = re.sub(pattern, str(value), result)
        return result


class ContextBuilder:
    """上下文构建器"""
    
    def __init__(self, target_root: Path):
        self.target_root = target_root
    
    def build_feature_context(self, feature_id: str, feature_name: str, 
                               description: str) -> Dict[str, Any]:
        """构建特性上下文"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        # 获取Git信息
        git_info = self._get_git_info()
        
        context = {
            "FEATURE_ID": feature_id,
            "FEATURE_NAME": feature_name,
            "TIMESTAMP": timestamp,
            "feature_id": feature_id,
            "feature_name": feature_name,
            "feature_description": description,
            "timestamp": timestamp,
            "project_name": self.target_root.name,
            **git_info
        }
        
        return context
    
    def build_deploy_context(self, project_name: str) -> Dict[str, Any]:
        """构建部署上下文"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        return {
            "PROJECT_NAME": project_name,
            "TIMESTAMP": timestamp,
            "project_name": project_name,
            "timestamp": timestamp
        }
    
    def _get_git_info(self) -> Dict[str, str]:
        """获取Git信息"""
        try:
            author = subprocess.check_output(
                ["git", "config", "user.name"],
                cwd=self.target_root,
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
        except:
            author = "Unknown Developer"
        
        try:
            branch = subprocess.check_output(
                ["git", "branch", "--show-current"],
                cwd=self.target_root,
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
        except:
            branch = "main"
        
        return {"author": author, "git_branch": branch}


class FeatureCreator:
    """特性创建器"""
    
    def __init__(self, target_root: Path):
        self.target_root = target_root
        self.specs_dir = target_root / "specs"
        self.template_engine = TemplateEngine(SKILL_ROOT / "templates")
        self.context_builder = ContextBuilder(target_root)
        
        # 模板映射 (路径相对于SKILL_ROOT)
        self.feature_templates = {
            "templates/t2_standards/DS-050_feature_specification.md": "_spec.md",
            "templates/t2_standards/DS-051_implementation_plan.md": "_plan.md",
            "templates/t2_standards/DS-052_atomic_tasks.md": "_tasks.md",
            "templates/t3_documentation/05_readme_templates.md": "_README.md",
        }
    
    def create_feature(self, name: str, description: str, 
                       create_branch: bool = True) -> Dict[str, Any]:
        """创建新特性"""
        
        # 准备目录
        if not self.specs_dir.exists():
            self.specs_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成特性ID和名称
        clean_name = self._sanitize_name(name)
        feature_id = self._get_next_feature_id()
        full_feature_name = f"{feature_id}-{clean_name}"
        feature_dir = self.specs_dir / full_feature_name
        
        # 检查目录是否存在
        if feature_dir.exists():
            return {
                "success": False,
                "error": f"Feature directory already exists: {feature_dir}"
            }
        
        # 创建特性目录
        feature_dir.mkdir()
        
        # 构建上下文
        context = self.context_builder.build_feature_context(
            feature_id, clean_name, description
        )
        
        # 生成文件
        generated_files = []
        for template_path, suffix in self.feature_templates.items():
            try:
                template_content = self.template_engine.load_template(template_path)
                rendered_content = self.template_engine.render(template_content, context)
                
                prefix = template_path.split('/')[-1].split('_')[0]
                output_filename = f"{prefix}_{feature_id}{suffix}"
                output_path = feature_dir / output_filename
                
                output_path.write_text(rendered_content, encoding=DEFAULT_ENCODING)
                generated_files.append(str(output_path.relative_to(self.target_root)))
            except Exception as e:
                # 记录错误但继续
                pass
        
        # 创建Git分支
        if create_branch:
            self._create_git_branch(full_feature_name)
        
        return {
            "success": True,
            "feature_id": feature_id,
            "feature_name": full_feature_name,
            "feature_dir": str(feature_dir),
            "generated_files": generated_files
        }
    
    def _sanitize_name(self, name: str) -> str:
        """清理特性名称"""
        s = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]+', '-', name)
        s = s.strip('-').lower()
        return s
    
    def _get_next_feature_id(self) -> str:
        """获取下一个特性ID"""
        if not self.specs_dir.exists():
            return "001"
        
        max_id = 0
        for item in self.specs_dir.iterdir():
            if item.is_dir():
                match = re.match(r'^(\d{3})-', item.name)
                if match:
                    try:
                        current_id = int(match.group(1))
                        if current_id > max_id:
                            max_id = current_id
                    except ValueError:
                        continue
        
        return f"{max_id + 1:03d}"
    
    def _create_git_branch(self, branch_name: str):
        """创建Git分支"""
        try:
            subprocess.run(
                ["git", "rev-parse", "--verify", branch_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=self.target_root,
                check=True
            )
            subprocess.run(["git", "checkout", branch_name], cwd=self.target_root, check=True)
        except subprocess.CalledProcessError:
            try:
                subprocess.run(["git", "checkout", "-b", branch_name], cwd=self.target_root, check=True)
            except subprocess.CalledProcessError as e:
                # 分支创建失败，但特性创建仍然成功
                pass


class ProjectDeployer:
    """项目部署器"""
    
    def __init__(self, target_root: Path):
        self.target_root = target_root
        self.memory_bank = target_root / "memory_bank"
        self.template_engine = TemplateEngine(SKILL_ROOT / "templates")
        self.context_builder = ContextBuilder(target_root)
        
        # 部署模板组
        self.deploy_templates = {
            "core": {
                "templates/t0_core/active_context.md": "t0_core/active_context.md",
                "templates/t0_core/knowledge_graph.md": "t0_core/knowledge_graph.md",
                "templates/t0_core/basic_law_index.md": "t0_core/basic_law_index.md",
                "templates/t0_core/operational_law_index.md": "t0_core/operational_law_index.md",
                "templates/t0_core/tools_law_index.md": "t0_core/tools_law_index.md",
            },
            "axioms": {
                "templates/t1_axioms/behavior_context.md": "t1_axioms/behavior_context.md",
                "templates/t1_axioms/system_patterns.md": "t1_axioms/system_patterns.md",
                "templates/t1_axioms/tech_context.md": "t1_axioms/tech_context.md",
            },
            "protocols": {
                "templates/t2_protocols/WF-001_clarify_workflow.md": "t2_protocols/WF-001_clarify_workflow.md",
                "templates/t2_protocols/WF-201_cdd_workflow.md": "t2_protocols/WF-201_cdd_workflow.md",
            },
            "standards": {
                "templates/t2_standards/DS-050_feature_specification.md": "t2_standards/DS-050_feature_specification.md",
                "templates/t2_standards/DS-053_quality_checklist.md": "t2_standards/DS-053_quality_checklist.md",
            }
        }
    
    def deploy(self, project_name: str, force: bool = False) -> Dict[str, Any]:
        """部署CDD Memory Bank结构"""
        
        # 创建目录结构
        self._create_directory_structure()
        
        # 构建上下文
        context = self.context_builder.build_deploy_context(project_name)
        
        # 部署模板
        deployed_files = []
        for group_name, templates in self.deploy_templates.items():
            for src_rel, dst_rel in templates.items():
                try:
                    result = self._deploy_template(src_rel, dst_rel, context, force)
                    if result:
                        deployed_files.append(result)
                except Exception as e:
                    # 记录错误但继续
                    pass
        
        # 创建标准目录
        self._create_standard_directories()
        
        # 复制配置文件
        self._copy_config_files()
        
        return {
            "success": True,
            "project_name": project_name,
            "target_dir": str(self.target_root),
            "memory_bank": str(self.memory_bank),
            "deployed_files": deployed_files
        }
    
    def _create_directory_structure(self):
        """创建Memory Bank目录结构"""
        subdirs = ["t0_core", "t1_axioms", "t2_protocols", "t2_standards", "t3_documentation"]
        for subdir in subdirs:
            (self.memory_bank / subdir).mkdir(parents=True, exist_ok=True)
    
    def _deploy_template(self, src_rel: str, dst_rel: str, 
                         context: Dict[str, Any], force: bool) -> Optional[str]:
        """部署单个模板"""
        src = SKILL_ROOT / src_rel
        dst = self.memory_bank / dst_rel
        
        if not src.exists():
            return None
        
        if dst.exists() and not force:
            return None
        
        content = src.read_text(encoding=DEFAULT_ENCODING)
        content = self.template_engine.render(content, context)
        
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(content, encoding=DEFAULT_ENCODING)
        
        return str(dst.relative_to(self.target_root))
    
    def _create_standard_directories(self):
        """创建标准项目目录"""
        for d in ["src", "tests", "specs"]:
            (self.target_root / d).mkdir(exist_ok=True)
    
    def _copy_config_files(self):
        """复制配置文件"""
        config_files = {
            "templates/cdd_config.yaml": "cdd_config.yaml",
            "Makefile": "Makefile",
            "pytest.ini": "pytest.ini"
        }
        
        for src_name, dst_name in config_files.items():
            src = SKILL_ROOT / src_name
            dst = self.target_root / dst_name
            
            if src.exists() and not dst.exists():
                if src.is_dir():
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
                else:
                    shutil.copy2(src, dst)


class FeatureService:
    """特性服务主类"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or SKILL_ROOT
    
    def create_feature(self, name: str, description: str = "", 
                       target: str = ".", create_branch: bool = True) -> Dict[str, Any]:
        """
        创建新特性
        
        Args:
            name: 特性名称
            description: 特性描述
            target: 目标目录
            create_branch: 是否创建Git分支
            
        Returns:
            Dict[str, Any]: 创建结果
        """
        target_root = Path(target).resolve()
        
        # 孢子隔离检查
        passed, message = check_spore_isolation(target_root, "create_feature")
        if not passed:
            return {
                "success": False,
                "error": f"Spore isolation violation: {message}"
            }
        
        creator = FeatureCreator(target_root)
        return creator.create_feature(
            name=name,
            description=description,
            create_branch=create_branch
        )
    
    def deploy_project(self, project_name: str, target: str = ".", 
                       force: bool = False) -> Dict[str, Any]:
        """
        部署CDD结构到项目
        
        Args:
            project_name: 项目名称
            target: 目标目录
            force: 是否覆盖现有文件
            
        Returns:
            Dict[str, Any]: 部署结果
        """
        target_root = Path(target).resolve()
        
        # 孢子隔离检查
        passed, message = check_spore_isolation(target_root, "deploy_project")
        if not passed:
            return {
                "success": False,
                "error": f"Spore isolation violation: {message}"
            }
        
        deployer = ProjectDeployer(target_root)
        return deployer.deploy(project_name, force=force)
    
    def list_features(self, target: str = ".") -> Dict[str, Any]:
        """列出所有特性"""
        target_root = Path(target).resolve()
        specs_dir = target_root / "specs"
        
        if not specs_dir.exists():
            return {
                "success": True,
                "target": str(target_root),
                "features": [],
                "count": 0,
                "specs_dir": str(specs_dir)
            }
        
        features = []
        for item in specs_dir.iterdir():
            if item.is_dir():
                feature_info = {
                    "name": item.name,
                    "path": str(item.relative_to(target_root)),
                    "files": []
                }
                
                # 统计文件
                for file_item in item.iterdir():
                    if file_item.is_file():
                        feature_info["files"].append({
                            "name": file_item.name,
                            "size": file_item.stat().st_size
                        })
                
                features.append(feature_info)
        
        return {
            "success": True,
            "target": str(target_root),
            "features": features,
            "count": len(features),
            "specs_dir": str(specs_dir)
        }
    
    def validate_feature_name(self, name: str) -> Dict[str, Any]:
        """验证特性名称"""
        # 检查长度
        if len(name) < 2:
            return {
                "valid": False,
                "reason": "Feature name too short (minimum 2 characters)"
            }
        
        if len(name) > 100:
            return {
                "valid": False,
                "reason": "Feature name too long (maximum 100 characters)"
            }
        
        # 检查特殊字符
        if re.search(r'[<>:"/\\|?*]', name):
            return {
                "valid": False,
                "reason": "Feature name contains invalid characters"
            }
        
        # 检查是否以数字开头
        if name[0].isdigit():
            return {
                "valid": False,
                "reason": "Feature name should not start with a digit"
            }
        
        # 检查是否包含空格
        if ' ' in name:
            return {
                "valid": True,
                "warning": "Feature name contains spaces, will be converted to hyphens"
            }
        
        return {
            "valid": True,
            "reason": "Feature name is valid"
        }