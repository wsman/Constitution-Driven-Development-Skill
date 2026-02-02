# CDD Dual-Model Architecture Configuration

## 核心理念
CDD 采用“快思考”与“慢思考”结合的双模型架构，以平衡效率与严谨性。

### 1. 架构师 (Architect) - "Slow Thinking"
- **模型**: deepseek-reasoner (或同等推理模型)
- **角色**: 负责 T0/T1 级别的宪法制定、复杂熵值分析、架构决策。
- **职责**:
  - 制定 `active_context.md`
  - 分析 $H_{sys}$ 趋势
  - 批准 Gate 3 豁免

### 2. 工程师 (Engineer) - "Fast Thinking"
- **模型**: MiniMax M2.1 / GPT-4o / Claude 3.5 Sonnet
- **角色**: 负责 T2 级别的立法执行、代码编写、测试修复。
- **职责**:
  - 运行 `cdd-feature.py`
  - 编写业务代码
  - 执行 `cdd_audit.py`

## 交互协议
1. **指令下发**: 架构师生成 Specs (DS-050)。
2. **执行反馈**: 工程师提交代码与审计报告。
3. **纠偏**: 若 Gate 3 失败，架构师介入重构。

## 🔧 相关模板 (Related Templates)

### 核心宪法模板
- **`core/active_context.md`**
- **`core/active_context.md`**

### 使用说明
1. **阅读顺序**: 先阅读本概念文件，再查阅相关模板
2. **模板实例化**: 使用 `cdd-feature.py` 自动生成具体实现
3. **层级对应**: 这些模板对应T0-T3文档体系的不同层级
