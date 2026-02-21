# Constitution-Driven Development (CDD)

<div align="center">

**🎯 让AI辅助开发变得可控、可预测、可持续**

**📖 本文档面向开发者/新用户 - 快速入门指南**

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

### 📋 5分钟快速检查表

#### ✅ 步骤1：环境检查（1分钟）
```bash
# 检查并修复环境依赖
python scripts/cdd_check_env.py --fix

# 预期输出：
# ✅ 环境检查完成: 3/3 必需依赖
```

#### ✅ 步骤2：技能验证（1分钟）
```bash
# 验证CDD技能完整性
python scripts/cdd_verify.py

# 预期输出：
# ✅ 技能完整性验证通过
```

#### ✅ 步骤3：创建项目（1分钟）
```bash
# 正确做法：在项目目录中执行
cd /path/to/your/project
python /path/to/cdd/scripts/cdd_feature.py deploy "项目名称"

# ❌ 错误做法：在CDD目录中执行（孢子隔离违例）
cd /path/to/cdd
python scripts/cdd_feature.py deploy "项目名称"  # ❌ 会失败
```

#### ✅ 步骤4：创建特性（1分钟）
```bash
# 检查熵值
python /path/to/cdd/scripts/cdd_entropy.py calculate

# 如果 H_sys ≤ 0.7，创建特性
python /path/to/cdd/scripts/cdd_feature.py create "特性名称"

# 查看生成的规格文档
cat specs/001-特性名称/DS-050_feature_specification.md
```

#### ✅ 步骤5：运行诊断（1分钟）
```bash
# 综合诊断
python /path/to/cdd/scripts/cdd_diagnose.py

# 如果发现问题，尝试自动修复
python /path/to/cdd/scripts/cdd_diagnose.py --fix
```

### 详细安装指南

#### 第一步：安装

```bash
# 克隆CDD技能库
git clone https://github.com/wsman/Constitution-Driven-Development-Skill.git
cd Constitution-Driven-Development-Skill

# 检查环境
python scripts/cdd_check_env.py --fix
```

#### 第二步：初始化你的项目

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

#### 第三步：创建第一个特性

```bash
# 使用绝对路径方式
cd /path/to/your/project
python /full/path/to/cdd/scripts/cdd_feature.py create "用户登录"

# 查看生成的文档
cat specs/001-用户登录/DS-050_feature_specification.md
```

**🎉 恭喜！你已经完成CDD的首次使用！**

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

#### 📊 熵值速查表

| H_sys范围 | 状态 | 颜色 | 立即操作 |
|-----------|------|------|----------|
| **0.0 - 0.3** | 🟢 优秀 | 绿色 | 正常开发 |
| **0.3 - 0.5** | 🟡 良好 | 黄色 | 监控技术债务 |
| **0.5 - 0.7** | 🟠 警告 | 橙色 | `cdd_entropy.py optimize --dry-run` |
| **> 0.7** | 🔴 危险 | 红色 | `cdd_entropy.py optimize` (立即停止新功能) |

##### 熵值相关命令
```bash
# 检查当前熵值
python /path/to/cdd/scripts/cdd_entropy.py calculate

# 解读结果：
# ✅ H_sys = 0.25 (优秀 🟢)    # 可以继续
# ⚠️ H_sys = 0.65 (警告 🟠)    # 需要优化
# ❌ H_sys = 0.85 (危险 🔴)    # 必须立即优化
```

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

#### 🔄 5状态工作流速查

##### State A (Intake) → State B (Plan)
```bash
# 1. 加载上下文
cat memory_bank/t0_core/active_context.md

# 2. 检查熵值
python /path/to/cdd/scripts/cdd_entropy.py calculate

# 3. 如果 H_sys ≤ 0.7，创建规格
python /path/to/cdd/scripts/cdd_feature.py create "特性名"
```

##### State B (Plan) → State C (Execute)
```bash
# 1. 检查规格文档是否已批准
cat specs/*/DS-050_*.md | grep "批准状态: ✅ 已批准"

# 2. 如果已批准，开始编码
# 3. 编写测试
# 4. 运行本地测试
pytest tests/ -v
```

##### State C (Execute) → State D (Verify)
```bash
# 1. 运行完整宪法审计
python /path/to/cdd/scripts/cdd_auditor.py --gate all

# 2. 如果Gate失败，根据错误信息修复
```

