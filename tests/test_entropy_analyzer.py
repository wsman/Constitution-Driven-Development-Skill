#!/usr/bin/env python3
"""
测试 entropy_analyzer.py 的熵值分析功能

v0.1.0 - Phase 1 MVP 测试
"""

import pytest
import sys
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入被测模块
try:
    from scripts.utils.entropy_analyzer import (
        EntropyType,
        Hotspot,
        DiagnosticReport,
        EntropyAnalyzer,
        create_entropy_analyzer
    )
    IMPORT_SUCCESS = True
except ImportError as e:
    IMPORT_SUCCESS = False
    print(f"导入失败: {e}")


# 跳过测试如果导入失败
pytestmark = pytest.mark.skipif(
    not IMPORT_SUCCESS,
    reason="无法导入 entropy_analyzer 模块"
)


class TestEntropyType:
    """测试熵值类型枚举"""
    
    def test_enum_values(self):
        """测试枚举值"""
        assert EntropyType.STRUCTURAL.value == "structural"
        assert EntropyType.ALIGNMENT.value == "alignment"
        assert EntropyType.COGNITIVE.value == "cognitive"
    
    def test_enum_membership(self):
        """测试枚举成员"""
        assert EntropyType.STRUCTURAL in EntropyType
        assert EntropyType.ALIGNMENT in EntropyType
        assert EntropyType.COGNITIVE in EntropyType


class TestHotspot:
    """测试热点数据类"""
    
    def test_dataclass_creation(self):
        """测试数据类创建"""
        hotspot = Hotspot(
            id="test_id",
            path="src/",
            entropy_score=0.75,
            entropy_type=EntropyType.STRUCTURAL,
            reason="目录结构不符合预期",
            suggested_fix="创建缺失目录"
        )
        
        assert hotspot.id == "test_id"
        assert hotspot.path == "src/"
        assert hotspot.entropy_score == 0.75
        assert hotspot.entropy_type == EntropyType.STRUCTURAL
        assert hotspot.reason == "目录结构不符合预期"
        assert hotspot.suggested_fix == "创建缺失目录"
    
    def test_to_dict(self):
        """测试转换为字典"""
        hotspot = Hotspot(
            id="test_id",
            path="src/",
            entropy_score=0.75,
            entropy_type=EntropyType.STRUCTURAL,
            reason="测试原因",
            suggested_fix="测试修复"
        )
        
        result = hotspot.to_dict()
        
        assert result["id"] == "test_id"
        assert result["path"] == "src/"
        assert result["entropy_score"] == 0.75
        assert result["entropy_type"] == "structural"
        assert result["reason"] == "测试原因"
        assert result["suggested_fix"] == "测试修复"
    
    def test_to_dict_no_suggested_fix(self):
        """测试转换为字典（无修复建议）"""
        hotspot = Hotspot(
            id="test_id",
            path="src/",
            entropy_score=0.75,
            entropy_type=EntropyType.STRUCTURAL,
            reason="测试原因"
        )
        
        result = hotspot.to_dict()
        
        assert result["suggested_fix"] is None


