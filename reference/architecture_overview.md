# CDD Architecture Panorama

## 法律体系分层 (The Hierarchy of Law)

CDD 系统由上至下分为三个法律层级，每一层都约束下一层的行为。

### T0: 核心宪法 (Constitutional Core)
- **定义**: 系统的最高真理，定义了“我们是谁”以及“系统状态”。
- **文件**: `templates/core/active_context.md`
- **变更**: 极低频。需通过 WF-amend 协议。

### T1: 系统公理 (System Axioms)
- **定义**: 这里的物理定律。定义了架构模式、技术栈约束和行为准则。
- **文件**: `system_patterns.md`, `tech_context.md`
- **变更**: 低频。随架构演进更新。

### T2: 执行标准 (Executive Standards)
- **定义**: 具体特性的立法文档。每个 Feature 必须对应一套 T2 文档。
- **文件**: `specs/xxx/DS-050_spec.md`, `DS-051_plan.md`
- **变更**: 高频。随特性开发产生。

## 同构映射 ($S_{fs} \cong S_{doc}$)
文件系统结构必须与文档结构保持同构。
- `src/auth/` 代码必须对应 `templates/axioms/system_patterns.md` 中的 Auth 模块定义。

## 🔧 相关模板 (Related Templates)

### 核心宪法模板
- **`core/active_context.md`**

### 系统公理模板
- **`axioms/system_patterns.md`**
- **`axioms/tech_context.md`**

### 执行标准模板
- **`standards/DS-050_feature_specification.md`**
- **`standards/DS-051_implementation_plan.md`**

### 使用说明
1. **阅读顺序**: 先阅读本概念文件，再查阅相关模板
2. **模板实例化**: 使用 `cdd-feature.py` 自动生成具体实现
3. **层级对应**: 这些模板对应T0-T3文档体系的不同层级
