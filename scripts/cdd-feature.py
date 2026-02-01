#!/usr/bin/env python3
"""
CDD Feature Scaffolding Tool v1.5.0

Usage:
    python scripts/cdd-feature.py "Feature Description"
    python scripts/cdd-feature.py "Add User Login" --short-name "user-login"

Features:
- Auto-numbering: Scans specs/ directory for next ID
- Git integration: Creates feature branch
- Template instantiation: Generates DS-050/051/052 from templates
"""

import os
import sys
import re
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
TEMPLATES_DIR = Path("/home/wsman/桌面/openclaw/skills/cdd/templates/standards")
SPECS_DIR = Path("/home/wsman/桌面/openclaw/skills/cdd/specs")

def get_next_feature_id():
    """Scan specs directory to get next feature ID"""
    if not SPECS_DIR.exists():
        return "001"
    
    max_id = 0
    for item in SPECS_DIR.iterdir():
        if item.is_dir():
            match = re.match(r"^(\d{3})-", item.name)
            if match:
                current_id = int(match.group(1))
                if current_id > max_id:
                    max_id = current_id
    
    return f"{max_id + 1:03d}"

def sanitize_name(name):
    """Convert description to kebab-case"""
    name = name.lower()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'\s+', '-', name)
    return name

def create_branch(branch_name):
    """Create and checkout Git branch"""
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                       check=True, capture_output=True)
        print(f"🌿 Creating branch: {branch_name}")
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Not a git repository. Skipping branch creation.")
        return False
    except FileNotFoundError:
        print("⚠️  Git not installed. Skipping branch creation.")
        return False

def instantiate_templates(target_dir, feature_id, feature_name):
    """Copy and fill templates"""
    target_dir.mkdir(parents=True, exist_ok=True)
    
    templates = {
        "DS-050_feature_specification.md": f"DS-050_{feature_id}_spec.md",
        "DS-051_implementation_plan.md": f"DS-051_{feature_id}_plan.md",
        "DS-052_atomic_tasks.md": f"DS-052_{feature_id}_tasks.md"
    }
    
    print(f"📄 Generating artifacts in {target_dir}/...")
    
    for tmpl_name, dest_name in templates.items():
        src = TEMPLATES_DIR / tmpl_name
        dest = target_dir / dest_name
        
        if not src.exists():
            print(f"   ❌ Template not found: {tmpl_name}")
            continue
            
        content = src.read_text(encoding='utf-8')
        
        # Template replacement
        content = content.replace("{{FEATURE_ID}}", feature_id)
        content = content.replace("{{FEATURE_NAME}}", feature_name)
        content = content.replace("{{TIMESTAMP}}", datetime.now().isoformat())
        
        dest.write_text(content, encoding='utf-8')
        print(f"   ✅ {dest_name}")

def main():
    parser = argparse.ArgumentParser(description="CDD Feature Scaffolding Tool v1.5.0")
    parser.add_argument("description", help="Feature description (e.g., 'Add User Login')")
    parser.add_argument("--short-name", "-s", help="Custom short name (e.g., 'user-login')")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Dry run (no changes)")
    
    args = parser.parse_args()
    
    # Calculate ID and name
    feature_id = get_next_feature_id()
    if args.short_name:
        short_name = sanitize_name(args.short_name)
    else:
        short_name = sanitize_name(args.description)
    full_name = f"{feature_id}-{short_name}"
    
    print(f"\n🚀 CDD Feature Scaffolding v1.5.0")
    print(f"   Feature: {full_name}")
    print(f"   Description: {args.description}\n")
    
    if args.dry_run:
        print("✅ Dry run complete (no changes made)")
        return
    
    # Create branch
    create_branch(full_name)
    
    # Generate documents
    feature_dir = SPECS_DIR / full_name
    instantiate_templates(feature_dir, feature_id, args.description)
    
    print(f"\n✅ Feature scaffolding complete!")
    print(f"   Directory: {feature_dir}")
    print(f"   Next step: Run 'cdd clarify' or start editing DS-050.\n")

if __name__ == "__main__":
    main()
