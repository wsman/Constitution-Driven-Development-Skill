"""
CDD State Transition Service v2.0.0
===================================
状态转换核心业务逻辑服务。

宪法依据: §102§104§103
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from core.constants import SKILL_ROOT
from utils.file_utils import read_json, write_json


@dataclass
class StateTransition:
    """状态转换数据类"""
    from_state: str
    to_state: str
    timestamp: str
    reason: str
    target_path: str
    
    def to_dict(self) -> dict:
        return {
            "from_state": self.from_state,
            "to_state": self.to_state,
            "timestamp": self.timestamp,
            "reason": self.reason,
            "target_path": self.target_path
        }


@dataclass
class StateCheckpoint:
    """状态检查点数据类"""
    checkpoint_id: str
    state: str
    timestamp: str
    note: str
    state_data: dict
    
    def to_dict(self) -> dict:
        return {
            "checkpoint_id": self.checkpoint_id,
            "state": self.state,
            "timestamp": self.timestamp,
            "note": self.note,
            "state_data": self.state_data
        }


class StateTransitionService:
    """
    CDD状态转换核心业务逻辑服务
    
    负责管理5状态工作流(A→B→C→D→E)的状态转换和检查点管理
    """
    
    # 定义状态转换规则
    VALID_TRANSITIONS = {
        "A": ["B"],  # Intake → Plan
        "B": ["C"],  # Plan → Execute (需要批准)
        "C": ["D"],  # Execute → Verify (需要测试通过)
        "D": ["E", "C"],  # Verify → Close 或 失败返回Execute
        "E": ["A"]  # Close → 重新开始
    }
    
    # 状态描述
    STATE_DESCRIPTIONS = {
        "A": "Intake (接收) - 加载项目上下文，明确任务",
        "B": "Plan (规划) - 生成T2规格文档(DS-050/051)，等待批准",
        "C": "Execute (执行) - 实现已批准的T2规格",
        "D": "Verify (验证) - 执行宪法审计，验证实现",
        "E": "Close (关闭) - 完成工作流，更新上下文"
    }
    
    def __init__(self, skill_root: Optional[Path] = None):
        self.skill_root = skill_root or SKILL_ROOT
    
    def perform_transition(
        self, 
        target_path: Path, 
        to_state: str, 
        from_state: Optional[str] = None,
        force: bool = False,
        reason: str = "manual"
    ) -> Dict[str, Any]:
        """
        执行状态转换
        
        Args:
            target_path: 目标项目路径
            to_state: 目标状态
            from_state: 当前状态（如未提供，从状态文件读取）
            force: 是否强制转换
            reason: 转换原因
            
        Returns:
            转换结果
        """
        # 获取当前状态
        current_state = self.read_state(target_path)
        if not from_state:
            from_state = current_state.get("state", "A")
        
        # 验证基本转换规则
        validation = self.validate_transition_internal(
            from_state, to_state, target_path, force
        )
        
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["error"],
                "details": validation.get("details", {})
            }
        
        # 执行转换
        result = self.execute_state_transition(from_state, to_state, target_path)
        
        if result["success"]:
            # 更新状态
            new_state_data = {
                "state": to_state,
                "previous_state": from_state,
                "transition_timestamp": datetime.now().isoformat(),
                "transition_reason": reason
            }
            
            # 合并现有数据
            if "state" in current_state:
                new_state_data["history"] = current_state.get("history", [])
                new_state_data["history"].append({
                    "from_state": from_state,
                    "to_state": to_state,
                    "timestamp": new_state_data["transition_timestamp"],
                    "reason": new_state_data["transition_reason"]
                })
            
            self.write_state(target_path, new_state_data)
            
            return {
                "success": True,
                "transition": f"{from_state} → {to_state}",
                "from_state": from_state,
                "to_state": to_state,
                "state_description": self.STATE_DESCRIPTIONS.get(to_state),
                "timestamp": new_state_data["transition_timestamp"],
                "details": result.get("details", {})
            }
        else:
            return result
    
    def get_current_state(self, target_path: Path) -> Dict[str, Any]:
        """获取当前状态"""
        state_data = self.read_state(target_path)
        
        return {
            "success": True,
            "current_state": state_data.get("state", "A"),
            "state_description": self.STATE_DESCRIPTIONS.get(state_data.get("state", "A"), ""),
            "state_data": state_data,
            "valid_next_states": self.VALID_TRANSITIONS.get(state_data.get("state", "A"), [])
        }
    
    def validate_transition(
        self, 
        from_state: str, 
        to_state: str, 
        target_path: Path,
        force: bool = False
    ) -> Dict[str, Any]:
        """验证状态转换"""
        validation = self.validate_transition_internal(
            from_state, to_state, target_path, force
        )
        
        return validation
    
    def create_checkpoint(
        self, 
        target_path: Path, 
        note: str = ""
    ) -> Dict[str, Any]:
        """创建检查点"""
        state_data = self.read_state(target_path)
        
        # 构建检查点数据
        checkpoint_data = {
            "checkpoint_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "state": state_data.get("state", "A"),
            "timestamp": datetime.now().isoformat(),
            "note": note,
            "state_data": state_data
        }
        
        # 保存检查点
        checkpoints_dir = target_path / ".cdd_checkpoints"
        checkpoints_dir.mkdir(exist_ok=True)
        
        checkpoint_file = checkpoints_dir / f"{checkpoint_data['checkpoint_id']}.json"
        write_json(checkpoint_file, checkpoint_data)
        
        return {
            "success": True,
            "checkpoint_id": checkpoint_data["checkpoint_id"],
            "state": checkpoint_data["state"],
            "timestamp": checkpoint_data["timestamp"],
            "note": checkpoint_data["note"],
            "checkpoint_file": str(checkpoint_file)
        }
    
    def validate_transition_internal(
        self, 
        from_state: str, 
        to_state: str, 
        target_path: Path,
        force: bool = False
    ) -> Dict[str, Any]:
        """内部验证转换"""
        # 基本验证
        if from_state not in ["A", "B", "C", "D", "E"]:
            return {
                "valid": False,
                "error": f"无效的当前状态: {from_state}",
                "valid_states": ["A", "B", "C", "D", "E"]
            }
        
        if to_state not in ["A", "B", "C", "D", "E"]:
            return {
                "valid": False,
                "error": f"无效的目标状态: {to_state}",
                "valid_states": ["A", "B", "C", "D", "E"]
            }
        
        # 检查转换规则
        valid_next_states = self.VALID_TRANSITIONS.get(from_state, [])
        if to_state not in valid_next_states and not force:
            return {
                "valid": False,
                "error": f"无效的状态转换: {from_state} → {to_state}",
                "valid_transitions": valid_next_states,
                "description": self.STATE_DESCRIPTIONS.get(from_state)
            }
        
        return {
            "valid": True,
            "from_state": from_state,
            "to_state": to_state,
            "description": f"{self.STATE_DESCRIPTIONS.get(from_state)} → {self.STATE_DESCRIPTIONS.get(to_state)}"
        }
    
    def execute_state_transition(
        self, 
        from_state: str, 
        to_state: str, 
        target_path: Path
    ) -> Dict[str, Any]:
        """执行状态转换逻辑"""
        if from_state == "A" and to_state == "B":
            # 触发规格生成
            return self._trigger_spec_generation(target_path)
        
        elif from_state == "B" and to_state == "C":
            # 标记规格为已批准
            return self._mark_spec_approved(target_path)
        
        elif from_state == "D" and to_state == "E":
            # 更新活动上下文
            return self._update_active_context(target_path)
        
        # 默认转换（无特殊逻辑）
        return {
            "success": True,
            "details": {
                "transition": f"{from_state} → {to_state}",
                "action": "状态标记更新"
            }
        }
    
    def read_state(self, target_path: Path) -> Dict[str, Any]:
        """读取状态"""
        state_file = target_path / ".cdd_state.json"
        active_context = target_path / "memory_bank" / "t0_core" / "active_context.md"
        
        state_data = {"state": "A", "timestamp": datetime.now().isoformat()}
        
        # 尝试从状态文件读取
        if state_file.exists():
            data = read_json(state_file)
            if data:
                state_data.update(data)
        
        # 尝试从active_context.md读取
        elif active_context.exists():
            content = active_context.read_text(encoding='utf-8')
            import re
            match = re.search(r"当前状态:\s*(\w+)", content)
            if match:
                state_data["state"] = match.group(1)
                # 提取更多上下文信息
                match = re.search(r"最近宪法事件:\s*(.+?)(?:\n|$)", content)
                if match:
                    state_data["last_event"] = match.group(1)
        
        return state_data
    
    def write_state(self, target_path: Path, state_data: Dict[str, Any]):
        """写入状态"""
        state_file = target_path / ".cdd_state.json"
        write_json(state_file, state_data)
        
        # 同时更新active_context.md
        active_context = target_path / "memory_bank" / "t0_core" / "active_context.md"
        if active_context.exists():
            content = active_context.read_text(encoding='utf-8')
            import re
            
            # 更新当前状态
            if "state" in state_data:
                new_state = state_data["state"]
                content = re.sub(
                    r"当前状态:\s*\w+",
                    f"当前状态: {new_state}",
                    content
                )
            
            # 添加状态转换记录
            if "transition_timestamp" in state_data and "transition_reason" in state_data:
                transition_record = f"\n- {state_data['transition_timestamp']}: 状态转换 {state_data.get('previous_state', '?')} → {state_data.get('state', '?')} ({state_data['transition_reason']})"
                
                # 找到最近宪法事件部分
                if "最近宪法事件:" in content:
                    content = content.replace(
                        "最近宪法事件:",
                        f"最近宪法事件:{transition_record}"
                    )
            
            active_context.write_text(content, encoding='utf-8')
    
    # 状态转换执行方法
    def _trigger_spec_generation(self, target_path: Path) -> Dict[str, Any]:
        """触发规格生成"""
        return {
            "success": True,
            "details": {
                "action": "建议使用 python scripts/cdd_feature.py create 生成规格",
                "next_step": "生成DS-050规格文档并等待批准"
            }
        }
    
    def _mark_spec_approved(self, target_path: Path) -> Dict[str, Any]:
        """标记规格为已批准"""
        return {
            "success": True,
            "details": {
                "action": "手动标记规格为已批准",
                "note": "在DS-050文件中添加'✅ 批准状态: 已批准'"
            }
        }
    
    def _update_active_context(self, target_path: Path) -> Dict[str, Any]:
        """更新活动上下文"""
        return {
            "success": True,
            "details": {
                "action": "更新active_context.md",
                "note": "记录完成事件和熵值变化"
            }
        }


# 便捷函数
def create_state_transition_service(skill_root: Optional[Path] = None) -> StateTransitionService:
    """创建状态转换服务实例"""
    return StateTransitionService(skill_root)