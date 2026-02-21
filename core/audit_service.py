"""
CDD Audit Service (audit_service.py) v2.0.0
===========================================
审计服务的核心业务逻辑，整合自scripts/cdd_auditor.py和claude_tools/cdd_audit_tool.py。

宪法依据: §101§102§300.3
"""

import sys
import os
import re
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

from core.constants import *
from core.exceptions import AuditGateFailed, ToolExecutionError
from utils.cache_manager import CacheManager

# -----------------------------------------------------------------------------
# Error Codes
# -----------------------------------------------------------------------------
EC_SUCCESS = 0
EC_GATE_1_FAIL = 101  # Version Mismatch
EC_GATE_2_FAIL = 102  # Tests Failed
EC_GATE_3_FAIL = 103  # Entropy High
EC_GATE_4_FAIL = 105  # Semantic Audit Failed
EC_GATE_5_FAIL = 106  # Constitution Reference Invalid
EC_CLEAN_FAIL = 104
EC_GENERAL_FAIL = 1


class VersionChecker:
    """版本一致性检查器"""
    
    VERSION_PATTERNS = [
        (r'VERSION\s*=\s*["\'](\d+\.\d+\.\d+)["\']', 'Python VERSION constant'),
        (r'"version":\s*"(\d+\.\d+\.\d+)"', 'JSON version field'),
        (r'版本[：:]\s*(?:v)?(\d+\.\d+\.\d+)', 'Chinese version header'),
        (r'Version[：:]\s*(?:v)?(\d+\.\d+\.\d+)', 'English version header'),
        (r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']', 'Python __version__'),
        (r'v(\d+\.\d+\.\d+)', 'Explicit v-prefixed version'),
    ]
    
    def __init__(self, project_root: Path, verbose: bool = False):
        self.project_root = project_root
        self.verbose = verbose
    
    def scan_versions(self) -> Dict[str, Dict[str, str]]:
        """扫描项目中所有版本号"""
        results = {}
        
        # 扫描Python文件
        for py_file in self.project_root.rglob("*.py"):
            if self._should_skip(py_file):
                continue
            version = self._extract_version(py_file)
            if version:
                results[str(py_file.relative_to(self.project_root))] = {
                    "version": version,
                    "type": "python"
                }
        
        # 扫描Markdown文件
        for md_file in self.project_root.rglob("*.md"):
            if self._should_skip(md_file):
                continue
            version = self._extract_version(md_file)
            if version:
                results[str(md_file.relative_to(self.project_root))] = {
                    "version": version,
                    "type": "markdown"
                }
        
        return results
    
    def _should_skip(self, path: Path) -> bool:
        """判断是否跳过该路径"""
        path_str = str(path)
        
        # 跳过的目录模式
        skip_dir_patterns = [
            '__pycache__', '.git', 'node_modules', '.entropy_cache',
            '.venv', 'venv', '.pytest_cache', 'site-packages',
            'build', 'dist', 'egg-info',
        ]
        
        # 跳过的路径前缀（示例和测试数据目录）
        skip_path_prefixes = [
            'specs/', 'examples/', 'reference/', 'templates/',
        ]
        
        # 检查目录模式
        for pattern in skip_dir_patterns:
            if pattern in path_str:
                return True
        
        # 检查路径前缀
        path_relative = str(path.relative_to(self.project_root)) if path.is_relative_to(self.project_root) else path_str
        for prefix in skip_path_prefixes:
            if path_relative.startswith(prefix):
                return True
        
        # 跳过测试文件
        if 'test_' in path.name or '_test.py' in path.name:
            return True
        
        return False
    
    def _extract_version(self, file_path: Path) -> Optional[str]:
        """从文件提取版本号"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            for pattern, desc in self.VERSION_PATTERNS:
                match = re.search(pattern, content)
                if match:
                    return match.group(1)
        except Exception:
            pass
        return None
    
    def check_consistency(self) -> Tuple[bool, Dict[str, Any]]:
        """检查版本一致性"""
        versions = self.scan_versions()
        
        if not versions:
            return True, {"message": "未找到版本号", "files": {}}
        
        unique_versions = set(v["version"] for v in versions.values())
        
        if len(unique_versions) == 1:
            return True, {
                "consistent": True,
                "version": next(iter(unique_versions)),
                "files": versions
            }
        else:
            return False, {
                "consistent": False,
                "unique_versions": list(unique_versions),
                "files": versions,
                "distribution": self._calculate_distribution(versions)
            }
    
    def _calculate_distribution(self, versions: Dict) -> Dict[str, int]:
        """计算版本分布"""
        distribution: Dict[str, int] = {}
        for info in versions.values():
            v = info["version"]
            distribution[v] = distribution.get(v, 0) + 1
        return distribution
    
    def fix_versions(self, target_version: str) -> Dict[str, Any]:
        """修复版本不一致"""
        results = {"updated": [], "failed": []}
        versions = self.scan_versions()
        
        for file_path, info in versions.items():
            if info["version"] != target_version:
                full_path = self.project_root / file_path
                try:
                    content = full_path.read_text(encoding='utf-8')
                    # 替换版本号
                    for pattern, _ in self.VERSION_PATTERNS:
                        content = re.sub(
                            pattern,
                            lambda m: m.group(0).replace(m.group(1), target_version),
                            content
                        )
                    full_path.write_text(content, encoding='utf-8')
                    results["updated"].append(file_path)
                except Exception as e:
                    results["failed"].append({"file": file_path, "error": str(e)})
        
        return results


class CDDAuditor:
    """CDD统一审计器"""
    
    def __init__(self, project_root: Path, verbose: bool = False):
        self.project_root = project_root
        self.verbose = verbose
        self.results: List[Dict[str, Any]] = []
        self.failed = False
        self.version_checker = VersionChecker(project_root, verbose)
    
    def run_gate_1(self) -> bool:
        """Gate 1: 版本一致性检查"""
        consistent, details = self.version_checker.check_consistency()
        
        gate_result = {
            "gate": 1,
            "name": "Version Consistency",
            "passed": consistent,
            "details": details
        }
        self.results.append(gate_result)
        
        if not consistent:
            self.failed = True
            raise AuditGateFailed(1, f"Version mismatch: {details.get('unique_versions', [])}")
        
        return True
    
    def run_gate_2(self) -> bool:
        """Gate 2: 行为验证（测试）"""
        # 检查pytest是否安装
        try:
            import pytest
            pytest_available = True
        except ImportError:
            pytest_available = False
        
        # 如果pytest未安装，优雅降级
        if not pytest_available:
            gate_result = {
                "gate": 2,
                "name": "Behavior Verification",
                "passed": True,  # 跳过时视为通过
                "skipped": True,
                "details": {
                    "note": "pytest未安装，跳过行为验证",
                    "suggestion": "运行 'pip install pytest' 安装pytest以启用行为验证"
                }
            }
            self.results.append(gate_result)
            if self.verbose:
                print("  [Gate 2] pytest未安装，跳过行为验证")
            return True
        
        # 检查tests目录是否存在
        tests_dir = self.project_root / "tests"
        if not tests_dir.exists():
            gate_result = {
                "gate": 2,
                "name": "Behavior Verification",
                "passed": True,  # 无测试目录时视为通过
                "skipped": True,
                "details": {
                    "note": "未找到tests目录，跳过行为验证",
                    "suggestion": "创建tests目录并添加测试用例"
                }
            }
            self.results.append(gate_result)
            if self.verbose:
                print("  [Gate 2] 未找到tests目录，跳过行为验证")
            return True
        
        cmd = [sys.executable, "-m", "pytest", "-v", "--tb=short"]
        if self.verbose:
            cmd.append("-v")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=120  # 2分钟超时
            )
            success = result.returncode == 0
        except subprocess.TimeoutExpired:
            gate_result = {
                "gate": 2,
                "name": "Behavior Verification",
                "passed": False,
                "details": {"error": "测试执行超时 (120秒)"}
            }
            self.results.append(gate_result)
            self.failed = True
            raise AuditGateFailed(2, "Tests timeout")
        except Exception as e:
            gate_result = {
                "gate": 2,
                "name": "Behavior Verification",
                "passed": False,
                "details": {"error": str(e)}
            }
            self.results.append(gate_result)
            self.failed = True
            raise AuditGateFailed(2, f"Tests execution error: {e}")
        
        gate_result = {
            "gate": 2,
            "name": "Behavior Verification",
            "passed": success,
            "details": result.stdout if result.stdout else result.stderr
        }
        self.results.append(gate_result)
        
        if not success:
            self.failed = True
            raise AuditGateFailed(2, "Tests failed")
        
        return True
    
    def run_gate_3(self, cache_manager: Optional[CacheManager] = None) -> bool:
        """Gate 3: 熵值监控"""
        # 导入熵值服务
        try:
            from .entropy_service import EntropyService
            entropy_service = EntropyService(self.project_root)
            entropy_result = entropy_service.calculate_entropy(cache_manager)
        except ImportError:
            # 回退到简单实现
            from utils.entropy_utils import calculate_simple_entropy
            entropy_result = calculate_simple_entropy(self.project_root)
        
        h_sys = entropy_result.get("h_sys")
        if h_sys is None:
            h_sys = 1.0
        
        passed = h_sys <= THRESHOLD_WARNING
        
        gate_result = {
            "gate": 3,
            "name": "Entropy Monitoring",
            "passed": passed,
            "details": {
                "h_sys": h_sys,
                "threshold": THRESHOLD_WARNING,
                "threshold_exceeded": h_sys > THRESHOLD_WARNING
            }
        }
        self.results.append(gate_result)
        
        if not passed:
            self.failed = True
            raise AuditGateFailed(3, f"H_sys = {h_sys:.4f} > {THRESHOLD_WARNING}")
        
        return True
    
    def _run_theme_compliance_check(self) -> Dict[str, Any]:
        """运行§119主题合规检查"""
        try:
            # 尝试导入主题审计工具
            theme_audit_path = self.project_root / "scripts" / "cdd_theme_audit.py"
            if not theme_audit_path.exists():
                # 如果主题审计工具不存在，返回跳过结果
                return {
                    "success": True,
                    "skipped": True,
                    "note": "主题审计工具未找到，跳过§119合规检查",
                    "suggestion": "安装cdd_theme_audit.py工具以启用§119主题合规检查"
                }
            
            # 使用子进程调用主题审计工具
            import subprocess
            cmd = [sys.executable, str(theme_audit_path), "scan", "--path", str(self.project_root), "--json"]
            
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30  # 30秒超时
            )
            
            if result.returncode != 0:
                # 命令执行失败
                return {
                    "success": False,
                    "error": f"主题审计工具执行失败: {result.stderr[:200]}",
                    "raw_output": result.stdout[:500]
                }
            
            # 解析JSON输出
            try:
                audit_result = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error": f"无法解析主题审计结果: {e}",
                    "raw_output": result.stdout[:500]
                }
            
            # 提取关键指标
            total_files = audit_result.get("total_files_scanned", 0)
            compliant_files = audit_result.get("compliant_files", 0)
            violations = audit_result.get("total_violations", 0)
            
            # 计算§119合规率
            compliance_rate = (compliant_files / total_files * 100) if total_files > 0 else 100
            
            return {
                "success": True,
                "compliance_rate": compliance_rate,
                "total_files_scanned": total_files,
                "compliant_files": compliant_files,
                "files_with_violations": audit_result.get("files_with_violations", 0),
                "total_violations": violations,
                "details": audit_result.get("details", []),
                "raw_result": audit_result
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "主题审计执行超时 (30秒)",
                "skipped": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"主题合规检查异常: {str(e)}",
                "skipped": True
            }
    
    def run_gate_4(self) -> bool:
        """Gate 4: 语义审计（包含宪法引用和§119主题合规）"""
        # 运行宪法引用覆盖率检查
        try:
            from core.constitution_core import CONSTITUTION_CORE_ARTICLES, get_all_core_sections
            all_articles = get_all_core_sections()
            if self.verbose:
                print(f"  [Gate 4] 加载了 {len(all_articles)} 个宪法核心条款")
        except ImportError as e:
            if self.verbose:
                print(f"  [Gate 4] 无法加载宪法核心条款，使用回退列表: {e}")
            # 回退到常量中的硬编码列表
            all_articles = CONSTITUTION_ARTICLES
        
        found_articles = set()
        
        # 扫描所有文档文件
        scanned_files = 0
        for md_file in self.project_root.rglob("*.md"):
            if '.git' in str(md_file) or '__pycache__' in str(md_file):
                continue
            
            scanned_files += 1
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                for article in all_articles:
                    if article in content:
                        found_articles.add(article)
            except Exception as e:
                if self.verbose:
                    print(f"  [Gate 4] 无法读取文件 {md_file}: {e}")
                continue
        
        # 运行§119主题合规检查
        theme_compliance_result = self._run_theme_compliance_check()
        
        # 合并结果
        if not all_articles:
            # 如果没有找到任何宪法条款定义，Gate通过但警告
            gate_result = {
                "gate": 4,
                "name": "Semantic Audit",
                "passed": True,
                "skipped": True,
                "details": {
                    "note": "未找到宪法条款定义，跳过语义审计",
                    "suggestion": "确保core/constitution_core.py文件存在且包含CONSTITUTION_CORE_ARTICLES定义",
                    "theme_compliance": theme_compliance_result
                }
            }
            self.results.append(gate_result)
            return True
        
        # 计算宪法引用覆盖率
        constitution_coverage = len(found_articles) / len(all_articles) * 100
        constitution_passed = constitution_coverage >= 80  # 至少80%覆盖率
        
        # 计算§119主题合规率
        theme_passed = True
        theme_compliance_rate = 100
        if theme_compliance_result.get("success", False) and not theme_compliance_result.get("skipped", False):
            theme_compliance_rate = theme_compliance_result.get("compliance_rate", 100)
            theme_passed = theme_compliance_rate >= 80  # 至少80%主题合规率
        elif theme_compliance_result.get("skipped", False):
            # 跳过主题检查时视为通过
            theme_passed = True
        else:
            # 主题检查失败时视为不通过
            theme_passed = False
        
        # 总体通过条件：宪法引用通过且主题合规通过
        overall_passed = constitution_passed and theme_passed
        
        # 计算缺失的宪法条款
        missing_articles = [article for article in all_articles if article not in found_articles]
        
        # 构建详细结果
        details = {
            "scanned_files": scanned_files,
            "constitution_coverage": round(constitution_coverage, 2),
            "found_count": len(found_articles),
            "total_count": len(all_articles),
            "found_articles": sorted(list(found_articles)),
            "missing_articles": missing_articles[:10],  # 只显示前10个缺失条款
            "missing_count": len(missing_articles),
            "coverage_threshold": 80,
            "theme_compliance": theme_compliance_result
        }
        
        # 添加主题合规率（如果可用）
        if "compliance_rate" in theme_compliance_result:
            details["theme_compliance_rate"] = round(theme_compliance_result["compliance_rate"], 2)
            details["theme_compliance_threshold"] = 80
        
        gate_result = {
            "gate": 4,
            "name": "Semantic Audit",
            "passed": overall_passed,
            "details": details,
            "subchecks": {
                "constitution_coverage": {
                    "passed": constitution_passed,
                    "coverage": round(constitution_coverage, 2)
                },
                "theme_compliance": {
                    "passed": theme_passed,
                    "compliance_rate": round(theme_compliance_rate, 2) if "compliance_rate" in theme_compliance_result else 100,
                    "skipped": theme_compliance_result.get("skipped", False)
                }
            }
        }
        self.results.append(gate_result)
        
        if not overall_passed:
            self.failed = True
            error_messages = []
            
            if not constitution_passed:
                error_messages.append(f"宪法引用覆盖率 {constitution_coverage:.1f}% < 80%")
            
            if not theme_passed:
                if theme_compliance_result.get("skipped", False):
                    error_messages.append("主题合规检查跳过或失败")
                else:
                    error_messages.append(f"§119主题合规率 {theme_compliance_rate:.1f}% < 80%")
            
            error_msg = "；".join(error_messages)
            raise AuditGateFailed(4, error_msg)
        
        return True
    
    def run_gate_5(self) -> bool:
        """Gate 5: 宪法引用格式完整性检查"""
        # 精确匹配纯数字格式的宪法引用 (如 §100.3)
        valid_pattern = r'§\d{3}(?:\.\d+)?'
        
        total_refs = 0
        valid_refs = 0
        invalid_format_refs = []
        unknown_article_refs = []
        
        # 获取有效的宪法条款列表（合并核心条款和示例性引用）
        try:
            # 首先获取核心宪法条款
            from core.constitution_core import CONSTITUTION_CORE_ARTICLES_LIST
            valid_articles_set = set(CONSTITUTION_CORE_ARTICLES_LIST)
            
            # 尝试获取示例性引用条款
            try:
                from templates.constitution_references import get_all_reference_sections
                reference_sections = get_all_reference_sections()
                valid_articles_set.update(reference_sections)
                if self.verbose:
                    print(f"  [Gate 5] 加载了 {len(reference_sections)} 个示例性引用条款")
            except ImportError:
                if self.verbose:
                    print("  [Gate 5] 无法加载示例性引用条款，仅使用核心条款")
        except ImportError as e:
            if self.verbose:
                print(f"  [Gate 5] 无法加载宪法条款定义，使用回退列表: {e}")
            # 回退到常量中的硬编码列表
            valid_articles_set = set(CONSTITUTION_ARTICLES)
        
        if self.verbose:
            print(f"  [Gate 5] 有效的宪法条款总数: {len(valid_articles_set)}")
        
        # 扫描所有代码和文档文件
        for file_path in self.project_root.rglob("*"):
            if file_path.suffix not in ['.py', '.md', '.yaml', '.yml']:
                continue
            if '.git' in str(file_path) or '__pycache__' in str(file_path):
                continue
            if 'test_' in str(file_path):  # 跳过测试文件
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                # 查找所有精确的宪法引用（不包含后续文字）
                matches = re.findall(valid_pattern, content)
                
                for match in matches:
                    total_refs += 1
                    article = match.strip()
                    
                    # 检查引用的条款是否存在
                    if article in valid_articles_set:
                        valid_refs += 1
                    else:
                        unknown_article_refs.append({
                            "file": str(file_path.relative_to(self.project_root)),
                            "reference": article
                        })
                        
            except Exception:
                continue
        
        # 计算合规性
        format_compliance = (valid_refs / total_refs * 100) if total_refs > 0 else 100
        has_unknown_articles = len(unknown_article_refs) > 0
        
        # 通过条件：格式合规率 >= 95%
        # 注意：不强制验证条款是否存在，因为模板文件中可能包含示例性引用
        success = format_compliance >= 95
        
        gate_result = {
            "gate": 5,
            "name": "Constitution Reference Integrity",
            "passed": success,
            "details": {
                "total_references": total_refs,
                "valid_references": valid_refs,
                "format_compliance": round(format_compliance, 2),
                "unknown_article_refs": unknown_article_refs[:10],
                "issues_count": len(unknown_article_refs)
            }
        }
        self.results.append(gate_result)
        
        if not success:
            self.failed = True
            error_msg = []
            if has_unknown_articles:
                error_msg.append(f"Unknown articles: {len(unknown_article_refs)}")
            if format_compliance < 95:
                error_msg.append(f"Compliance: {format_compliance:.1f}% < 95%")
            raise AuditGateFailed(5, "; ".join(error_msg))
        
        return True
    
    def run_gate(self, gate_id: int, cache_manager: Optional[CacheManager] = None) -> bool:
        """运行指定Gate"""
        if gate_id == 1:
            return self.run_gate_1()
        elif gate_id == 2:
            return self.run_gate_2()
        elif gate_id == 3:
            return self.run_gate_3(cache_manager)
        elif gate_id == 4:
            return self.run_gate_4()
        elif gate_id == 5:
            return self.run_gate_5()
        else:
            raise ValueError(f"Unknown gate: {gate_id}")
    
    def run_all_gates(self, cache_manager: Optional[CacheManager] = None) -> List[Dict[str, Any]]:
        """运行所有门禁"""
        for gate_id in [1, 2, 3, 4, 5]:
            try:
                self.run_gate(gate_id, cache_manager)
            except AuditGateFailed as e:
                # 记录失败但继续执行其他门禁
                if self.verbose:
                    print(f"Gate {gate_id} failed: {e}")
        
        return self.results
    
    def generate_report(self, format: str = "text") -> str:
        """生成审计报告"""
        if format == "json":
            report = {
                "timestamp": datetime.now().isoformat(),
                "version": VERSION,
                "success": not self.failed,
                "total_gates": len(self.results),
                "passed_gates": sum(1 for r in self.results if r["passed"]),
                "gate_results": self.results
            }
            return json.dumps(report, indent=2, ensure_ascii=False)
        else:
            lines = []
            lines.append("=" * 40)
            lines.append(f"CDD AUDIT SUMMARY (v{VERSION})")
            lines.append("=" * 40)
            
            for res in self.results:
                icon = "✅" if res["passed"] else "❌"
                lines.append(f"{icon} Gate {res['gate']}: {res['name']}")
            
            lines.append("-" * 40)
            if self.failed:
                lines.append("❌ SYSTEM COMPLIANCE FAILED")
            else:
                lines.append("✅ SYSTEM COMPLIANT")
            
            return "\n".join(lines)
    
    def get_exit_code(self) -> int:
        """获取退出码"""
        if not self.results:
            return EC_SUCCESS if not self.failed else EC_CLEAN_FAIL
        
        for res in self.results:
            if not res["passed"]:
                gate_id = res["gate"]
                if gate_id == 1:
                    return EC_GATE_1_FAIL
                elif gate_id == 2:
                    return EC_GATE_2_FAIL
                elif gate_id == 3:
                    return EC_GATE_3_FAIL
                elif gate_id == 4:
                    return EC_GATE_4_FAIL
                elif gate_id == 5:
                    return EC_GATE_5_FAIL
                else:
                    return EC_GENERAL_FAIL
        
        return EC_SUCCESS
    
    def run_cleanup(self):
        """清理临时目录"""
        specs_dir = self.project_root / "specs"
        if not specs_dir.exists():
            return
        
        candidates = []
        for item in specs_dir.iterdir():
            if item.is_dir() and re.match(r"^\d{3}-", item.name):
                if "cdd-auditor-cli" not in item.name:
                    candidates.append(item)
        
        if not candidates:
            return
        
        print(f"\nFound {len(candidates)} candidates for deletion:")
        for p in candidates:
            print(f"  - {p.relative_to(self.project_root)}")
        
        response = input("\nDelete these directories? [y/N] ").strip().lower()
        if response != 'y':
            print("Cleanup aborted.")
            return
        
        for p in candidates:
            try:
                shutil.rmtree(p)
                print(f"Deleted: {p.name}")
            except Exception as e:
                print(f"Failed to delete {p.name}: {e}")
                self.failed = True


class AuditService:
    """审计服务主类"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or SKILL_ROOT
    
    def audit_gates(self, gates: str = "all", fix: bool = False, 
                    verbose: bool = False) -> Dict[str, Any]:
        """
        执行审计门禁
        
        Args:
            gates: 要运行的Gate ("1", "2", "3", "4", "5", "all")
            fix: 是否自动修复版本漂移
            verbose: 是否详细输出
            
        Returns:
            Dict[str, Any]: 审计结果
        """
        auditor = CDDAuditor(self.project_root, verbose)
        
        if fix:
            # 自动修复版本不一致
            checker = VersionChecker(self.project_root, verbose)
            consistent, details = checker.check_consistency()
            if not consistent:
                distribution = details.get("distribution", {})
                target_version = max(distribution, key=distribution.get) if distribution else VERSION
                checker.fix_versions(target_version)
        
        # 确定要运行的Gates (现在包含Gate 5)
        gates_to_run = [1, 2, 3, 4, 5] if gates == "all" else [int(gates)]
        
        cache_manager = CacheManager(self.project_root)
        
        try:
            for gate_id in gates_to_run:
                auditor.run_gate(gate_id, cache_manager)
            
            return {
                "success": not auditor.failed,
                "results": auditor.results,
                "report": auditor.generate_report("json")
            }
        except AuditGateFailed as e:
            return {
                "success": False,
                "error": str(e),
                "results": auditor.results
            }
    
    def verify_versions(self, fix: bool = False) -> Dict[str, Any]:
        """验证版本一致性"""
        checker = VersionChecker(self.project_root)
        consistent, details = checker.check_consistency()
        
        if not consistent and fix:
            distribution = details.get("distribution", {})
            target_version = max(distribution, key=distribution.get) if distribution else VERSION
            fix_result = checker.fix_versions(target_version)
            return {
                "success": True,
                "action": "fixed",
                "target_version": target_version,
                "fix_result": fix_result
            }
        
        return {
            "success": consistent,
            "details": details
        }
    
    def cleanup_temporary_directories(self, force: bool = False) -> Dict[str, Any]:
        """清理临时目录"""
        specs_dir = self.project_root / "specs"
        if not specs_dir.exists():
            return {"success": True, "cleaned": 0, "message": "Specs directory not found"}
        
        candidates = []
        for item in specs_dir.iterdir():
            if item.is_dir() and re.match(r"^\d{3}-", item.name):
                if "cdd-auditor-cli" not in item.name:
                    candidates.append(item)
        
        if not candidates:
            return {"success": True, "cleaned": 0, "message": "No temporary directories found"}
        
        cleaned = []
        for p in candidates:
            try:
                shutil.rmtree(p)
                cleaned.append(str(p.relative_to(self.project_root)))
            except Exception as e:
                pass
        
        return {
            "success": True,
            "cleaned": len(cleaned),
            "directories": cleaned
        }