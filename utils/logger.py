"""
Simple Logger

简化日志工具，避免复杂依赖。

宪法依据: §309
"""

import sys
from datetime import datetime
from typing import Optional


class Logger:
    """简单日志记录器"""
    
    LEVELS = {
        "DEBUG": 0,
        "INFO": 1,
        "WARNING": 2,
        "ERROR": 3,
        "CRITICAL": 4
    }
    
    def __init__(self, name: str = "cdd", level: str = "INFO"):
        self.name = name
        self.level = self.LEVELS.get(level.upper(), self.LEVELS["INFO"])
    
    def _log(self, level: str, message: str, **kwargs):
        """记录日志"""
        level_num = self.LEVELS.get(level.upper(), self.LEVELS["INFO"])
        if level_num < self.level:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] [{level}] [{self.name}] {message}"
        
        # 处理额外参数
        if kwargs:
            args_str = " ".join(f"{k}={v}" for k, v in kwargs.items())
            full_message += f" ({args_str})"
        
        # 输出到stderr（INFO及以下到stdout）
        output_stream = sys.stdout if level in ["DEBUG", "INFO"] else sys.stderr
        print(full_message, file=output_stream)
    
    def debug(self, message: str, **kwargs):
        """调试日志"""
        self._log("DEBUG", message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """信息日志"""
        self._log("INFO", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """警告日志"""
        self._log("WARNING", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """错误日志"""
        self._log("ERROR", message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """严重错误日志"""
        self._log("CRITICAL", message, **kwargs)
    
    def set_level(self, level: str):
        """设置日志级别"""
        self.level = self.LEVELS.get(level.upper(), self.LEVELS["INFO"])


# 默认全局日志器
_default_logger: Optional[Logger] = None

def get_logger(name: str = "cdd") -> Logger:
    """获取日志器实例"""
    global _default_logger
    if _default_logger is None or _default_logger.name != name:
        _default_logger = Logger(name)
    return _default_logger