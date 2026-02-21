#!/usr/bin/env python3
"""
CDD Claude Code Bridge (cdd_claude_bridge.py) v2.0.0
=====================================================
整合Claude Code集成的核心桥梁功能

整合来源：
- claude_tools/claude_code_bridge.py (核心桥梁)
- claude_tools/tool_registry.py (工具注册)
- claude_tools/base_tool.py (基础工具类)
- claude_tools/placeholder_resolver.py (占位符解析)
- scripts/utils/bridge.py (API桥梁)

宪法依据: §309§304

Usage:
    # 作为模块导入
    from cdd_claude_bridge import ClaudeCodeBridge, get_bridge
    
    # 命令行测试
    python scripts/cdd_claude_bridge.py --status
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable, Type

# -----------------------------------------------------------------------------
# Constants & Configuration
# -----------------------------------------------------------------------------

VERSION = "2.0.0"
SKILL_ROOT = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------
# Base Tool Class
# -----------------------------------------------------------------------------

class BaseTool:
    """
    工具基类
    
    所有CDD工具都应继承此类以获得标准化的接口
    """
    
    name: str = "base_tool"
    description: str = "Base tool class"
    constitutional_basis: List[str] = []
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or SKILL_ROOT
        self.version = "1.0.0"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """执行工具"""
        raise NotImplementedError("Subclasses must implement execute()")
    
    def validate_args(self, **kwargs) -> bool:
        """验证参数"""
        return True
    
    def get_info(self) -> Dict[str, Any]:
        """获取工具信息"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "constitutional_basis": self.constitutional_basis
        }

# -----------------------------------------------------------------------------
# Tool Registry
# -----------------------------------------------------------------------------

class ToolRegistry:
    """
    工具注册中心
    
    管理所有可用工具的注册和发现
    """
    
    _instance: Optional['ToolRegistry'] = None
    _tools: Dict[str, Type[BaseTool]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, tool_class: Type[BaseTool]) -> Type[BaseTool]:
        """注册工具（装饰器模式）"""
        cls._tools[tool_class.name] = tool_class
        return tool_class
    
    @classmethod
    def get_tool(cls, name: str) -> Optional[Type[BaseTool]]:
        """获取工具类"""
        return cls._tools.get(name)
    
    @classmethod
    def list_tools(cls) -> List[str]:
        """列出所有已注册工具"""
        return list(cls._tools.keys())
    
    @classmethod
    def create_instance(cls, name: str, **kwargs) -> Optional[BaseTool]:
        """创建工具实例"""
        tool_class = cls.get_tool(name)
        if tool_class:
            return tool_class(**kwargs)
        return None

# -----------------------------------------------------------------------------
# Placeholder Resolver
# -----------------------------------------------------------------------------

class PlaceholderResolver:
    """
    占位符解析器
    
    处理模板中的变量替换
    """
    
    # 标准占位符
    STANDARD_PLACEHOLDERS = {
        "PROJECT_NAME": lambda ctx: ctx.get("project_name", "Unknown Project"),
        "TIMESTAMP": lambda ctx: datetime.now().strftime("%Y-%m-%d"),
        "DATETIME": lambda ctx: datetime.now().isoformat(),
        "YEAR": lambda ctx: str(datetime.now().year),
        "VERSION": lambda ctx: ctx.get("version", "1.0.0"),
    }
    
    def __init__(self):
        self.custom_resolvers: Dict[str, Callable] = {}
    
    def register_resolver(self, name: str, resolver: Callable):
        """注册自定义解析器"""
        self.custom_resolvers[name] = resolver
    
    def resolve(self, content: str, context: Dict[str, Any]) -> str:
        """解析占位符"""
        import re
        
        result = content
        
        # 合并标准解析器和自定义解析器
        all_resolvers = {**self.STANDARD_PLACEHOLDERS, **self.custom_resolvers}
        
        # 添加上下文值
        for key, value in context.items():
            if key not in all_resolvers:
                all_resolvers[key] = lambda ctx, v=value: str(v)
        
        # 替换占位符 {{ var }}
        for name, resolver in all_resolvers.items():
            pattern = r"\{\{\s*" + re.escape(name) + r"\s*\}\}"
            try:
                value = resolver(context) if callable(resolver) else str(resolver)
                result = re.sub(pattern, value, result)
            except Exception:
                pass
        
        return result

