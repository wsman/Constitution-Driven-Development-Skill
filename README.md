# Constitution-Driven Development Skill (CDD)

**Version**: 1.0.0  
**License**: Apache-2.0  
**Author**: wsman

A comprehensive skill for OpenClaw that implements Constitution-Driven Development (CDD) methodology using MiniMax M2.1 model.

## Overview

CDD is a systematic approach to AI-assisted software development that enforces strict documentation-driven workflows, three-tier verification, and system entropy monitoring.

## Features

- 📜 **Three-Law System**: Basic Law → Procedural Law → Technical Law
- 🔄 **Five-State Workflow**: A→B→C→D→E (Ingest → Plan → Execute → Verify → Converge)
- ✅ **Three-Tier Verification**: Structure → Signatures → Behavior
- 📊 **Entropy Monitoring**: Real-time $H_{sys}$ metrics
- 🎯 **T0-T3 Document Hierarchy**: Systematic context management

## Document Hierarchy

| Level | Name | Tokens | Description |
|-------|------|--------|-------------|
| **T0** | Core Consciousness | <800 | Must always be loaded |
| **T1** | Axioms & Indices | <200 | Loaded when T0 insufficient |
| **T2** | Executable Standards | <100/task | Lazy loaded on demand |
| **T3** | Archives | 0 | Loaded only for audit |

## Quick Start

```bash
# Clone this skill to your OpenClaw skills directory
cp -r Constitution-Driven-Development-Skill/ ../openclaw/skills/cdd/
```

## Structure

```
cdd/
├── SKILL.md                    # Main skill file
├── templates/                  # T0 document templates
│   ├── 01_basic_law_index.md
│   ├── 02_procedural_law_index.md
│   ├── 03_technical_law_index.md
│   ├── activeContext.md
│   └── KNOWLEDGE_GRAPH.md
├── reference/                 # Reference documentation
│   └── 文档分级体系说明书.md
└── LICENSE                   # Apache-2.0
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

## References

- See `reference/文档分级体系说明书.md` for complete documentation
- See `templates/README.md` for template usage guide

## License

Licensed under the Apache License, Version 2.0. See LICENSE file for details.
