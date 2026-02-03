# CDD工具与模板综合使用手册

## 🏛️ 第一部分：CDD工具链架构

### 1.1 工具分类：元工具 vs 交付工具

CDD SKILL 项目中的脚本根据作用对象分为两类：**元工具**（用于CDD SKILL自身开发）和**交付工具**（用于用户项目开发）。

#### 元工具 (Meta-Tools) - 仅用于CDD SKILL自身开发

| 脚本名称 | 作用对象 | 设计目的 |
|----------|----------|----------|
| `cdd_audit.py` | CDD SKILL技能库自身 | 确保CDD SKILL这个"产品"本身的质量和宪法合规性 |
| `Makefile` | CDD SKILL技能库自身 | CDD Local Development Interface（本地开发接口） |

#### 交付工具 (Delivery Tools) - 可在用户项目中运行

| 脚本名称 | 参数支持 | 设计目的 |
|----------|----------|----------|
| `cdd-feature.py` (v2.1+) | `--target` (默认: 当前目录) | 特性脚手架，在目标项目中生成特性文档 |
| `measure_entropy.py` | `--project` (默认: 当前目录) | 熵值计算器，测量目标项目的系统熵值 |
| `verify_versions.py` | `--project` (默认: 当前目录) | 版本一致性检查器，验证目标项目的版本一致性 |
| `deploy_cdd.py` | `--target` (默认: 当前目录) | 部署工具，从CDD SKILL复制模板到目标项目 |

### 1.2 各工具详细说明

#### 1.2.1 `cdd_audit.py` - 宪法审计器

**作用对象**: CDD SKILL技能库自身  
**设计目的**: 确保CDD SKILL这个"产品"本身的质量和宪法合规性  

**强制绑定机制**:
1. **工作目录锁定 (CWD Locking)**:
   - 硬编码 `PROJECT_ROOT`，所有子命令强制在CDD技能根目录执行
2. **参数传递截断**:
   - 不传递外部"目标路径"参数给子脚本，仅传递 `--fix` 或 `-v` 参数

**使用场景**:
```bash
# 仅在CDD SKILL目录内运行
python scripts/cdd_audit.py --gate all --format json
```

#### 1.2.2 `Makefile` - 本地开发接口

**作用对象**: CDD SKILL技能库自身  
**设计意图**: "CDD Local Development Interface"

**硬编码调用**:
```makefile
audit:
	python scripts/cdd_audit.py --gate 1
gate2:
	python scripts/cdd_audit.py --gate 2
```

#### 1.2.3 `cdd-feature.py` (v2.1) - 特性脚手架

**重构改进**:
- **SKILL_ROOT**: `Path(__file__).resolve().parent.parent` (模板源)
- **TARGET_ROOT**: `Path(args.target).resolve()` (生成目标)
- **新增 `--target` 参数**: 指定目标项目路径

**使用场景**:
```bash
# 在CDD SKILL目录内运行 (向后兼容)
python scripts/cdd-feature.py "test-feature" "描述"

# 在外部项目中运行 (新功能)
python /path/to/skill/scripts/cdd-feature.py "登录功能" --target /path/to/project
```

#### 1.2.4 `measure_entropy.py` - 熵值计算器

**参数支持**: `--project` (默认: 当前目录)  
**使用场景**:
```bash
# 在任何CDD项目中运行
python scripts/measure_entropy.py --project /path/to/project --json
```

#### 1.2.5 `verify_versions.py` - 版本一致性检查器

**参数支持**: `--project` (默认: 当前目录)  
**使用场景**:
```bash
# 在任何CDD项目中运行
python scripts/verify_versions.py --project /path/to/project --fix
```

#### 1.2.6 `deploy_cdd.py` - 部署工具

**路径模式**: 混合  
- **读取**: 从CDD SKILL的 `templates/` 目录读取模板
- **写入**: 向目标项目的 `memory_bank/` 目录写入文件