class TestDiagnosticReport:
    """测试诊断报告数据类"""
    
    @pytest.fixture
    def sample_hotspots(self):
        """创建示例热点列表"""
        return [
            Hotspot(
                id="hotspot1",
                path="src/",
                entropy_score=0.8,
                entropy_type=EntropyType.STRUCTURAL,
                reason="目录缺失",
                suggested_fix="创建目录"
            ),
            Hotspot(
                id="hotspot2",
                path="tests/",
                entropy_score=0.6,
                entropy_type=EntropyType.STRUCTURAL,
                reason="文件多余",
                suggested_fix="删除文件"
            )
        ]
    
    def test_dataclass_creation(self, sample_hotspots):
        """测试数据类创建"""
        report = DiagnosticReport(
            timestamp="2026-02-06T01:30:00Z",
            global_entropy=0.65,
            hotspots=sample_hotspots,
            summary="发现2个结构熵热点"
        )
        
        assert report.timestamp == "2026-02-06T01:30:00Z"
        assert report.global_entropy == 0.65
        assert len(report.hotspots) == 2
        assert report.summary == "发现2个结构熵热点"
    
    def test_to_json(self, sample_hotspots):
        """测试转换为JSON格式"""
        report = DiagnosticReport(
            timestamp="2026-02-06T01:30:00Z",
            global_entropy=0.65,
            hotspots=sample_hotspots,
            summary="测试摘要"
        )
        
        result = report.to_json()
        
        assert result["timestamp"] == "2026-02-06T01:30:00Z"
        assert result["global_entropy"] == 0.65
        assert result["summary"] == "测试摘要"
        assert len(result["hotspots"]) == 2
        
        # 验证热点数据
        hotspot1 = result["hotspots"][0]
        assert hotspot1["id"] == "hotspot1"
        assert hotspot1["path"] == "src/"
        assert hotspot1["entropy_score"] == 0.8
        assert hotspot1["entropy_type"] == "structural"
    
    def test_to_markdown(self, sample_hotspots):
        """测试转换为Markdown格式"""
        report = DiagnosticReport(
            timestamp="2026-02-06T01:30:00Z",
            global_entropy=0.65,
            hotspots=sample_hotspots,
            summary="测试摘要"
        )
        
        result = report.to_markdown()
        
        # 验证基本结构
        assert "# CDD 熵值诊断报告" in result
        assert "**生成时间**: 2026-02-06T01:30:00Z" in result
        assert "**全局熵值**: 0.6500" in result
        assert "## 摘要" in result
        assert "测试摘要" in result
        assert "## 高熵热点 Top-10" in result
        
        # 验证表格
        assert "| 排名 | 路径 | 熵值贡献 | 类型 | 原因 | 建议 |" in result
        assert "| 1 | `src/` | 0.8000 | structural | 目录缺失 | 创建目录 |" in result
        assert "| 2 | `tests/` | 0.6000 | structural | 文件多余 | 删除文件 |" in result
        
        # 验证统计信息
        assert "**总热点数**: 2" in result
        assert "**报告版本**: v0.1.0" in result


