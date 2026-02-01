# CDD v1.5.0 迁移指南 (Migration Guide)

**适用对象**: 从 v1.4.0 升级到 v1.5.0 的项目  
**发布日期**: 2026-02-01  
**CDD版本**: v1.5.0 (Ecosystem & Automation)

---

## 🚀 核心变更摘要

v1.5.0 引入了**生态集成**能力，不再是纯静态文档管理。

| 变更 | 描述 |
|------|------|
| **脚本化** | 新增 `scripts/cdd-feature.py` 用于自动创建特性 |
| **GitHub同步** | 新增 `WF-sync-issues.md` 用于同步任务到Issue |
| **配置更新** | `cdd_config.yaml` 增加了 `github_integration` 和 `governance` 字段 |
| **治理协议** | 新增 `WF-amend.md` 宪法修正案协议 |

---

## 🛠️ 迁移步骤 (Step-by-Step)

### 1. 更新配置文件

请将您的 `cdd_config.yaml` 更新为以下结构，增加 v1.5.0 新字段：

```yaml
# ... (保留原 v1.4.0 配置)

# [New v1.5.0] GitHub 集成
github_integration:
  enabled: true
  protocol: "templates/protocols/WF-sync-issues.md"
  sync_behavior: "create_and_link"

# [New v1.5.0] 治理配置
governance:
  amendment_protocol: "templates/protocols/WF-amend.md"
  versioning_scheme: "semver"
```

### 2. 部署新脚本

1. 复制 `scripts/cdd-feature.py` 到您的项目 `scripts/` 目录
2. 赋予执行权限:
```bash
chmod +x scripts/cdd-feature.py
```

3. 确保您的项目根目录下有 `templates/standards/` 目录，且包含 DS-050/051/052 模板

### 3. 部署新协议

将以下文件复制到 `templates/protocols/`:

- `WF-sync-issues.md`
- `WF-amend.md`

### 4. 验证安装

运行脚本测试：

```bash
./scripts/cdd-feature.py --dry-run "Test Feature"
```

如果输出 `🚀 Initializing Feature...` 则说明环境配置正确。

---

## 📖 脚本使用方法

### 基本用法

```bash
# 创建新特性
python scripts/cdd-feature.py "Add User Login"

# 干运行（不实际创建）
python scripts/cdd-feature.py "Add User Login" --dry-run
```

### 输出示例

```
🚀 Initializing Feature: 001-add-user-login
🌿 Creating branch: 001-add-user-login
📄 Generating artifacts in specs/001-add-user-login/...
   ✅ DS-050_001_spec.md
   ✅ DS-051_001_plan.md
   ✅ DS-052_001_tasks.md

✨ Feature scaffolding complete!
   Work directory: specs/001-add-user-login
```

---

## ⚠️ 常见问题 (FAQ)

**Q: 我必须使用 GitHub 吗？**

A: 不强制。`WF-sync-issues` 是可选协议。如果不需要，可以在 config 中设为 `enabled: false`。

**Q: 旧的 specs 目录结构怎么处理？**

A: `cdd-feature.py` 兼容旧结构，它会自动扫描 `specs/` 下的文件夹来计算下一个 ID。建议将旧特性手动重命名为 `00x-name` 格式以便脚本识别。

**Q: 脚本需要什么环境？**

A: 需要 Python 3.6+ 和 Git（可选，用于分支创建）。

**Q: 如何自定义模板？**

A: 修改 `templates/standards/` 目录下的 DS-050/051/052 模板文件。

---

## 📋 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.5.0 | 2026-02-01 | 初始发布：生态集成、脚本化脚手架 |
| v1.4.0 | 2026-01-31 | 质量与治理集成 |

---

**文档版本**: v1.5.0  
**最后更新**: {{TIMESTAMP}}
