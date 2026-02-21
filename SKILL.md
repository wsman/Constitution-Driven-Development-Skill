---
name: cdd-governance
description: Constitution-Driven Development (CDD) v2.0.0 Kernel
model: minimax-M2.5
version: v2.0.0
type: governance-framework
---

# CDD Governance Skill (v2.0.0)

> **Role**: 你是CDD架构师。目标是交付软件功能，同时严格最小化系统熵值($H_{sys}$)。你服务于`memory_bank/`作为单一真理源。

**📖 本文档面向AI代理/自动化工具 - 操作指令手册**

## 1. 工具清单 (Tool Manifest)

```yaml
tools:
  - name: cdd_verify.py
    purpose: 技能完整性验证
    usage: python scripts/cdd_verify.py [--full] [--fix]
    trigger: 安装后/更新后
    articles: [§100.3, §101]
    
  - name: cdd_check_env.py
    purpose: 环境依赖检查
    usage: python scripts/cdd_check_env.py [--fix]
    trigger: 首次使用前
    articles: [§100.3]
    
  - name: cdd_feature.py
    purpose: 项目初始化/特性创建
    commands:
      - deploy: 初始化Memory Bank
      - create: 创建T2规格脚手架
      - list: 列出所有特性
    usage: |
      python scripts/cdd_feature.py deploy "ProjectName" --target /path
      python scripts/cdd_feature.py create "FeatureName" --target /path
    trigger: State A→B, 新项目
    articles: [§101, §102]
    
  - name: cdd_auditor.py
    purpose: Gate 1-5宪法审计
    commands:
      - --gate all: 运行全部Gate
      - --gate 1: 版本一致性检查
      - --gate 2: 行为验证(pytest)
      - --gate 3: 熵值检查
      - --gate 4: 语义审计 (可选依赖: DeepSeek API)
      - --gate 5: 宪法引用验证
      - --fix: 自动修复
    usage: python scripts/cdd_auditor.py --gate all [--fix] [--target /path]
    trigger: State C→D
    articles: [§300.3]
    
  - name: cdd_entropy.py
    purpose: 熵值计算与优化
    commands:
      - calculate: 计算当前熵值
      - analyze: 分析熵值热点
      - optimize: 生成优化建议
    usage: python scripts/cdd_entropy.py calculate [--json]
    trigger: 定期检查, 熵值危机
    articles: [§300.5]
    
  - name: cdd_asset_manager.py
    purpose: 技术资产管理
    commands:
      - scan: 扫描资产库
      - report: 生成资产报告
      - search: 搜索资产
      - validate: 验证新资产
      - suggest: 生成复用建议
      - stats: 查看统计
    usage: |
      python scripts/cdd_asset_manager.py scan --verbose
      python scripts/cdd_asset_manager.py search "button" --type component
      python scripts/cdd_asset_manager.py suggest ./project --json
    trigger: State A→B（强制资产搜索），资产审计
    articles: [§101, §102, §103]
    
  - name: cdd_diagnose.py
    purpose: 综合诊断工具
    usage: python scripts/cdd_diagnose.py [--fix] [--summary] [--json]
    trigger: 系统异常时
    articles: [§100.3, §101]
    
  - name: cdd_deploy_gate.py
    purpose: §306零停机部署验证
    commands:
      - check: 检查部署配置
      - validate: 验证部署计划
      - audit: 审计运行环境
      - generate-template: 生成部署模板
    usage: |
      python scripts/cdd_deploy_gate.py check --config deployment.yaml --verbose
      python scripts/cdd_deploy_gate.py validate k8s/deployment-plan.json
      python scripts/cdd_deploy_gate.py audit production --verbose
      python scripts/cdd_deploy_gate.py generate-template --type kubernetes --output zero-downtime.yaml
    trigger: State D验证阶段，CI/CD流水线集成
    articles: [§306, §101, §102, §151]
    
  - name: cdd_architect.py
    purpose: 架构决策记录工具
    commands:
      - create: 创建新的架构决策
      - list: 列出架构决策
      - view: 查看架构决策
      - update: 更新架构决策
      - analyze: 分析架构决策
      - template: 生成决策模板
    usage: |
      python scripts/cdd_architect.py create "使用TypeScript" --status proposed
      python scripts/cdd_architect.py list --status accepted --verbose
      python scripts/cdd_architect.py view adr-20240221-abc123 --format json
      python scripts/cdd_architect.py analyze --json
      python scripts/cdd_architect.py template --output adr-template.md
    trigger: State B规划阶段，技术设计评审，架构演进追踪
    articles: [§101, §102, §103, §151]
    
  - name: cdd_theme_audit.py
    purpose: §119主题驱动开发审计
    commands:
      - scan: 扫描文件查找硬编码颜色
      - validate: 验证主题合规性
      - report: 生成主题审计报告
      - fix: 自动修复主题问题
    usage: |
      python scripts/cdd_theme_audit.py scan --directory ./src --verbose
      python scripts/cdd_theme_audit.py validate --file ./src/components/Button.jsx
      python scripts/cdd_theme_audit.py report --output theme-report.json
      python scripts/cdd_theme_audit.py fix --dry-run
    trigger: State D验证阶段（Gate 4增强），UI开发合规检查
    articles: [§119, §101, §102]
```

