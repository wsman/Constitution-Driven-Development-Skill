# DS-007: 上下文管理标准 (Context Management Standard)

**ID**: DS-007
**类型**: T2 (Standard)
**版本**: v1.0.0
**用途**: 定义 LLM 上下文窗口的加载、卸载与压缩策略

---

## 1. 核心策略 (The Packing Strategy)

为了在有限的 Context Window (通常 8k-128k) 内保持高信噪比，系统根据 **当前状态 (State)** 动态加载文档。

**基本公式**:

$$	ext{Context}_{loaded} = 	ext{T0 Kernel} + 	ext{State Mode}(T1 + T2) + 	ext{Working Set}$$

### 1.1 T0 Kernel (常驻)

* `activeContext.md` (状态与仪表盘)
* `KNOWLEDGE_GRAPH.md` (导航图谱)
* `SKILL.md` (核心指令集 - System Prompt)

---

## 2. 模式定义 (Modes)

### Mode A: Planning (State A & B)

* **Focus**: 需求分析与架构设计
* **Load**:
* T1: `systemPatterns.md` (架构约束)
* T1: `techContext.md` (接口约束)
* Input: `README.md` (项目背景)
* Input: `Clarified Requirements`

* **Token Budget**: 40% T0/T1, 40% Input/Analysis, 20% Output

### Mode B: Coding (State C)

* **Focus**: 代码实现
* **Load**:
* Spec: `DS-050 (Current Feature)`
* Plan: `DS-051 (Current Plan)`
* Task: `DS-052 (Current Atomic Task)`
* Code: `Current Edited Files` (Top 3 most relevant)

* **Unload**: 卸载 `systemPatterns.md` 的全文，仅保留 T0 中的索引引用。
* **Token Budget**: 20% T0, 30% Specs, 50% Code

### Mode C: Verifying (State D)

* **Focus**: 测试与验证
* **Load**:
* T1: `behaviorContext.md` (行为公理)
* Code: `Test Files`
* Logs: `Error Logs / Test Output`

* **Token Budget**: 20% T0, 30% Axioms, 50% Logs/Code

---

## 3. 卸载与压缩 (Eviction & Compression)

1. **LRU 策略**: 当 Token 使用率 > 80% 时，优先卸载最久未被引用的 T2 文档。
2. **摘要机制**: 对于超长文档（如长代码文件），仅加载 `Interface/Class Definition` 而非完整实现，除非是当前编辑对象。
3. **One-shot**: `README.md` 等背景文档在初始化读取后，提取关键信息至 `activeContext.md`，随后卸载。

---

**引用标准**: DS-007 v1.0.0
**最后更新**: {{timestamp}}
