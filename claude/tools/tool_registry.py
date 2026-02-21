#!/usr/bin/env python3
"""
CDD Tool Registry (tool_registry.py) v2.0.0
==========================================
Claude Code工具注册器，管理所有CDD工具的注册和调用。

宪法依据: §309§310
"""

import sys
import json
import inspect
from pathlib import Path
from typing import Dict, Any, Optional, List, Type, Callable, Union

# -----------------------------------------------------------------------------
# Base Tool Class
# -----------------------------------------------------------------------------

class BaseTool:
    """
    CDD工具基类
    
    所有Claude Code工具都应继承此类以获得标准化接口
    """
    
    name: str = "base_tool"
    description: str = "Base tool class"
    version: str = "1.0.0"
    constitutional_basis: List[str] = []
    
    def __init__(self, project_root: Optional[Path] = None):
        """初始化工具
        
        Args:
            project_root: 项目根目录，默认为CDD技能库根目录
        """
        try:
            # 优先尝试从core.constants导入
            from core.constants import SKILL_ROOT
        except ImportError:
            # 后备方案：直接计算
            from pathlib import Path
            SKILL_ROOT = Path(__file__).parent.parent.resolve()
            
        self.project_root = project_root or SKILL_ROOT
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行工具的主要逻辑
        
        Returns:
            Dict[str, Any]: 执行结果，必须包含success字段
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    def validate_args(self, **kwargs) -> bool:
        """验证输入参数"""
        return True
    
    def get_info(self) -> Dict[str, Any]:
        """获取工具信息"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "constitutional_basis": self.constitutional_basis,
            "parameters": self._get_parameters_info()
        }
    
    def _get_parameters_info(self) -> List[Dict[str, Any]]:
        """获取工具参数信息"""
        params = []
        
        # 通过反射获取execute方法的参数
        sig = inspect.signature(self.execute)
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
                
            param_info = {
                "name": param_name,
                "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "any",
                "required": param.default == inspect.Parameter.empty,
                "default": param.default if param.default != inspect.Parameter.empty else None
            }
            params.append(param_info)
        
        return params
    
    def create_response(self, success: bool, **kwargs) -> Dict[str, Any]:
        """创建标准响应格式"""
        response = {
            "success": success,
            "timestamp": self._get_timestamp(),
            "tool": self.name,
            "version": self.version
        }
        
        if not success:
            response["error"] = kwargs.get("error", "Unknown error")
        
        response.update(kwargs)
        return response
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

# -----------------------------------------------------------------------------
# Tool Registry
# -----------------------------------------------------------------------------

class CDDToolRegistry:
    """
    CDD工具注册器
    
    单例模式，管理所有CDD工具的注册、发现和调用
    """
    
    _instance: Optional['CDDToolRegistry'] = None
    _tools: Dict[str, Type[BaseTool]] = {}
    _tool_instances: Dict[str, BaseTool] = {}
    
    def __new__(cls):
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register(self, tool_class: Type[BaseTool]) -> Type[BaseTool]:
        """
        注册工具类
        
        Args:
            tool_class: 工具类（继承自BaseTool）
            
        Returns:
            Type[BaseTool]: 注册的工具类
        """
        if not issubclass(tool_class, BaseTool):
            raise TypeError(f"Tool class must inherit from BaseTool: {tool_class}")
        
        self._tools[tool_class.name] = tool_class
        return tool_class
    
    def register_decorator(self) -> Callable:
        """工具注册装饰器"""
        def decorator(tool_class: Type[BaseTool]) -> Type[BaseTool]:
            return self.register(tool_class)
        return decorator
    
    def get_tool(self, name: str) -> Optional[Type[BaseTool]]:
        """获取工具类"""
        return self._tools.get(name)
    
    def create_tool_instance(self, name: str, **kwargs) -> Optional[BaseTool]:
        """创建工具实例"""
        tool_class = self.get_tool(name)
        if tool_class:
            instance = tool_class(**kwargs)
            self._tool_instances[name] = instance
            return instance
        return None
    
    def get_tool_instance(self, name: str) -> Optional[BaseTool]:
        """获取工具实例（已存在的）"""
        return self._tool_instances.get(name)
    
    def list_tools(self) -> List[str]:
        """列出所有已注册工具"""
        return list(self._tools.keys())
    
    def list_tools_with_info(self) -> List[Dict[str, Any]]:
        """列出所有工具及其详细信息"""
        tools_info = []
        
        for name, tool_class in self._tools.items():
            try:
                instance = tool_class()
                tools_info.append(instance.get_info())
            except Exception as e:
                tools_info.append({
                    "name": name,
                    "error": f"Failed to get info: {e}"
                })
        
        return tools_info
    
    def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        执行指定工具
        
        Args:
            name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            Dict[str, Any]: 执行结果
        """
        tool_class = self.get_tool(name)
        if not tool_class:
            return {
                "success": False,
                "error": f"Tool not found: {name}",
                "available_tools": self.list_tools()
            }
        
        try:
            # 创建实例并执行
            tool_instance = tool_class()
            
            # 验证参数
            if not tool_instance.validate_args(**kwargs):
                return tool_instance.create_response(
                    success=False,
                    error="Parameter validation failed"
                )
            
            # 执行工具
            result = tool_instance.execute(**kwargs)
            
            # 确保结果包含success字段
            if "success" not in result:
                result["success"] = True
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}",
                "tool": name
            }
    
    def get_registry_info(self) -> Dict[str, Any]:
        """获取注册器信息"""
        return {
            "version": "2.0.0",
            "total_tools": len(self._tools),
            "tools": self.list_tools(),
            "constitutional_basis": ["§309", "§310"]
        }

