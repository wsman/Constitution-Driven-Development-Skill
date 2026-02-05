#!/usr/bin/env python3
"""
CDD 熵值分析器 (Entropy Analyzer)
================================
Phase 1 MVP: 结构熵 ($H_{struct}$) 热点分析

宪法依据:
- §300.1 孢子协议: 所有文件操作通过 ToolBridge
- §438 工具调用公理: 复用现有工具链架构
- §201.5 熵减公理: 分析过程零副作用

版本: v0.1.0 (MVP)
"""

import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, UTC
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

from .tool_bridge import create_tool_bridge, ToolBridge
from .cache_manager import CacheManager


class EntropyType(Enum):
    """熵值类型枚举"""
    STRUCTURAL = "structural"
    ALIGNMENT = "alignment"
    COGNITIVE = "cognitive"


@dataclass
class Hotspot:
    """熵值热点数据类"""
    id: str
    path: str
    entropy_score: float
    entropy_type: EntropyType
    reason: str
    suggested_fix: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['entropy_type'] = self.entropy_type.value
        return data


@dataclass
class DiagnosticReport:
    """诊断报告数据类"""
    timestamp: str
    global_entropy: float
    hotspots: List[Hotspot]
    summary: str
    
    def to_json(self) -> Dict[str, Any]:
        """转换为JSON格式"""
        return {
            "timestamp": self.timestamp,
            "global_entropy": round(self.global_entropy, 4),
            "hotspots": [h.to_dict() for h in self.hotspots],
            "summary": self.summary
        }
    
    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        md = f"""# CDD 熵值诊断报告

**生成时间**: {self.timestamp}
**全局熵值**: {self.global_entropy:.4f}

## 摘要
{self.summary}

## 高熵热点 Top-10

| 排名 | 路径 | 熵值贡献 | 类型 | 原因 | 建议 |
|------|------|----------|------|------|------|
"""
        for i, hotspot in enumerate(self.hotspots[:10], 1):
            md += f"| {i} | `{hotspot.path}` | {hotspot.entropy_score:.4f} | {hotspot.entropy_type.value} | {hotspot.reason} | {hotspot.suggested_fix or 'N/A'} |\n"
        
        md += f"\n**总热点数**: {len(self.hotspots)}\n"
        md += f"**报告版本**: v0.1.0 (CDD 熵值分析器 MVP)\n"
        
        return md


