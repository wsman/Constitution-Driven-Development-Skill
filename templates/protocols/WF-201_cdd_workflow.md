# WF-201: CDD 核心工作流 (Constitution-Driven Development Workflow)

**版本**: v1.4.0
**核心思想**: 规范驱动 (Spec-Driven) + 熵减治理 (Entropy-Control) + 质量闭环 (Quality-Loop)

---

## 状态机视图 (State Machine)

### State A: 基准摄入 (Baseline Intake)

* **Goal**: 加载宪法与项目上下文
* **Action**: Bootloader Sequence
* **Context Mode**: `Planning`

### State B: 规范驱动规划 (Spec-Driven Planning)

* **Goal**: 将模糊需求转化为可执行、已校验的原子任务
* **Flow**:
1. **Clarify**: 执行 `WF-CLARIFY`，消除歧义。
   * *Output*: `Clarified Requirements`

2. **Specify**: 基于清晰需求，生成 `DS-050 (Feature Spec)`。
   * *Check*: 符合 T1 架构约束？

3. **Plan**: 基于 Spec，生成 `DS-051 (Impl Plan)`。

4. **Tasking**: 将 Plan 拆解为 `DS-052 (Atomic Tasks)`。

5. **Analyze**: 执行 `WF-ANALYZE` 规划一致性校验。
   * *Purpose*: 检测Spec/Plan/Tasks之间的逻辑矛盾和遗漏
   * *Output*: `analysis_report.md`
   * *Gate*: 必须通过 (无CRITICAL问题)

6. **Checklist Generation**: 生成 `DS-053 (Quality Checklist)`。
   * *Purpose*: 需求质量验证 ("需求的单元测试")
   * *Output*: `memory_bank/checklists/{domain}.md`

* **Exit Criteria**: 
- [ ] 用户批准 Spec & Plan
- [ ] Analyze通过 (无CRITICAL问题)
- [ ] Checklist生成完成

### State C: 受控执行 (Controlled Execution)

* **Goal**: 原子化编码与环境一致性
* **Flow**:
1. **Environment Hardening**: 执行 `DS-054` 环境硬化检查
   * 检查 `.gitignore` / `.dockerignore`
   * 验证 Lint 工具配置
2. **Execute Tasks**: 逐个执行 `DS-052` 中的任务。

* **Context Mode**: `Coding`
* **Rule**: 禁止在一个 Task 中修改 Plan 未定义的范围。

### State D: 三级验证 (Tiered Verification)

* **Goal**: 数学与行为验证
* **Flow**:
* **Tier 1 (结构验证)**: 检查文件结构是否符合 `system_patterns.md` 定义的 ASCII 树。 (`tree` check)
* **Tier 2 (签名验证)**: 检查代码接口是否覆盖 `tech_context.md` 定义的签名。 (Interface check)
* **Tier 3 (行为验证)**: 运行测试用例，验证是否符合 `behavior_context.md` 断言。 (Test check)

* **Context Mode**: `Verifying`

### State E: 收敛与审计 (Convergence & Audit)

* **Goal**: 熵值校准
* **Action**:
1. 运行 `measure_entropy.py`。
2. 触发外部审计 (若配置启用)。
3. 更新 `active_context.md` 的仪表盘。
4. **Checklist验收**: 逐项勾选 `DS-053` 检查单。

* **Transition**: 若 $H_{sys} \leq 0.3$，结束；否则回退 State C 修复。

---

## 数据流转换协议 (Data Transformation Protocol)

1. **User -> Clarify**: 自然语言 -> 结构化 Q&A
2. **Clarify -> DS-050**: Q&A -> User Stories & AC
3. **DS-050 -> DS-051**: Stories -> Engineering Steps
4. **DS-051 -> DS-052**: Step -> File-level Actions
5. **DS-052 -> WF-ANALYZE**: Tasks -> 一致性报告
6. **WF-ANALYZE -> DS-053**: 分析结果 -> 质量检查单
7. **DS-054 -> Execute**: 环境检查 -> 任务执行

---

## 组件引用

| 组件 | 版本 | 用途 |
|------|------|------|
| WF-CLARIFY | v1.4.0 | 需求澄清 |
| DS-050 | v1.4.0 | 功能规格 |
| DS-051 | v1.4.0 | 实施计划 |
| DS-052 | v1.4.0 | 原子任务 |
| WF-ANALYZE | v1.4.0 | 规划一致性校验 |
| DS-053 | v1.4.0 | 质量检查单 |
| DS-054 | v1.4.0 | 环境硬化 |

---

**引用标准**: WF-201 v1.4.0
**最后更新**: {{TIMESTAMP}}
