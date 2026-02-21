# DS-054: 环境硬化标准

**版本**: v1.4.0  
**标准类型**: T2-DS实现标准  
**用途**: 环境配置验证与初始化  
**执行时机**: State C (任务执行前)  
**触发条件**: 技术栈检测完成后  
**最后更新**: {{timestamp}}

---

## 标准概述

**目的**: 在执行`DS-052`任务前，强制检查并生成项目环境配置文件，防止代码写完才发现配置缺失。

**核心原则**:
- **技术栈感知**: 根据项目实际技术栈生成对应ignore文件
- **增量验证**: 已存在文件仅补充缺失的关键模式
- **全面覆盖**: 覆盖主流编程语言、构建工具、容器化场景

---

## 执行流程

### Step 1: 技术栈检测

从项目检测技术栈（按优先级）：

| 检测信号 | 技术栈 |
|----------|--------|
| `package.json`, `node_modules/` | Node.js/JavaScript/TypeScript |
| `requirements.txt`, `setup.py`, `__pycache__/` | Python |
| `pom.xml`, `build.gradle`, `target/` | Java |
| `*.csproj`, `*.sln`, `bin/`, `obj/` | C#/.NET |
| `go.mod`, `vendor/` | Go |
| `Gemfile`, `vendor/bundle/` | Ruby |
| `composer.json`, `vendor/` | PHP |
| `Cargo.toml`, `target/` | Rust |
| `*.kt`, `build.gradle.kts`, `.gradle/` | Kotlin |
| `CMakeLists.txt`, `Makefile` | C/C++ |
| `Package.swift`, `*.xcodeproj` | Swift |
| `*.Rproj`, `renv/` | R |

### Step 2: Ignore文件检测与生成

#### 2.1 Git仓库检测

```bash
git rev-parse --git-dir 2>/dev/null
```

- **是Git仓库**: 生成/验证 `.gitignore`
- **非Git仓库**: 跳过 `.gitignore`，仅处理其他ignore文件

#### 2.2 Ignore文件矩阵

| 技术栈 | .gitignore | .dockerignore | .eslintignore | .prettierignore | 其他 |
|--------|------------|---------------|---------------|-----------------|------|
| Node.js | ✅ | ✅ | ✅ | ✅ | .npmignore |
| Python | ✅ | ✅ | - | - | |
| Java | ✅ | ✅ | - | - | |
| Go | ✅ | ✅ | - | - | |
| Rust | ✅ | ✅ | - | - | |
| Docker通用 | - | ✅ | - | - | |
| Terraform | ✅ | - | - | - | .terraformignore |
| Kubernetes | ✅ | - | - | - | |

### Step 3: 关键模式清单

#### 3.1 通用模式 (所有项目)

```
# OS Generated
.DS_Store
Thumbs.db
*.tmp
*.swp
*~

# IDE
.vscode/
.idea/
*.swp
*.swo

# Secrets
.env*
*.pem
*.key
*.crt
```

#### 3.2 技术栈特定模式

##### Node.js/JavaScript/TypeScript
```
node_modules/
dist/
build/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
coverage/
.nyc_output/
```

