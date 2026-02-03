# Constitution-Driven Development Skill (CDD)

**Version**: 1.6.1  
**Codename**: Memory Bank First  
**License**: Apache-2.0  
**Author**: wsman

A comprehensive skill for OpenClaw that implements Constitution-Driven Development (CDD) methodology using MiniMax M2.1 model. Features **Memory Bank First** architecture, ecosystem automation, GitHub integration, and governance protocols.

## Overview

CDD is a systematic approach to AI-assisted software development that enforces strict documentation-driven workflows, three-tier verification, and system entropy monitoring. v1.6.1 introduces **Memory Bank First** principle with **Spore Protocol (Seed→Root→Sprout)**, ecosystem automation with GitHub sync, feature scaffolding, and constitution amendment protocols.

## Features

- 🌱 **Memory Bank First**: Biological architecture design with Spore Protocol (Seed→Root→Sprout)
- 📜 **T0/T1/T2 Document System**: Core consciousness → System axioms → Executable standards
- 🔄 **Five-State Workflow**: A→B→C→D→E (Ingest → Plan → Execute → Verify → Converge)
- ✅ **Three-Tier Verification**: Structure → Signatures → Behavior
- 📊 **Entropy Monitoring**: Real-time $H_{sys}$ metrics with compliance-based scoring
- 🤖 **External Auditor**: Third-party AI review with deepseek-reasoner
- 🚀 **Ecosystem Automation**: GitHub Issues sync, feature scaffolding scripts
- ⚖️ **Governance Protocols**: Constitution amendment workflows (SemVer-based)
- 📋 **Knowledge Graph**: Mermaid visualization support

## Document Hierarchy

| Level | Name | Tokens | Description |
|-------|------|--------|-------------|
| **T0** | Core Consciousness | <800 | Must always be loaded (5 core documents) |
| **T1** | System Axioms | <200 | NEW: systemPatterns, techContext, behaviorContext |
| **T2** | Executable Standards | <100/task | Lazy loaded on demand (DS/WF files) |
| **T3** | Archives | 0 | Loaded only for audit |

## Architecture

```mermaid
graph TD
    subgraph External [External Layer]
        Auditor[External Auditor<br/>deepseek-reasoner]
        Discord[Discord Notification]
    end
    
    subgraph T0 [T0 Core Layer]
        README[README.md<br/>Bootloader Input]
        ActiveCtx[active_context.md]
        KG[KNOWLEDGE_GRAPH<br/>with Mermaid]
        BasicLaw[Basic Law Index]
        ProcLaw[Procedural Law Index]
        TechLaw[Technical Law Index]
    end
    
    subgraph T1 [T1 System Axioms]
        SysPatterns[system_patterns.md]
        TechCtx[tech_context.md]
        BehaviorCtx[behavior_context.md]
    end
    
    Auditor -->|Review| T0
    Auditor -->|Report| Discord
    
    README --> ActiveCtx
    ActiveCtx --> KG
    KG --> BasicLaw
    BasicLaw --> SysPatterns
    BasicLaw --> TechCtx
    BasicLaw --> BehaviorCtx
```

## Core Workflow (Closed-Loop)

```
1. Load README.md (Bootloader Input - One-shot)
2. Load All 5 T0 Documents + 3 T1 Documents
3. Calculate H_sys (Entropy Baseline)
4. Execute CDD Five-State Workflow (A→B→C→D→E)
5. Detect T0 Changes
   ├─ No Change → Continue Development
   └─ Change → Trigger External Audit
6. External Audit (deepseek-reasoner, max_tokens=8192)
   ├─ Review T0 Documents
   ├─ Generate Report with real API data
   └─ Send to Discord
7. User Confirmation
8. Closed-Loop Verification (Tier 1/2/3)
9. Complete/Continue
```

## Quick Start

### 🌱 Using the Spore Deployer (推荐 - 自动化部署)

使用新的 `deploy_cdd.py` 脚本自动化初始化 Memory Bank 结构和工具链：