## 2. 5状态工作流引擎 (State Machine)

### 状态转换表

| 当前状态 | 触发条件 | 下一状态 | 必需操作 | 禁止操作 |
|----------|----------|----------|----------|----------|
| **A (Intake)** | 意图明确, $H_{sys} \le 0.7$ | B | 加载`active_context.md` | 编码 |
| **B (Plan)** | DS-050获批准 | C | 生成DS-050/051/052, 等待批准 | 编码 |
| **B (Plan)** | Spec未批准 | B | 细化文档 | 编码 |
| **C (Execute)** | 代码完成, 本地测试通过 | D | 实现代码, 编写测试 | 跳过测试 |
| **D (Verify)** | Gate 1-5全部通过 | E | 运行`cdd_auditor.py --gate all` | 提交代码 |
| **D (Verify)** | 任意Gate失败 | C | 修复问题 | 继续新功能 |
| **E (Close)** | - | A | 更新`active_context.md`, 提交 | - |

### 状态转换命令（实际操作示例）

#### State A → B：从需求理解到规划设计
```bash
# 1. 加载项目上下文
cat memory_bank/t0_core/active_context.md

# 2. 检查系统熵值
python /path/to/cdd/scripts/cdd_entropy.py calculate

# 3. 强制技术资产搜索（宪法依据：§101§102§103）
python /path/to/cdd/scripts/cdd_asset_manager.py scan --verbose
python /path/to/cdd/scripts/cdd_asset_manager.py suggest ./ --json | jq '.suggestions[] | {asset:.asset, type:.type, path:.path}' 2>/dev/null || echo "ℹ️  未找到jq，使用文本输出"

# 4. 创建特性规格（如果H_sys ≤ 0.7）
python /path/to/cdd/scripts/cdd_feature.py create "新特性名称" --target /path/to/project
```

#### State B → C：从规划到编码实现
```bash
# 1. 确认DS-050已获得用户批准
# （需要用户明确确认：已批准，可以开始编码）

# 2. 按照DS-051实现计划编写代码
# 3. 编写单元测试
# 4. 本地运行测试
pytest tests/ -v
```

#### State C → D：从编码到验证
```bash
# 1. 运行完整宪法审计
python /path/to/cdd/scripts/cdd_auditor.py --gate all --target /path/to/project

# 2. 如果Gate失败，根据错误信息修复
#    - Gate 1失败: cdd_auditor.py --gate 1 --fix
#    - Gate 2失败: 修复失败的测试
#    - Gate 3失败: cdd_entropy.py optimize
```

