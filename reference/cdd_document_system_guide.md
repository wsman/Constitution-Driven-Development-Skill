# CDD文档体系与使用指南 (T0-T3 System)

## 🏛️ Part 1: 文档分类体系 (Theory)

### 1.1 四级文档体系概述

The CDD framework uses a four-level document hierarchy (T0-T3) to optimize AI context management and system entropy reduction. This hierarchy implements the **"Cognitive Load Optimization"** principle, ensuring AI agents load only the necessary context for each task.

#### Core Principle
$$
\text{Attention}(T0) \gg \text{Attention}(T1) > \text{Attention}(T2) \gg \text{Attention}(T3)
$$

**Token Allocation Targets**:
- **T0**: <800 tokens (always loaded)
- **T1**: <200 tokens (loaded on demand)
- **T2**: <100 tokens per file (lazy loaded)
- **T3**: 0 tokens (audit-only)

### 1.2 T0: Constitutional Core (Mandatory Load)

The **"consciousness layer"** - defines who we are and our current state.

#### Core Documents
- **`templates/core/active_context.md`**: Current focus, task state, and entropy metrics. READ THIS FIRST.
- **`templates/core/knowledge_graph.md`**: Navigation map with Mermaid visualizations.
- **Law Indices**: Basic, Procedural, and Technical law indices.

#### Loading Rules
1. **Boot Sequence**: Load all 5 T0 documents on system start.
2. **Always Resident**: T0 documents must remain in AI context throughout development.
3. **State Tracking**: `active_context.md` records all architectural decisions and entropy states.

### 1.3 T1: System Axioms (On-Demand Load)

The **"physical laws"** - defines architectural constraints and technical signatures.

#### Core Documents
- **`templates/axioms/system_patterns.md`**: Architecture patterns and design constraints.
- **`templates/axioms/tech_context.md`**: Interface signatures and technical stack.
- **`templates/axioms/behavior_context.md`**: Behavioral assertions and test expectations.

#### Retrieval Strategy
- Load **only when** T0 cannot resolve a technical question.
- Use for: Architecture validation, interface design, behavior specification.
- Release after use to free context.

### 1.4 T2: Executable Standards (Lazy Load)

The **"legislative code"** - specific feature specifications and implementation plans.

#### Template System
- **DS-050**: Feature Specification ("what" and "why")
- **DS-051**: Implementation Plan ("how")
- **DS-052**: Atomic Tasks (checklist decomposition)

#### Instantiation Protocol
```bash
# Use cdd-feature.py for automatic instantiation
python scripts/cdd-feature.py "Feature Name" "Description"
```

**NEVER** create T2 documents manually. Always use the scaffolding tool to ensure:
1. Automatic numbering
2. Template consistency
3. Git branch creation
4. GitHub Issues synchronization

### 1.5 T3: Archives (Audit-Only Load)

The **"historical record"** - used for analysis, audit, and retrospectives.

#### Content Types
- Analysis reports and visualization data
- Historical versions and deprecated standards
- Entropy trend analysis and performance metrics

#### Access Protocol
- Load **only** during system audits or retrospectives.
- Read-only reference; never modify during active development.
- Supports cold storage to external systems.

### 1.6 宪法合规与熵值监控

#### Constitutional Compliance

##### Core Axioms
- **§102.3 Synchronization Axiom**: Code ↔ Document atomic synchronization
- **§201.5 Entropy Reduction Axiom**: All changes must decrease or maintain $H_{sys}$
- **Isomorphism Principle**: $S_{fs} \cong S_{doc}$ (filesystem ≈ documentation structure)

##### Three-Tier Verification
1. **Tier 1 (Structure)**: Verify $S_{fs} \cong S_{doc}$ against `system_patterns.md`
2. **Tier 2 (Signature)**: Verify $I_{code} \supseteq I_{doc}$ against `tech_context.md`
3. **Tier 3 (Behavior)**: Verify $B_{code} \equiv B_{spec}$ against `behavior_context.md`

#### Entropy Integration
The T0-T3 hierarchy directly impacts System Entropy ($H_{sys}$):
- **$H_{cog}$ (Cognitive Load)**: Minimized by proper tiered loading
- **$H_{struct}$ (Structural Entropy)**: Reduced by isomorphic mapping
- **$H_{align}$ (Alignment Deviation)**: Managed by signature verification

