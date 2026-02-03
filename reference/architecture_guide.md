# CDD架构综合指南

## 🏛️ 第一部分：架构全景图

### 1.1 法律体系分层 (T0-T2)

CDD 系统由上至下分为三个法律层级，每一层都约束下一层的行为，形成严格的宪法驱动体系。

#### T0: 核心宪法 (Constitutional Core)
- **定义**: 系统的最高真理，定义了"我们是谁"以及"系统状态"
- **文件**: `templates/core/active_context.md`
- **内容**: 当前焦点、任务状态、熵值指标
- **变更频率**: 极低频，需通过 WF-amend 协议
- **加载规则**: 始终驻留在AI上下文中

#### T1: 系统公理 (System Axioms)
- **定义**: 系统的物理定律，定义了架构模式、技术栈约束和行为准则
- **文件**: `axioms/system_patterns.md`, `axioms/tech_context.md`, `axioms/behavior_context.md`
- **内容**: 架构约束、接口签名、行为断言
- **变更频率**: 低频，随架构演进更新
- **加载规则**: 按需加载，使用后释放

#### T2: 执行标准 (Executive Standards)
- **定义**: 具体特性的立法文档，每个特性必须对应一套T2文档
- **文件**: `specs/xxx/DS-050_spec.md`, `DS-051_plan.md`, `DS-052_tasks.md`
- **内容**: 特性规范、实施计划、原子任务
- **变更频率**: 高频，随特性开发产生
- **加载规则**: 惰性加载，按需读取

#### 同构映射原则 ($S_{fs} \cong S_{doc}$)
文件系统结构必须与文档结构保持同构，确保代码实现与设计规范的一致性：
- `src/auth/` 代码必须对应 `templates/axioms/system_patterns.md` 中的Auth模块定义
- 文件系统层次反映文档体系层次
- 代码结构映射到架构约束

### 1.2 三级递进架构 (导航体系)

CDD采用三级递进架构设计，确保AI能够高效理解和执行宪法驱动开发：

```
第一级: SKILL.md (总纲层) - AI执行手册，快速上手
第二级: reference/ (概念层) - 模块化概念，深度理解  
第三级: templates/ (实现层) - 具体模板，直接使用
```

#### 第一级：SKILL.md (总纲层)
- **目的**: AI执行手册，提供快速上手指南
- **内容**: 核心工作流、工具链概述、快速开始
- **特点**: 简洁明了，<800 tokens，始终可用
- **使用场景**: AI代理初次接触CDD时阅读

#### 第二级：reference/ (概念层)
- **目的**: 模块化概念文档，提供深度理解
- **内容**: 架构概念、工作流程、法律框架、技术标准
- **特点**: 专题化组织，按需查阅
- **使用场景**: 遇到特定问题时深入查阅

#### 第三级：templates/ (实现层)
- **目的**: 具体模板文件，提供直接实现
- **内容**: 宪法核心、系统公理、工作流程、执行标准
- **特点**: 可直接复制或实例化，具体实现
- **使用场景**: 需要具体实现时使用

## 📊 第二部分：架构地图与导航

### 2.1 文件统计概览

| 层级 | 目录 | 文件数量 | 平均大小 | 设计目的 |
|------|------|----------|----------|----------|
| **第一级** | SKILL.md | 1个文件 | ~3KB | AI快速上手指南 |
| **第二级** | reference/ | 11个文件 | ~1KB/文件 | 概念深度理解 |
| **第三级** | templates/ | 24个文件 | ~2KB/文件 | 具体模板实现 |

### 2.2 详细映射关系

#### 架构体系 (Architecture System)

| 概念文件 | 描述 | 相关模板 |
|----------|------|----------|
| `architecture_overview.md` | 架构全景概念 | `core/active_context.md`, `axioms/system_patterns.md`, `axioms/tech_context.md`, `standards/DS-050_feature_specification.md`, `standards/DS-051_implementation_plan.md` |
| `cdd_document_system_guide.md` | 文档体系指南 | `core/active_context.md`, `core/knowledge_graph.md`, 所有法律索引文件, 所有公理文件, 所有标准模板 |

#### 工作流程 (Workflow)

| 概念文件 | 描述 | 相关模板 |
|----------|------|----------|
| `core_workflow.md` | 核心工作流 | `protocols/WF-201_cdd_workflow.md`, `protocols/WF-review.md`, `protocols/WF-amend.md` |
| `external_auditor.md` | 外部审计接口 | `protocols/WF-review.md`, `standards/DS-060_code_review.md` |

#### 法律框架 (Legal Framework)

| 概念文件 | 描述 | 相关模板 |
|----------|------|----------|
| `legal_framework.md` | 法律框架 | `core/basic_law_index.md`, `core/procedural_law_index.md`, `core/technical_law_index.md`, `protocols/WF-amend.md` |

#### 技术实现 (Technical Implementation)

| 概念文件 | 描述 | 相关模板 |
|----------|------|----------|
| `cdd_model_config.md` | 模型配置 | `core/active_context.md` |
| `entropy_metrics.md` | 熵值指标 | `core/active_context.md`, `standards/DS-054_environment_hardening.md` |
| `entropy_calculation_guide.md` | 熵值计算指南 | `axioms/system_patterns.md`, `axioms/tech_context.md`, `axioms/behavior_context.md` |

#### 模板使用 (Template Usage)

| 概念文件 | 描述 | 相关模板 |
|----------|------|----------|
| `template_usage.md` | 模板使用指南 | `standards/DS-050_feature_specification.md`, `standards/DS-051_implementation_plan.md`, `standards/DS-052_atomic_tasks.md`, `standards/feature_readme_template.md` |

