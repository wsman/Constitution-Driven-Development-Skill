#!/usr/bin/env python3
"""
CDD Architect (cdd_architect.py) v1.0.0 - 修复版
=========================================
架构决策记录工具，用于创建、管理和跟踪架构决策记录（ADR）。

宪法依据: §101单一真理源原则、§102熵减原则、§103文档优先公理、§151持久化原则

使用场景:
1. State B规划阶段：记录关键架构决策
2. 技术设计评审：提供结构化决策记录
3. 架构演进追踪：跟踪决策状态和影响
4. 知识传承：为团队提供决策上下文

Usage:
    python scripts/cdd_architect.py create <title> [--status STATUS] [--context CONTEXT] [--verbose]
    python scripts/cdd_architect.py list [--status STATUS] [--verbose]
    python scripts/cdd_architect.py view <adr_id> [--format json|markdown] [--verbose]
    python scripts/cdd_architect.py update <adr_id> [--status STATUS] [--note NOTE] [--verbose]
    python scripts/cdd_architect.py analyze [--json] [--verbose]
    python scripts/cdd_architect.py template [--output FILE] [--type TYPE] [--verbose]

示例:
    python scripts/cdd_architect.py create "使用React Hooks替代Class组件" --status proposed
    python scripts/cdd_architect.py list --status accepted --verbose
    python scripts/cdd_architect.py view adr-001 --format markdown
    python scripts/cdd_architect.py update adr-001 --status accepted --note "团队评审通过"
    python scripts/cdd_architect.py analyze --json
    python scripts/cdd_architect.py template --output adr-template.md
"""

import sys
import os
import re
import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime
import uuid
from enum import Enum

# 添加项目根目录到Python路径
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SKILL_ROOT))

VERSION = "2.0.0"

# -----------------------------------------------------------------------------
# 常量定义
# -----------------------------------------------------------------------------

class ADRStatus(Enum):
    """架构决策记录状态枚举"""
    PROPOSED = "proposed"      # 提案中
    ACCEPTED = "accepted"      # 已接受
    SUPERSEDED = "superseded"  # 已替代
    DEPRECATED = "deprecated"  # 已废弃
    REJECTED = "rejected"      # 已拒绝

class DecisionImpact(Enum):
    """决策影响级别枚举"""
    LOW = "low"        # 低影响：局部影响，易于修改
    MEDIUM = "medium"  # 中影响：模块级影响
    HIGH = "high"      # 高影响：系统级影响
    CRITICAL = "critical"  # 关键影响：架构级影响

class DecisionScope(Enum):
    """决策范围枚举"""
    COMPONENT = "component"    # 组件级
    MODULE = "module"          # 模块级
    SYSTEM = "system"          # 系统级
    ARCHITECTURE = "architecture"  # 架构级

# 宪法条款与架构决策的映射
CONSTITUTION_ARCHITECTURE_MAPPING = {
    "§101": ["单一真理源原则", "配置管理", "文档一致性"],
    "§102": ["熵减原则", "复杂性管理", "技术债务控制"],
    "§103": ["文档优先公理", "设计文档", "规格说明"],
    "§119": ["主题驱动开发", "UI一致性", "设计系统"],
    "§151": ["持久化原则", "数据存储", "审计日志"],
    "§306": ["零停机部署", "部署架构", "高可用性"],
    "§320": ["Claude Code原则", "工具选择", "开发流程"]
}

# 架构决策类别
ARCHITECTURE_CATEGORIES = [
    "技术栈选型",
    "架构模式",
    "数据存储",
    "API设计",
    "部署架构",
    "安全设计",
    "性能优化",
    "可维护性",
    "可扩展性",
    "兼容性",
    "开发流程",
    "监控告警"
]

# -----------------------------------------------------------------------------
# 核心模型
# -----------------------------------------------------------------------------