class EntropyAnalyzer:
    """
    CDD 熵值分析器 - MVP Phase 1
    
    核心功能:
    1. 结构熵 ($H_{struct}$) 分析
    2. 安全文件访问 (通过 ToolBridge)
    3. 缓存优化 (通过 CacheManager)
    4. 双格式输出 (JSON + Markdown)
    """
    
    # 结构熵权重配置
    STRUCT_WEIGHT_MISSING = 0.7  # 缺失文件比多余文件更严重
    STRUCT_WEIGHT_EXTRA = 0.3
    
    # 热点排序权重
    SORT_WEIGHT_SCORE = 0.6
    SORT_WEIGHT_IMPACT = 0.3
    SORT_WEIGHT_EASE = 0.1
    
    def __init__(self, project_root: Union[str, Path]):
        """
        初始化熵值分析器
        
        Args:
            project_root: 项目根目录
            
        Raises:
            ValueError: 项目根目录不存在
        """
        self.project_root = Path(project_root).resolve()
        if not self.project_root.exists():
            raise ValueError(f"项目根目录不存在: {self.project_root}")
        
        # 宪法合规: 所有文件操作通过 ToolBridge
        self.tool_bridge = create_tool_bridge(self.project_root)
        
        # 性能优化: 使用缓存管理器
        self.cache = CacheManager(self.project_root)
        
        # 系统模式文件路径
        self.system_patterns_file = self.project_root / "templates/t1_axioms/system_patterns.md"
        
        # 分析结果缓存
        self._cached_hotspots: Optional[List[Hotspot]] = None
    
    def _parse_system_patterns(self) -> Dict[str, List[str]]:
        """
        解析 system_patterns.md，提取预期的目录结构
        
        Returns:
            字典: {目录路径: [预期子项列表]}
            
        Raises:
            FileNotFoundError: system_patterns.md 不存在
        """
        if not self.system_patterns_file.exists():
            raise FileNotFoundError(
                f"系统模式文件不存在: {self.system_patterns_file}\n"
                "请确保 templates/t1_axioms/system_patterns.md 存在。"
            )
        
        content = self.tool_bridge.read_file(
            str(self.system_patterns_file.relative_to(self.project_root))
        )
        
        patterns = {}
        current_dir = None
        
        # 简单解析：查找代码块中的目录结构
        lines = content.split('\n')
        in_tree_block = False
        
        for line in lines:
            # 检测 tree 命令输出块
            if '```bash' in line and 'tree' in content:
                in_tree_block = True
                continue
            if in_tree_block and line.strip() == '```':
                in_tree_block = False
                continue
            
            if in_tree_block:
                # 解析 tree 输出格式
                # 示例: "├── src/"
                line = line.strip()
                if line.startswith(('├──', '└──', '│   ')):
                    # 提取路径
                    path = line.replace('├──', '').replace('└──', '').replace('│   ', '').strip()
                    if path.endswith('/'):  # 目录
                        patterns.setdefault(path.rstrip('/'), [])
        
        # 如果没有找到 tree 输出，使用简单的默认模式
        if not patterns:
            patterns = {
                "src": ["__init__.py", "core/", "interfaces/", "infrastructure/", "shared/"],
                "tests": ["__init__.py", "unit/", "integration/", "contract/"],
                "docs": ["README.md", "api/", "guides/"]
            }
        
        return patterns
    
    def _calculate_structural_score(self, 
                                   missing_count: int, 
                                   extra_count: int,
                                   expected_total: int,
                                   actual_total: int) -> float:
        """
        计算结构熵贡献分数
        
        公式: score = w_missing * (missing/expected) + w_extra * (extra/actual)
        
        Args:
            missing_count: 缺失的预期项数
            extra_count: 多余的未定义项数
            expected_total: 预期总项数
            actual_total: 实际总项数
            
        Returns:
            float: 熵贡献分数 [0.0, 1.0]
        """
        if expected_total == 0:
            missing_ratio = 0.0
        else:
            missing_ratio = missing_count / expected_total
        
        if actual_total == 0:
            extra_ratio = 0.0
        else:
            extra_ratio = extra_count / actual_total
        
        score = (self.STRUCT_WEIGHT_MISSING * missing_ratio +
                 self.STRUCT_WEIGHT_EXTRA * extra_ratio)
        
        return min(max(score, 0.0), 1.0)
    
    def _get_directory_contents(self, dir_path: str) -> Tuple[List[str], List[str]]:
        """
        获取目录内容（通过 ToolBridge）
        
        Args:
            dir_path: 目录相对路径
            
        Returns:
            (files, directories): 文件列表和目录列表
        """
        all_items = self.tool_bridge.list_files(dir_path, recursive=False)
        
        files = []
        dirs = []
        
        for item in all_items:
            # 转换为相对于当前目录的路径
            rel_item = Path(item)
            if dir_path != ".":
                # 处理相对路径
                try:
                    rel_item = rel_item.relative_to(dir_path)
                except ValueError:
                    continue
            
            # 检查是文件还是目录
            full_path = self.project_root / item
            if full_path.is_file():
                files.append(str(rel_item))
            else:
                dirs.append(str(rel_item))
        
        return files, dirs
    
    def analyze_structural_entropy(self) -> List[Hotspot]:
        """
        分析结构熵 ($H_{struct}$) 热点
        
        实现逻辑:
        1. 读取 system_patterns.md 中的预期结构
        2. 扫描实际目录结构
        3. 识别缺失项和多余项
        4. 计算每个目录的熵贡献
        
        Returns:
            List[Hotspot]: 结构熵热点列表
        """
        print("🔍 分析结构熵 ($H_{struct}$)...")
        
        try:
            expected_patterns = self._parse_system_patterns()
        except FileNotFoundError as e:
            print(f"⚠️  {e}")
            # 返回空热点列表，而不是崩溃
            return []
        
        hotspots = []
        
        for expected_dir, expected_items in expected_patterns.items():
            # 检查目录是否存在
            if not self.tool_bridge.file_exists(expected_dir):
                # 整个目录缺失是严重问题
                hotspot = Hotspot(
                    id=f"struct_missing_dir_{expected_dir}",
                    path=expected_dir,
                    entropy_score=0.8,  # 高熵值
                    entropy_type=EntropyType.STRUCTURAL,
                    reason=f"目录缺失: 预期目录 '{expected_dir}' 不存在",
                    suggested_fix=f"创建目录: mkdir -p {expected_dir}"
                )
                hotspots.append(hotspot)
                continue
            
            # 获取实际内容
            actual_files, actual_dirs = self._get_directory_contents(expected_dir)
            actual_items = actual_files + [d + '/' for d in actual_dirs]
            
            # 规范化预期项（目录添加斜杠）
            normalized_expected = []
            for item in expected_items:
                if item.endswith('/'):
                    normalized_expected.append(item)
                else:
                    normalized_expected.append(item)
            
            # 识别缺失项
            missing_items = [item for item in normalized_expected 
                           if item not in actual_items]
            
            # 识别多余项
            extra_items = [item for item in actual_items 
                          if item not in normalized_expected]
            
            # 计算熵贡献
            if normalized_expected or actual_items:
                score = self._calculate_structural_score(
                    missing_count=len(missing_items),
                    extra_count=len(extra_items),
                    expected_total=len(normalized_expected),
                    actual_total=len(actual_items)
                )
                
                if score > 0.1:  # 只报告显著的热点
                    # 生成原因描述
                    reason_parts = []
                    if missing_items:
                        reason_parts.append(f"缺失 {len(missing_items)} 项")
                    if extra_items:
                        reason_parts.append(f"多余 {len(extra_items)} 项")
                    
                    reason = f"目录结构不符合预期: {', '.join(reason_parts)}"
                    
                    # 生成修复建议
                    suggestions = []
                    if missing_items:
                        suggestions.append(f"创建缺失项: {', '.join(missing_items[:3])}")
                    if extra_items:
                        suggestions.append(f"检查多余项: {', '.join(extra_items[:3])}")
                    
                    suggested_fix = "; ".join(suggestions) if suggestions else None
                    
                    hotspot = Hotspot(
                        id=f"struct_{expected_dir}_{hash(str(missing_items) + str(extra_items)) % 10000:04d}",
                        path=expected_dir,
                        entropy_score=score,
                        entropy_type=EntropyType.STRUCTURAL,
                        reason=reason,
                        suggested_fix=suggested_fix
                    )
                    hotspots.append(hotspot)
        
        # 检查预期外的目录（未在 system_patterns.md 中定义）
        all_dirs = self.tool_bridge.list_files(".", recursive=True)
        all_dirs = [d for d in all_dirs if Path(d).is_dir()]
        
        for actual_dir in all_dirs:
            if actual_dir not in expected_patterns and actual_dir != ".":
                # 这是未定义的目录，可能是冗余的
                # 检查是否为空目录
                dir_files, sub_dirs = self._get_directory_contents(actual_dir)
                if not dir_files and not sub_dirs:
                    # 空目录 - 低熵贡献
                    score = 0.2
                else:
                    # 非空未定义目录 - 中等熵贡献
                    score = 0.4
                
                hotspot = Hotspot(
                    id=f"struct_extra_dir_{actual_dir.replace('/', '_')}",
                    path=actual_dir,
                    entropy_score=score,
                    entropy_type=EntropyType.STRUCTURAL,
                    reason=f"未定义的目录: 不在 system_patterns.md 中",
                    suggested_fix=f"评估目录必要性，或添加到 system_patterns.md"
                )
                hotspots.append(hotspot)
        
        # 热点排序
        hotspots = self._sort_hotspots(hotspots)
        
        print(f"✅ 结构熵分析完成: 发现 {len(hotspots)} 个热点")
        return hotspots
    
    def analyze_alignment_entropy(self) -> List[Hotspot]:
        """
        分析对齐熵 ($H_{align}$) 热点 (Phase 2 功能)
        
        Returns:
            List[Hotspot]: 对齐熵热点列表
        """
        print("⚠️  对齐熵分析将在 Phase 2 实现")
        return []
    
    def analyze_cognitive_entropy(self) -> List[Hotspot]:
        """
        分析认知熵 ($H_{cog}$) 热点 (Phase 3 功能)
        
        Returns:
            List[Hotspot]: 认知熵热点列表
        """
        print("⚠️  认知熵分析将在 Phase 3 实现")
        return []
    
    def _sort_hotspots(self, hotspots: List[Hotspot]) -> List[Hotspot]:
        """
        热点排序算法
        
        公式: priority = α·score + β·impact + γ·ease
        其中 impact ≈ 1.0 (简化), ease ≈ 0.5 (默认)
        
        Args:
            hotspots: 原始热点列表
            
        Returns:
            List[Hotspot]: 排序后的热点列表
        """
        if not hotspots:
            return []
        
        # 计算每个热点的优先级
        prioritized = []
        for hotspot in hotspots:
            # 简化版本: 只使用分数
            priority = hotspot.entropy_score
            prioritized.append((priority, hotspot))
        
        # 按优先级降序排序
        prioritized.sort(key=lambda x: x[0], reverse=True)
        
        return [hotspot for _, hotspot in prioritized]
    
    def _calculate_global_entropy(self, hotspots: List[Hotspot]) -> float:
        """
        基于热点计算全局熵值
        
        Args:
            hotspots: 所有热点列表
            
        Returns:
            float: 全局熵值 [0.0, 1.0]
        """
        if not hotspots:
            return 0.0
        
        # 使用热点分数的加权平均
        total_score = sum(h.entropy_score for h in hotspots)
        avg_score = total_score / len(hotspots)
        
        # 应用对数衰减：热点越多，全局熵值越高
        count_factor = min(len(hotspots) / 20, 1.0)  # 20个热点为上限
        
        global_entropy = avg_score * 0.7 + count_factor * 0.3
        
        return min(max(global_entropy, 0.0), 1.0)
    
    def generate_diagnostic_report(self, 
                                  format: str = "both",
                                  top_n: int = 10) -> Union[Dict[str, Any], str, Tuple[Dict[str, Any], str]]:
        """
        生成诊断报告
        
        Args:
            format: 输出格式 ("json", "markdown", "both")
            top_n: 报告中的热点数量限制
            
        Returns:
            根据 format 返回相应格式的数据
        """
        print("📊 生成熵值诊断报告...")
        
        # 分析所有熵类型（当前只有结构熵）
        structural_hotspots = self.analyze_structural_entropy()
        alignment_hotspots = self.analyze_alignment_entropy()
        cognitive_hotspots = self.analyze_cognitive_entropy()
        
        # 合并热点
        all_hotspots = (structural_hotspots + 
                       alignment_hotspots + 
                       cognitive_hotspots)
        
        # 全局熵值
        global_entropy = self._calculate_global_entropy(all_hotspots)
        
        # 生成摘要
        summary_parts = []
        if structural_hotspots:
            summary_parts.append(f"结构熵热点: {len(structural_hotspots)} 个")
        if alignment_hotspots:
            summary_parts.append(f"对齐熵热点: {len(alignment_hotspots)} 个")
        if cognitive_hotspots:
            summary_parts.append(f"认知熵热点: {len(cognitive_hotspots)} 个")
        
        summary = f"发现 {len(all_hotspots)} 个熵值热点。{', '.join(summary_parts)}。"
        
        if global_entropy > 0.7:
            summary += " 🔴 系统熵值偏高，建议立即优化。"
        elif global_entropy > 0.5:
            summary += " 🟡 系统熵值中等，建议近期优化。"
        elif global_entropy > 0.3:
            summary += " 🟢 系统熵值良好，保持当前状态。"
        else:
            summary += " 🟢 系统熵值优秀，继续保持。"
        
        # 限制热点数量 - 确保 top_n 是整数
        try:
            top_n_int = int(top_n) if top_n is not None else 10
            limited_hotspots = all_hotspots[:top_n_int]
        except (ValueError, TypeError):
            # 如果无法转换为整数，使用默认值
            limited_hotspots = all_hotspots[:10]
        
        # 创建报告 - 修复 datetime 弃用警告
        report = DiagnosticReport(
            timestamp=datetime.now(UTC).isoformat() + "Z",
            global_entropy=global_entropy,
            hotspots=limited_hotspots,
            summary=summary
        )
        
        if format == "json":
            return report.to_json()
        elif format == "markdown":
            return report.to_markdown()
        else:  # "both"
            return report.to_json(), report.to_markdown()


