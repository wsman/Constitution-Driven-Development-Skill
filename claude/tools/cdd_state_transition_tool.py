#!/usr/bin/env python3
"""
CDD State Transition Tool v2.0.0
================================
Claude Code工具API层，调用services/state_transition_service.py和services/state_validation_service.py。

宪法依据: §102§104§103
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# 处理导入路径
try:
    # 作为模块导入时使用相对导入
    from .tool_registry import BaseTool, cdd_tool
except ImportError:
    # 直接运行脚本时使用绝对导入
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from claude.tools.tool_registry import BaseTool, cdd_tool

# 导入服务层
try:
    from core.state_transition_service import StateTransitionService, create_state_transition_service
    from core.state_validation_service import StateValidationService, create_state_validation_service
    SERVICE_AVAILABLE = True
except ImportError as e:
    SERVICE_AVAILABLE = False
    print(f"❌ 无法导入services层: {e}")
    StateTransitionService = None
    StateValidationService = None


@cdd_tool(name="cdd_state_transition", description="CDD工作流状态转换工具")
class CDDStateTransitionTool(BaseTool):
    """
    CDD工作流状态转换工具API层
    
    支持5状态工作流(A→B→C→D→E)的状态转换和检查点管理
    """
    
    name = "cdd_state_transition"
    description = "CDD State Transition Tool - 管理5状态工作流状态转换"
    version = "2.0.0"
    constitutional_basis = ["§102", "§104", "§103"]
    
    def execute(self, action: str = "transition", **kwargs) -> Dict[str, Any]:
        """
        执行工具主函数
        
        Args:
            action: 操作类型 (transition, get_state, validate, checkpoint)
            target (str): 目标项目目录
            from_state (str): 当前状态 (A-E)
            to_state (str): 目标状态 (A-E)
            note (str): 检查点备注
            force (bool): 是否强制转换
            reason (str): 转换原因
            
        Returns:
            Dict[str, Any]: 执行结果
        """
        if not SERVICE_AVAILABLE:
            return self.create_response(
                success=False,
                error="StateTransitionService not available. Please check services/ directory."
            )
        
        try:
            # 确定目标路径
            target = kwargs.get("target", ".")
            target_path = Path(target).resolve()
            
            # 创建服务实例
            transition_service = create_state_transition_service()
            validation_service = create_state_validation_service()
            
            if action == "transition":
                return self._perform_transition(
                    transition_service, validation_service, target_path, **kwargs
                )
            elif action == "get_state":
                return self._get_current_state(transition_service, target_path)
            elif action == "validate":
                return self._validate_transition(
                    transition_service, validation_service, target_path, **kwargs
                )
            elif action == "checkpoint":
                return self._create_checkpoint(transition_service, target_path, **kwargs)
            else:
                return {
                    "success": False,
                    "error": f"无效的操作类型: {action}",
                    "valid_actions": ["transition", "get_state", "validate", "checkpoint"]
                }
                
        except Exception as e:
            return self.create_response(
                success=False,
                error=f"Tool execution failed: {str(e)}"
            )
    
    def _perform_transition(
        self,
        transition_service: StateTransitionService,
        validation_service: StateValidationService,
        target_path: Path,
        **kwargs
    ) -> Dict[str, Any]:
        """执行状态转换"""
        from_state = kwargs.get("from_state")
        to_state = kwargs.get("to_state")
        force = kwargs.get("force", False)
        reason = kwargs.get("reason", "manual")
        
        if not to_state:
            return {
                "success": False,
                "error": "缺少目标状态参数 (to_state)",
                "required": ["to_state"]
            }
        
        # 执行转换
        result = transition_service.perform_transition(
            target_path=target_path,
            to_state=to_state,
            from_state=from_state,
            force=force,
            reason=reason
        )
        
        # 添加额外信息
        if result.get("success", False):
            result.update({
                "action": "transition",
                "target": str(target_path),
                "tool_version": self.version
            })
        
        return result
    
    def _get_current_state(
        self,
        transition_service: StateTransitionService,
        target_path: Path
    ) -> Dict[str, Any]:
        """获取当前状态"""
        result = transition_service.get_current_state(target_path)
        
        # 添加额外信息
        if result.get("success", False):
            result.update({
                "action": "get_state",
                "target": str(target_path),
                "tool_version": self.version
            })
        
        return result
    
    def _validate_transition(
        self,
        transition_service: StateTransitionService,
        validation_service: StateValidationService,
        target_path: Path,
        **kwargs
    ) -> Dict[str, Any]:
        """验证状态转换"""
        from_state = kwargs.get("from_state", "A")
        to_state = kwargs.get("to_state")
        force = kwargs.get("force", False)
        
        if not to_state:
            return {
                "success": False,
                "error": "缺少目标状态参数 (to_state)"
            }
        
        # 基本转换验证
        validation = transition_service.validate_transition(
            from_state=from_state,
            to_state=to_state,
            target_path=target_path,
            force=force
        )
        
        if validation["valid"]:
            # 状态特定条件验证
            state_validation = validation_service.validate_state_specific_conditions(
                from_state=from_state,
                to_state=to_state,
                target_path=target_path
            )
            
            if not state_validation["success"]:
                return state_validation
        
        return validation
    
    def _create_checkpoint(
        self,
        transition_service: StateTransitionService,
        target_path: Path,
        **kwargs
    ) -> Dict[str, Any]:
        """创建检查点"""
        note = kwargs.get("note", "")
        
        result = transition_service.create_checkpoint(
            target_path=target_path,
            note=note
        )
        
        # 添加额外信息
        if result.get("success", False):
            result.update({
                "action": "checkpoint",
                "target": str(target_path),
                "tool_version": self.version
            })
        
        return result


def execute_tool(**kwargs) -> Dict[str, Any]:
    """
    Claude Code工具执行接口
    
    Args:
        target (str): 目标项目目录
        from_state (str): 当前状态 (A-E)
        to_state (str): 目标状态 (A-E)
        action (str): 操作类型
        
    Returns:
        Dict[str, Any]: 执行结果
    """
    tool = CDDStateTransitionTool()
    return tool.execute(**kwargs)


if __name__ == "__main__":
    # CLI测试接口
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="CDD State Transition Tool CLI")
    parser.add_argument("--action", choices=["transition", "get_state", "validate", "checkpoint"], 
                       default="get_state", help="操作类型")
    parser.add_argument("--target", default=".", help="目标目录")
    parser.add_argument("--from-state", help="当前状态")
    parser.add_argument("--to-state", help="目标状态")
    parser.add_argument("--note", help="检查点备注")
    parser.add_argument("--force", action="store_true", help="强制转换")
    
    args = parser.parse_args()
    
    tool = CDDStateTransitionTool()
    result = tool.execute(
        action=args.action,
        target=args.target,
        from_state=args.from_state,
        to_state=args.to_state,
        note=args.note,
        force=args.force
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))