class ArchitectureDecision:
    """架构决策记录模型"""
    
    def __init__(self, title: str, context: str = "", status: ADRStatus = ADRStatus.PROPOSED):
        self.id = self._generate_id()
        self.title = title
        self.context = context or f"记录关于 {title} 的架构决策"
        self.status = status
        self.decision_date = datetime.now().isoformat()
        self.last_updated = self.decision_date
        
        # 决策属性
        self.decision = ""
        self.rationale = ""
        self.consequences = []
        self.alternatives = []
        self.related_decisions = []
        
        # 技术属性
        self.scope = DecisionScope.COMPONENT.value
        self.impact = DecisionImpact.MEDIUM.value
        self.category = "技术栈选型"
        
        # 宪法合规性
        self.constitution_articles = []
        self.constitution_compliance = True
        
        # 元数据
        self.authors = []
        self.stakeholders = []
        self.references = []
    
    def _generate_id(self) -> str:
        """生成决策ID"""
        timestamp = datetime.now().strftime("%Y%m%d")
        short_uuid = str(uuid.uuid4())[:8]
        return f"adr-{timestamp}-{short_uuid}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "context": self.context,
            "status": self.status.value,
            "decision_date": self.decision_date,
            "last_updated": self.last_updated,
            
            "decision": self.decision,
            "rationale": self.rationale,
            "consequences": self.consequences,
            "alternatives": self.alternatives,
            "related_decisions": self.related_decisions,
            
            "scope": self.scope,
            "impact": self.impact,
            "category": self.category,
            
            "constitution_articles": self.constitution_articles,
            "constitution_compliance": self.constitution_compliance,
            
            "authors": self.authors,
            "stakeholders": self.stakeholders,
            "references": self.references
        }
    
    def from_dict(self, data: Dict[str, Any]) -> 'ArchitectureDecision':
        """从字典加载"""
        self.id = data.get("id", self._generate_id())
        self.title = data.get("title", "")
        self.context = data.get("context", "")
        self.status = ADRStatus(data.get("status", ADRStatus.PROPOSED.value))
        self.decision_date = data.get("decision_date", datetime.now().isoformat())
        self.last_updated = data.get("last_updated", self.decision_date)
        
        self.decision = data.get("decision", "")
        self.rationale = data.get("rationale", "")
        self.consequences = data.get("consequences", [])
        self.alternatives = data.get("alternatives", [])
        self.related_decisions = data.get("related_decisions", [])
        
        self.scope = data.get("scope", DecisionScope.COMPONENT.value)
        self.impact = data.get("impact", DecisionImpact.MEDIUM.value)
        self.category = data.get("category", "技术栈选型")
        
        self.constitution_articles = data.get("constitution_articles", [])
        self.constitution_compliance = data.get("constitution_compliance", True)
        
        self.authors = data.get("authors", [])
        self.stakeholders = data.get("stakeholders", [])
        self.references = data.get("references", [])
        
        return self
    
    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        md = []
        
        # 标题和元数据
        md.append(f"# {self.title}")
        md.append("")
        md.append(f"**决策ID**: {self.id}")
        md.append(f"**状态**: {self.status.value.upper()}")
        md.append(f"**日期**: {self.decision_date}")
        md.append(f"**最后更新**: {self.last_updated}")
        md.append(f"**范围**: {self.scope.upper()}")
        md.append(f"**影响**: {self.impact.upper()}")
        md.append(f"**类别**: {self.category}")
        md.append("")
        
        # 作者和利益相关者
        if self.authors:
            md.append(f"**作者**: {', '.join(self.authors)}")
        if self.stakeholders:
            md.append(f"**利益相关者**: {', '.join(self.stakeholders)}")
        md.append("")
        
        # 宪法合规性
        if self.constitution_articles:
            md.append(f"**宪法依据**: {', '.join(self.constitution_articles)}")
            md.append(f"**宪法合规**: {'✅ 合规' if self.constitution_compliance else '❌ 不合规'}")
            md.append("")
        
        # 上下文
        md.append("## 📋 上下文")
        md.append("")
        md.append(self.context)
        md.append("")
        
        # 决策
        md.append("## 🎯 决策")
        md.append("")
        md.append(self.decision or "*（待填写）*")
        md.append("")
        
        # 理由
        if self.rationale:
            md.append("## 📖 理由")
            md.append("")
            md.append(self.rationale)
            md.append("")
        
        # 备选方案
        if self.alternatives:
            md.append("## 🔄 备选方案")
            md.append("")
            for i, alternative in enumerate(self.alternatives, 1):
                md.append(f"{i}. {alternative}")
            md.append("")
        
        # 后果
        if self.consequences:
            md.append("## ⚡ 后果")
            md.append("")
            for i, consequence in enumerate(self.consequences, 1):
                md.append(f"{i}. {consequence}")
            md.append("")
        
        # 相关决策
        if self.related_decisions:
            md.append("## 🔗 相关决策")
            md.append("")
            for decision in self.related_decisions:
                md.append(f"- {decision}")
            md.append("")
        
        # 参考
        if self.references:
            md.append("## 📚 参考")
            md.append("")
            for ref in self.references:
                md.append(f"- {ref}")
            md.append("")
        
        # 状态变更记录（预留）
        md.append("## 📝 变更记录")
        md.append("")
        md.append(f"- {self.decision_date}: 创建决策")
        md.append(f"- {self.last_updated}: 更新状态为 {self.status.value.upper()}")
        
        return "\n".join(md)
    
    def validate(self) -> List[str]:
        """验证决策记录的完整性"""
        errors = []
        
        if not self.title:
            errors.append("决策标题不能为空")
        
        if not self.context:
            errors.append("决策上下文不能为空")
        
        if not self.decision:
            errors.append("决策内容不能为空")
        
        if not self.rationale:
            errors.append("决策理由不能为空")
        
        if self.impact not in [i.value for i in DecisionImpact]:
            errors.append(f"无效的影响级别: {self.impact}")
        
        if self.scope not in [s.value for s in DecisionScope]:
            errors.append(f"无效的决策范围: {self.scope}")
        
        if self.category not in ARCHITECTURE_CATEGORIES:
            errors.append(f"无效的决策类别: {self.category}")
        
        # 宪法合规检查
        if not self.constitution_compliance and self.constitution_articles:
            errors.append("决策引用宪法条款但标记为不合规，请提供解释")
        
        return errors
    
    def suggest_constitution_articles(self) -> List[str]:
        """根据决策内容建议宪法条款"""
        suggestions = []
        decision_text = f"{self.title} {self.context} {self.decision}".lower()
        
        for article, keywords in CONSTITUTION_ARCHITECTURE_MAPPING.items():
            for keyword in keywords:
                if keyword.lower() in decision_text:
                    if article not in suggestions:
                        suggestions.append(article)
        
        return suggestions

