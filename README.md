# Constitution-Driven Development (CDD)

<div align="center">

**🎯 让AI辅助开发变得可控、可预测、可持续**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/wsman/Constitution-Driven-Development-Skill)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org/)

</div>

---

## 🤔 CDD是什么？

**CDD（宪法驱动开发）** 是一个专为AI辅助开发设计的方法论和工具集。它通过"宪法"（一套明确的规则和约束）来指导AI代理进行软件开发，确保代码质量和项目可持续性。

### 核心理念

| 概念 | 说明 | 类比 |
|------|------|------|
| **宪法** | 定义开发规则和约束的文档 | 像国家的宪法，是最高准则 |
| **熵值** | 衡量系统混乱程度的指标 | 像温度计，告诉你系统健康程度 |
| **Memory Bank** | 项目的知识库 | 像团队的知识库，记录所有重要决策 |
| **5状态工作流** | 从需求到交付的标准流程 | 像工厂流水线，标准化生产过程 |

### CDD适合你吗？

✅ **适合**：
- 使用Claude Code等AI代理进行开发
- 希望项目有清晰的结构和文档
- 团队需要统一的开发规范
- 关注代码质量和可维护性

❌ **可能不适合**：
- 简单的一次性脚本
- 不使用AI辅助开发
- 项目规模很小（<100行代码）

---

## 🚀 快速开始

### 第一步：安装

```bash
# 克隆CDD技能库
git clone https://github.com/wsman/Constitution-Driven-Development-Skill.git
cd Constitution-Driven-Development-Skill

# 检查环境
python scripts/cdd_check_env.py --fix
```

### 第二步：初始化你的项目

```bash
# 方式1: 使用绝对路径（推荐）
cd /path/to/your/project
python /full/path/to/cdd/scripts/cdd_feature.py deploy "我的项目"

# 方式2: 如果在CDD技能目录中（注意孢子隔离）
python scripts/cdd_feature.py deploy "我的项目" --target /path/to/your/project
```

**⚠️ 重要提示**：
- **孢子隔离原则**：CDD工具不能意外修改技能库自身
- **正确做法**：在你的项目目录中调用CDD工具
- **常见错误**：在CDD技能目录中直接运行工具（违反§106.1）

### 第三步：创建第一个特性

```bash
# 使用绝对路径方式
cd /path/to/your/project
python /full/path/to/cdd/scripts/cdd_feature.py create "用户登录"

# 查看生成的文档
cat specs/001-用户登录/DS-050_feature_specification.md
```

**🎉 恭喜！你已经完成CDD的首次使用！**

---

## 📚 详细安装

### 系统要求

| 依赖 | 最低版本 | 如何检查 | 如何安装 |
|------|----------|----------|----------|
| **Python** | 3.8+ | `python3 --version` | 系统包管理器 |
| **pytest** | 6.0+ | `pytest --version` | `pip install pytest` |
| **PyYAML** | 6.0+ | `python -c "import yaml"` | `pip install pyyaml` |

### 安装验证

```bash
# 验证CDD技能完整性
python scripts/cdd_verify.py

# 如果看到 ✅，安装成功！
```

---

## 🎓 核心概念简介

### 熵值 ($H_{sys}$)

熵值是衡量系统"混乱程度"的指标。熵值越低，系统越健康。

| 熵值范围 | 状态 | 含义 |
|----------|------|------|
| **0.0 - 0.3** | 🟢 优秀 | 系统非常健康 |
| **0.3 - 0.5** | 🟡 良好 | 存在少量技术债务 |
| **0.5 - 0.7** | 🟠 警告 | 需要关注 |
| **> 0.7** | 🔴 危险 | 需要立即重构 |

### 5状态工作流

CDD将开发过程分为5个明确的状态：

```
📝 State A (Intake)    → 理解需求，加载上下文
     ↓
📋 State B (Plan)      → 编写规格文档，等待批准
     ↓                 ⚠️ 此时不能编码！
💻 State C (Execute)   → 实现代码，编写测试
     ↓
🔍 State D (Verify)    → 运行审计，确保合规
     ↓
✅ State E (Close)     → 更新文档，提交代码
```

**关键规则**：
- State B **必须等待批准** 才能编码
- State D **所有Gate通过** 才能提交
- 熵值 > 0.7 时**必须先重构**

### Memory Bank

Memory Bank是项目的"大脑"，存储所有重要信息：

| 目录 | 内容 | 用途 |
|------|------|------|
| `t0_core/` | 当前状态、知识图谱 | 了解项目现状 |
| `t1_axioms/` | 架构模式、接口签名 | 理解系统约束 |
| `t2_protocols/` | 工作流协议 | 执行标准流程 |
| `t2_standards/` | 实现标准 | 遵循开发规范 |

---

## 📋 快速参考

### 常用命令速查表

