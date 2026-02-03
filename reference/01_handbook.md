# 01_Handbook: CDD Operations Manual

**Type**: Operational Guide (Reference)
**Purpose**: Detailed instructions on how to operate the CDD system, managing documents, and using prompts.

## 1. The T0-T3 Documentation System
CDD organizes knowledge into four tiers to optimize context loading.

### T0: Kernel (Consciousness)
* **Files**: `active_context.md`, `knowledge_graph.md`, `basic_law_index.md`, 
            `procedural_law_index.md`, `technical_law_index.md`
* **Location**: `templates/01_core/`
* **Usage**: 5-dimensional truth representation. Must be loaded at the start of every session. Contains the "Now" and the "Self".

**Note**: `SKILL.md` is the project overview (meta-document) and serves as the entry point for AI agents.

### T1: Axioms (Physics)
* **Files**: `system_patterns.md`, `tech_context.md`, `behavior_context.md`
* **Location**: `templates/02_axioms/`
* **Usage**: Defines the invariant rules of the project (directory structure, technology stack, and behavior scenarios). Consult when designing architecture.

### T2: Standards (Legislation)
* **Files**: `DS-050_feature_specification.md` (required), `DS-051_implementation_plan.md` (required), `DS-052_atomic_tasks.md`, `DS-053_quality_checklist.md`, `DS-054_environment_hardening.md`, `DS-060_code_review.md`, `DS-007_context_management.md`
* **Location**: `templates/04_standards/`
* **Usage**: The "Bill" that becomes Law. Every feature request MUST generate at least DS-050 and DS-051 documents first.

### T3: Archives (History)
* **Files**: Runtime-generated audit logs (e.g., `decision_log.md`, `changelog.md`)
* **Usage**: Write-only logs for auditing project history and decisions. These are created during project execution, not stored as templates.

## 2. Prompt Engineering Guide
When acting as the CDD Architect, use these structures:

### The "Entropy Check" Block
Before any action, assess the state:
> **Entropy Check**:
> - Current $H_{sys}$: (Value or Estimate)
> - Risk: (Low/High)
> - Action: Proceed / Refactor

### The "Memory Update" Block
When closing a task:
> **Memory Update**:
> - Modified: `active_context.md` (State moved to E)
> - Created: `src/new_feature.py`
> - Verified: `cdd_audit.py` passed.

## 3. Dealing with Templates
Do not copy templates blindly. Follow this 4‑step workflow:

1.  **Select**: Identify the correct template ID from `reference/05_templates_index.md`.
    - **DS‑* (Standards)**: For feature development (auto‑instantiated)
    - **WF‑* (Protocols)**: For workflow execution (manual copy)
    - **AX‑* (Axioms)**: For architectural definitions (pre‑installed)

2.  **Instantiate**: For feature development, run:
    ```bash
    python scripts/cdd‑feature.py "Feature Name"
    ```
    This creates `specs/{ID}-{name}/` with DS‑050/051/052 and a README.

3.  **Fill**: Open the generated files and replace `{{PLACEHOLDERS}}` with actual project data.

4.  **Link**: Ensure the feature's README is referenced in `knowledge_graph.md` for traceability.

## 4. Document Query Guide for AI Agents
As an AI agent operating the CDD system, you need to efficiently query information from the three core reference documents. This guide helps you determine **when** to consult **which document** and **how** to extract the needed information.

### 4.1 Core Reference Documents Overview

| Document | Purpose | Key Information | When to Consult |
|----------|---------|-----------------|-----------------|
| **`02_architecture.md`** | **宪法架构** | Legal Framework (宪法条款), System Entropy Metrics ($H_{sys}$), T0-T3 Hierarchy, Three-Tier Verification, **Integrated Toolchain & Workflow Matrix** | When you need to: • Understand constitutional laws (§100-§300) • Calculate or interpret system entropy ($H_{sys}$) • Check architectural compliance • See the big-picture integration of tools, workflow, and scenarios |
| **`03_toolchain.md`** | **工具链参考** | Complete tool directory, usage scenarios, parameter specifications, configuration guides, **Tool Usage Timing Matrix** | When you need to: • Run any CDD script (`deploy_cdd.py`, `cdd-feature.py`, etc.) • Understand tool parameters and options • Configure `cdd_config.yaml` • Know when to use each tool |
| **`04_core_workflow.md`** | **工作流引擎** | 5-State Workflow details, state transitions, **Entropy Crisis Protocol**, **Checkpoint Recovery**, **Standardized Scenarios** | When you need to: • Execute the 5-state workflow (A→B→C→D→E) • Handle state transitions • Manage checkpoint recovery • Respond to entropy crises ($H_{sys} > 0.7$) |

### 4.2 Query Decision Matrix by Scenario

Use this matrix to quickly find the right document for your current task:

