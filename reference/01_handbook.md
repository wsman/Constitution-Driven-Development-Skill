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