```bash
# Clone this skill to your OpenClaw skills directory
git clone https://github.com/wsman/Constitution-Driven-Development-Skill.git
cp -r Constitution-Driven-Development-Skill/ ../openclaw/skills/cdd/

# Navigate to your target project directory
cd /path/to/your/project

# 使用 Spore 部署协议初始化 Memory Bank
python ../openclaw/skills/cdd/scripts/deploy_cdd.py "Your Project Name"

# 或者，如果已经在 CDD 技能库目录中：
cd /path/to/openclaw/skills/cdd
python scripts/deploy_cdd.py "Your Project Name" --target /path/to/your/project
```

### 📁 手动方法 (备选方案)

如果需要手动控制，可以使用原始方法：

```bash
# For a new project, create Memory Bank:
cd /path/to/your/project
mkdir -p memory_bank/core
mkdir -p memory_bank/axioms
mkdir -p memory_bank/protocols
mkdir -p memory_bank/standards

# Copy T0 templates (core)
cp cdd/templates/core/*_index.md memory_bank/core/
cp cdd/templates/core/active_context.md memory_bank/core/
cp cdd/templates/core/knowledge_graph.md memory_bank/core/

# Copy T1 templates (axioms)
cp cdd/templates/axioms/system_patterns.md memory_bank/axioms/
cp cdd/templates/axioms/tech_context.md memory_bank/axioms/
cp cdd/templates/axioms/behavior_context.md memory_bank/axioms/

# Copy T2 templates (protocols/standards)
cp cdd/templates/protocols/*.md memory_bank/protocols/
cp cdd/templates/standards/*.md memory_bank/standards/

# Create project README from template
cp reference/project_readme_template.md README.md
```

## 🛡️ Standard Usage Protocol (标准使用协议)

为了确保 CDD SKILL 的稳定性和目标项目的安全性，所有操作必须遵循以下 **"自检-执行"** 流程：

### Phase 1: Environment Self-Check (环境自检)
在调用任何 CDD 工具之前，**必须**先检查 CDD SKILL 本身的宪法合规性。此步骤确保工具链未被篡改且处于稳定状态。

```bash
# ⚠️ 仅作用于 CDD SKILL 自身目录
# 运行 Gate 1-3 完整审计
python scripts/cdd_audit.py

```

> **注意**: `cdd_audit.py` 是唯一一个**严禁**指定外部目标文件夹的脚本。它被硬编码为仅审计本技能库 (`PROJECT_ROOT`)。

### Phase 2: Targeted Execution (指定目标执行)

确认环境无误后，使用交付工具对您的业务项目进行操作。**所有交付脚本都必须明确指定目标路径。**

| 脚本名称 | 用途 | 必需参数 | 示例 |
| --- | --- | --- | --- |
| `deploy_cdd.py` | 部署 CDD Memory Bank 结构 | `--target <path>` | `python scripts/deploy_cdd.py "MyProj" --target ../my-app` |
| `cdd-feature.py` | 生成特性文档 (DS-050/051/052) | `--target <path>` | `python scripts/cdd-feature.py "Login" --target ../my-app` |
| `measure_entropy.py` | 测量系统熵值 ($H_{sys}$) | `--project <path>` | `python scripts/measure_entropy.py --project ../my-app` |
| `verify_versions.py` | 校验版本一致性 (Gate 1 核心) | `--project <path>` 或 `--fix` | `python scripts/verify_versions.py --project ../my-app --fix` |

> 🚫 **警告**: 严禁在不带参数的情况下运行上述脚本，否则它们将默认修改 CDD SKILL 自身的源码结构。

**工具版本与功能**:
- `deploy_cdd.py` (v2.0): 孢子部署器，实现 Seed→Root→Sprout 协议
- `cdd-feature.py` (v2.1.0): 特性脚手架生成器，支持跨项目运行
- `measure_entropy.py` (v1.4.0): 熵值计量器，计算 $H_{sys}$ 并输出 JSON 报告
- `verify_versions.py` (v1.7.0): 版本一致性检查器，支持自动修复 (--fix)
- `cdd_audit.py` (v1.0): 宪法审计器，运行 Gate 1-3 (仅用于 CDD 技能库自检)

## Project Structure

