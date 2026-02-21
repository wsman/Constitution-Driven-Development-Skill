"""
CDD Asset Service (asset_service.py) v2.0.0
===========================================
技术资产管理服务的核心业务逻辑，支持科技部library/资产库的扫描、统计、版本管理。

宪法依据: §101单一真理源原则、§102熵减原则、§103文档优先公理

使用场景:
1. State A→B阶段：强制搜索现有技术资产
2. 资产贡献阶段：标准化资产入库流程
3. 资产审计阶段：定期检查资产质量和复用率
"""

import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass

from core.constants import SKILL_ROOT, DEFAULT_ENCODING, VERSION
from core.exceptions import CDDError
from utils.file_utils import safe_read_text, safe_write_text, find_files
from utils.cache_manager import CacheManager


@dataclass
class AssetMetrics:
    """资产指标数据类"""
    total_assets: int = 0
    by_type: Dict[str, int] = None
    avg_file_size: float = 0.0
    coverage: float = 0.0  # 资产类型覆盖率
    reuse_rate: float = 0.0  # 复用率（需要项目扫描）
    documentation_completeness: float = 0.0  # 文档完整性
    constitutional_compliance: float = 0.0  # 宪法合规性
    
    def __post_init__(self):
        if self.by_type is None:
            self.by_type = {}
    
    def to_dict(self) -> dict:
        return {
            "total_assets": self.total_assets,
            "by_type": self.by_type,
            "avg_file_size": round(self.avg_file_size, 2),
            "coverage": round(self.coverage, 4),
            "reuse_rate": round(self.reuse_rate, 4),
            "documentation_completeness": round(self.documentation_completeness, 4),
            "constitutional_compliance": round(self.constitutional_compliance, 4),
        }


@dataclass
class AssetInfo:
    """资产信息数据类"""
    path: Path
    name: str
    asset_type: str  # component, pattern, hook, standard, template, theme, test
    file_type: str  # jsx, tsx, js, ts, py, css, md
    size: int
    created_time: datetime
    modified_time: datetime
    constitutional_refs: List[str]
    dependencies: List[str]
    metadata: Dict[str, Any]
    
    @property
    def relative_path(self) -> str:
        """获取相对于library/的相对路径"""
        try:
            return str(self.path.relative_to(self.path.parents[2]))
        except:
            return str(self.path)
    
    @property
    def has_constitutional_compliance(self) -> bool:
        """检查宪法合规性"""
        required_refs = ["§101", "§102"]
        return all(ref in self.constitutional_refs for ref in required_refs)
    
    @property
    def is_theme_compliant(self) -> bool:
        """检查主题合规性（§119）"""
        if self.file_type in ["css", "jsx", "tsx"]:
            return "§119" in self.constitutional_refs
        return True
    
    def to_dict(self) -> dict:
        return {
            "path": str(self.relative_path),
            "name": self.name,
            "asset_type": self.asset_type,
            "file_type": self.file_type,
            "size": self.size,
            "created_time": self.created_time.isoformat(),
            "modified_time": self.modified_time.isoformat(),
            "constitutional_refs": self.constitutional_refs,
            "dependencies": self.dependencies,
            "metadata": self.metadata,
            "has_constitutional_compliance": self.has_constitutional_compliance,
            "is_theme_compliant": self.is_theme_compliant,
        }


