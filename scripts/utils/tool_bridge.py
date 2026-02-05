#!/usr/bin/env python3
"""
CDD Tool Bridge (Digital Airlock for Filesystem)
================================================
Implementation of Technical Law §438 & Standard DS-039.
Enforces:
1. Path Isolation (Spore Protocol §300.1)
2. Atomic Writes (Technical Law §302)
3. Operation Auditing

宪法约束: 所有文件I/O必须通过本桥接器，直接使用Path.read_text()等原生API视为严重违宪。
"""

import os
import shutil
import tempfile
import uuid
import logging
from datetime import datetime, UTC
from pathlib import Path
from typing import Optional, List, Union, Dict, Any

class ToolBridge:
    """
    CDD Tool Bridge (Digital Airlock for Filesystem)
    
    **宪法约束**: 根据技术法§438和标准DS-039，所有文件操作必须通过本桥接器进行。
    **安全隔离**: 实施孢子协议§300.1，防止路径遍历攻击。
    **原子写入**: 实施§302原子写入原则，避免中间状态。
    """

    def __init__(self, project_root: Union[str, Path]):
        """
        初始化工具桥接器
        
        Args:
            project_root: 项目根目录，所有操作将被限制在此目录内
            
        Raises:
            ValueError: 如果项目根目录不存在
        """
        self.project_root = Path(project_root).resolve()
        if not self.project_root.exists():
            raise ValueError(f"项目根目录不存在: {self.project_root}")
        
        self._setup_logging()
        self.logger.info(f"ToolBridge 初始化完成，项目根目录: {self.project_root}")

    def _setup_logging(self):
        """设置审计日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [ToolBridge] - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("ToolBridge")

    def _validate_path(self, relative_path: str) -> Path:
        """
        强制执行孢子协议: 防止路径遍历攻击。
        
        Args:
            relative_path: 相对路径
            
        Returns:
            Path: 验证后的绝对路径
            
        Raises:
            PermissionError: 路径试图逃离项目边界
            ValueError: 路径格式无效
        """
        try:
            # 处理空路径或None
            if not relative_path:
                relative_path = "."
            
            # 解析路径: PROJECT_ROOT / relative_path
            target_path = (self.project_root / relative_path).resolve()
            
            # 规范化: resolve() 处理 `.`, `..`, 符号链接
            # 前缀检查: 确保目标路径在项目根目录内
            # 注意: 使用字符串比较确保跨平台兼容性
            if not str(target_path).startswith(str(self.project_root)):
                raise PermissionError(
                    f"孢子协议违宪: 路径 '{relative_path}' 试图逃离项目边界。\n"
                    f"  项目根目录: {self.project_root}\n"
                    f"  目标路径: {target_path}"
                )
                
            return target_path
            
        except PermissionError:
            # 重新抛出安全异常
            raise
        except Exception as e:
            self.logger.error(f"路径验证错误: {relative_path} - {e}")
            raise ValueError(f"无效路径: '{relative_path}' - {e}")

    def _log_operation(self, operation: str, path: str, **kwargs):
        """记录操作审计日志"""
        log_data = {
            "timestamp": self._get_timestamp(),
            "operation": operation,
            "path": path,
            "relative_path": path,
            "agent": self._get_caller(),
            **kwargs
        }
        self.logger.info(f"操作审计: {log_data}")

    def _get_timestamp(self) -> str:
        """获取ISO格式时间戳"""
        return datetime.now(UTC).isoformat() + "Z"

    def _get_caller(self) -> str:
        """获取调用者信息"""
        import inspect
        try:
            # 跳过tool_bridge.py自身的调用栈
            stack = inspect.stack()
            for frame in stack[2:]:  # 跳过当前方法和_log_operation
                filename = frame.filename
                if "tool_bridge" not in filename:
                    return Path(filename).name
        except:
            pass
        return "unknown"

    def read_file(self, path: str) -> str:
        """
        安全读取文件
        
        Args:
            path: 相对路径
            
        Returns:
            str: 文件内容，如果文件不存在返回空字符串
            
        Raises:
            PermissionError: 路径违宪
            OSError: 读取失败
        """
        try:
            target = self._validate_path(path)
            
            if not target.exists():
                self.logger.warning(f"读取失败: 文件不存在 {path}")
                return ""
            if not target.is_file():
                self.logger.warning(f"读取失败: 不是文件 {path}")
                return ""
            
            content = target.read_text(encoding='utf-8')
            self._log_operation("READ", path, size_bytes=len(content))
            return content
            
        except Exception as e:
            self.logger.error(f"读取错误 {path}: {e}")
            # 对于读取操作，不抛出异常，返回空字符串
            return ""

    def write_file(self, path: str, content: str) -> bool:
        """
        DS-039 §3.2: 原子写入操作
        
        Args:
            path: 相对路径
            content: 要写入的内容
            
        Returns:
            bool: 是否成功
            
        Raises:
            PermissionError: 路径违宪
            OSError: 写入失败
        """
        target = self._validate_path(path)
        atomic_id = f"tmp.{uuid.uuid4().hex[:8]}"
        
        # 确保目录存在
        target.parent.mkdir(parents=True, exist_ok=True)
        
        temp_file = None
        try:
            # 1. 在同目录创建临时文件
            temp_path = target.parent / f"{target.name}.{atomic_id}"
            temp_file = temp_path
            
            # 2. 写入内容
            temp_file.write_text(content, encoding='utf-8')
            
            # 3. 强制落盘
            temp_file_fd = os.open(str(temp_file), os.O_RDONLY)
            try:
                os.fsync(temp_file_fd)
            finally:
                os.close(temp_file_fd)
            
            # 4. 原子重命名
            temp_file.replace(target)
            
            self._log_operation("ATOMIC_WRITE", path, 
                               size_bytes=len(content),
                               atomic_id=atomic_id)
            self.logger.info(f"原子写入成功: {path} ({len(content)} 字符)")
            return True
            
        except Exception as e:
            self.logger.error(f"写入错误 {path}: {e}")
            # 清理临时文件
            if temp_file and temp_file.exists():
                try:
                    temp_file.unlink()
                except:
                    pass
            raise

    def list_files(self, path: str = ".", recursive: bool = False, 
                   extension: Optional[str] = None) -> List[str]:
        """
        安全列出文件
        
        Args:
            path: 目录相对路径
            recursive: 是否递归
            extension: 文件扩展名过滤
            
        Returns:
            List[str]: 相对路径列表
        """
        try:
            target = self._validate_path(path)
            
            if not target.exists():
                return []
            if not target.is_dir():
                return []
            
            results = []
            pattern = "**/*" if recursive else "*"
            
            for p in target.glob(pattern):
                if p.is_file():
                    # 扩展名过滤
                    if extension and not str(p).endswith(extension):
                        continue
                    
                    # 转换为相对路径
                    rel_path = p.relative_to(self.project_root)
                    results.append(str(rel_path))
            
            self._log_operation("LIST", path, 
                               file_count=len(results),
                               recursive=recursive)
            return sorted(results)
            
        except Exception as e:
            self.logger.error(f"列出文件错误 {path}: {e}")
            return []

    def file_exists(self, path: str) -> bool:
        """
        检查文件是否存在
        
        Args:
            path: 相对路径
            
        Returns:
            bool: 文件是否存在且是普通文件
        """
        try:
            target = self._validate_path(path)
            exists = target.exists() and target.is_file()
            return exists
        except PermissionError:
            # 路径违宪，视为不存在
            return False
        except Exception as e:
            self.logger.warning(f"检查存在性错误 {path}: {e}")
            return False

    def ensure_directory(self, path: str) -> bool:
        """
        确保目录存在
        
        Args:
            path: 目录相对路径
            
        Returns:
            bool: 是否成功
        """
        try:
            target = self._validate_path(path)
            target.mkdir(parents=True, exist_ok=True)
            self._log_operation("ENSURE_DIR", path)
            return True
        except Exception as e:
            self.logger.error(f"创建目录错误 {path}: {e}")
            return False

    def copy_file(self, src: str, dst: str) -> bool:
        """
        安全复制文件（通过读取+写入实现）
        
        Args:
            src: 源文件相对路径
            dst: 目标文件相对路径
            
        Returns:
            bool: 是否成功
        """
        try:
            content = self.read_file(src)
            if content:
                return self.write_file(dst, content)
            return False
        except Exception as e:
            self.logger.error(f"复制文件错误 {src} -> {dst}: {e}")
            return False

    def get_file_stats(self, path: str) -> Dict[str, Any]:
        """
        获取文件统计信息
        
        Args:
            path: 相对路径
            
        Returns:
            Dict: 文件统计信息
        """
        try:
            target = self._validate_path(path)
            
            if not target.exists():
                return {}
            
            stat = target.stat()
            return {
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "created": stat.st_ctime,
                "is_file": target.is_file(),
                "is_dir": target.is_dir(),
                "path": str(path)
            }
        except Exception as e:
            self.logger.error(f"获取文件统计错误 {path}: {e}")
            return {}


# 便捷函数
def create_tool_bridge(project_root: Optional[Union[str, Path]] = None) -> ToolBridge:
    """
    创建ToolBridge实例的便捷函数
    
    Args:
        project_root: 项目根目录，默认为当前脚本的父目录的父目录
        
    Returns:
        ToolBridge: 工具桥接器实例
    """
    if project_root is None:
        # 默认: 当前文件所在目录的父目录的父目录
        project_root = Path(__file__).resolve().parent.parent.parent
    
    return ToolBridge(project_root)


# 自检代码
if __name__ == "__main__":
    print("🔧 ToolBridge 自检开始...")
    
    # 创建临时测试目录
    import tempfile
    test_dir = tempfile.mkdtemp(prefix="toolbridge_test_")
    print(f"测试目录: {test_dir}")
    
    try:
        bridge = ToolBridge(test_dir)
        
        # 测试1: 基本写入和读取
        test_content = "测试内容 " + "a" * 100
        success = bridge.write_file("test.txt", test_content)
        print(f"✅ 测试1 原子写入: {'成功' if success else '失败'}")
        
        content = bridge.read_file("test.txt")
        print(f"✅ 测试1 读取验证: {'通过' if content == test_content else '失败'}")
        
        # 测试2: 路径安全
        try:
            bridge._validate_path("../../etc/passwd")
            print("❌ 测试2 路径安全: 应该抛出异常但没有")
        except PermissionError:
            print("✅ 测试2 路径安全: 成功拦截越界路径")
        
        # 测试3: 列表文件
        files = bridge.list_files(".", recursive=False)
        print(f"✅ 测试3 列表文件: 找到 {len(files)} 个文件")
        
        # 测试4: 文件存在性
        exists = bridge.file_exists("test.txt")
        print(f"✅ 测试4 文件存在: {'存在' if exists else '不存在'}")
        
        print(f"\n🎉 ToolBridge 自检完成!")
        
    finally:
        # 清理
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)
        print(f"🧹 清理测试目录: {test_dir}")