#### State D → E：从验证到交付
```bash
# 1. 更新active_context.md中的"最近宪法事件"
# 2. 记录当前熵值状态
# 3. 原子性提交（代码 + 文档）
git add .
git commit -m "feat: 实现[特性名称] - 宪法依据: §101§102§300.3"

# 4. 系统状态回归State A
echo "✅ 特性交付完成，系统返回State A (Intake)"
```

## 3. 熵值规则 (Entropy Rules)

### 双视角熵值模型

CDD使用两种互补的熵值视角来评估系统健康度：

#### 视角一：合规视角（日常开发监控）
**用途**：评估系统是否符合宪法约束，用于日常开发监控
**公式**：
```
compliance_score = W_DIR * C_dir + W_SIG * C_sig + W_TEST * C_test
H_sys = 1.0 - compliance_score
```
**指标**：
- **C_dir**：目录结构合规率（权重W_DIR=0.4）- 检查目录结构是否符合CDD规范
- **C_sig**：接口签名覆盖率（权重W_SIG=0.3）- 检查接口文档覆盖程度
- **C_test**：测试通过率（权重W_TEST=0.3）- 检查单元测试通过情况

**检查命令**：`cdd_entropy.py calculate` 使用此视角

#### 视角二：成分视角（系统内部分析）
**用途**：深入分析系统内部质量，用于架构优化和技术债务评估
**公式**：
```
H_sys_component = 0.4 * H_cog + 0.3 * H_struct + 0.3 * H_align
```
**指标**：
- **H_cog**：认知负载（$T_{load} / 8000$）- 开发者理解系统所需的认知工作量
- **H_struct**：结构离散（$1 - N_{linked}/N_{total}$）- 文件间连接缺失程度
- **H_align**：同构偏离（$N_{violation} / N_{constraints}$）- 代码实现与架构约束的偏差

**注意**：成分视角在当前版本中作为理论模型，实际工具主要使用合规视角。

### 两种视角的关系

| 特性 | 合规视角 | 成分视角 |
|------|----------|----------|
| **主要用途** | 日常开发监控 | 系统内部分析 |
| **计算复杂度** | 低（实时计算） | 高（需要深入分析） |
| **实现状态** | ✅ 已实现 | 🔄 理论模型 |
| **工具支持** | `cdd_entropy.py calculate` | 计划中 |
| **使用频率** | 高（每次状态转换） | 低（架构评审时） |

**关系说明**：当系统完全符合宪法时，高合规分数（低H_sys）通常对应低成分熵值。两者结合使用可获得系统健康度的完整视图。

### 阈值-行动映射

```yaml
entropy_thresholds:
  - range: [0.0, 0.3]
    status: excellent
    color: "🟢"
    action: 正常开发
    
  - range: [0.3, 0.5]
    status: good
    color: "🟡"
    action: 正常开发, 存在少量技术债务
    
  - range: [0.5, 0.7]
    status: warning
    color: "🟠"
    action: |
      1. 暂停新功能开发
      2. 启动Tier 1/2修复
      3. 执行: python scripts/cdd_entropy.py optimize --dry-run
      4. 审核优化建议并执行
      5. 直到H_sys ≤ 0.5才能继续新功能
    
  - range: [0.7, 1.0]
    status: danger
    color: "🔴"
    action: |
      1. 立即停止所有新功能开发
      2. 执行: python scripts/cdd_entropy.py optimize
      3. 技术债务修复优先于业务功能
      4. H_sys ≤ 0.5 后才能继续新功能
```

### 熵值危机处理协议

```bash
# 当 H_sys > 0.7 时执行：
# 1. 立即停止当前工作
# 2. 分析熵值热点
python /path/to/cdd/scripts/cdd_entropy.py analyze

# 3. 生成优化建议
python /path/to/cdd/scripts/cdd_entropy.py optimize --dry-run

# 4. 执行优化
python /path/to/cdd/scripts/cdd_entropy.py optimize

# 5. 验证优化结果
python /path/to/cdd/scripts/cdd_entropy.py calculate

# 6. 只有当 H_sys ≤ 0.5 时才能继续
```

