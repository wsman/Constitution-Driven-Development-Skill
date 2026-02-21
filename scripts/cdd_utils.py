#!/usr/bin/env python3
"""
CDD Unified Utilities (cdd_utils.py) v2.0.0
===========================================
整合所有通用工具函数和辅助类

整合来源：
- scripts/utils/bridge.py (API桥梁)
- scripts/utils/cache.py (缓存管理)
- scripts/utils/spore.py (孢子隔离)
- scripts/utils/__init__.py (初始化)

宪法依据: §200§102

Usage:
    from cdd_utils import run_command, CacheManager, check_spore_isolation
"""

import os
import sys
import json
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Union

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

VERSION = "2.0.0"
SKILL_ROOT = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------
# Command Execution (from bridge.py)
# -----------------------------------------------------------------------------

def run_command(
    cmd: Union[str, List[str]],
    cwd: Optional[Path] = None,
    timeout: int = 30,
    capture: bool = True,
    shell: bool = False
) -> Tuple[str, str, int]:
    """
    执行命令的统一接口
    
    Args:
        cmd: 命令（字符串或列表）
        cwd: 工作目录
        timeout: 超时时间（秒）
        capture: 是否捕获输出
        shell: 是否使用shell
        
    Returns:
        Tuple[str, str, int]: (stdout, stderr, returncode)
    """
    if cwd is None:
        cwd = SKILL_ROOT
    
    try:
        if isinstance(cmd, str) and not shell:
            cmd = cmd.split()
        
        kwargs = {
            "cwd": cwd,
            "text": True,
            "encoding": "utf-8",
            "timeout": timeout
        }
        
        if capture:
            kwargs["capture_output"] = True
        else:
            kwargs["stdout"] = None
            kwargs["stderr"] = None
        
        result = subprocess.run(cmd, shell=shell, **kwargs)
        
        if capture:
            return result.stdout or "", result.stderr or "", result.returncode
        return "", "", result.returncode
    
    except subprocess.TimeoutExpired:
        return "", f"Command timeout ({timeout}s)", 1
    except FileNotFoundError:
        return "", f"Command not found: {cmd[0] if isinstance(cmd, list) else cmd}", 127
    except Exception as e:
        return "", str(e), 1

