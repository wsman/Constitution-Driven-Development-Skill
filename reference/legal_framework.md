# CDD Legal Framework & Axioms

## 核心公理
1. **§102.3 同步公理**: 代码与文档必须原子性同步。任何代码变更若无文档更新，视为非法。
2. **§201.5 熵减公理**: 任何提交不得使 $H_{sys}$ 突破 0.7，除非获得架构委员会豁免。
3. **Tier 2 签名验证**: 实现代码 ($I_{code}$) 必须是文档定义 ($I_{doc}$) 的超集 ($I_{code} \supseteq I_{doc}$)。

## 文档效力
- **Binding (约束性)**: T0, T1 文档。违反即 Build Fail。
- **Guiding (指导性)**: T2 模板。推荐遵循，但允许根据特性调整。

## 🔧 相关模板 (Related Templates)

### 核心宪法模板
- **`core/basic_law_index.md`**
- **`core/procedural_law_index.md`**
- **`core/technical_law_index.md`**

### 工作流协议模板
- **`protocols/WF-amend.md`**

### 使用说明
1. **阅读顺序**: 先阅读本概念文件，再查阅相关模板
2. **模板实例化**: 使用 `cdd-feature.py` 自动生成具体实现
3. **层级对应**: 这些模板对应T0-T3文档体系的不同层级