# -----------------------------------------------------------------------------
# 决策存储管理
# -----------------------------------------------------------------------------

class ADRRepository:
    """架构决策记录存储库"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or SKILL_ROOT / "adrs"
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, adr: ArchitectureDecision) -> bool:
        """保存决策记录"""
        try:
            # 创建JSON和Markdown文件
            json_path = self.base_path / f"{adr.id}.json"
            md_path = self.base_path / f"{adr.id}.md"
            
            # 保存JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(adr.to_dict(), f, indent=2, ensure_ascii=False)
            
            # 保存Markdown
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(adr.to_markdown())
            
            return True
        except Exception as e:
            print(f"保存决策记录失败: {e}")
            return False
    
    def load(self, adr_id: str) -> Optional[ArchitectureDecision]:
        """加载决策记录"""
        try:
            json_path = self.base_path / f"{adr_id}.json"
            if not json_path.exists():
                return None
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            adr = ArchitectureDecision(title="")
            adr.from_dict(data)
            return adr
        except Exception as e:
            print(f"加载决策记录失败: {e}")
            return None
    
    def list_all(self) -> List[Dict[str, Any]]:
        """列出所有决策记录"""
        adrs = []
        
        for json_file in self.base_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 只添加基本摘要信息
                summary = {
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "status": data.get("status"),
                    "decision_date": data.get("decision_date"),
                    "scope": data.get("scope"),
                    "impact": data.get("impact"),
                    "category": data.get("category")
                }
                adrs.append(summary)
            except Exception:
                continue
        
        # 按日期排序（最新的在前面）
        adrs.sort(key=lambda x: x.get("decision_date", ""), reverse=True)
        return adrs
    
    def filter_by_status(self, status: str) -> List[Dict[str, Any]]:
        """按状态筛选决策记录"""
        all_adrs = self.list_all()
        return [adr for adr in all_adrs if adr.get("status") == status]
    
    def filter_by_category(self, category: str) -> List[Dict[str, Any]]:
        """按类别筛选决策记录"""
        all_adrs = self.list_all()
        return [adr for adr in all_adrs if adr.get("category") == category]
    
    def delete(self, adr_id: str) -> bool:
        """删除决策记录"""
        try:
            json_path = self.base_path / f"{adr_id}.json"
            md_path = self.base_path / f"{adr_id}.md"
            
            if json_path.exists():
                json_path.unlink()
            
            if md_path.exists():
                md_path.unlink()
            
            return True
        except Exception as e:
            print(f"删除决策记录失败: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        all_adrs = self.list_all()
        
        if not all_adrs:
            return {
                "total": 0,
                "by_status": {},
                "by_category": {},
                "by_impact": {},
                "by_scope": {}
            }
        
        stats = {
            "total": len(all_adrs),
            "by_status": {},
            "by_category": {},
            "by_impact": {},
            "by_scope": {}
        }
        
        for adr in all_adrs:
            # 按状态统计
            status = adr.get("status", "unknown")
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            
            # 按类别统计
            category = adr.get("category", "unknown")
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            
            # 按影响统计
            impact = adr.get("impact", "unknown")
            stats["by_impact"][impact] = stats["by_impact"].get(impact, 0) + 1
            
            # 按范围统计
            scope = adr.get("scope", "unknown")
            stats["by_scope"][scope] = stats["by_scope"].get(scope, 0) + 1
        
        return stats

# -----------------------------------------------------------------------------
# 决策分析器
# -----------------------------------------------------------------------------

class ArchitectureAnalyzer:
    """架构决策分析器"""
    
    def __init__(self, repository: ADRRepository):
        self.repository = repository
    
    def analyze_consistency(self) -> Dict[str, Any]:
        """分析决策一致性"""
        all_adrs = self.repository.list_all()
        
        analysis = {
            "total_decisions": len(all_adrs),
            "consistency_score": 0,
            "issues": [],
            "recommendations": []
        }
        
        if len(all_adrs) < 2:
            analysis["consistency_score"] = 100
            analysis["recommendations"].append("决策记录不足，无法进行一致性分析")
            return analysis
        
        # 检查决策间的冲突
        conflicts = self._find_conflicts(all_adrs)
        if conflicts:
            analysis["issues"].extend(conflicts)
        
        # 计算一致性分数
        total_possible_conflicts = len(all_adrs) * (len(all_adrs) - 1) // 2
        actual_conflicts = len(conflicts)
        
        if total_possible_conflicts > 0:
            consistency_score = 100 - (actual_conflicts / total_possible_conflicts * 100)
            analysis["consistency_score"] = max(0, consistency_score)
        else:
            analysis["consistency_score"] = 100
        
        # 生成建议
        if analysis["consistency_score"] < 80:
            analysis["recommendations"].append("决策一致性较低，建议进行架构评审")
        
        if not conflicts:
            analysis["recommendations"].append("决策间未发现明显冲突，架构一致性良好")
        
        return analysis
    
    def _find_conflicts(self, adrs: List[Dict[str, Any]]) -> List[str]:
        """查找决策冲突"""
        conflicts = []
        
        # 简化的冲突检测（根据标题关键词）
        for i, adr1 in enumerate(adrs):
            for adr2 in adrs[i+1:]:
                # 检查相同类别下的不同决策
                if (adr1.get("category") == adr2.get("category") and 
                    adr1.get("status") == "accepted" and 
                    adr2.get("status") == "accepted"):
                    
                    title1 = adr1.get("title", "").lower()
                    title2 = adr2.get("title", "").lower()
                    
                    # 检查是否有明显的技术冲突
                    tech_keywords = [
                        ("react", "vue"),
                        ("rest", "graphql"),
                        ("sql", "nosql"),
                        ("microservices", "monolith"),
                        ("docker", "kubernetes")
                    ]
                    
                    for tech1, tech2 in tech_keywords:
                        if tech1 in title1 and tech2 in title2:
                            conflicts.append(f"技术冲突: {adr1.get('id')} ({tech1}) 与 {adr2.get('id')} ({tech2})")
        
        return conflicts
    
    def analyze_constitution_compliance(self) -> Dict[str, Any]:
        """分析宪法合规性"""
        all_adrs = self.repository.list_all()
        
        analysis = {
            "total_decisions": len(all_adrs),
            "with_constitution_refs": 0,
            "compliance_rate": 0,
            "articles_used": {},
            "recommendations": []
        }
        
        # 加载详细的决策数据以检查宪法引用
        for adr_summary in all_adrs:
            adr = self.repository.load(adr_summary.get("id", ""))
            if adr and adr.constitution_articles:
                analysis["with_constitution_refs"] += 1
                
                # 统计宪法条款使用情况
                for article in adr.constitution_articles:
                    analysis["articles_used"][article] = analysis["articles_used"].get(article, 0) + 1
        
        # 计算合规率
        if all_adrs:
            compliance_rate = (analysis["with_constitution_refs"] / len(all_adrs)) * 100
            analysis["compliance_rate"] = round(compliance_rate, 2)
        
        # 生成建议
        if analysis["compliance_rate"] < 80:
            analysis["recommendations"].append("宪法引用率较低，建议在决策中增加宪法条款引用")
        
        if not analysis["articles_used"]:
            analysis["recommendations"].append("未使用任何宪法条款，建议学习宪法与架构的映射关系")
        else:
            most_used = max(analysis["articles_used"].items(), key=lambda x: x[1], default=(None, 0))
            if most_used[0]:
                analysis["recommendations"].append(f"最常用的宪法条款: {most_used[0]} (使用{most_used[1]}次)")
        
        return analysis
    
    def generate_report(self) -> Dict[str, Any]:
        """生成分析报告"""
        consistency_analysis = self.analyze_consistency()
        constitution_analysis = self.analyze_constitution_compliance()
        stats = self.repository.get_stats()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "version": VERSION,
            "summary": {
                "total_decisions": stats["total"],
                "consistency_score": consistency_analysis["consistency_score"],
                "constitution_compliance_rate": constitution_analysis["compliance_rate"],
                "overall_health": self._calculate_health_score(
                    consistency_analysis["consistency_score"],
                    constitution_analysis["compliance_rate"]
                )
            },
            "statistics": stats,
            "consistency_analysis": consistency_analysis,
            "constitution_analysis": constitution_analysis,
            "recommendations": self._generate_overall_recommendations(
                consistency_analysis,
                constitution_analysis,
                stats
            )
        }
        
        return report
    
    def _calculate_health_score(self, consistency_score: float, compliance_rate: float) -> float:
        """计算整体健康分数"""
        # 加权平均：一致性占60%，合规性占40%
        return (consistency_score * 0.6 + compliance_rate * 0.4)
    
    def _generate_overall_recommendations(self, consistency: Dict[str, Any], 
                                         constitution: Dict[str, Any], 
                                         stats: Dict[str, Any]) -> List[str]:
        """生成总体建议"""
        recommendations = []
        
        # 基于统计的建议
        if stats["total"] == 0:
            recommendations.append("尚未记录任何架构决策，建议从关键决策开始记录")
        
        if stats["total"] > 0 and stats.get("by_status", {}).get("proposed", 0) > 3:
            recommendations.append("有多项提案中的决策，建议及时评审并确定状态")
        
        # 基于一致性的建议
        if consistency["consistency_score"] < 70:
            recommendations.append("决策一致性较低，建议组织架构评审会议")
        
        # 基于宪法合规性的建议
        if constitution["compliance_rate"] < 70:
            recommendations.append("宪法引用率较低，建议在决策模板中强制要求宪法引用")
        
        # 基于状态分布的建议
        accepted_count = stats.get("by_status", {}).get("accepted", 0)
        total_count = stats["total"]
        
        if total_count > 0 and accepted_count / total_count < 0.5:
            recommendations.append("已接受的决策比例较低，建议加快决策流程")
        
        if not recommendations:
            recommendations.append("架构决策管理状况良好，继续保持")
        
        return recommendations

# -----------------------------------------------------------------------------
# CLI工具类
# -----------------------------------------------------------------------------

class CDDArchitectCLI:
    """CDD Architect CLI主类"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.repository = ADRRepository()
        self.analyzer = ArchitectureAnalyzer(self.repository)
    
    def create_decision(self, title: str, context: str = "", status: str = "proposed") -> Dict[str, Any]:
        """创建新的架构决策"""
        try:
            # 验证状态
            try:
                adr_status = ADRStatus(status)
            except ValueError:
                return {
                    "success": False,
                    "error": f"无效的状态: {status}，有效状态: {[s.value for s in ADRStatus]}"
                }
            
            # 创建决策记录
            adr = ArchitectureDecision(title=title, context=context, status=adr_status)
            
            # 设置默认作者
            import getpass
            adr.authors = [getpass.getuser()]
            
            # 自动建议宪法条款
            suggested_articles = adr.suggest_constitution_articles()
            if suggested_articles:
                adr.constitution_articles = suggested_articles[:3]  # 最多3个
            
            # 保存
            saved = self.repository.save(adr)
            
            if saved:
                return {
                    "success": True,
                    "message": f"架构决策记录已创建: {adr.id}",
                    "adr_id": adr.id,
                    "adr": adr.to_dict(),
                    "suggested_next_steps": [
                        f"编辑文件完善决策内容: {self.repository.base_path}/{adr.id}.json",
                        f"使用命令查看决策: python scripts/cdd_architect.py view {adr.id}",
                        f"使用命令更新状态: python scripts/cdd_architect.py update {adr.id} --status accepted"
                    ]
                }
            else:
                return {
                    "success": False,
                    "error": "保存决策记录失败"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"创建决策记录失败: {e}"
            }
    
    def list_decisions(self, status: Optional[str] = None, verbose: bool = False) -> Dict[str, Any]:
        """列出决策记录"""
        try:
            if status:
                adrs = self.repository.filter_by_status(status)
            else:
                adrs = self.repository.list_all()
            
            return {
                "success": True,
                "count": len(adrs),
                "status_filter": status,
                "decisions": adrs,
                "summary": {
                    "total": len(adrs),
                    "by_status": self.repository.get_stats().get("by_status", {}),
                    "by_category": self.repository.get_stats().get("by_category", {})
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"列出决策记录失败: {e}"
            }
    
    def view_decision(self, adr_id: str, format: str = "markdown") -> Dict[str, Any]:
        """查看决策记录"""
        try:
            adr = self.repository.load(adr_id)
            if not adr:
                return {
                    "success": False,
                    "error": f"未找到决策记录: {adr_id}"
                }
            
            if format == "json":
                return {
                    "success": True,
                    "adr_id": adr_id,
                    "format": format,
                    "data": adr.to_dict()
                }
            else:  # markdown
                return {
                    "success": True,
                    "adr_id": adr_id,
                    "format": format,
                    "content": adr.to_markdown()
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"查看决策记录失败: {e}"
            }
    
    def update_decision(self, adr_id: str, status: Optional[str] = None, note: Optional[str] = None) -> Dict[str, Any]:
        """更新决策记录"""
        try:
            adr = self.repository.load(adr_id)
            if not adr:
                return {
                    "success": False,
                    "error": f"未找到决策记录: {adr_id}"
                }
            
            # 更新状态
            if status:
                try:
                    adr.status = ADRStatus(status)
                except ValueError:
                    return {
                        "success": False,
                        "error": f"无效的状态: {status}"
                    }
            
            # 更新最后修改时间
            adr.last_updated = datetime.now().isoformat()
            
            # 保存更新
            saved = self.repository.save(adr)
            
            if saved:
                return {
                    "success": True,
                    "message": f"决策记录已更新: {adr_id}",
                    "adr_id": adr_id,
                    "updates": {
                        "status": status,
                        "last_updated": adr.last_updated,
                        "note_applied": bool(note)
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "保存更新失败"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"更新决策记录失败: {e}"
            }
    
    def analyze_decisions(self) -> Dict[str, Any]:
        """分析决策记录"""
        try:
            report = self.analyzer.generate_report()
            
            return {
                "success": True,
                "report": report,
                "summary": report.get("summary", {}),
                "health_status": self._get_health_status(report.get("summary", {}).get("overall_health", 0))
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"分析决策记录失败: {e}"
            }
    
    def generate_template(self, output_file: Optional[str] = None, template_type: str = "full") -> Dict[str, Any]:
        """生成决策模板"""
        try:
            # 创建示例决策
            example_adr = ArchitectureDecision(
                title="示例：选择React作为前端框架",
                context="项目需要选择合适的前端框架，以支持快速开发和良好的用户体验。",
                status=ADRStatus.ACCEPTED
            )
            
            example_adr.decision = "选择React作为主要前端框架，配合TypeScript和Vite构建工具。"
            example_adr.rationale = "React具有广泛的社区支持、丰富的生态系统、良好的TypeScript集成，并且团队已有React经验。"
            example_adr.consequences = [
                "需要学习和维护React技术栈",
                "可以利用丰富的React生态系统",
                "TypeScript提供更好的类型安全和开发体验"
            ]
            example_adr.alternatives = ["Vue.js", "Angular", "Svelte"]
            example_adr.scope = DecisionScope.SYSTEM.value
            example_adr.impact = DecisionImpact.HIGH.value
            example_adr.category = "技术栈选型"
            example_adr.constitution_articles = ["§101", "§102", "§103"]
            example_adr.authors = ["技术架构师"]
            example_adr.stakeholders = ["开发团队", "产品经理", "用户体验设计师"]
            
            template_content = example_adr.to_markdown()
            
            # 添加模板说明
            template_with_instructions = f"""# 架构决策记录（ADR）模板

## 使用说明

1. **复制此模板**到新的决策记录文件
2. **填写各个部分**，特别是上下文、决策、理由等
3. **更新元数据**（状态、范围、影响等）
4. **保存文件**到`adrs/`目录（使用`.md`和`.json`格式）
5. **使用工具管理**：`python scripts/cdd_architect.py` 命令

## 宪法合规提示

- 引用相关宪法条款（§101, §102, §103等）
- 确保决策符合宪法原则
- 记录宪法合规性评估

---

{template_content}

## 📝 模板填写指南

### 必填部分
1. **标题**：清晰描述决策内容
2. **上下文**：为什么需要这个决策
3. **决策**：具体决定是什么
4. **理由**：为什么做出这个决定

### 建议填写部分
1. **后果**：决策带来的影响
2. **备选方案**：考虑过的其他选项
3. **相关决策**：与此决策相关的其他决策

### 元数据
- **状态**：proposed | accepted | superseded | deprecated | rejected
- **范围**：component | module | system | architecture  
- **影响**：low | medium | high | critical
- **类别**：从预定义类别中选择

**宪法依据**: 根据决策内容引用相关宪法条款
"""
            
            if output_file:
                output_path = Path(output_file)
                output_path.write_text(template_with_instructions, encoding='utf-8')
                
                return {
                    "success": True,
                    "message": f"模板已保存到: {output_file}",
                    "file_path": output_file,
                    "template_type": template_type
                }
            else:
                return {
                    "success": True,
                    "template_type": template_type,
                    "content": template_with_instructions
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"生成模板失败: {e}"
            }
    
    def _get_health_status(self, health_score: float) -> str:
        """根据健康分数获取状态"""
        if health_score >= 80:
            return "🟢 健康"
        elif health_score >= 60:
            return "🟡 一般"
        else:
            return "🔴 需要关注"

# -----------------------------------------------------------------------------
# CLI输出格式化
# -----------------------------------------------------------------------------

def format_create_result(result: Dict[str, Any]) -> str:
    """格式化创建结果"""
    output = []
    
    output.append(f"🏗️  CDD Architect v{VERSION}")
    output.append("=" * 40)
    
    if not result.get("success", False):
        output.append(f"❌ 创建失败: {result.get('error', 'Unknown error')}")
        return "\n".join(output)
    
    output.append(f"✅ 架构决策记录创建成功")
    output.append(f"📋 决策ID: {result.get('adr_id', 'N/A')}")
    output.append(f"📅 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    adr_data = result.get("adr", {})
    if adr_data:
        output.append(f"📝 标题: {adr_data.get('title', 'N/A')}")
        output.append(f"📊 状态: {adr_data.get('status', 'N/A').upper()}")
        output.append(f"🎯 范围: {adr_data.get('scope', 'N/A').upper()}")
        output.append(f"⚡ 影响: {adr_data.get('impact', 'N/A').upper()}")
        
        if adr_data.get("constitution_articles"):
            output.append(f"⚖️ 宪法引用: {', '.join(adr_data['constitution_articles'])}")
    
    output.append("\n💡 下一步建议:")
    for step in result.get("suggested_next_steps", []):
        output.append(f"  • {step}")
    
    return "\n".join(output)

def format_list_result(result: Dict[str, Any], verbose: bool = False) -> str:
    """格式化列表结果"""
    output = []
    
    output.append(f"📋 CDD Architect - 决策记录列表 v{VERSION}")
    output.append("=" * 40)
    
    if not result.get("success", False):
        output.append(f"❌ 列表失败: {result.get('error', 'Unknown error')}")
        return "\n".join(output)
    
    decisions = result.get("decisions", [])
    count = result.get("count", 0)
    
    output.append(f"📊 找到决策记录: {count} 个")
    
    if result.get("status_filter"):
        output.append(f"🔍 状态过滤: {result.get('status_filter')}")
    
    summary = result.get("summary", {})
    if summary.get("by_status"):
        output.append("\n📈 状态分布:")
        for status, count in summary["by_status"].items():
            output.append(f"  • {status.upper()}: {count} 个")
    
    if decisions:
        output.append("\n📄 决策记录:")
        for i, decision in enumerate(decisions, 1):
            status_emoji = {
                "proposed": "🟡",
                "accepted": "✅",
                "superseded": "🔄",
                "deprecated": "⚠️",
                "rejected": "❌"
            }.get(decision.get("status", ""), "❓")
            
            output.append(f"\n  {i}. {status_emoji} {decision.get('id', 'N/A')}")
            output.append(f"      标题: {decision.get('title', 'N/A')}")
            output.append(f"      日期: {decision.get('decision_date', 'N/A')}")
            output.append(f"      状态: {decision.get('status', 'N/A').upper()}")
            output.append(f"      范围: {decision.get('scope', 'N/A').upper()}")
            output.append(f"      影响: {decision.get('impact', 'N/A').upper()}")
            
            if verbose:
                output.append(f"      类别: {decision.get('category', 'N/A')}")
    
    if count == 0:
        output.append("\n💡 建议: 使用 'create' 命令创建第一个架构决策记录")
    
    return "\n".join(output)

def format_view_result(result: Dict[str, Any]) -> str:
    """格式化查看结果"""
    output = []
    
    if not result.get("success", False):
        return f"❌ 查看失败: {result.get('error', 'Unknown error')}"
    
    if result.get("format") == "json":
        # JSON格式输出
        return json.dumps(result.get("data", {}), indent=2, ensure_ascii=False)
    else:
        # Markdown格式直接输出
        return result.get("content", "内容为空")

def format_update_result(result: Dict[str, Any]) -> str:
    """格式化更新结果"""
    output = []
    
    output.append(f"🔄 CDD Architect - 更新决策记录 v{VERSION}")
    output.append("=" * 40)
    
    if not result.get("success", False):
        output.append(f"❌ 更新失败: {result.get('error', 'Unknown error')}")
        return "\n".join(output)
    
    output.append(f"✅ 决策记录更新成功")
    output.append(f"📋 决策ID: {result.get('adr_id', 'N/A')}")
    
    updates = result.get("updates", {})
    if updates.get("status"):
        output.append(f"📊 新状态: {updates['status'].upper()}")
    
    output.append(f"📅 最后更新: {updates.get('last_updated', 'N/A')}")
    
    if updates.get("note_applied"):
        output.append("📝 备注已应用")
    
    output.append("\n💡 下一步: 使用 'view' 命令查看更新后的决策记录")
    
    return "\n".join(output)

def format_analyze_result(result: Dict[str, Any]) -> str:
    """格式化分析结果"""
    output = []
    
    output.append(f"📊 CDD Architect - 决策分析报告 v{VERSION}")
    output.append("=" * 40)
    
    if not result.get("success", False):
        output.append(f"❌ 分析失败: {result.get('error', 'Unknown error')}")
        return "\n".join(output)
    
    report = result.get("report", {})
    summary = report.get("summary", {})
    
    output.append(f"📅 报告生成时间: {report.get('generated_at', 'N/A')}")
    output.append(f"📋 总决策数: {summary.get('total_decisions', 0)} 个")
    output.append(f"📈 一致性分数: {summary.get('consistency_score', 0):.1f}/100")
    output.append(f"⚖️ 宪法合规率: {summary.get('constitution_compliance_rate', 0):.1f}%")
    output.append(f"🏥 整体健康度: {summary.get('overall_health', 0):.1f}/100 ({result.get('health_status', 'N/A')})")
    
    stats = report.get("statistics", {})
    if stats:
        output.append("\n📊 统计信息:")
        output.append(f"  • 总决策数: {stats.get('total', 0)} 个")
        
        by_status = stats.get("by_status", {})
        if by_status:
            output.append("  • 状态分布:")
            for status, count in by_status.items():
                output.append(f"    - {status.upper()}: {count} 个")
        
        by_category = stats.get("by_category", {})
        if by_category:
            most_common = max(by_category.items(), key=lambda x: x[1], default=(None, 0))
            if most_common[0]:
                output.append(f"  • 最常见类别: {most_common[0]} ({most_common[1]} 个)")
    
    # 显示建议
    recommendations = report.get("recommendations", [])
    if recommendations:
        output.append("\n💡 建议:")
        for i, rec in enumerate(recommendations[:5], 1):  # 只显示前5个
            output.append(f"  {i}. {rec}")
    
    return "\n".join(output)

def format_template_result(result: Dict[str, Any]) -> str:
    """格式化模板生成结果"""
    output = []
    
    output.append(f"📄 CDD Architect - 决策模板生成器 v{VERSION}")
    output.append("=" * 40)
    
    if not result.get("success", False):
        output.append(f"❌ 模板生成失败: {result.get('error', 'Unknown error')}")
        return "\n".join(output)
    
    output.append(f"✅ 决策模板生成成功")
    output.append(f"📋 模板类型: {result.get('template_type', 'N/A')}")
    
    if "file_path" in result:
        output.append(f"💾 保存位置: {result.get('file_path')}")
        output.append("\n💡 使用说明:")
        output.append("  1. 复制模板内容到新文件")
        output.append("  2. 填写各个部分")
        output.append("  3. 保存到 adrs/ 目录")
        output.append("  4. 使用工具命令管理")
    else:
        output.append("\n📝 模板内容:")
        output.append("-" * 40)
        output.append(result.get("content", "")[:500] + "...")
        output.append("... (内容截断，使用 --output 参数保存到文件查看完整内容)")
    
    return "\n".join(output)

# -----------------------------------------------------------------------------
# 主函数
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=f"CDD Architect v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/cdd_architect.py create "使用TypeScript" --status proposed
  python scripts/cdd_architect.py list --status accepted --verbose
  python scripts/cdd_architect.py view adr-20240221-abc123 --format json
  python scripts/cdd_architect.py update adr-20240221-abc123 --status accepted
  python scripts/cdd_architect.py analyze --json
  python scripts/cdd_architect.py template --output adr-template.md
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新的架构决策")
    create_parser.add_argument("title", help="决策标题")
    create_parser.add_argument("--context", "-c", help="决策上下文")
    create_parser.add_argument("--status", "-s", choices=[s.value for s in ADRStatus], 
                               default="proposed", help="决策状态")
    create_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    create_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出架构决策")
    list_parser.add_argument("--status", "-s", choices=[s.value for s in ADRStatus], 
                             help="按状态过滤")
    list_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    list_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # view 命令
    view_parser = subparsers.add_parser("view", help="查看架构决策")
    view_parser.add_argument("adr_id", help="决策ID")
    view_parser.add_argument("--format", "-f", choices=["json", "markdown"], 
                             default="markdown", help="输出格式")
    view_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    view_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    # update 命令
    update_parser = subparsers.add_parser("update", help="更新架构决策")
    update_parser.add_argument("adr_id", help="决策ID")
    update_parser.add_argument("--status", "-s", choices=[s.value for s in ADRStatus], 
                               help="更新状态")
    update_parser.add_argument("--note", "-n", help="更新备注")
    update_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    update_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="分析架构决策")
    analyze_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    analyze_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    # template 命令
    template_parser = subparsers.add_parser("template", help="生成决策模板")
    template_parser.add_argument("--output", "-o", help="输出文件路径")
    template_parser.add_argument("--type", "-t", choices=["full", "simple"], 
                                 default="full", help="模板类型")
    template_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    template_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 安全获取verbose属性，如果不存在则使用默认值False
    verbose = getattr(args, 'verbose', False)
    cli = CDDArchitectCLI(verbose=verbose)
    
    try:
        if args.command == "create":
            result = cli.create_decision(args.title, args.context, args.status)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_create_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
        
        elif args.command == "list":
            result = cli.list_decisions(args.status, args.verbose)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_list_result(result, args.verbose))
            
            sys.exit(0 if result.get("success", False) else 1)
        
        elif args.command == "view":
            result = cli.view_decision(args.adr_id, args.format)
            
            if args.json or args.format == "json":
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_view_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
        
        elif args.command == "update":
            result = cli.update_decision(args.adr_id, args.status, args.note)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_update_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
        
        elif args.command == "analyze":
            result = cli.analyze_decisions()
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_analyze_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
        
        elif args.command == "template":
            result = cli.generate_template(args.output, args.type)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_template_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  操作被用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

# -----------------------------------------------------------------------------
# Claude Code桥梁接口
# -----------------------------------------------------------------------------

def create_decision_claude(title: str, context: str = "", status: str = "proposed", **kwargs) -> dict:
    """Claude Code架构决策创建接口"""
    cli = CDDArchitectCLI(kwargs.get('verbose', False))
    result = cli.create_decision(title, context, status)
    
    result["tool_version"] = VERSION
    
    return result

def list_decisions_claude(status: Optional[str] = None, **kwargs) -> dict:
    """Claude Code架构决策列表接口"""
    cli = CDDArchitectCLI(kwargs.get('verbose', False))
    result = cli.list_decisions(status, kwargs.get('verbose', False))
    
    result["tool_version"] = VERSION
    
    return result

def view_decision_claude(adr_id: str, format: str = "markdown", **kwargs) -> dict:
    """Claude Code架构决策查看接口"""
    cli = CDDArchitectCLI(kwargs.get('verbose', False))
    result = cli.view_decision(adr_id, format)
    
    result["tool_version"] = VERSION
    
    return result

def update_decision_claude(adr_id: str, status: Optional[str] = None, note: Optional[str] = None, **kwargs) -> dict:
    """Claude Code架构决策更新接口"""
    cli = CDDArchitectCLI(kwargs.get('verbose', False))
    result = cli.update_decision(adr_id, status, note)
    
    result["tool_version"] = VERSION
    
    return result

def analyze_decisions_claude(**kwargs) -> dict:
    """Claude Code架构决策分析接口"""
    cli = CDDArchitectCLI(kwargs.get('verbose', False))
    result = cli.analyze_decisions()
    
    result["tool_version"] = VERSION
    
    return result

def generate_template_claude(output_file: Optional[str] = None, template_type: str = "full", **kwargs) -> dict:
    """Claude Code架构决策模板接口"""
    cli = CDDArchitectCLI(kwargs.get('verbose', False))
    result = cli.generate_template(output_file, template_type)
    
    result["tool_version"] = VERSION
    
    return result

if __name__ == "__main__":
    main()