#### Performance Optimization
- **Index Lookup**: $O(1)$ complexity using law reference maps
- **Graph Navigation**: $O(\log k)$ complexity using knowledge graph
- **Context Switching**: <100ms for tier transitions

#### Retrieval Algorithm in CDD

##### Example: "How to create a new authentication feature?"
1. **T0 Analysis**: Read `active_context.md` → Check current architecture state
2. **T1 Loading**: If needed, load `system_patterns.md` for Auth module patterns
3. **T2 Instantiation**: Run `cdd-feature.py "Add User Auth" "..."`
4. **T2 Execution**: Implement according to generated DS-050/DS-051 specs
5. **T0 Update**: Update `active_context.md` with new architectural decision

##### Example: "Verify interface compliance?"
1. **T1 Loading**: Load `tech_context.md` for interface definitions
2. **Code Analysis**: Check implementation against T1 signatures
3. **Tier 2 Verification**: Run `cdd_audit.py --gate 2`

---

## 🛠️ Part 2: 模板使用指南 (Practice)

### 2.1 模型配置 (双模型架构)

CDD框架使用双模型架构：

| 用途 | 模型 | 配置文件位置 |
|------|------|--------------|
| **开发模型** | MiniMax-M2.1 | OpenClaw默认配置 |
| **审计模型** | DeepSeek-Reasoner | `cdd_config.yaml` |

#### cdd_config.yaml 配置示例

```yaml
external_auditor:
  model: "deepseek-reasoner"  # 外部审计模型
  api:
    base_url: "https://api.deepseek.com"
    api_key: "${DEEPSEEK_API_KEY}"
```

### 2.2 模板结构说明

```
cdd/templates/
├── core/                          # T0: 宪法核心层
│   ├── active_context.md          # 活动上下文模板
│   ├── basic_law_index.md         # 基本法索引
│   ├── procedural_law_index.md    # 程序法索引
│   ├── technical_law_index.md     # 技术法索引
│   ├── knowledge_graph.md         # 知识图谱模板
├── axioms/                        # T1: 系统公理层
│   ├── system_patterns.md         # 架构约束
│   ├── tech_context.md            # 接口约束
│   └── behavior_context.md        # 行为约束
├── protocols/                     # T1/T2: 工作流程
│   ├── WF-201_cdd_workflow.md     # CDD工作流
│   ├── WF-review.md               # 代码审查协议
│   ├── WF-amend.md                # 宪法修正案协议
│   └── WF-001_clarify_workflow.md # 需求澄清工作流
├── standards/                     # T2: 执行标准层
│   ├── DS-050_feature_specification.md  # 特性规范模板
│   ├── DS-051_implementation_plan.md    # 实施计划模板
│   ├── DS-052_atomic_tasks.md           # 原子任务模板
│   ├── DS-053_quality_checklist.md      # 质量检查清单
│   ├── DS-054_environment_hardening.md  # 环境强化标准
│   ├── DS-060_code_review.md            # 代码审查标准
│   └── feature_readme_template.md       # 特性README模板
└── cdd_config.yaml                # 配置文件
```

### 2.3 创建项目Memory Bank

在项目根目录创建 `memory_bank` 文件夹：

```bash
mkdir -p memory_bank/00_indices
mkdir -p memory_bank/01_active_state
mkdir -p memory_bank/02_systemaxioms
mkdir -p memory_bank/03_protocols/workflows
mkdir -p memory_bank/03_protocols/standards
```

#### 复制索引文件
将三个索引文件复制到 `memory_bank/00_indices/`：

```bash
cp templates/core/basic_law_index.md memory_bank/00_indices/
cp templates/core/procedural_law_index.md memory_bank/00_indices/
cp templates/core/technical_law_index.md memory_bank/00_indices/
```

#### ⭐ 创建项目README.md (项目背景文档)
**在项目根目录创建** `README.md`（与 `memory_bank/` 同级）：

```bash
cp reference/project_readme_template.md README.md
```

编辑 `README.md`，填入项目背景信息：
- 项目名称和描述
- 技术栈概览
- 核心功能列表
- 外部依赖说明

**注意**: README.md 不属于T0级别文档，是项目背景说明文档。

#### 创建活动上下文
复制模板到 `memory_bank/01_active_state/activeContext.md`：

```bash
cp templates/core/active_context.md memory_bank/01_active_state/activeContext.md
```

