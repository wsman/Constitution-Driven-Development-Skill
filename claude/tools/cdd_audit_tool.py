#!/usr/bin/env python3
"""
CDD Audit Tool (cdd_audit_tool.py) v2.0.0
=========================================
Claude Code审计工具API层，调用services/audit_service.py。

宪法依据: §101§102§300.3
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from .tool_registry import BaseTool, cdd_tool

# 导入新的服务层
try:
    from core.audit_service import AuditService
    SERVICE_AVAILABLE = True
except ImportError:
    SERVICE_AVAILABLE = False
    AuditService = None


@cdd_tool(name="cdd_audit", description="CDD宪法审计工具")
class CDDAuditTool(BaseTool):
    """CDD宪法审计工具API层"""
    
    name = "cdd_audit"
    description = "执行CDD宪法审计（Gate 1-4）"
    version = "2.0.0"
    constitutional_basis = ["§101", "§102", "§300.3", "§310"]
    
    def execute(self, gates: str = "all", fix: bool = False, target: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        执行CDD宪法审计
        
        Args:
            gates: 审计门禁（1-4或all）
            fix: 是否自动修复版本漂移
            target: 目标项目路径（可选）
            
        Returns:
            Dict[str, Any]: 审计结果
        """
        try:
            # 确定目标路径
            project_root = Path(target).resolve() if target else self.project_root
            
            if not SERVICE_AVAILABLE:
                return self.create_response(
                    success=False,
                    error="AuditService not available. Please check services/ directory."
                )
            
            # 创建审计服务实例
            audit_service = AuditService(project_root)
            
            # 执行审计
            result = audit_service.audit_gates(
                gates=gates,
                fix=fix,
                verbose=kwargs.get("verbose", False)
            )
            
            # 添加额外信息
            result.update({
                "gates": gates,
                "fix_applied": fix,
                "target": str(project_root),
                "tool_version": self.version
            })
            
            return result
            
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Audit execution failed: {str(e)}"
            )
    
    def get_gate_status(self, gate: str = "all") -> Dict[str, Any]:
        """
        获取指定门禁的状态
        
        Args:
            gate: 门禁编号（1-4或all）
            
        Returns:
            Dict[str, Any]: 门禁状态信息
        """
        descriptions = {
            "1": "版本一致性检查 (§100.3)",
            "2": "行为验证检查 (§300.3)",
            "3": "熵值监控检查 (§102)",
            "4": "语义审计检查 (§101, §300.5)",
            "all": "完整宪法审计 (Gate 1-4)"
        }
        
        basis_map = {
            "1": ["§100.3"],
            "2": ["§300.3"],
            "3": ["§102"],
            "4": ["§101", "§300.5"],
            "all": ["§100.3", "§300.3", "§102", "§101", "§300.5"]
        }
        
        return {
            "success": True,
            "gate": gate,
            "status": "available",
            "description": descriptions.get(gate, "未知门禁"),
            "constitutional_basis": basis_map.get(gate, []),
            "tool_version": self.version
        }


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CDD Audit Tool CLI")
    
    parser.add_argument("--gates", type=str, default="all", help="Audit gates (1-4 or all)")
    parser.add_argument("--fix", action="store_true", help="Auto-fix version drift")
    parser.add_argument("--target", type=str, help="Target project path")
    parser.add_argument("--status", action="store_true", help="Show gate status")
    parser.add_argument("--gate", type=str, help="Get specific gate info")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    tool = CDDAuditTool()
    
    if args.status:
        gate = args.gate or "all"
        result = tool.get_gate_status(gate)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.gate:
        # 获取单个门禁信息
        result = tool.get_gate_status(args.gate)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        # 执行审计
        result = tool.execute(
            gates=args.gates,
            fix=args.fix,
            target=args.target,
            verbose=args.verbose
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()