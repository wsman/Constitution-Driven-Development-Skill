"""hello 模块测试 - 演示 CDD 行为验证"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.hello import greet, get_version


class TestGreet:
    """问候功能测试"""
    
    def test_greet_with_name(self):
        """测试带名字的问候"""
        result = greet("World")
        assert "World" in result
        assert len(result) > 0
    
    def test_greet_empty_name(self):
        """测试空名字的边界情况"""
        result = greet("")
        assert len(result) > 0  # 应返回默认问候
        assert "CDD" in result  # 默认问候包含 CDD
    
    def test_greet_chinese_name(self):
        """测试中文名字"""
        result = greet("世界")
        assert "世界" in result


class TestGetVersion:
    """版本获取测试"""
    
    def test_get_version(self):
        """测试版本号格式"""
        version = get_version()
        # 版本格式: X.Y.Z
        parts = version.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)
    
    def test_version_not_empty(self):
        """测试版本号非空"""
        version = get_version()
        assert len(version) > 0