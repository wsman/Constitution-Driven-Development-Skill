# WF-201: CDD 核心工作流 (Constitution-Driven Development Workflow)

**版本**: v1.3.0
**核心思想**: 规范驱动 (Spec-Driven) + 熵减治理 (Entropy-Control)

---

## 状态机视图 (State Machine)

### State A: 基准摄入 (Baseline Intake)

* **Goal**: 加载宪法与项目上下文
* **Action**: Bootloader Sequence
* **Context Mode**: `Planning`

### State B: 规范驱动规划 (Spec-Driven Planning)

* **Goal**: 将模糊需求转化为可执行的原子任务
* **Flow**:
1. **Clarify**: 执行 `WF-CLARIFY`，消除歧义。
* *Output*: `Clarified Requirements`

2. **Specify**: 基于清晰需求，生成 `DS-050 (Feature Spec)`。
* *Check*: 符合 T1 架构约束？

3. **Plan**: 基于 Spec，生成 `DS-051 (Impl Plan)`。
4. **Tasking**: 将 Plan 拆解为 `DS-052 (Atomic Tasks)`。

* **Exit Criteria**: 用户批准 Spec & Plan。

### State C: 受控执行 (Controlled Execution)

* **Goal**: 原子化编码
* **Action**: 逐个执行 `DS-052` 中的任务。
* **Context Mode**: `Coding`
* **Rule**: 禁止在一个 Task 中修改 Plan 未定义的范围。

### State D: 三级验证 (Tiered Verification)

* **Goal**: 数学与行为验证
* **Flow**:
* Tier 1: 结构验证 (`tree` check vs `systemPatterns`)
* Tier 2: 签名验证 (Interface check vs `techContext`)
* Tier 3: 行为验证 (Test check vs `behaviorContext`)

* **Context Mode**: `Verifying`

### State E: 收敛与审计 (Convergence & Audit)

* **Goal**: 熵值校准
* **Action**:
1. 运行 `measure_entropy.py`。
2. 触发外部审计 (若配置启用)。
3. 更新 `activeContext.md` 的仪表盘。

* **Transition**: 若 $H_{sys} \leq 0.3$，结束；否则回退 State C 修复。

---

## 数据流转换协议 (Data Transformation Protocol)

1. **User -> Clarify**: 自然语言 -> 结构化 Q&A
2. **Clarify -> DS-050**: Q&A -> User Stories & AC
3. **DS-050 -> DS-051**: Stories -> Engineering Steps
4. **DS-051 -> DS-052**: Step -> File-level Actions (Edit/Test)

---

**引用标准**: WF-201 v1.3.0
**最后更新**: 2026-02-01
