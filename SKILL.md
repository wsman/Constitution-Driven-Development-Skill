---
name: cdd
description: 宪法驱动开发 (Constitution-Driven Development)。使用MiniMax M2.1模型在OpenClaw中进行AI辅助软件开发，遵循三级法律体系（基本法、程序法、技术法）约束，通过五状态工作流(A→E)和三级验证确保代码质量。
model: minimax/MiniMax-M2.1
---

# 宪法驱动开发 (CDD)

使用 MiniMax M2.1 模型进行 AI 辅助软件开发，遵循逆熵实验室三级法律体系约束。

## 📐 架构概览

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CDD 架构全景                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      外部审计层 (External Auditor)              │   │
│  │  deepseek-reasoner → 审计T0文档 → 报告 → Discord抄送            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    T0 核心意识层 (始终加载)                      │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │   │
│  │  │README   │ │Active   │ │Knowledge│ │ Basic   │ │Procedural│  │   │
│  │  │.md      │ │Context  │ │Graph    │ │Law      │ │Law      │  │   │
│  │  │(项目背景)│ │(当前焦点)│ │(导航图) │ │(核心公理)│ │(工作流) │  │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘  │   │
│  │       ↓            ↓           ↓           ↓           ↓       │   │
│  │       └────────────┴───────────┴───────────┴───────────┘       │   │
│  │                         ↓ 强制加载                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    T1 系统公理层 (按需加载)                      │   │
│  │     systemPatterns.md (架构约束) → techContext.md (接口)        │   │
│  │                        → behaviorContext.md (行为断言)          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    T2 执行标准层 (懒加载)                        │   │
│  │     workflows/ (WF-xxx) → standards/ (DS-xxx) → 执行 → 释放     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    CDD 五状态工作流                              │   │
│  │    State A → State B → State C → State D → State E              │   │
│  │    (基准摄入) (策略规划) (受控执行) (三级验证) (收敛纠错)         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🔄 核心流程 (闭环)

```
【启动】 OpenClaw + MiniMax M2.1 启动
    ↓
【1】加载 README.md (项目背景文档，来自 readme_template.md)
    ↓
【2】加载全部 T0 文档 (5个)
    ↓
【3】执行 CDD 五状态工作流
    ├─ State A: 加载 T1 文档，基准摄入
    ├─ State B: 文档规划，用户批准
    ├─ State C: 按文档执行代码修改
    ├─ State D: 三级验证 (Tier 1/2/3)
    └─ State E: 收敛纠错，校准确认
    ↓
【4】T0 文档变更检测
    ├─ 无变更 → 继续开发
    └─ 有变更 → 触发外部审计
    ↓
【5】外部审计 (deepseek-reasoner)
    ├─ 审查 T0 文档
    ├─ 生成审计报告
    └─ 发送到 Discord
    ↓
【6】用户确认 / 修正
    ↓
【7】校准检查 (闭环验证)
    ├─ 代码 ↔ systemPatterns.md 同构
    ├─ 接口 ↔ techContext.md 匹配
    ├─ 行为 ↔ behaviorContext.md 一致
    └─ $H_{sys} ≤ 0.3$
    ↓
【8】结束 → 返回 State A (或退出)

### Memory Bank 结构
在使用 CDD skill 之前，**必须在项目文件夹下创建 `memory_bank` 目录**：

```
memory_bank/
├── 00_indices/                    # 🔥 T0-法律体系索引层
│   ├── 01_basic_law_index.md      # T0-基本法索引 (宪法内核/Bootloader协议)
│   ├── 02_procedural_law_index.md # T0-程序法索引 (核心流程指针)
│   └── 03_technical_law_index.md  # T0-技术法索引 (技术公理指针)
├── 01_active_state/               # T0-活跃上下文层
│   ├── activeContext.md           # T0-活跃上下文 (当前短期记忆与焦点)
│   └── systemState.md             # T1-系统状态
├── 02_systemaxioms/               # T0/T1-意识与架构层
│   ├── KNOWLEDGE_GRAPH.md         # T0-神经中枢 (全局联想导航图)
│   ├── systemPatterns.md          # T1-ASCII目录树约束
│   ├── techContext.md             # T1-接口签名约束
│   └── behaviorContext.md         # T1-行为断言
├── 03_protocols/                  # T2-协议与标准
│   ├── workflows/                 # T2-标准工作流 (WF-xxx)
│   └── standards/                 # T2-DS-xxx实现标准
└── cdd_config.yaml                # CDD配置 (外部审计者/API配置)

### ⭐ 项目README.md (项目背景文档)

**定义**: 描述项目背景、技术栈、核心功能的概览文档，**不属于T0级别**。
**模板来源**: `templates/readme_template.md` (复制到项目根目录后重命名为 `README.md`)

**位置**: 项目根目录 (与 `memory_bank/` 同级)

**内容**:
- 项目名称和描述
- 技术栈概览
- 核心功能列表
- 外部依赖 (API、数据源)
- 项目定位 (如: 量化分析系统)

**与T0的区别**:
| 特性 | T0文档 | README.md (项目背景) |
|------|--------|---------------------|
| 加载时机 | 始终加载 | 仅首次或需要时 |
| 约束作用 | 强制约束 | 仅供参考 |
| 大小目标 | <800 tokens | 无限制 |
| 属于Memory Bank | 是 | 否 |

**使用时机**:
1. 项目初始化时创建 (复制 `readme_template.md`)
2. 外部审计前提供背景信息
3. 新成员加入时了解项目
```

**T0层级导航：**
```
启动 → 加载活跃上下文 (短期记忆)
     → 加载神经中枢 (导航能力)
     → 加载法律体系索引 (行为准则)
          → 基本法索引 (核心公理)
          → 程序法索引 (工作流指针)
          → 技术法索引 (标准指针)