# 便捷函数
def create_entropy_analyzer(project_root: Optional[Union[str, Path]] = None) -> EntropyAnalyzer:
    """
    创建熵值分析器实例的便捷函数
    
    Args:
        project_root: 项目根目录，默认为当前工作目录
        
    Returns:
        EntropyAnalyzer: 熵值分析器实例
    """
    if project_root is None:
        # 默认: 当前工作目录
        project_root = Path.cwd()
    
    return EntropyAnalyzer(project_root)


# 自检代码
if __name__ == "__main__":
    print("🔧 EntropyAnalyzer 自检开始...")
    
    import tempfile
    test_dir = tempfile.mkdtemp(prefix="entropy_test_")
    print(f"测试目录: {test_dir}")
    
    try:
        # 创建测试项目结构
        test_root = Path(test_dir)
        (test_root / "templates/t1_axioms").mkdir(parents=True, exist_ok=True)
        
        # 创建简单的 system_patterns.md
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
        (test_root / "templates/t1_axioms/system_patterns.md").write_text(patterns_content)
        
        # 创建部分预期目录
        (test_root / "src").mkdir(exist_ok=True)
        (test_root / "tests").mkdir(exist_ok=True)
        (test_root / "src/core").mkdir(exist_ok=True)
        
        # 缺失: src/interfaces, docs/, tests/unit
        # 多余: extra_dir/
        (test_root / "extra_dir").mkdir(exist_ok=True)
        
        # 测试分析器
        analyzer = EntropyAnalyzer(test_root)
        
        # 测试结构熵分析
        hotspots = analyzer.analyze_structural_entropy()
        print(f"✅ 结构熵分析: 发现 {len(hotspots)} 个热点")
        
        for i, hotspot in enumerate(hotspots[:3], 1):
            print(f"  热点 {i}: {hotspot.path} (得分: {hotspot.entropy_score:.2f})")
        
        # 测试报告生成
        json_report, md_report = analyzer.generate_diagnostic_report(format="both", top_n=5)
        print(f"✅ 报告生成: JSON大小={len(str(json_report))} 字符, Markdown行数={md_report.count(chr(10))+1}")
        
        print(f"\n🎉 EntropyAnalyzer 自检完成!")
        
    finally:
        # 清理
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)
        print(f"🧹 清理测试目录: {test_dir}")