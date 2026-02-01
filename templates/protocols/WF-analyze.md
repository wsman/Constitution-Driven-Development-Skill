# WF-ANALYZE: 规划一致性校验工作流

**版本**: v1.3.2  
**协议类型**: T2-工作流协议  
**触发时机**: State B (DS-052 Tasks生成后) → State C (执行前)  
**执行模式**: 只读分析 (Read-Only Analysis)

---

## 协议概述

**目的**: 在进入State C执行阶段前，自动检测DS-050(Spec)、DS-051(Plan)、DS-052(Tasks)之间的逻辑矛盾、遗漏和不一致。

**核心原则**: 
- **只读模式**: 不修改任何文件，仅输出分析报告
- **宪法优先**: 违反T1约束的条目自动标记为CRITICAL
- **Token效率**: 限制50项发现，聚合溢出

---

## 执行步骤

### Step 1: 加载上下文

从项目Memory Bank加载以下文档：

| 文档 | 路径 | 用途 |
|------|------|------|
| **DS-050** | `memory_bank/standards/DS-050_*.md` | 功能/非功能需求 |
| **DS-051** | `memory_bank/standards/DS-051_*.md` | 架构设计、技术栈 |
| **DS-052** | `memory_bank/standards/DS-052_*.md` | 原子任务列表 |
| **T1公理** | `memory_bank/axioms/system_patterns.md` | 架构约束验证 |
| **T1公理** | `memory_bank/axioms/tech_context.md` | 接口签名验证 |

### Step 2: 构建语义模型

创建内部表示（不出现在输出中）：

```
Requirements Inventory:
  - 需求键 (slug): 功能描述
  - 来源: DS-050 §X.Y
  
Task Coverage Matrix:
  - 任务ID → 需求键映射
  - 未覆盖需求检测
  
Constitution Rules:
  - T1约束检查清单
  - MUST/SHOULD语句提取
```

### Step 3: 检测分析 (Detection Passes)

#### A. 重复检测 (Duplication)
- 识别相似需求
- 标记需合并的低质量表述

#### B. 模糊检测 (Ambiguity)
- 标记缺少量化标准的形容词
- 标记未解决占位符 (TODO, ???, TKTK)

#### C. 欠规范检测 (Underspecification)
- 缺少宾语或可测量结果的需求
- User Story缺少验收标准对齐
- 任务引用了Spec/Plan中未定义的文件

#### D. 宪法对齐 (Constitution Alignment)
- 任何违反MUST原则的需求/计划元素
- 缺少T1强制的章节

#### E. 覆盖缺口 (Coverage Gaps)
- 零任务覆盖的需求
- 无需求映射的任务
- NFR未反映在任务中

#### F. 不一致检测 (Inconsistency)
- 术语漂移 (同一概念不同命名)
- 数据实体在Plan有但Spec无
- 任务排序矛盾

### Step 4: 严重性分配

| 级别 | 标准 |
|------|------|
| **CRITICAL** | 违反宪法MUST、核心工件缺失、零覆盖需求 |
| **HIGH** | 重复/冲突需求、模糊安全/性能属性、不可测试的验收标准 |
| **MEDIUM** | 术语漂移、NFR任务覆盖缺失、边界情况欠规范 |
| **LOW** | 样式改进建议、无执行影响的冗余 |

### Step 5: 生成分析报告

输出结构化Markdown报告（无文件写入）：

```markdown
## 规划一致性分析报告

### 发现清单

| ID | 类别 | 严重性 | 位置 | 摘要 | 建议 |
|----|------|--------|------|------|------|
| A1 | 重复 | HIGH | DS-050:§3.2 | 两个相似需求... | 合并表述 |
| C1 | 覆盖 | CRITICAL | DS-050:§1.1 | 核心功能零任务覆盖 | 添加任务 |

### 覆盖摘要

| 需求键 | 有任务? | 任务ID | 备注 |
|--------|---------|--------|------|
| user-can-upload | ✅ | T001,T002 | |
| api-rate-limit | ❌ | - | 需添加 |

### 宪法对齐问题

- [CRITICAL] system_patterns.md §2.3: "所有API必须定义速率限制" - DS-050未覆盖

### 未映射任务

- T005: 引用文件 `src/auth.rs` 在Spec中未定义

### 统计指标

- 总需求数: 12
- 总任务数: 15
- 覆盖率: 83%
- 模糊项: 3
- 重复项: 2
- CRITICAL项: 1
```

### Step 6: 下一步行动

```
## 下一步行动

⚠️ 存在CRITICAL问题: 建议在运行 /cdd.implement 前解决

[ ] 解决DS-050:§1.1的零覆盖问题
[ ] 添加API速率限制需求的任务
[ ] 合并重复需求 A2,A3

如仅存在LOW/MEDIUM问题，可继续执行，但建议改进。
```

---

## 集成到CDD工作流

### State B (v1.4.0更新)

```
State B: 规划阶段
├── Clarify (WF-CLARIFY)
├── Specify (DS-050)
├── Plan (DS-051)
├── Tasking (DS-052)
├── ✅ ANALYZE (WF-ANALYZE) ← 新增门禁
└── ✅ CHECKLIST生成 (DS-053) ← 新增输出
```

### 触发条件

```yaml
analyze_trigger:
  after: "DS-052生成完成"
  before: "State C执行"
  mandatory: true  # 必须通过才能进入State C
```

---

## 上下文效率原则

1. **渐进式披露**: 按需加载文档，避免全量dump
2. **高信号Tokens**: 聚焦可操作发现，非 exhaustive 文档
3. **确定性结果**: 无变化重跑应产生一致ID和计数
4. **零发现优雅处理**: 输出成功报告和覆盖率统计

---

**协议版本**: v1.3.2  
**最后更新**: {{TIMESTAMP}}  
**维护者**: CDD Framework