# -----------------------------------------------------------------------------
# Global Registry Instance
# -----------------------------------------------------------------------------

# 全局注册器实例
_registry_instance: Optional[CDDToolRegistry] = None

def get_registry() -> CDDToolRegistry:
    """获取全局注册器实例"""
    global _registry_instance
    
    if _registry_instance is None:
        _registry_instance = CDDToolRegistry()
    
    return _registry_instance

def register_tools(tool_classes: List[Type[BaseTool]]) -> None:
    """批量注册工具"""
    registry = get_registry()
    for tool_class in tool_classes:
        registry.register(tool_class)

def get_tool(name: str) -> Optional[Type[BaseTool]]:
    """获取工具类"""
    return get_registry().get_tool(name)

def list_tools() -> List[str]:
    """列出所有工具"""
    return get_registry().list_tools()

def list_tools_with_info() -> List[Dict[str, Any]]:
    """列出工具详细信息"""
    return get_registry().list_tools_with_info()

def execute_tool(name: str, **kwargs) -> Dict[str, Any]:
    """执行工具"""
    return get_registry().execute_tool(name, **kwargs)

# -----------------------------------------------------------------------------
# Tool Registration Decorator
# -----------------------------------------------------------------------------

def cdd_tool(name: Optional[str] = None, description: Optional[str] = None):
    """
    CDD工具装饰器
    
    Args:
        name: 工具名称，如未提供则使用类名的小写形式
        description: 工具描述
    """
    def decorator(cls: Type[BaseTool]) -> Type[BaseTool]:
        # 设置工具名称
        if name:
            cls.name = name
        elif not hasattr(cls, 'name') or cls.name == "base_tool":
            cls.name = cls.__name__.lower()
        
        # 设置工具描述
        if description:
            cls.description = description
        elif not hasattr(cls, 'description') or cls.description == "Base tool class":
            cls.description = cls.__doc__ or f"{cls.__name__} tool"
        
        # 注册工具
        registry = get_registry()
        return registry.register(cls)
    
    return decorator

# -----------------------------------------------------------------------------
# MCP Server Entry Point
# -----------------------------------------------------------------------------

def main():
    """
    MCP服务器入口点
    
    此函数可作为MCP服务器的入口，通过标准输入/输出与Claude Code通信
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="CDD Tool Registry MCP Server")
    
    parser.add_argument("--list", action="store_true", help="List all registered tools")
    parser.add_argument("--info", action="store_true", help="Show registry info")
    parser.add_argument("--execute", metavar="TOOL", help="Execute a tool")
    parser.add_argument("--args", type=str, default="{}", help="Tool arguments (JSON)")
    
    args = parser.parse_args()
    registry = get_registry()
    
    if args.list:
        tools_info = registry.list_tools_with_info()
        print(json.dumps({"tools": tools_info}, indent=2, ensure_ascii=False))
    
    elif args.info:
        info = registry.get_registry_info()
        print(json.dumps(info, indent=2, ensure_ascii=False))
    
    elif args.execute:
        try:
            tool_args = json.loads(args.args)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "success": False,
                "error": f"Invalid JSON arguments: {e}"
            }, indent=2))
            return
        
        result = registry.execute_tool(args.execute, **tool_args)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()