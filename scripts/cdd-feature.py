#!/usr/bin/env python3
"""
CDD Feature Scaffold (Legislative Generator) v2.0
=================================================
自动化生成符合 CDD 宪法标准的特性文档结构。

功能升级 (v2.0):
1. 基于文件的模板系统 (TemplateEngine)
2. 智能上下文注入 (ContextBuilder)
3. 动态版本提取
4. 标准化目录结构生成

Usage:
    python scripts/cdd-feature.py <feature_name> [description]
"""

import sys
import os
import re
import shutil
import argparse
import datetime
import subprocess
from pathlib import Path
from typing import Dict, Any, List

# -----------------------------------------------------------------------------
# Configuration & Constants
# -----------------------------------------------------------------------------

VERSION = "v2.0.0"
DEFAULT_ENCODING = "utf-8"

# 核心路径定义
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates" / "standards"
SPECS_DIR = PROJECT_ROOT / "specs"

# 关键版本源文件 (用于提取版本号)
VERSION_SOURCE_FILES = {
    "project": PROJECT_ROOT / "README.md",
    "active_context": PROJECT_ROOT / "templates" / "core" / "active_context.md",
    "system_patterns": PROJECT_ROOT / "templates" / "axioms" / "system_patterns.md",
}

# 默认模板映射 (文件名 -> 目标后缀)
TEMPLATE_MAPPING = {
    "DS-050_feature_specification.md": "_spec.md",
    "DS-051_implementation_plan.md": "_plan.md",
    "DS-052_atomic_tasks.md": "_tasks.md",
    "feature_readme_template.md": "_README.md",
    # 未来可扩展 DS-053, DS-054 等
}

# -----------------------------------------------------------------------------
# Core Classes
# -----------------------------------------------------------------------------

class TemplateEngine:
    """负责加载和渲染 Markdown 模板"""
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        if not self.templates_dir.exists():
            print(f"⚠️ Warning: Templates directory not found: {self.templates_dir}")

    def load_template(self, template_name: str) -> str:
        """从文件加载模板，如果文件不存在则返回内置的简易 Fallback"""
        template_path = self.templates_dir / template_name
        
        if template_path.exists():
            return template_path.read_text(encoding=DEFAULT_ENCODING)
        
        # Fallback: 如果找不到模板文件，返回一个最小化的默认内容
        print(f"⚠️ Template missing: {template_name}, using fallback.")
        return f"# Feature: {{{{ feature_name }}}}\n\n> Auto-generated fallback for {template_name}\n"

    def render(self, content: str, context: Dict[str, Any]) -> str:
        """执行简单的变量替换 {{ var }}"""
        result = content
        for key, value in context.items():
            pattern = r"\{\{\s*" + re.escape(key) + r"\s*\}\}"
            result = re.sub(pattern, str(value), result)
        return result