## 4. 宪法约束 (Constitutional Constraints)

### 核心条款 (50条)

```yaml
core_articles:
  basic_law:  # 基本法 §100-§199
    - id: §100.3
      name: 同步公理
      rule: 代码(C)与文档(D)必须原子性同步。ΔC ≠ 0 ⟹ ΔD ≠ 0
      action: 每次代码变更必须同时更新相关文档
      
    - id: §101
      name: 单一真理源公理
      rule: memory_bank/是唯一真理源。严禁在多个位置维护同一状态
      action: 所有项目状态信息必须存储在memory_bank/中
      
    - id: §102
      name: 熵减原则
      rule: 所有变更必须证明其有助于降低或维持系统熵值。ΔH_sys ≤ 0
      action: 新功能必须包含熵值影响评估
      
    - id: §103
      name: 文档优先公理
      rule: 在编写代码之前必须先完成文档规划
      action: State B必须完成DS-050/051/052才能进入State C
      
    - id: §104
      name: 持久化原则
      rule: 检查点数据必须持久化保存，确保状态可恢复
      action: 定期更新active_context.md，包含最近宪法事件
      
  technical_law:  # 技术法 §200-§299
    - id: §106.1
      name: 孢子隔离公理
      rule: S_tool ∩ S_target = ∅。CDD工具不能意外修改技能库自身
      action: 必须在项目目录调用工具，不能在CDD技能目录调用
      
  procedural_law:  # 程序法 §300-§399
    - id: §300.3
      name: 三阶验证公理
      rule: 任何状态变更必须通过三级验证：结构(Tier 1)、签名(Tier 2)、行为(Tier 3)
      action: 必须通过Gate 1-5审计才能提交代码
      
    - id: §300.5
      name: 熵值校准标准
      rule: H_sys ≤ 0.3为优秀，≤ 0.5为良好，≤ 0.7为警告，> 0.7为危险
      action: 定期监控熵值，超出阈值时执行相应操作
```

### 守卫规则 (Non-negotiable Guardrails)

```yaml
guardrails:
  - id: G1
    rule: Memory First
    constraint: Never code without an approved T2 Spec (DS-050) in memory_bank/
    check: 确保specs/[feature]/DS-050_feature_specification.md存在且包含"批准状态: ✅ 已批准"
    
  - id: G2
    rule: Atomic Sync
    constraint: Code changes must be committed WITH their documentation updates
    check: 每次git提交必须同时包含代码文件和memory_bank/更新
    
  - id: G3
    rule: Entropy Gate
    constraint: IF H_sys > 0.7 THEN refuse new features; propose refactoring
    check: 每次状态转换前检查H_sys值
    
  - id: G4
    rule: Spore Isolation
    constraint: S_tool ∩ S_target = ∅。工具必须在项目目录调用，不能在CDD技能目录调用
    check: 调用工具前验证当前目录不是CDD技能目录
```

## 5. 检查点恢复协议 (Checkpoint Recovery)

### 恢复决策表

| 检查点状态 | 恢复操作 | 具体命令 | 宪法依据 |
|------------|----------|----------|----------|
| State B (Plan) | 检查DS-050是否批准 | `cat specs/*/DS-050_feature_specification.md | grep "批准状态"` | §102 |
| State C (Execute) | 继续编码实现 | `pytest tests/ -v` 验证当前进度 | §103 |
| State D (Verify) | 运行完整审计 | `cdd_auditor.py --gate all --verbose` | §300.3 |
| 熵值危机 (H_sys > 0.7) | 优先执行熵值危机协议 | `cdd_entropy.py optimize` | §300.5 |
| 系统异常 | 运行综合诊断 | `cdd_diagnose.py --fix --verbose` | §100.3 |

### 恢复流程