#### (可选) 创建知识图谱
复制模板到 `memory_bank/core/knowledge_graph.md`：

```bash
cp templates/core/knowledge_graph.md memory_bank/core/
```

#### (可选) 创建配置文件
复制配置文件到 `memory_bank/cdd_config.yaml`：

```bash
cp templates/cdd_config.yaml memory_bank/cdd_config.yaml
```

#### 配置外部审计者
编辑 `memory_bank/cdd_config.yaml`，配置 DeepSeek 深度推理模型：

```yaml
external_auditor:
  enabled: true
  model: "deepseek-reasoner"
  api:
    base_url: "https://api.deepseek.com"
    api_key: "${DEEPSEEK_API_KEY}"  # 或直接填入API密钥
```

### 2.4 开发流程 (State A-E)

#### 启动开发 (Bootloader Sequence)

1. **Phase 1: 引导输入** - 加载 `README.md`，提取项目背景注入 `activeContext.md`
2. **Phase 2: 内核加载** - 加载 5 个 T0 核心文档
3. **Phase 3: 熵值校准** - 计算 $H_{sys}$ (含 $H_{align}$ 检查)

**关于 README.md 的定位**:
- 角色: 引导加载器输入 (Bootloader Input)
- 生命周期: 仅在会话初始化阶段存在
- 作用: 为 `activeContext.md` 提供初始"世界观"，防止冷启动幻觉

#### 执行 CDD

1. **State A (基准摄入)** - 读取 systemPatterns/techContext/behaviorContext
2. **State B (文档规划)** - 先修改文档，等待用户批准
3. **State C (受控执行)** - 按文档执行代码修改
4. **State D (三级验证)** - Tier 1(结构) → Tier 2(签名) → Tier 3(行为)
5. **State E (收敛纠错)** - 确保 $H_{sys} \leq 0.3$

#### State B: Spec-Driven Planning 指令示例

使用 DS-050 和 DS-051 模板进行规范驱动的规划：

##### 1. 生成特性规范 (DS-050)

```bash
# 输入示例
python scripts/cdd-feature.py "用户登录功能" "包括邮箱密码登录和第三方OAuth登录"

# 系统将生成:
# specs/[###-user-login]/spec.md
# 基于 DS-050_feature_specification.md 模板
```

**DS-050 标准结构**:
```
1. 宪法合规性检查 (引用 systemPatterns/techContext)
2. 用户场景与测试 (P1/P2/P3 用户故事)
3. 功能/非功能需求
4. 数据模型变更
5. 接口定义
6. 验证计划 (Tier 1/2/3)
```

##### 2. 生成实施计划 (DS-051)

```bash
# 输入示例 (在规范批准后)
/cdd plan "用户登录" --spec="specs/[###-user-login]/spec.md"

# 系统将生成:
# specs/[###-user-login]/plan.md
# 基于 DS-051_IMPLEMENTATION_PLAN.md 模板
```

**DS-051 标准结构**:
```
1. 实施摘要与核心技术决策
2. 技术上下文 (语言/依赖/存储/测试)
3. 三级验证准备
4. 实施步骤 (Step 1/2/3...)
5. 回滚计划
6. 验收标准
7. 里程碑
```

##### 3. 审批流程

```bash
# 用户审批
/cdd approve "规范和计划已审查，同意实施"

// 或拒绝并要求修改
/cdd reject "需要补充OAuth流程的异常处理"
```

##### 4. 完整流程示例

```bash
# 1. 启动 State A
/cdd start "实现支付模块"

// 2. State B - 规范规划
/cdd analyze "支付模块需要支持支付宝和微信支付"
/cdd spec "支付模块"  # 生成 DS-050
/cdd plan "支付模块"  # 生成 DS-051

// 3. 用户审批
/cdd approve "通过"

// 4. State C - 执行
/cdd execute step-1  # 实现支付接口
/cdd execute step-2  # 实现支付宝适配器
/cdd execute step-3  # 实现微信支付适配器

// 5. State D - 验证
/cdd verify tier1  # 结构验证
/cdd verify tier2  # 签名验证
/cdd verify tier3  # 行为验证

// 6. State E - 收敛
/cdd calibrate
```

## 4. Toolchain Architecture (工具链架构)