```
cdd/
├── SKILL.md                           # AI agent interface (v1.6.1)
├── README.md                          # User-facing project overview (v1.6.1)
├── Makefile                           # Local development interface
├── reference/                         # Reference documentation directory (T1)
│   ├── 01_handbook.md                 # CDD operations manual
│   ├── 02_architecture.md             # Constitutional principles & entropy metrics
│   ├── 03_toolchain.md                # CLI tools and configuration guide
│   ├── 04_core_workflow.md            # 5-state workflow definition
│   ├── 05_templates_index.md          # Centralized index of all templates
│   ├── 06_project_readme_template.md  # Project README template
│   └── 07_feature_readme_template.md  # Feature README template (generated by cdd-feature.py)
├── templates/                         # Template directory (T0-T2)
│   ├── 01_core/                       # T0 Kernel layer (5 documents)
│   │   ├── active_context.md          # Active Context (v1.6.1)
│   │   ├── knowledge_graph.md         # Knowledge Graph with Mermaid support
│   │   ├── basic_law_index.md         # Core axioms index
│   │   ├── procedural_law_index.md    # Workflow procedures index
│   │   └── technical_law_index.md     # Technical constraints index
│   ├── 02_axioms/                     # T1 Axioms layer (3 documents)
│   │   ├── system_patterns.md         # Architecture patterns & directory structure
│   │   ├── tech_context.md            # Technology stack & interface signatures
│   │   └── behavior_context.md        # Testing scenarios & invariants
│   ├── 03_protocols/                  # Workflow protocols (WF-* documents)
│   │   ├── WF-001_clarify_workflow.md # Clarification workflow
│   │   ├── WF-201_cdd_workflow.md     # Standard CDD execution protocol
│   │   ├── WF-amend.md                # Amendment protocol
│   │   ├── WF-analyze.md              # Analysis protocol
│   │   ├── WF-review.md               # Review protocol
│   │   └── WF-sync-issues.md          # GitHub issue sync protocol
│   └── 04_standards/                  # T2 Standards layer (DS-* documents)
│       ├── DS-007_context_management.md   # Context management standard
│       ├── DS-050_feature_specification.md    # Feature specification (REQUIRED)
│       ├── DS-051_implementation_plan.md       # Implementation plan (REQUIRED)
│       ├── DS-052_atomic_tasks.md              # Atomic tasks breakdown
│       ├── DS-053_quality_checklist.md         # Quality assurance checklist
│       ├── DS-054_environment_hardening.md     # Environment hardening guide
│       └── DS-060_code_review.md               # Code review findings template
└── scripts/                           # Toolchain scripts
    ├── cdd_audit.py                   # Constitutional auditor (Gate 1-3)
    ├── cdd-feature.py                 # Feature scaffold generator (v2.1.2)
    ├── deploy_cdd.py                  # Spore deployer (v2.0.1)
    ├── measure_entropy.py             # Entropy calculator (v1.4.0)
    ├── verify_versions.py             # Version consistency checker (v1.7.0)
    └── utils/                         # Utility modules
        ├── cache_manager.py           # Entropy calculation caching
        └── command_utils.py           # CLI execution utilities
```

## Core Mathematics (v1.6.1)

**System Entropy** (Updated with H_align):
$$
H_{sys} = 0.4 \cdot H_{cog} + 0.3 \cdot H_{struct} + 0.3 \cdot H_{align}
$$

Where:
- **H_cog** (Cognitive Load): $T_{load} / 8000$
- **H_struct** (Structural Entropy): $1 - N_{linked}/N_{total}$
- **H_align** (Alignment Deviation): $N_{violation} / N_{constraints}$ (NEW)

**Calibration Standard** (v1.6.1):
- 🟢 **Excellent**: $0.0 - 0.3$ (Calibration Target)
- 🟡 **Good**: $0.3 - 0.5$ (Normal Development)
- 🟠 **Warning**: $0.5 - 0.7$ (Start Repairs)
- 🔴 **Danger**: $0.7 - 1.0$ (Force Refactoring)

**Attention Distribution**:
$$
\text{Attention}(T0) \gg \text{Attention}(T1) > \text{Attention}(T2) \gg \text{Attention}(T3)
$$

## Usage

Use with OpenClaw + MiniMax M2.1 for development, DeepSeek-Reasoner for auditing:

```bash
# In OpenClaw
/cdd "Your development task description"
```