**使用场景**:
```bash
# 部署CDD结构到目标项目
python scripts/deploy_cdd.py "我的项目" --target /path/to/project
```

### 1.3 架构优势

#### 1. 清晰的职责分离
- **元工具**: 确保"产品"(CDD SKILL)的质量
- **交付工具**: 帮助用户应用CDD到自己的项目

#### 2. 工具开发与工具使用分离
- CDD技能库自身使用一套工具（元工具）来保证质量
- 用户使用另一套工具（交付工具）来应用CDD

#### 3. 更好的可移植性
- 交付工具都设计为可跨项目运行
- 通过参数明确指定目标路径，避免隐式依赖

## 📄 第二部分：CDD模板系统

### 2.1 核心模板介绍

CDD 提供了标准化的文档模板以降低认知负载。

#### DS-050 Feature Specification (特性规范)
- **用途**: 定义"做什么"和"为什么做"
- **必填内容**: 用户故事、验收标准
- **标准结构**:
  1. 宪法合规性检查 (引用 systemPatterns/techContext)
  2. 用户场景与测试 (P1/P2/P3 用户故事)
  3. 功能/非功能需求
  4. 数据模型变更
  5. 接口定义
  6. 验证计划 (Tier 1/2/3)

#### DS-051 Implementation Plan (实施计划)
- **用途**: 定义"怎么做"
- **必填内容**: 阶段划分、技术决策
- **标准结构**:
  1. 实施摘要与核心技术决策
  2. 技术上下文 (语言/依赖/存储/测试)
  3. 三级验证准备
  4. 实施步骤 (Step 1/2/3...)
  5. 回滚计划
  6. 验收标准
  7. 里程碑

#### DS-052 Atomic Tasks (原子任务)
- **用途**: 任务分解
- **必填内容**: Checkbox 列表

### 2.2 模板实例化指南

**重要原则**: 使用 `scripts/cdd-feature.py` 自动实例化这些模板。**不要手动复制粘贴**。

#### 实例化工具
```bash
# 自动实例化模板
python scripts/cdd-feature.py "Feature Name" "Description"
```

#### 模板层级对应
- **T0**: 宪法核心层 - `core/` 目录下的模板
- **T1**: 系统公理层 - `axioms/` 目录下的模板  
- **T2**: 执行标准层 - `standards/` 目录下的模板
- **T3**: 归档层 - 历史记录和审计数据

### 2.3 相关模板索引

#### 执行标准模板
- **`standards/DS-050_feature_specification.md`** - 特性规范模板
- **`standards/DS-051_implementation_plan.md`** - 实施计划模板
- **`standards/DS-052_atomic_tasks.md`** - 原子任务模板
- **`standards/feature_readme_template.md`** - 特性README模板

#### 使用说明
1. **阅读顺序**: 先阅读本概念文件，再查阅相关模板
2. **模板实例化**: 使用 `cdd-feature.py` 自动生成具体实现
3. **层级对应**: 这些模板对应T0-T3文档体系的不同层级

## 🛠️ 第三部分：综合工作流程

### 3.1 新项目初始化流程

#### 步骤1：部署CDD结构到目标项目
```bash
python /path/to/cdd/scripts/deploy_cdd.py "我的项目" --target /path/to/project
```

#### 步骤2：在目标项目中生成特性文档
```bash
python /path/to/cdd/scripts/cdd-feature.py "用户登录" --target /path/to/project
```

#### 步骤3：监控项目健康
```bash
# 在目标项目目录中运行
cd /path/to/project && python /path/to/cdd/scripts/measure_entropy.py --json

# 验证版本一致性
cd /path/to/project && python /path/to/cdd/scripts/verify_versions.py --fix
```

### 3.2 CDD技能库开发流程

#### 步骤1：本地开发（使用元工具）
```bash
# 运行Makefile命令
make audit     # 执行Gate 1审计
make gate2     # 执行Gate 2审计
make clean     # 清理临时文件
```

