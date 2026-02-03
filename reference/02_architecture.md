# CDD Architecture & Legal Framework

**Version**: v1.6.1
**Type**: T0 (System Axiom)
**Purpose**: Defines the immutable laws, architectural layers, and entropy metrics of the CDD system.

---

## 🏛️ I. The Legal Framework (宪法体系)

CDD 系统依据以下三类法典运行。所有开发行为必须符合法典约束。

### §100 Basic Law (基本法 - 核心公理)
* **§102.3 Synchronization Axiom**: 代码 ($C$) 与文档 ($D$) 必须原子性同步。$\Delta C \neq 0 \implies \Delta D \neq 0$。
* **§152 Single Source of Truth**: `memory_bank/` 是唯一真理源。严禁在多个位置维护同一状态。
* **§201.5 Entropy Reduction**: 所有变更必须证明其有助于降低或维持系统熵值 ($H_{sys}$)。$\Delta H_{sys} \le 0$。

### §300 Technical Law (技术法 - 实现约束)
* **§300.1 Spore Protocol**: CDD Skill 是一个附着于宿主项目 (`TARGET_ROOT`) 的独立孢子。严禁污染宿主业务逻辑。
* **§315 Isomorphism Principle**: 文件系统结构 ($S_{fs}$) 必须与文档定义的架构 ($S_{doc}$) 同构。$S_{fs} \cong S_{doc}$。

---

## 🏗️ II. The T0-T3 Document Hierarchy (架构分层)

为了优化 Agent 的 **Context Window ($H_{cog}$)**，CDD 采用四级加载策略。

| Tier | Name | Token Cost | Role | Loading Policy |
|:---:|:---|:---:|:---|:---|
| **T0** | **Kernel** (Consciousness) | < 800 | 身份、当前状态、导航图谱 | **Always Resident** |
| **T1** | **Axioms** (Physics) | < 2000 | 架构模式、接口签名、行为公理 | **On-Demand** (Arch Check) |
| **T2** | **Standards** (Legislation) | < 500/file | 特性规范、实施计划、任务清单 | **Lazy Load** (Task Execution) |
| **T3** | **Archives** (History) | 0 | 审计日志、历史版本 | **Audit Only** |

### 核心文件映射
* **T0**: `memory_bank/core/active_context.md` (State), `knowledge_graph.md` (Relationships)
* **Meta**: `SKILL.md` (Project Overview & Agent Directives)
* **T1**: `memory_bank/axioms/system_patterns.md` (Topology), `tech_context.md` (Signatures)
* **T2**: `memory_bank/standards/DS-*` (Templates)

---

## 📉 III. System Entropy Metrics ($H_{sys}$)

系统熵值是衡量软件腐化的核心指标。

$$H_{sys} = w_1 \cdot H_{cog} + w_2 \cdot H_{struct} + w_3 \cdot H_{align}$$

### 1. Metric Definitions
* **$H_{cog}$ (Cognitive Load)**: 上下文污染度。
    * Formula: $Tokens_{loaded} / Tokens_{limit}$
    * Goal: $< 0.4$
* **$H_{struct}$ (Structural Entropy)**: 文件组织混乱度。
    * Formula: $1 - (N_{indexed\_files} / N_{total\_files})$
    * Goal: $< 0.1$ (All files must be indexed)
* **$H_{align}$ (Alignment Deviation)**: 实现与规范的偏离度。
    * Formula: $1 - (Sig_{matched} / Sig_{total})$
    * Goal: $0.0$ (Strict Isomorphism)

### 2. Thresholds (v1.6.1 Calibrated)
* 🟢 **Green ($0.0 - 0.3$)**: Healthy. Allow feature development.
* 🟡 **Yellow ($0.3 - 0.7$)**: Debt accumulation. Refactor recommended.
* 🔴 **Red ($> 0.7$)**: Critical state. **STOP** all feature work. Initiate `Refactoring Protocol`.

---

## ⚖️ IV. Three-Tier Verification (司法验证)

任何状态变更 (State C $\to$ D) 必须通过三级验证：

1.  **Tier 1 (Structural)**: `tree src/` matches `system_patterns.md`.
2.  **Tier 2 (Signature)**: Code symbols match `tech_context.md`.
3.  **Tier 3 (Behavioral)**: Tests pass and satisfy `behavior_context.md` invariants.

> **Tooling**: Use `scripts/cdd_audit.py` to enforce these gates automatically.