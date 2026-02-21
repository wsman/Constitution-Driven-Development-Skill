#!/usr/bin/env python3
"""
Unit tests for State Transition Service (state_transition_service.py)
Part of CDD P1 Test Coverage Improvement Plan

宪法依据: §103§104
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

import pytest

from core.state_transition_service import (
    StateTransitionService,
    create_state_transition_service,
    StateTransition,
    StateCheckpoint
)


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def state_service():
    """Create StateTransitionService instance"""
    return StateTransitionService()


@pytest.fixture
def mock_state_file():
    """Mock state file content"""
    return {
        "state": "A",
        "timestamp": "2026-02-20T10:00:00",
        "history": []
    }


@pytest.fixture
def mock_active_context():
    """Mock active_context.md content"""
    return """# Active Context

当前状态: A
最近宪法事件: 项目初始化
熵值状态: 优秀 (H_sys = 0.21)
"""


# -----------------------------------------------------------------------------
# Core Class Tests
# -----------------------------------------------------------------------------

class TestStateTransitionClass:
    """Test StateTransition and StateCheckpoint dataclasses"""
    
    def test_state_transition_creation(self):
        """Test StateTransition dataclass creation"""
        transition = StateTransition(
            from_state="A",
            to_state="B",
            timestamp="2026-02-20T10:00:00",
            reason="测试转换",
            target_path="/test/project"
        )
        
        assert transition.from_state == "A"
        assert transition.to_state == "B"
        assert transition.reason == "测试转换"
        assert transition.to_dict() == {
            "from_state": "A",
            "to_state": "B",
            "timestamp": "2026-02-20T10:00:00",
            "reason": "测试转换",
            "target_path": "/test/project"
        }
    
    def test_state_checkpoint_creation(self):
        """Test StateCheckpoint dataclass creation"""
        checkpoint = StateCheckpoint(
            checkpoint_id="20260220_100000",
            state="A",
            timestamp="2026-02-20T10:00:00",
            note="测试检查点",
            state_data={"state": "A"}
        )
        
        assert checkpoint.checkpoint_id == "20260220_100000"
        assert checkpoint.state == "A"
        assert checkpoint.note == "测试检查点"
        assert checkpoint.to_dict() == {
            "checkpoint_id": "20260220_100000",
            "state": "A",
            "timestamp": "2026-02-20T10:00:00",
            "note": "测试检查点",
            "state_data": {"state": "A"}
        }


# -----------------------------------------------------------------------------
# StateTransitionService Tests
# -----------------------------------------------------------------------------

class TestStateTransitionService:
    """Test StateTransitionService core functionality"""
    
    def test_initialization(self):
        """Test service initialization"""
        service = StateTransitionService()
        assert service.skill_root is not None
        assert hasattr(service, "VALID_TRANSITIONS")
        assert hasattr(service, "STATE_DESCRIPTIONS")
    
    def test_valid_transitions_structure(self, state_service):
        """Test valid transitions are properly defined"""
        assert "A" in state_service.VALID_TRANSITIONS
        assert "B" in state_service.VALID_TRANSITIONS
        assert "C" in state_service.VALID_TRANSITIONS
        assert "D" in state_service.VALID_TRANSITIONS
        assert "E" in state_service.VALID_TRANSITIONS
        
        # Check specific transitions
        assert state_service.VALID_TRANSITIONS["A"] == ["B"]
        assert "C" in state_service.VALID_TRANSITIONS["B"]
        assert "D" in state_service.VALID_TRANSITIONS["C"]
        assert set(state_service.VALID_TRANSITIONS["D"]) == {"E", "C"}
        assert state_service.VALID_TRANSITIONS["E"] == ["A"]
    
    def test_state_descriptions(self, state_service):
        """Test state descriptions are properly defined"""
        assert state_service.STATE_DESCRIPTIONS["A"] == "Intake (接收) - 加载项目上下文，明确任务"
        assert state_service.STATE_DESCRIPTIONS["B"] == "Plan (规划) - 生成T2规格文档(DS-050/051)，等待批准"
        assert state_service.STATE_DESCRIPTIONS["C"] == "Execute (执行) - 实现已批准的T2规格"
        assert state_service.STATE_DESCRIPTIONS["D"] == "Verify (验证) - 执行宪法审计，验证实现"
        assert state_service.STATE_DESCRIPTIONS["E"] == "Close (关闭) - 完成工作流，更新上下文"
    
    @patch("utils.file_utils.read_json")
    def test_get_current_state_from_file(self, mock_read_json, state_service, temp_project_dir):
        """Test get_current_state with existing state file"""
        # Create state file first
        state_file = temp_project_dir / ".cdd_state.json"
        state_file.write_text('{"state": "B", "timestamp": "2026-02-20T10:00:00"}')
        
        result = state_service.get_current_state(temp_project_dir)
        
        assert result["success"] is True
        assert result["current_state"] == "B"
        assert result["state_description"] == state_service.STATE_DESCRIPTIONS["B"]
        assert "state_data" in result
        assert result["valid_next_states"] == ["C"]
        # Note: read_json may not be called if service reads file directly
    
    @patch("core.state_transition_service.Path.exists")
    @patch("core.state_transition_service.read_json")
    def test_get_current_state_default(self, mock_read_json, mock_exists, state_service, temp_project_dir):
        """Test get_current_state with no state file (defaults to A)"""
        mock_read_json.return_value = None
        mock_exists.return_value = False
        
        result = state_service.get_current_state(temp_project_dir)
        
        assert result["success"] is True
        assert result["current_state"] == "A"
        assert result["state_description"] == state_service.STATE_DESCRIPTIONS["A"]
        assert result["valid_next_states"] == ["B"]
    
    def test_validate_transition_valid(self, state_service, temp_project_dir):
        """Test valid transition validation"""
        result = state_service.validate_transition(
            from_state="A",
            to_state="B",
            target_path=temp_project_dir
        )
        
        assert result["valid"] is True
        assert result["from_state"] == "A"
        assert result["to_state"] == "B"
        assert "description" in result
    
    def test_validate_transition_invalid(self, state_service, temp_project_dir):
        """Test invalid transition validation"""
        result = state_service.validate_transition(
            from_state="A",
            to_state="C",  # Invalid: A can only go to B
            target_path=temp_project_dir
        )
        
        assert result["valid"] is False
        assert "invalid" in result["error"].lower() or "无效" in result["error"]
        assert "valid_transitions" in result
    
    def test_validate_transition_invalid_state(self, state_service, temp_project_dir):
        """Test validation with invalid state code"""
        result = state_service.validate_transition(
            from_state="X",  # Invalid state
            to_state="B",
            target_path=temp_project_dir
        )
        
        assert result["valid"] is False
        assert "无效" in result["error"] or "invalid" in result["error"].lower()
        assert "valid_states" in result
    
    def test_validate_transition_force_mode(self, state_service, temp_project_dir):
        """Test validation with force mode (bypasses transition rules)"""
        result = state_service.validate_transition(
            from_state="A",
            to_state="C",  # Normally invalid
            target_path=temp_project_dir,
            force=True
        )
        
        # With force=True, even invalid transitions should pass basic validation
        # (though they still need valid state codes)
        assert result["valid"] is True  # Because states A and C are valid codes
    
    @patch("core.state_transition_service.StateTransitionService.read_state")
    @patch("core.state_transition_service.StateTransitionService.write_state")
    @patch("core.state_transition_service.StateTransitionService.execute_state_transition")
    def test_perform_transition_success(
        self, mock_execute, mock_write, mock_read, state_service, temp_project_dir
    ):
        """Test successful state transition"""
        mock_read.return_value = {"state": "A"}
        mock_execute.return_value = {"success": True, "details": {}}
        
        result = state_service.perform_transition(
            target_path=temp_project_dir,
            to_state="B",
            from_state="A",
            reason="测试转换"
        )
        
        assert result["success"] is True
        assert result["transition"] == "A → B"
        assert result["from_state"] == "A"
        assert result["to_state"] == "B"
        assert "timestamp" in result
        assert mock_write.called
    
    @patch("core.state_transition_service.StateTransitionService.read_state")
    def test_perform_transition_invalid(
        self, mock_read, state_service, temp_project_dir
    ):
        """Test failed state transition (invalid transition)"""
        mock_read.return_value = {"state": "A"}
        
        result = state_service.perform_transition(
            target_path=temp_project_dir,
            to_state="C",  # Invalid: A → C
            from_state="A",
            reason="测试转换"
        )
        
        assert result["success"] is False
        assert "error" in result
        assert "details" in result
    
    @patch("core.state_transition_service.StateTransitionService.read_state")
    @patch("core.state_transition_service.StateTransitionService.execute_state_transition")
    def test_perform_transition_execution_failed(
        self, mock_execute, mock_read, state_service, temp_project_dir
    ):
        """Test transition where execution logic fails"""
        mock_read.return_value = {"state": "A"}
        mock_execute.return_value = {
            "success": False,
            "error": "Execution failed"
        }
        
        result = state_service.perform_transition(
            target_path=temp_project_dir,
            to_state="B",
            from_state="A"
        )
        
        assert result["success"] is False
        assert "error" in result
    
    @patch("core.state_transition_service.write_json")
    def test_create_checkpoint(self, mock_write_json, state_service, temp_project_dir):
        """Test checkpoint creation"""
        # Create state file first
        state_file = temp_project_dir / ".cdd_state.json"
        state_file.write_text(json.dumps({"state": "B", "timestamp": "2026-02-20T10:00:00"}))
        
        result = state_service.create_checkpoint(
            target_path=temp_project_dir,
            note="测试检查点"
        )
        
        assert result["success"] is True
        assert "checkpoint_id" in result
        assert result["state"] == "B"
        assert result["note"] == "测试检查点"
        assert "checkpoint_file" in result
        assert mock_write_json.called
    
    def test_create_checkpoint_no_state_file(self, state_service, temp_project_dir):
        """Test checkpoint creation with no state file (defaults to A)"""
        result = state_service.create_checkpoint(
            target_path=temp_project_dir,
            note="测试检查点"
        )
        
        assert result["success"] is True
        assert result["state"] == "A"  # Default state
    
    def test_read_state_from_file(self, state_service, temp_project_dir):
        """Test reading state from existing state file"""
        state_data = {
            "state": "C",
            "timestamp": "2026-02-20T10:00:00",
            "history": [
                {"from_state": "A", "to_state": "B", "timestamp": "2026-02-20T09:00:00"}
            ]
        }
        
        state_file = temp_project_dir / ".cdd_state.json"
        state_file.write_text(json.dumps(state_data))
        
        result = state_service.read_state(temp_project_dir)
        
        assert result["state"] == "C"
        assert result["timestamp"] == "2026-02-20T10:00:00"
        assert len(result["history"]) == 1
    
    def test_read_state_from_active_context(self, state_service, temp_project_dir):
        """Test reading state from active_context.md"""
        # Create memory_bank/t0_core directory and active_context.md
        core_dir = temp_project_dir / "memory_bank" / "t0_core"
        core_dir.mkdir(parents=True, exist_ok=True)
        
        active_context = core_dir / "active_context.md"
        active_context.write_text("当前状态: B\n最近宪法事件: 测试", encoding='utf-8')
        
        result = state_service.read_state(temp_project_dir)
        
        assert result["state"] == "B"
    
    def test_read_state_default(self, state_service, temp_project_dir):
        """Test reading state when no files exist (default to A)"""
        # Ensure no files exist
        result = state_service.read_state(temp_project_dir)
        
        assert result["state"] == "A"
        assert "timestamp" in result
    
    def test_write_state(self, state_service, temp_project_dir):
        """Test writing state data"""
        # Create memory_bank/t0_core directory and active_context.md
        core_dir = temp_project_dir / "memory_bank" / "t0_core"
        core_dir.mkdir(parents=True, exist_ok=True)
        
        active_context = core_dir / "active_context.md"
        active_context.write_text("当前状态: A\n最近宪法事件: 旧事件", encoding='utf-8')
        
        state_data = {
            "state": "B",
            "previous_state": "A",
            "transition_timestamp": "2026-02-20T10:00:00",
            "transition_reason": "测试"
        }
        
        state_service.write_state(temp_project_dir, state_data)
        
        # Verify state file was created
        state_file = temp_project_dir / ".cdd_state.json"
        assert state_file.exists()
        
        # Verify content
        content = json.loads(state_file.read_text(encoding='utf-8'))
        assert content["state"] == "B"
        assert content["previous_state"] == "A"
        assert content["transition_reason"] == "测试"
    
    def test_execute_state_transition_a_to_b(self, state_service, temp_project_dir):
        """Test execution logic for A→B transition"""
        result = state_service.execute_state_transition("A", "B", temp_project_dir)
        
        assert result["success"] is True
        assert "details" in result
        assert "建议使用" in result["details"]["action"]
    
    def test_execute_state_transition_b_to_c(self, state_service, temp_project_dir):
        """Test execution logic for B→C transition"""
        result = state_service.execute_state_transition("B", "C", temp_project_dir)
        
        assert result["success"] is True
        assert "手动标记规格为已批准" in result["details"]["action"]
    
    def test_execute_state_transition_d_to_e(self, state_service, temp_project_dir):
        """Test execution logic for D→E transition"""
        result = state_service.execute_state_transition("D", "E", temp_project_dir)
        
        assert result["success"] is True
        assert "更新active_context.md" in result["details"]["action"]
    
    def test_execute_state_transition_default(self, state_service, temp_project_dir):
        """Test execution logic for default transitions"""
        result = state_service.execute_state_transition("C", "D", temp_project_dir)
        
        assert result["success"] is True
        assert result["details"]["action"] == "状态标记更新"


# -----------------------------------------------------------------------------
# Utility Function Tests
# -----------------------------------------------------------------------------

class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_create_state_transition_service(self):
        """Test create_state_transition_service factory function"""
        service = create_state_transition_service()
        
        assert isinstance(service, StateTransitionService)
        assert service.skill_root is not None
    
    def test_create_state_transition_service_with_root(self, temp_project_dir):
        """Test factory function with custom root path"""
        service = create_state_transition_service(temp_project_dir)
        
        assert isinstance(service, StateTransitionService)
        assert service.skill_root == temp_project_dir


# -----------------------------------------------------------------------------
# Integration Tests
# -----------------------------------------------------------------------------

class TestIntegration:
    """Integration-style tests"""
    
    def test_end_to_end_transition(self, temp_project_dir):
        """Test end-to-end state transition workflow"""
        service = StateTransitionService()
        
        # 1. Get initial state (should be A)
        initial_state = service.get_current_state(temp_project_dir)
        assert initial_state["current_state"] == "A"
        assert initial_state["valid_next_states"] == ["B"]
        
        # 2. Validate A→B transition
        validation = service.validate_transition(
            from_state="A",
            to_state="B",
            target_path=temp_project_dir
        )
        assert validation["valid"] is True
        
        # 3. Perform the transition
        transition_result = service.perform_transition(
            target_path=temp_project_dir,
            to_state="B",
            reason="集成测试"
        )
        assert transition_result["success"] is True
        assert transition_result["transition"] == "A → B"
        
        # 4. Verify new state
        new_state = service.get_current_state(temp_project_dir)
        assert new_state["current_state"] == "B"
        assert new_state["valid_next_states"] == ["C"]
        
        # 5. Create checkpoint
        checkpoint_result = service.create_checkpoint(
            target_path=temp_project_dir,
            note="集成测试检查点"
        )
        assert checkpoint_result["success"] is True
        assert "checkpoint_id" in checkpoint_result
    
    def test_state_file_persistence(self, temp_project_dir):
        """Test that state is properly persisted to file"""
        service = StateTransitionService()
        
        # Perform transition
        service.perform_transition(
            target_path=temp_project_dir,
            to_state="B",
            reason="持久性测试"
        )
        
        # Verify file was created
        state_file = temp_project_dir / ".cdd_state.json"
        assert state_file.exists()
        
        # Read and verify content
        with open(state_file, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        
        assert state_data["state"] == "B"
        assert "transition_timestamp" in state_data
        assert "transition_reason" in state_data
        assert state_data["transition_reason"] == "持久性测试"
        
        # Verify history was recorded
        assert "history" in state_data
        assert len(state_data["history"]) == 1
        assert state_data["history"][0]["from_state"] == "A"
        assert state_data["history"][0]["to_state"] == "B"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])