# -----------------------------------------------------------------------------
# Claude Code Bridge
# -----------------------------------------------------------------------------

class ClaudeCodeBridge:
    """
    Claude Code 桥接器
    
    提供与Claude Code环境的集成接口
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        self.version = VERSION
        self.constitutional_basis = ["§309", "§304", "§101", "§102"]
        
        # 确定项目根目录
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = SKILL_ROOT
        
        # Claude Code配置路径
        self.claude_config_dir = Path.home() / ".claude"
        self.skills_dir = self.claude_config_dir / "skills"
        
        # 组件
        self.tool_registry = ToolRegistry()
        self.placeholder_resolver = PlaceholderResolver()
        
        # 会话状态
        self.current_session: Optional[Dict[str, Any]] = None
        self.checkpoint_data: Optional[Dict[str, Any]] = None
    
    def is_claude_code_environment(self) -> bool:
        """检测是否在Claude Code环境中"""
        claude_env_vars = [
            "CLAUDE_CODE_SESSION",
            "ANTHROPIC_API_KEY",
            "CLAUDE_SESSION_ID"
        ]
        
        for var in claude_env_vars:
            if os.environ.get(var):
                return True
        
        if self.claude_config_dir.exists():
            return True
        
        return False
    
    def get_session_info(self) -> Dict[str, Any]:
        """获取当前会话信息"""
        session_info = {
            "in_claude_code": self.is_claude_code_environment(),
            "project_root": str(self.project_root),
            "bridge_version": self.version,
            "timestamp": datetime.now().isoformat()
        }
        
        session_id = os.environ.get("CLAUDE_SESSION_ID") or os.environ.get("CLAUDE_CODE_SESSION")
        if session_id:
            session_info["session_id"] = session_id
        
        return session_info
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        调用CDD工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            Dict[str, Any]: 工具执行结果
        """
        # 首先尝试从注册中心获取
        tool = self.tool_registry.create_instance(tool_name, **kwargs)
        if tool:
            return tool.execute(**kwargs)
        
        # 回退到动态导入新工具
        tool_mapping = {
            "cdd_audit": ("cdd_auditor", "audit_gates_claude"),
            "cdd_feature": ("cdd_feature", "create_feature_claude"),
            "cdd_deploy": ("cdd_feature", "deploy_project_claude"),
            "cdd_entropy": ("cdd_entropy", "measure_entropy_claude"),
            "cdd_analyze": ("cdd_entropy", "analyze_entropy_claude"),
        }
        
        if tool_name in tool_mapping:
            module_name, func_name = tool_mapping[tool_name]
            try:
                # 动态导入
                import importlib
                module = importlib.import_module(f"scripts.{module_name}")
                func = getattr(module, func_name)
                return func(**kwargs)
            except ImportError as e:
                return {"success": False, "error": f"Module import failed: {e}"}
            except AttributeError as e:
                return {"success": False, "error": f"Function not found: {e}"}
        
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}",
            "available_tools": list(tool_mapping.keys()) + self.tool_registry.list_tools()
        }
    
    def execute_command(self, command: str, timeout: int = 300) -> Dict[str, Any]:
        """执行命令（安全封装）"""
        # 危险命令检查
        dangerous_patterns = [
            "rm -rf /",
            "sudo rm",
            "chmod 777",
            "> /dev/sda",
            "mkfs",
            "dd if="
        ]
        
        for pattern in dangerous_patterns:
            if pattern in command:
                return {
                    "success": False,
                    "error": f"Dangerous command blocked: {pattern}",
                    "constitutional_violation": "§310"
                }
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command,
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timeout ({timeout}s)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_checkpoint(self, state: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建检查点"""
        checkpoint = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "state": state,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "constitutional_basis": self.constitutional_basis
        }
        
        checkpoint_dir = self.project_root / "memory_bank" / "checkpoints"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        checkpoint_path = checkpoint_dir / f"checkpoint_{checkpoint['id']}.json"
        
        try:
            with open(checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(checkpoint, f, indent=2, ensure_ascii=False)
            
            self.checkpoint_data = checkpoint
            
            return {
                "success": True,
                "checkpoint_id": checkpoint['id'],
                "path": str(checkpoint_path),
                "state": state
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def restore_checkpoint(self, checkpoint_id: Optional[str] = None) -> Dict[str, Any]:
        """恢复检查点"""
        checkpoint_dir = self.project_root / "memory_bank" / "checkpoints"
        
        if not checkpoint_dir.exists():
            return {"success": False, "error": "Checkpoint directory not found"}
        
        if checkpoint_id:
            checkpoint_path = checkpoint_dir / f"checkpoint_{checkpoint_id}.json"
        else:
            checkpoints = sorted(checkpoint_dir.glob("checkpoint_*.json"), reverse=True)
            if not checkpoints:
                return {"success": False, "error": "No checkpoints found"}
            checkpoint_path = checkpoints[0]
        
        try:
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
            
            self.checkpoint_data = checkpoint
            
            return {
                "success": True,
                "checkpoint": checkpoint,
                "path": str(checkpoint_path)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_bridge_status(self) -> Dict[str, Any]:
        """获取桥接器状态"""
        return {
            "version": self.version,
            "constitutional_basis": self.constitutional_basis,
            "project_root": str(self.project_root),
            "claude_code_environment": self.is_claude_code_environment(),
            "session_info": self.get_session_info(),
            "registered_tools": self.tool_registry.list_tools(),
            "checkpoint_active": self.checkpoint_data is not None,
            "timestamp": datetime.now().isoformat()
        }

# -----------------------------------------------------------------------------
# Global Bridge Instance
# -----------------------------------------------------------------------------

_bridge_instance: Optional[ClaudeCodeBridge] = None

def get_bridge(project_root: Optional[Path] = None) -> ClaudeCodeBridge:
    """获取全局桥接器实例"""
    global _bridge_instance
    
    if _bridge_instance is None:
        _bridge_instance = ClaudeCodeBridge(project_root)
    
    return _bridge_instance

def execute_in_claude_code(tool_name: str, **kwargs) -> Dict[str, Any]:
    """在Claude Code环境中执行工具"""
    bridge = get_bridge()
    return bridge.call_tool(tool_name, **kwargs)

# -----------------------------------------------------------------------------
# Registered Tools (使用新工具)
# -----------------------------------------------------------------------------

@ToolRegistry.register
class CDDAuditTool(BaseTool):
    """审计工具包装器"""
    name = "cdd_audit"
    description = "CDD宪法审计工具"
    constitutional_basis = ["§101", "§102"]
    
    def execute(self, gates: str = "all", fix: bool = False, **kwargs) -> Dict[str, Any]:
        from cdd_auditor import audit_gates_claude
        return audit_gates_claude(gates=gates, fix=fix, **kwargs)

@ToolRegistry.register
class CDDFeatureTool(BaseTool):
    """特性工具包装器"""
    name = "cdd_feature"
    description = "CDD特性脚手架工具"
    constitutional_basis = ["§309"]
    
    def execute(self, name: str, description: str = "", **kwargs) -> Dict[str, Any]:
        from cdd_feature import create_feature_claude
        return create_feature_claude(name=name, description=description, **kwargs)

@ToolRegistry.register
class CDDEntropyTool(BaseTool):
    """熵值工具包装器"""
    name = "cdd_entropy"
    description = "CDD熵值计算工具"
    constitutional_basis = ["§102"]
    
    def execute(self, project_path: str = ".", **kwargs) -> Dict[str, Any]:
        from cdd_entropy import measure_entropy_claude
        return measure_entropy_claude(project_path=project_path, **kwargs)

# -----------------------------------------------------------------------------
# CLI Entry Point
# -----------------------------------------------------------------------------

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description=f"CDD Claude Code Bridge v{VERSION}")
    
    parser.add_argument("--status", action="store_true", help="Show bridge status")
    parser.add_argument("--list-tools", action="store_true", help="List available tools")
    parser.add_argument("--call", metavar="TOOL", help="Call a tool")
    parser.add_argument("--args", type=str, default="{}", help="Tool arguments (JSON)")
    
    args = parser.parse_args()
    
    bridge = get_bridge()
    
    if args.status:
        status = bridge.get_bridge_status()
        print(json.dumps(status, indent=2))
    
    elif args.list_tools:
        print("Available Tools:")
        for tool in ToolRegistry.list_tools():
            tool_class = ToolRegistry.get_tool(tool)
            if tool_class:
                info = tool_class().get_info()
                print(f"  - {info['name']}: {info['description']}")
    
    elif args.call:
        try:
            tool_args = json.loads(args.args)
        except json.JSONDecodeError:
            tool_args = {}
        
        result = bridge.call_tool(args.call, **tool_args)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()