CDD SKILL 的工具链根据 **作用域 (Scope)** 分为两类。理解这一区分对于防止误操作至关重要。

### 4.1 Meta-Tools (元工具)
* **代表脚本**: `scripts/cdd_audit.py`, `Makefile`
* **作用域**: **Local Only (仅限技能库本身)**
* **行为特征**: 
    * 硬编码锁定 `PROJECT_ROOT` 为脚本所在目录的父级。
    * 用于 CDD SKILL 的持续集成 (CI) 和自我进化。
    * **禁止**用于审计外部业务项目。

**强制绑定机制分析** (`cdd_audit.py`):
1. **工作目录锁定 (CWD Locking)**: 硬编码 `PROJECT_ROOT`，所有子命令强制在CDD技能根目录执行
2. **参数传递截断**: 不传递外部"目标路径"参数给子脚本，仅传递 `--fix` 或 `-v` 参数

#### 元工具详细说明

| 脚本名称 | 作用对象 | 设计目的 |
|----------|----------|----------|
| `cdd_audit.py` | CDD SKILL技能库自身 | 确保CDD SKILL这个"产品"本身的质量和宪法合规性 |
| `Makefile` | CDD SKILL技能库自身 | CDD Local Development Interface（本地开发接口） |

### 4.2 Delivery Tools (交付工具)
* **代表脚本**: `cdd-feature.py`, `measure_entropy.py`, `deploy_cdd.py`, `verify_versions.py`
* **作用域**: **Target Oriented (面向目标项目)**
* **行为特征**: 
    * 实现了逻辑 (Skill Root) 与数据 (Target Root) 的分离。
    * 必须通过 `--target` 或 `--project` 参数指定业务项目路径。
    * 若未指定参数，默认行为是操作当前目录（在开发 CDD SKILL 本身时使用），但在生产使用中应避免此情况。

#### 交付工具详细说明

| 脚本名称 | 参数支持 | 设计目的 |
|----------|----------|----------|
| `cdd-feature.py` (v2.1+) | `--target` (默认: 当前目录) | 特性脚手架，在目标项目中生成特性文档 |
| `measure_entropy.py` | `--project` (默认: 当前目录) | 熵值计算器，测量目标项目的系统熵值 |
| `verify_versions.py` | `--project` (默认: 当前目录) | 版本一致性检查器，验证目标项目的版本一致性 |
| `deploy_cdd.py` | `--target` (默认: 当前目录) | 部署工具，从CDD SKILL复制模板到目标项目 |

**重要提醒**:
- **`cdd_audit` 仅用于审计CDD技能库自身**，若需审计您的业务项目，请直接在项目根目录使用 `measure_entropy.py` 和 `verify_versions.py`
- **`Makefile` 是CDD技能库的本地开发接口**，不应在用户项目中运行

**使用示例**:
```bash
# 1. 部署CDD结构到用户项目
python /path/to/cdd/scripts/deploy_cdd.py "我的项目" --target /path/to/project

# 2. 在用户项目中生成特性文档
python /path/to/cdd/scripts/cdd-feature.py "用户登录" --target /path/to/project

# 3. 监控用户项目熵值
cd /path/to/project && python /path/to/cdd/scripts/measure_entropy.py --json

# 4. 验证用户项目版本一致性
cd /path/to/project && python /path/to/cdd/scripts/verify_versions.py --fix
```

### 4.3 Standard Workflow (标准工作流)

1.  **Step 0 (Pre-flight)**: 运行 `python scripts/cdd_audit.py` 确保工具链纯净 (Green Status)。
2.  **Step 1 (Action)**: 使用交付工具操作目标项目，例如：
    * `python scripts/cdd-feature.py "Payment" --target /path/to/my_app`

### 2.6 T1/T2 标准快速参考

| 标准ID | 名称 | 用途 | 使用场景 |
|--------|------|------|----------|
| systemPatterns.md | T1-架构约束 | Tier 1 验证依据 | 检查文件结构 |
| techContext.md | T1-接口约束 | Tier 2 验证依据 | 检查接口签名 |
| behaviorContext.md | T1-行为约束 | Tier 3 验证依据 | 检查业务逻辑 |
| DS-050 | 特性规范 | State B 输出 | 生成功能Spec |
| DS-051 | 实施计划 | State B 输出 | 生成实施Plan |
| DS-052 | 原子任务 | State C 输入 | 任务分解 |
| DS-053 | 质量清单 | State D 输入 | 质量检查 |
| DS-054 | 环境强化 | State E 输入 | 环境优化 |
| DS-060 | 代码审查 | State D 输入 | 代码评审 |

