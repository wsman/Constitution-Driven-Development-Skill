# CDD完整参考手册

<div align="center">

**📚 宪法驱动开发（CDD）v2.0.0 完整技术参考**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/wsman/Constitution-Driven-Development-Skill)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org/)

</div>

---

## 📖 文档定位

**本手册是CDD的完整技术参考文档**，面向：

| 读者 | 适用内容 | 建议阅读 |
|------|----------|----------|
| **高级用户** | 技术细节、配置参数、高级功能 | 全部章节 |
| **贡献者** | 架构设计、开发者指南、扩展开发 | 开发者指南、架构设计详解 |
| **技术专家** | 实现原理、算法细节、性能优化 | 熵值计算详解、架构设计详解 |
| **AI代理** | 操作手册、工作流指令 | 请参考 [SKILL.md](SKILL.md) |
| **新用户** | 快速开始、核心概念 | 请参考 [README.md](README.md) |

**与其他文档的关系**：
- **[README.md](README.md)**：面向开发者/新用户的简介和快速开始
- **[SKILL.md](SKILL.md)**：面向AI代理的操作手册和指令集
- **reference.md**（本手册）：完整的技术参考和实现细节

---

## 📖 目录

- [宪法条款索引](#宪法条款索引)
- [熵值计算详解](#熵值计算详解)
- [5状态工作流详解](#5状态工作流详解)
- [5门禁审计详解](#5门禁审计详解)
- [工具参考](#工具参考)
- [错误代码参考](#错误代码参考)
- [故障排除](#故障排除)
- [高级主题](#高级主题)
- [开发者指南](#开发者指南)
- [架构设计详解](#架构设计详解)
- [附录](#附录)

---

## 宪法条款索引

### 基本法（§100-§199） - 治理框架

| 条款 | 名称 | 描述 | 使用场景 |
|------|------|------|----------|
| **§100.3** | 同步公理 | 代码(C)与文档(D)必须原子性同步 | 版本控制、Gate 1 |
| **§101** | 单一真理源公理 | `memory_bank/`是唯一真理源 | 状态管理 |
| **§102** | 熵减原则 | 所有变更必须降低或维持系统熵值 | 架构设计、Gate 3 |
| **§103** | 文档优先公理 | 编码前必须先完成文档规划 | 特性开发 |
| **§104** | 持久化原则 | 检查点数据必须持久化保存 | 状态恢复 |
| **§148** | 控制论架构公理 | 三层控制论架构（治理层→控制层→执行层） | 系统架构 |

### 技术法（§200-§299） - 实施标准

| 条款 | 名称 | 描述 | 使用场景 |
|------|------|------|----------|
| **§106.1** | 孢子隔离公理 | S_tool ∩ S_target = ∅ | 工具安全、部署隔离 |
| **§267** | 观测回路 | 实时状态同步 | 状态监控 |
| **§268** | 控制回路 | 控制决策执行 | 决策执行 |
| **§269** | 记忆回路 | 知识结晶存储 | 知识管理 |

### 程序法（§300-§399） - 工作流程

| 条款 | 名称 | 描述 | 使用场景 |
|------|------|------|----------|
| **§300.3** | 三阶验证公理 | 状态变更需通过三级验证 | 审计验证、Gate 2 |
| **§300.5** | 熵值校准标准 | H_sys ≤ 0.3为优秀，≤ 0.5为良好 | 熵值评估、Gate 3 |
| **§309** | Claude Code自动化原则 | 鼓励使用Claude Code自动化 | 工具集成 |
| **§310** | 工具调用公理 | 文件操作必须通过工具桥接器 | 文件操作安全 |

**完整宪法条款列表**：请参考 `core/constitution_core.py`，包含62个实际使用的核心条款定义。

---

## 熵值计算详解

CDD使用两种互补的熵值视角来评估系统健康度：

### 1. 成分视角（用于系统内部分析）

此视角从系统内部组件的混乱程度来衡量熵值：

```
H_sys = 0.4 * H_cog + 0.3 * H_struct + 0.3 * H_align
```

| 指标 | 公式 | 描述 | 理想值 |
|------|------|------|--------|
| **H_cog** | $T_{load} / 8000$ | 认知负载：开发者理解系统所需的认知工作量 | < 0.4 |
| **H_struct** | $1 - N_{linked}/N_{total}$ | 结构离散：文件间连接缺失程度 | < 0.1 |
| **H_align** | $N_{violation} / N_{constraints}$ | 同构偏离：代码实现与架构约束的偏差 | 0.0 |

**使用场景**：
- 系统内部质量分析
- 架构优化决策
- 技术债务评估

### 2. 合规视角（用于宪法遵循度评估）

此视角从宪法遵循程度来衡量系统熵值：

```
compliance_score = W_DIR * C_dir + W_SIG * C_sig + W_TEST * C_test
H_sys = 1.0 - compliance_score
```

| 合规指标 | 权重 | 描述 | 计算公式 |
|----------|------|------|----------|
| **C_dir** | 0.4 | 目录结构合规率 | 符合CDD标准的目录比例 |
| **C_sig** | 0.3 | 接口签名覆盖率 | 文档中定义的接口实现比例 |
| **C_test** | 0.3 | 测试通过率 | 通过的测试用例比例 |

**权重配置**：
- W_DIR = 0.4（目录结构合规率权重）
- W_SIG = 0.3（接口签名覆盖率权重）
- W_TEST = 0.3（测试通过率权重）

### 3. 两种视角的关系与使用策略

**关系说明**：
- 当系统完全符合宪法时：合规分数高 → H_sys（合规）低
- 高合规分数通常对应低成分熵值
- 两者结合使用可获得系统健康度的完整视图

**使用时机**：
- **日常开发**：主要参考合规视角的H_sys值
- **架构重构**：深入分析成分熵值的各个维度
- **质量审计**：两者结合，全面评估系统健康度

### 4. 熵值评估标准

| H_sys范围 | 状态 | 颜色 | 含义 | 建议操作 |
|-----------|------|------|------|----------|
| **0.0 - 0.3** | 优秀 | 🟢 | 系统非常健康 | 正常开发 |
| **0.3 - 0.5** | 良好 | 🟡 | 存在少量技术债务 | 正常开发，注意监控 |
| **0.5 - 0.7** | 警告 | 🟠 | 熵增显著，需要关注 | 暂停新功能，优先修复 |
| **> 0.7** | 危险 | 🔴 | 需要立即重构 | 停止所有新功能开发 |

**关键阈值**：
- THRESHOLD_EXCELLENT = 0.3（优秀阈值）
- THRESHOLD_GOOD = 0.5（良好阈值）
- THRESHOLD_WARNING = 0.7（警告阈值）
- THRESHOLD_DANGER = 0.9（危险阈值）

### 5. 熵值管理工具

```bash
# 计算当前熵值
python scripts/cdd_entropy.py calculate

# 分析熵值热点
python scripts/cdd_entropy.py analyze

# 获取优化建议
python scripts/cdd_entropy.py optimize --dry-run

# 强制重新计算（忽略缓存）
python scripts/cdd_entropy.py calculate --force
```

---

## 5状态工作流详解

### 状态图

```
📝 State A (Intake)
    ↓
📋 State B (Plan) ← 等待批准
    ↓
💻 State C (Execute)
    ↓
🔍 State D (Verify)
    ↓
✅ State E (Close)
```

### 详细状态说明

#### State A: Intake（需求理解）
**目标**：充分理解需求，加载必要上下文
**必需操作**：
1. 加载 `memory_bank/t0_core/active_context.md`
2. 阅读 `memory_bank/t1_axioms/` 中的公理文档
3. 检查系统熵值：`H_sys ≤ 0.7`
**禁止操作**：编码

#### State B: Plan（规划设计）
**目标**：生成详细的实现规格
**必需操作**：
1. 创建T2规格文档（DS-050、DS-051、DS-052）
2. 等待用户明确批准DS-050
3. 确保规格符合技术约束（`tech_context.md`）
**关键规则**：**必须等待批准才能编码**

#### State C: Execute（编码实现）
**目标**：按照批准的规格实现代码
**必需操作**：
1. 实现DS-050中定义的功能
2. 编写单元测试
3. 本地运行测试确保通过
**质量要求**：遵循接口签名（`tech_context.md`）

#### State D: Verify（验证审计）
**目标**：确保实现符合宪法要求
**必需操作**：
1. 运行完整审计：`cdd_auditor.py --gate all`
2. 确保所有5个Gate通过
3. 如有失败，返回State C修复
**禁止操作**：在Gate通过前提交代码

#### State E: Close（交付关闭）
**目标**：完成特性交付
**必需操作**：
1. 更新 `active_context.md` 记录变更
2. 更新熵值状态
3. 原子性提交（代码 + 文档）
**最佳实践**：编写有意义的提交信息

### 状态转换检查表

| 转换 | 条件 | 验证命令 | 宪法依据 |
|------|------|----------|----------|
| A→B | 意图明确，H_sys ≤ 0.7 | `cdd_entropy.py calculate` | §102 |
| B→C | DS-050获得批准 | 用户明确确认 | §103 |
| C→D | 代码完成，测试通过 | `pytest tests/ -v` | §300.3 |
| D→E | 所有Gate通过 | `cdd_auditor.py --gate all` | §300.3 |
| 紧急回退 | H_sys > 0.7 | 立即执行熵值优化 | §300.5 |

---

## 5门禁审计详解

### Gate 1：版本一致性检查
**目的**：确保所有文件的版本信息一致
**检查内容**：
- 所有Python文件的`VERSION`常量
- 所有Markdown文件的版本头
- JSON/YAML配置文件的版本字段
**宪法依据**：§100.3（同步公理）
**修复命令**：`cdd_auditor.py --gate 1 --fix`
**错误代码**：101

### Gate 2：行为验证检查
**目的**：验证代码行为符合规格
**检查内容**：
- 运行pytest测试套件
- 确保所有测试通过
- 检查测试覆盖率（如配置）
**宪法依据**：§300.3（三阶验证公理）
**修复命令**：`pytest tests/ -v` 然后修复失败的测试
**错误代码**：102

### Gate 3：熵值监控检查
**目的**：监控系统熵值状态
**检查内容**：
- 计算当前系统熵值H_sys
- 验证H_sys ≤ 0.7（警告阈值）
- 检查熵值趋势（如配置）
**宪法依据**：§102（熵减原则）、§300.5（熵值校准标准）
**修复命令**：`cdd_entropy.py optimize`
**错误代码**：103

### Gate 4：语义审计检查
**目的**：检查宪法引用和语义一致性
**检查内容**：
- 扫描所有文档中的宪法引用
- 验证引用的条款存在（从`core/constitution_core.py`）
- 确保宪法引用覆盖率达到80%以上
**宪法依据**：§101（单一真理源公理）、§300.5（熵值校准标准）
**修复命令**：添加缺失的宪法引用
**错误代码**：105

### Gate 5：宪法引用完整性检查
**目的**：验证所有宪法引用格式正确
**检查内容**：
- 检查宪法引用格式（§NNN或§NNN.N）
- 验证引用的条款在宪法核心列表中存在
- 确保无无效或未知的条款引用
**宪法依据**：§305（宪法引用规范）
**修复命令**：修复无效的引用格式
**错误代码**：106

### 审计最佳实践

```bash
# 1. 定期运行完整审计
python scripts/cdd_auditor.py --gate all

# 2. 自动修复版本问题
python scripts/cdd_auditor.py --gate 1 --fix

# 3. 详细输出模式（调试用）
python scripts/cdd_auditor.py --gate all --verbose

# 4. 仅检查特定Gate
python scripts/cdd_auditor.py --gate 3  # 仅检查熵值

# 5. 生成JSON报告
python scripts/cdd_auditor.py --gate all --format json
```

---

## 工具参考

### cdd_check_env.py - 环境检查

**用途**：检查系统环境依赖
```bash
# 基本检查
python scripts/cdd_check_env.py

# 自动修复缺失依赖
python scripts/cdd_check_env.py --fix

# 检查特定组件
python scripts/cdd_check_env.py --check python
python scripts/cdd_check_env.py --check pytest
```

### cdd_verify.py - 技能完整性验证

**用途**：验证CDD技能库完整性
```bash
# 基本验证
python scripts/cdd_verify.py

# 完整验证（包含所有检查）
python scripts/cdd_verify.py --full

# 修复模式
python scripts/cdd_verify.py --fix
```

### cdd_feature.py - 项目管理

**用途**：项目初始化和特性管理
```bash
# 初始化新项目
python scripts/cdd_feature.py deploy "项目名称" --target /path/to/project

# 创建新特性
python scripts/cdd_feature.py create "特性名称" --description "特性描述"

# 列出所有特性
python scripts/cdd_feature.py list --target /path/to/project
```

### cdd_auditor.py - 宪法审计

**用途**：运行门禁审计
```bash
# 运行所有Gate
python scripts/cdd_auditor.py --gate all

# 运行特定Gate
python scripts/cdd_auditor.py --gate 1    # 版本一致性
python scripts/cdd_auditor.py --gate 2    # 行为验证
python scripts/cdd_auditor.py --gate 3    # 熵值检查
python scripts/cdd_auditor.py --gate 4    # 语义审计
python scripts/cdd_auditor.py --gate 5    # 宪法引用完整性

# 自动修复
python scripts/cdd_auditor.py --gate 1 --fix

# 详细输出
python scripts/cdd_auditor.py --gate all --verbose

# JSON格式输出
python scripts/cdd_auditor.py --gate all --format json
```

### cdd_entropy.py - 熵值管理

**用途**：计算、分析和优化熵值
```bash
# 计算当前熵值
python scripts/cdd_entropy.py calculate

# 分析熵值热点
python scripts/cdd_entropy.py analyze

# 获取优化建议（模拟运行）
python scripts/cdd_entropy.py optimize --dry-run

# 执行优化
python scripts/cdd_entropy.py optimize

# JSON格式输出
python scripts/cdd_entropy.py calculate --format json

# 强制重新计算（忽略缓存）
python scripts/cdd_entropy.py calculate --force
```

### cdd_claude_bridge.py - Claude Code集成

**用途**：Claude Code环境集成桥梁
```bash
# 检查桥接器状态
python scripts/cdd_claude_bridge.py --status

# 列出可用工具
python scripts/cdd_claude_bridge.py --list-tools

# 调用工具
python scripts/cdd_claude_bridge.py --call cdd_audit --args '{"gates": "all"}'
```

### cdd_diagnose.py - 综合诊断工具

**用途**：运行所有CDD检查的综合诊断，包括环境、技能完整性、宪法审计等
```bash
# 基本诊断
python scripts/cdd_diagnose.py

# 尝试自动修复问题
python scripts/cdd_diagnose.py --fix

# 仅显示摘要
python scripts/cdd_diagnose.py --summary

# JSON格式输出
python scripts/cdd_diagnose.py --json

# 诊断外部项目
python scripts/cdd_diagnose.py --target /path/to/project

# 详细输出模式
python scripts/cdd_diagnose.py --verbose
```

**检查内容包括**：
1. ✅ 环境依赖检查（cdd_check_env.py）
2. ✅ 技能完整性验证（cdd_verify.py）
3. ✅ 宪法审计（Gate 1-5）（cdd_auditor.py）
4. ✅ 系统熵值计算（cdd_entropy.py）
5. ✅ Claude Code桥接状态（cdd_claude_bridge.py）
6. ✅ 特性管理功能（cdd_feature.py）

**宪法依据**：§100.3, §101, §102, §106.1

---

## 错误代码参考

| 代码 | 名称 | 宪法依据 | 症状 | 解决方案 |
|------|------|----------|------|----------|
| **C001** | 熵值超标 | §102 | H_sys > 0.7 | 执行熵值优化 |
| **C002** | 文档不同步 | §101 | 代码与文档不一致 | 更新memory_bank/ |
| **C003** | 孢子隔离违例 | §106.1 | 在CDD目录中运行工具 | 在项目目录调用工具 |
| **C004** | 工作流状态无效 | §102 | 状态转换违反规则 | 检查active_context.md |
| **C005** | Spec未批准 | §104 | 在State B编码 | 等待用户批准 |
| **C006** | Gate审计失败 | §300.3 | Gate检查失败 | 运行详细审计找出问题 |

### 详细错误处理

#### C001：熵值超标
```bash
# 1. 分析熵值热点
python scripts/cdd_entropy.py analyze

# 2. 生成优化建议
python scripts/cdd_entropy.py optimize --dry-run

# 3. 执行优化
python scripts/cdd_entropy.py optimize

# 4. 验证结果
python scripts/cdd_entropy.py calculate
```

#### C003：孢子隔离违例
**错误示例**：
```bash
cd /path/to/cdd
python scripts/cdd_feature.py deploy "Test"  # ❌ 错误
```

**正确做法**：
```bash
cd /path/to/your/project
python /path/to/cdd/scripts/cdd_feature.py deploy "Test"  # ✅ 正确
```

---

## 故障排除

### 常见问题

<details>
<summary><b>安装问题</b></summary>

#### 1. ModuleNotFoundError: No module named 'pytest'
```bash
# 自动修复
python scripts/cdd_check_env.py --fix

# 或手动安装
pip install pytest pyyaml
```

#### 2. 权限问题
```bash
# 确保有执行权限
chmod +x scripts/*.py

# 或使用Python显式调用
python3 scripts/cdd_check_env.py
```
</details>

<details>
<summary><b>运行问题</b></summary>

#### 1. Gate 1失败：版本不一致
```bash
# 自动修复
python scripts/cdd_auditor.py --gate 1 --fix

# 手动检查
python scripts/cdd_auditor.py --gate 1 --verbose
```

#### 2. Gate 2失败：测试失败
```bash
# 运行测试查看详细错误
pytest tests/ -v

# 修复失败的测试后重新运行
python scripts/cdd_auditor.py --gate 2
```

#### 3. Gate 4失败：宪法引用覆盖率不足
```bash
# 查看缺失的宪法引用
python scripts/cdd_auditor.py --gate 4 --verbose

# 在相关文档中添加缺失的宪法引用
```
</details>

<details>
<summary><b>性能问题</b></summary>

#### 1. 熵值计算缓慢
```bash
# 使用缓存
python scripts/cdd_entropy.py calculate

# 清除缓存重新计算
python scripts/cdd_entropy.py calculate --force
```

#### 2. 审计时间过长
```bash
# 只运行必要的Gate
python scripts/cdd_auditor.py --gate 3  # 仅检查熵值

# 或分阶段运行
python scripts/cdd_auditor.py --gate 1
python scripts/cdd_auditor.py --gate 2
```
</details>

### 调试技巧

#### 启用详细日志
```bash
# 所有工具都支持--verbose参数
python scripts/cdd_auditor.py --gate all --verbose
python scripts/cdd_entropy.py calculate --verbose
```

#### 生成JSON报告
```bash
# 生成机器可读的报告
python scripts/cdd_auditor.py --gate all --format json > audit_report.json
python scripts/cdd_entropy.py calculate --format json > entropy_report.json
```

#### 检查系统状态
```bash
# 查看当前工作流状态
cat memory_bank/t0_core/active_context.md | grep -A5 "系统状态概览"

# 检查熵值历史
find memory_bank/ -name "*entropy*" -type f
```

---

## 高级主题

### 自定义宪法条款

CDD支持自定义宪法条款扩展：

```python
# 在项目中创建 custom_constitution.py
from core.constitution_core import ConstitutionArticle

CUSTOM_ARTICLES = {
    "§500": ConstitutionArticle(
        section="§500",
        name="项目特定规则",
        category="custom",
        description="本项目特定的开发规则",
        usage="项目内部约定"
    )
}

# 在文档中引用
# 宪法依据: §101§102§300.3
```

### 集成CI/CD流水线

在GitHub Actions中的示例配置：

```yaml
name: CDD Constitution Audit
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install CDD
        run: |
          git clone https://github.com/wsman/Constitution-Driven-Development-Skill.git cdd
          cd cdd
          pip install -r requirements.txt
      - name: Run Constitution Audit
        run: |
          python cdd/scripts/cdd_auditor.py --gate all
```

### 扩展CDD工具链

创建自定义工具：

```python
#!/usr/bin/env python3
"""
custom_tool.py - 自定义CDD工具示例
"""
import sys
from pathlib import Path

# 添加CDD技能库到路径
cdd_path = Path(__file__).parent.parent / "cdd"
sys.path.insert(0, str(cdd_path))

from core.constants import *
from utils.spore_utils import check_spore_isolation

def main():
    # 检查孢子隔离
    if not check_spore_isolation(Path.cwd()):
        print("❌ 孢子隔离违例: 请在项目目录中运行此工具")
        sys.exit(1)
    
    # 自定义逻辑...
    print("✅ 自定义工具运行成功")

if __name__ == "__main__":
    main()
```

---

## 开发者指南

### 项目结构

```
cdd/
├── core/                    # 核心服务层
│   ├── __init__.py
│   ├── audit_service.py    # 审计服务（Gate 1-5）
│   ├── constants.py        # 全局常量（熵值公式等）
│   ├── constitution_core.py # 宪法核心条款（62条）
│   ├── entropy_service.py  # 熵值服务
│   ├── exceptions.py       # 异常定义
│   ├── feature_service.py  # 特性管理服务
│   ├── state_transition_service.py  # 状态转换服务
│   └── state_validation_service.py  # 状态验证服务
├── scripts/                # CLI工具层（用户入口）
│   ├── cdd_auditor.py     # 宪法审计工具
│   ├── cdd_check_env.py   # 环境检查工具
│   ├── cdd_claude_bridge.py # Claude Code集成
│   ├── cdd_entropy.py     # 熵值管理工具
│   ├── cdd_feature.py     # 项目管理工具
│   ├── cdd_utils.py       # 工具辅助函数
│   └── cdd_verify.py      # 技能验证工具
├── utils/                 # 工具函数库
│   ├── cache_manager.py   # 缓存管理
│   ├── entropy_utils.py   # 熵值计算工具
│   ├── file_utils.py      # 文件操作工具
│   ├── logger.py          # 日志工具
│   ├── spore_utils.py     # 孢子隔离检查
│   └── version_utils.py   # 版本管理工具
├── templates/             # 项目模板
│   ├── cdd_config.yaml    # CDD配置文件模板
│   ├── constitution_references.py  # 宪法引用模板
│   ├── t0_core/           # T0核心层模板
│   ├── t1_axioms/         # T1公理层模板
│   ├── t2_protocols/      # T2协议层模板
│   ├── t2_standards/      # T2标准层模板
│   └── t3_documentation/  # T3文档层模板
├── claude/                # Claude Code集成
│   ├── README.md          # Claude Code使用指南
│   ├── config.yaml        # Claude配置
│   ├── hooks.yaml         # 钩子配置
│   ├── mcp_config.yaml    # MCP服务器配置
│   ├── slash_commands.yaml # 斜杠命令配置
│   ├── workflows.yaml     # 工作流配置
│   ├── skills/            # Claude技能定义
│   └── tools/             # Claude工具定义
├── examples/              # 示例项目
│   └── hello-cdd/         # Hello CDD示例
├── tests/                 # 测试套件
├── README.md              # 用户指南（本文档）
├── SKILL.md               # AI代理指令
├── reference.md           # 参考手册（当前文件）
└── requirements.txt       # Python依赖
```

### 核心服务交互图

```
用户 → CLI工具（scripts/） → 核心服务（core/） → 工具函数（utils/）
          ↓                       ↓                     ↓
     项目目录                宪法条款定义          文件操作/缓存
```

### 开发准则

1. **遵循宪法**：所有变更必须引用相关宪法条款
2. **熵值优先**：新功能不应显著增加系统熵值
3. **文档同步**：代码变更必须伴随文档更新
4. **测试覆盖**：新功能需有相应测试
5. **向后兼容**：API变更需考虑现有用户

### 贡献流程

1. **Fork仓库**：创建个人分支
2. **创建特性**：使用CDD工作流开发新功能
3. **运行审计**：确保所有Gate通过
4. **提交PR**：包含清晰的变更说明
5. **等待审查**：维护者将进行宪法审计

### 测试策略

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试模块
pytest tests/test_cdd_audit.py -v

# 生成测试覆盖率报告
pytest tests/ --cov=core --cov-report=html

# 运行性能测试
pytest tests/ --benchmark-only
```

---

## 架构设计详解

CDD技能库采用控制论架构设计，遵循§148（控制论架构公理）。本文档面向开发者、贡献者和需要深入了解CDD工作原理的技术人员。

### 🏗️ 整体架构

#### 架构层次图

```
┌─────────────────────────────────────────────┐
│            用户界面层 (UI Layer)             │
│  ┌───────────────────────────────────────┐  │
│  │   CLI工具层 (scripts/)                │  │
│  │  • cdd_auditor.py                     │  │
│  │  • cdd_check_env.py                   │  │
│  │  • cdd_feature.py                     │  │
│  │  • cdd_entropy.py                     │  │
│  │  • cdd_verify.py                      │  │
│  │  • cdd_claude_bridge.py               │  │
│  │  • cdd_diagnose.py                    │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│          核心服务层 (Core Layer)             │
│  ┌───────────────────────────────────────┐  │
│  │  核心服务 (core/)                     │  │
│  │  • audit_service.py      - Gate 1-5审计 │
│  │  • entropy_service.py    - 熵值计算服务 │
│  │  • feature_service.py    - 特性管理服务 │
│  │  • state_transition_service.py - 状态转换│
│  │  • state_validation_service.py - 状态验证│
│  │  • constitution_core.py  - 宪法条款定义 │
│  │  • constants.py          - 全局常量定义 │
│  │  • exceptions.py         - 异常类定义   │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│          工具函数层 (Utility Layer)          │
│  ┌───────────────────────────────────────┐  │
│  │  工具函数 (utils/)                    │  │
│  │  • spore_utils.py      - 孢子隔离检查 │
│  │  • entropy_utils.py    - 熵值计算函数 │
│  │  • file_utils.py       - 文件操作函数 │
│  │  • cache_manager.py    - 缓存管理     │
│  │  • logger.py           - 日志记录     │
│  │  • version_utils.py    - 版本管理     │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│          数据持久层 (Persistence Layer)      │
│  ┌───────────────────────────────────────┐  │
│  │  文件系统                            │  │
│  │  • .entropy_cache/    - 熵值缓存目录 │
│  │  • .cdd_state.json    - CDD状态文件  │
│  │  • 项目文件结构                      │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

#### 控制论架构集成

CDD采用三层控制论架构，与代码架构对应：

| 控制论层次 | 对应代码组件 | 职责 |
|------------|--------------|------|
| **治理层 (Governance)** | `core/constitution_core.py` | 定义宪法规则和约束 |
| **控制层 (Control)** | `core/audit_service.py`, `core/entropy_service.py` | 执行审计、验证、熵值监控 |
| **执行层 (Execution)** | `scripts/` 工具, `core/feature_service.py` | 执行具体开发任务 |

### 🔧 核心服务详解

#### 1. Audit Service (`core/audit_service.py`)

**职责**: 执行5门禁宪法审计

**关键组件**：
- `CDDAuditor` 类：主审计器，执行Gate 1-5
- `VersionChecker` 类：Gate 1版本一致性检查
- `AuditService` 类：服务接口，供CLI工具调用

**审计流程**：
```python
# 核心审计逻辑
auditor = CDDAuditor(project_root, verbose=True)
auditor.run_gate(1)  # 版本一致性检查
auditor.run_gate(2)  # 行为验证（测试）
auditor.run_gate(3)  # 熵值监控
auditor.run_gate(4)  # 语义审计
auditor.run_gate(5)  # 宪法引用完整性检查
```

**Gate 4增强说明**：
审查报告中提到Gate 4的外部依赖问题已解决。现在Gate 4：
1. 动态加载所有宪法核心条款（62条）
2. 扫描所有Markdown文档中的引用
3. 计算覆盖率，要求达到80%
4. 提供缺失条款列表以便修复

#### 2. Entropy Service (`core/entropy_service.py`)

**职责**: 计算、分析和优化系统熵值

**关键组件**：
- `EntropyCalculator` 类：计算目录、接口、测试合规率
- `EntropyAnalyzer` 类：分析熵值热点
- `EntropyOptimizer` 类：生成和执行优化建议
- `EntropyService` 类：服务接口

**熵值计算逻辑**：
```python
# 合规视角熵值计算
compliance_score = W_DIR * C_dir + W_SIG * C_sig + W_TEST * C_test
h_sys = 1.0 - compliance_score

# 成分视角熵值计算（用于内部分析）
h_sys_component = 0.4 * h_cog + 0.3 * h_struct + 0.3 * h_align
```

**错误处理增强**：
已添加详细的错误信息和恢复建议，包括：
- 文件访问失败时的优雅降级
- pytest未安装时的友好提示
- 包含堆栈跟踪的verbose模式输出

#### 3. Feature Service (`core/feature_service.py`)

**职责**: 管理CDD项目特性生命周期

**功能**：
- 项目初始化（`deploy_project`）
- 特性创建（`create_feature`）
- 特性状态管理
- 模板渲染（处理占位符变量）

**模板变量处理**：
已创建详细的模板变量说明文档（`templates/TEMPLATE_VARIABLES.md`），包含：
- 9类共50+个占位符变量
- 变量解析机制（自动/用户/动态生成）
- 使用示例和故障排除

#### 4. Constitution Core (`core/constitution_core.py`)

**职责**: 定义和维护宪法条款

**内容**：
- 62个核心宪法条款，分为三类：
  - 基本法 (§100-§199)：治理框架
  - 技术法 (§200-§299)：实施标准  
  - 程序法 (§300-§399)：工作流程
- 条款搜索和查询功能
- 自定义条款扩展接口

### 🛠️ 工具函数层详解

#### 1. Spore Utils (`utils/spore_utils.py`)

**孢子隔离协议实现**：
```python
def check_spore_isolation(target_path: Path, tool_name: str = "", allow_skill_root: bool = False) -> Tuple[bool, str]:
    """
    检查工具是否在正确的目录中运行
    
    规则：S_tool ∩ S_target = ∅ (工具目录与目标目录无交集)
    
    Args:
        target_path: 目标项目路径
        tool_name: 工具名称（用于错误消息）
        allow_skill_root: 是否允许在CDD技能库自身运行
    
    Returns:
        Tuple[是否通过, 错误消息]
    """
```

**用途**：防止意外修改CDD技能库自身

#### 2. Entropy Utils (`utils/entropy_utils.py`)

**熵值计算辅助函数**：
- `calculate_simple_entropy()`: 简化的熵值计算
- `find_entropy_hotspots()`: 识别熵值热点
- `quick_entropy_estimate()`: 快速熵值估算

#### 3. Cache Manager (`utils/cache_manager.py`)

**缓存管理**：
- 熵值计算结果缓存
- 宪法审计结果缓存
- 模板渲染结果缓存

**缓存策略**：基于文件修改时间自动失效

### 🔄 数据流与交互

#### 典型工作流：创建新特性

```
用户 → cdd_feature.py → FeatureService → 模板引擎 → 文件系统
      ↓
     验证结果 → 用户反馈
```

#### 典型工作流：运行宪法审计

```
用户 → cdd_auditor.py → AuditService → CDDAuditor → Gate 1-5
      ↓
     审计报告 → 用户反馈
```

#### 错误处理流程

```
异常抛出 → 异常类包装 → 用户友好消息 → 恢复建议
```

### 🚀 性能优化

#### 缓存策略
1. **熵值计算缓存**：结果存储在 `.entropy_cache/` 目录
2. **宪法审计缓存**：Gate检查结果缓存
3. **模板渲染缓存**：已渲染的模板缓存

#### 并发处理
- 工具设计为无状态，可并发执行
- 文件操作使用原子性操作
- 避免全局状态，使用依赖注入

#### 资源管理
- 大文件使用流式处理
- 内存使用监控和限制
- 超时处理机制

### 🔌 外部集成

#### 1. Claude Code集成

**桥梁架构**：
```
Claude Code → cdd_claude_bridge.py → 核心服务 → 执行操作
```

**MCP服务器配置**：
- `cdd-audit`: 审计服务MCP服务器
- `cdd-feature`: 特性管理MCP服务器  
- `cdd-entropy`: 熵值管理MCP服务器

**斜杠命令**：8个预定义斜杠命令，详见 `claude/README.md`

#### 2. 自定义扩展

**宪法条款扩展**：
```python
# 在项目中创建 custom_constitution.py
from core.constitution_core import ConstitutionArticle

CUSTOM_ARTICLES = {
    "§309": ConstitutionArticle(...)
}
```

**工具扩展**：
```python
# 创建自定义工具
from utils.spore_utils import check_spore_isolation
from core.constants import *
```

### 🧪 测试架构

#### 测试层次
```
单元测试 (Unit Tests) → 集成测试 (Integration Tests) → 端到端测试 (E2E Tests)
```

#### 测试覆盖
| 模块 | 测试文件 | 覆盖率目标 |
|------|----------|------------|
| `core/` | `tests/test_*.py` | ≥ 80% |
| `scripts/` | 功能测试 | ≥ 70% |
| `utils/` | `tests/test_*.py` | ≥ 85% |

#### 测试数据管理
- 使用临时目录进行文件操作测试
- 模拟外部依赖（pytest等）
- 测试环境隔离

### 📊 监控与日志

#### 日志级别
| 级别 | 用途 | 示例 |
|------|------|------|
| DEBUG | 详细调试信息 | 文件读取、变量解析 |
| INFO | 正常操作信息 | 特性创建成功、Gate通过 |
| WARNING | 潜在问题 | 熵值接近阈值、可选依赖缺失 |
| ERROR | 操作失败 | 文件访问失败、宪法违例 |
| CRITICAL | 系统级错误 | 内存不足、磁盘空间不足 |

#### 监控指标
1. **性能指标**：
   - 工具执行时间
   - 内存使用峰值
   - 文件操作次数

2. **质量指标**：
   - 系统熵值 (H_sys)
   - 宪法覆盖率
   - 测试通过率

3. **使用指标**：
   - 工具调用频率
   - 常见错误类型
   - 用户反馈评分

### 🔒 安全架构

#### 1. 孢子隔离协议

**核心原则**：`S_tool ∩ S_target = ∅`

**实现**：
- 工具运行时检查当前目录
- 防止在CDD技能库目录中运行项目工具
- 允许的例外情况（如技能验证）

#### 2. 输入验证

**文件路径验证**：
- 路径规范化
- 符号链接解析
- 权限检查

**模板变量验证**：
- 变量名称白名单
- 内容转义
- 大小限制

#### 3. 权限管理

**最小权限原则**：
- 只读取必要的文件
- 只写入指定的目录
- 使用临时文件进行中间处理

### 🚧 维护指南

#### 代码质量标准
1. **宪法一致性**：所有变更必须引用宪法条款
2. **测试覆盖**：新功能必须有相应测试
3. **文档同步**：代码变更必须更新相关文档
4. **向后兼容**：API变更需考虑现有用户

#### 依赖管理
**核心依赖**：
- Python 3.8+
- pytest ≥ 6.0
- PyYAML ≥ 6.0

**可选依赖**：
- tree命令（目录可视化）
- git（版本控制）
- DeepSeek API（Gate 4外部审计）

### 🆘 故障排除

#### 常见架构问题

**问题1：导入错误**
**症状**：`ImportError: cannot import name '...'`
**原因**：循环依赖或路径问题
**解决方案**：
1. 检查 `__init__.py` 文件
2. 验证Python路径设置
3. 使用绝对导入

**问题2：性能瓶颈**
**症状**：工具执行缓慢
**原因**：文件扫描过多或缓存失效
**解决方案**：
1. 启用缓存
2. 限制扫描深度
3. 使用更高效的算法

**问题3：内存泄漏**
**症状**：内存使用持续增长
**原因**：资源未正确释放
**解决方案**：
1. 使用上下文管理器
2. 及时关闭文件句柄
3. 限制大文件处理

### 🔮 未来扩展

#### 计划中的功能
1. **分布式审计**：支持多项目并行审计
2. **机器学习集成**：智能熵值预测
3. **可视化仪表板**：Web界面监控
4. **插件系统**：第三方扩展支持

#### 架构演进方向
1. **微服务架构**：将核心服务拆分为独立服务
2. **事件驱动**：基于事件的架构设计
3. **容器化**：Docker容器支持
4. **云原生**：Kubernetes部署支持

---

## 附录

### A. 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v2.0.0 | 2026-02 | 核心服务重构，Claude Code集成 |
| v1.6.0 | 2026-01 | 控制论架构，三级验证体系 |
| v1.0.0 | 2025-12 | 初始版本发布 |

### B. 相关资源

- **GitHub仓库**：https://github.com/wsman/Constitution-Driven-Development-Skill
- **问题跟踪**：https://github.com/wsman/Constitution-Driven-Development-Skill/issues
- **讨论区**：https://github.com/wsman/Constitution-Driven-Development-Skill/discussions

### C. 许可证信息

基于 Apache License 2.0 授权。详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**📚 宪法驱动开发 - 让AI辅助开发变得可控、可预测、可持续**

</div>