##### State D (Verify) → State E (Close)
```bash
# 1. 所有Gate通过后，更新文档
echo "最近宪法事件: [日期] Gate 1-5全部通过" >> memory_bank/t0_core/active_context.md

# 2. 原子性提交
git add .
git commit -m "feat: 实现[特性名称] - 宪法依据: §101§102§300.3"
```

##### State E (Close) → State A (Intake)
```bash
# 系统自动返回State A，准备下一个特性
echo "✅ 特性交付完成，系统返回State A (Intake)"
```

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

### 🛠️ 工具速查表

#### 所有工具通用参数
```bash
# 获取帮助
python scripts/cdd_feature.py --help
python scripts/cdd_auditor.py --help
python scripts/cdd_entropy.py --help
python scripts/cdd_diagnose.py --help
```

#### 1. cdd_feature.py - 项目管理
```bash
# 🔥 核心用例
cd /path/to/project && python /path/to/cdd/scripts/cdd_feature.py deploy "项目名"  # 初始化项目
cd /path/to/project && python /path/to/cdd/scripts/cdd_feature.py create "特性名"  # 创建特性
cd /path/to/project && python /path/to/cdd/scripts/cdd_feature.py list          # 列出所有特性

# 🎯 进阶用法
cd /path/to/project && python /path/to/cdd/scripts/cdd_feature.py create "特性名" --dry-run  # 预览不生成
cd /path/to/project && python /path/to/cdd/scripts/cdd_feature.py create "特性名" --json    # JSON格式输出
```

#### 2. cdd_auditor.py - 宪法审计
```bash
# 🔥 核心用例
cd /path/to/project && python /path/to/cdd/scripts/cdd_auditor.py --gate all  # 完整审计
cd /path/to/project && python /path/to/cdd/scripts/cdd_auditor.py --gate 1 --fix  # 自动修复版本问题

# 🎯 进阶用法
cd /path/to/project && python /path/to/cdd/scripts/cdd_auditor.py --gate all --verbose  # 详细输出
cd /path/to/project && python /path/to/cdd/scripts/cdd_auditor.py --gate all --format json  # JSON报告
cd /path/to/project && python /path/to/cdd/scripts/cdd_auditor.py --gate 3  # 仅检查熵值
```

#### 3. cdd_entropy.py - 熵值管理
```bash
# 🔥 核心用例
cd /path/to/project && python /path/to/cdd/scripts/cdd_entropy.py calculate  # 计算当前熵值
cd /path/to/project && python /path/to/cdd/scripts/cdd_entropy.py optimize   # 优化熵值

# 🎯 进阶用法
cd /path/to/project && python /path/to/cdd/scripts/cdd_entropy.py analyze   # 分析熵值热点
cd /path/to/project && python /path/to/cdd/scripts/cdd_entropy.py optimize --dry-run  # 预览优化建议
cd /path/to/project && python /path/to/cdd/scripts/cdd_entropy.py calculate --force  # 强制重新计算
```

#### 4. cdd_diagnose.py - 综合诊断
```bash
# 🔥 核心用例
cd /path/to/project && python /path/to/cdd/scripts/cdd_diagnose.py  # 综合诊断
cd /path/to/project && python /path/to/cdd/scripts/cdd_diagnose.py --fix  # 诊断并自动修复

# 🎯 进阶用法
cd /path/to/project && python /path/to/cdd/scripts/cdd_diagnose.py --json  # JSON格式输出
cd /path/to/project && python /path/to/cdd/scripts/cdd_diagnose.py --summary  # 只显示摘要
```

### ⚠️ 常见错误与立即解决方案

#### 错误1：❌ 孢子隔离违例 (C003)
**症状**：`Target directory is CDD Skill Root: /path/to/cdd`
**原因**：在CDD技能目录中运行工具，违反§106.1
**解决方案**：
```bash
# 错误做法 ❌
cd /path/to/cdd
python scripts/cdd_feature.py deploy "项目名"

# 正确做法 ✅
cd /path/to/your/project
python /path/to/cdd/scripts/cdd_feature.py deploy "项目名"
```

#### 错误2：❌ 熵值超标 (C001)
**症状**：`H_sys = 0.85 (危险 🔴)` 或 `Gate 3 failed`
**原因**：系统熵值过高，违反§102
**解决方案**：
```bash
# 1. 分析熵值热点
python /path/to/cdd/scripts/cdd_entropy.py analyze

# 2. 生成优化建议
python /path/to/cdd/scripts/cdd_entropy.py optimize --dry-run

# 3. 执行优化
python /path/to/cdd/scripts/cdd_entropy.py optimize

# 4. 重新计算熵值
python /path/to/cdd/scripts/cdd_entropy.py calculate

# ✅ 只有当 H_sys ≤ 0.5 时才能继续新功能
```