##### Python
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.venv/
venv/
ENV/
```

##### Java
```
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar
!.mvn/wrapper/maven-wrapper.properties
*.class
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar
```

##### Go
```
*.exe
*.exe~
*.test
*.out
vendor/
go.work
```

##### Rust
```
target/
Cargo.lock
**/*.rs.bk
*.rlib
*.prof
*.profraw
```

##### Docker (通用)
```
.git/
.gitignore
.gitattributes
!.gitignore
!.gitattributes
Dockerfile*
docker-compose*
*.log
*.md
docs/
tests/
*_test.go
*_mock.go
Makefile
```

##### Lint工具

**ESLint**:
```
node_modules/
dist/
build/
coverage/
*.min.js
*.bundle.js
```

**Prettier**:
```
node_modules/
dist/
build/
coverage/
package-lock.json
yarn.lock
pnpm-lock.yaml
```

##### Terraform
```
*.tfstate
*.tfstate.*
*.tfvars
*.tfvars.json
crash.log
crash.*.log
*.retry
.hclfmt/*
*.backup
/.terraform/
*.plan
*.plan.json
```

### Step 4: 验证与补充逻辑

#### 4.1 文件已存在

```bash
# 检查现有文件
if [ -f ".gitignore" ]; then
    # 读取现有内容，补充缺失的关键模式
    grep -q "node_modules/" .gitignore || echo "node_modules/" >> .gitignore
fi
```

**原则**: 仅追加缺失的关键模式，保留用户自定义内容

#### 4.2 文件不存在

```bash
# 根据检测到的技术栈生成完整ignore文件
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Universal
.DS_Store
Thumbs.db
*.tmp
*.swp
.vscode/
.idea/

# [检测到的技术栈模式]
EOF
fi
```

---

## 执行检查清单

### 执行前检查

- [ ] 检测项目技术栈
- [ ] 识别已有ignore文件
- [ ] 确定需要生成/验证的文件列表

### Gitignore检查

- [ ] 基础OS/IDE模式存在
- [ ] 技术栈特定模式存在
- [ ] 敏感文件(.env*, *.key)已排除

### Docker检查 (如适用)

- [ ] `.dockerignore` 存在
- [ ] 排除 `.git/` 和敏感文件
- [ ] 包含必要的构建上下文

### Lint配置检查

| 工具 | 检查项 |
|------|--------|
| ESLint | `.eslintignore` 存在且覆盖 `node_modules/`, `dist/` |
| Prettier | `.prettierignore` 存在且覆盖 lock 文件 |
| Terraform | `.terraformignore` 存在 (如使用TF) |

---

## 集成到CDD工作流

### State C (v1.4.0更新)

```
State C: 受控执行
├── 1. Environment Hardening (DS-054) ← 新增入口检查
│   ├── 检测技术栈
│   ├── 生成/验证 .gitignore
│   ├── 生成/验证 .dockerignore (如适用)
│   └── 生成/验证 lint ignore文件 (如适用)
│
├── 2. Execute Tasks
│   ├── Setup Phase
│   ├── Tests Phase
│   ├── Core Phase
│   ├── Integration Phase
│   └── Polish Phase
```

### 触发配置

```yaml
environment_hardening:
  enabled: true
  mandatory: true  # 必须通过才能执行任务
  skip_patterns:
    - "*.docs"  # 文档任务可跳过
    - "*.refactor"  # 重构任务可跳过
```

---

## 错误处理

| 场景 | 处理 |
|------|------|
| Git仓库但无.gitignore | 生成标准模板 |
| Docker存在但无.dockerignore | 生成Docker通用模板 |
| ESLint配置存在但无.eslintignore | 生成标准ESLint ignore |
| 多种技术栈混合 | 合并所有相关模式 |

---

## 输出报告

执行完成后输出：

```markdown
## 环境硬化报告

**时间**: {{TIMESTAMP}}  
**技术栈**: Node.js + TypeScript

### 文件状态

| 文件 | 状态 | 操作 |
|------|------|------|
| .gitignore | ✅ 已生成 | 新建 |
| .dockerignore | ✅ 已生成 | 新建 |
| .eslintignore | ⚠️ 已补充 | 追加3条 |
| .prettierignore | ✅ 已存在 | 无需修改 |

### 模式统计

- 总模式数: 47
- 新增: 32
- 保留: 15

### 建议

- ✅ 环境配置完成，可安全执行任务
- ℹ️ 建议运行 `npm install` 确保依赖完整
```

---

**标准版本**: v1.3.2  
**最后更新**: {{TIMESTAMP}}  
**来源**: spec-kit implement.md §4

---

### Step 5: 自定义跳过机制 (v1.4.0增强)

对于边缘技术栈或高度定制化环境，提供声明式跳过配置：

#### 5.1 跳过语法

在项目根目录创建 `.cddignore` 文件：

```yaml
# CDD Environment Hardening Skip Config
version: "1.0"

skip:
  checks:
    - ".dockerignore"
    - ".eslintignore"
  all: false
  
reason: "Legacy project with custom build system"
```

#### 5.2 跳过优先级

| 场景 | 处理逻辑 |
|------|----------|
| `.cddignore` + `all: true` | 跳过整个DS-054阶段 |
| `.cddignore` + `checks` | 跳过指定检查项 |
| 无 `.cddignore` | 执行完整环境硬化 |

#### 5.3 安全红线 (不可跳过)

- `.gitignore` 基础模式
- 敏感文件 (`.env*`, `*.key`, `*.pem`)
