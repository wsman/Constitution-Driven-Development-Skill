# CDD v1.5.0 (Ecosystem & Automation) 开发计划

**状态**: 🚀 Phase 2 Complete  
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

### Phase 2: 特性脚手架 (cdd-feature) ✅ 完成
| 任务 | 文件 | 状态 |
|------|------|------|
| 创建cdd-feature.py | `scripts/cdd-feature.py` | ✅ 已完成 |
| 自动编号逻辑 | `get_next_feature_id()` | ✅ 已完成 |
| Git分支创建 | `create_branch()` | ✅ 已完成 |
| 模板实例化 | `instantiate_templates()` | ✅ 已完成 |

### Phase 3: 宪法修正案 (WF-AMEND) ⏳ 待开始
| 任务 | 文件 | 状态 |
|------|------|------|
| 创建WF-AMEND协议 | `templates/protocols/WF-amend.md` | ⏳ 待开发 |
| 实现版本自动更新 | - | ⏳ 待开发 |
| 测试传播机制 | - | ⏳ 待测试 |

---

## ✅ Phase 2 完成内容

### cdd-feature.py 脚本
**文件**: `scripts/cdd-feature.py`

```bash
# 使用示例
python scripts/cdd-feature.py "Add User Login"
python scripts/cdd-feature.py "Integrate Stripe" --short-name "stripe"
```

**功能**:
- 自动编号 (扫描 specs/ 目录)
- Git 集成 (自动创建分支)
- 模板实例化 (DS-050/051/052)

### 使用方法

```bash
# 赋予执行权限
chmod +x scripts/cdd-feature.py

# 创建新特性
python scripts/cdd-feature.py "Add User Login"

# 输出
🚀 CDD Feature Scaffolding v1.5.0
   Feature: 001-add-user-login
   Description: Add User Login

🌿 Creating branch: 001-add-user-login
📄 Generating artifacts in specs/001-add-user-login/...
   ✅ DS-050_001_spec.md
   ✅ DS-051_001_plan.md
   ✅ DS-052_001_tasks.md

✅ Feature scaffolding complete!
   Directory: specs/001-add-user-login
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

**计划更新**: 2026-02-01 19:55  
**状态**: Phase 2 Complete, Phase 3 Ready