```

### 🔥 T0级别核心文档（强制）

**T0 = 核心意识与引导层 (Kernel & Consciousness)**

**定义**: 系统启动时的最小必要集合 (Minimum Viable Context)。这些文档必须常驻内存或被优先索引，它们构成了系统的"自我意识"和"导航能力"。

**5个T0文档：**

| 文件 | 类型 | 别名 | 定义 | 大小目标 |
|------|------|------|------|----------|
| `activeContext.md` | T0-活跃上下文 | 当前短期记忆 | 当前短期记忆与焦点 | <800 tokens |
| `KNOWLEDGE_GRAPH.md` | T0-神经中枢 | 全局联想导航图 | 全局联想导航图 | <1000 tokens |
| `01_basic_law_index.md` | T0-基本法索引 | 宪法内核 | 宪法内核与 Bootloader 协议 | <500 tokens |
| `02_procedural_law_index.md` | T0-程序法索引 | 核心流程指针 | 核心流程索引与指针 | <300 tokens |
| `03_technical_law_index.md` | T0-技术法索引 | 技术公理指针 | 核心技术公理与指针 | <500 tokens |

**T0层级结构：**

```
┌─────────────────────────────────────────────────────────────┐
│               T0 核心意识与引导层                              │
│              (Kernel & Consciousness)                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐                    │
│  │  活跃上下文       │  │   神经中枢       │                    │
│  │  activeContext  │  │ KNOWLEDGE_GRAPH │                    │
│  │  (短期记忆/焦点)  │  │ (全局联想导航)   │                    │
│  └─────────────────┘  └─────────────────┘                    │
│  ┌─────────────────────────────────────────────────┐        │
│  │               法律体系索引层                       │        │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐     │        │
│  │  │ 基本法索引 │ │ 程序法索引 │ │ 技术法索引 │     │        │
│  │  │ (Bootloader│ │ (流程指针) │ │ (公理指针) │     │        │
│  │  │  协议)     │ │           │ │           │     │        │
│  │  └───────────┘ └───────────┘ └───────────┘     │        │
│  └─────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### 📋 其他文档级别

**T0只有以上5个文档，其他文档按重要程度分为T1/T2/T3：**

| 级别 | 类型 | 示例文件 | 说明 |
|------|------|----------|------|
| **T1** | 系统公理 | `systemPatterns.md`, `techContext.md`, `behaviorContext.md` | 项目架构约束（重要） |
| **T2** | 协议标准 | `workflows/*.md`, `standards/*.md` | DS/WF标准文件（一般） |
| **T3** | 临时记录 | `*.log`, `*.tmp` | 临时文件（可清理） |

### ⚡ T0文档生命周期规则（强制）

#### 1. 创建阶段（项目初始化）
- ✅ **第一时间创建**: 项目开始时必须创建全部5个T0文档
- ✅ **初始加载**: OpenClaw + MiniMax 启动后立即加载全部T0文档到上下文
- ✅ **版本标记**: 标记为 v1.0.0，版本同步

#### 2. 计划阶段（修改前）
- ✅ **先文档后代码**: 任何项目修改前，必须先在T0文档中制定计划
- ✅ **反映在文档中**: 计划必须反映在：
  - `activeContext.md` - 任务描述、变更向量
  - `systemPatterns.md` - 架构变更
  - `techContext.md` - 接口变更
  - `behaviorContext.md` - 行为变更
- ✅ **用户批准**: 等待用户确认 (YES) 后才能进入执行阶段

#### 3. 执行阶段（代码修改）
- ✅ **按文档执行**: 严格依据T0文档中的计划进行代码修改
- ✅ **保持加载**: T0文档必须保持在上下文中
- ✅ **实时校准**: 代码变更必须与T0文档同步更新

#### 4. 验证阶段（三级验证）
- ✅ **文档一致性检查**: Tier 1 验证前先检查T0文档与代码的一致性
- ✅ **三级验证**: Tier 1(结构) → Tier 2(签名) → Tier 3(行为)

#### 5. 结项阶段（校准与归档）
- ✅ **完全校准**: 任务完成后，**必须**与T0文档完全校准：
  - 代码 ↔ `systemPatterns.md` (架构同构 $S_{fs} \cong S_{doc}$)
  - 接口 ↔ `techContext.md` (签名匹配 $I_{code} \supseteq I_{doc}$)
  - 行为 ↔ `behaviorContext.md` (行为断言 $B_{code} \equiv B_{spec}$)
- ✅ **更新activeContext**: 记录完成状态和验证结果
- ✅ **熵值验证**: 确保 $\Delta H > 0$ (熵减)
- ✅ **结项条件**: **只有完全一致才能结项** ❗

### 🔥 内核加载规则（强制）

**OpenClaw + MiniMax 开发时，每一步都必须加载索引内核到上下文：**

| 索引文件 | 内容 | 大小目标 |
|----------|------|----------|
| `01_basic_law_index.md` | 基本法核心公理摘要 + 引用路径 | <500 tokens |
| `02_procedural_law_index.md` | 程序法工作流索引 + WF-xxx路径 | <300 tokens |
| `03_technical_law_index.md` | 技术法标准索引 + DS-xxx路径 | <500 tokens |

**加载时机：**
- ✅ **每一步开发操作前**：必须确认T0文档已在上下文中
- ✅ **新对话开始时**：立即加载全部T0文档
- ✅ **切换任务时**：重新确认T0文档加载状态

**禁止行为：**
- ❌ 加载完整法典文件到内存
- ❌ 在上下文中保留超过5个T0文档
- ❌ 绕过T0文档直接修改代码
- ❌ 在未加载T0文档的情况下执行CDD流程
- ❌ **未完成校准就结项**

**工作流程：**
```
1. [创建] 5个T0文档 (项目初始化)
2. [加载] T0文档到上下文 (每一步操作前)
3. [计划] 先在T0文档中制定计划 (先文档后代码)
4. [执行] 按T0文档计划执行代码修改
5. [验证] 三级验证 + T0文档一致性检查
6. [校准] 代码 ↔ T0文档完全一致
7. [结项] 只有完全一致才能结项
```

### 📊 知识图谱架构

Memory Bank 中的文档按**级别**组织：

```
memory_bank/
├── 00_indices/                    # 🔥 T0（必须始终加载）
│   ├── 01_basic_law_index.md
│   ├── 02_procedural_law_index.md
│   └── 03_technical_law_index.md
├── 01_active_state/               # T0/T1
│   └── activeContext.md           # T0-活动上下文
├── 02_systemaxioms/               # T1（项目架构）
│   ├── KNOWLEDGE_GRAPH.md         # T0-知识图谱入口
│   ├── systemPatterns.md          # T1-目录树约束
│   ├── techContext.md             # T1-接口约束
│   └── behaviorContext.md         # T1-行为断言
└── 03_protocols/                  # T2（协议标准）
    ├── workflows/                 # T2-WF-xxx工作流
    └── standards/                 # T2-DS-xxx标准
```

### 📋 文档级别体系