class ContextBuilder:
    """负责构建项目上下文元数据"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root

    def _extract_version(self, file_path: Path) -> str:
        """尝试从文件中提取 '版本: vX.Y.Z' 或类似模式"""
        if not file_path.exists():
            return "unknown"
        
        content = file_path.read_text(encoding=DEFAULT_ENCODING)
        # 匹配模式: "**版本**: v1.5.0" 或 "Version: 1.5.0" (允许v前缀)
        match = re.search(r"(?:版本|Version)[^:：]*[:：]\s*(?:v)?(\d+\.\d+\.\d+)", content, re.IGNORECASE)
        if match:
            return match.group(1)
        return "unknown"

    def _get_git_info(self) -> Dict[str, str]:
        """获取当前 Git 用户和分支信息"""
        try:
            author = subprocess.check_output(["git", "config", "user.name"], text=True).strip()
        except:
            author = "Unknown Developer"
            
        try:
            branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
        except:
            branch = "unknown-branch"
            
        return {"author": author, "git_branch": branch}

    def build(self, feature_id: str, feature_name: str, description: str) -> Dict[str, Any]:
        """构建完整的上下文合并字典"""
        
        # 1. 基础信息
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # 2. 版本提取
        versions = {
            "project_version": self._extract_version(VERSION_SOURCE_FILES["project"]),
            "active_context_version": self._extract_version(VERSION_SOURCE_FILES["active_context"]),
            "system_patterns_version": self._extract_version(VERSION_SOURCE_FILES["system_patterns"]),
        }
        
        # 3. Git 信息
        git_info = self._get_git_info()
        
        # 4. 组合上下文 (Snake Case Keys)
        context = {
            "FEATURE_ID": feature_id,          # 兼容旧模板
            "FEATURE_NAME": feature_name,      # 兼容旧模板
            "TIMESTAMP": timestamp,            # 兼容旧模板
            
            "feature_id": feature_id,
            "feature_name": feature_name,
            "feature_description": description,
            "timestamp": timestamp,
            "project_name": self.project_root.name,
            
            **versions,
            **git_info
        }
        
        return context

# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------

def sanitize_name(name: str) -> str:
    """Convert 'Add User Login' to 'add-user-login'"""
    # 替换非字母数字字符为横杠
    s = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]+', '-', name)
    s = s.strip('-').lower()
    return s

def get_next_feature_id(specs_dir: Path) -> str:
    """Scan specs dir to find next ID (e.g., '003')"""
    if not specs_dir.exists():
        return "001"
    
    max_id = 0
    for item in specs_dir.iterdir():
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

def create_git_branch(branch_name: str):
    """Create and switch to a new git branch"""
    try:
        # Check if branch exists
        subprocess.run(
            ["git", "rev-parse", "--verify", branch_name], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            check=True
        )
        print(f"ℹ️  Branch '{branch_name}' already exists. Switching to it...")
        subprocess.run(["git", "checkout", branch_name], check=True)
    except subprocess.CalledProcessError:
        # Branch does not exist, create it
        print(f"🌿 Creating new branch: {branch_name}")
        try:
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create branch: {e}")
            # Non-fatal, continue with file generation

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=f"CDD Feature Scaffold {VERSION}")
    parser.add_argument("name", help="Feature name (e.g. 'user-login')")
    parser.add_argument("description", nargs="?", default="No description provided", help="Feature description")
    parser.add_argument("--no-branch", action="store_true", help="Skip git branch creation")
    args = parser.parse_args()

    # 1. Prepare Paths & IDs
    if not SPECS_DIR.exists():
        SPECS_DIR.mkdir(parents=True)
        print(f"📁 Created specs directory: {SPECS_DIR}")

    clean_name = sanitize_name(args.name)
    feature_id = get_next_feature_id(SPECS_DIR)
    full_feature_name = f"{feature_id}-{clean_name}"
    feature_dir = SPECS_DIR / full_feature_name
    
    print(f"🚀 Initializing Feature: {full_feature_name}")
    print(f"   ID: {feature_id}")
    print(f"   Name: {clean_name}")

    # 2. Context Building
    print("🧠 Building context...")
    builder = ContextBuilder(PROJECT_ROOT)
    context = builder.build(feature_id, clean_name, args.description)
    
    # Debug: Print loaded versions
    print(f"   Project Version: {context.get('project_version')}")
    print(f"   Core Version:    {context.get('active_context_version')}")

    # 3. Create Directory
    if feature_dir.exists():
        print(f"⚠️  Directory already exists: {feature_dir}")
        response = input("   Overwrite? [y/N] ").lower()
        if response != 'y':
            print("❌ Aborted.")
            sys.exit(1)
    else:
        feature_dir.mkdir()
        print(f"📁 Created feature directory: {feature_dir}")

    # 4. Generate Files from Templates
    engine = TemplateEngine(TEMPLATES_DIR)
    
    for template_file, suffix in TEMPLATE_MAPPING.items():
        # Load
        tpl_content = engine.load_template(template_file)
        
        # Render
        rendered_content = engine.render(tpl_content, context)
        
        # Determine Output Filename
        # E.g., DS-050_003_spec.md
        prefix = template_file.split('_')[0] # "DS-050"
        output_filename = f"{prefix}_{feature_id}{suffix}"
        output_path = feature_dir / output_filename
        
        # Write
        output_path.write_text(rendered_content, encoding=DEFAULT_ENCODING)
        print(f"   📄 Generated: {output_filename}")

    # 5. Git Branching
    if not args.no_branch:
        create_git_branch(full_feature_name)

    print(f"\n✅ Feature scaffold ready at: specs/{full_feature_name}/")
    print("   Next Step: Fill in the specifications using CDD process.")

if __name__ == "__main__":
    main()