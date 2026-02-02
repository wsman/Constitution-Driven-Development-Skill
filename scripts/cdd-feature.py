#!/usr/bin/env python3
"""
CDD Feature Scaffolding Tool v1.5.0

Usage:
    python scripts/cdd-feature.py "Feature Description"
    python scripts/cdd-feature.py "Add User Login" --dry-run

Features:
- Auto-numbering: Scans specs/ directory for next ID
- Git integration: Creates feature branch
- Template instantiation: Generates DS-050/051/052 from templates
- Error handling: Environment checks, graceful failures
"""

import os
import sys
import re
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration Constants
TEMPLATES_DIR = Path("templates/standards")
SPECS_DIR = Path("specs")
REQUIRED_TEMPLATES = [
    "DS-050_feature_specification.md",
    "DS-051_implementation_plan.md",
    "DS-052_atomic_tasks.md"
]

def check_environment():
    """Environment self-check before execution"""
    if not TEMPLATES_DIR.exists():
        print(f"❌ Error: Templates directory not found at {TEMPLATES_DIR}")
        print("   Please run this script from the project root.")
        sys.exit(1)
        
    for tmpl in REQUIRED_TEMPLATES:
        if not (TEMPLATES_DIR / tmpl).exists():
            print(f"❌ Error: Missing required template: {tmpl}")
            sys.exit(1)

def get_next_feature_id():
    """Scan specs directory to get next feature ID"""
    if not SPECS_DIR.exists():
        return "001"
    
    max_id = 0
    for item in SPECS_DIR.iterdir():
        if item.is_dir():
            match = re.match(r"^(\d{3})-", item.name)
            if match:
                try:
                    current_id = int(match.group(1))
                    if current_id > max_id:
                        max_id = current_id
                except ValueError:
                    continue
    
    return f"{max_id + 1:03d}"

def sanitize_name(name):
    """Convert description to kebab-case"""
    name = name.lower()
    # Replace underscores and spaces with hyphens
    name = re.sub(r'[_\s]+', '-', name)
    # Remove any characters that are not alphanumeric, hyphens, or Chinese characters
    name = re.sub(r'[^a-z0-9\-\u4e00-\u9fa5]', '', name)
    # Remove leading/trailing hyphens
    name = re.sub(r'^-+|-+$', '', name)
    return name

def create_branch(branch_name):
    """Create and checkout Git branch"""
    try:
        # Check git status
        subprocess.run(["git", "status"], check=True, capture_output=True)
        
        # Check if branch exists
        result = subprocess.run(["git", "branch", "--list", branch_name], 
                               capture_output=True, text=True)
        if branch_name in result.stdout:
            print(f"⚠️  Branch '{branch_name}' already exists. Switching to it.")
            subprocess.run(["git", "checkout", branch_name], check=True)
        else:
            print(f"🌿 Creating branch: {branch_name}")
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Git error or not a git repository. Skipping branch creation.")
        return False
    except FileNotFoundError:
        print("⚠️  Git not installed. Skipping branch creation.")
        return False

def instantiate_templates(target_dir, feature_id, feature_name):
    """Copy and fill templates"""
    target_dir.mkdir(parents=True, exist_ok=True)
    
    templates_map = {
        "DS-050_feature_specification.md": f"DS-050_{feature_id}_spec.md",
        "DS-051_implementation_plan.md": f"DS-051_{feature_id}_plan.md",
        "DS-052_atomic_tasks.md": f"DS-052_{feature_id}_tasks.md"
    }
    
    print(f"📄 Generating artifacts in {target_dir}/...")
    
    for tmpl_name, dest_name in templates_map.items():
        src = TEMPLATES_DIR / tmpl_name
        dest = target_dir / dest_name
        
        if dest.exists():
            print(f"   ⚠️  Skipping {dest_name} (already exists)")
            continue
            
        try:
            content = src.read_text(encoding='utf-8')
            
            # Template replacement
            content = content.replace("{{FEATURE_ID}}", feature_id)
            content = content.replace("{{FEATURE_NAME}}", feature_name)
            content = content.replace("{{TIMESTAMP}}", datetime.now().isoformat())
            
            dest.write_text(content, encoding='utf-8')
            print(f"   ✅ Created {dest_name}")
        except Exception as e:
            print(f"   ❌ Failed to create {dest_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="CDD Feature Scaffolding Tool (v1.5.0)")
    parser.add_argument("description", help="Feature description (e.g., 'Add User Login')")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without creating files")
    args = parser.parse_args()
    
    # 0. Environment check
    if not args.dry_run:
        check_environment()
    
    # 1. Calculate ID and name
    feature_id = get_next_feature_id()
    short_name = sanitize_name(args.description)
    full_name = f"{feature_id}-{short_name}"
    
    print(f"🚀 Initializing Feature: {full_name}")
    if args.dry_run:
        print("[Dry Run] Would create branch and files. Exiting.")
        return
    
    # 2. Create branch
    create_branch(full_name)
    
    # 3. Generate documents
    feature_dir = SPECS_DIR / full_name
    instantiate_templates(feature_dir, feature_id, args.description)
    
    print(f"\n✨ Feature scaffolding complete!")
    print(f"   Work directory: {feature_dir}")
    print(f"   Next step: Run 'cdd clarify' or edit DS-050.")

if __name__ == "__main__":
    main()
