# WF-SYNC-ISSUES: GitHub Issues 同步协议

**版本**: v1.5.0  
**协议类型**: T2-工作流协议  
**来源**: Spec-Kit taskstoissues.md  
**触发**: State B (Tasking结束) 或 State C (执行中)  
**工具依赖**: `github-mcp-server`

---

## 1. 目标

将 `DS-052` (原子任务清单) 中的 Markdown 任务自动转换为 GitHub Issues，并保持双向链接，实现"文档即管理"。

## 2. 前置检查

1. **Git Remote**: 必须配置了 `remote.origin.url` 指向 GitHub。
2. **MCP Server**: GitHub MCP Server 必须处于活跃状态。
3. **DS-052**: 必须存在 `memory_bank/standards/DS-052_atomic_tasks.md`。

## 3. 执行流程

### Step 1: 解析任务 (Parse)

扫描 `DS-052` 中未标记 Issue ID 的任务：

| 模式 | 匹配 | 说明 |
|------|------|------|
| `- [ ] {Task}` | ✅ 新任务 | 无Issue链接，需要同步 |
| `- [ ] {Task} [#123]` | ⏭️ 已同步 | 已有Issue链接，跳过 |
| `- [x] {Task}` | ⏭️ 已完成 | 跳过已完成任务 |

### Step 2: 创建 Issue (Sync)

对每个新任务调用 GitHub API：

```markdown
**Title**: `[Task] {Task Description}`

**Body**:
```markdown
**Origin**: Generated from CDD DS-052
**Context**: See `memory_bank/standards/DS-052_atomic_tasks.md`
**Related Spec**: DS-050_feature_specification.md

{Task Description}
```
```

**Labels**: `cdd-task`, `feature-{feature-id}`

### Step 3: 回写链接 (Write Back)

获取创建的 Issue Number (e.g., `101`)，更新 `DS-052`：

| Before | After |
|--------|-------|
| `- [ ] 实现用户登录接口` | `- [ ] 实现用户登录接口 [#101]` |
| `- [ ] T002: 添加JWT生成` | `- [ ] T002: 添加JWT生成 [#102]` |

## 4. 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| **Remote Mismatch** | 终止并警告："Remote不是GitHub仓库" |
| **API Rate Limit** | 暂停并提示用户 |
| **MCP Server不可用** | 跳过同步，记录警告 |
| **Issue创建失败** | 记录错误，继续处理下一任务 |

## 5. 配置选项

在 `cdd_config.yaml` 中配置：

```yaml
github_integration:
  enabled: true
  sync_on_state_b: true  # State B完成后自动同步
  sync_on_demand: true   # 支持手动触发
  labels:
    - "cdd-task"
    - "automated"
  behavior: "create_and_link"  # create | link_only
```

## 6. 示例输出

```markdown
## DS-052: 原子任务清单

- [ ] T001: 定义 User Schema [#12]
- [ ] T002: 编写 API 测试用例 [#13]
- [ ] T003: 实现用户认证接口 [#14]
- [x] T004: 集成测试通过
```

---

**协议版本**: v1.5.0  
**最后更新**: {{TIMESTAMP}}
