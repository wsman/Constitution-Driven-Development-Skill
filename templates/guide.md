# CDD 模板使用指南

## 模板结构

```
cdd/templates/
├── 01_basic_law_index.md           # 基本法索引（始终加载）
├── 02_procedural_law_index.md      # 程序法索引（始终加载）
├── 03_technical_law_index.md       # 技术法索引（始终加载）
├── activeContext.md                # 活动上下文模板
├── KNOWLEDGE_GRAPH.md              # 知识图谱模板
├── cdd_config.yaml                 # CDD配置文件（外部审计者/API配置）
├── guide.md                        # ⭐ 模板使用指南
├── readme_template.md              # ⭐ 项目背景文档模板（非T0级别）
└── memory_bank/                    # 完整 Memory Bank 结构
    ├── 00_indices/
    ├── 01_active_state/
    ├── 02_systemaxioms/
    └── 03_protocols/
        ├── workflows/
        └── standards/
```

## 使用方法

### 1. 创建项目 Memory Bank

在项目根目录创建 `memory_bank` 文件夹：

```bash
mkdir -p memory_bank/00_indices
mkdir -p memory_bank/01_active_state
mkdir -p memory_bank/02_systemaxioms
mkdir -p memory_bank/03_protocols/workflows
mkdir -p memory_bank/03_protocols/standards
```

### 2. 复制索引文件

将三个索引文件复制到 `memory_bank/00_indices/`：

```bash
cp templates/01_basic_law_index.md memory_bank/00_indices/
cp templates/02_procedural_law_index.md memory_bank/00_indices/
cp templates/03_technical_law_index.md memory_bank/00_indices/
```

### 3. ⭐ 创建项目README.md (项目背景文档)

**在项目根目录创建** `README.md`（与 `memory_bank/` 同级）：

```bash
cp templates/README_PROJECT.md README.md
```

编辑 `README.md`，填入项目背景信息：
- 项目名称和描述
- 技术栈概览
- 核心功能列表
- 外部依赖说明

**注意**: README.md 不属于T0级别文档，是项目背景说明文档。
**模板来源**: `templates/readme_template.md`

### 3. 创建活动上下文

复制模板到 `memory_bank/01_active_state/activeContext.md`：

```bash
cp templates/activeContext.md memory_bank/01_active_state/activeContext.md
```

### 4. (可选) 创建知识图谱

复制模板到 `memory_bank/02_systemaxioms/KNOWLEDGE_GRAPH.md`：

```bash
cp templates/KNOWLEDGE_GRAPH.md memory_bank/02_systemaxioms/
```

### 5. (可选) 创建配置文件

复制配置文件到 `memory_bank/cdd_config.yaml`：

```bash
cp templates/cdd_config.yaml memory_bank/cdd_config.yaml
```

### 6. 配置外部审计者

编辑 `memory_bank/cdd_config.yaml`，配置 DeepSeek 深度推理模型：

```yaml
external_auditor:
  enabled: true
  model: "deepseek-reasoner"
  api:
    base_url: "https://api.deepseek.com"
    api_key: "${DEEPSEEK_API_KEY}"  # 或直接填入API密钥
```

### 7. 定制化修改

根据项目需求修改：
- `activeContext.md` 中的项目名称、维护者
- `KNOWLEDGE_GRAPH.md` 中的项目特定节点
- `cdd_config.yaml` 中的审计策略
- 添加自定义的 DS-xxx 和 WF-xxx 文件

## 开发流程 [v1.1.0更新]

### 启动开发 (Bootloader Sequence) [v1.1.0更新]

1. **Phase 1: 引导输入** - 加载 `README.md`，提取项目背景注入 `activeContext.md`
2. **Phase 2: 内核加载** - 加载 5 个 T0 核心文档
3. **Phase 3: 熵值校准** - 计算 $H_{sys}$ (含 $H_{align}$ 检查)

**关于 README.md 的定位**:
- 角色: 引导加载器输入 (Bootloader Input)
- 生命周期: 仅在会话初始化阶段存在
- 作用: 为 `activeContext.md` 提供初始"世界观"，防止冷启动幻觉

### 执行 CDD

1. **State A (基准摄入)** - 读取 systemPatterns/techContext/behaviorContext
2. **State B (文档规划)** - 先修改文档，等待用户批准
3. **State C (受控执行)** - 按文档执行代码修改
4. **State D (三级验证)** - Tier 1(结构) -> Tier 2(签名) -> Tier 3(行为)
5. **State E (收敛纠错)** - 确保 $H_{sys} \leq 0.3$

### T0文档变更与外部审计 ⭐

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

### 结束开发

1. **更新活动上下文** - 记录任务状态
2. **计算系统熵值** - 更新 $H_{sys}$
3. **释放临时引用** - 保持索引内核

## 文件说明

### 索引文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `01_basic_law_index.md` | <500 tokens | 基本法核心公理 |
| `02_procedural_law_index.md` | <300 tokens | 程序法工作流索引 |
| `03_technical_law_index.md` | <500 tokens | 技术法标准索引 |

### 配置文件

| 文件 | 说明 |
|------|------|
| `cdd_config.yaml` | 外部审计者配置 (DeepSeek API) |

### 核心原则

- ✅ 每一步操作前加载索引内核
- ✅ 按需加载 DS-xxx/WF-xxx 文件
- ✅ 执行完成后释放临时文件
- ❌ 禁止加载完整法典
- ❌ 禁止保留超过 3 个索引文件

## 熵值监控

### 每次加载上下文时

```markdown
## System Health Report

| 指标 | 值 | 评分 |
|------|-----|------|
| $H_{sys}$ (系统熵) | 0.00 | 🟢 |
| $T_{load}$ (Token占用) | 0 / 8000 | 0% |
| $N_{linked}/N_{total}$ (关联度) | 0 / 0 | 0% |
| $F_{drift}/F_{total}$ (漂移率) | 0 / 0 | 0% |
```

### 健康标准

| $H_{sys}$ 范围 | 状态 | 行动 |
|----------------|------|------|
| 0.0 - 0.3 | 🟢 优秀 | 保持现状 |
| 0.3 - 0.5 | 🟡 良好 | 关注负载 |
| 0.5 - 0.7 | 🟠 警告 | 优化结构 |
| 0.7 - 1.0 | 🔴 危险 | 立即整理 |

---

*遵循宪法驱动开发: 代码即数学证明，架构即宪法约束。*
