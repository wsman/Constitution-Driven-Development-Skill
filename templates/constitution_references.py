"""
CDD Constitution Reference Definitions (constitution_references.py)
==================================================================
示例性宪法条款引用定义模块，包含114个用于模板展示的示例性引用。

宪法依据: §100.3§305

版本: v2.0.0 (参考条款分离版本)
说明: 此文件包含模板文件中使用的示例性引用，这些引用仅用于展示宪法体系结构，不影响核心功能。
注意: 在生产环境中，主要关注 core/constitution_core.py 中定义的核心条款。
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ConstitutionArticle:
    """宪法条款定义"""
    section: str  # 条款编号，如 "§108"
    name: str     # 条款名称
    category: str # 分类: "basic" (基本法), "technical" (技术法), "procedural" (程序法), "axiomatic" (公理层)
    description: str  # 详细描述
    usage: str    # 使用场景


# 示例性宪法条款引用定义 (114个用于模板展示的引用)
CONSTITUTION_REFERENCE_ARTICLES: Dict[str, ConstitutionArticle] = {
    # === 基本法示例性引用 (§100-§199) ===
    "§107": ConstitutionArticle(
        section="§107",
        name="安全公理",
        category="basic",
        description="检查依赖包存在性，使用参数化查询防御注入（示例性引用）",
        usage="安全标准、注入防御"
    ),
    "§108": ConstitutionArticle(
        section="§108",
        name="基本法条款§108",
        category="basic",
        description="基本法条款§108，定义项目基本宪法原则（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§112": ConstitutionArticle(
        section="§112",
        name="基本法条款§112",
        category="basic",
        description="基本法条款§112，定义项目基本宪法原则（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§113": ConstitutionArticle(
        section="§113",
        name="基本法条款§113",
        category="basic",
        description="基本法条款§113，定义项目基本宪法原则（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§126": ConstitutionArticle(
        section="§126",
        name="基本法条款§126",
        category="basic",
        description="基本法条款§126，定义项目基本宪法原则（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§127": ConstitutionArticle(
        section="§127",
        name="基本法条款§127",
        category="basic",
        description="基本法条款§127，定义项目基本宪法原则（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§136": ConstitutionArticle(
        section="§136",
        name="基本法扩展",
        category="basic",
        description="基本法扩展条款，定义项目治理原则（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§150": ConstitutionArticle(
        section="§150",
        name="基本法条款§150",
        category="basic",
        description="基本法条款§150，定义项目基本宪法原则（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§151": ConstitutionArticle(
        section="§151",
        name="观测回路引用",
        category="basic",
        description="控制论观测回路引用，用于状态监控和审计追踪（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    
    # === 技术法示例性引用 (§200-§299) ===
    "§206": ConstitutionArticle(
        section="§206",
        name="预留工具链扩展",
        category="technical",
        description="预留工具链扩展条款（示例性引用）",
        usage="工具扩展、体系完整性"
    ),
    "§207": ConstitutionArticle(
        section="§207",
        name="工具链安全标准",
        category="technical",
        description="工具链安全标准和规范（示例性引用）",
        usage="工具安全、标准规范"
    ),
    "§208": ConstitutionArticle(
        section="§208",
        name="知识漂移检测标准",
        category="technical",
        description="知识漂移检测标准，确保系统知识保持最新（示例性引用）",
        usage="知识管理、质量保证"
    ),
    "§205": ConstitutionArticle(
        section="§205",
        name="程序效率优化",
        category="technical",
        description="程序效率优化标准，预留程序效率优化（示例性引用）",
        usage="性能优化、效率标准"
    ),
    "§209": ConstitutionArticle(
        section="§209",
        name="紧急处理程序",
        category="technical",
        description="紧急处理程序标准，预留紧急处理程序（示例性引用）",
        usage="应急处理、危机管理"
    ),
    "§212": ConstitutionArticle(
        section="§212",
        name="预留程序扩展",
        category="technical",
        description="预留程序扩展标准，预留扩展条款（示例性引用）",
        usage="系统扩展、预留功能"
    ),
    "§219": ConstitutionArticle(
        section="§219",
        name="技术法条款§219",
        category="technical",
        description="技术法条款§219，定义系统技术规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§220": ConstitutionArticle(
        section="§220",
        name="数据管理标准",
        category="technical",
        description="数据管理和存储标准（示例性引用）",
        usage="数据管理、存储标准"
    ),
    "§229": ConstitutionArticle(
        section="§229",
        name="操作法条款§229",
        category="technical",
        description="操作法条款§229，定义系统操作规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§319": ConstitutionArticle(
        section="§319",
        name="工具桥接器标准",
        category="technical",
        description="工具桥接器标准，定义文件操作和安全性规范（示例性引用）",
        usage="工具集成、文件安全"
    ),
    "§321": ConstitutionArticle(
        section="§321",
        name="预留技术标准",
        category="technical",
        description="预留技术标准，用于未来扩展（示例性引用）",
        usage="技术扩展、未来兼容"
    ),
    "§329": ConstitutionArticle(
        section="§329",
        name="技术标准§329",
        category="technical",
        description="技术标准条款§329，定义系统技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§231": ConstitutionArticle(
        section="§231",
        name="资源策略§231",
        category="technical",
        description="操作法条款§231，定义资源与模型策略（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§232": ConstitutionArticle(
        section="§232",
        name="资源策略§232",
        category="technical",
        description="操作法条款§232，定义资源与模型策略（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§233": ConstitutionArticle(
        section="§233",
        name="资源策略§233",
        category="technical",
        description="操作法条款§233，定义资源与模型策略（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§234": ConstitutionArticle(
        section="§234",
        name="资源策略§234",
        category="technical",
        description="操作法条款§234，定义资源与模型策略（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§235": ConstitutionArticle(
        section="§235",
        name="资源策略§235",
        category="technical",
        description="操作法条款§235，定义资源与模型策略（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§238": ConstitutionArticle(
        section="§238",
        name="资源策略§238",
        category="technical",
        description="操作法条款§238，定义资源与模型策略（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§239": ConstitutionArticle(
        section="§239",
        name="资源策略§239",
        category="technical",
        description="操作法条款§239，定义资源与模型策略（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§242": ConstitutionArticle(
        section="§242",
        name="资源策略§242",
        category="technical",
        description="操作法条款§242，定义资源与模型策略（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§243": ConstitutionArticle(
        section="§243",
        name="资源策略§243",
        category="technical",
        description="操作法条款§243，定义资源与模型策略（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§249": ConstitutionArticle(
        section="§249",
        name="资源策略§249",
        category="technical",
        description="操作法条款§249，定义资源与模型策略（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§250": ConstitutionArticle(
        section="§250",
        name="系统治理§250",
        category="technical",
        description="操作法条款§250，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§251": ConstitutionArticle(
        section="§251",
        name="系统治理§251",
        category="technical",
        description="操作法条款§251，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§252": ConstitutionArticle(
        section="§252",
        name="系统治理§252",
        category="technical",
        description="操作法条款§252，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§253": ConstitutionArticle(
        section="§253",
        name="系统治理§253",
        category="technical",
        description="操作法条款§253，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§254": ConstitutionArticle(
        section="§254",
        name="系统治理§254",
        category="technical",
        description="操作法条款§254，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§255": ConstitutionArticle(
        section="§255",
        name="系统治理§255",
        category="technical",
        description="操作法条款§255，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§256": ConstitutionArticle(
        section="§256",
        name="系统治理§256",
        category="technical",
        description="操作法条款§256，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§257": ConstitutionArticle(
        section="§257",
        name="系统治理§257",
        category="technical",
        description="操作法条款§257，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§258": ConstitutionArticle(
        section="§258",
        name="系统治理§258",
        category="technical",
        description="操作法条款§258，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§259": ConstitutionArticle(
        section="§259",
        name="系统治理§259",
        category="technical",
        description="操作法条款§259，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§260": ConstitutionArticle(
        section="§260",
        name="系统治理§260",
        category="technical",
        description="操作法条款§260，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§261": ConstitutionArticle(
        section="§261",
        name="系统治理§261",
        category="technical",
        description="操作法条款§261，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§262": ConstitutionArticle(
        section="§262",
        name="系统治理§262",
        category="technical",
        description="操作法条款§262，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§264": ConstitutionArticle(
        section="§264",
        name="系统治理§264",
        category="technical",
        description="操作法条款§264，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§265": ConstitutionArticle(
        section="§265",
        name="系统治理§265",
        category="technical",
        description="操作法条款§265，定义系统扩展与治理（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§270.1": ConstitutionArticle(
        section="§270.1",
        name="技术标准§270.1",
        category="technical",
        description="技术标准条款§270.1，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§271": ConstitutionArticle(
        section="§271",
        name="技术标准§271",
        category="technical",
        description="技术标准条款§271，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§272": ConstitutionArticle(
        section="§272",
        name="技术标准§272",
        category="technical",
        description="技术标准条款§272，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§273": ConstitutionArticle(
        section="§273",
        name="技术标准§273",
        category="technical",
        description="技术标准条款§273，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§274": ConstitutionArticle(
        section="§274",
        name="技术标准§274",
        category="technical",
        description="技术标准条款§274，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§275": ConstitutionArticle(
        section="§275",
        name="技术标准§275",
        category="technical",
        description="技术标准条款§275，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§276": ConstitutionArticle(
        section="§276",
        name="技术标准§276",
        category="technical",
        description="技术标准条款§276，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§277": ConstitutionArticle(
        section="§277",
        name="技术标准§277",
        category="technical",
        description="技术标准条款§277，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§278": ConstitutionArticle(
        section="§278",
        name="技术标准§278",
        category="technical",
        description="技术标准条款§278，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§279": ConstitutionArticle(
        section="§279",
        name="技术标准§279",
        category="technical",
        description="技术标准条款§279，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§280": ConstitutionArticle(
        section="§280",
        name="技术标准§280",
        category="technical",
        description="技术标准条款§280，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§283": ConstitutionArticle(
        section="§283",
        name="技术标准§283",
        category="technical",
        description="技术标准条款§283，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§284": ConstitutionArticle(
        section="§284",
        name="技术标准§284",
        category="technical",
        description="技术标准条款§284，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§287": ConstitutionArticle(
        section="§287",
        name="技术标准§287",
        category="technical",
        description="技术标准条款§287，定义技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§288": ConstitutionArticle(
        section="§288",
        name="技术标准§288",
        category="technical",
        description="技术标准条款§288，定义系统技术实施规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§289": ConstitutionArticle(
        section="§289",
        name="前端与可视化标准",
        category="technical",
        description="前端与可视化标准，§288-§289: 前端与可视化标准（示例性引用）",
        usage="前端开发、可视化标准"
    ),
    "§290": ConstitutionArticle(
        section="§290",
        name="操作法条款§290",
        category="technical",
        description="操作法条款§290，定义系统操作规范（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    
    # === 程序法示例性引用 (§300-§399) ===
    "§307": ConstitutionArticle(
        section="§307",
        name="预留工作流扩展",
        category="procedural",
        description="预留工作流扩展条款（示例性引用）",
        usage="工作流扩展、体系完整性"
    ),
    "§313": ConstitutionArticle(
        section="§313",
        name="Claude Code集成 (旧编号)",
        category="procedural",
        description="旧编号的Claude Code集成条款，应该迁移到§309（示例性引用）",
        usage="向后兼容、迁移标识"
    ),
    "§314": ConstitutionArticle(
        section="§314",
        name="程序法条款§314",
        category="procedural",
        description="程序法条款§314，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§315": ConstitutionArticle(
        section="§315",
        name="程序法条款§315",
        category="procedural",
        description="程序法条款§315，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§316": ConstitutionArticle(
        section="§316",
        name="程序法条款§316",
        category="procedural",
        description="程序法条款§316，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§317": ConstitutionArticle(
        section="§317",
        name="程序法条款§317",
        category="procedural",
        description="程序法条款§317，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§318": ConstitutionArticle(
        section="§318",
        name="程序法条款§318",
        category="procedural",
        description="程序法条款§318，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§322": ConstitutionArticle(
        section="§322",
        name="程序法条款§322",
        category="procedural",
        description="程序法条款§322，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§323": ConstitutionArticle(
        section="§323",
        name="程序法条款§323",
        category="procedural",
        description="程序法条款§323，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§324": ConstitutionArticle(
        section="§324",
        name="程序法条款§324",
        category="procedural",
        description="程序法条款§324，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§325": ConstitutionArticle(
        section="§325",
        name="程序法条款§325",
        category="procedural",
        description="程序法条款§325，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§327": ConstitutionArticle(
        section="§327",
        name="程序法条款§327",
        category="procedural",
        description="程序法条款§327，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§328": ConstitutionArticle(
        section="§328",
        name="程序法条款§328",
        category="procedural",
        description="程序法条款§328，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§330": ConstitutionArticle(
        section="§330",
        name="程序法条款§330",
        category="procedural",
        description="程序法条款§330，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§339": ConstitutionArticle(
        section="§339",
        name="程序法条款§339",
        category="procedural",
        description="程序法条款§339，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§340": ConstitutionArticle(
        section="§340",
        name="程序法条款§340",
        category="procedural",
        description="程序法条款§340，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§349": ConstitutionArticle(
        section="§349",
        name="程序法条款§349",
        category="procedural",
        description="程序法条款§349，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§360": ConstitutionArticle(
        section="§360",
        name="程序法条款§360",
        category="procedural",
        description="程序法条款§360，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§369": ConstitutionArticle(
        section="§369",
        name="程序法条款§369",
        category="procedural",
        description="程序法条款§369，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§370": ConstitutionArticle(
        section="§370",
        name="程序法条款§370",
        category="procedural",
        description="程序法条款§370，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§379": ConstitutionArticle(
        section="§379",
        name="程序法条款§379",
        category="procedural",
        description="程序法条款§379，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§380": ConstitutionArticle(
        section="§380",
        name="程序法条款§380",
        category="procedural",
        description="程序法条款§380，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§389": ConstitutionArticle(
        section="§389",
        name="程序法条款§389",
        category="procedural",
        description="程序法条款§389，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    "§390": ConstitutionArticle(
        section="§390",
        name="程序法条款§390",
        category="procedural",
        description="程序法条款§390，定义工作流程和验证标准（示例性引用）",
        usage="模板引用，保持法律体系完整性"
    ),
    
    # === 公理层示例性引用 (§400-§699) ===
    "§426": ConstitutionArticle(
        section="§426",
        name="公理层引用§426",
        category="axiomatic",
        description="公理层引用§426，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§434": ConstitutionArticle(
        section="§434",
        name="公理层引用§434",
        category="axiomatic",
        description="公理层引用§434，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§450": ConstitutionArticle(
        section="§450",
        name="公理层引用§450",
        category="axiomatic",
        description="公理层引用§450，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§459": ConstitutionArticle(
        section="§459",
        name="公理层引用§459",
        category="axiomatic",
        description="公理层引用§459，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§499": ConstitutionArticle(
        section="§499",
        name="公理层引用§499",
        category="axiomatic",
        description="公理层引用§499，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§500": ConstitutionArticle(
        section="§500",
        name="公理层引用§500",
        category="axiomatic",
        description="公理层引用§500，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§510": ConstitutionArticle(
        section="§510",
        name="公理层引用§510",
        category="axiomatic",
        description="公理层引用§510，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§511": ConstitutionArticle(
        section="§511",
        name="公理层引用§511",
        category="axiomatic",
        description="公理层引用§511，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§518": ConstitutionArticle(
        section="§518",
        name="公理层引用§518",
        category="axiomatic",
        description="公理层引用§518，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§520": ConstitutionArticle(
        section="§520",
        name="公理层引用§520",
        category="axiomatic",
        description="公理层引用§520，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§521": ConstitutionArticle(
        section="§521",
        name="公理层引用§521",
        category="axiomatic",
        description="公理层引用§521，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§530": ConstitutionArticle(
        section="§530",
        name="公理层引用§530",
        category="axiomatic",
        description="公理层引用§530，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§531": ConstitutionArticle(
        section="§531",
        name="公理层引用§531",
        category="axiomatic",
        description="公理层引用§531，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§540": ConstitutionArticle(
        section="§540",
        name="公理层引用§540",
        category="axiomatic",
        description="公理层引用§540，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§541": ConstitutionArticle(
        section="§541",
        name="公理层引用§541",
        category="axiomatic",
        description="公理层引用§541，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§554": ConstitutionArticle(
        section="§554",
        name="公理层引用§554",
        category="axiomatic",
        description="公理层引用§554，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§555": ConstitutionArticle(
        section="§555",
        name="公理层引用§555",
        category="axiomatic",
        description="公理层引用§555，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§559": ConstitutionArticle(
        section="§559",
        name="公理层引用§559",
        category="axiomatic",
        description="公理层引用§559，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§561": ConstitutionArticle(
        section="§561",
        name="公理层引用§561",
        category="axiomatic",
        description="公理层引用§561，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§569": ConstitutionArticle(
        section="§569",
        name="公理层引用§569",
        category="axiomatic",
        description="公理层引用§569，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§571": ConstitutionArticle(
        section="§571",
        name="公理层引用§571",
        category="axiomatic",
        description="公理层引用§571，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§579": ConstitutionArticle(
        section="§579",
        name="公理层引用§579",
        category="axiomatic",
        description="公理层引用§579，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§599": ConstitutionArticle(
        section="§599",
        name="公理层引用§599",
        category="axiomatic",
        description="公理层引用§599，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§600": ConstitutionArticle(
        section="§600",
        name="公理层引用§600",
        category="axiomatic",
        description="公理层引用§600，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§601": ConstitutionArticle(
        section="§601",
        name="公理层引用§601",
        category="axiomatic",
        description="公理层引用§601，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§609": ConstitutionArticle(
        section="§609",
        name="公理层引用§609",
        category="axiomatic",
        description="公理层引用§609，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§610": ConstitutionArticle(
        section="§610",
        name="公理层引用§610",
        category="axiomatic",
        description="公理层引用§610，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§619": ConstitutionArticle(
        section="§619",
        name="公理层引用§619",
        category="axiomatic",
        description="公理层引用§619，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§620": ConstitutionArticle(
        section="§620",
        name="公理层引用§620",
        category="axiomatic",
        description="公理层引用§620，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§629": ConstitutionArticle(
        section="§629",
        name="公理层引用§629",
        category="axiomatic",
        description="公理层引用§629，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§630": ConstitutionArticle(
        section="§630",
        name="公理层引用§630",
        category="axiomatic",
        description="公理层引用§630，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§639": ConstitutionArticle(
        section="§639",
        name="公理层引用§639",
        category="axiomatic",
        description="公理层引用§639，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§640": ConstitutionArticle(
        section="§640",
        name="公理层引用§640",
        category="axiomatic",
        description="公理层引用§640，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),
    "§649": ConstitutionArticle(
        section="§649",
        name="公理层引用§649",
        category="axiomatic",
        description="公理层引用§649，示例性引用，用于模板展示",
        usage="模板引用，保持法律体系完整性"
    ),

    # === 旧编号迁移示例 ===
    "§438": ConstitutionArticle(
        section="§438",
        name="双存储映射标准 (旧编号)",
        category="technical",
        description="旧编号的双存储映射标准，应该迁移到§207（向后兼容示例）",
        usage="向后兼容、迁移标识"
    ),
    "§440": ConstitutionArticle(
        section="§440",
        name="知识漂移检测 (旧编号)",
        category="technical",
        description="旧编号的知识漂移检测标准，应该迁移到§208（向后兼容示例）",
        usage="向后兼容、迁移标识"
    ),
    "§501": ConstitutionArticle(
        section="§501",
        name="输入输出标准 (旧编号)",
        category="technical",
        description="旧编号的输入输出标准，应该迁移到§320（向后兼容示例）",
        usage="向后兼容、迁移标识"
    ),
    "§502": ConstitutionArticle(
        section="§502",
        name="预留技术标准 (旧编号)",
        category="technical",
        description="旧编号的预留技术标准，应该迁移到§321（向后兼容示例）",
        usage="向后兼容、迁移标识"
    ),
    "§550": ConstitutionArticle(
        section="§550",
        name="执行层标准一 (旧编号)",
        category="procedural",
        description="旧编号的执行层标准一，应该迁移到§350（向后兼容示例）",
        usage="向后兼容、迁移标识"
    ),
    "§551": ConstitutionArticle(
        section="§551",
        name="执行层标准二 (旧编号)",
        category="procedural",
        description="旧编号的执行层标准二，应该迁移到§351（向后兼容示例）",
        usage="向后兼容、迁移标识"
    ),
    "§552": ConstitutionArticle(
        section="§552",
        name="执行层标准三 (旧编号)",
        category="procedural",
        description="旧编号的执行层标准三，应该迁移到§352（向后兼容示例）",
        usage="向后兼容、迁移标识"
    ),
}


def get_reference_article(section: str) -> Optional[ConstitutionArticle]:
    """
    获取指定示例性引用条款的定义
    
    Args:
        section: 条款编号，如 "§108" 或 "108"
        
    Returns:
        ConstitutionArticle 或 None
    """
    # 规范化条款编号
    if not section.startswith("§"):
        section = f"§{section}"
    
    return CONSTITUTION_REFERENCE_ARTICLES.get(section)


def get_all_reference_sections() -> List[str]:
    """获取所有示例性引用条款编号列表"""
    return list(CONSTITUTION_REFERENCE_ARTICLES.keys())


if __name__ == "__main__":
    print(f"CDD Constitution References v2.0.0")
    print(f"示例性引用总数: {len(CONSTITUTION_REFERENCE_ARTICLES)}")
    print("注意: 这些是用于模板展示的示例性引用，不影响核心功能。")
    print("实际使用的核心条款请参考 core/constitution_core.py")