class AssetScanner:
    """资产扫描器"""
    
    ASSET_TYPE_PATTERNS = {
        "component": ["components/", "ui/"],
        "pattern": ["patterns/"],
        "hook": ["hooks/"],
        "standard": ["standards/"],
        "template": ["templates/"],
        "theme": ["themes/"],
        "test": ["tests/"],
    }
    
    FILE_TYPE_PATTERNS = {
        "jsx": r"\.jsx$",
        "tsx": r"\.tsx$",
        "js": r"\.js$",
        "ts": r"\.ts$",
        "py": r"\.py$",
        "css": r"\.css$",
        "md": r"\.md$",
    }
    
    def __init__(self, library_root: Path, verbose: bool = False):
        self.library_root = library_root
        self.verbose = verbose
        self.cache = CacheManager(library_root)
    
    def log(self, msg: str):
        if self.verbose:
            print(f"[ASSET SCAN] {msg}")
    
    def scan_assets(self) -> List[AssetInfo]:
        """扫描所有资产"""
        self.log(f"开始扫描资产库: {self.library_root}")
        
        assets = []
        for file_path in self._find_asset_files():
            try:
                asset_info = self._analyze_file(file_path)
                if asset_info:
                    assets.append(asset_info)
                    self.log(f"  ✓ 发现资产: {asset_info.name} ({asset_info.asset_type})")
            except Exception as e:
                self.log(f"  ✗ 分析失败: {file_path} - {e}")
        
        self.log(f"扫描完成: 发现 {len(assets)} 个资产")
        return assets
    
    def _find_asset_files(self) -> List[Path]:
        """查找所有资产文件"""
        patterns = [
            "**/*.jsx", "**/*.tsx", "**/*.js", "**/*.ts",
            "**/*.py", "**/*.css", "**/*.md",
        ]
        
        files = []
        for pattern in patterns:
            for file_path in self.library_root.glob(pattern):
                # 跳过隐藏文件和缓存目录
                if file_path.name.startswith(".") or "__pycache__" in str(file_path):
                    continue
                files.append(file_path)
        
        return sorted(files, key=lambda p: str(p))
    
    def _analyze_file(self, file_path: Path) -> Optional[AssetInfo]:
        """分析单个文件"""
        if not file_path.exists():
            return None
        
        # 确定资产类型
        asset_type = self._determine_asset_type(file_path)
        if not asset_type:
            return None
        
        # 确定文件类型
        file_type = self._determine_file_type(file_path)
        
        # 获取文件统计信息
        stat = file_path.stat()
        
        # 分析内容
        content = safe_read_text(file_path)
        constitutional_refs = self._extract_constitutional_refs(content)
        dependencies = self._extract_dependencies(content)
        metadata = self._extract_metadata(content, file_type)
        
        return AssetInfo(
            path=file_path,
            name=file_path.stem,
            asset_type=asset_type,
            file_type=file_type,
            size=stat.st_size,
            created_time=datetime.fromtimestamp(stat.st_ctime),
            modified_time=datetime.fromtimestamp(stat.st_mtime),
            constitutional_refs=constitutional_refs,
            dependencies=dependencies,
            metadata=metadata,
        )
    
    def _determine_asset_type(self, file_path: Path) -> Optional[str]:
        """确定资产类型"""
        path_str = str(file_path)
        
        for asset_type, patterns in self.ASSET_TYPE_PATTERNS.items():
            for pattern in patterns:
                if pattern in path_str:
                    return asset_type
        
        # 默认类型
        return "standard" if "standard" in path_str else "unknown"
    
    def _determine_file_type(self, file_path: Path) -> str:
        """确定文件类型"""
        suffix = file_path.suffix.lower()
        
        for file_type, pattern in self.FILE_TYPE_PATTERNS.items():
            if re.search(pattern, suffix):
                return file_type
        
        return "unknown"
    
    def _extract_constitutional_refs(self, content: str) -> List[str]:
        """提取宪法引用"""
        pattern = r"§(\d{3}(?:\.\d+)?)"
        matches = re.findall(pattern, content)
        return [f"§{match}" for match in set(matches)]
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """提取依赖项"""
        dependencies = []
        
        # 提取导入语句
        import_patterns = [
            r"import\s+.*\s+from\s+['\"]([^'\"]+)['\"]",
            r"require\(['\"]([^'\"]+)['\"]\)",
            r"from\s+([a-zA-Z0-9_.]+)\s+import",
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            dependencies.extend(matches)
        
        # 提取组件引用
        component_pattern = r"<([A-Z][a-zA-Z0-9]+)\s"
        matches = re.findall(component_pattern, content)
        dependencies.extend(matches)
        
        return sorted(set(dependencies))
    
    def _extract_metadata(self, content: str, file_type: str) -> Dict[str, Any]:
        """提取元数据"""
        metadata = {
            "lines": len(content.splitlines()),
            "has_documentation": False,
            "has_examples": False,
            "has_tests": False,
        }
        
        # 检查文档
        doc_patterns = [
            r"#.*README|#.*文档|#.*Documentation",
            r"/\*\*.*\*/",  # JSDoc
            r'"""[\s\S]*?"""',  # Python docstring
        ]
        
        for pattern in doc_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                metadata["has_documentation"] = True
                break
        
        # 检查示例
        if "example" in content.lower() or "示例" in content:
            metadata["has_examples"] = True
        
        # 检查测试
        if "test" in content.lower() or "spec" in content.lower():
            metadata["has_tests"] = True
        
        return metadata


class AssetAnalyzer:
    """资产分析器"""
    
    def __init__(self, library_root: Path):
        self.library_root = library_root
        self.scanner = AssetScanner(library_root)
    
    def calculate_metrics(self, assets: List[AssetInfo]) -> AssetMetrics:
        """计算资产指标"""
        metrics = AssetMetrics()
        
        if not assets:
            return metrics
        
        # 基础统计
        metrics.total_assets = len(assets)
        
        # 按类型统计
        type_counts = {}
        for asset in assets:
            type_counts[asset.asset_type] = type_counts.get(asset.asset_type, 0) + 1
        metrics.by_type = type_counts
        
        # 平均文件大小
        total_size = sum(asset.size for asset in assets)
        metrics.avg_file_size = total_size / len(assets)
        
        # 资产类型覆盖率
        expected_types = 7  # component, pattern, hook, standard, template, theme, test
        actual_types = len(type_counts)
        metrics.coverage = actual_types / expected_types
        
        # 文档完整性（简化计算）
        docs_count = sum(1 for asset in assets if asset.metadata.get("has_documentation", False))
        metrics.documentation_completeness = docs_count / len(assets)
        
        # 宪法合规性
        compliant_count = sum(1 for asset in assets if asset.has_constitutional_compliance)
        metrics.constitutional_compliance = compliant_count / len(assets)
        
        return metrics
    
    def find_similar_assets(self, assets: List[AssetInfo], target_asset: AssetInfo) -> List[AssetInfo]:
        """查找相似资产（避免重复）"""
        similar = []
        
        for asset in assets:
            if asset.path == target_asset.path:
                continue
            
            # 简单的相似性判断
            similarity_score = self._calculate_similarity(asset, target_asset)
            if similarity_score > 0.7:  # 阈值
                similar.append(asset)
        
        return similar
    
    def _calculate_similarity(self, asset1: AssetInfo, asset2: AssetInfo) -> float:
        """计算资产相似度"""
        score = 0.0
        
        # 资产类型相同
        if asset1.asset_type == asset2.asset_type:
            score += 0.3
        
        # 文件类型相同
        if asset1.file_type == asset2.file_type:
            score += 0.2
        
        # 依赖项重叠
        dep1 = set(asset1.dependencies)
        dep2 = set(asset2.dependencies)
        if dep1 and dep2:
            overlap = len(dep1.intersection(dep2)) / len(dep1.union(dep2))
            score += overlap * 0.3
        
        # 名称相似
        name1 = asset1.name.lower()
        name2 = asset2.name.lower()
        if name1 in name2 or name2 in name1:
            score += 0.2
        
        return min(score, 1.0)
    
    def generate_reuse_suggestions(self, assets: List[AssetInfo], project_path: Path) -> List[Dict[str, Any]]:
        """生成复用建议"""
        suggestions = []
        
        # 扫描项目文件
        project_files = self._scan_project_files(project_path)
        
        for asset in assets:
            # 检查资产是否在项目中使用
            is_used = self._check_asset_usage(asset, project_files)
            
            if not is_used:
                suggestions.append({
                    "asset": asset.name,
                    "type": asset.asset_type,
                    "path": asset.relative_path,
                    "suggestion": f"考虑复用 {asset.name} ({asset.asset_type})",
                    "reason": "相似功能未在项目中使用",
                })
        
        return suggestions
    
    def _scan_project_files(self, project_path: Path) -> List[str]:
        """扫描项目文件"""
        patterns = ["**/*.jsx", "**/*.tsx", "**/*.js", "**/*.ts", "**/*.py"]
        
        files = []
        for pattern in patterns:
            for file_path in project_path.glob(pattern):
                if file_path.is_file():
                    files.append(str(file_path))
        
        return files
    
    def _check_asset_usage(self, asset: AssetInfo, project_files: List[str]) -> bool:
        """检查资产是否在项目中使用"""
        asset_name = asset.name
        
        for file_path in project_files:
            try:
                content = safe_read_text(Path(file_path))
                if asset_name in content:
                    return True
            except:
                continue
        
        return False


class AssetRepository:
    """资产仓库管理器"""
    
    def __init__(self, library_root: Path):
        self.library_root = library_root
        self.scanner = AssetScanner(library_root)
        self.analyzer = AssetAnalyzer(library_root)
    
    def get_asset_report(self, format: str = "json") -> Dict[str, Any]:
        """获取资产报告"""
        assets = self.scanner.scan_assets()
        metrics = self.analyzer.calculate_metrics(assets)
        
        report = {
            "version": VERSION,
            "timestamp": datetime.now().isoformat(),
            "library_root": str(self.library_root),
            "metrics": metrics.to_dict(),
            "assets": [asset.to_dict() for asset in assets],
            "summary": {
                "total_assets": len(assets),
                "asset_types": len(metrics.by_type),
                "constitutional_compliance": metrics.constitutional_compliance,
                "documentation_completeness": metrics.documentation_completeness,
            }
        }
        
        return report
    
    def search_assets(self, query: str, asset_type: Optional[str] = None) -> List[AssetInfo]:
        """搜索资产"""
        assets = self.scanner.scan_assets()
        
        results = []
        for asset in assets:
            # 类型过滤
            if asset_type and asset.asset_type != asset_type:
                continue
            
            # 搜索匹配
            if (query.lower() in asset.name.lower() or 
                query.lower() in str(asset.path).lower() or
                any(query.lower() in dep.lower() for dep in asset.dependencies)):
                results.append(asset)
        
        return results
    
    def validate_new_asset(self, asset_path: Path, content: str) -> Dict[str, Any]:
        """验证新资产"""
        errors = []
        warnings = []
        
        # 检查宪法引用
        if "§101" not in content:
            errors.append("缺少§101单一真理源引用")
        if "§102" not in content:
            errors.append("缺少§102熵减原则引用")
        
        # 检查§119主题合规性
        if asset_path.suffix.lower() in [".css", ".jsx", ".tsx"]:
            if "§119" not in content:
                warnings.append("建议添加§119主题驱动开发引用")
            
            # 检查硬编码颜色
            hardcoded_colors = re.findall(r"#[0-9a-fA-F]{3,6}", content)
            if hardcoded_colors:
                errors.append(f"发现硬编码颜色（违反§119）: {', '.join(hardcoded_colors)}")
        
        # 检查文档
        if not ("#" in content or "/**" in content or '"""' in content):
            warnings.append("建议添加文档注释")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": [
                "在文件头部添加宪法引用注释",
                "确保使用Nordic主题变量（而非硬编码颜色）",
                "添加完整的API文档",
            ]
        }