| 工具 | 用途 | 基本命令 |
|------|------|----------|
| `cdd_feature.py` | 项目初始化/特性创建 | `python scripts/cdd_feature.py deploy "项目名称"`<br>`python scripts/cdd_feature.py create "特性名称"` |
| `cdd_auditor.py` | 宪法审计 | `python scripts/cdd_auditor.py --gate all`<br>`python scripts/cdd_auditor.py --gate 1 --fix` |
| `cdd_entropy.py` | 熵值管理 | `python scripts/cdd_entropy.py calculate`<br>`python scripts/cdd_entropy.py optimize` |
| `cdd_check_env.py` | 环境检查 | `python scripts/cdd_check_env.py --fix` |
| `cdd_verify.py` | 技能完整性验证 | `python scripts/cdd_verify.py` |
| `cdd_diagnose.py` | 综合诊断 | `python scripts/cdd_diagnose.py --fix` |

### 熵值阈值表

| 熵值范围 | 状态 | 颜色 | 建议操作 |
|----------|------|------|----------|
| **0.0 - 0.3** | 🟢 优秀 | 绿色 | 正常开发 |
| **0.3 - 0.5** | 🟡 良好 | 黄色 | 正常开发，监控技术债务 |
| **0.5 - 0.7** | 🟠 警告 | 橙色 | 暂停新功能，优先修复 |
| **> 0.7** | 🔴 危险 | 红色 | 立即停止所有新功能，重构优先 |

### 状态转换表

| 当前状态 | 触发条件 | 下一状态 | 关键规则 |
|----------|----------|----------|----------|
| **State A (Intake)** | 意图明确，H_sys ≤ 0.7 | B | 理解需求，加载上下文 |
| **State B (Plan)** | DS-050获批准 | C | **必须等待批准**才能编码 |
| **State C (Execute)** | 代码完成，本地测试通过 | D | 实现代码，编写测试 |
| **State D (Verify)** | Gate 1-5全部通过 | E | **所有Gate通过**才能提交 |
| **State E (Close)** | 文档更新，代码提交 | A | 更新文档，原子性提交 |

### 错误代码速查表

| 代码 | 含义 | 解决方案 |
|------|------|----------|
| **C001** | 熵值超标 | `cdd_entropy.py optimize` |
| **C002** | 文档不同步 | 更新`memory_bank/`中的文档 |
| **C003** | 孢子隔离违例 | 在项目目录调用工具 |
| **C004** | 工作流状态无效 | 检查`active_context.md` |
| **C005** | Spec未批准 | 等待用户批准DS-050文档 |
| **C006** | Gate审计失败 | `cdd_auditor.py --gate all --verbose` |

---

## 📖 文档导航

CDD提供三份核心文档，面向不同读者：

### 1. **README.md** (你现在读的)
- **目标读者**：开发者、新用户
- **内容**：项目概述、快速开始、核心概念简介
- **用途**：快速了解CDD并开始使用

### 2. **[SKILL.md](SKILL.md)** (AI代理手册)
- **目标读者**：AI代理、自动化工具
- **内容**：工具指令、状态机、宪法约束、操作流程
- **用途**：指导AI代理执行CDD工作流

### 3. **[reference.md](reference.md)** (完整参考手册)
- **目标读者**：高级用户、贡献者、技术专家
- **内容**：完整技术参考、架构设计、API详情、深入原理
- **用途**：查阅所有技术细节和实现原理

---

## 📂 项目结构概览

### CDD技能目录

```
cdd/
├── README.md              # 👈 你正在看的文档
├── SKILL.md              # AI代理指南
├── reference.md          # 完整参考手册
├── scripts/              # 核心工具
├── core/                 # 核心模块
├── templates/            # 项目模板
├── claude/               # Claude Code集成
└── examples/             # 示例项目
```

### 初始化后的项目结构

```
your_project/
├── memory_bank/           # 知识库（重要！）
│   ├── t0_core/          # 核心文档
│   ├── t1_axioms/        # 架构公理
│   ├── t2_protocols/     # 工作流协议
│   └── t2_standards/     # 实现标准
├── specs/                 # 特性规格
│   └── 001-feature/
├── src/                   # 源代码
└── tests/                 # 测试文件
```

---

## 🎯 下一步学习

| 学习路径 | 建议文档 | 内容 |
|----------|----------|------|
| **使用AI代理开发** | [SKILL.md](SKILL.md) | AI代理完整指令和操作流程 |
| **深入了解技术细节** | [reference.md](reference.md) | 完整的技术参考和实现原理 |
| **查看示例项目** | [examples/hello-cdd/](examples/hello-cdd/) | 完整的CDD项目示例 |
| **Claude Code集成** | [claude/README.md](claude/README.md) | Claude Code详细集成指南 |

---

## 🔗 相关资源

- **GitHub仓库**：https://github.com/wsman/Constitution-Driven-Development-Skill
- **问题反馈**：https://github.com/wsman/Constitution-Driven-Development-Skill/issues
- **讨论区**：https://github.com/wsman/Constitution-Driven-Development-Skill/discussions

---

## 📄 许可证

基于 Apache License 2.0 授权。详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**Made with ❤️ for better AI-assisted development**

</div>