| Scenario | Primary Document | Secondary Document | Key Information to Extract |
|----------|------------------|-------------------|----------------------------|
| **Starting New Project** | `03_toolchain.md` | `02_architecture.md` | • `deploy_cdd.py` usage (§102.3) • Memory Bank initialization • Constitutional constraints |
| **Continuing from Checkpoint** | `04_core_workflow.md` | `01_handbook.md` | • Checkpoint recovery process (§125) • Reading `active_context.md` • Resuming workflow state |
| **State A→B Transition** | `04_core_workflow.md` | `03_toolchain.md` | • `cdd-feature.py` parameters (§141) • DS-050 generation • Approval workflow |
| **State B→C Transition** | `04_core_workflow.md` | `02_architecture.md` | • Manual implementation requirements (§152) • Code structure compliance • Interface signature matching |
| **State C→D Transition** | `03_toolchain.md` | `04_core_workflow.md` | • `cdd_audit.py` gates (§201.3) • Three-tier verification details • Audit pass/fail criteria |
| **State D→E Transition** | `04_core_workflow.md` | `01_handbook.md` | • Updating `active_context.md` (§125) • Closing workflow loop • Git commit requirements |
| **Entropy Crisis ($H_{sys} > 0.7$)** | `02_architecture.md` | `04_core_workflow.md` | • Entropy Crisis Protocol (§201.5) • Refactoring priorities • Recovery standards |
| **Version Drift Repair** | `03_toolchain.md` | `02_architecture.md` | • `verify_versions.py` usage (§102.3) • Version consistency requirements • Auto-fix procedures |
| **System Health Monitoring** | `03_toolchain.md` | `02_architecture.md` | • `measure_entropy.py` parameters • Entropy metric definitions • Threshold interpretation |
| **Uncertain About Usage** | `01_handbook.md` | `02_architecture.md` | • Overall system operation • Constitutional foundations • Cross-document navigation |

### 4.3 Effective Query Process

Follow this 3-step process when you need information:

**Step 1: Identify Your Scenario**
- What are you trying to accomplish? (e.g., "start new project", "continue from checkpoint", "transition state A→B")
- Refer to the **Standardized Scenarios** in `04_core_workflow.md` or `SKILL.md` for scenario identification.

**Step 2: Consult Primary Document**
- Based on the scenario matrix above, open the **Primary Document**.
- Use the document's table of contents or search for:
  - **Scenario keywords** (e.g., "State A→B Transition", "Entropy Crisis")
  - **Tool names** (e.g., "cdd-feature.py", "measure_entropy.py")
  - **Constitutional references** (e.g., "§102.3", "§201.5")

**Step 3: Cross-Reference with Secondary Document**
- If the primary document doesn't contain all needed information, consult the **Secondary Document**.
- Look for complementary information, especially:
  - Constitutional basis for the action
  - Detailed tool parameters
  - Workflow state implications

### 4.4 Quick Reference Examples

#### Example 1: Starting a New Project
```markdown
**Query Process**:
1. **Scenario**: "🚀 Start New Project"
2. **Primary Document**: `03_toolchain.md` → Section "1. Project Initialization Tools"
3. **Extract**: `deploy_cdd.py` usage, parameters, examples
4. **Secondary Document**: `02_architecture.md` → Section "V. Toolchain & Workflow Integration"
5. **Extract**: Constitutional basis (§102.3), Memory Bank architecture
```

#### Example 2: Handling Entropy Crisis
```markdown
**Query Process**:
1. **Scenario**: "🔥 Entropy Crisis ($H_{sys} > 0.7$)"
2. **Primary Document**: `02_architecture.md` → Section "V.2 Entropy Crisis Protocol"
3. **Extract**: Stop criteria, refactoring priorities, recovery standards
4. **Secondary Document**: `04_core_workflow.md` → Section "🔥 Entropy Crisis Protocol"
5. **Extract**: Detailed crisis response workflow, tool interactions
```

#### Example 3: State C→D Transition
```markdown
**Query Process**:
1. **Scenario**: "✅ State C→D Transition"
2. **Primary Document**: `03_toolchain.md` → Section "3. Verification Phase Tools"
3. **Extract**: `cdd_audit.py` gates, parameters, output formats
4. **Secondary Document**: `04_core_workflow.md` → Section "C→D: Execute → Verify"
5. **Extract**: Verification checks, constitutional basis (§201.3)
```

### 4.5 Integration with SKILL.md

The `SKILL.md` file provides a **scenario-driven navigation index** that complements this query guide:

- **For quick scenario lookup**: Use `SKILL.md` → "🎯 Standardized Scenarios for AGENT Operations"
- **For detailed query guidance**: Use this section (`01_handbook.md` → "4. Document Query Guide")
- **For constitutional understanding**: Use `02_architecture.md` → "V. Toolchain & Workflow Integration"

**Remember**: Always start with `SKILL.md` for scenario identification, then use this query guide to determine which detailed document to consult.

### 4.6 Constitutional Query Principles

1. **§102.3 Synchronization Axiom**: When you query tool usage, also check its constitutional basis.
2. **§141 State Machine Axiom**: When querying workflow states, ensure you understand the state transitions.
3. **§201.5 Entropy Reduction Axiom**: When querying entropy-related topics, consider the impact on $H_{sys}$.
4. **§152 Single Source of Truth**: Each piece of information has one primary source document; avoid consulting multiple sources for the same information.

**Last Updated**: 2026-02-03 (Integrated with v1.6.1 enhancements to `02_architecture.md`, `03_toolchain.md`, `04_core_workflow.md`)
