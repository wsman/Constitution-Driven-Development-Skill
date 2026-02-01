# WF-201: CDD 核心工作流 (Constitution-Driven Development Workflow)

**版本**: v1.4.0  
**核心思想**: 规范驱动 (Spec-Driven) + 熵减治理 (Entropy-Control) + 质量门禁 (Quality Gates)

---

## 状态机视图 (State Machine)

### State A: 基准摄入 (Baseline Intake)

* **Goal**: 加载宪法与项目上下文
* **Action**: Bootloader Sequence
* **Context Mode**: `Planning`

### State B: 规范驱动规划 (Spec-Driven Planning) [v1.4.0增强]

* **Goal**: 将模糊需求转化为可执行的原子任务
* **Flow**:
1. **Clarify**: 执行 `WF-CLARIFY`，消除歧义。
   * *Output*: `Clarified Requirements`

2. **Specify**: 基于清晰需求，生成 `DS-050 (Feature Spec)`。
   * *Check*: 符合 T1 架构约束？

3. **Plan**: 基于 Spec，生成 `DS-051 (Impl Plan)`。

4. **Tasking**: 将 Plan 拆解为 `DS-052 (Atomic Tasks)`。

5. **Analyze [NEW]**: 执行 `WF-ANALYZE` 规划一致性校验。
   * *Purpose*: 检测Spec/Plan/Tasks之间的逻辑矛盾和遗漏
   * *Output*: `analysis_report.md`
   * *Gate*: 必须通过 (无CRITICAL问题)

6. **Checklist Generation [NEW]**: 生成 `DS-053 (Quality Checklist)`。
   * *Purpose*: 需求质量验证 ("需求的单元测试")
   * *Output*: `memory_bank/checklists/{domain}.md`

* **Exit Criteria**: 
- [ ] 用户批准 Spec & Plan
- [ ] Analyze通过 (无CRITICAL问题)
- [ ] Checklist生成完成

### State C: 受控执行 (Controlled Execution) [v1.4.0增强]

* **Goal**: 原子化编码
* **Flow**:
1. **Environment Hardening [NEW]**: 执行 `DS-054` 环境硬化检查
   * 检查 `.gitignore` / `.dockerignore`
   * 验证 Lint 工具配置
2. **Execute Tasks**: 逐个执行 `DS-052` 中的任务。

* **Context Mode**: `Coding`
* **Rule**: 禁止在一个 Task 中修改 Plan 未定义的范围。

### State D: 三级验证 (Tiered Verification) [v1.4.0增强]

* **Goal**: 数学与行为验证，确保代码实现符合T1公理约束
* **Context Mode**: `Verifying`

* **Flow**:
1. **Tier 1: 结构验证 (Structure Verification)**
   - **检查点**: 代码目录结构 vs `systemPatterns.md` 定义
   - **验证**: $S_{fs} \cong S_{doc}$ (文件系统 ≅ 文档定义)
   - **工具**: `tree` 命令对比 ASCII 目录树
   - **失败处理**: 回退 State C 修复架构偏离

2. **Tier 2: 签名验证 (Signature Verification)**
   - **检查点**: 接口实现 vs `techContext.md` 定义
   - **验证**: $I_{code} \supseteq I_{doc}$ (代码接口 ⊇ 文档接口)
   - **工具**: 函数签名、API端点、类型签名对比
   - **失败处理**: 回退 State C 补充接口实现

3. **Tier 3: 行为验证 (Behavior Verification)**
   - **检查点**: 测试用例 vs `behaviorContext.md` 断言
   - **验证**: $B_{code} \equiv B_{spec}$ (代码行为 ≡ 规范行为)
   - **工具**: 单元测试/集成测试覆盖断言
   - **失败处理**: 回退 State C 修复行为偏离

* **Exit Criteria**:
- [ ] Tier 1: 目录结构 100% 匹配
- [ ] Tier 2: 所有定义的接口已实现
- [ ] Tier 3: 关键行为测试通过率 ≥ 90%

### State E: 收敛与审计 (Convergence & Audit)

* **Goal**: 熵值校准
* **Action**:
1. 运行 `measure_entropy.py`。
2. 触发外部审计 (若配置启用)。
3. 更新 `activeContext.md` 的仪表盘。
4. **Checklist验收**: 逐项勾选 `DS-053` 检查单。

* **Transition**: 若 $H_{sys} \leq 0.3$，结束；否则回退 State C 修复。

---

## v1.4.0 新增组件

### 质量门禁 (Quality Gates)

| Gate | 位置 | 检查内容 | 失败处理 |
|------|------|----------|----------|
| **WF-ANALYZE** | State B → C | Spec/Plan/Tasks一致性 | 阻断进入State C |
| **DS-053** | State B输出 | 需求质量检查单 | State E验收 |
| **DS-054** | State C入口 | 环境配置硬化 | 阻断执行任务 |

### 数据流转换协议 (Data Transformation Protocol)

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
| WF-CLARIFY | v1.3.2 | 需求澄清 |
| DS-050 | v1.3.2 | 功能规格 |
| DS-051 | v1.3.2 | 实施计划 |
| DS-052 | v1.3.2 | 原子任务 |
| **WF-ANALYZE** | **v1.3.2** | **规划一致性校验** |
| **DS-053** | **v1.3.2** | **质量检查单** |
| **DS-054** | **v1.4.0** | **环境硬化** |

---

**引用标准**: WF-201 v1.4.0  
**最后更新**: {{TIMESTAMP}}
