# CDD v1.5.0 (Ecosystem & Automation) 开发计划

**状态**: 🚀 Phase 1 In Progress  
**版本**: v1.5.0  
**代号**: Ecosystem & Automation  
**目标**: 将"单机版文档治理"升级为"与外部生态(GitHub/Git)联动的自动化治理"

---

## 📅 实施路线图

### Phase 1: GitHub Issues同步 (WF-SYNC-ISSUES) ✅ 完成
| 任务 | 文件 | 状态 |
|------|------|------|
| 创建WF-SYNC-ISSUES协议 | `templates/protocols/WF-sync-issues.md` | ✅ 已完成 |
| 配置github-mcp集成 | `cdd_config.yaml` (v1.5.0) | ✅ 已完成 |
| 更新规划文档 | `PLANNING_v1.5.0_ECOSYSTEM_INTEGRATION.md` | ✅ 已完成 |

### Phase 2: 特性脚手架 (cdd-feature) ⏳ 待开始
| 任务 | 文件 | 状态 |
|------|------|------|
| 创建cdd-feature脚本 | `scripts/cdd-feature.sh` | ⏳ 待开发 |
| 更新State A流程 | `WF-201_cdd_workflow.md` | ⏳ 待更新 |
| 测试分支创建 | - | ⏳ 待测试 |

### Phase 3: 宪法修正案 (WF-AMEND) ⏳ 待开始
| 任务 | 文件 | 状态 |
|------|------|------|
| 创建WF-AMEND协议 | `templates/protocols/WF-amend.md` | ⏳ 待开发 |
| 实现版本自动更新 | - | ⏳ 待开发 |
| 测试传播机制 | - | ⏳ 待测试 |

---

## ✅ Phase 1 完成内容

### 1. WF-SYNC-ISSUES 协议
**文件**: `templates/protocols/WF-sync-issues.md`

- 解析DS-052任务 (匹配 `- [ ]` 模式)
- 调用GitHub MCP Server创建Issue
- 回写Issue链接到DS-052
- 异常处理机制

### 2. cdd_config.yaml v1.5.0
**新增配置**:

```yaml
# GitHub 生态集成 (v1.5.0新增)
github_integration:
  enabled: true
  protocol: "templates/protocols/WF-sync-issues.md"
  sync_on_state_b: true        # State B完成后自动同步
  sync_on_demand: true         # 支持手动触发
  default_labels:
    - "cdd-task"
    - "automated"
  behavior: "create_and_link"
  task_prefix: "T"
```

---

## 🔧 依赖项

1. **github-mcp-server**: 用于GitHub API调用
2. **Git**: 分支管理
3. **Python 3**: 脚本语言

---

## 📊 预期效果

| 维度 | 改进 |
|------|------|
| **PM联动** | 任务自动同步到GitHub Issues |
| **生命周期** | 特性创建从5分钟→30秒 |
| **元治理** | 宪法变更传播自动化 |

---

**计划更新**: 2026-02-01 19:50  
**状态**: Phase 1 Complete, Phase 2 Ready
