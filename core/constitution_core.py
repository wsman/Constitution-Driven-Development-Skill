"""
CDD Constitution Core Definitions (constitution_core.py)
========================================================
核心宪法条款统一定义模块，包含实际使用的 62 个核心条款。

宪法依据: §100.3§101§102

版本: v2.0.0 (核心条款分离版本)
说明: 此文件包含实际使用的核心条款，不包含示例性引用。
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ConstitutionArticle:
    """宪法条款定义"""
    section: str  # 条款编号，如 "§100.3"
    name: str     # 条款名称
    category: str # 分类: "basic" (基本法), "technical" (技术法), "procedural" (程序法)
    description: str  # 详细描述
    usage: str    # 使用场景


# 核心宪法条款统一定义 (62个实际使用的核心条款)
CONSTITUTION_CORE_ARTICLES: Dict[str, ConstitutionArticle] = {
    # === 基本法 (§100-§199) - 核心条款 ===
    "§100": ConstitutionArticle(
        section="§100",
        name="宪法治理总纲",
        category="basic",
        description="定义CDD宪法治理的基本框架和原则",
        usage="宪法治理、决策依据"
    ),
    "§100.3": ConstitutionArticle(
        section="§100.3",
        name="同步公理",
        category="basic",
        description="代码 (C) 与文档 (D) 必须原子性同步。ΔC ≠ 0 ⟹ ΔD ≠ 0",
        usage="版本控制、文档维护、Gate 1验证"
    ),
    "§101": ConstitutionArticle(
        section="§101",
        name="单一真理源公理",
        category="basic",
        description="memory_bank/ 是唯一真理源。严禁在多个位置维护同一状态",
        usage="状态管理、文档同步"
    ),
    "§102": ConstitutionArticle(
        section="§102",
        name="熵减原则",
        category="basic",
        description="所有变更必须证明其有助于降低或维持系统熵值 (H_sys)。ΔH_sys ≤ 0",
        usage="架构设计、重构决策、Gate 3验证"
    ),
    "§103": ConstitutionArticle(
        section="§103",
        name="文档优先公理",
        category="basic",
        description="在编写代码之前必须先完成文档规划，确保设计先行",
        usage="特性开发、架构设计"
    ),
    "§104": ConstitutionArticle(
        section="§104",
        name="持久化原则",
        category="basic",
        description="检查点数据必须持久化保存，确保状态可恢复",
        usage="状态恢复、检查点管理"
    ),
    "§105": ConstitutionArticle(
        section="§105",
        name="可追溯性公理",
        category="basic",
        description="所有变更必须有明确的来源和原因记录",
        usage="审计追踪、变更管理"
    ),
    "§119": ConstitutionArticle(
        section="§119",
        name="Nordic主题驱动公理",
        category="basic",
        description="必须使用主题变量，禁止硬编码颜色值",
        usage="UI设计、样式管理"
    ),
    "§148": ConstitutionArticle(
        section="§148",
        name="控制论架构公理",
        category="basic",
        description="系统必须实现三层控制论架构（治理层→控制层→执行层）",
        usage="系统架构、组织设计"
    ),
    "§199": ConstitutionArticle(
        section="§199",
        name="基本法上限",
        category="basic",
        description="基本法的编号上限，保持编号体系完整性",
        usage="法律体系完整性"
    ),
    
    # === 技术法 (§200-§299) - 核心条款 ===
    "§106.1": ConstitutionArticle(
        section="§106.1",
        name="孢子隔离公理",
        category="technical",
        description="S_tool ∩ S_target = ∅。CDD工具不能意外修改技能库自身",
        usage="工具安全、部署隔离"
    ),
    "§200": ConstitutionArticle(
        section="§200",
        name="孢子协议总纲",
        category="technical",
        description="CDD Skill 是独立工具，必须与目标项目保持隔离",
        usage="工具部署、环境隔离"
    ),
    "§201": ConstitutionArticle(
        section="§201",
        name="工具链规范",
        category="technical",
        description="所有工具必须遵循统一的命名和接口规范",
        usage="工具开发、CLI设计"
    ),
    "§202": ConstitutionArticle(
        section="§202",
        name="模板引擎规范",
        category="technical",
        description="模板使用 {{PLACEHOLDER}} 格式，支持上下文渲染",
        usage="模板开发、文档生成"
    ),
    "§203": ConstitutionArticle(
        section="§203",
        name="事务决策层级",
        category="technical",
        description="日常事务自主决定，重要事项需项目负责人批准",
        usage="权限管理、决策流程"
    ),
    "§204": ConstitutionArticle(
        section="§204",
        name="信息流动路径",
        category="technical",
        description="信息流动必须遵循规定路径：执行者→管理者→决策者",
        usage="信息汇报、沟通路径"
    ),
    "§210": ConstitutionArticle(
        section="§210",
        name="会议记录规范",
        category="technical",
        description="所有重要讨论必须形成包含时间、参与者、讨论要点、决议事项、责任分工的书面记录",
        usage="会议管理、文档记录"
    ),
    "§211": ConstitutionArticle(
        section="§211",
        name="成员质量检验",
        category="technical",
        description="通过面试机制检验团队成员质量，确保每个上岗成员都是训练有素的宪法捍卫者",
        usage="人员管理、质量标准"
    ),
    "§230": ConstitutionArticle(
        section="§230",
        name="异构模型策略",
        category="technical",
        description="使用Tier 0模型处理规划协调，执行层使用Tier 1/2模型处理具体任务",
        usage="模型选择、资源分配"
    ),
    "§263": ConstitutionArticle(
        section="§263",
        name="熵值计算基础",
        category="technical",
        description="系统熵值计算的基础条款",
        usage="熵值监控、系统健康"
    ),
    "§266": ConstitutionArticle(
        section="§266",
        name="熵值监控标准",
        category="technical",
        description="熵值监控的标准和要求",
        usage="熵值管理、质量监控"
    ),
    "§267": ConstitutionArticle(
        section="§267",
        name="观测回路",
        category="technical",
        description="实时状态同步，确保系统状态可见性",
        usage="状态监控"
    ),
    "§268": ConstitutionArticle(
        section="§268",
        name="控制回路",
        category="technical",
        description="控制决策执行，确保系统行为可控",
        usage="决策执行"
    ),
    "§269": ConstitutionArticle(
        section="§269",
        name="记忆回路",
        category="technical",
        description="知识结晶存储，确保系统知识持久化",
        usage="知识管理"
    ),
    "§270": ConstitutionArticle(
        section="§270",
        name="技术标准集成总纲",
        category="technical",
        description="技术标准体系总纲，作为开发时始终加载的技术实施规范",
        usage="技术标准、开发规范"
    ),
    "§299": ConstitutionArticle(
        section="§299",
        name="操作法上限",
        category="technical",
        description="操作法的编号上限，保持编号体系完整性",
        usage="法律体系完整性"
    ),
    
    # === 程序法 (§300-§399) - 核心条款 ===
    "§300": ConstitutionArticle(
        section="§300",
        name="工作流总纲",
        category="procedural",
        description="定义CDD的核心工作流程和状态转换规则",
        usage="工作流管理"
    ),
    "§300.3": ConstitutionArticle(
        section="§300.3",
        name="三阶验证公理",
        category="procedural",
        description="任何状态变更必须通过三级验证：结构(Tier 1)、签名(Tier 2)、行为(Tier 3)",
        usage="审计验证、Gate 2"
    ),
    "§300.5": ConstitutionArticle(
        section="§300.5",
        name="熵值校准标准",
        category="procedural",
        description="H_sys ≤ 0.3 为优秀，≤ 0.5 为良好，≤ 0.7 为警告，> 0.7 为危险",
        usage="熵值评估、Gate 3"
    ),
    "§301": ConstitutionArticle(
        section="§301",
        name="State A - Intake",
        category="procedural",
        description="上下文加载阶段，加载T0内核和T1公理",
        usage="工作流状态"
    ),
    "§302": ConstitutionArticle(
        section="§302",
        name="State B - Plan",
        category="procedural",
        description="规划阶段，生成T2规格文档，必须等待批准",
        usage="工作流状态"
    ),
    "§303": ConstitutionArticle(
        section="§303",
        name="同构原则",
        category="procedural",
        description="文件系统结构 (S_fs) 必须与文档定义的架构 (S_doc) 同构",
        usage="架构验证、Tier 1"
    ),
    "§304": ConstitutionArticle(
        section="§304",
        name="L2+项目强制使用原则",
        category="procedural",
        description="L2及以上复杂度项目必须使用Claude Code自动化",
        usage="项目复杂度评估"
    ),
    "§305": ConstitutionArticle(
        section="§305",
        name="宪法引用规范",
        category="procedural",
        description="所有宪法引用必须使用 §NNN 格式，引用的条款必须存在",
        usage="文档规范、Gate 5"
    ),
    "§306": ConstitutionArticle(
        section="§306",
        name="文件操作标准",
        category="procedural",
        description="文件操作的标准流程和规范",
        usage="文件管理、操作规范"
    ),
    "§308": ConstitutionArticle(
        section="§308",
        name="数据卫生标准",
        category="procedural",
        description="数据卫生和存储的标准要求",
        usage="数据管理、卫生标准"
    ),
    "§309": ConstitutionArticle(
        section="§309",
        name="Claude Code自动化原则",
        category="procedural",
        description="鼓励使用Claude Code自动化任务执行",
        usage="工具集成、自动化"
    ),
    "§310": ConstitutionArticle(
        section="§310",
        name="工具调用公理",
        category="procedural",
        description="所有文件操作必须通过工具桥接器进行，确保原子写入和安全隔离",
        usage="文件操作安全"
    ),
    "§311": ConstitutionArticle(
        section="§311",
        name="错误处理规范",
        category="procedural",
        description="所有错误必须有明确的错误代码和恢复建议",
        usage="异常处理"
    ),
    "§312": ConstitutionArticle(
        section="§312",
        name="日志记录规范",
        category="procedural",
        description="关键操作必须有日志记录，支持审计追踪",
        usage="日志管理"
    ),
    "§320": ConstitutionArticle(
        section="§320",
        name="输入输出标准",
        category="procedural",
        description="输入输出与持久化的技术标准",
        usage="IO管理、数据持久化"
    ),
    "§350": ConstitutionArticle(
        section="§350",
        name="执行层总纲",
        category="procedural",
        description="执行层的核心职责和接口定义",
        usage="执行层设计"
    ),
    "§351": ConstitutionArticle(
        section="§351",
        name="执行层扩展一",
        category="procedural",
        description="执行层扩展条款一",
        usage="执行层设计、扩展功能"
    ),
    "§352": ConstitutionArticle(
        section="§352",
        name="执行层扩展二",
        category="procedural",
        description="执行层扩展条款二",
        usage="执行层设计、扩展功能"
    ),
    "§359": ConstitutionArticle(
        section="§359",
        name="执行层扩展上限",
        category="procedural",
        description="执行层扩展的编号上限",
        usage="法律体系完整性"
    ),
    "§399": ConstitutionArticle(
        section="§399",
        name="程序法上限",
        category="procedural",
        description="程序法的编号上限，保持编号体系完整性",
        usage="法律体系完整性"
    ),
    
    # === 公理层扩展 - 核心条款 ===
    "§400": ConstitutionArticle(
        section="§400",
        name="公理层开始",
        category="basic",
        description="公理层编号开始标记",
        usage="法律体系完整性"
    ),
    "§699": ConstitutionArticle(
        section="§699",
        name="公理层上限",
        category="basic",
        description="公理层的编号上限，保持编号体系完整性",
        usage="法律体系完整性"
    ),
    
    # === 子条款扩展 - 核心条款 ===
    "§200.1": ConstitutionArticle(
        section="§200.1",
        name="孢子协议细化",
        category="technical",
        description="孢子协议的细化实施标准",
        usage="工具部署、环境隔离细化"
    ),
    "§108.1": ConstitutionArticle(
        section="§108.1",
        name="技术隔离细化",
        category="technical",
        description="技术隔离的细化实施标准",
        usage="技术隔离、安全细化"
    ),
}


def get_core_article(section: str) -> Optional[ConstitutionArticle]:
    """
    获取指定核心条款的定义
    
    Args:
        section: 条款编号，如 "§100.3" 或 "100.3"
        
    Returns:
        ConstitutionArticle 或 None
    """
    # 规范化条款编号
    if not section.startswith("§"):
        section = f"§{section}"
    
    return CONSTITUTION_CORE_ARTICLES.get(section)


def get_core_articles_by_category(category: str) -> List[ConstitutionArticle]:
    """
    获取指定分类的所有核心条款
    
    Args:
        category: 分类名称 ("basic", "technical", "procedural")
        
    Returns:
        条款列表
    """
    return [
        article for article in CONSTITUTION_CORE_ARTICLES.values()
        if article.category == category
    ]


def validate_core_reference(section: str) -> tuple[bool, str]:
    """
    验证宪法引用是否为核心条款
    
    Args:
        section: 条款编号
        
    Returns:
        (是否有效, 错误消息或描述)
    """
    article = get_core_article(section)
    if article:
        return True, article.description
    return False, f"未知的宪法核心条款: {section}"


def get_all_core_sections() -> List[str]:
    """获取所有有效的核心条款编号列表"""
    return list(CONSTITUTION_CORE_ARTICLES.keys())


def format_constitutional_basis(sections: List[str]) -> str:
    """
    格式化宪法依据字符串，仅使用核心条款
    
    Args:
        sections: 条款编号列表
        
    Returns:
        格式化的字符串，如 "宪法依据: §101§102§300.3"
    """
    valid_sections = []
    for s in sections:
        if not s.startswith("§"):
            s = f"§{s}"
        if s in CONSTITUTION_CORE_ARTICLES:
            valid_sections.append(s)
    
    if valid_sections:
        return f"宪法依据: {''.join(valid_sections)}"
    return ""


# 导出常量列表
CONSTITUTION_CORE_ARTICLES_LIST = get_all_core_sections()

if __name__ == "__main__":
    print(f"CDD Constitution Core v2.0.0")
    print(f"核心条款总数: {len(CONSTITUTION_CORE_ARTICLES)}")
    print(f"按分类统计:")
    for category in ["basic", "technical", "procedural"]:
        articles = get_core_articles_by_category(category)
        print(f"  {category}: {len(articles)} 条")