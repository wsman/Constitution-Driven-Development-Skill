# CDD for Claude Code - 集成指南

**版本**: v2.0.0  
**最后更新**: 2026-02-21  
**宪法依据**: §309, §310

> 📘 **本文档是CDD与Claude Code集成的完整指南，包含斜杠命令、MCP服务器、工具配置等所有内容。**

---

## 📚 目录

1. [快速开始](#快速开始)
2. [斜杠命令](#斜杠命令)
3. [MCP服务器集成](#mcp服务器集成)
4. [工具配置](#工具配置)
5. [工作流集成](#工作流集成)
6. [故障排除](#故障排除)

---

## 🚀 快速开始

### 步骤 1: 环境准备

```bash
# 1. 确保Claude Code已安装
claude --version

# 2. 检查CDD环境
python scripts/cdd_check_env.py --fix
```

### 步骤 2: 配置CDD技能

```bash
# 1. 列出CDD工具
python scripts/cdd_claude_bridge.py --list-tools

# 2. 在Claude Code中加载CDD技能
# 方法A: 通过命令行
claude --skill /path/to/cdd/claude/skills/cdd-unified-workflow.skill

# 方法B: 通过Claude Code UI
# Settings → Skills → Add Skill → 选择 cdd-unified-workflow.skill
```

### 步骤 3: 验证集成

```bash
# 在Claude Code中运行
/cdd-workflow "测试CDD集成"

# 应该看到CDD工作流启动
```

---

## ⚡ 斜杠命令

CDD提供以下斜杠命令，用于快速执行常用操作。

### 命令列表

| 命令 | 语法 | 用途 | 宪法依据 |
|------|------|------|----------|
| `/cdd-workflow` | `/cdd-workflow <task>` | 启动完整5状态工作流 | §102, §310 |
| `/constitution-check` | `/constitution-check [--gate=1-4]` | 宪法合规检查 | §101, §100.3 |
| `/entropy-monitor` | `/entropy-monitor [--optimize]` | 熵值监控与优化 | §100.3 |
| `/code-review` | `/code-review <path>` | 代码审查 | §300.3 |
| `/checkpoint-save` | `/checkpoint-save [--note=...]` | 保存检查点 | §104 |
| `/checkpoint-restore` | `/checkpoint-restore --latest` | 恢复检查点 | §104 |
| `/theme-check` | `/theme-check <path> [--fix]` | §119主题合规检查 | §119 |
| `/feature-spec` | `/feature-spec <name>` | 生成特性规格 | §101 |

### 快捷别名

- `/cc` → `/constitution-check`
- `/em` → `/entropy-monitor`
- `/cw` → `/cdd-workflow`

### 命令详解

#### `/cdd-workflow` - 完整工作流

启动完整的5状态工作流，从State A到State E。

```bash
# 基本用法
/cdd-workflow "开发用户登录功能"

# 指定目标项目
/cdd-workflow "开发用户登录功能" --target /path/to/project

# 跳过某些步骤（谨慎使用）
/cdd-workflow "快速修复" --skip-audit
```

**工作流步骤**:
1. **State A**: 加载上下文和T0/T1文档
2. **State B**: 生成T2规格（DS-050, DS-051, DS-052）
3. **State C**: 实现已批准的规格
4. **State D**: 运行宪法审计（Gate 1-4）
5. **State E**: 更新检查点并闭环

#### `/constitution-check` - 宪法检查

检查项目的宪法合规性。

```bash
# 检查所有Gate
/constitution-check --gate all

# 只检查特定Gate
/constitution-check --gate 1,2,3

# 自动修复问题
/constitution-check --gate all --fix

# JSON格式输出
/constitution-check --format json
```

**Gate说明**:
- **Gate 1**: 版本一致性检查
- **Gate 2**: 行为验证（pytest测试）
- **Gate 3**: 熵值检查
- **Gate 4**: 语义审计（需要DeepSeek API）
- **Gate 5**: 宪法引用验证

#### `/entropy-monitor` - 熵值监控

监控和优化系统熵值。

```bash
# 查看当前熵值
/entropy-monitor

# 分析熵值热点
/entropy-monitor --analyze --top-n 10

# 生成优化计划
/entropy-monitor --optimize --dry-run

# 执行优化
/entropy-monitor --optimize
```

**熵值阈值**:
- 🟢 优秀: 0.0 - 0.3
- 🟡 良好: 0.3 - 0.5
- 🟠 警告: 0.5 - 0.7
- 🔴 危险: > 0.7

#### `/code-review` - 代码审查

对指定代码进行审查。

```bash
# 审查单个文件
/code-review src/user.py

# 审查整个目录
/code-review src/

# 审查最近修改的文件
/code-review --recent

# 自动修复发现的问题
/code-review src/user.py --fix
```

#### `/checkpoint-save` - 保存检查点

保存当前工作状态。

```bash
# 保存检查点
/checkpoint-save

# 添加备注
/checkpoint-save --note "完成了用户认证功能"

# 自动保存（定期）
/checkpoint-save --auto --interval 3600  # 每小时
```

#### `/checkpoint-restore` - 恢复检查点

从检查点恢复工作状态。

```bash
# 恢复最新检查点
/checkpoint-restore --latest

# 列出所有检查点
/checkpoint-restore --list

# 恢复特定检查点
/checkpoint-restore --id checkpoint_20260221_120000
```

#### `/theme-check` - 主题检查

检查代码是否符合Nordic主题规范（§119）。

```bash
# 检查主题合规性
/theme-check src/styles/

# 自动修复主题问题
/theme-check src/styles/ --fix

# 检查特定颜色使用
/theme-check src/styles/ --check-color --bg-primary
```

#### `/feature-spec` - 生成特性规格

为指定特性生成T2规格文档。

```bash
# 生成特性规格
/feature-spec "用户登录系统"

# 指定模板
/feature-spec "用户登录系统" --template DS-050

# 预览而不生成
/feature-spec "用户登录系统" --dry-run
```

---

## 🔌 MCP服务器集成

### 什么是MCP服务器？

MCP（Model Context Protocol）服务器允许Claude Code与外部服务和工具集成。

### 推荐的MCP服务器

#### 1. Git MCP

**用途**: 版本控制集成，查看提交历史、分支管理等。

**安装**:
```bash
claude mcp add git -- npx -y @modelcontextprotocol/server-git
```

**使用**:
```bash
# 在Claude Code中
"查看最近的git提交"
"创建新分支feature/login"
```

#### 2. GitHub MCP

**用途**: GitHub API集成，查看Issues、PRs、Actions等。

**安装**:
```bash
claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

**配置**:
```yaml
# 在 ~/.config/claude/mcp_config.yaml 中添加
github:
  accessToken: "your-github-token"
```

**使用**:
```bash
# 在Claude Code中
"查看我的GitHub Issues"
"创建新的Pull Request"
```

#### 3. Sentry MCP

**用途**: 错误监控集成，查看Sentry错误报告。

**安装**:
```bash
claude mcp add sentry -- npx -y @modelcontextprotocol/server-sentry
```

**配置**:
```yaml
# 在 ~/.config/claude/mcp_config.yaml 中添加
sentry:
  dsn: "your-sentry-dsn"
  authToken: "your-sentry-auth-token"
```

**使用**:
```bash
# 在Claude Code中
"查看最近的Sentry错误"
"分析错误趋势"
```

### MCP配置文件

配置文件位置: `~/.config/claude/mcp_config.yaml`

```yaml
# 示例配置
mcpServers:
  git:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-git"]
    env: {}
  
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_ACCESS_TOKEN: "your-token-here"
  
  sentry:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-sentry"]
    env:
      SENTRY_DSN: "your-dsn-here"
      SENTRY_AUTH_TOKEN: "your-auth-token"
```

### 验证MCP集成

```bash
# 检查MCP服务器状态
claude mcp list

# 测试MCP连接
claude mcp test github

# 查看MCP日志
claude mcp logs
```

---

## 🛠️ 工具配置

### CDD工具桥接器

CDD通过工具桥接器与Claude Code集成，确保文件操作的安全性和原子性。

#### 可用工具

| 工具 | 函数 | 用途 | 宪法依据 |
|------|------|------|----------|
| `cdd_audit` | `audit_gates_claude()` | 审计Gate 1-5 | §100.3 |
| `cdd_feature` | `create_feature_claude()` | 创建特性 | §101 |
| `cdd_feature` | `deploy_project_claude()` | 部署项目 | §106.1 |
| `cdd_entropy` | `measure_entropy_claude()` | 测量熵值 | §102 |
| `cdd_entropy` | `analyze_entropy_claude()` | 分析熵值 | §102 |
| `cdd_env` | `check_environment_claude()` | 环境检查 | §100.3 |

#### 工具调用示例

```python
# 在Claude Code中调用工具
{
  "tool": "cdd_audit",
  "parameters": {
    "gates": "all",
    "fix": false,
    "target": "/path/to/project"
  }
}
```

### 工具配置文件

配置文件位置: `claude/mcp_config.yaml`

```yaml
# CDD MCP服务器配置
mcpServers:
  cdd-audit:
    command: python
    args: ["/path/to/cdd/scripts/cdd_auditor.py"]
    env: {}
  
  cdd-feature:
    command: python
    args: ["/path/to/cdd/scripts/cdd_feature.py"]
    env: {}
  
  cdd-entropy:
    command: python
    args: ["/path/to/cdd/scripts/cdd_entropy.py"]
    env: {}
```

---

## 🔄 工作流集成

### 5状态工作流自动化

CDD提供完整的5状态工作流自动化脚本，位于 `claude/workflows/` 目录。

#### 工作流文件

| 文件 | 说明 | 状态转换 |
|------|------|----------|
| `state_a_to_b_transition.yaml` | State A → State B | 加载上下文 → 生成规格 |
| `state_b_to_c_transition.yaml` | State B → State C | 规格批准 → 开始编码 |
| `state_c_to_d_verification.yaml` | State C → State D | 编码完成 → 运行审计 |
| `state_d_to_e_closing.yaml` | State D → State E | 审计通过 → 闭环 |

#### 使用工作流

```bash
# 方法1: 通过斜杠命令
/cdd-workflow "我的任务"

# 方法2: 直接加载工作流
claude --workflow claude/workflows/state_a_to_b_transition.yaml

# 方法3: 在Claude Code中
"加载CDD工作流: state_a_to_b"
```

### GitHub Actions集成

CDD提供CI/CD工作流模板，位于 `claude/github_actions/` 目录。

#### Constitution Check工作流

文件: `claude/github_actions/constitution-check.yml`

```yaml
name: CDD Constitution Check
on: [push, pull_request]
jobs:
  constitution-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run CDD Audit
        run: |
          python /path/to/cdd/scripts/cdd_auditor.py --gate all
```

#### 使用GitHub Actions

1. 复制工作流文件到你的项目:
```bash
cp claude/github_actions/constitution-check.yml .github/workflows/
```

2. 提交到GitHub:
```bash
git add .github/workflows/constitution-check.yml
git commit -m "Add CDD constitution check"
git push
```

3. 在GitHub Actions中查看结果

### Hooks集成

CDD提供Claude Code Hooks，用于自动触发特定操作。

#### 可用Hooks

| Hook | 文件 | 触发时机 | 用途 |
|------|------|----------|------|
| 检查点恢复 | `checkpoint_recovery_hook.yaml` | 工作流启动时 | 从上次中断处继续 |
| 宪法约束注入 | `constitutional_constraint_injection_hook.yaml` | 每次请求时 | 注入宪法约束 |
| 错误处理恢复 | `error_handling_recovery_hook.yaml` | 错误发生时 | 自动恢复 |
| 项目状态仪表板 | `project_status_dashboard_hook.yaml` | 定期 | 显示项目状态 |

#### 配置Hooks

```bash
# 复制Hooks到Claude Code配置目录
cp claude/hooks/*.yaml ~/.config/claude/hooks/

# 或者通过命令行启用
claude hooks enable checkpoint_recovery
```

---

## 🆘 故障排除

### 问题1: 斜杠命令不响应

**症状**: 输入 `/cdd-workflow` 后无响应

**解决方案**:
```bash
# 1. 检查CDD技能是否已加载
claude --skill list

# 2. 重新加载CDD技能
claude --skill reload cdd-unified-workflow

# 3. 检查技能文件是否存在
ls -la claude/skills/cdd-unified-workflow.skill
```

### 问题2: MCP服务器连接失败

**症状**: "MCP server not responding"

**解决方案**:
```bash
# 1. 检查MCP配置
cat ~/.config/claude/mcp_config.yaml

# 2. 测试MCP连接
claude mcp test <server-name>

# 3. 查看MCP日志
claude mcp logs

# 4. 重启Claude Code
claude --restart
```

### 问题3: 工具调用失败

**症状**: "Tool invocation failed"

**解决方案**:
```bash
# 1. 检查Python环境
python scripts/cdd_check_env.py

# 2. 手动测试工具
python scripts/cdd_auditor.py --gate all

# 3. 检查工具路径
python scripts/cdd_claude_bridge.py --list-tools

# 4. 查看详细错误
claude --verbose /cdd-workflow "test"
```

### 问题4: 宪法审计失败

**症状**: Gate审计失败，退出码非0

**解决方案**:
```bash
# 1. 运行详细审计
python scripts/cdd_auditor.py --gate all --verbose

# 2. 查看错误恢复指南
cat reference.md  # 故障排除章节

# 3. 尝试自动修复
python scripts/cdd_auditor.py --gate 1 --fix
```

### 问题5: 熵值过高

**症状**: H_sys > 0.7，无法继续开发

**解决方案**:
```bash
# 1. 分析熵值热点
python scripts/cdd_entropy.py analyze --top-n 10

# 2. 生成优化计划
python scripts/cdd_entropy.py optimize --dry-run

# 3. 执行优化
python scripts/cdd_entropy.py optimize

# 4. 验证熵值降低
python scripts/cdd_entropy.py calculate
```

---

## 📚 相关文档

- **[SKILL.md](../SKILL.md)** - AI代理完整操作手册
- **[reference.md](../reference.md)** - 完整参考手册（操作指南 + 宪法与故障排除）

---

**宪法依据**: §309, §310  
**文件状态**: 🟢 活跃  
**更新日期**: 2026-02-21