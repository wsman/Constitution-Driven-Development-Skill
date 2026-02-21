#!/usr/bin/env python3
"""
CDD Theme Auditor (cdd_theme_audit.py) v1.0.0
============================================
§119主题驱动开发公理审计工具，用于检测硬编码颜色违规。

宪法依据: §119主题驱动开发公理、§102熵减原则、§101单一真理源原则

使用场景:
1. State D验证阶段：检查UI组件是否符合§119主题合规
2. 提交前检查：防止硬编码颜色提交
3. 定期审计：确保技术资产库主题合规

Usage:
    python scripts/cdd_theme_audit.py scan [--path PATH] [--fix] [--verbose]
    python scripts/cdd_theme_audit.py validate <file> [--fix] [--verbose]
    python scripts/cdd_theme_audit.py stats [--json]

示例:
    python scripts/cdd_theme_audit.py scan --path library/components --verbose
    python scripts/cdd_theme_audit.py validate library/components/EntropyDashboard.tsx
    python scripts/cdd_theme_audit.py stats --json
"""

import sys
import os
import re
import argparse
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime

# 添加项目根目录到Python路径
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SKILL_ROOT))

VERSION = "2.0.0"

# -----------------------------------------------------------------------------
# 常量定义
# -----------------------------------------------------------------------------

# §119主题合规标准
THEME_COMPLIANCE_RULES = {
    "nordic_theme": {
        "required_import": r'@import.*nordic\.css',
        "theme_class": r'nordic-theme',
        "css_variable_prefix": r'var\(--[^)]+\)'
    }
}

# 硬编码颜色检测模式
HARDCODED_COLOR_PATTERNS = [
    # Hex颜色
    (r'#[0-9a-fA-F]{3,6}\b', 'hex_color'),
    # RGB/RGBA
    (r'rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(?:,\s*[\d\.]+)?\s*\)', 'rgb_color'),
    # HSL/HSLA
    (r'hsla?\(\s*\d+\s*,\s*\d+%?\s*,\s*\d+%?\s*(?:,\s*[\d\.]+)?\s*\)', 'hsl_color'),
    # CSS颜色名称（部分关键名称）
    (r'\b(?:red|green|blue|black|white|gray|grey)\b', 'named_color'),
    # 数字颜色值（在某些框架中）
    (r'color:\s*\d+', 'numeric_color')
]

# 允许的例外模式（主题文件本身、注释等）
ALLOWED_EXCEPTIONS = [
    r'nordic\.css',  # 主题文件本身
    r'/\*.*?\*/',    # CSS注释
    r'//.*?$',       # JS/TS单行注释
    r'#.*?$',        # Shell/Python注释
    r'<!--.*?-->',   # HTML注释
    r'template:',    # 模板文件
]

# 北欧主题CSS变量（从nordic.css中提取的核心变量）
NORDIC_CSS_VARIABLES = [
    '--bg-primary', '--bg-secondary', '--bg-tertiary', '--bg-elevated', '--bg-inset',
    '--text-primary', '--text-secondary', '--text-tertiary', '--text-inverse',
    '--accent-primary', '--accent-hover', '--accent-bg',
    '--status-success', '--status-warning', '--status-error', '--status-info',
    '--border-primary', '--border-secondary'
]

# -----------------------------------------------------------------------------
# 核心审计逻辑
# -----------------------------------------------------------------------------

