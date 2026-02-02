# Template Usage Guide

CDD 提供了标准化的文档模板以降低认知负载。

## 核心模板
- **DS-050 Feature Specification**:
  - 用途: 定义“做什么”和“为什么做”。
  - 必填: 用户故事、验收标准。
  
- **DS-051 Implementation Plan**:
  - 用途: 定义“怎么做”。
  - 必填: 阶段划分、技术决策。
  
- **DS-052 Atomic Tasks**:
  - 用途: 任务分解。
  - 必填: Checkbox 列表。

## 实例化工具
使用 `scripts/cdd-feature.py` 自动实例化这些模板。不要手动复制粘贴。

## 🔧 相关模板 (Related Templates)

### 执行标准模板
- **`standards/DS-050_feature_specification.md`**
- **`standards/DS-051_implementation_plan.md`**
- **`standards/DS-052_atomic_tasks.md`**
- **`standards/feature_readme_template.md`**

### 使用说明
1. **阅读顺序**: 先阅读本概念文件，再查阅相关模板
2. **模板实例化**: 使用 `cdd-feature.py` 自动生成具体实现
3. **层级对应**: 这些模板对应T0-T3文档体系的不同层级