### 2.6 熵值监控与健康标准

#### 健康报告示例
```markdown
## System Health Report

| 指标 | 值 | 评分 |
|------|-----|------|
| $H_{sys}$ (系统熵) | 0.00 | 🟢 |
| $T_{load}$ (Token占用) | 0 / 8000 | 0% |
| $N_{linked}/N_{total}$ (关联度) | 0 / 0 | 0% |
| $F_{drift}/F_{total}$ (漂移率) | 0 / 0 | 0% |
```

#### 健康标准

| $H_{sys}$ 范围 | 状态 | 行动 |
|----------------|------|------|
| 0.0 - 0.3 | 🟢 优秀 | 保持现状 |
| 0.3 - 0.5 | 🟡 良好 | 关注负载 |
| 0.5 - 0.7 | 🟠 警告 | 优化结构 |
| 0.7 - 1.0 | 🔴 危险 | 立即整理 |

### 2.7 T0文档变更与外部审计

**当T0级别文档发生变更时：**

1. **变更检测** - 系统检测到T0文档变更
2. **外部审计触发** - 调用 deepseek-reasoner 进行审查
3. **生成审计报告** - 包含合规性检查、风险评估
4. **发送附件到频道** - ⭐ 将报告作为附件发送到 Discord
5. **用户确认** - 用户查看报告并确认/修正

**T0文档变更工作流：**
```
T0文档变更
    ↓
外部审计者触发 (deepseek-reasoner)
    ↓
T0文档合规性审查
    ↓
生成审计报告 (report_by_deepseek-reasoner_时间戳.md)
    ↓
⭐ 发送附件到 Discord (报告MD文件作为附件)
    ↓
用户确认/修正
```

---

## 🔗 Part 3: 相关模板索引

### 3.1 核心宪法模板 (T0)
- **`core/active_context.md`** - 活动上下文，系统当前状态
- **`core/basic_law_index.md`** - 基本法核心公理索引
- **`core/knowledge_graph.md`** - 知识图谱导航地图
- **`core/procedural_law_index.md`** - 程序法工作流索引
- **`core/technical_law_index.md`** - 技术法标准索引
- **`core/project_readme_template.md`** - 项目背景文档模板

### 3.2 系统公理模板 (T1)
- **`axioms/behavior_context.md`** - 行为约束和测试期望
- **`axioms/system_patterns.md`** - 架构模式和设计约束
- **`axioms/tech_context.md`** - 技术栈和接口签名

### 3.3 工作流程模板 (T1/T2)
- **`protocols/WF-201_cdd_workflow.md`** - CDD标准工作流
- **`protocols/WF-review.md`** - 代码审查协议
- **`protocols/WF-amend.md`** - 宪法修正案协议
- **`protocols/WF-001_clarify_workflow.md`** - 需求澄清工作流
- **`protocols/WF-analyze.md`** - 分析协议
- **`protocols/WF-sync-issues.md`** - GitHub Issues同步协议

### 3.4 执行标准模板 (T2)
- **`standards/DS-050_feature_specification.md`** - 特性规范模板
- **`standards/DS-051_implementation_plan.md`** - 实施计划模板
- **`standards/DS-052_atomic_tasks.md`** - 原子任务模板
- **`standards/DS-053_quality_checklist.md`** - 质量检查清单
- **`standards/DS-054_environment_hardening.md`** - 环境强化标准
- **`standards/DS-060_code_review.md`** - 代码审查标准
- **`standards/feature_readme_template.md`** - 特性README模板

### 3.5 配置文件
- **`cdd_config.yaml`** - CDD配置文件（外部审计者/API配置）

### 使用说明
1. **阅读顺序**: 先阅读本概念文件，再查阅相关模板
2. **模板实例化**: 使用 `cdd-feature.py` 自动生成具体实现
3. **层级对应**: 这些模板对应T0-T3文档体系的不同层级

---

**最后更新**: 2026-02-02  
**版本**: v1.6.0  
**状态**: 🟢 活跃 (与CDD宪法v1.6.0同步)

*遵循宪法驱动开发: 代码即数学证明，架构即宪法约束。*