class ThemeAuditor:
    """§119主题合规审计器"""
    
    def __init__(self, root_path: Optional[Path] = None, verbose: bool = False):
        self.root_path = root_path or SKILL_ROOT
        self.verbose = verbose
        self.results = {
            "scan_time": datetime.now().isoformat(),
            "version": VERSION,
            "total_files_scanned": 0,
            "files_with_violations": 0,
            "total_violations": 0,
            "violations_by_type": {},
            "compliant_files": 0,
            "details": []
        }
    
    def scan_directory(self, path: Path, file_patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        扫描目录下的文件，检查§119主题合规性
        
        Args:
            path: 要扫描的目录路径
            file_patterns: 文件模式列表，如['*.css', '*.jsx', '*.tsx']
        
        Returns:
            扫描结果字典
        """
        if file_patterns is None:
            file_patterns = ['*.css', '*.scss', '*.sass', '*.jsx', '*.tsx', '*.js', '*.ts']
        
        for pattern in file_patterns:
            for file_path in path.rglob(pattern):
                # 跳过不需要检查的文件
                if self._should_skip_file(file_path):
                    continue
                
                self.results["total_files_scanned"] += 1
                
                file_result = self._check_file(file_path)
                if file_result["has_violations"]:
                    self.results["files_with_violations"] += 1
                    self.results["total_violations"] += file_result["violation_count"]
                    self.results["details"].append(file_result)
                else:
                    self.results["compliant_files"] += 1
        
        return self.results
    
    def validate_file(self, file_path: Path, fix: bool = False) -> Dict[str, Any]:
        """
        验证单个文件的§119主题合规性
        
        Args:
            file_path: 文件路径
            fix: 是否自动修复
        
        Returns:
            验证结果字典
        """
        if not file_path.exists():
            return {
                "success": False,
                "error": f"文件不存在: {file_path}",
                "file_path": str(file_path)
            }
        
        file_result = self._check_file(file_path)
        
        if fix and file_result["has_violations"]:
            fixed_result = self._fix_file(file_path, file_result)
            file_result.update({
                "fixed": True,
                "fix_result": fixed_result
            })
        
        return file_result
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """判断是否跳过文件检查"""
        skip_patterns = [
            '__pycache__', '.git', 'node_modules', '.entropy_cache',
            '.pytest_cache', 'dist', 'build', 'coverage'
        ]
        
        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)
    
    def _check_file(self, file_path: Path) -> Dict[str, Any]:
        """
        检查单个文件的主题合规性
        
        Returns:
            检查结果字典
        """
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return {
                "file_path": str(file_path),
                "file_type": file_path.suffix,
                "success": False,
                "error": f"无法读取文件: {e}",
                "has_violations": False,
                "violation_count": 0,
                "violations": []
            }
        
        violations = self._detect_violations(content, file_path)
        has_theme_import = self._check_theme_import(content, file_path)
        uses_css_variables = self._check_css_variables_usage(content)
        
        return {
            "file_path": str(file_path),
            "file_type": file_path.suffix,
            "success": True,
            "has_violations": len(violations) > 0,
            "violation_count": len(violations),
            "violations": violations,
            "has_theme_import": has_theme_import,
            "uses_css_variables": uses_css_variables,
            "compliance_score": self._calculate_compliance_score(
                len(violations), has_theme_import, uses_css_variables
            )
        }
    
    def _detect_violations(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """检测硬编码颜色违规"""
        violations = []
        lines = content.splitlines()
        
        for line_num, line in enumerate(lines, 1):
            for pattern, violation_type in HARDCODED_COLOR_PATTERNS:
                matches = list(re.finditer(pattern, line, re.IGNORECASE))
                
                for match in matches:
                    # 检查是否在允许的例外中
                    if self._is_allowed_exception(line, match.group()):
                        continue
                    
                    # 检查是否在CSS变量定义中（主题文件本身）
                    if file_path.name == 'nordic.css' and ':' in line:
                        # 主题文件定义CSS变量是允许的
                        continue
                    
                    violation = {
                        "line": line_num,
                        "column": match.start() + 1,
                        "violation_type": violation_type,
                        "offending_text": match.group(),
                        "context": line.strip()[:100],
                        "suggestion": self._generate_fix_suggestion(match.group(), file_path)
                    }
                    violations.append(violation)
        
        return violations
    
    def _is_allowed_exception(self, line: str, match_text: str) -> bool:
        """检查是否属于允许的例外情况"""
        # 检查是否在注释中
        comment_patterns = [r'/\*.*?\*/', r'//.*$', r'#.*$', r'<!--.*?-->']
        for pattern in comment_patterns:
            if re.search(pattern, line):
                return True
        
        # 检查是否是CSS变量的一部分（如 var(--accent-primary) 中的 primary 不是颜色）
        if 'var(' in line and '--' in line:
            return True
        
        # 检查是否是字符串字面量的一部分
        string_patterns = [r"'.*?'", r'".*?"', r'`.*?`']
        for pattern in string_patterns:
            for string_match in re.finditer(pattern, line):
                if string_match.start() <= line.find(match_text) <= string_match.end():
                    return True
        
        return False
    
    def _check_theme_import(self, content: str, file_path: Path) -> bool:
        """检查是否导入了北欧主题"""
        if file_path.suffix not in ['.css', '.scss', '.sass']:
            return True  # 非CSS文件不需要主题导入
        
        import_patterns = [
            r'@import\s+[\'"`].*nordic\.css[\'"`]',
            r'@import\s+url\(.*nordic\.css\)',
            r'import\s+[\'"`].*nordic\.css[\'"`]'  # 对于某些预处理器的导入
        ]
        
        for pattern in import_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _check_css_variables_usage(self, content: str) -> bool:
        """检查是否使用了CSS变量"""
        variable_pattern = r'var\(--[^)]+\)'
        matches = re.findall(variable_pattern, content)
        
        # 检查是否使用了任何北欧主题变量
        for match in matches:
            for var_name in NORDIC_CSS_VARIABLES:
                if var_name in match:
                    return True
        
        return len(matches) > 0  # 即使不是北欧变量，使用CSS变量也是好的
    
    def _calculate_compliance_score(self, violation_count: int, has_theme_import: bool, 
                                   uses_css_variables: bool) -> float:
        """计算合规分数（0-100）"""
        if violation_count == 0:
            base_score = 100
        elif violation_count <= 2:
            base_score = 80
        elif violation_count <= 5:
            base_score = 60
        else:
            base_score = 40
        
        # 调整分数
        if not has_theme_import:
            base_score -= 20
        
        if not uses_css_variables:
            base_score -= 10
        
        return max(0, min(100, base_score))
    
    def _generate_fix_suggestion(self, offending_text: str, file_path: Path) -> str:
        """生成修复建议"""
        file_type = file_path.suffix
        
        if file_type in ['.css', '.scss', '.sass']:
            # CSS文件建议使用语义化变量
            if 'background' in offending_text.lower() or 'bg' in offending_text:
                return f"使用 var(--bg-primary) 或 var(--bg-secondary) 代替 {offending_text}"
            elif 'color' in offending_text.lower() or 'text' in offending_text:
                return f"使用 var(--text-primary) 或 var(--text-secondary) 代替 {offending_text}"
            elif any(status in offending_text.lower() for status in ['success', 'error', 'warning', 'info']):
                return f"使用相应的状态变量代替 {offending_text}"
            else:
                return f"使用适当的CSS变量代替 {offending_text}，参考 library/themes/nordic.css"
        
        elif file_type in ['.jsx', '.tsx', '.js', '.ts']:
            # JS/TS文件建议使用CSS变量或主题配置
            return f"使用CSS变量或主题配置代替硬编码颜色 {offending_text}"
        
        return f"请使用主题变量代替硬编码颜色 {offending_text}"
    
    def _fix_file(self, file_path: Path, file_result: Dict[str, Any]) -> Dict[str, Any]:
        """尝试自动修复文件（基础版本，未来可扩展）"""
        # 目前只记录需要修复的内容
        # 实际修复逻辑需要更复杂的实现
        return {
            "fixed_violations": file_result["violation_count"],
            "notes": "自动修复功能尚在开发中。请手动修复违规。",
            "manual_fixes_needed": file_result["violations"]
        }
    
    def generate_stats(self) -> Dict[str, Any]:
        """生成统计信息"""
        if not self.results["details"]:
            return {
                "success": False,
                "error": "未执行扫描，请先运行 scan 命令",
                "results": self.results
            }
        
        # 分析违规类型分布
        violation_types = {}
        for detail in self.results["details"]:
            for violation in detail["violations"]:
                v_type = violation["violation_type"]
                violation_types[v_type] = violation_types.get(v_type, 0) + 1
        
        # 计算合规率
        total_files = self.results["total_files_scanned"]
        compliant_files = self.results["compliant_files"]
        compliance_rate = (compliant_files / total_files * 100) if total_files > 0 else 0
        
        stats = {
            "scan_summary": {
                "total_files_scanned": total_files,
                "compliant_files": compliant_files,
                "files_with_violations": self.results["files_with_violations"],
                "total_violations": self.results["total_violations"],
                "compliance_rate": round(compliance_rate, 2)
            },
            "violation_analysis": {
                "by_type": violation_types,
                "most_common_violation": max(violation_types.items(), key=lambda x: x[1]) if violation_types else None,
                "average_violations_per_file": round(self.results["total_violations"] / max(1, self.results["files_with_violations"]), 2)
            },
            "file_type_analysis": self._analyze_by_file_type(),
            "recommendations": self._generate_recommendations()
        }
        
        return {
            "success": True,
            "stats": stats,
            "raw_results": self.results
        }
    
    def _analyze_by_file_type(self) -> Dict[str, Any]:
        """按文件类型分析"""
        analysis = {}
        for detail in self.results["details"]:
            file_type = detail["file_type"]
            if file_type not in analysis:
                analysis[file_type] = {
                    "count": 0,
                    "violations": 0,
                    "compliant": 0
                }
            
            analysis[file_type]["count"] += 1
            if detail["has_violations"]:
                analysis[file_type]["violations"] += 1
            else:
                analysis[file_type]["compliant"] += 1
        
        return analysis
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        compliance_rate = (self.results["compliant_files"] / self.results["total_files_scanned"] * 100) \
            if self.results["total_files_scanned"] > 0 else 0
        
        if compliance_rate < 80:
            recommendations.append("§119合规率低于80%，建议进行主题合规培训")
        
        if self.results["total_violations"] > 10:
            recommendations.append(f"发现 {self.results['total_violations']} 处硬编码颜色，建议批量修复")
        
        # 检查主题导入情况
        missing_imports = 0
        for detail in self.results["details"]:
            if detail["file_type"] in ['.css', '.scss', '.sass'] and not detail["has_theme_import"]:
                missing_imports += 1
        
        if missing_imports > 0:
            recommendations.append(f"{missing_imports} 个CSS文件缺少北欧主题导入")
        
        # 检查CSS变量使用情况
        low_variable_usage = 0
        for detail in self.results["details"]:
            if not detail["uses_css_variables"] and detail["file_type"] in ['.css', '.scss', '.sass']:
                low_variable_usage += 1
        
        if low_variable_usage > 0:
            recommendations.append(f"{low_variable_usage} 个CSS文件未使用CSS变量，建议学习变量使用")
        
        if not recommendations:
            recommendations.append("§119主题合规性良好，继续保持")
        
        return recommendations

# -----------------------------------------------------------------------------
# CLI接口
# -----------------------------------------------------------------------------

def format_scan_result(result: Dict[str, Any], verbose: bool = False) -> str:
    """格式化扫描结果输出"""
    output = []
    
    output.append(f"🎨 CDD Theme Auditor v{VERSION}")
    output.append(f"📅 扫描时间: {result.get('scan_time', 'N/A')}")
    output.append("=" * 40)
    
    # 概要信息
    output.append("📊 扫描概要:")
    output.append(f"  扫描文件数: {result.get('total_files_scanned', 0)}")
    output.append(f"  合规文件数: {result.get('compliant_files', 0)}")
    output.append(f"  违规文件数: {result.get('files_with_violations', 0)}")
    output.append(f"  总违规数: {result.get('total_violations', 0)}")
    
    # 合规率计算
    total_files = result.get('total_files_scanned', 1)
    compliant_files = result.get('compliant_files', 0)
    compliance_rate = (compliant_files / total_files * 100) if total_files > 0 else 0
    
    if compliance_rate >= 90:
        status_emoji = "🟢"
    elif compliance_rate >= 70:
        status_emoji = "🟡"
    else:
        status_emoji = "🔴"
    
    output.append(f"  §119合规率: {compliance_rate:.1f}% {status_emoji}")
    
    # 违规类型分布
    violation_types = {}
    for detail in result.get('details', []):
        for violation in detail.get('violations', []):
            v_type = violation.get('violation_type', 'unknown')
            violation_types[v_type] = violation_types.get(v_type, 0) + 1
    
    if violation_types:
        output.append("\n🔍 违规类型分布:")
        for v_type, count in sorted(violation_types.items()):
            output.append(f"  • {v_type}: {count} 处")
    
    # 详细违规信息（详细模式）
    if verbose and result.get('details'):
        output.append("\n📋 详细违规信息:")
        for detail in result['details']:
            if detail['has_violations']:
                output.append(f"\n  📄 {detail['file_path']}")
                output.append(f"    类型: {detail['file_type']}")
                output.append(f"    违规数: {detail['violation_count']}")
                output.append(f"    合规分数: {detail.get('compliance_score', 'N/A')}")
                
                for i, violation in enumerate(detail['violations'][:3], 1):
                    output.append(f"    {i}. 行 {violation['line']}: {violation['offending_text']}")
                    output.append(f"       建议: {violation['suggestion']}")
                
                if detail['violation_count'] > 3:
                    output.append(f"    ... 还有 {detail['violation_count'] - 3} 处违规")
    
    # 建议
    recommendations = []
    if compliance_rate < 80:
        recommendations.append("进行主题合规培训，学习CSS变量使用")
    if result.get('total_violations', 0) > 0:
        recommendations.append("修复硬编码颜色违规")
    
    if recommendations:
        output.append("\n💡 建议:")
        for rec in recommendations:
            output.append(f"  • {rec}")
    
    return "\n".join(output)

def format_validation_result(result: Dict[str, Any]) -> str:
    """格式化验证结果输出"""
    output = []
    
    output.append(f"✅ CDD Theme Validator v{VERSION}")
    output.append(f"📄 验证文件: {result.get('file_path', 'N/A')}")
    output.append("=" * 40)
    
    if not result.get('success', False):
        output.append(f"❌ 验证失败: {result.get('error', 'Unknown error')}")
        return "\n".join(output)
    
    if result.get('has_violations', False):
        output.append("❌ §119主题合规检查失败")
        output.append(f"   违规数量: {result.get('violation_count', 0)}")
        output.append(f"   合规分数: {result.get('compliance_score', 0)}")
        
        output.append("\n🔍 违规详情:")
        for i, violation in enumerate(result.get('violations', []), 1):
            output.append(f"\n  {i}. 行 {violation['line']}, 列 {violation['column']}")
            output.append(f"     违规类型: {violation['violation_type']}")
            output.append(f"     违规内容: {violation['offending_text']}")
            output.append(f"     上下文: {violation['context']}")
            output.append(f"     修复建议: {violation['suggestion']}")
    else:
        output.append("✅ §119主题合规检查通过")
        output.append(f"   合规分数: {result.get('compliance_score', 100)}")
        
        # 额外信息
        if not result.get('has_theme_import', True) and result.get('file_type') in ['.css', '.scss', '.sass']:
            output.append("⚠️  提示: 文件缺少北欧主题导入，但无硬编码颜色违规")
        elif not result.get('uses_css_variables', False) and result.get('file_type') in ['.css', '.scss', '.sass']:
            output.append("💡 建议: 考虑使用CSS变量提高主题一致性")
    
    return "\n".join(output)

def format_stats_result(result: Dict[str, Any]) -> str:
    """格式化统计结果输出"""
    if not result.get('success', False):
        return f"❌ 统计生成失败: {result.get('error', 'Unknown error')}"
    
    stats = result.get('stats', {})
    summary = stats.get('scan_summary', {})
    
    output = []
    
    output.append(f"📊 CDD Theme Statistics v{VERSION}")
    output.append("=" * 40)
    
    output.append("📈 扫描统计:")
    output.append(f"  • 总扫描文件数: {summary.get('total_files_scanned', 0)}")
    output.append(f"  • 合规文件数: {summary.get('compliant_files', 0)}")
    output.append(f"  • 违规文件数: {summary.get('files_with_violations', 0)}")
    output.append(f"  • 总违规数: {summary.get('total_violations', 0)}")
    output.append(f"  • §119合规率: {summary.get('compliance_rate', 0)}%")
    
    # 违规分析
    violation_analysis = stats.get('violation_analysis', {})
    if violation_analysis:
        output.append("\n🔍 违规分析:")
        by_type = violation_analysis.get('by_type', {})
        if by_type:
            output.append("  违规类型分布:")
            for v_type, count in sorted(by_type.items()):
                output.append(f"    • {v_type}: {count} 处")
        
        most_common = violation_analysis.get('most_common_violation')
        if most_common:
            output.append(f"  最常见违规: {most_common[0]} ({most_common[1]} 处)")
        
        avg_violations = violation_analysis.get('average_violations_per_file', 0)
        output.append(f"  平均每文件违规数: {avg_violations}")
    
    # 文件类型分析
    file_type_analysis = stats.get('file_type_analysis', {})
    if file_type_analysis:
        output.append("\n📂 文件类型分析:")
        for file_type, analysis in file_type_analysis.items():
            compliance_rate = (analysis.get('compliant', 0) / max(1, analysis.get('count', 1))) * 100
            output.append(f"  • {file_type}: {analysis.get('count', 0)} 文件, {compliance_rate:.1f}% 合规")
    
    # 建议
    recommendations = stats.get('recommendations', [])
    if recommendations:
        output.append("\n💡 改进建议:")
        for rec in recommendations:
            output.append(f"  • {rec}")
    
    return "\n".join(output)

# -----------------------------------------------------------------------------
# 主函数
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=f"CDD Theme Auditor v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/cdd_theme_audit.py scan --path library/components --verbose
  python scripts/cdd_theme_audit.py validate library/components/EntropyDashboard.tsx
  python scripts/cdd_theme_audit.py scan --fix  # 尝试自动修复
  python scripts/cdd_theme_audit.py stats --json
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # scan 命令
    scan_parser = subparsers.add_parser("scan", help="扫描目录检查§119合规性")
    scan_parser.add_argument("--path", "-p", default=".", help="扫描路径（默认：当前目录）")
    scan_parser.add_argument("--fix", "-f", action="store_true", help="尝试自动修复")
    scan_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    scan_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # validate 命令
    validate_parser = subparsers.add_parser("validate", help="验证单个文件§119合规性")
    validate_parser.add_argument("file", help="要验证的文件路径")
    validate_parser.add_argument("--fix", "-f", action="store_true", help="尝试自动修复")
    validate_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    validate_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="查看主题审计统计")
    stats_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "scan":
            scan_path = Path(args.path).resolve()
            if not scan_path.exists():
                print(f"❌ 路径不存在: {scan_path}")
                sys.exit(1)
            
            auditor = ThemeAuditor(scan_path, args.verbose)
            result = auditor.scan_directory(scan_path)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_scan_result(result, args.verbose))
            
            # 退出码：有违规则返回1
            sys.exit(0 if result.get('files_with_violations', 0) == 0 else 1)
        
        elif args.command == "validate":
            file_path = Path(args.file).resolve()
            if not file_path.exists():
                print(f"❌ 文件不存在: {file_path}")
                sys.exit(1)
            
            auditor = ThemeAuditor(file_path.parent, args.verbose)
            result = auditor.validate_file(file_path, args.fix)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_validation_result(result))
            
            # 退出码：有违规则返回1
            sys.exit(0 if not result.get('has_violations', False) else 1)
        
        elif args.command == "stats":
            # stats需要先有扫描结果
            # 这里我们重新扫描当前目录或使用缓存结果
            # 简单实现：扫描当前目录
            scan_path = Path(".").resolve()
            auditor = ThemeAuditor(scan_path, False)
            auditor.scan_directory(scan_path)
            result = auditor.generate_stats()
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_stats_result(result))
            
            sys.exit(0 if result.get('success', False) else 1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  操作被用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

# -----------------------------------------------------------------------------
# Claude Code桥梁接口
# -----------------------------------------------------------------------------

def scan_theme_claude(path: str = ".", verbose: bool = False, **kwargs) -> dict:
    """Claude Code主题扫描接口"""
    scan_path = Path(path).resolve()
    if not scan_path.exists():
        return {"success": False, "error": f"Path does not exist: {path}"}
    
    auditor = ThemeAuditor(scan_path, verbose)
    result = auditor.scan_directory(scan_path)
    
    result["success"] = result.get('files_with_violations', 0) == 0
    result["tool_version"] = VERSION
    
    return result

def validate_theme_claude(file_path: str, fix: bool = False, **kwargs) -> dict:
    """Claude Code主题验证接口"""
    file_path_obj = Path(file_path).resolve()
    if not file_path_obj.exists():
        return {"success": False, "error": f"File does not exist: {file_path}"}
    
    auditor = ThemeAuditor(file_path_obj.parent, kwargs.get('verbose', False))
    result = auditor.validate_file(file_path_obj, fix)
    
    result["tool_version"] = VERSION
    
    return result

def theme_stats_claude(**kwargs) -> dict:
    """Claude Code主题统计接口"""
    scan_path = Path(".").resolve()
    auditor = ThemeAuditor(scan_path, False)
    auditor.scan_directory(scan_path)
    result = auditor.generate_stats()
    
    result["tool_version"] = VERSION
    
    return result

if __name__ == "__main__":
    main()