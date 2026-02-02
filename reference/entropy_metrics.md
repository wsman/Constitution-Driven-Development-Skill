# System Entropy Metrics ($H_{sys}$)

CDD 使用热力学熵的概念来量化软件系统的混乱度。

## 核心公式
$$H_{sys} = w_1 \cdot H_{cog} + w_2 \cdot H_{struct} + w_3 \cdot H_{align}$$

### 1. 认知负载 ($H_{cog}$)
- **定义**: 理解一个模块所需的上下文大小。
- **计算**: $Token_{context} / Token_{limit}$
- **阈值**: > 0.8 为危险。

### 2. 结构离散 ($H_{struct}$)
- **定义**: 文件与目录的混乱程度。
- **计算**: $1 - (N_{linked} / N_{total})$ (孤儿文件比例)

### 3. 同构偏离 ($H_{align}$)
- **定义**: 代码实现与架构文档的不一致性。
- **计算**: $1 - C_{sig}$ (接口签名覆盖率)

## 状态阈值 (v1.6.0 校准)
- **🟢 优秀**: $0.0 - 0.3$
- **🟡 良好**: $0.3 - 0.7$ (Template Repo 豁免线)
- **🔴 危险**: $> 0.7$ (必须重构)

## 🔧 相关模板 (Related Templates)

### 核心宪法模板
- **`core/active_context.md`**

### 执行标准模板
- **`standards/DS-054_environment_hardening.md`**

### 使用说明
1. **阅读顺序**: 先阅读本概念文件，再查阅相关模板
2. **模板实例化**: 使用 `cdd-feature.py` 自动生成具体实现
3. **层级对应**: 这些模板对应T0-T3文档体系的不同层级