| 级别 | 定义 | 加载时机 | 示例 |
|------|------|----------|------|
| **T0** | 核心意识与引导层 (Kernel & Consciousness)<br>系统启动时的最小必要集合，常驻内存或优先索引 | 始终加载 | 活跃上下文、知识图谱、3个法律索引 |
| **T1** | 系统公理与全局索引层 (Axioms & Indices)<br>系统的世界观与查找表。当 T0 层无法提供足够细节，或需要进行 $O(1)$ 精确检索时加载 | 按需加载 (T0不足时) | systemPatterns, techContext, behaviorContext |
| **T2** | 协议与标准层 (Protocols & Standards)<br>具体的实现标准和操作流程 | 按需加载 (执行时) | workflows/*.md, standards/*.md |
| **T3** | 临时记录层 (Temporary Records)<br>临时日志、缓存、可清理文件 | 临时使用 | *.log, *.tmp |

**T1层级结构：**
```
┌─────────────────────────────────────────────────────────────────┐
│                   T1 系统公理与全局索引层                          │
│               (Axioms & Indices)                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────────────────────────┐   │
│  │   核心定义 (Axioms) │  │       全局查找表 (Indices)        │   │
│  │ ┌───────────────┐ │  │ ┌─────────────────────────────┐   │   │
│  │ │ systemPatterns│ │  │ │ LAW_REFERENCE_MAP          │   │   │
│  │ │ techContext   │ │  │ │ STANDARD_CATALOG          │   │   │
│  │ │ behaviorContext│ │ │ │ DECISION_LOG              │   │   │
│  │ └───────────────┘ │  │ └─────────────────────────────┘   │   │
│  │                   │  └───────────────────────────────────┘   │
│  │ ┌───────────────────────────────────────────────────────┐   │
│  │ │  CONCEPTS │ ARCHITECTURE │ GLOSSARY │ systemState   │   │
│  │ └───────────────────────────────────────────────────────┘   │
│  └─────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

**T1文档分类：**
| 类别 | 文件 | 说明 |
|------|------|------|
| **核心定义** | systemPatterns, techContext, behaviorContext | 项目架构约束 |
| **全局查找表** | LAW_REFERENCE_MAP, STANDARD_CATALOG, DECISION_LOG | O(1)定位 |
| **概念定义** | CONCEPTS, ARCHITECTURE, GLOSSARY | 术语与架构 |
| **状态快照** | systemState | 组件状态 |

**T1加载条件：**
- T0层的索引无法满足需求时
- 需要 $O(1)$ 精确检索项目特定约束时
- 进行三级验证前加载

### 必须创建的T0文档
1. **基本法索引**: `00_indices/01_basic_law_index.md`
2. **程序法索引**: `00_indices/02_procedural_law_index.md`
3. **技术法索引**: `00_indices/03_technical_law_index.md`
4. **活动上下文**: `01_active_state/activeContext.md`
5. **知识图谱入口**: `02_systemaxioms/KNOWLEDGE_GRAPH.md`

### T1级别文档
| 文件 | 别名 | 定义 | 加载时机 |
|------|------|------|----------|
| `systemPatterns.md` | 系统模式图谱 | ASCII目录树约束，项目的架构蓝图 | T0不足时 |
| `techContext.md` | 接口上下文 | 接口签名约束，API规范定义 | T0不足时 |
| `behaviorContext.md` | 行为上下文 | 关键行为断言，运行时约束 | T0不足时 |
| `LAW_REFERENCE_MAP.md` | 全局查找表 | 文件路径映射，O(1)定位 | T0不足时 |
| `STANDARD_CATALOG.md` | 标准目录 | 标准分类目录 | T0不足时 |
| `systemState.md` | 系统状态 | 组件状态快照 | T0不足时 |
| `DECISION_LOG.md` | 决策记忆 | 历史架构决策记录 | T0不足时 |
| `CONCEPTS.md` | 核心概念 | 项目核心概念定义 | T0不足时 |
| `ARCHITECTURE.md` | 架构蓝图 | 系统架构蓝图 | T0不足时 |
| `GLOSSARY.md` | 术语表 | 专业术语定义 | |

### 📖 T0不足时 T2: 执行标准与协议层 (Executable Standards)

**定义**: 具体的**可执行规范 (Lazy Loaded Implementation)**。绝大多数时候处于"休眠"状态，仅通过图谱导航或索引检索**按需加载**。

**T2文档分类:**
| 类别 | 文件模式 | 说明 | 示例 |
|------|----------|------|------|
| **DS 标准库** | `standards/DS-*.md` | 技术实现标准 | DS-001 (UTF-8), DS-002 (原子写入), DS-007 (架构验证) |
| **工作流库** | `workflows/WF-*.md` | 操作流程标准 | WF-201 (CDD流程), WF-210 (安全操作) |
| **MCP 工具库** | `mcp_library/MC-*.md` | MCP协议标准 | MC-010 (故障排除) |
| **API 规范库** | `api_reference/AP-*.md` | 接口定义标准 | AP-xxx (API契约) |

**懒加载协议 (Lazy Loading Protocol):**
```
1. 检索 → 在 LAW_REFERENCE_MAP.md 或 STANDARD_CATALOG.md 中查找关键词
2. 加载 → 使用 read_file 读取具体的 DS-xxx 或 WF-xxx 文件
3. 执行 → 按照标准实现
4. 释放 → 完成后释放上下文（通过不再引用细节）
5. 验证 → 确保实现符合相关宪法条款
```

**T2层级结构:**
```
┌─────────────────────────────────────────────────────────────────┐
│                   T2 执行标准与协议层                             │
│           (Executable Standards)                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐        │
│  │   DS 标准库   │  │  工作流库     │  │  MCP 工具库   │        │
│  │ standards/   │  │ workflows/   │  │ mcp_library/ │        │
│  │ DS-001~DS-050│  │ WF-201~WF-230│  │ MC-010~MC-099│        │
│  └───────────────┘  └───────────────┘  └───────────────┘        │
│                        ┌───────────────┐                      │
│                        │  API 规范库   │                      │
│                        │ api_reference│                      │
│                        │ AP-*.md      │                      │
│                        └───────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

**T2加载规则:**
- ✅ 任务执行时才加载
- ✅ 完成特定标准检索后加载
- ✅ 任务完成后立即释放
- ❌ 不常驻内存
- ❌ 不在T0/T1不足时加载

### T3级别文档
| 级别 | 示例 | 说明 |
|------|------|------|
| T3 | `*.log`, `*.tmp`, `archive/` | 临时文件、历史归档 |

### 📦 模板使用

**通用模板位置**: `skills/cdd/templates/`

```bash
# 复制T0模板到项目memory bank
cp -r skills/cdd/templates/* memory_bank/
```

**T0级别模板（5个文件，必须第一时间创建）：**
| 文件 | 类型 | 说明 |
|------|------|------|
| `01_basic_law_index.md` | T0-基本法 | 基本法核心公理索引 |
| `02_procedural_law_index.md` | T0-程序法 | 程序法工作流索引 |
| `03_technical_law_index.md` | T0-技术法 | 技术法标准索引 |
| `activeContext.md` | T0-活跃上下文 | 活动上下文模板（含 $H_{sys}$ 仪表盘） |
| `KNOWLEDGE_GRAPH.md` | T0-知识图谱 | 知识图谱模板（核心拓扑 + 领域簇） |

**其他文档级别：**
| 级别 | 示例 | 说明 |
|------|------|------|
| T1 | `systemPatterns.md`, `techContext.md` | 项目架构约束 |
| T2 | `workflows/*.md`, `standards/*.md` | DS/WF标准，按需加载 |

### 📊 T3: 分析与归档层 (Analysis & Archives)

**定义**: 系统的**元数据与历史记录**。用于审计、分析或回溯，通常不需要在开发任务中加载。

**T3文档分类:**
| 类别 | 文件模式 | 说明 | 加载时机 |
|------|----------|------|----------|
| **分析报告** | `04_analysis_and_visualization/*.md` | 系统性能分析、架构评估、熵值趋势 | 仅审计时 |
| **历史归档** | `archive/*.md` | 历史版本备份、已弃用标准、项目历史记录 | 仅回溯时 |
| **可视化元数据** | `codex_graph.json`, `codex_summary.json`, `entropy_monitoring_report.md` | 节点关系图、摘要索引、熵监控报告 | 仅分析时 |

**T3层级结构:**
```
┌─────────────────────────────────────────────────────────────────┐
│                   T3 分析与归档层                                 │
│               (Analysis & Archives)                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────────────────────────┐   │
│  │   分析报告库       │  │        历史归档库                  │   │
│  │ 04_analysis_and_ │  │           archive/                │   │
│  │   visualization/ │  │                                   │   │
│  │                   │  │  历史版本 │ 已弃用标准 │ 项目历史  │   │
│  └───────────────────┘  └───────────────────────────────────┘   │
│                        ┌───────────────────┐                   │
│                        │  可视化元数据      │                   │
│                        │ codex_graph.json  │                   │
│                        │ codex_summary.json│                   │
│                        │ entropy_*.md     │                   │
│                        └───────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

**T3访问策略:**
- ✅ **审计时加载**: 仅在进行系统审计时加载
- ✅ **只读访问**: 所有T3文件均为只读参考
- ✅ **冷存储**: 支持归档到外部存储系统
- ❌ **不在开发任务中加载**: 保持低熵状态

### 📚 参考文档库

**完整文档体系说明**: `skills/cdd/reference/document_classification_guide.md`
- 版本: v1.0.0
- 宪法依据: §10.6
- 内容: 完整的T0-T3分级体系定义、检索策略算法、性能指标

**核心公式:**
- 注意力分配: $\text{Attention}(T0) \gg \text{Attention}(T1) > \text{Attention}(T2) \gg \text{Attention}(T3)$
- 复杂度优化: $O(N) \rightarrow O(1) + O(\log k)$

## 📊 系统熵值指标 ($H_{sys}$)

为了量化系统的有序度，每次加载上下文时必须计算并展示 **归一化系统熵 ($H_{sys}$)**。

### 指标定义

$$H_{sys} = \alpha \cdot \underbrace{\left(\frac{T_{load}}{T_{limit}}\right)}_{\text{认知负载熵}} + \beta \cdot \underbrace{\left(1 - \frac{N_{linked}}{N_{total}}\right)}_{\text{结构离散熵}} + \gamma \cdot \underbrace{\left(\frac{F_{drift}}{F_{total}}\right)}_{\text{版本漂移熵}}$$

### 参数定义

| 参数 | 定义 | 默认值 |
|------|------|--------|
| $T_{load}$ | 当前 Bootloader 上下文 Token 占用 | - |
| $T_{limit}$ | 上下文硬性阈值 | 8000 Tokens |
| $N_{linked}$ | 图谱中拥有有效入度/出度的节点数 | - |
| $N_{total}$ | 总文件节点数 | - |
| $F_{drift}$ | 版本号滞后或被标记为 Deprecated 的文件数 | - |
| $F_{total}$ | 总文件数 | - |

### 权重配置

| 权重 | 值 | 优先级 |
|------|-----|--------|
| $\alpha$ (认知负载) | 0.4 | 性能优先 |
| $\beta$ (结构离散) | 0.3 | 关联优先 |
| $\gamma$ (版本漂移) | 0.3 | 合规优先 |

### 解读标准

| $H_{sys}$ 范围 | 状态 | 行动建议 |
|----------------|------|----------|
| 0.0 - 0.3 | 🟢 优秀 | 保持现状 |
| 0.3 - 0.5 | 🟡 良好 | 关注负载 |
| 0.5 - 0.7 | 🟠 警告 | 优化结构 |
| 0.7 - 1.0 | 🔴 危险 | 立即整理 |

### 仪表盘模板 (activeContext.md)

每次加载上下文时，输出以下"体检报告"：

```markdown
## System Health Report

| 指标 | 值 | 评分 |
|------|-----|------|
| $H_{sys}$ (系统熵) | 0.00 - 1.00 | 🟢/🟡/🟠/🔴 |
| $T_{load}$ (Token占用) | 0 / 8000 | 百分比 |
| $N_{linked}/N_{total}$ (关联度) | 0 / 0 | 百分比 |
| $F_{drift}/F_{total}$ (漂移率) | 0 / 0 | 百分比 |

**健康评估**: [状态描述]
**优化建议**: [具体行动建议]
```

### 使用规则

- ✅ **每次加载上下文前**: 计算并显示 $H_{sys}$
- ✅ **当 $H_{sys} > 0.5$ 时**: 触发优化建议
- ✅ **当 $H_{sys} > 0.7$ 时**: 强制执行熵减操作
- ✅ **版本更新后**: 重新计算所有文件的漂移状态

## 法律体系架构

```
┌─────────────────────────────────────────────────────┐
│                    基本法 (Basic Law)                │ ← §102, §152, §141
│           核心公理: 单一真理源、熵减验证               │
├─────────────────────────────────────────────────────┤
│                   程序法 (Procedural Law)           │ ← §200-§223
│           工作流程: CDD流程、灰度晋升、知识管理        │
├─────────────────────────────────────────────────────┤
│                   技术法 (Technical Law)            │ ← §300-§440
│           技术标准: DS-xxx 实现标准、验证协议          │
└─────────────────────────────────────────────────────┘
```

## 核心公理 (§100-§199)

### §102.3 宪法同步公理
版本变更必须触发全体系同步扫描与强制对齐。

### §114 双存储同构公理
内存状态必须与文件系统状态一致：$S_{runtime} \equiv S_{disk}$

### §141 熵减验证
重构必须满足语义保持性 ($S' = S$) 和熵减验证 ($H' \leq H$)。

### §152 单一真理源公理
`memory_bank` 是可执行规范的单一真理源，不要复制规则，引用它们。

### §171 activeContext单一存储公理
活动上下文必须存储在单一位置。

### §181 类型公理优先
类型定义先于代码实现：$T_{define} \rightarrow T_{implement}$

### §381 安全公理
检查依赖包存在性，使用参数化查询防御注入。

## CDD五状态工作流

```
    ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
    │ State A  │ ──→ │ State B  │ ──→ │ State C  │ ──→ │ State D  │ ──→ │ State E  │
    │ 基准摄入 │     │ 文档规划 │     │ 受控执行 │     │ 三级验证 │     │ 收敛纠错 │
    └──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
         ↓                ↓                ↓                ↓                ↓
    加载T0文档      先文档后代码       原子化写入      验证即循环        迭代/校准
```

### State A: 基准摄入 (Context Ingestion)
读取项目的"可执行规范"（单一真理源）：
- **T0**: `activeContext.md` - 活动上下文
- **T1**: `systemPatterns.md` - ASCII目录树约束
- **T1**: `techContext.md` - 接口签名约束
- **T1**: `behaviorContext.md` - 行为断言
- `.clinerules` - 项目规则 (T1)

### State B: 文档驱动规划 (Documentation First)
**[法定动作 §152]**
- 严禁直接修改代码
- 架构变更 → 先修改 `systemPatterns.md`
- 接口变更 → 先修改 `techContext.md`
- 行为变更 → 先修改 `behaviorContext.md`
- 等待用户批准 (YES) 后继续

### State C: 受控执行 (Safe Implementation)
依据已批准的 Memory Bank 执行：
- 遵循 §381 安全公理
- 检查依赖包是否存在（防幻觉）
- 使用参数化查询（防注入）
- 原子化写入操作

### State D: 三级验证闭环 (Verification Loop)
**[验证即循环 §136]**

| Tier | 验证内容 | 数学公理 |
|------|----------|----------|
| **Tier 1** | 物理文件系统 vs ASCII树 | $S_{fs} \cong S_{doc}$ |
| **Tier 2** | 代码AST签名 vs 接口定义 | $I_{code} \supseteq I_{doc}$ |
| **Tier 3** | 运行时行为 vs 行为断言 | $B_{code} \equiv B_{spec}$ |

### State E: 收敛与纠错 (Convergence)
- 任何验证失败 → 修正代码或文档
- 全部通过 → **与T0文档完全校准** → 完成任务，记录成果

**校准检查清单:**
- [ ] 代码 ↔ `systemPatterns.md` 同构
- [ ] 接口 ↔ `techContext.md` 匹配
- [ ] 行为 ↔ `behaviorContext.md` 一致
- [ ] $H_{sys} \leq 0.5$ (或改善)
- [ ] `activeContext.md` 已更新

## 懒加载协议

遇到具体技术问题，**严禁**凭空生成代码，必须按需加载：

```
1. 检索 → 索引文件 (O(1)查找)
2. 加载 → 读取具体的 DS-xxx 标准文件
3. 执行 → 按照标准实现
4. 释放 → 不再引用时释放上下文（保持T0文档）
```

**高频标准索引：**
- **DS-001**: UTF-8输出配置 [§301]
- **DS-002**: 原子文件写入 [§302]
- **DS-007**: 架构同构性验证 [§352]
- **DS-024**: 自动化架构同步 [§320]
- **DS-039**: 工具调用桥接器 [§438-§440]

## 🤖 外部审计者 (External Auditor)

CDD 引入 **外部审计者 (External Auditor)** 角色，作为独立的AI审计实体，使用深度推理模型进行**T0级别文档审查**。

### ⭐ 核心理念：第三方视角评估

**外部审计的核心价值**：

> "通过第三方视角评估本项目的文档逻辑是否清晰，结构是否明确。"

CDD文档体系虽然由项目团队内部编写，但可能存在以下盲点：
- **逻辑自洽性**: 团队可能默认假设某些逻辑关系，实际可能存在跳跃或矛盾
- **结构清晰度**: 对团队而言 очевидно (显而易见) 的结构，对新成员或外部审计者可能不清晰
- **术语一致性**: 同一术语在不同文档中可能有不同解释
- **完整性检查**: 团队可能遗漏某些必要的文档或条款

**外部审计者**作为独立的AI实体，不带项目先入为主的假设，能够：
1. **客观评估文档结构** - 以"新人"视角审视文档组织
2. **验证逻辑完整性** - 检查论证链条是否完整
3. **发现隐含假设** - 识别团队未明确说明的假设
4. **提供改进建议** - 基于最佳实践给出优化方向

**审计原则**：
- ✅ 第三方视角，无利益关联
- ✅ 评估文档逻辑和结构，不评估代码实现
- ✅ 识别盲点和遗漏
- ✅ 提供建设性改进建议
- ⚠️ 不替代团队决策，仅提供参考意见

### 核心职责定位

**🎯 专注范围**: 仅审查 T0 级别文档，不审查代码

**📋 T0 级别文档清单**:
| 文件 | 路径 | 说明 |
|------|------|------|
| `01_basic_law_index.md` | `00_indices/` | 基本法核心公理 |
| `02_procedural_law_index.md` | `00_indices/` | 程序法工作流索引 |
| `03_technical_law_index.md` | `00_indices/` | 技术法标准索引 |
| `activeContext.md` | `01_active_state/` | 活跃上下文 |
| `KNOWLEDGE_GRAPH.md` | `02_systemaxioms/` | 知识图谱 |

### 外部审计者配置

**配置文件**: `memory_bank/cdd_config.yaml`

```yaml
# CDD 外部审计者配置
external_auditor:
  # 是否启用
  enabled: true
  
  # 模型配置
  model: "deepseek-reasoner"  # 深度推理模型
  
  # API 配置
  api:
    base_url: "https://api.deepseek.com"  # API基础地址
    api_key: "${DEEPSEEK_API_KEY}"        # API密钥 (支持环境变量)
  
  # 审计策略
  audit:
    # 审计范围: 仅T0级别文档
    scope:
      - "t0_documents"  # T0级别文档审查
    
    # 触发时机: T0文档变更时
    trigger_on:
      - "t0_document_change"  # T0文档变更时触发 ⭐
      
    # 审计深度
    depth: "comprehensive"  # shallow/comprehensive/deep
      
    # 审计报告格式
    report_format: "markdown"
    
    # 通知设置
    notifications:
      # 抄送用户
      cc_to_user: true  # ⭐ 审计报告同步抄送给用户
      
      # 通知方式 (Discord/Slack等)
      channels:
        - "discord"  # 通过Discord发送审计报告
```

### 外部审计者职责

| 职责 | 触发时机 | 输出 |
|------|----------|------|
| **T0文档合规性审查** | T0文档变更时 | 合规性审计报告 |
| **宪法约束验证** | 修改后立即触发 | 条款引用检查 |
| **文档一致性检查** | 变更时 | 一致性验证报告 |
| **架构完整性评估** | 重大变更后 | 完整性评估报告 |

### 外部审计者工作流

```
T0文档变更检测
        │
        ↓
┌───────────────────┐
│  变更类型判断      │
│  (新增/修改/删除)  │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│  外部审计者触发    │ ← deepseek-reasoner
└─────────┬─────────┘
          ↓
┌───────────────────┐
│  构建审计请求      │ ← 记录API调用信息
└─────────┬─────────┘
          ↓
┌───────────────────┐
│  T0文档审查        │ ← deepseek-reasoner API调用
│  - 基本法检查      │   记录: 端点/模型/请求ID/耗时/Token
│  - 程序法检查      │
│  - 技术法检查      │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│  生成审计报告      │ ← 包含完整API调用信息
│  - API调用详情     │
│  - 审查结果       │
│  - 风险评估       │
│  - 修复建议       │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│  抄送用户          │ ⭐
│  (Discord消息)    │
│  - 包含API摘要    │
└───────────────────┘
```

### ⭐ 外部审计API调用信息记录标准 (v2.0)

**从2026-02-01起，所有审计报告必须包含完整的API调用信息**：

```markdown
## API调用详情

### 调用 #1: 审计请求
| 字段 | 值 |
|------|-----|
| **端点** | `https://api.deepseek.com/chat/completions` |
| **模型** | `deepseek-reasoner` |
| **请求ID** | `{REQUEST_ID}` |
| **发送时间** | `{SEND_TIMESTAMP}` |
| **收到时间** | `{RECV_TIMESTAMP}` |
| **耗时** | `{LATENCY}ms` |
| **Token使用** | 输入: {IN_TOKENS} / 输出: {OUT_TOKENS} / 总计: {TOTAL_TOKENS} |

**请求参数**:
```json
{
  "model": "deepseek-reasoner",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "temperature": 0.2,
  "max_tokens": 4096
}
```

**响应状态**: {STATUS_CODE} OK
```

### 外部审计者系统提示

```
你是一位资深CDD合规性审计专家，专注于T0级别文档的宪法合规审查。

⚠️ **重要：项目背景说明**
在审查前，必须首先确认并理解被审计项目的定位和领域。不同的项目类型（量化分析、Web3、传统软件等）有不同的合规要求和审计重点。

**审计职责：**
1. 审查T0级别文档的完整性和一致性
2. 验证文档是否符合宪法约束（§102.3, §114, §141, §152等）
3. 检查文档间的引用关系是否正确
4. 识别潜在的逻辑矛盾或遗漏
5. 生成详细的审计报告

**审计原则：**
- ⭐ **先确认项目背景**：审查开始前，必须明确项目的领域定位和技术栈
- 仅审查T0级别文档，不审查代码
- 引用具体条款（§xxx）说明问题
- 量化风险等级（低/中/高/严重）
- 提供具体的修复建议
```

### T0文档审查清单

| 审查维度 | 检查内容 | 宪法依据 |
|----------|----------|----------|
| **完整性** | 5个T0文档是否齐全 | §152 单一真理源 |
| **一致性** | 文档间引用是否一致 | §114 双存储同构 |
| **合规性** | 是否符合宪法条款 | §102.3 宪法同步 |
| **时效性** | 版本是否最新 | §102.3 版本同步 |
| **熵值** | $H_{sys}$ 是否在合理范围 | §141 熵减验证 |

### 审计报告模板 (v2.0 - 含API调用信息)

**报告文件名格式**: `report_by_deepseek-reasoner_YYYY-MM-DD_HH-MM-SS.md`

**报告保存路径**: `research_report/`

```markdown
# T0文档审计报告 (T0 Document Audit Report)

## 审计元数据
- **审计时间**: {timestamp}
- **触发原因**: {trigger}
- **审查范围**: {scope}
- **审计模型**: deepseek-reasoner

## API调用详情

### 调用 #1: 审计请求
| 字段 | 值 |
|------|-----|
| **端点** | `https://api.deepseek.com/chat/completions` |
| **模型** | `deepseek-reasoner` |
| **请求ID** | `{REQUEST_ID}` |
| **发送时间** | `{SEND_TIME}` |
| **收到时间** | `{RECV_TIME}` |
| **耗时** | `{LATENCY}ms` |
| **Token使用** | 输入: {IN_TOKENS} / 输出: {OUT_TOKENS} / 总计: {TOTAL_TOKENS} |

**请求参数**:
```json
{
  "model": "deepseek-reasoner",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "temperature": 0.2,
  "max_tokens": 4096
}
```

**响应状态**: {STATUS_CODE} OK

---

## 审查摘要

{summary}

## 通过项列表

- ✅ {pass_1}
- ✅ {pass_2}
- ✅ ...

## 警告项列表

- ⚠️ {warning_1}
- ⚠️ {warning_2}
- ⚠️ ...

## 问题项列表

- ❌ {issue_1}
- ❌ {issue_2}
- ❌ ...

## 风险评估

| 维度 | 风险等级 |
|------|----------|
| 完整性风险 | {risk_completeness} |
| 一致性风险 | {risk_consistency} |
| 合规性风险 | {risk_compliance} |
| 时效性风险 | {risk_timeliness} |
| 熵值风险 | {risk_entropy} |

**整体风险评估**: {overall_risk}

## 合规性检查

| 检查项 | 状态 | 宪法依据 |
|--------|------|----------|
| 完整性检查 | ✅/⚠️/❌ | §152 单一真理源 |
| 一致性检查 | ✅/⚠️/❌ | §114 双存储同构 |
| 合规性检查 | ✅/⚠️/❌ | §102.3 宪法同步 |
| 时效性检查 | ✅/⚠️/❌ | §102.3 版本同步 |
| 熵值检查 | ✅/⚠️/❌ | §141 熵减验证 |

## 改进建议

1. {suggestion_1}
2. {suggestion_2}
3. {suggestion_3}

## 下一步行动

- [ ] {next_action_1}
- [ ] {next_action_2}
- [ ] {next_action_3}

---

**审计者**: External Auditor (deepseek-reasoner)
**生成时间**: {timestamp}
```

### 外部审计者API调用示例 (v2.0 - 含完整记录)

```python
import requests
import time
from datetime import datetime
import json

class ExternalAuditor:
    """外部审计者 - T0文档审计 (v2.0)"""
    
    def __init__(self, api_key: str, model: str = "deepseek-reasoner"):
        self.api_url = "https://api.deepseek.com/chat/completions"
        self.api_key = api_key
        self.model = model
    
    def audit_t0_documents(self, changed_files: list, all_t0_docs: dict) -> dict:
        """审计T0级别文档 - 记录完整API调用信息"""
        
        # 构建审查上下文
        context = self._build_context(changed_files, all_t0_docs)
        
        # 记录API调用前的状态
        send_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        start_time = time.time()
        
        # 调用深度推理模型
        response = requests.post(
            self.api_url,
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": context}
                ],
                "temperature": 0.2,
                "max_tokens": 4096
            },
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=180
        )
        
        # 记录API响应信息
        recv_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        latency_ms = int((time.time() - start_time) * 1000)
        
        result = response.json()
        request_id = result.get("id", "N/A")
        usage = result.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        
        # 提取审计内容
        audit_content = result["choices"][0]["message"]["content"]
        
        # 构建API调用信息
        api_info = {
            "endpoint": self.api_url,
            "model": self.model,
            "request_id": request_id,
            "send_time": send_time,
            "recv_time": recv_time,
            "latency_ms": latency_ms,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "status_code": response.status_code
        }
        
        # 生成审计报告
        report = self._generate_report(api_info, audit_content)
        
        return {
            "report": report,
            "api_info": api_info
        }
    
    def _build_context(self, changed_files: list, all_t0_docs: dict) -> str:
        """构建审查上下文"""
        # ... (同前)
        pass
    
    def _generate_report(self, api_info: dict, audit_content: str) -> str:
        """生成审计报告 (v2.0)"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        report = f"""# T0文档审计报告

## 审计元数据
- **审计时间**: {timestamp}
- **审查范围**: T0文档体系
- **审计模型**: {api_info['model']}

## API调用详情

### 调用 #1: 审计请求
| 字段 | 值 |
|------|-----|
| **端点** | `{api_info['endpoint']}` |
| **模型** | `{api_info['model']}` |
| **请求ID** | `{api_info['request_id']}` |
| **发送时间** | `{api_info['send_time']}` |
| **收到时间** | `{api_info['recv_time']}` |
| **耗时** | `{api_info['latency_ms']}ms` |
| **Token使用** | 输入: {api_info['input_tokens']} / 输出: {api_info['output_tokens']} |

**响应状态**: {api_info['status_code']} OK

---

{audit_content}

---
**审计者**: External Auditor ({api_info['model']})
**生成时间**: {api_info['send_time']}
"""
        return report
```审计以下T0级别文档变更：

变更文件: {changed_files}

完整T0文档内容:
{for path, content in all_t0_docs.items()}
---{path}---
{content}
---

请执行完整的合规性审查。
"""}
            ],
            temperature=0.2,
        )
        
        audit_report = response.choices[0].message.content
        
        # 保存审计报告 ⭐
        report_path = self._save_audit_report(audit_report, changed_files)
        
        return {
            "audit_report": audit_report,
            "report_path": report_path,  # ⭐ 报告保存路径
            "changed_files": changed_files,
            "cc_to_user": self.cc_to_user,  # ⭐ 标记需要抄送
            "conclusion": "通过" if "通过" in audit_report else "需修正"
        }
    
    def _save_audit_report(self, content: str, changed_files: list) -> str:
        """保存审计报告为MD文件"""
        from datetime import datetime
        import os
        
        # 报告保存目录
        report_dir = "research_report"
        os.makedirs(report_dir, exist_ok=True)
        
        # 生成报告文件名: report_by_deepseek-reasoner_YYYY-MM-DD_HH-MM-SS.md
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"report_by_deepseek-reasoner_{timestamp}.md"
        report_path = os.path.join(report_dir, filename)
        
        # 报告内容
        report_content = f"# T0文档审计报告\n\n## 审计元数据\n- **审计时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n- **变更文件**: {', '.join(changed_files)}\n- **审计模型**: deepseek-reasoner\n\n---\n\n{content}\n\n---\n**审计者**: External Auditor"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_path
    
    def _build_context(self, changed_files: list, all_t0_docs: dict) -> str:
        """构建审查上下文"""
        return f"""
审查以下T0文档变更：
变更文件: {', '.join(changed_files)}

请检查：
1. 变更是否符合宪法条款
2. 文档间引用是否一致
3. 熵值是否在合理范围
4. 版本是否同步
"""
```

### 外部审计者集成

在 T0 文档变更时触发：

```python
# 检测到T0文档变更
def on_t0_document_change(changed_files: list):
    # 1. 加载所有T0文档
    all_t0_docs = load_all_t0_documents()
    
    # 2. 触发外部审计
    auditor = ExternalAuditor(config['external_auditor'])
    result = auditor.audit_t0_documents(changed_files, all_t0_docs)
    
    # 3. 获取审计结果
    audit_report = result['audit_report']
    report_path = result['report_path']  # ⭐ 报告文件路径
    
    # 4. 发送附件到 Discord ⭐
    if result['cc_to_user']:
        send_attachment_to_channel(
            channel="discord",
            file_path=report_path,  # ⭐ 附件: 审计报告MD文件
            caption=f"📋 **T0文档审计报告**\n\n"
                   f"**审计结论**: {result['conclusion']}\n"
                   f"**变更文件**: {', '.join(changed_files)}"
        )
    
    # 返回审计结果
    return result

### 标准流程: T0文档变更与外部审计 ⭐

**当T0级别文档发生变更时：**

```
T0文档变更
    ↓
外部审计者触发 (deepseek-reasoner)
    ↓
T0文档合规性审查
    ↓
生成审计报告
    ├─ 保存到: research_report/report_by_deepseek-reasoner_YYYY-MM-DD_HH-MM-SS.md
    ↓
⭐ 发送附件到 Discord/其他频道
    ├─ 附件: 审计报告MD文件
    ├─ 消息: 审计摘要 + 报告路径
    ↓
确认/修正
```

**完整工作流代码：**

```python
from datetime import datetime
import os

def on_t0_document_change(changed_files: list):
    """T0文档变更处理完整流程"""
    
    # 1. 加载所有T0文档
    all_t0_docs = load_all_t0_documents()
    
    # 2. 触发外部审计
    auditor = ExternalAuditor(config['external_auditor'])
    result = auditor.audit_t0_documents(changed_files, all_t0_docs)
    
    # 3. 获取审计报告和路径
    audit_report = result['audit_report']
    report_path = result['report_path']  # research_report/report_by_xxx.md
    
    # 4. 发送附件到 Discord ⭐
    if result['cc_to_user']:
        send_attachment_to_channel(
            channel="discord",
            file_path=report_path,  # ⭐ 附件路径
            caption=f"📋 **T0文档审计报告**\n\n"
                   f"**审计结论**: {result['conclusion']}\n"
                   f"**变更文件**: {', '.join(changed_files)}"
        )
    
    return result
```

**Discord附件发送示例：**

```python
def send_attachment_to_channel(channel: str, file_path: str, caption: str = ""):
    """
    发送文件附件到指定频道
    
    Args:
        channel: 频道标识 (discord/slack等)
        file_path: 附件文件路径
        caption: 附件说明文字
    """
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 发送消息 (带附件)
    send_message(
        channel=channel,
        message=caption,
        attachment={
            "filename": os.path.basename(file_path),
            "content": content
        }
    )
```

**流程说明：**
1. **变更检测** - 系统检测T0文档变更
2. **审计触发** - 调用 deepseek-reasoner 审查
3. **报告生成** - 保存为 `report_by_deepseek-reasoner_时间戳.md`
4. **附件发送** - 将报告作为附件发送到 Discord
5. **用户确认** - 用户查看报告并确认/修正

## 性能指标

- **上下文占用**: <8K tokens (T0文档 + 按需加载)
- **检索速度**: $O(1)$ 索引查找
- **熵减目标**: $\Delta H > 0$
- **架构同构性**: 100%
- **引用完整性**: 100%
- **校准完成率**: 100% (结项前)

## 使用方式

1. **项目初始化**: 
   - 创建5个T0文档到 `memory_bank/`
   - ⭐ **创建项目README.md** (项目背景文档，非T0级别)
2. **启动开发**: 加载T0文档，计算 $H_{sys}$
3. **制定计划**: 在T0文档中定义变更
4. **执行开发**: 按计划修改代码
5. **三级验证**: 运行Tier 1/2/3验证
6. **完全校准**: 代码 ↔ T0文档完全一致
7. **结项**: 更新 `activeContext.md`，记录成果

## ⚠️ 注意事项

### 前置条件
- ✅ 必须在项目根目录创建 `memory_bank/` 文件夹
- ⭐ **必须创建项目README.md** (项目背景文档，来自 templates/readme_template.md)
- ✅ 必须创建5个T0文档（第一时间）
- ✅ 必须保持T0文档在上下文中（全程）
- ✅ 必须先文档后代码（计划阶段）
- ✅ 必须完全校准才能结项

### 索引加载规范
- ✅ **每一步操作前**：必须确认T0文档在上下文中
- ✅ 始终加载5个T0文档文件
- ✅ 遇到具体问题 → 索引查找 O(1)
- ✅ 按需加载 DS-xxx/WF-xxx 文件
- ✅ 执行完成后**立即释放**具体文件引用（保持T0文档）
- ❌ **禁止**加载完整法典文件到内存
- ❌ **禁止**在上下文中保留超过5个T0文档
- ❌ **禁止**绕过T0文档直接引用具体条款
- ❌ **禁止**在未加载T0文档的情况下执行任何CDD操作

### 知识图谱规范
- ✅ 非索引文档以知识图谱形式组织
- ✅ 使用 `KNOWLEDGE_GRAPH.md` 作为图谱入口
- ✅ 遵循节点关系导航 (Implements/Related_to/Required_by)
- ✅ 最大跳数限制: 3 跳
- ✅ 仅按需读取节点内容（浏览关系时只读索引）

### 操作规范
- ✅ 信任索引，优先使用索引查找
- ✅ 图谱导航，复杂问题使用知识图谱推理
- ✅ 原子操作，所有修改遵循 §125 数据完整性公理
- ❌ 禁止手动加载完整知识库到内存
- ❌ 禁止凭空捏造 DS 标准
- ❌ 禁止绕过图谱推理进行线性思维决策
- ❌ **严禁**在 memory bank 未建立时执行 CDD 流程
- ❌ **严禁**未完成校准就结项

### 熵值监控规范
- ✅ **每次加载上下文时**: 计算 $H_{sys}$ 并显示仪表盘
- ✅ **在 activeContext.md 中记录**: 当前 $H_{sys}$ 值和历史趋势
- ✅ **当 $H_{sys} > 0.5$**: 在输出中显示"🟠 警告：系统熵值偏高"
- ✅ **当 $H_{sys} > 0.7$**: 在输出中显示"🔴 危险：立即执行熵减操作"
- ✅ **版本更新后**: 扫描所有文件，更新 $F_{drift}$ 统计
- ✅ **结项前**: 确认 $H_{sys}$ 符合预期（或改善）

## 🚀 快速开始

### 步骤1: 项目初始化
```bash
# 创建 Memory Bank
mkdir -p memory_bank/00_indices
mkdir -p memory_bank/01_active_state
mkdir -p memory_bank/02_systemaxioms
mkdir -p memory_bank/03_protocols/workflows
mkdir -p memory_bank/03_protocols/standards

# 复制模板
cp templates/*_index.md memory_bank/00_indices/
cp templates/activeContext.md memory_bank/01_active_state/
cp templates/KNOWLEDGE_GRAPH.md memory_bank/02_systemaxioms/

# 创建项目 README.md
cp templates/readme_template.md README.md
```

### 步骤2: 启动 CDD
1. 加载 README.md (项目背景)
2. 加载全部 5 个 T0 文档
3. 进入 State A (基准摄入)

### 步骤3: 开发循环
```
State A → State B → State C → State D → State E
   ↑__________________________________|
            (继续开发)
```

### 步骤4: 外部审计 (T0变更时)
```
T0 文档变更 → 触发审计 → deepseek-reasoner → 报告 → Discord → 用户确认
```

## ✅ 闭环验证清单

每次开发任务结束时，必须确认以下全部通过：

| 检查项 | 验证标准 | 状态 |
|--------|----------|------|
| **代码 ↔ 架构同构** | `代码结构` ≅ `systemPatterns.md` | ☐ |
| **接口 ↔ 签名匹配** | `接口定义` ⊇ `techContext.md` | ☐ |
| **行为 ↔ 断言一致** | `实际行为` ≡ `behaviorContext.md` | ☐ |
| **T0 文档同步** | 全部 5 个 T0 文档已更新 | ☐ |
| **熵值达标** | $H_{sys} \leq 0.3$ | ☐ |
| **无悬空引用** | 所有 DS/WF 标准已释放 | ☐ |
| **外部审计通过** | (如有T0变更) 审计报告结论为"通过" | ☐ |

**全部打勾后方可结项。**

---

*CDD v1.0 - 逻辑清晰，架构闭环。*