class TestEntropyAnalyzer:
    """测试熵值分析器"""
    
    @pytest.fixture
    def temp_project(self):
        """创建临时测试项目"""
        temp_dir = tempfile.mkdtemp(prefix="entropy_test_")
        project_path = Path(temp_dir)
        
        # 创建基本目录结构
        (project_path / "templates" / "02_axioms").mkdir(parents=True, exist_ok=True)
        
        # 创建 system_patterns.md 文件
        patterns_content = """# 系统模式定义

## 目录结构

```bash
├── src/
│   ├── __init__.py
│   ├── core/
│   └── interfaces/
├── tests/
│   ├── __init__.py
│   └── unit/
└── docs/
    └── README.md
```
"""
        (project_path / "templates" / "02_axioms" / "system_patterns.md").write_text(patterns_content)
        
        yield project_path
        
        # 清理
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def analyzer(self, temp_project):
        """创建分析器实例"""
        return EntropyAnalyzer(temp_project)
    
    def test_initialization(self, analyzer, temp_project):
        """测试初始化"""
        assert analyzer.project_root == temp_project
        assert analyzer.tool_bridge is not None
        assert analyzer.cache is not None
        assert analyzer.system_patterns_file == temp_project / "templates/02_axioms/system_patterns.md"
        assert analyzer._cached_hotspots is None
        
        # 验证权重配置
        assert analyzer.STRUCT_WEIGHT_MISSING == 0.7
        assert analyzer.STRUCT_WEIGHT_EXTRA == 0.3
        assert analyzer.SORT_WEIGHT_SCORE == 0.6
        assert analyzer.SORT_WEIGHT_IMPACT == 0.3
        assert analyzer.SORT_WEIGHT_EASE == 0.1
    
    def test_initialization_nonexistent_project(self):
        """测试初始化（项目不存在）"""
        with pytest.raises(ValueError, match="项目根目录不存在"):
            EntropyAnalyzer("/nonexistent/path")
    
    def test_parse_system_patterns_success(self, analyzer):
        """测试解析系统模式文件（成功）"""
        patterns = analyzer._parse_system_patterns()
        
        # 验证解析结果
        assert isinstance(patterns, dict)
        assert "src" in patterns
        assert "tests" in patterns
        assert "docs" in patterns
    
    def test_parse_system_patterns_file_not_found(self, temp_project):
        """测试解析系统模式文件（文件不存在）"""
        # 删除文件
        (temp_project / "templates" / "02_axioms" / "system_patterns.md").unlink()
        
        analyzer = EntropyAnalyzer(temp_project)
        
        with pytest.raises(FileNotFoundError, match="系统模式文件不存在"):
            analyzer._parse_system_patterns()
    
    @patch('scripts.utils.entropy_analyzer.ToolBridge')
    def test_parse_system_patterns_no_tree_block(self, mock_tool_bridge, temp_project):
        """测试解析系统模式文件（无tree代码块）"""
        # 创建没有tree代码块的文件
        patterns_content = """# 系统模式定义

没有tree命令输出
"""
        (temp_project / "templates" / "02_axioms" / "system_patterns.md").write_text(patterns_content)
        
        analyzer = EntropyAnalyzer(temp_project)
        patterns = analyzer._parse_system_patterns()
        
        # 应该返回默认模式
        assert isinstance(patterns, dict)
        assert "src" in patterns
        assert "tests" in patterns
        assert "docs" in patterns
    
    def test_calculate_structural_score(self, analyzer):
        """测试计算结构熵分数"""
        # 测试缺失项为主的情况
        score = analyzer._calculate_structural_score(
            missing_count=3,
            extra_count=1,
            expected_total=10,
            actual_total=5
        )
        
        # 手动计算验证
        missing_ratio = 3 / 10  # 0.3
        extra_ratio = 1 / 5     # 0.2
        expected_score = 0.7 * 0.3 + 0.3 * 0.2  # 0.21 + 0.06 = 0.27
        
        assert abs(score - expected_score) < 0.001
        
        # 测试边界情况：除零
        score_zero = analyzer._calculate_structural_score(
            missing_count=0,
            extra_count=0,
            expected_total=0,
            actual_total=0
        )
        assert score_zero == 0.0
        
        # 测试边界情况：分数截断
        score_high = analyzer._calculate_structural_score(
            missing_count=100,
            extra_count=100,
            expected_total=1,
            actual_total=1
        )
        assert 0.0 <= score_high <= 1.0
    
    @patch.object(EntropyAnalyzer, '_parse_system_patterns')
    @patch('scripts.utils.entropy_analyzer.ToolBridge')
    def test_analyze_structural_entropy_missing_dir(self, mock_tool_bridge, mock_parse_patterns, analyzer):
        """测试分析结构熵（缺失目录）"""
        # 模拟预期模式
        mock_parse_patterns.return_value = {
            "src": ["__init__.py", "core/"],
            "tests": ["__init__.py", "unit/"]
        }
        
        # 模拟ToolBridge行为
        mock_bridge = Mock()
        mock_bridge.file_exists.side_effect = lambda path: path != "tests"  # tests目录不存在
        mock_bridge.list_files.return_value = []  # 空目录
        
        analyzer.tool_bridge = mock_bridge
        
        hotspots = analyzer.analyze_structural_entropy()
        
        # 应该发现tests目录缺失
        assert len(hotspots) == 1
        hotspot = hotspots[0]
        assert hotspot.path == "tests"
        assert hotspot.entropy_type == EntropyType.STRUCTURAL
        assert "目录缺失" in hotspot.reason
        assert hotspot.entropy_score == 0.8  # 缺失目录的高熵值
    
    @patch.object(EntropyAnalyzer, '_parse_system_patterns')
    @patch('scripts.utils.entropy_analyzer.ToolBridge')
    def test_analyze_structural_entropy_structure_violation(self, mock_tool_bridge, mock_parse_patterns, analyzer):
        """测试分析结构熵（结构违反）"""
        # 模拟预期模式
        mock_parse_patterns.return_value = {
            "src": ["__init__.py", "core/"]
        }
        
        # 模拟ToolBridge行为
        mock_bridge = Mock()
        mock_bridge.file_exists.return_value = True
        mock_bridge.list_files.return_value = ["src/extra_file.py", "src/missing_dir/"]
        
        analyzer.tool_bridge = mock_bridge
        
        # 模拟_get_directory_contents返回
        with patch.object(analyzer, '_get_directory_contents') as mock_get_contents:
            mock_get_contents.return_value = (
                ["extra_file.py"],  # 实际文件（多余）
                ["missing_dir"]     # 实际目录（多余）
            )
            
            hotspots = analyzer.analyze_structural_entropy()
        
        # 应该发现结构违反
        assert len(hotspots) == 1
        hotspot = hotspots[0]
        assert hotspot.path == "src"
        assert hotspot.entropy_type == EntropyType.STRUCTURAL
        assert "目录结构不符合预期" in hotspot.reason
    
    @patch.object(EntropyAnalyzer, '_parse_system_patterns')
    @patch('scripts.utils.entropy_analyzer.ToolBridge')
    def test_analyze_structural_entropy_no_system_patterns(self, mock_tool_bridge, mock_parse_patterns, analyzer):
        """测试分析结构熵（无系统模式文件）"""
        # 模拟文件不存在异常
        mock_parse_patterns.side_effect = FileNotFoundError("文件不存在")
        
        hotspots = analyzer.analyze_structural_entropy()
        
        # 应该返回空列表而不是崩溃
        assert hotspots == []
    
    def test_analyze_alignment_entropy_phase2(self, analyzer):
        """测试分析对齐熵（Phase 2 功能）"""
        hotspots = analyzer.analyze_alignment_entropy()
        
        # Phase 1 应该返回空列表
        assert hotspots == []
    
    def test_analyze_cognitive_entropy_phase3(self, analyzer):
        """测试分析认知熵（Phase 3 功能）"""
        hotspots = analyzer.analyze_cognitive_entropy()
        
        # Phase 1 应该返回空列表
        assert hotspots == []
    
    def test_sort_hotspots(self, analyzer):
        """测试热点排序"""
        hotspots = [
            Hotspot(
                id="low",
                path="path1",
                entropy_score=0.3,
                entropy_type=EntropyType.STRUCTURAL,
                reason="低熵"
            ),
            Hotspot(
                id="high",
                path="path2",
                entropy_score=0.8,
                entropy_type=EntropyType.STRUCTURAL,
                reason="高熵"
            ),
            Hotspot(
                id="medium",
                path="path3",
                entropy_score=0.5,
                entropy_type=EntropyType.STRUCTURAL,
                reason="中熵"
            )
        ]
        
        sorted_hotspots = analyzer._sort_hotspots(hotspots)
        
        # 应该按熵值降序排序
        assert len(sorted_hotspots) == 3
        assert sorted_hotspots[0].id == "high"  # 0.8
        assert sorted_hotspots[1].id == "medium"  # 0.5
        assert sorted_hotspots[2].id == "low"  # 0.3
    
    def test_sort_hotspots_empty(self, analyzer):
        """测试热点排序（空列表）"""
        sorted_hotspots = analyzer._sort_hotspots([])
        
        assert sorted_hotspots == []
    
    def test_calculate_global_entropy(self, analyzer):
        """测试计算全局熵值"""
        # 测试有热点的情况
        hotspots = [
            Hotspot(
                id="hotspot1",
                path="path1",
                entropy_score=0.8,
                entropy_type=EntropyType.STRUCTURAL,
                reason="测试"
            ),
            Hotspot(
                id="hotspot2",
                path="path2",
                entropy_score=0.6,
                entropy_type=EntropyType.STRUCTURAL,
                reason="测试"
            )
        ]
        
        global_entropy = analyzer._calculate_global_entropy(hotspots)
        
        # 验证计算逻辑
        avg_score = (0.8 + 0.6) / 2  # 0.7
        count_factor = min(2 / 20, 1.0)  # 0.1
        expected_entropy = avg_score * 0.7 + count_factor * 0.3  # 0.7*0.7 + 0.1*0.3 = 0.49 + 0.03 = 0.52
        
        assert abs(global_entropy - expected_entropy) < 0.001
        
        # 测试无热点的情况
        global_entropy_empty = analyzer._calculate_global_entropy([])
        assert global_entropy_empty == 0.0
        
        # 测试热点很多的情况（超过上限）
        many_hotspots = [Hotspot(
            id=f"hotspot{i}",
            path=f"path{i}",
            entropy_score=0.5,
            entropy_type=EntropyType.STRUCTURAL,
            reason="测试"
        ) for i in range(30)]
        
        global_entropy_many = analyzer._calculate_global_entropy(many_hotspots)
        assert 0.0 <= global_entropy_many <= 1.0
    
    @patch.object(EntropyAnalyzer, 'analyze_structural_entropy')
    @patch.object(EntropyAnalyzer, 'analyze_alignment_entropy')
    @patch.object(EntropyAnalyzer, 'analyze_cognitive_entropy')
    @patch.object(EntropyAnalyzer, '_calculate_global_entropy')
    def test_generate_diagnostic_report_json(self, mock_calc_entropy, mock_cog, mock_align, mock_struct, analyzer):
        """测试生成诊断报告（JSON格式）"""
        # 模拟分析结果
        mock_struct.return_value = [
            Hotspot(
                id="struct1",
                path="src/",
                entropy_score=0.8,
                entropy_type=EntropyType.STRUCTURAL,
                reason="结构问题"
            )
        ]
        mock_align.return_value = []
        mock_cog.return_value = []
        mock_calc_entropy.return_value = 0.65
        
        report = analyzer.generate_diagnostic_report(format="json", top_n=5)
        
        # 验证结果
        assert isinstance(report, dict)
        assert "timestamp" in report
        assert report["global_entropy"] == 0.65
        assert len(report["hotspots"]) == 1
        assert "发现 1 个熵值热点" in report["summary"]
    
    @patch.object(EntropyAnalyzer, 'analyze_structural_entropy')
    @patch.object(EntropyAnalyzer, 'analyze_alignment_entropy')
    @patch.object(EntropyAnalyzer, 'analyze_cognitive_entropy')
    @patch.object(EntropyAnalyzer, '_calculate_global_entropy')
    def test_generate_diagnostic_report_markdown(self, mock_calc_entropy, mock_cog, mock_align, mock_struct, analyzer):
        """测试生成诊断报告（Markdown格式）"""
        # 模拟分析结果
        mock_struct.return_value = [
            Hotspot(
                id="struct1",
                path="src/",
                entropy_score=0.8,
                entropy_type=EntropyType.STRUCTURAL,
                reason="结构问题",
                suggested_fix="修复"
            )
        ]
        mock_align.return_value = []
        mock_cog.return_value = []
        mock_calc_entropy.return_value = 0.9  # 高熵值
        
        report = analyzer.generate_diagnostic_report(format="markdown", top_n=5)
        
        # 验证结果
        assert isinstance(report, str)
        assert "# CDD 熵值诊断报告" in report
        assert "src/" in report
        assert "🔴 系统熵值偏高" in report  # 高熵值警告
    
    @patch.object(EntropyAnalyzer, 'analyze_structural_entropy')
    @patch.object(EntropyAnalyzer, 'analyze_alignment_entropy')
    @patch.object(EntropyAnalyzer, 'analyze_cognitive_entropy')
    @patch.object(EntropyAnalyzer, '_calculate_global_entropy')
    def test_generate_diagnostic_report_both(self, mock_calc_entropy, mock_cog, mock_align, mock_struct, analyzer):
        """测试生成诊断报告（双格式）"""
        # 模拟分析结果
        mock_struct.return_value = [
            Hotspot(
                id="struct1",
                path="src/",
                entropy_score=0.4,
                entropy_type=EntropyType.STRUCTURAL,
                reason="结构问题"
            )
        ]
        mock_align.return_value = []
        mock_cog.return_value = []
        mock_calc_entropy.return_value = 0.35  # 良好
        
        json_report, md_report = analyzer.generate_diagnostic_report(format="both", top_n=5)
        
        # 验证结果
        assert isinstance(json_report, dict)
        assert isinstance(md_report, str)
        assert json_report["global_entropy"] == 0.35
        assert "🟢 系统熵值良好" in md_report


class TestCreateEntropyAnalyzer:
    """测试便捷函数"""
    
    def test_create_with_custom_path(self, temp_project):
        """测试使用自定义路径创建"""
        analyzer = create_entropy_analyzer(temp_project)
        
        assert analyzer.project_root == temp_project
        assert analyzer.tool_bridge is not None
    
    def test_create_with_default_path(self):
        """测试使用默认路径创建"""
        with patch('pathlib.Path.cwd') as mock_cwd:
            mock_cwd.return_value = Path("/fake/path")
            analyzer = create_entropy_analyzer()
            
            assert analyzer.project_root == Path("/fake/path")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])