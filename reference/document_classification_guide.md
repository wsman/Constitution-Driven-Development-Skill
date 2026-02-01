# 逆熵实验室 - 文档分级体系说明书

**版本**: v1.0.0
**宪法依据**: [基本法 §10.6]
**用途**: 指导系统上下文管理与注意力分配。

## 📚 分级概述

文档分级体系是 **Bootloader Mode** 的核心逻辑基础，决定了上下文加载的优先级和系统的注意力分配。通过 T0-T3 四级分层，实现了系统的认知层次结构优化，确保了低熵状态下的高效运作。

### 数学公理

$$
\sum_{file \in Context} \text{Token}(file) \leq T_{limit} \quad \text{where} \quad Context \approx T0 + \text{Active}(T2)
$$

**注意力分配不等式**:
$$
\text{Attention}(T0) \gg \text{Attention}(T1) > \text{Attention}(T2) \gg \text{Attention}(T3)
$$

## 🔥 T0: 核心意识层 (Kernel & Consciousness)

**定义**: 系统的"大脑"和"地图"。启动时的**最小必要集合 (Minimum Viable Context)**，必须常驻内存或被优先索引，构成了系统的"自我意识"和"导航能力"。

### 文件列表
- **`activeContext.md`**: 短期记忆与焦点。包含当前任务状态、宪法事件记录和熵值监测。
- **`KNOWLEDGE_GRAPH.md`**: 联想导航图。提供系统实体间的高维关联导航，支持神经网络导航协议。
- **法典内核**: 宪法引导器集合：
  - `default-rules.md`: 基本法内核与 Bootloader 协议
  - `procedural_law.md`: 程序法内核 (核心流程索引与指针)
  - `technical_law.md`: 技术法内核 (核心技术公理与指针)

### 启动协议 (Boot Protocol)
遵循宪法§3内存加载协议，启动时**仅允许**加载：
1. `activeContext.md` (自我意识)
2. `KNOWLEDGE_GRAPH.md` (神经中枢) 
3. 法典内核 (宪法约束)

## 🧠 T1: 索引与状态层 (Indices & State)

**定义**: 系统的"字典"和"仪表盘"。当 T0 层无法提供足够细节，或需要进行精确检索时加载。

### 文件列表
- **全局查找表**:
  - `LAW_REFERENCE_MAP.md`: 文件路径映射，提供$O(1)$查找能力
  - `STANDARD_CATALOG.md`: 标准分类目录，索引所有DS/WF标准

- **系统状态**:
  - `systemState.md`: 组件状态快照，记录系统运行时状态
  - `DECISION_LOG.md`: 历史架构决策，支持决策追溯

- **核心定义 (Axioms)**:
  - `CONCEPTS.md`: 核心概念定义
  - `ARCHITECTURE.md`: 架构蓝图
  - `systemPatterns.md`: 系统模式约束
  - `GLOSSARY.md`: 术语表

### 检索策略
- **高频检索**: $O(1)$查找复杂度
- **按需加载**: 仅当T0层无法解决问题时才加载
- **上下文优化**: 完成任务后及时释放

## 📖 T2: 执行规范层 (Executables)

**定义**: 具体的"技能书"。绝大多数时候处于"休眠"状态，仅通过图谱导航或索引检索**按需加载**。

### 文件分类
- **DS 标准库**: `standards/DS-*.md` (如 DS-001, DS-002)
  - DS-001: UTF-8输出配置标准实现 [技术法 §301.1]
  - DS-002: 原子文件写入标准实现 [技术法 §302.1]
  - DS-007: 架构同构性验证标准实现 [技术法 §352]
  - 共40+个技术标准

- **工作流库**: `workflows/WF-*.md` (如 WF-201, WF-210)
  - WF-201: 宪法驱动开发工作流程 [程序法 §201]
  - WF-210: 安全操作流程 [程序法 §210]
  - 共10+个操作流程

- **MCP 工具库**: `mcp_library/MC-*.md` (如 MC-010)
  - MCP协议标准与工具配置

- **API 规范库**: `api_reference/AP-*.md`
  - 接口定义与契约标准

### 懒加载协议 (Lazy Loading Protocol)
1. **检索**: 在 `LAW_REFERENCE_MAP.md` 或 `STANDARD_CATALOG.md` 中查找关键词
2. **加载**: 使用 `read_file` 读取具体的 `DS-xxx` 或 `WF-xxx` 文件
3. **执行**: 完成后释放上下文（通过不再引用细节）
4. **验证**: 确保实现符合相关宪法条款

## 📊 T3: 分析与归档层 (Archives)

**定义**: 系统的"历史档案"。用于审计、分析或回溯，通常不需要在开发任务中加载。

### 文件分类
- **分析报告**: `04_analysis_and_visualization/` 下的所有报告
  - 系统性能分析
  - 架构评估报告
  - 熵值趋势分析

- **可视化元数据**:
  - `codex_graph.json`: 法典节点关系图
  - `codex_summary.json`: 三层摘要索引
  - `entropy_monitoring_report.md`: 熵监控报告