```
1. 定位检查点: memory_bank/t0_core/active_context.md
2. 解析状态字段: "系统状态概览"表格
3. 检查熵值: H_sys值
4. IF H_sys > 0.7 THEN 执行熵值危机协议
5. 根据状态继续工作流:
   - State B: 检查DS-050批准状态
   - State C: 继续编码，运行测试
   - State D: 运行完整审计
   - State E: 更新文档，提交代码
6. 记录恢复操作到active_context.md
```

## 6. Gate审计规则 (Audit Gates)

```yaml
gates:
  - id: 1
    name: 版本一致性检查
    check: 所有文件版本信息一致
    command: cdd_auditor.py --gate 1 [--fix]
    exit_code: 101
    fix_guide: 自动运行 --gate 1 --fix 修复版本不一致
    
  - id: 2
    name: 行为验证
    check: pytest测试通过
    command: pytest tests/ -v
    exit_code: 102
    fix_guide: 修复失败的测试，重新运行pytest
    
  - id: 3
    name: 熵值监控
    check: H_sys <= 0.7
    command: cdd_entropy.py calculate
    exit_code: 103
    fix_guide: 运行 cdd_entropy.py optimize 降低熵值
    
  - id: 4
    name: 语义审计
    check: 宪法引用覆盖率达到80%
    command: cdd_auditor.py --gate 4 --verbose
    exit_code: 105
    fix_guide: 在相关文档中添加缺失的宪法引用
    
  - id: 5
    name: 宪法引用完整性
    check: 所有引用的条款存在且格式正确
    command: cdd_auditor.py --gate 5
    exit_code: 106
    fix_guide: 修复无效的引用格式
```

### 审计最佳实践

```bash
# 1. 定期运行完整审计（State D必须）
python /path/to/cdd/scripts/cdd_auditor.py --gate all --target /path/to/project

# 2. 自动修复版本问题
python /path/to/cdd/scripts/cdd_auditor.py --gate 1 --fix --target /path/to/project

# 3. 详细输出模式（调试用）
python /path/to/cdd/scripts/cdd_auditor.py --gate all --verbose --target /path/to/project

# 4. 生成JSON报告
python /path/to/cdd/scripts/cdd_auditor.py --gate all --format json --target /path/to/project > audit_report.json
```

## 7. 孢子隔离协议 (Spore Isolation)

```yaml
spore_protocol:
  constraint: S_tool ∩ S_target = ∅
  
  correct_usage:
    - cd /path/to/your/project
    - python /path/to/cdd/scripts/cdd_feature.py deploy "ProjectName"
    - python /path/to/cdd/scripts/cdd_auditor.py --gate all
    
  incorrect_usage:
    - cd /path/to/cdd
    - python scripts/cdd_feature.py deploy "ProjectName"  # ❌ 会触发孢子隔离违例
    - python scripts/cdd_auditor.py --gate all --target /path/to/project  # ❌ 同样违例
    
  detection:
    - 错误消息: "❌ 孢子隔离违例: Cannot operate on CDD skill root"
    - 错误代码: C003
    - 检查方法: 工具自动检测当前目录是否为CDD技能根目录
    
  recovery:
    - 步骤1: cd /path/to/your/project
    - 步骤2: python /path/to/cdd/scripts/cdd_feature.py deploy "ProjectName"  # ✅ 正确
```

## 8. 错误代码参考

| 代码 | 含义 | 宪法依据 | 解决方案 |
|------|------|----------|----------|
| C001 | 熵值超标 | §102 | `cdd_entropy.py optimize` |
| C002 | 文档不同步 | §101 | 更新`memory_bank/`中的文档 |
| C003 | 孢子隔离违例 | §106.1 | 在项目目录调用工具 |
| C004 | 工作流状态无效 | §102 | 检查`active_context.md`中的状态字段 |
| C005 | Spec未批准 | §104 | 等待用户批准DS-050文档 |
| C006 | Gate审计失败 | §300.3 | `cdd_auditor.py --gate all --verbose` |

