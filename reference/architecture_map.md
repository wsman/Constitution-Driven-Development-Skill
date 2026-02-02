# CDD三级递进架构地图

## 🏛️ 架构概述

CDD采用三级递进架构设计，确保AI能够高效理解和执行宪法驱动开发：

```
第一级: SKILL.md (总纲层) - AI执行手册，快速上手
第二级: reference/ (概念层) - 模块化概念，深度理解  
第三级: templates/ (实现层) - 具体模板，直接使用
```

## 📊 文件统计

| 层级 | 目录 | 文件数量 | 平均大小 |
|------|------|----------|----------|
| **第一级** | SKILL.md | 1个文件 | ~3KB |
| **第二级** | reference/ | 11个文件 || 10个文件 | ~1KB/文件 |
| **第三级** | templates/ | 24个文件 | ~2KB/文件 |

## 🔗 映射关系

### 架构体系 (Architecture)

### 架构体系

#### `architecture_overview.md`
- **描述**: reference/architecture_overview.md的相关模板
- **相关模板**:
  - `core/active_context.md`
  - `axioms/system_patterns.md`
  - `axioms/tech_context.md`
  - `standards/DS-050_feature_specification.md`
  - `standards/DS-051_implementation_plan.md`

#### `cdd_document_system_guide.md`
- **描述**: reference/cdd_document_system_guide.md的相关模板
- **相关模板**:
  - `core/active_context.md`
  - `core/knowledge_graph.md`
  - `core/basic_law_index.md`
  - `core/procedural_law_index.md`
  - `core/technical_law_index.md`
  - `axioms/system_patterns.md`
  - `axioms/tech_context.md`
  - `axioms/behavior_context.md`
  - `standards/DS-050_feature_specification.md`
  - `standards/DS-051_implementation_plan.md`
  - `standards/DS-052_atomic_tasks.md`


### 工作流程

#### `core_workflow.md`
- **描述**: reference/core_workflow.md的相关模板
- **相关模板**:
  - `protocols/WF-201_cdd_workflow.md`
  - `protocols/WF-review.md`
  - `protocols/WF-amend.md`

#### `external_auditor.md`
- **描述**: reference/external_auditor.md的相关模板
- **相关模板**:
  - `protocols/WF-review.md`
  - `standards/DS-060_code_review.md`


### 法律框架

#### `legal_framework.md`
- **描述**: reference/legal_framework.md的相关模板
- **相关模板**:
  - `core/basic_law_index.md`
  - `core/procedural_law_index.md`
  - `core/technical_law_index.md`
  - `protocols/WF-amend.md`

#### `template_usage.md`
- **描述**: reference/template_usage.md的相关模板
- **相关模板**:
  - `standards/DS-050_feature_specification.md`
  - `standards/DS-051_implementation_plan.md`
  - `standards/DS-052_atomic_tasks.md`
  - `standards/feature_readme_template.md`


### 技术实现

#### `cdd_model_config.md`
- **描述**: reference/cdd_model_config.md的相关模板
- **相关模板**:
  - `core/active_context.md`
  - `core/guide.md`

#### `entropy_metrics.md`
- **描述**: reference/entropy_metrics.md的相关模板
- **相关模板**:
  - `core/active_context.md`
  - `standards/DS-054_environment_hardening.md`

#### `entropy_calculation_guide.md`
- **描述**: reference/entropy_calculation_guide.md的相关模板
- **相关模板**:
  - `axioms/system_patterns.md`
  - `axioms/tech_context.md`
  - `axioms/behavior_context.md`


### 版本管理

#### `README.md#version-history--features`
- **描述**: README.md中的版本历史与特性(已合并)
- **相关模板**:
  - `core/active_context.md`
  - `protocols/WF-amend.md`

## 🚀 使用指南

### 对于AI代理
1. **初次接触**: 从SKILL.md开始，了解核心工作流
2. **遇到问题**: 查阅reference/中的相关概念文件
3. **需要实现**: 查看templates/中的具体模板
4. **审计验证**: 使用`cdd_audit.py`确保合规

### 对于开发者
1. **新特性开发**: 使用`cdd-feature.py`自动生成T2文档
2. **架构变更**: 更新templates/core/中的宪法文件
3. **概念扩展**: 在reference/中添加新的概念文档
4. **模板优化**: 改进templates/standards/中的模板

## 🔄 工作流示例

### 示例1: 创建用户认证特性
```
SKILL.md → template_usage.md → DS-050_feature_specification.md
                                  ↓
                         cdd-feature.py "用户认证"
                                  ↓
                        specs/xxx-user-auth/
```

### 示例2: 审计项目状态
```
SKILL.md → external_auditor.md → WF-review.md
                                   ↓
                          cdd_audit.py --ai-hint
```

### 示例3: 更新宪法约束
```
SKILL.md → legal_framework.md → basic_law_index.md
                                   ↓
                            WF-amend协议
```

## 📈 架构优势

1. **认知负载优化**: 三级分离避免信息过载
2. **导航路径清晰**: AI知道何时查阅哪个层级
3. **维护成本低**: 概念与实现分离，易于更新
4. **扩展性强**: 新增概念只需添加reference文件

---

**最后更新**: 2026-02-03  
**版本**: v1.6.1  
**状态**: 🟢 活跃 (与CDD宪法v1.6.1同步)
