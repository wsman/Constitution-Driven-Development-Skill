# Constitution-Driven Development Skill (CDD)

**Version**: 1.0.0  
**License**: Apache-2.0  
**Author**: wsman

A comprehensive skill for OpenClaw that implements Constitution-Driven Development (CDD) methodology using MiniMax M2.1 model.

## Overview

CDD is a systematic approach to AI-assisted software development that enforces strict documentation-driven workflows, three-tier verification, and system entropy monitoring. It features a closed-loop architecture with external auditing capabilities.

## Features

- 📜 **Three-Law System**: Basic Law → Procedural Law → Technical Law
- 🔄 **Five-State Workflow**: A→B→C→D→E (Ingest → Plan → Execute → Verify → Converge)
- ✅ **Three-Tier Verification**: Structure → Signatures → Behavior
- 📊 **Entropy Monitoring**: Real-time $H_{sys}$ metrics
- 🎯 **T0-T3 Document Hierarchy**: Systematic context management
- 🤖 **External Auditor**: Third-party AI review with deepseek-reasoner
- 📋 **Project README**: Background documentation for audits and onboarding

## Document Hierarchy

| Level | Name | Tokens | Description |
|-------|------|--------|-------------|
| **T0** | Core Consciousness | <800 | Must always be loaded (5 core documents) |
| **T1** | Axioms & Indices | <200 | Loaded when T0 insufficient |
| **T2** | Executable Standards | <100/task | Lazy loaded on demand |
| **T3** | Archives | 0 | Loaded only for audit |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CDD Architecture Overview                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              External Auditor (deepseek-reasoner)               │   │
│  │  T0 Review → Report → Discord Notification                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    T0 Core Consciousness Layer                  │   │
│  │  README.md → activeContext → KNOWLEDGE_GRAPH → Basic/Proc/Tech  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    CDD Five-State Workflow                      │   │
│  │    State A → State B → State C → State D → State E              │   │
│  │    (Ingest) (Plan) (Execute) (Verify) (Converge)                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Workflow (Closed-Loop)

```
1. Load README.md (Project Background)
2. Load All 5 T0 Documents
3. Execute CDD Five-State Workflow (A→B→C→D→E)
4. Detect T0 Changes
   ├─ No Change → Continue Development
   └─ Change → Trigger External Audit
5. External Audit (deepseek-reasoner)
   ├─ Review T0 Documents
   ├─ Generate Report
   └─ Send to Discord
6. User Confirmation
7. Closed-Loop Verification
8. Complete/Continue
```

## Quick Start

```bash
# Clone this skill to your OpenClaw skills directory
cp -r Constitution-Driven-Development-Skill/ ../openclaw/skills/cdd/

# For a new project, create Memory Bank:
cd /path/to/your/project
mkdir -p memory_bank/00_indices
mkdir -p memory_bank/01_active_state
mkdir -p memory_bank/02_systemaxioms
mkdir -p memory_bank/03_protocols/workflows
mkdir -p memory_bank/03_protocols/standards

# Copy templates
cp cdd/templates/*_index.md memory_bank/00_indices/
cp cdd/templates/activeContext.md memory_bank/01_active_state/
cp cdd/templates/KNOWLEDGE_GRAPH.md memory_bank/02_systemaxioms/

# Create project README from template
cp cdd/templates/readme_template.md README.md
```

## Structure

```
cdd/
├── SKILL.md                         # Main skill file (1225 lines)
├── README.md                        # This file
├── reference/
│   └── document_classification_guide.md  # Document classification guide
└── templates/                       # T0 document templates
    ├── 01_basic_law_index.md        # Basic Law Index
    ├── 02_procedural_law_index.md   # Procedural Law Index
    ├── 03_technical_law_index.md    # Technical Law Index
    ├── activeContext.md             # Active Context
    ├── KNOWLEDGE_GRAPH.md           # Knowledge Graph
    ├── cdd_config.yaml              # CDD Configuration (External Auditor)
    ├── guide.md                     # Template Usage Guide
    └── readme_template.md           # Project README Template
```

## Core Mathematics

**System Entropy**:
$$
H_{sys} = 0.4 \cdot \frac{T_{load}}{8000} + 0.3 \cdot \left(1 - \frac{N_{linked}}{N_{total}}\right) + 0.3 \cdot \frac{F_{drift}}{F_{total}}
$$

**Attention Distribution**:
$$
\text{Attention}(T0) \gg \text{Attention}(T1) > \text{Attention}(T2) \gg \text{Attention}(T3)
$$

## Usage

Use with OpenClaw + MiniMax M2.1:

```bash
# In OpenClaw
/cdd "Your development task description"
```

## CDD Workflow

1. **State A (Context Ingestion)**: Load T0 documents
2. **State B (Documentation First)**: Plan in T0 docs, wait for approval
3. **State C (Safe Implementation)**: Execute code changes
4. **State D (Three-Tier Verification)**: Structure → Signatures → Behavior
5. **State E (Convergence)**: Calibrate and complete

## External Auditor

CDD includes an **External Auditor** role for third-party AI review:

- **Trigger**: T0 document changes
- **Model**: deepseek-reasoner (via DeepSeek API)
- **Scope**: T0 documents only
- **Output**: Markdown report → Discord notification

**Core Philosophy**:
> "Evaluate document logic clarity and structure through third-party perspective."

## Closed-Loop Verification Checklist

Before completing any task, verify:

| Check | Standard |
|-------|----------|
| Code ↔ Architecture Isomorphism | `code` ≅ `systemPatterns.md` |
| Interface ↔ Signature Match | `interface` ⊇ `techContext.md` |
| Behavior ↔ Assertion Consistency | `behavior` ≡ `behaviorContext.md` |
| T0 Documents Synced | All 5 T0 docs updated |
| Entropy达标 | $H_{sys} \leq 0.3$ |
| External Audit Passed | (If T0 changed) |

## References

- See `reference/document_classification_guide.md` for complete documentation
- See `templates/guide.md` for template usage guide
- See `templates/readme_template.md` for project README template

## License

Licensed under the Apache License, Version 2.0. See LICENSE file for details.
