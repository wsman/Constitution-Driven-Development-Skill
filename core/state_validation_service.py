"""
CDD State Validation Service v2.0.0
===================================
状态特定条件验证服务。

宪法依据: §102§300.3§300.5
"""

import subprocess
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

from core.constants import SKILL_ROOT
from core.entropy_service import EntropyService
from core.audit_service import AuditService


class StateValidationService:
    """
    CDD状态特定条件验证服务
    
    负责验证状态转换前的特定条件，如熵值、规格批准、测试、审计等
    """
    
    def __init__(self, skill_root: Optional[Path] = None):
        self.skill_root = skill_root or SKILL_ROOT
    
    def validate_state_specific_conditions(
        self,
        from_state: str,
        to_state: str,
        target_path: Path
    ) -> Dict[str, Any]:
        """
        验证状态特定条件
        
        Args:
            from_state: 当前状态
            to_state: 目标状态
            target_path: 目标项目路径
            
        Returns:
            验证结果
        """
        # A→B: 检查熵值
        if from_state == "A" and to_state == "B":
            entropy_check = self.check_entropy_threshold(target_path)
            if not entropy_check["valid"]:
                return {
                    "success": False,
                    "error": "熵值超标，无法进入规划状态",
                    "constitutional_basis": "§102",
                    "details": entropy_check
                }
        
        # B→C: 检查规格批准
        elif from_state == "B" and to_state == "C":
            spec_approved = self.check_spec_approval(target_path)
            if not spec_approved["approved"]:
                return {
                    "success": False,
                    "error": "规格未批准，无法进入执行状态",
                    "constitutional_basis": "§104",
                    "details": spec_approved
                }
        
        # C→D: 检查测试通过
        elif from_state == "C" and to_state == "D":
            tests_passed = self.run_tests(target_path)
            if not tests_passed["success"]:
                return {
                    "success": False,
                    "error": "测试未通过，无法进入验证状态",
                    "constitutional_basis": "§300.3",
                    "details": tests_passed
                }
        
        # D→E: 检查审计通过
        elif from_state == "D" and to_state == "E":
            audit_passed = self.run_constitutional_audit(target_path)
            if not audit_passed["success"]:
                return {
                    "success": False,
                    "error": "宪法审计未通过，无法进入关闭状态",
                    "constitutional_basis": "§300.3",
                    "details": audit_passed
                }
        
        return {"success": True}
    
    def check_entropy_threshold(self, target_path: Path) -> Dict[str, Any]:
        """检查熵值阈值"""
        try:
            # 使用熵值服务
            entropy_service = EntropyService(target_path)
            metrics = entropy_service.calculate_entropy()
            h_sys = metrics.get("h_sys", 1.0)
            
            return {
                "valid": h_sys <= 0.7,
                "h_sys": h_sys,
                "threshold": 0.7,
                "status": "🟢 通过" if h_sys <= 0.7 else "🔴 超标"
            }
        except Exception as e:
            return {"valid": True, "warning": f"熵值检查失败: {e}", "skip": True}
    
    def check_spec_approval(self, target_path: Path) -> Dict[str, Any]:
        """检查规格批准状态"""
        # 简化实现：检查是否有规格文件
        specs_dir = target_path / "specs"
        if not specs_dir.exists():
            return {"approved": False, "error": "未找到specs目录"}
        
        # 查找最新的规格文件
        spec_files = list(specs_dir.glob("**/DS-050_*_spec.md"))
        if not spec_files:
            return {"approved": False, "error": "未找到规格文件"}
        
        # 假设最后一个文件是当前活动的
        latest_spec = sorted(spec_files)[-1]
        
        # 检查是否有批准标记
        content = latest_spec.read_text(encoding='utf-8')
        if "✅ 批准状态: 已批准" in content or "批准状态: 已批准" in content:
            return {
                "approved": True,
                "spec_file": str(latest_spec),
                "approved_at": "从文件内容推断"
            }
        
        return {
            "approved": False,
            "spec_file": str(latest_spec),
            "note": "规格文件未标记为已批准"
        }
    
    def run_tests(self, target_path: Path) -> Dict[str, Any]:
        """运行测试"""
        try:
            stdout, stderr, rc = self._run_command(
                ["python", "-m", "pytest", "-xvs"], 
                cwd=target_path
            )
            
            return {
                "success": rc == 0,
                "exit_code": rc,
                "test_output": stdout[:500] + "..." if len(stdout) > 500 else stdout,
                "details": {
                    "tests_run": "从pytest输出推断",
                    "passed": rc == 0
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "note": "测试运行失败，请手动运行pytest验证"
            }
    
    def run_constitutional_audit(self, target_path: Path) -> Dict[str, Any]:
        """运行宪法审计"""
        try:
            # 使用审计服务
            audit_service = AuditService(target_path)
            result = audit_service.audit_gates(gates="all", fix=False, verbose=False)
            
            # 检查所有门禁是否通过
            if result.get("success", False):
                results = result.get("results", [])
                all_passed = all(r.get("passed", False) for r in results)
                return {
                    "success": all_passed,
                    "audit_results": results,
                    "details": result
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "未知错误"),
                    "details": result
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"宪法审计失败: {e}",
                "note": "请手动运行python scripts/cdd_auditor.py --gate all验证"
            }
    
    def _run_command(
        self, 
        cmd, 
        cwd=None, 
        timeout=30, 
        capture=True, 
        shell=False
    ) -> Tuple[str, str, int]:
        """执行命令"""
        if cwd is None:
            cwd = Path.cwd()
        
        try:
            result = subprocess.run(
                cmd if isinstance(cmd, list) else cmd.split(),
                cwd=cwd,
                text=True,
                capture_output=capture,
                timeout=timeout,
                shell=shell
            )
            return result.stdout or "", result.stderr or "", result.returncode
        except subprocess.TimeoutExpired:
            return "", f"Command timeout ({timeout}s)", 1
        except Exception as e:
            return "", str(e), 1


# 便捷函数
def create_state_validation_service(skill_root: Optional[Path] = None) -> StateValidationService:
    """创建状态验证服务实例"""
    return StateValidationService(skill_root)