def run_command_safe(
    cmd: Union[str, List[str]],
    cwd: Optional[Path] = None,
    blocked_patterns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    安全执行命令（带危险命令检查）
    
    Args:
        cmd: 命令
        cwd: 工作目录
        blocked_patterns: 阻止的模式列表
        
    Returns:
        Dict[str, Any]: 执行结果
    """
    if blocked_patterns is None:
        blocked_patterns = [
            "rm -rf /",
            "sudo rm",
            "chmod 777",
            "> /dev/sda",
            "mkfs",
            "dd if=",
            ":(){ :|:& };:"
        ]
    
    cmd_str = cmd if isinstance(cmd, str) else " ".join(cmd)
    
    for pattern in blocked_patterns:
        if pattern in cmd_str:
            return {
                "success": False,
                "error": f"Blocked dangerous pattern: {pattern}",
                "constitutional_violation": "§310"
            }
    
    stdout, stderr, rc = run_command(cmd, cwd)
    
    return {
        "success": rc == 0,
        "exit_code": rc,
        "stdout": stdout,
        "stderr": stderr,
        "command": cmd_str
    }

# -----------------------------------------------------------------------------
# Cache Management (from cache.py)
# -----------------------------------------------------------------------------

class CacheManager:
    """
    通用缓存管理器
    
    用于缓存计算结果以减少重复计算
    """
    
    CACHE_DIR_NAME = ".entropy_cache"
    CACHE_FILE = "entropy_cache.json"
    
    def __init__(self, project_path: Union[str, Path]):
        self.project_path = Path(project_path)
        self.cache_dir = self.project_path / self.CACHE_DIR_NAME
        self.cache_file = self.cache_dir / self.CACHE_FILE
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """确保缓存目录存在"""
        self.cache_dir.mkdir(exist_ok=True)
        gitignore = self.cache_dir / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text("*\n!.gitignore\n")
    
    def _compute_hash(self, data: Any) -> str:
        """计算数据哈希"""
        if isinstance(data, list):
            data = "|".join(sorted(str(d) for d in data))
        elif isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        else:
            data = str(data)
        
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if not self.cache_file.exists():
            return None
        
        try:
            cache_data = json.loads(self.cache_file.read_text())
            return cache_data.get(key, {}).get("value")
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """设置缓存值"""
        try:
            cache_data = {}
            if self.cache_file.exists():
                cache_data = json.loads(self.cache_file.read_text())
            
            entry = {
                "value": value,
                "timestamp": datetime.now().isoformat()
            }
            
            if ttl:
                entry["expires"] = (datetime.now().timestamp() + ttl)
            
            cache_data[key] = entry
            self.cache_file.write_text(json.dumps(cache_data, indent=2))
        except Exception:
            pass
    
    def get_with_deps(
        self, 
        key: str, 
        dependencies: List[str],
        force: bool = False
    ) -> Tuple[Optional[Any], bool]:
        """
        带依赖检查的缓存获取
        
        Args:
            key: 缓存键
            dependencies: 依赖文件列表
            force: 是否强制刷新
            
        Returns:
            Tuple[Optional[Any], bool]: (缓存值, 是否需要重新计算)
        """
        if force or not self.cache_file.exists():
            return None, True
        
        try:
            cache_data = json.loads(self.cache_file.read_text())
            cached = cache_data.get(key, {})
            
            current_hash = self._compute_hash(dependencies)
            
            if cached.get("deps_hash") == current_hash:
                # 检查TTL
                if "expires" in cached:
                    if datetime.now().timestamp() > cached["expires"]:
                        return None, True
                return cached.get("value"), False
            
            return None, True
        except Exception:
            return None, True
    
    def set_with_deps(
        self, 
        key: str, 
        value: Any, 
        dependencies: List[str],
        ttl: Optional[int] = None
    ):
        """带依赖哈希的缓存设置"""
        try:
            cache_data = {}
            if self.cache_file.exists():
                cache_data = json.loads(self.cache_file.read_text())
            
            entry = {
                "value": value,
                "deps_hash": self._compute_hash(dependencies),
                "timestamp": datetime.now().isoformat()
            }
            
            if ttl:
                entry["expires"] = (datetime.now().timestamp() + ttl)
            
            cache_data[key] = entry
            self.cache_file.write_text(json.dumps(cache_data, indent=2))
        except Exception:
            pass
    
    def clear(self):
        """清除缓存"""
        if self.cache_file.exists():
            self.cache_file.unlink()
    
    def get_info(self) -> Dict[str, Any]:
        """获取缓存信息"""
        if not self.cache_file.exists():
            return {"exists": False, "entries": 0}
        
        try:
            cache_data = json.loads(self.cache_file.read_text())
            return {
                "exists": True,
                "entries": len(cache_data),
                "keys": list(cache_data.keys()),
                "size_bytes": self.cache_file.stat().st_size
            }
        except Exception as e:
            return {"exists": False, "error": str(e)}

    # 向后兼容方法别名
    def get_cached_metric(self, key: str) -> Optional[Any]:
        """获取缓存指标（向后兼容）"""
        return self.get(key)
    
    def set_cached_metric(self, key: str, value: Any, ttl: Optional[int] = None):
        """设置缓存指标（向后兼容）"""
        self.set(key, value, ttl)

# -----------------------------------------------------------------------------
# Spore Isolation (from spore.py)
# -----------------------------------------------------------------------------

def check_spore_isolation(
    target_root: Path, 
    tool_name: str,
    allow_skill_root: bool = False,
    strict_mode: bool = True
) -> Tuple[bool, str]:
    """
    孢子隔离检查
    
    确保工具不会意外修改CDD技能库自身
    
    Args:
        target_root: 目标目录
        tool_name: 工具名称
        allow_skill_root: 是否允许操作技能库
        strict_mode: 是否严格模式（默认True，检查部署标志）
        
    Returns:
        Tuple[bool, str]: (是否通过, 消息)
    """
    target_root = Path(target_root).resolve()
    
    # 1. 检查部署模式
    if not strict_mode or is_deployment_mode(target_root):
        return True, "Deployment mode detected, spore isolation bypassed"
    
    # 2. 检查是否是技能库本身
    if target_root == SKILL_ROOT:
        if allow_skill_root:
            return True, "Self-modification allowed"
        else:
            return False, f"""
⛔ **SPORE ISOLATION VIOLATION [{tool_name}]**
    Target directory is CDD Skill Root: {SKILL_ROOT}
    CDD Skill is a tool, not a target project.
    Please specify a different target: --target /path/to/project
"""
    
    # 3. 检查是否在技能库内（子目录）
    try:
        target_root.relative_to(SKILL_ROOT)
        if strict_mode:
            return False, f"""
⛔ **SPORE ISOLATION VIOLATION [{tool_name}]**
    Target directory is inside CDD Skill Root: {target_root}
    Cannot operate on CDD skill subdirectories.
    Please specify a different target: --target /path/to/independent/project
"""
        else:
            return True, "Warning: Target is inside CDD Skill Root"
    except ValueError:
        pass  # 不在SKILL_ROOT内，安全
    
    return True, "Spore isolation check passed"

def create_deployment_flag(skill_root: Path, deployed_dir: Path):
    """
    创建部署标志
    
    标记已部署的工具处于部署模式
    """
    flag_file = deployed_dir / ".cdd_deployed"
    
    flag_content = {
        "source_skill": str(skill_root),
        "deployed_at": datetime.now().isoformat(),
        "version": VERSION
    }
    
    flag_file.write_text(json.dumps(flag_content, indent=2))

def is_deployment_mode(script_dir: Path) -> bool:
    """检查是否处于部署模式"""
    flag_file = script_dir / ".cdd_deployed"
    return flag_file.exists()

# -----------------------------------------------------------------------------
# File Utilities
# -----------------------------------------------------------------------------

def ensure_dir(path: Union[str, Path]) -> Path:
    """确保目录存在"""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def read_json(path: Union[str, Path]) -> Optional[Dict[str, Any]]:
    """读取JSON文件"""
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:
        return None

def write_json(path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> bool:
    """写入JSON文件"""
    try:
        Path(path).write_text(
            json.dumps(data, indent=indent, ensure_ascii=False),
            encoding='utf-8'
        )
        return True
    except Exception:
        return False

def read_file(path: Union[str, Path], default: str = "") -> str:
    """读取文件"""
    try:
        return Path(path).read_text(encoding='utf-8')
    except Exception:
        return default

def write_file(path: Union[str, Path], content: str) -> bool:
    """写入文件"""
    try:
        Path(path).write_text(content, encoding='utf-8')
        return True
    except Exception:
        return False

def file_matches_patterns(path: Path, patterns: List[str]) -> bool:
    """检查文件是否匹配任何模式"""
    path_str = str(path)
    for pattern in patterns:
        if pattern in path_str:
            return True
    return False

# -----------------------------------------------------------------------------
# Logging Utilities
# -----------------------------------------------------------------------------

class Logger:
    """简单日志器"""
    
    LEVELS = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
    
    def __init__(self, name: str, level: str = "INFO"):
        self.name = name
        self.level = self.LEVELS.get(level, 1)
    
    def _log(self, level: str, message: str):
        if self.LEVELS.get(level, 1) >= self.level:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] [{self.name}] {message}")
    
    def debug(self, message: str):
        self._log("DEBUG", message)
    
    def info(self, message: str):
        self._log("INFO", message)
    
    def warning(self, message: str):
        self._log("WARNING", message)
    
    def error(self, message: str):
        self._log("ERROR", message)

# -----------------------------------------------------------------------------
# Version Utilities
# -----------------------------------------------------------------------------

def parse_version(version_str: str) -> Tuple[int, int, int]:
    """解析版本字符串"""
    import re
    match = re.search(r'(\d+)\.(\d+)\.(\d+)', version_str)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    return 0, 0, 0

def compare_version(v1: str, v2: str) -> int:
    """
    比较版本号
    
    Returns:
        int: -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2
    """
    p1 = parse_version(v1)
    p2 = parse_version(v2)
    
    if p1 < p2:
        return -1
    elif p1 > p2:
        return 1
    return 0

# -----------------------------------------------------------------------------
# CLI Test
# -----------------------------------------------------------------------------

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description=f"CDD Utilities v{VERSION}")
    
    parser.add_argument("--test-command", metavar="CMD", help="Test command execution")
    parser.add_argument("--cache-info", metavar="PATH", help="Show cache info")
    parser.add_argument("--cache-clear", metavar="PATH", help="Clear cache")
    parser.add_argument("--spore-check", metavar="PATH", help="Check spore isolation")
    
    args = parser.parse_args()
    
    if args.test_command:
        stdout, stderr, rc = run_command(args.test_command)
        print(f"stdout: {stdout[:200]}...")
        print(f"stderr: {stderr[:200]}...")
        print(f"returncode: {rc}")
    
    elif args.cache_info:
        cache = CacheManager(args.cache_info)
        info = cache.get_info()
        print(json.dumps(info, indent=2))
    
    elif args.cache_clear:
        cache = CacheManager(args.cache_clear)
        cache.clear()
        print("Cache cleared")
    
    elif args.spore_check:
        passed, message = check_spore_isolation(Path(args.spore_check), "test")
        print(f"Passed: {passed}")
        print(message)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()