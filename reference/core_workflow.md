# CDD 5-State Workflow (Standard Operating Procedure)

所有开发活动必须遵循以下五状态循环：

## State A: Propose (提出)
- **输入**: 用户模糊需求。
- **动作**: 创建 Issue，讨论价值。
- **产出**: 明确的 Feature Request。

## State B: Plan (立法)
- **工具**: `cdd-feature.py`
- **动作**: 生成 T2 文档 (`DS-050`, `DS-051`)。
- **产出**: 包含上下文的 Spec 文档。
- **门禁**: 必须通过人工或架构师审批。

## State C: Act (执行)
- **原则**: Test-Driven Development (TDD)。
- **动作**: 编写代码以满足 Spec。
- **产出**: 源代码与测试用例。

## State D: Verify (司法)
- **工具**: `cdd_audit.py`
- **动作**: 运行 Gate 1-3。
  - Gate 1: 版本一致性
  - Gate 2: 行为测试 (Pytest)
  - Gate 3: 熵值检查
- **产出**: 绿色构建 (Pass)。

## State E: Evolve (演进)
- **动作**: 更新 T0 状态，合并代码。
- **产出**: 新的系统版本 (vX.Y.Z)。

## 🔧 相关模板 (Related Templates)

### 工作流协议模板
- **`protocols/WF-201_cdd_workflow.md`**
- **`protocols/WF-amend.md`**
- **`protocols/WF-review.md`**

### 使用说明
1. **阅读顺序**: 先阅读本概念文件，再查阅相关模板
2. **模板实例化**: 使用 `cdd-feature.py` 自动生成具体实现
3. **层级对应**: 这些模板对应T0-T3文档体系的不同层级