#### 步骤2：合规审计
```bash
# 运行完整审计
python scripts/cdd_audit.py --gate all --format json

# 修复版本问题
python scripts/cdd_audit.py --fix
```

### 3.3 完整开发流程示例

#### 场景：实现支付模块
```bash
# 1. 生成特性规范 (State B)
python scripts/cdd-feature.py "支付模块" "支持支付宝和微信支付"

# 2. 等待用户审批
# ... 用户审查生成的DS-050/DS-051文档 ...

# 3. 执行实现 (State C)
# 按照DS-052原子任务列表逐步实现

# 4. 三级验证 (State D)
# - Tier 1: 结构验证 (文件结构一致性)
# - Tier 2: 签名验证 (接口一致性)  
# - Tier 3: 行为验证 (业务逻辑一致性)

# 5. 收敛与优化 (State E)
# 确保系统熵值 $H_{sys} \leq 0.3$
```

## 📖 第四部分：使用建议与最佳实践

### 4.1 重要提醒

#### 元工具使用边界
- **`cdd_audit` 仅用于审计CDD技能库自身**，若需审计您的业务项目，请直接在项目根目录使用 `measure_entropy.py` 和 `verify_versions.py`
- **`Makefile` 是CDD技能库的本地开发接口**，不应在用户项目中运行

#### 交付工具使用原则
1. **明确指定目标路径**: 始终使用 `--target` 或 `--project` 参数
2. **保持向后兼容**: 在不指定参数时，默认在当前目录运行
3. **分离数据与逻辑**: SKILL_ROOT存放工具逻辑，TARGET_ROOT存放用户数据

### 4.2 常见场景指南

#### 场景A：开发CDD技能库本身
1. 在CDD技能目录内工作
2. 使用所有脚本（包括元工具）
3. 运行 `make audit` 或 `python scripts/cdd_audit.py` 确保合规

#### 场景B：在业务项目中应用CDD
1. 使用 `deploy_cdd.py` 部署CDD结构
2. 使用 `cdd-feature.py --target` 生成文档
3. 使用 `measure_entropy.py` 和 `verify_versions.py` 监控项目

#### 场景C：团队协作与审计
1. 确保所有成员理解元工具与交付工具的区别
2. 建立清晰的工具使用规范
3. 定期审计项目健康度

### 4.3 错误处理与调试

#### 常见错误
1. **错误使用元工具**: 在用户项目中运行 `cdd_audit.py`
2. **缺少参数**: 忘记指定 `--target` 或 `--project` 参数
3. **路径问题**: 使用相对路径而非绝对路径

#### 调试建议
1. **检查当前目录**: `pwd` 确认工作目录
2. **验证参数**: 使用 `--help` 查看工具参数
3. **检查权限**: 确保有读写目标目录的权限

## 附录：命令快速参考

### 元工具命令
```bash
# CDD技能库自身审计
make audit                    # 执行Gate 1审计
python scripts/cdd_audit.py --gate all --format json  # 完整审计
python scripts/cdd_audit.py --fix                     # 修复版本问题
```

### 交付工具命令
```bash
# 部署CDD结构
python scripts/deploy_cdd.py "项目名" --target /path/to/project

# 生成特性文档
python scripts/cdd-feature.py "特性名" "描述" --target /path/to/project

# 项目监控
cd /path/to/project && python /path/to/cdd/scripts/measure_entropy.py --json
cd /path/to/project && python /path/to/cdd/scripts/verify_versions.py --fix
```

### 模板实例化
```bash
# 自动实例化所有T2模板
python scripts/cdd-feature.py "用户登录功能" "包括邮箱密码登录和第三方OAuth登录"
```

## 版本与状态

**最后更新**: 2026-02-03  
**文档版本**: v1.0.0  
**基于CDD宪法版本**: v1.6.1  
**状态**: 🟢 活跃  

---

*遵循宪法驱动开发：工具即接口，模板即契约，代码即证明。*