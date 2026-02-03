# WF-AMEND: 宪法修正案协议

**版本**: v1.5.0  
**协议类型**: T2-工作流协议  
**来源**: Spec-Kit constitution.md  
**触发**: 任何针对 T0 (Core) 或 T1 (Axioms) 文档的修改请求

---

## 1. 目标

确保核心法则 (Constitution) 的变更是有序、可追溯且版本兼容的，防止"违宪"或架构漂移。

## 2. 修正流程 (Amendment Process)

### Step 1: 提案与起草 (Drafting)

用户输入变更意图，AI 识别目标文档：

| 类型 | 文档示例 | 影响范围 |
|------|----------|----------|
| **T0** | `basic_law_index.md`, `procedural_law_index.md` | 影响全局 |
| **T1** | `system_patterns.md`, `tech_context.md` | 影响特定域 |

### Step 2: 版本号计算 (SemVer Calculation)

根据变更性质决定版本升级策略：

| 变更类型 | 版本 | 说明 |
|----------|------|------|
| **MAJOR** | x.0.0 | 移除原则、改变核心架构模式 (不兼容) |
| **MINOR** | 1.x.0 | 新增原则、扩展解释 (向下兼容) |
| **PATCH** | 1.0.x | 措辞优化、勘误 (无语义变更) |

### Step 3: 传播检查 (Consistency Propagation)

这是最关键的一步。如果 T0/T1 变更了，必须检查 T2 模板是否需要同步：

| T0/T1变更 | T2检查项 |
|-----------|----------|
| 新增"隐私原则" | `DS-050` 是否需要增加"隐私需求"章节？ |
| 修改"工作流" | `DS-051` 模板是否过时？ |
| 删除"行为约束" | `DS-052` 任务类型是否需要调整？ |

### Step 4: 影响报告 (Impact Report)

在提交变更前，生成以下摘要：

```markdown
## ⚖️ 修正案影响报告

**变更文档**: `templates/core/basic_law_index.md`
**版本变更**: v1.4.0 → v1.5.0 (MINOR)

### 变更摘要
- [新增] 第5条：所有API必须幂等

### 传播检查
- [⚠️] `DS-050_feature_specification.md`: 需增加"幂等性"验收标准
- [✅] `DS-052_atomic_tasks.md`: 无影响

### 操作建议
1. 更新 `basic_law_index.md` 版本号
2. 同步更新 `DS-050` 模板
3. 提交时附带此报告 3. 提交与生效

1. 更新目标
```

##文档内容
2. 更新文档头部的 `Version` 字段
3. 如果有传播项，必须在此次 Commit 中一并修正 T2 模板

## 4. 配置选项

在 `cdd_config.yaml` 中配置：

```yaml
# 治理配置 (v1.5.0)
governance:
  amendment_protocol: "templates/protocols/WF-amend.md"
  versioning_scheme: "semver"  # 语义化版本
  protected_paths:
    - "templates/core/*"       # T0核心文件保护
    - "templates/axioms/*"     # T1公理文件保护
  require_impact_report: true  # 必须生成影响报告
```

---

## 5. 示例场景

### 场景: 新增"安全第一"原则

**输入**: "在T0层增加'安全第一'原则"

**处理**:
1. 识别目标: `templates/core/basic_law_index.md`
2. 版本计算: MINOR (新增原则，向下兼容)
3. 传播检查:
   - `DS-050`: 需要增加"安全需求"章节
   - `DS-051`: 无影响
4. 生成影响报告

**输出**:
- 更新后的 `basic_law_index.md` (v1.5.0)
- 更新后的 `DS-050` 模板
- 修正案报告

---

**协议版本**: v1.5.0  
**最后更新**: {{TIMESTAMP}}