class AssetService:
    """资产服务主类"""
    
    def __init__(self, library_root: Optional[Path] = None):
        self.library_root = library_root or SKILL_ROOT.parent.parent / "library"
        self.repository = AssetRepository(self.library_root)
    
    def scan_assets(self, verbose: bool = False) -> Dict[str, Any]:
        """
        扫描技术资产库
        
        Args:
            verbose: 详细输出模式
            
        Returns:
            Dict[str, Any]: 扫描结果
        """
        try:
            scanner = AssetScanner(self.library_root, verbose=verbose)
            assets = scanner.scan_assets()
            metrics = AssetAnalyzer(self.library_root).calculate_metrics(assets)
            
            return {
                "success": True,
                "library_root": str(self.library_root),
                "assets_found": len(assets),
                "metrics": metrics.to_dict(),
                "asset_types": metrics.by_type,
                "constitutional_compliance": metrics.constitutional_compliance,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"资产扫描失败: {e}",
                "library_root": str(self.library_root),
                "suggestions": [
                    "检查library/目录是否存在且可访问",
                    "确认有足够的文件权限",
                    "尝试手动检查目录结构",
                ]
            }
    
    def generate_report(self, format: str = "json") -> Dict[str, Any]:
        """
        生成资产报告
        
        Args:
            format: 报告格式（json/text）
            
        Returns:
            Dict[str, Any]: 资产报告
        """
        try:
            report = self.repository.get_asset_report(format=format)
            return {
                "success": True,
                "report": report,
                "formatted": format == "text"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"报告生成失败: {e}",
                "suggestions": [
                    "确保资产扫描功能正常工作",
                    "检查library/目录结构完整性",
                    "验证文件读取权限",
                ]
            }
    
    def search(self, query: str, asset_type: Optional[str] = None) -> Dict[str, Any]:
        """
        搜索资产
        
        Args:
            query: 搜索查询
            asset_type: 资产类型过滤
            
        Returns:
            Dict[str, Any]: 搜索结果
        """
        try:
            results = self.repository.search_assets(query, asset_type)
            
            return {
                "success": True,
                "query": query,
                "asset_type": asset_type,
                "results_found": len(results),
                "results": [r.to_dict() for r in results],
                "suggestions": [
                    "尝试更具体的查询词",
                    "使用资产类型过滤提高精确度",
                    "检查资产名称拼写",
                ]
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"搜索失败: {e}",
                "query": query,
                "asset_type": asset_type,
            }
    
    def validate(self, asset_path: str, content: str) -> Dict[str, Any]:
        """
        验证新资产
        
        Args:
            asset_path: 资产路径
            content: 资产内容
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            result = self.repository.validate_new_asset(Path(asset_path), content)
            return {
                "success": True,
                "validation": result,
                "compliance_required": True,
                "theme_compliance_required": Path(asset_path).suffix.lower() in [".css", ".jsx", ".tsx"],
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"验证失败: {e}",
                "asset_path": asset_path,
            }
    
    def suggest_reuse(self, project_path: str) -> Dict[str, Any]:
        """
        生成资产复用建议
        
        Args:
            project_path: 项目路径
            
        Returns:
            Dict[str, Any]: 复用建议
        """
        try:
            project_root = Path(project_path).resolve()
            
            # 扫描资产
            scanner = AssetScanner(self.library_root)
            assets = scanner.scan_assets()
            
            # 生成建议
            analyzer = AssetAnalyzer(self.library_root)
            suggestions = analyzer.generate_reuse_suggestions(assets, project_root)
            
            return {
                "success": True,
                "project_path": str(project_root),
                "assets_scanned": len(assets),
                "suggestions_found": len(suggestions),
                "suggestions": suggestions,
                "recommendations": [
                    "在State A→B阶段优先考虑现有资产",
                    "定期更新资产库以提高复用率",
                    "建立资产质量评估标准",
                ]
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"复用建议生成失败: {e}",
                "project_path": project_path,
            }