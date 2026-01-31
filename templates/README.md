# CDD 模板使用指南

## 模板结构

```
cdd/templates/
├── 01_basic_law_index.md           # 基本法索引（始终加载）
├── 02_procedural_law_index.md      # 程序法索引（始终加载）
├── 03_technical_law_index.md       # 技术法索引（始终加载）
├── activeContext.md                # 活动上下文模板
├── KNOWLEDGE_GRAPH.md              # 知识图谱模板
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

### 5. 定制化修改

根据项目需求修改：
- `activeContext.md` 中的项目名称、维护者
- `KNOWLEDGE_GRAPH.md` 中的项目特定节点
- 添加自定义的 DS-xxx 和 WF-xxx 文件

## 开发流程

### 启动开发

1. **加载索引内核** - 读取三个索引文件
2. **加载活动上下文** - 读取 `activeContext.md`
3. **计算系统熵值** - 输出 $H_{sys}$ 仪表盘

### 执行 CDD

1. **State A (基准摄入)** - 读取 systemPatterns/techContext/behaviorContext
2. **State B (文档规划)** - 先修改文档，等待用户批准
3. **State C (受控执行)** - 按文档执行代码修改
4. **State D (三级验证)** - 执行 Tier 1/2/3 验证
5. **State E (收敛纠错)** - 修正问题或完成任务

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
