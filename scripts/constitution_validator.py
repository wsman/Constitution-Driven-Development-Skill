#!/usr/bin/env python3
"""
CDD Constitution Validator (宪法验证器)
=========================================
验证代码中的宪法引用是否与三级法律体系一致。
支持三级法律体系：基本法§1-§299，技术法§300-§499，程序法§500-§599

使用：python scripts/constitution_validator.py [--fix] [--tier {basic,technical,procedural,all}]
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Set, Dict, Tuple, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class ConstitutionValidator:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.three_tier_clauses = self._extract_three_tier_clauses()
        self.code_references: List[Dict] = []
        
    def _extract_three_tier_clauses(self) -> Dict[str, Set[str]]:
        """从三级法律体系中提取所有条款编号"""
        clauses = {
            "basic_law": set(),      # §1-§299
            "technical_law": set(),  # §300-§499
            "procedural_law": set()  # §500-§599
        }
        
        # 1. 基本法（宪法核心）
        basic_law_paths = [
            self.project_root / "templates/01_core/basic_law_index.md",
            self.project_root / "memory_bank/core/basic_law_index.md"
        ]
        
        for path in basic_law_paths:
            if path.exists():
                content = path.read_text(encoding="utf-8")
                for match in re.finditer(r'§(\d+(?:\.\d+)?)', content):
                    clause = match.group(0)
                    clause_num = float(clause.replace("§", ""))
                    if 1 <= clause_num < 300:
                        clauses["basic_law"].add(clause)
                break
        
        # 2. 技术法
        technical_law_paths = [
            self.project_root / "templates/01_core/technical_law_index.md",
            self.project_root / "memory_bank/core/technical_law_index.md"
        ]
        
        for path in technical_law_paths:
            if path.exists():
                content = path.read_text(encoding="utf-8")
                for match in re.finditer(r'§(\d+(?:\.\d+)?)', content):
                    clause = match.group(0)
                    clause_num = float(clause.replace("§", ""))
                    if 300 <= clause_num < 500:
                        clauses["technical_law"].add(clause)
                break
        
        # 3. 程序法
        procedural_law_paths = [
            self.project_root / "templates/01_core/procedural_law_index.md",
            self.project_root / "memory_bank/core/procedural_law_index.md"
        ]
        
        for path in procedural_law_paths:
            if path.exists():
                content = path.read_text(encoding="utf-8")
                for match in re.finditer(r'§(\d+(?:\.\d+)?)', content):
                    clause = match.group(0)
                    clause_num = float(clause.replace("§", ""))
                    if 500 <= clause_num < 600:
                        clauses["procedural_law"].add(clause)
                break
        
        print("📜 三级法律体系条款库加载完成:")
        for tier, tier_clauses in clauses.items():
            tier_name = {
                "basic_law": "基本法§1-§299",
                "technical_law": "技术法§300-§499",
                "procedural_law": "程序法§500-§599"
            }[tier]
            print(f"   - {tier_name}: {len(tier_clauses)} 个条款")
            for clause in sorted(tier_clauses)[:5]:
                print(f"      {clause}", end="")
            if len(tier_clauses) > 5:
                print(f" ... 还有 {len(tier_clauses) - 5} 个条款", end="")
            print()
        
        return clauses
    
    def scan_code_references(self, target_dir: Optional[Path] = None) -> List[Dict]:
        """扫描代码中的宪法引用"""
        if target_dir is None:
            target_dir = self.project_root / "scripts"
            
        references: List[Dict] = []
        
        # 扫描Python文件
        for py_file in target_dir.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
                for match in re.finditer(r'§(\d+(?:\.\d+)?)', content):
                    clause = match.group(0)
                    clause_num = float(clause.replace("§", ""))
                    
                    # 确定法律层级
                    if 1 <= clause_num < 300:
                        law_tier = "basic_law"
                    elif 300 <= clause_num < 500:
                        law_tier = "technical_law"
                    elif 500 <= clause_num < 600:
                        law_tier = "procedural_law"
                    else:
                        law_tier = "unknown"
                    
                    ref = {
                        "file": py_file.relative_to(self.project_root),
                        "clause": clause,
                        "law_tier": law_tier,
                        "line": content[:match.start()].count('\n') + 1,
                        "context": self._extract_context(content, match.start(), match.end())
                    }
                    references.append(ref)
            except Exception as e:
                print(f"⚠️  无法读取文件 {py_file}: {e}")
                
        self.code_references = references
        return references
    
    def _extract_context(self, content: str, start: int, end: int, context_lines: int = 2) -> str:
        """提取引用周围的上下文"""
        lines = content.split('\n')
        line_num = content[:start].count('\n')
        
        start_line = max(0, line_num - context_lines)
        end_line = min(len(lines), line_num + context_lines + 1)
        
        context_lines_list: List[str] = []
        for i in range(start_line, end_line):
            prefix = ">>> " if i == line_num else "    "
            context_lines_list.append(f"{prefix}{i+1:3}: {lines[i]}")
            
        return '\n'.join(context_lines_list)
    
    def validate_references(self, target_tier: str = "all") -> Tuple[List[Dict], List[Dict]]:
        """验证引用是否在对应的法律层级中有效"""
        valid: List[Dict] = []
        invalid: List[Dict] = []
        
        tier_names = {
            "basic_law": "基本法§1-§299",
            "technical_law": "技术法§300-§499", 
            "procedural_law": "程序法§500-§599"
        }
        
        for ref in self.code_references:
            law_tier = ref["law_tier"]
            clause = ref["clause"]
            
            # 过滤目标层级
            if target_tier != "all" and target_tier != law_tier:
                continue
            
            # 检查条款是否存在于对应的法律层级
            if law_tier in self.three_tier_clauses and clause in self.three_tier_clauses[law_tier]:
                valid.append(ref)
            else:
                # 检查是否存在于其他层级（法律层级错误）
                found_in_other = False
                for tier, clauses in self.three_tier_clauses.items():
                    if tier != law_tier and clause in clauses:
                        ref["expected_tier"] = tier
                        ref["expected_tier_name"] = tier_names[tier]
                        found_in_other = True
                        break
                
                if found_in_other:
                    # 法律层级错误（如§300.1引用为"宪法§300.1"但实际是技术法）
                    invalid.append(ref)
                else:
                    # 完全不存在
                    invalid.append(ref)
                
        return valid, invalid
    
    def fix_missing_clauses(self, missing_clauses: Set[str]):
        """修复缺失的宪法条款（添加到相应的法律层级）"""
        # 分析缺失条款的法律层级
        basic_missing = set()
        technical_missing = set()
        procedural_missing = set()
        
        for clause in missing_clauses:
            clause_num = float(clause.replace("§", ""))
            if 1 <= clause_num < 300:
                basic_missing.add(clause)
            elif 300 <= clause_num < 500:
                technical_missing.add(clause)
            elif 500 <= clause_num < 600:
                procedural_missing.add(clause)
        
        # 修复基本法缺失条款
        if basic_missing:
            self._fix_basic_law_clauses(basic_missing)
        
        # 修复技术法缺失条款
        if technical_missing:
            self._fix_technical_law_clauses(technical_missing)
        
        # 修复程序法缺失条款
        if procedural_missing:
            self._fix_procedural_law_clauses(procedural_missing)
    
    def _fix_basic_law_clauses(self, missing_clauses: Set[str]):
        """修复基本法缺失条款"""
        basic_law_path = self.project_root / "templates/01_core/basic_law_index.md"
        if not basic_law_path.exists():
            print("❌ 基本法索引文件不存在")
            return
            
        content = basic_law_path.read_text(encoding="utf-8")
        
        # 找到核心公理表格的位置
        table_start = content.find("## 核心公理 (必须熟记)")
        if table_start == -1:
            print("❌ 找不到核心公理表格")
            return
            
        # 找到表格结束位置
        table_end = content.find("\n\n", table_start)
        if table_end == -1:
            table_end = content.find("\n---", table_start)
            
        # 插入缺失的条款
        for clause in sorted(missing_clauses):
            if clause == "§300.1":
                # §300.1已添加到基本法，跳过
                print(f"✅ 条款 {clause} 已在基本法中（孢子协议）")
                continue
                
            clause_num = clause.replace("§", "")
            new_row = f'| **{clause}** | [待定义] | [待定义] |\n'
            
            # 找到插入位置（按数字顺序）
            lines = content[table_start:table_end].split('\n')
            insert_pos = -1
            
            for i, line in enumerate(lines):
                if '| **§' in line:
                    # 提取当前行的条款号
                    match = re.search(r'§(\d+(?:\.\d+)?)', line)
                    if match:
                        current_num = float(match.group(1))
                        clause_num_float = float(clause_num)
                        
                        if clause_num_float < current_num:
                            insert_pos = table_start + sum(len(l) + 1 for l in lines[:i])
                            break
            
            if insert_pos == -1:
                # 在表格末尾添加
                content = content[:table_end] + new_row + content[table_end:]
            else:
                content = content[:insert_pos] + new_row + content[insert_pos:]
            
            print(f"✅ 已添加条款 {clause} 到基本法索引")
        
        # 保存文件
        basic_law_path.write_text(content, encoding="utf-8")
        print("📝 基本法索引已更新")
    
    def _fix_technical_law_clauses(self, missing_clauses: Set[str]):
        """修复技术法缺失条款"""
        print(f"⚠️  技术法缺失条款修复功能待实现: {missing_clauses}")
        # 技术法结构复杂，需要更复杂的修复逻辑
    
    def _fix_procedural_law_clauses(self, missing_clauses: Set[str]):
        """修复程序法缺失条款"""
        print(f"⚠️  程序法缺失条款修复功能待实现: {missing_clauses}")
        # 程序法结构复杂，需要更复杂的修复逻辑
    
    def generate_report(self, valid: List[Dict], invalid: List[Dict], target_tier: str = "all") -> str:
        """生成验证报告"""
        report: List[str] = []
        report.append("=" * 70)
        report.append("📜 CDD 三级法律体系引用验证报告")
        report.append("=" * 70)
        
        # 统计信息
        total_refs = len(self.code_references)
        tier_stats = {"basic_law": 0, "technical_law": 0, "procedural_law": 0, "unknown": 0}
        for ref in self.code_references:
            tier_stats[ref["law_tier"]] += 1
        
        report.append(f"\n📊 统计信息:")
        report.append(f"   - 代码引用总数: {total_refs} 处")
        report.append(f"   - 基本法引用: {tier_stats['basic_law']} 处")
        report.append(f"   - 技术法引用: {tier_stats['technical_law']} 处")
        report.append(f"   - 程序法引用: {tier_stats['procedural_law']} 处")
        report.append(f"   - 有效引用: {len(valid)} 处")
        report.append(f"   - 无效引用: {len(invalid)} 处")
        
        if invalid:
            report.append(f"\n❌ 无效法律引用 ({len(invalid)} 处):")
            for i, ref in enumerate(invalid, 1):
                report.append(f"\n{i}. 文件: {ref['file']}:{ref['line']}")
                report.append(f"   引用条款: {ref['clause']}")
                report.append(f"   引用层级: {self._get_tier_name(ref['law_tier'])}")
                
                if "expected_tier" in ref:
                    report.append(f"   ❌ 法律层级错误: 应属于 {ref['expected_tier_name']}")
                else:
                    report.append(f"   ❌ 条款不存在于任何法律层级")
                
                report.append(f"   上下文:")
                report.append(ref['context'])
        
        if valid:
            report.append(f"\n✅ 有效法律引用 ({len(valid)} 处):")
            # 按层级分组显示
            tier_groups = {"basic_law": [], "technical_law": [], "procedural_law": []}
            for ref in valid:
                tier_groups[ref["law_tier"]].append(ref)
            
            for tier, refs in tier_groups.items():
                if refs:
                    tier_name = self._get_tier_name(tier)
                    report.append(f"\n   {tier_name} ({len(refs)} 处):")
                    for i, ref in enumerate(refs[:5], 1):
                        report.append(f"   {i}. {ref['file']}:{ref['line']} - {ref['clause']}")
                    if len(refs) > 5:
                        report.append(f"   ... 还有 {len(refs) - 5} 处引用")
                
        return "\n".join(report)
    
    def _get_tier_name(self, tier: str) -> str:
        """获取层级名称"""
        tier_names = {
            "basic_law": "基本法§1-§299",
            "technical_law": "技术法§300-§499",
            "procedural_law": "程序法§500-§599",
            "unknown": "未知层级"
        }
        return tier_names.get(tier, tier)

def main():
    parser = argparse.ArgumentParser(description="CDD Constitution Validator (三级法律体系)")
    parser.add_argument("--target", default="scripts", help="目标目录 (默认: scripts)")
    parser.add_argument("--tier", choices=["basic", "technical", "procedural", "all"], default="all", 
                       help="验证特定法律层级 (默认: 所有层级)")
    parser.add_argument("--fix", action="store_true", help="自动修复缺失的法律条款")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    validator = ConstitutionValidator(PROJECT_ROOT)
    
    # 扫描引用
    target_path = PROJECT_ROOT / args.target
    print(f"🔍 扫描 {target_path.relative_to(PROJECT_ROOT)} 目录中的法律引用...")
    references = validator.scan_code_references(target_path)
    
    if not references:
        print("ℹ️  未找到任何法律引用")
        return
    
    # 验证引用
    tier_map = {
        "basic": "basic_law",
        "technical": "technical_law", 
        "procedural": "procedural_law",
        "all": "all"
    }
    target_tier = tier_map[args.tier]
    
    valid, invalid = validator.validate_references(target_tier)
    
    # 生成报告
    report = validator.generate_report(valid, invalid, target_tier)
    print(report)
    
    # 自动修复
    if args.fix and invalid:
        missing_clauses = set(ref["clause"] for ref in invalid if "expected_tier" not in ref)
        if missing_clauses:
            print(f"\n🔧 正在修复 {len(missing_clauses)} 个缺失的法律条款...")
            validator.fix_missing_clauses(missing_clauses)
            
            # 重新验证
            print("\n🔍 重新验证修复后的引用...")
            validator.three_tier_clauses = validator._extract_three_tier_clauses()
            valid, invalid = validator.validate_references(target_tier)
            print(f"✅ 修复后: {len(valid)} 处有效引用, {len(invalid)} 处无效引用")
    
    # 输出退出码
    if invalid:
        print(f"\n❌ 验证失败: {len(invalid)} 处无效法律引用")
        sys.exit(1)
    else:
        print(f"\n✅ 所有法律引用有效!")
        sys.exit(0)

if __name__ == "__main__":
    main()