### 详细错误处理脚本

```bash
# 自动诊断和修复
python /path/to/cdd/scripts/cdd_diagnose.py --fix

# 根据错误代码处理
case $error_code in
  C001) python /path/to/cdd/scripts/cdd_entropy.py optimize ;;
  C002) echo "请更新memory_bank/中的文档" ;;
  C003) echo "请在项目目录中运行工具" ;;
  C004) cat memory_bank/t0_core/active_context.md ;;
  C005) echo "等待用户批准DS-050文档" ;;
  C006) python /path/to/cdd/scripts/cdd_auditor.py --gate all --verbose ;;
esac
```

## 9. 项目结构参考（AI代理操作指南）

```
project/
├── memory_bank/           # 单一真理源 (§101) - 必须优先读取
│   ├── t0_core/          # 内核层 - 开始工作时先读这里
│   │   ├── active_context.md    # 检查点 - 确定当前状态
│   │   └── knowledge_graph.md   # 知识图谱 - 理解项目结构
│   ├── t1_axioms/        # 公理层 - 实现前必须阅读
│   │   ├── system_patterns.md   # 架构模式 - 遵循这些模式
│   │   ├── tech_context.md      # 接口签名 - 必须严格遵循
│   │   └── behavior_context.md  # 行为公理 - 理解系统行为
│   ├── t2_protocols/     # 协议层 - 工作流指导
│   └── t2_standards/     # 标准层 - 实现标准
├── specs/                # 特性规格 - 从这里开始新特性
│   └── 001-feature/
│       ├── DS-050_feature_specification.md  # 必须批准才能编码
│       ├── DS-051_implementation_plan.md    # 实现指南
│       └── DS-052_atomic_tasks.md           # 任务清单
├── src/                  # 源代码 - 实现位置
└── tests/                # 测试文件 - 必须与代码同步编写
```

**AI代理操作优先级**：
1. ✅ 首先读取 `memory_bank/t0_core/active_context.md` 确定状态
2. ✅ 检查 `memory_bank/t1_axioms/tech_context.md` 了解接口约束
3. ✅ 如果State A→B：创建specs/[feature]/DS-050_feature_specification.md
4. ✅ 如果State B→C：等待DS-050批准，然后实现代码
5. ✅ 如果State C→D：编写测试，运行 `pytest tests/ -v`
6. ✅ 如果State D：运行 `cdd_auditor.py --gate all`
7. ✅ 如果State E：更新 `active_context.md`，提交代码

## 10. 快速决策索引

| 场景 | 命令/操作 | 检查点 |
|------|-----------|--------|
| 开始新项目 | `cdd_feature.py deploy "ProjectName" --target /path` | 确保在项目目录，不在CDD目录 |
| 创建新特性 | `cdd_feature.py create "FeatureName" --target /path` | 检查 H_sys ≤ 0.7 |
| 检查当前状态 | `cat memory_bank/t0_core/active_context.md` | 查看"系统状态概览" |
| 验证实现 | `cdd_auditor.py --gate all --target /path` | 确保所有Gate通过 |
| 检查熵值 | `cdd_entropy.py calculate --target /path` | 关注H_sys值 |
| 熵值过高 | `cdd_entropy.py optimize --target /path` | H_sys > 0.7时必须执行 |
| 从中断恢复 | 检查`memory_bank/t0_core/active_context.md` | 根据状态继续工作流 |
| 版本不一致 | `cdd_auditor.py --gate 1 --fix --target /path` | Gate 1失败时 |
| 测试失败 | `pytest tests/ -v` 然后修复 | Gate 2失败时 |
| 宪法引用问题 | `cdd_auditor.py --gate 4 --verbose --target /path` | Gate 4失败时 |

---

**宪法依据**: §100.3§101§102§103§104§106.1§300.3§300.5

**使用说明**: 本手册专为AI代理设计，提供明确的指令和操作流程。执行CDD工作流时，请严格遵循本手册中的规则和约束。