#### 错误3：❌ Gate 1失败
**症状**：`Gate 1: 版本一致性检查 ❌ FAILED`
**原因**：文件版本信息不一致，违反§100.3
**解决方案**：
```bash
# 自动修复版本问题
python /path/to/cdd/scripts/cdd_auditor.py --gate 1 --fix
```

#### 错误4：❌ Gate 2失败
**症状**：`Gate 2: 行为验证检查 ❌ FAILED`
**原因**：测试未通过，违反§300.3
**解决方案**：
```bash
# 查看详细测试错误
pytest tests/ -v

# 修复失败的测试后重新运行
python /path/to/cdd/scripts/cdd_auditor.py --gate 2
```

#### 错误5：❌ Spec未批准 (C005)
**症状**：`Spec未批准: 不能在State B编码`
**原因**：未获得DS-050规格文档批准，违反§103
**解决方案**：
```bash
# 检查规格文档状态
cat specs/*/DS-050_*.md | grep "批准状态"

# 等待用户明确批准：✅ 已批准
```

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

### 状态转换表 (详细版)

| 当前状态 | 触发条件 | 下一状态 | 必需操作 | 禁止操作 |
|----------|----------|----------|----------|----------|
| **A (Intake)** | 意图明确，H_sys ≤ 0.7 | B | 加载`active_context.md`，检查系统熵值 | 编码 |
| **B (Plan)** | DS-050获批准 | C | 生成DS-050/051/052文档，等待用户批准 | 编码 |
| **B (Plan)** | Spec未批准 | B | 细化规格文档，重新提交批准 | 编码 |
| **C (Execute)** | 代码完成，本地测试通过 | D | 实现代码，编写并通过单元测试 | 跳过测试 |
| **D (Verify)** | Gate 1-5全部通过 | E | 运行`cdd_auditor.py --gate all` | 提交代码 |
| **D (Verify)** | 任意Gate失败 | C | 修复问题，重新运行测试 | 继续新功能 |
| **E (Close)** | - | A | 更新`active_context.md`，原子性提交代码和文档 | - |

### 快速参考表

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

### 🚨 紧急恢复流程

#### 系统异常中断恢复
```bash
# 1. 检查当前状态
cat memory_bank/t0_core/active_context.md

# 2. 运行综合诊断
python /path/to/cdd/scripts/cdd_diagnose.py --fix

# 3. 根据诊断结果修复
```

#### 项目结构损坏恢复
```bash
# 1. 验证项目结构
python /path/to/cdd/scripts/cdd_feature.py list

# 2. 重新部署Memory Bank（谨慎使用）
python /path/to/cdd/scripts/cdd_feature.py deploy "项目名" --force

# 3. 恢复备份（如果有）
```

#### Git冲突解决流程
```bash
# 1. 检查冲突状态
git status

# 2. 优先保持memory_bank/一致性
# 3. 解决冲突，确保宪法引用完整
# 4. 运行审计确保合规
python /path/to/cdd/scripts/cdd_auditor.py --gate all
```

### 📞 快速帮助

#### 忘记命令时
```bash
# 记住这个万能命令：
python scripts/cdd_diagnose.py --fix

# 它会：
# 1. 检查环境
# 2. 验证技能
# 3. 运行审计
# 4. 检查熵值
# 5. 尝试自动修复
```

#### 需要更多帮助时
```bash
# 查看完整文档
cat README.md        # 基础指南
cat SKILL.md         # AI代理指南
cat reference.md     # 技术参考

# 或者直接搜索
grep -r "孢子隔离" reference.md
grep -r "熵值超标" SKILL.md
```

### 🎯 最佳实践摘要

1. **✅ 总是在项目目录调用工具** - 避免孢子隔离违例
2. **✅ 先检查熵值再创建特性** - 确保H_sys ≤ 0.7
3. **✅ State B必须等待批准才能编码** - 遵守文档优先公理
4. **✅ State D必须通过所有Gate才能提交** - 确保宪法合规
5. **✅ 熵值 > 0.7时立即停止新功能** - 优先降低熵值

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

**🔄 本指南已包含CDD 80%的日常使用场景**

**📚 如需深入了解，请阅读完整文档**

</div>

---

**宪法依据**: §100.3§101§102§103§104§106.1§300.3§300.5  
**版本**: v2.0.0  
**更新日期**: 2026-02-21

---

<div align="center">

**Made with ❤️ for better AI-assisted development**

</div>