## 🛡️ 宪法门禁 (Constitutional Guardrails)

本项目依据 **CDD (Constitution-Driven Development)** 实施自动化审计。任何提交必须通过以下三道自动化门禁：

| 门禁 (Gate) | 检查项 | 宪法依据 | 失败后果 |
|-------------|--------|----------|----------|
| **Gate 1** | **版本一致性** | §102.3 同步公理 | 拒绝合并 (Non-negotiable) |
| **Gate 2** | **行为验证** | Tier 3 行为标准 | 拒绝合并 (Functional Regression) |
| **Gate 3** | **熵值监控** | 系统热力学定律 | $H_{sys} > 0.5$ 时构建失败 |

### 💻 本地开发 (Makefile)

为确保代码能通过 CI 门禁，请在提交前使用 `Makefile` 进行本地预审：

```bash
# 运行完整宪法审计 (推荐)
make audit

# 仅检查版本一致性
make gate1

# 自动修复版本漂移
make fix-versions

```

更多细节请参考 [自动化工作流文档](https://www.google.com/search?q=.github/workflows/cdd_guardrails.yml)。

## CDD Workflow

1. **State A (Context Ingestion)**: Load T0 + T1 documents
2. **State B (Documentation First)**: Plan in T0/T1 docs, wait for approval
3. **State C (Safe Implementation)**: Execute code changes
4. **State D (Three-Tier Verification)**:
   - **Tier 1**: Structure ($S_{fs} \cong S_{doc}$) vs `system_patterns.md`
   - **Tier 2**: Signatures ($I_{code} \supseteq I_{doc}$) vs `tech_context.md`
   - **Tier 3**: Behavior ($B_{code} \equiv B_{spec}$) vs `behavior_context.md`
5. **State E (Converge)**: Calibrate $H_{sys} \leq 0.3$, complete

## External Auditor (v1.6.1)

CDD includes an **External Auditor** for third-party AI review:

- **Trigger**: T0 document changes
- **Model**: deepseek-reasoner
- **Max Tokens**: 8192 (for complete audit output)
- **Scope**: T0 documents only
- **Output**: Markdown report with real API data → Discord notification

**API Data Requirement** (v1.6.1):
- Request ID, timestamps, latency (ms), token counts (exact, no estimates)

## Closed-Loop Verification Checklist

Before completing any task, verify:

| Check | Standard | Template |
|-------|----------|----------|
| Code ↔ Architecture Isomorphism | `code` ≅ `system_patterns.md` | system_patterns.md |
| Interface ↔ Signature Match | `interface` ⊇ `tech_context.md` | tech_context.md |
| Behavior ↔ Assertion Consistency | `behavior` ≡ `behavior_context.md` | behavior_context.md |
| T0 Documents Synced | All 5 T0 docs updated | - |
| Entropy Calibrated | $H_{sys} \leq 0.3$ | active_context.md |
| External Audit Passed | (If T0 changed) | Audit Report |

## Documentation System (面向不同受众)

CDD 维护两个主要的项目文档，分别服务于不同的目标读者：

| 文档 | 目标读者 | 内容重点 | 发布位置 |
|------|----------|----------|----------|
| **`README.md`** (本文件) | **真人开发者**、项目贡献者、初次使用者 | 项目介绍、安装使用、架构说明、快速开始指南 | GitHub 项目主页 |
| **`SKILL.md`** | **AI 代理** (如 OpenClaw、Claude 等) | AI 角色定义、工具链接口、宪法护栏、工作流状态机 | AI 技能库 (供 AI 直接加载) |
| **`reference/` 目录** | **深入学习的开发者**和 **AI 代理** | 详细的操作手册、架构原理、工具链说明、模板索引 | 项目内部参考文档 |

### 核心参考文档索引 (`reference/` 目录)

CDD 将所有详细文档组织在 `reference/` 目录中，按功能编号：

| ID | 文档 | 用途 |
|----|------|------|
| **01** | [`01_handbook.md`](reference/01_handbook.md) | **操作手册**：CDD 详细使用指南，T0-T3 系统说明 |
| **02** | [`02_architecture.md`](reference/02_architecture.md) | **架构原理**：宪法、公理、熵值指标和核心法律层 |
| **03** | [`03_toolchain.md`](reference/03_toolchain.md) | **工具链**：CLI 工具使用指南和配置说明 |
| **04** | [`04_core_workflow.md`](reference/04_core_workflow.md) | **工作流**：5 状态工作流 (Intake→Close) 定义 |
| **05** | [`05_templates_index.md`](reference/05_templates_index.md) | **模板索引**：所有可用模板的集中目录 |
| **06** | [`06_project_readme_template.md`](reference/06_project_readme_template.md) | **项目模板**：用于创建项目级 README 文档 |
| **07** | [`07_feature_readme_template.md`](reference/07_feature_readme_template.md) | **特性模板**：用于创建特性级 README (由 `cdd-feature.py` 生成) |

## References

- See [`SKILL.md`](SKILL.md) Appendix A for entropy calculation scripts
- See [`reference/01_handbook.md`](reference/01_handbook.md) for complete CDD usage guide
- See [`templates/01_core/knowledge_graph.md`](templates/01_core/knowledge_graph.md) for Mermaid visualization examples
- See [`templates/02_axioms/system_patterns.md`](templates/02_axioms/system_patterns.md) for Tier 1 verification template
- See [`templates/02_axioms/tech_context.md`](templates/02_axioms/tech_context.md) for Tier 2 verification template
- See [`templates/02_axioms/behavior_context.md`](templates/02_axioms/behavior_context.md) for Tier 3 verification template

## 🚀 CDD v1.6.1 (Memory Bank First) - Gold Release

**Status**: 🟢 Production Ready | **Score**: 9.5/10 | **Audit**: deepseek-reasoner

### v1.6.1 New Features

| Component | Function |
|-----------|----------|
| `scripts/deploy_cdd.py` | **Spore Protocol**: Seed→Root→Sprout deployment with Memory Bank First |
| `SKILL.md` | Enhanced with Memory Bank First constitutional guardrails (v1.6.1) |
| `reference/project_readme_template.md` | Updated with correct memory_bank/core/ paths |
| Memory Bank Architecture | Biological growth model: **Seed → Root → Sprout** |
| Cross-Space Interaction | AI agent resolves `{SKILL_ROOT}` for remote deployment |
| Automated Detection | AI automatically detects and initializes missing `memory_bank/` |

### Quick Start (v1.6.1)

```bash
# Clone
git clone https://github.com/wsman/Constitution-Driven-Development-Skill.git
cd Constitution-Driven-Development-Skill

# Create new feature
python scripts/cdd-feature.py "Add User Login"

# Dry run (no changes)
python scripts/cdd-feature.py "Add User Login" --dry-run
```

### Version History & Features

#### v1.6.1 (Memory Bank First)
- **Feature**: 引入 **Memory Bank First** 宪法护栏作为最高优先级规则。
- **Feature**: 实现 **Spore Protocol (Seed→Root→Sprout)** 仿生学部署流程。
- **Feature**: 增强 SKILL.md 支持跨空间交互 (`{SKILL_ROOT}` 路径解析)。
- **Feature**: `deploy_cdd.py` 自动创建完整 Memory Bank 结构。
- **Feature**: 更新所有模板路径为 `memory_bank/core/` 标准结构。

#### v1.6.0 (Automated Governance)
- **Feature**: `cdd_audit.py` 全面接管审计。
- **Feature**: 实现 Gate 1-3 自动化检查。
- **Feature**: 引入 `--ai-hint` 支持 AI 自愈。
- **Fix**: 熵值阈值调整为 0.7。

#### v1.5.0 (Foundation)
- **Feature**: 确立 T0-T2 文档体系。
- **Feature**: 引入熵值计算脚本 `measure_entropy.py`。

#### Earlier Milestones
| Version | Focus |
|---------|-------|
| v1.0-v1.2 | T0/T1/T2 document system + five-state workflow |
| v1.3 | Entropy metrics + external auditing |
| v1.4 | Quality gates integration |

### Documentation

- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Upgrade from v1.4.0
- [SKILL.md](SKILL.md) - Complete skill documentation

## License

Licensed under the Apache License, Version 2.0. See LICENSE file for details.
