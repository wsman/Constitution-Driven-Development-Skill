"""
File Utilities

文件操作工具函数。

宪法依据: §309
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union, List

from core.constants import SKILL_ROOT, DEFAULT_ENCODING
from core.exceptions import CDDError


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
            "encoding": DEFAULT_ENCODING,
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


def ensure_dir(path: Union[str, Path]) -> Path:
    """确保目录存在"""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_json(path: Union[str, Path]) -> Optional[Dict[str, Any]]:
    """读取JSON文件"""
    try:
        return json.loads(Path(path).read_text(encoding=DEFAULT_ENCODING))
    except Exception:
        return None


def write_json(path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> bool:
    """写入JSON文件"""
    try:
        Path(path).write_text(
            json.dumps(data, indent=indent, ensure_ascii=False),
            encoding=DEFAULT_ENCODING
        )
        return True
    except Exception:
        return False


def read_file(path: Union[str, Path], default: str = "") -> str:
    """读取文件"""
    try:
        return Path(path).read_text(encoding=DEFAULT_ENCODING)
    except Exception:
        return default


def write_file(path: Union[str, Path], content: str) -> bool:
    """写入文件"""
    try:
        Path(path).write_text(content, encoding=DEFAULT_ENCODING)
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

def safe_read_text(path: Union[str, Path], encoding: str = DEFAULT_ENCODING) -> str:
    """安全读取文本文件，自动处理编码问题"""
    try:
        return Path(path).read_text(encoding=encoding)
    except UnicodeDecodeError:
        # 尝试不同的编码
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        for enc in encodings:
            try:
                return Path(path).read_text(encoding=enc)
            except UnicodeDecodeError:
                continue
        # 如果所有编码都失败，尝试二进制读取
        try:
            return Path(path).read_bytes().decode('utf-8', errors='ignore')
        except Exception as e:
            raise CDDError(f"无法读取文件 {path}: {e}")
    except Exception as e:
        raise CDDError(f"无法读取文件 {path}: {e}")

def safe_write_text(path: Union[str, Path], content: str, encoding: str = DEFAULT_ENCODING) -> bool:
    """安全写入文本文件"""
    try:
        Path(path).write_text(content, encoding=encoding)
        return True
    except Exception:
        return False

def find_files(root: Path, pattern: str = "**/*") -> List[Path]:
    """查找匹配模式的所有文件"""
    try:
        return list(root.glob(pattern))
    except Exception:
        return []