### 2.3 模板关系索引

#### T0层：核心宪法模板
- **`core/active_context.md`** - 活动上下文，系统当前状态
- **`core/basic_law_index.md`** - 基本法核心公理索引
- **`core/knowledge_graph.md`** - 知识图谱导航地图
- **`core/procedural_law_index.md`** - 程序法工作流索引
- **`core/technical_law_index.md`** - 技术法标准索引

#### T1层：系统公理模板
- **`axioms/behavior_context.md`** - 行为约束和测试期望
- **`axioms/system_patterns.md`** - 架构模式和设计约束
- **`axioms/tech_context.md`** - 技术栈和接口签名

#### T2层：执行标准模板
- **`standards/DS-050_feature_specification.md`** - 特性规范模板
- **`standards/DS-051_implementation_plan.md`** - 实施计划模板
- **`standards/DS-052_atomic_tasks.md`** - 原子任务模板
- **`standards/DS-053_quality_checklist.md`** - 质量检查清单
- **`standards/DS-054_environment_hardening.md`** - 环境强化标准
- **`standards/DS-060_code_review.md`** - 代码审查标准
- **`standards/feature_readme_template.md`** - 特性README模板

#### T1/T2层：工作流程模板
- **`protocols/WF-201_cdd_workflow.md`** - CDD标准工作流
- **`protocols/WF-review.md`** - 代码审查协议
- **`protocols/WF-amend.md`** - 宪法修正案协议
- **`protocols/WF-001_clarify_workflow.md`** - 需求澄清工作流
- **`protocols/WF-analyze.md`** - 分析协议
- **`protocols/WF-sync-issues.md`** - GitHub Issues同步协议

## 🚀 第三部分：使用与实施

### 3.1 使用指南

#### 对于AI代理
1. **初次接触**: 从SKILL.md开始，了解核心工作流（约5分钟阅读）
2. **遇到问题**: 查阅reference/中的相关概念文件（按需查阅）
3. **需要实现**: 查看templates/中的具体模板（直接使用）
4. **审计验证**: 使用`cdd_audit.py`确保合规（定期执行）

#### 对于开发者
1. **新特性开发**: 使用`cdd-feature.py`自动生成T2文档（避免手动创建）
2. **架构变更**: 更新templates/core/中的宪法文件（遵循WF-amend协议）
3. **概念扩展**: 在reference/中添加新的概念文档（保持模块化）
4. **模板优化**: 改进templates/standards/中的模板（基于实践经验）

### 3.2 工作流示例

#### 示例1：创建用户认证特性
```
SKILL.md → template_usage.md → DS-050_feature_specification.md
                                  ↓
                         cdd-feature.py "用户认证"
                                  ↓
                        specs/xxx-user-auth/ (自动生成)
                                  ↓
                    DS-050_spec.md, DS-051_plan.md
                                  ↓
                             代码实现
                                  ↓
                         三级验证 (Tier 1/2/3)
```

#### 示例2：审计项目状态
```
SKILL.md → external_auditor.md → WF-review.md
                                   ↓
                          cdd_audit.py --ai-hint
                                   ↓
                      JSON格式的审计报告
                                   ↓
                     AI生成的修复建议
```

#### 示例3：更新宪法约束
```
SKILL.md → legal_framework.md → basic_law_index.md
                                   ↓
                            WF-amend协议
                                   ↓
                    deepseek-reasoner审计
                                   ↓
                    宪法修正案提案与批准
```

### 3.3 架构优势总结

#### 1. 认知负载优化
- **三级分离**: 避免信息过载，AI只需加载必要内容
- **按需加载**: T1/T2模板只在需要时加载，释放上下文空间
- **Token控制**: 严格限制各层级的Token使用量

#### 2. 导航路径清晰
- **明确指引**: AI知道何时查阅哪个层级
- **映射关系**: 概念文件与模板文件的清晰对应
- **工作流示例**: 具体场景下的操作路径

#### 3. 维护成本低
- **概念与实现分离**: reference/存放概念，templates/存放实现
- **模板化**: 标准化文档模板，减少重复劳动
- **自动化**: 使用`cdd-feature.py`自动生成文档

#### 4. 扩展性强
- **模块化设计**: 新增概念只需添加reference文件
- **模板体系**: 新模板可轻松集成到现有体系
- **层级清晰**: 各层级职责明确，互不干扰

## 附录：导航快速参考

### 常见问题导航路径

| 问题类型 | 建议导航路径 |
|----------|--------------|
| **如何开始CDD开发？** | SKILL.md → core_workflow.md |
| **如何创建新特性？** | template_usage.md → cdd-feature.py |
| **如何审计项目？** | external_auditor.md → cdd_audit.py |
| **如何更新宪法？** | legal_framework.md → WF-amend协议 |
| **如何计算熵值？** | entropy_calculation_guide.md → measure_entropy.py |

### 关键命令参考
```bash
# 特性开发
python scripts/cdd-feature.py "特性名" "描述"

# 项目审计
python scripts/cdd_audit.py --gate all --format json

# 熵值监控
python scripts/measure_entropy.py --json

# 版本验证
python scripts/verify_versions.py --fix
```

## 版本与状态

**最后更新**: 2026-02-03  
**文档版本**: v1.0.0  
**基于CDD宪法版本**: v1.6.1  
**状态**: 🟢 活跃  

---

*遵循宪法驱动开发：架构即约束，文档即法律，代码即证明。*