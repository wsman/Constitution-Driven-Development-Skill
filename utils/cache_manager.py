"""
Cache Manager

通用缓存管理器，用于缓存计算结果以减少重复计算。

宪法依据: §102
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Tuple, Dict

from core.constants import CACHE_DIR_NAME, CACHE_FILE
from core.exceptions import CacheError


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.cache_dir = self.project_path / CACHE_DIR_NAME
        self.cache_file = self.cache_dir / CACHE_FILE
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
        except Exception as e:
            raise CacheError("get", str(e))
    
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
        except Exception as e:
            raise CacheError("set", str(e))
    
    def get_with_deps(
        self, 
        key: str, 
        dependencies: list,
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
        except Exception as e:
            return None, True
    
    def set_with_deps(
        self, 
        key: str, 
        value: Any, 
        dependencies: list,
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
        except Exception as e:
            raise CacheError("set_with_deps", str(e))
    
    def get_cached_metric(self, key: str, dependencies: list, force: bool = False) -> Tuple[Optional[Any], bool]:
        """
        获取缓存的指标值（兼容性接口）
        
        Args:
            key: 缓存键
            dependencies: 依赖列表
            force: 是否强制刷新
            
        Returns:
            (缓存值, 是否需要重新计算)
        """
        return self.get_with_deps(key, dependencies, force)
    
    def set_cached_metric(self, key: str, value: Any, dependencies: list, ttl: Optional[int] = None):
        """
        设置缓存的指标值（兼容性接口）
        """
        self.set_with_deps(key, value, dependencies, ttl)
    
    def clear(self):
        """清除缓存"""
        if self.cache_file.exists():
            try:
                self.cache_file.unlink()
            except Exception as e:
                raise CacheError("clear", str(e))
    
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
    
    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息（兼容性接口）"""
        return self.get_info()
    
    def clear_cache(self):
        """清除缓存（兼容性接口）"""
        self.clear()