- **历史归档**: `storage/archive/` 目录
  - 历史版本备份
  - 已弃用标准存档
  - 项目历史记录

### 访问策略
- **审计时才加载**: 除非进行系统审计，否则不加载
- **只读访问**: 所有T3文件均为只读参考
- **冷存储**: 支持归档到外部存储系统

## 🔄 检索策略算法 (Retrieval Strategy Algorithm)

### 标准问题解决路径
```
1. 问题分析 → 2. 图谱定位 → 3. 索引检索 → 4. 标准执行 → 5. 熵减验证
```

### 具体检索示例

#### 示例1: "如何部署系统？"
1. **Scan T0**: 查阅 `KNOWLEDGE_GRAPH.md` -> 发现 `WF-Ops` 簇 (运维簇)
2. **Lookup T1**: 在 `LAW_REFERENCE_MAP.md` 找到 `WF-220` 路径
3. **Load T2**: 读取 `WF-220_MCP运维流程.md`
4. **Execute**: 执行部署操作
5. **Unload**: 任务完成后释放 T2 上下文

#### 示例2: "如何处理UTF-8输出编码？"
1. **Query T0**: 检查当前认知 (无直接答案)
2. **Search T1**: 查询 `LAW_REFERENCE_MAP.md` -> 技术法§301
3. **Load T2**: 读取 `DS-001_UTF-8输出配置标准实现.md`
4. **Execute**: 按照DS-001标准配置UTF-8编码
5. **Constitution**: 验证符合§301.1通用输出编码

#### 示例3: "如何保证重构安全？"
1. **Neural Navigation**: `KNOWLEDGE_GRAPH.md` -> 安全簇 -> DS-005
2. **Related Nodes**: 发现 `related_to: [DS-006, DS-024]`
3. **Load Bundle**: 同时加载 DS-005 + DS-006 + DS-024
4. **Execute**: 执行完整的安全重构流程
5. **Audit**: 运行 `judicial_verify_structure` 验证架构同构

## 📈 性能与熵减指标

### 上下文占用目标
| 层级 | Token占用目标 | 实际占用 | 状态 |
|------|---------------|----------|------|
| **T0** | <800 tokens | ~600 tokens | ✅ 达标 |
| **T1** | <200 tokens | ~150 tokens | ✅ 达标 |
| **T2** | <100 tokens (每次) | ~50-80 tokens | ✅ 达标 |
| **T3** | 0 tokens (不加载) | 0 tokens | ✅ 达标 |

### 复杂度优化
- **原始复杂度**: $T_{\text{load}} = O(N)$，$N=96$个文件
- **优化后复杂度**: $T_{\text{load}} = O(1)$（索引查找）+ $O(\log k)$（图谱导航）
- **熵减效果**: $\Delta H = H_{\text{before}} - H_{\text{after}} > 0$ (符合§141)

### 检索性能
- **索引查找**: <100ms ($O(1)$复杂度)
- **图谱导航**: <50ms ($O(\log k)$复杂度)
- **文件加载**: <20ms (SSD读取)

## ⚖️ 宪法符合性验证

### 核心宪法条款
- **§10.6**: 文档分级公理 (本体系宪法化)
- **§152**: 单一真理源公理 (T0-T3分层管理)
- **§114**: 双存储同构公理 (物理与认知层对齐)
- **§125**: 数据完整性公理 (原子写入与释放)
- **§141**: 熵减验证 (分级体系降低认知熵)

### 三级司法验证
1. **Tier 1 (Structure)**: `judicial_verify_structure` - 验证 $S_{fs} \cong S_{doc}$
2. **Tier 2 (Signature)**: `judicial_verify_signatures` - 验证 $I_{code} \supseteq I_{doc}$
3. **Tier 3 (Behavior)**: `judicial_run_tests` - 验证 $B_{code} \equiv B_{spec}$

## 🔧 维护与更新协议

### 版本管理
- **主版本**: 与宪法版本同步 (当前: v6.8.0)
- **次版本**: 体系结构调整时更新
- **修订号**: 文档内容更新时递增

### 更新流程
1. **检测需求**: 系统熵值$H_{sys} > 0.3$时触发评估
2. **架构调整**: 更新分级体系定义
3. **宪法同步**: 更新§10.6条款
4. **状态记录**: 更新`activeContext.md`
5. **验证合规**: 运行三级司法验证

### 熵值监控
- **绿色区**: $H_{sys} \leq 0.2$ - 体系运行良好
- **黄色区**: $0.2 < H_{sys} \leq 0.4$ - 需要监控优化
- **红色区**: $H_{sys} > 0.4$ - 必须启动`WF-206`三位一体收敛协议

---

**维护者**: 监察部 - 逆熵实验室架构委员会  
**最后更新**: 2026-02-01  
**状态**: 🟢 **活跃 (与宪法v6.8.0同步)**  

*遵循逆熵实验室宪法约束: 认知即分层，注意力即资源。*