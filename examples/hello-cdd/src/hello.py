"""hello 模块 - 演示 CDD 工作流"""

__version__ = "2.0.0"

def greet(name: str) -> str:
    """
    返回问候语
    
    Args:
        name: 用户名
        
    Returns:
        问候字符串
    """
    if not name:
        return "Hello, CDD World!"
    return f"Hello, {name}!"

def get_version() -> str:
    """
    返回版本号
    
    Returns:
        版本字符串 (如 "0.1.0")
    """
    return __version__