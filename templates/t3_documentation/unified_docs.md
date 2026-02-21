# CDD T3 Documentation Index

> **Template Version**: 1.0.0  
> **Last Updated**: {{TIMESTAMP}}  
> **Location**: `memory_bank/t3_documentation/`  
> **Level**: T3 (User & Developer Documentation)

## 📚 文档体系概述

本项目采用 **CDD (Constitution-Driven Development)** 文档体系，所有文档统一存放在 `memory_bank/` 目录下。

### CDD 文档层级

| 层级 | 目录 | 用途 | 主要受众 |
|------|------|------|----------|
| **T0** | `../t0_core/` | 核心宪法文档 (每次会话加载) | AI Agents, 系统架构师 |
| **T1** | `../t1_axioms/` | 公理层 (技术上下文、行为模式) | AI Agents, 高级开发者 |
| **T2** | `../t2_protocols/`, `../t2_standards/` | 工作流协议、实现标准 | 开发者, 技术负责人 |
| **T3** | `./` | 用户和开发者文档 (本层级) | 用户, 开发者, DevOps |

## 📖 文档索引

### 入门指南

| 文档 | 描述 | 状态 |
|------|------|------|
| [快速入门](./quickstart.md) | 安装、配置和启动项目 | 📝 待填充 |
| [开发入门](./getting-started.md) | 开发环境配置 | 📝 待填充 |

### 架构文档

| 文档 | 描述 | 状态 |
|------|------|------|
| [架构概览](./overview.md) | 系统架构和技术栈 | 📝 待填充 |
| [模块化架构](./modular-architecture.md) | 模块化设计详情 | 📝 待填充 |

### API 文档

| 文档 | 描述 | 状态 |
|------|------|------|
| [API 参考](./api-reference.md) | REST 和 WebSocket API 完整参考 | 📝 待填充 |
| [后端 API](./backend-api.md) | 后端接口详情 | 📝 待填充 |

### 部署运维

| 文档 | 描述 | 状态 |
|------|------|------|
| [部署指南](./deployment.md) | 开发、生产环境部署指南 | 📝 待填充 |

### 模板

| 文档 | 描述 | 状态 |
|------|------|------|
| [文档模板](./document-template.md) | 创建新 T3 文档的模板 | 📝 待填充 |

## 🏗️ 项目结构

```
{{PROJECT_NAME}}/
├── src/                    # 源码目录
│   ├── main/              # 主应用代码
│   └── test/              # 测试代码
├── config/                # 配置文件
│   ├── environments/      # 环境配置
│   └── features/          # 功能开关
├── docs/                  # 项目文档（如有）
└── memory_bank/           # 📚 统一文档体系
    ├── t0_core/           # T0 核心宪法
    ├── t1_axioms/         # T1 公理层
    ├── t2_protocols/      # T2 工作流协议
    ├── t2_standards/      # T2 实现标准
    └── t3_documentation/  # T3 用户/开发者文档 (本目录)
```

## 📊 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| **v1.0.0** | {{TIMESTAMP}} | 初始版本，基于 CDD 模板创建 |

## 🔗 相关链接

- **项目 README**: `../../README.md`
- **变更日志**: `../../CHANGELOG.md`
- **CDD 规范**: Constitution-Driven Development v1.8.0

## 📋 T3 文档标准

### 格式要求
- **Markdown**: 标准 Markdown 语法，清晰的层级结构
- **结构**: 逻辑组织，包含目录表
- **示例**: 实用、可运行的代码示例
- **链接**: 有效的相对链接，包含描述性锚文本
- **图片**: 必要时添加，包含替代文本和标题

### 内容标准
- **用户导向**: 实用指导优先于理论概念
- **可操作**: 明确的步骤和预期结果
- **及时**: 版本特定的信息，定期更新
- **完整**: 主题的全面覆盖
- **易访问**: 清晰语言，避免不必要术语

### 元数据要求
每个 T3 文档应包含：
- 版本和最后更新日期
- 文档类别和目标受众
- 源位置（指向 `memory_bank/t3_documentation/` 目录）
- 状态指示器（当前、已弃用、进行中）

## 🔧 维护流程

### 更新流程
1. **源更新**: 更新 `memory_bank/t3_documentation/` 目录中的主文档
2. **链接验证**: 验证所有内部和外部链接
3. **版本更新**: 更新版本和最后更新信息
4. **一致性检查**: 确保 T3 文档准确反映源内容

### 版本控制策略
- **真相源**: `memory_bank/t3_documentation/` 目录包含权威内容
- **向后兼容**: 注明破坏性变更和迁移路径
- **弃用策略**: 明确标记已弃用文档并提供替代方案

### 质量控制
- **技术准确性**: 确保所有技术信息正确
- **链接有效性**: 定期检查所有链接
- **用户测试**: 从用户角度测试文档可用性
- **AI 代理测试**: 确保文档对 AI 系统可访问

## 🤝 贡献指南

### 添加新 T3 文档
1. **创建文档**: 在 `memory_bank/t3_documentation/` 目录中添加新文档
2. **更新索引**: 在本索引表中添加条目
3. **更新链接**: 确保所有相关文档链接正确

### 文档标准执行
- 遵循既定模板和格式
- 包含所有必需的元数据
- 使用一致的术语和命名约定
- 测试所有代码示例和命令

---

**T3 文档状态**: 📝 初始模板 (v1.0.0)  
**维护者**: {{PROJECT_NAME}} Team  
**CDD 框架**: v1.8.0  
**最后系统审计**: 待审计  
**文档数量**: 7 个核心文档模板

*文档版本: v2.0.0 | 更新日期: {{TIMESTAMP}}*# {{PROJECT_NAME}} 架构概览

> **版本**: 1.0.0  
> **最后更新**: {{TIMESTAMP}}  
> **类别**: 架构文档  
> **目标读者**: 架构师、技术负责人、高级开发者

## 🏗️ 系统架构

### 架构原则

{{PROJECT_NAME}} 基于以下核心架构原则构建：

1. **模块化设计**: 清晰的关注点分离，高内聚低耦合
2. **可扩展性**: 支持水平扩展和垂直扩展
3. **可维护性**: 代码组织清晰，文档完善
4. **可靠性**: 错误处理和容错机制
5. **安全性**: 纵深防御，最小权限原则

### 技术栈

#### 后端技术栈
- **语言**: Python 3.12+
- **Web 框架**: FastAPI / Django / Flask (根据实际选择)
- **数据库**: PostgreSQL / MySQL / SQLite
- **ORM**: SQLAlchemy / Django ORM
- **缓存**: Redis / Memcached
- **消息队列**: RabbitMQ / Redis Streams
- **任务队列**: Celery / RQ

#### 前端技术栈 (如果适用)
- **框架**: React 18+ / Vue 3 / Angular
- **构建工具**: Vite / Webpack
- **样式**: Tailwind CSS / CSS Modules
- **状态管理**: Redux / Zustand / Pinia
- **测试**: Jest / Vitest / Cypress

#### 基础设施
- **容器**: Docker, Docker Compose
- **编排**: Kubernetes (可选)
- **CI/CD**: GitHub Actions / GitLab CI
- **监控**: Prometheus, Grafana
- **日志**: ELK Stack / Loki

### 架构模式

#### 分层架构
```
┌─────────────────────────────────────┐
│         表示层 (Presentation)        │
│  ┌─────────────┐  ┌─────────────┐  │
│  │   Web API   │  │     UI      │  │
│  └─────────────┘  └─────────────┘  │
├─────────────────────────────────────┤
│         业务层 (Business)           │
│  ┌─────────────┐  ┌─────────────┐  │
│  │  服务逻辑   │  │  领域模型   │  │
│  └─────────────┘  └─────────────┘  │
├─────────────────────────────────────┤
│         数据层 (Data)               │
│  ┌─────────────┐  ┌─────────────┐  │
│  │   仓库层    │  │  数据访问   │  │
│  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────┘
```

#### 微服务架构 (可选)
```
┌─────────┐    ┌─────────┐    ┌─────────┐
│ 用户服务 │    │ 订单服务 │    │ 支付服务 │
└─────────┘    └─────────┘    └─────────┘
     │              │              │
     └──────────────┼──────────────┘
                    │
             ┌─────────────┐
             │   API网关   │
             └─────────────┘
                    │
             ┌─────────────┐
             │    客户端    │
             └─────────────┘
```

### 核心组件

#### 1. 认证与授权
- **身份验证**: JWT, OAuth 2.0, Session-based
- **授权**: RBAC (基于角色的访问控制)
- **安全**: HTTPS, CSRF 保护, CORS 配置

#### 2. 数据处理
- **数据库设计**: 规范化/反规范化平衡
- **缓存策略**: 多级缓存 (内存, Redis, CDN)
- **数据迁移**: Alembic / Django Migrations

#### 3. API 设计
- **RESTful 原则**: 资源导向，HTTP 语义
- **版本控制**: URL 版本或请求头版本
- **文档**: OpenAPI/Swagger 规范

#### 4. 前端架构 (如果适用)
- **组件设计**: 原子设计模式
- **状态管理**: 全局状态 vs 局部状态
- **路由**: 客户端路由，代码分割

### 部署架构

#### 开发环境
```yaml
开发环境:
  - 本地 Docker Compose
  - 热重载支持
  - 调试工具集成
```

#### 生产环境
```yaml
生产环境:
  - 容器化部署 (Docker)
  - 负载均衡 (Nginx/Traefik)
  - 自动伸缩
  - 蓝绿部署/金丝雀发布
```

### 数据流

#### 典型请求流程
```mermaid
graph TD
    A[客户端请求] --> B[负载均衡器]
    B --> C[Web 服务器]
    C --> D[应用服务器]
    D --> E{业务逻辑}
    E --> F[数据库查询]
    F --> G[缓存检查]
    G --> H[返回数据]
    H --> I[响应客户端]
```

#### 异步任务流程
```mermaid
graph LR
    A[用户操作] --> B[API 端点]
    B --> C[任务队列]
    C --> D[工作进程]
    D --> E[处理任务]
    E --> F[更新状态]
    F --> G[通知用户]
```

### 安全架构

#### 安全层次
1. **网络层**: 防火墙, VPN, 网络隔离
2. **应用层**: 输入验证, 输出编码, 会话管理
3. **数据层**: 加密, 访问控制, 审计日志
4. **基础设施**: 安全组, IAM 策略, 漏洞扫描

#### 合规性考虑
- **数据保护**: GDPR, CCPA
- **行业标准**: PCI DSS, HIPAA (如果适用)
- **安全认证**: ISO 27001, SOC 2

### 性能考量

#### 性能指标
- **响应时间**: P95 < 200ms, P99 < 500ms
- **吞吐量**: 根据业务需求定义
- **可用性**: 99.9% uptime SLA
- **可扩展性**: 支持 10x 流量增长

#### 优化策略
- **数据库优化**: 索引, 查询优化, 分库分表
- **缓存策略**: CDN, 内存缓存, 数据库缓存
- **代码优化**: 异步处理, 批处理, 懒加载

### 监控与运维

#### 监控体系
- **基础设施监控**: CPU, 内存, 磁盘, 网络
- **应用监控**: 请求率, 错误率, 延迟
- **业务监控**: 关键业务指标, 用户行为
- **日志收集**: 结构化日志, 分布式追踪

#### 告警策略
- **紧急告警**: 服务不可用, 数据丢失
- **警告告警**: 性能下降, 容量预警
- **信息告警**: 配置变更, 部署完成

### 扩展路线图

#### 短期扩展 (0-6个月)
1. 增加缓存层
2. 实现异步任务队列
3. 优化数据库查询
4. 添加监控告警

#### 中期扩展 (6-12个月)
1. 引入微服务架构
2. 实现多区域部署
3. 添加高级分析功能
4. 优化移动端体验

#### 长期扩展 (12+个月)
1. AI/ML 功能集成
2. 区块链/去中心化特性
3. 国际化支持
4. 生态平台建设

### 技术决策记录

#### 重要技术决策
| 决策 | 理由 | 备选方案 | 影响 |
|------|------|----------|------|
| 使用 FastAPI | 高性能, 异步支持, 自动文档 | Flask, Django | 开发效率提升 30% |
| 选择 PostgreSQL | ACID 合规, 丰富功能, 社区支持 | MySQL, MongoDB | 数据一致性保证 |
| 采用 Docker | 环境一致性, 部署简化 | 虚拟机, 裸机 | 部署时间减少 50% |

### 架构演进

#### 当前架构状态
- **成熟度**: 生产就绪
- **复杂度**: 中等
- **维护成本**: 低
- **团队熟悉度**: 高

#### 架构债务
1. **技术债务**: 需要重构的模块
2. **文档债务**: 需要完善的文档
3. **测试债务**: 需要增加的测试覆盖率

### 相关文档

- **详细设计文档**: `memory_bank/t3_documentation/modular-architecture.md`
- **API 文档**: `memory_bank/t3_documentation/api-reference.md`
- **部署指南**: `memory_bank/t3_documentation/deployment.md`
- **开发指南**: `memory_bank/t3_documentation/getting-started.md`

---

**架构状态**: ✅ 生产就绪 (v1.0.0)  
**架构复杂度**: 🟡 中等  
**技术债务**: 🟢 低  
**扩展性**: 🟢 良好

*文档版本: v2.0.0 | 更新日期: {{TIMESTAMP}}*# {{PROJECT_NAME}} 开发环境配置指南

> **版本**: 1.0.0  
> **最后更新**: {{TIMESTAMP}}  
> **类别**: 开发指南  
> **目标读者**: 开发者、贡献者

## 🛠️ 开发环境设置

本指南详细介绍如何为 {{PROJECT_NAME}} 设置完整的开发环境。

### 系统要求

#### 最低要求
- **操作系统**: Ubuntu 20.04+ / macOS 11+ / Windows 10+ (WSL2 推荐)
- **内存**: 8GB RAM (推荐 16GB+)
- **存储**: 20GB 可用空间
- **网络**: 稳定的互联网连接

#### 软件要求
- **Python**: 3.9, 3.10, 3.11, 3.12 (推荐 3.12)
- **Node.js**: 18.x, 20.x (如果项目使用前端)
- **Git**: 2.30+
- **Docker**: 20.10+ (可选，用于容器化开发)
- **数据库**: PostgreSQL 12+/MySQL 8+/SQLite 3.35+

### 环境配置步骤

#### 1. 系统级准备

##### Ubuntu/Debian
```bash
# 更新包管理器
sudo apt update && sudo apt upgrade -y

# 安装基础开发工具
sudo apt install -y build-essential curl wget git zsh fish \
    libssl-dev libffi-dev python3-dev python3-pip python3-venv \
    postgresql postgresql-contrib redis-server
```

##### macOS
```bash
# 安装 Homebrew (如果未安装)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装基础工具
brew install python@3.12 node@20 git postgresql redis
```

##### Windows (WSL2)
```bash
# 启用 WSL2
wsl --install -d Ubuntu

# 在 WSL 中运行 Ubuntu 设置脚本
# (参考 Ubuntu 部分)
```

#### 2. Python 环境配置

##### 创建虚拟环境
```bash
# 创建项目目录
mkdir -p ~/projects/{{PROJECT_NAME}}
cd ~/projects/{{PROJECT_NAME}}

# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
```

##### 配置 pip
```bash
# 升级 pip
pip install --upgrade pip

# 配置 pip 镜像源 (中国用户)
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
```

#### 3. 项目依赖安装

##### 安装开发依赖
```bash
# 克隆项目
git clone <repository-url> .
# 或如果是已有项目
cd {{PROJECT_NAME}}

# 安装项目依赖
pip install -r requirements.txt

# 安装开发依赖 (如果有)
pip install -r requirements-dev.txt

# 安装 pre-commit hooks
pre-commit install
```

##### 验证安装
```bash
# 检查 Python 版本
python --version

# 检查主要依赖
python -c "import django; print(f'Django: {django.__version__}')"  # 如果是 Django 项目
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"  # 如果是 FastAPI 项目
```

#### 4. 数据库配置

##### PostgreSQL (推荐)
```bash
# 创建数据库用户
sudo -u postgres createuser --createdb --createrole --superuser {{project_user}}
# 或
sudo -u postgres psql -c "CREATE USER {{project_user}} WITH PASSWORD 'secure_password';"

# 创建数据库
sudo -u postgres createdb {{project_name}}_dev

# 设置环境变量
echo "export DATABASE_URL=postgresql://{{project_user}}:secure_password@localhost/{{project_name}}_dev" >> ~/.bashrc
```

##### SQLite (简单项目)
```bash
# SQLite 不需要额外配置，只需确保文件可写
touch db.sqlite3
chmod 666 db.sqlite3
```

#### 5. 前端环境 (如果适用)

##### Node.js 环境
```bash
# 安装 Node Version Manager (nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 重新加载 shell
source ~/.bashrc  # 或 ~/.zshrc

# 安装 Node.js
nvm install 20
nvm use 20

# 验证安装
node --version
npm --version
```

##### 安装前端依赖
```bash
cd frontend  # 或 apps/frontend，根据项目结构
npm install
# 或
yarn install
# 或
pnpm install
```

#### 6. IDE 配置

##### VS Code 推荐扩展
```json
// .vscode/extensions.json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "ms-python.isort",
        "eamodio.gitlens",
        "ms-vscode.makefile-tools",
        "redhat.vscode-yaml",
        "ms-azuretools.vscode-docker",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
    ]
}
```

##### PyCharm 配置
- 设置 Python 解释器为虚拟环境
- 启用自动导入优化
- 配置代码风格为 PEP 8
- 设置测试运行器为 pytest

### 开发工作流

#### 1. 代码质量工具

##### 代码格式化
```bash
# 运行 black 格式化
black src/

# 运行 isort 排序导入
isort src/

# 运行 ruff linting
ruff check --fix src/
```

##### 类型检查
```bash
# 运行 mypy 类型检查
mypy src/

# 或使用 pyright
pyright src/
```

#### 2. 测试框架

##### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_models.py

# 运行带覆盖率的测试
pytest --cov=src --cov-report=html

# 运行性能测试
pytest tests/ -m "performance"
```

##### 测试数据库配置
```bash
# 创建测试数据库
createdb {{project_name}}_test

# 设置测试环境变量
export TEST_DATABASE_URL=postgresql://localhost/{{project_name}}_test
```

#### 3. 调试配置

##### VS Code 调试配置
```json
// .vscode/launch.json
{
    "version": "2.0.0",
    "configurations": [
        {
            "name": "Python: Debug",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

##### Python 调试
```python
# 在代码中添加断点
import pdb; pdb.set_trace()

# 或使用 ipdb (需要安装)
import ipdb; ipdb.set_trace()
```

### 环境验证

#### 完整验证脚本
```bash
#!/bin/bash
# 环境验证脚本

echo "🔍 验证 {{PROJECT_NAME}} 开发环境..."

# 1. 检查 Python
echo "1. 检查 Python..."
python --version
python -c "import sys; print(f'Python 路径: {sys.executable}')"

# 2. 检查虚拟环境
echo "2. 检查虚拟环境..."
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 虚拟环境已激活: $VIRTUAL_ENV"
else
    echo "❌ 虚拟环境未激活"
fi

# 3. 检查依赖
echo "3. 检查依赖..."
pip list | grep -E "(django|fastapi|flask|sqlalchemy)"

# 4. 检查数据库
echo "4. 检查数据库..."
if command -v psql &> /dev/null; then
    psql -c "\l" | grep {{project_name}}
fi

# 5. 运行基础测试
echo "5. 运行基础测试..."
pytest tests/test_environment.py -v

echo "✅ 环境验证完成！"
```

### 常见问题解决

#### 1. 虚拟环境问题
```bash
# 问题: 虚拟环境未激活
# 解决: 
source .venv/bin/activate

# 问题: 虚拟环境损坏
# 解决:
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2. 数据库连接问题
```bash
# 问题: PostgreSQL 连接失败
# 解决:
sudo systemctl restart postgresql
sudo -u postgres psql -c "ALTER USER {{project_user}} WITH PASSWORD 'new_password';"

# 问题: 权限问题
# 解决:
sudo chown -R $(whoami):$(whoami) ~/.pgpass
chmod 600 ~/.pgpass
```

#### 3. 依赖冲突
```bash
# 问题: 依赖版本冲突
# 解决:
pip install --upgrade pip-tools
pip-compile requirements.in
pip-sync

# 或使用 poetry
poetry install
```

### 高级配置

#### Docker 开发环境
```dockerfile
# Dockerfile.dev
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
```

#### 多环境配置
```bash
# 环境配置文件结构
config/
├── development.yaml
├── testing.yaml
├── staging.yaml
└── production.yaml
```

#### 监控和日志
```python
# 日志配置示例
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

### 下一步

成功配置开发环境后，您可以：

1. **探索项目结构**:
   ```bash
   tree -I '__pycache__|*.pyc|.git' -L 3
   ```

2. **阅读代码规范**:
   - 查看 `CONTRIBUTING.md`
   - 阅读项目编码规范

3. **运行完整测试套件**:
   ```bash
   make test-all
   ```

4. **开始第一个贡献**:
   - 查找 `good first issue` 标签
   - 从文档改进开始

---

**开发环境状态**: ✅ 完整指南 (v1.0.0)  
**支持平台**: Ubuntu, macOS, Windows (WSL2)  
**验证脚本**: 包含  
**预计配置时间**: 30-60 分钟

*文档版本: v2.0.0 | 更新日期: {{TIMESTAMP}}*# {{PROJECT_NAME}} 快速入门指南

> **版本**: 1.0.0  
> **最后更新**: {{TIMESTAMP}}  
> **类别**: 入门指南  
> **目标读者**: 新用户、开发者

## 🚀 快速启动

本指南将帮助您在几分钟内启动并运行 {{PROJECT_NAME}}。

### 环境要求

#### 基本要求
- **操作系统**: Linux/macOS/Windows (推荐 Linux/macOS)
- **Python**: 3.9+ (推荐 3.12+)
- **Node.js**: 18+ (如果项目包含前端部分)
- **包管理器**: pip, npm/yarn/pnpm (根据项目需求)
- **版本控制**: Git

#### 可选依赖
- **数据库**: PostgreSQL/MySQL/SQLite (根据项目需求)
- **缓存**: Redis/Memcached (根据项目需求)
- **消息队列**: RabbitMQ/Redis (根据项目需求)

### 安装步骤

#### 1. 克隆项目
```bash
git clone <repository-url>
cd {{PROJECT_NAME}}
```

#### 2. 创建虚拟环境 (推荐)
```bash
# 使用 venv
python -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

#### 3. 安装依赖
```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 如果项目包含前端，安装 Node.js 依赖
# cd frontend && npm install
```

#### 4. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，设置必要的配置
# 至少需要设置：
# - 数据库连接
# - API 密钥 (如果需要)
# - 调试模式
```

#### 5. 初始化数据库
```bash
# 运行数据库迁移
python manage.py migrate  # Django 项目
# 或
alembic upgrade head     # SQLAlchemy 项目
# 或根据项目文档执行相应命令
```

#### 6. 启动开发服务器

##### 后端启动
```bash
# 通用 Python 项目
python app.py
# 或
python main.py

# FastAPI 项目
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Django 项目
python manage.py runserver
```

##### 前端启动 (如果有)
```bash
cd frontend
npm run dev
# 或
yarn dev
```

### 验证安装

#### 健康检查
```bash
# 检查后端服务是否运行
curl http://localhost:8000/health
# 应该返回: {"status": "ok", "version": "2.0.0"}

# 检查前端服务是否运行
# 打开浏览器访问: http://localhost:3000
```

#### 基本功能测试
```bash
# 运行单元测试
pytest tests/ -v

# 或运行特定测试
python -m pytest tests/test_basic.py
```

### 常见问题

#### 1. 端口被占用
```bash
# 查找占用端口的进程
lsof -ti:8000
# 或
netstat -tulpn | grep :8000

# 停止进程
kill -9 <进程ID>

# 或使用其他端口
python app.py --port 8080
```

#### 2. 依赖安装失败
```bash
# 升级 pip
pip install --upgrade pip

# 使用清华镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用 conda
conda env create -f environment.yml
```

#### 3. 数据库连接失败
- 检查数据库服务是否启动
- 验证 .env 中的数据库配置
- 检查网络连接和防火墙设置

### 下一步

成功启动项目后，您可以：

1. **探索 API 文档**:
   - 访问: http://localhost:8000/docs (FastAPI)
   - 或 http://localhost:8000/swagger (其他框架)

2. **查看管理界面** (如果有):
   - 访问: http://localhost:8000/admin

3. **运行更多测试**:
   ```bash
   # 运行所有测试
   pytest

   # 运行集成测试
   pytest tests/integration/

   # 生成覆盖率报告
   pytest --cov=. --cov-report=html
   ```

4. **开始开发**:
   - 查看 `src/` 目录结构
   - 阅读项目架构文档
   - 了解编码规范和贡献指南

### 获取帮助

#### 遇到问题？
1. **查看详细文档**:
   - `memory_bank/t3_documentation/getting-started.md` (开发环境详细配置)
   - `memory_bank/t3_documentation/deployment.md` (部署指南)

2. **检查现有问题**:
   - 查看项目 Issues 页面
   - 搜索常见问题解决方案

3. **寻求帮助**:
   - 项目讨论区/论坛
   - Discord/Slack 频道
   - 提交新的 Issue

### 开发工作流

#### 典型开发流程
1. **拉取最新代码**:
   ```bash
   git pull origin main
   ```

2. **创建功能分支**:
   ```bash
   git checkout -b feature/new-feature
   ```

3. **进行开发**:
   ```bash
   # 编写代码
   # 运行测试
   pytest
   
   # 提交代码
   git add .
   git commit -m "feat: add new feature"
   ```

4. **推送到远程**:
   ```bash
   git push origin feature/new-feature
   ```

5. **创建 Pull Request**:
   - 在 GitHub/GitLab 上创建 PR
   - 等待代码审查和 CI 通过

### 工具推荐

#### 开发工具
- **编辑器**: VS Code, PyCharm, Vim
- **终端**: iTerm2 (macOS), Windows Terminal
- **数据库工具**: DBeaver, TablePlus, pgAdmin
- **API 测试**: Postman, Insomnia, curl

#### 调试工具
- **Python 调试**: pdb, ipdb, debugpy
- **浏览器调试**: Chrome DevTools
- **网络调试**: Wireshark, tcpdump

---

**快速入门状态**: ✅ 完成 (v1.0.0)  
**测试环境**: {{TIMESTAMP}}  
**支持平台**: Linux, macOS, Windows  
**预计时间**: 10-30 分钟

*文档版本: v2.0.0 | 更新日期: {{TIMESTAMP}}*# {{PROJECT_NAME}} API 参考文档

> **版本**: 1.0.0  
> **最后更新**: {{TIMESTAMP}}  
> **类别**: API 文档  
> **目标读者**: API 消费者、开发者

## 📚 API 概览

{{PROJECT_NAME}} 提供 RESTful API 接口，支持 JSON 格式的数据交换。

### 基础信息
- **Base URL**: `https://api.example.com/v1` (生产环境)
- **开发环境**: `http://localhost:8000/v1`
- **内容类型**: `application/json`
- **认证方式**: Bearer Token / API Key

### 状态码
| 状态码 | 描述 | 说明 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 认证失败 |
| 403 | Forbidden | 权限不足 |
| 404 | Not Found | 资源不存在 |
| 429 | Too Many Requests | 请求频率限制 |
| 500 | Internal Server Error | 服务器内部错误 |

## 🔐 认证与授权

### 获取访问令牌
```http
POST /auth/token
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**响应**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "def50200aecc12a..."
}
```

### 使用 API Key
```http
GET /api/resource
Authorization: Api-Key your-api-key-here
```

## 📋 API 端点

### 用户管理

#### 获取用户列表
```http
GET /users
Authorization: Bearer <token>
```

**查询参数**:
| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| page | integer | 否 | 页码，默认 1 |
| limit | integer | 否 | 每页数量，默认 20 |
| sort | string | 否 | 排序字段 |
| order | string | 否 | 排序方向 (asc/desc) |

**响应**:
```json
{
  "data": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

#### 创建用户
```http
POST /users
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "new_user",
  "email": "user@example.com",
  "password": "secure_password"
}
```

#### 获取单个用户
```http
GET /users/{id}
Authorization: Bearer <token>
```

#### 更新用户
```http
PUT /users/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "updated@example.com"
}
```

#### 删除用户
```http
DELETE /users/{id}
Authorization: Bearer <token>
```

### 产品管理

#### 获取产品列表
```http
GET /products
```

#### 创建产品
```http
POST /products
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "产品名称",
  "description": "产品描述",
  "price": 99.99,
  "stock": 100
}
```

### 订单管理

#### 创建订单
```http
POST /orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2,
  "shipping_address": "收货地址"
}
```

#### 获取订单状态
```http
GET /orders/{id}/status
Authorization: Bearer <token>
```

## 🔄 WebSocket 端点

### 实时通知
```javascript
// 连接 WebSocket
const ws = new WebSocket('wss://api.example.com/ws/notifications');

// 发送认证消息
ws.onopen = () => {
  ws.send(JSON.stringify({
    "type": "auth",
    "token": "your_jwt_token"
  }));
};

// 接收消息
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('收到通知:', data);
};
```

### 事件类型
| 事件类型 | 描述 | 数据格式 |
|----------|------|----------|
| notification | 系统通知 | `{type: "notification", data: {...}}` |
| order_update | 订单更新 | `{type: "order_update", order_id: 123, status: "shipped"}` |
| chat_message | 聊天消息 | `{type: "chat_message", from: "user1", message: "hello"}` |

## 📊 数据模型

### 用户模型
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "status": "string (active/inactive)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 产品模型
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "price": "decimal",
  "stock": "integer",
  "category_id": "integer",
  "created_at": "datetime"
}
```

### 订单模型
```json
{
  "id": "integer",
  "user_id": "integer",
  "total_amount": "decimal",
  "status": "string (pending/paid/shipped/delivered/cancelled)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🛡️ 速率限制

### 限制规则
| 端点 | 限制 | 周期 |
|------|------|------|
| 认证端点 | 10 次 | 每分钟 |
| 公开 API | 100 次 | 每小时 |
| 认证用户 | 1000 次 | 每天 |
| 管理员 | 5000 次 | 每天 |

### 响应头信息
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1640995200
```

## 🔧 错误处理

### 错误响应格式
```json
{
  "error": {
    "code": "validation_error",
    "message": "输入验证失败",
    "details": {
      "email": ["邮箱格式不正确"],
      "password": ["密码长度至少8位"]
    },
    "timestamp": "2024-01-01T00:00:00Z",
    "request_id": "req_123456789"
  }
}
```

### 常见错误码
| 错误码 | 描述 | 解决方案 |
|--------|------|----------|
| invalid_token | 令牌无效 | 重新获取访问令牌 |
| insufficient_permission | 权限不足 | 检查用户角色和权限 |
| resource_not_found | 资源不存在 | 检查资源ID是否正确 |
| validation_error | 验证失败 | 检查请求参数格式 |

## 📝 代码示例

### Python 示例
```python
import requests

# 获取访问令牌
response = requests.post(
    "https://api.example.com/auth/token",
    json={"username": "user", "password": "pass"}
)
token = response.json()["access_token"]

# 调用 API
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("https://api.example.com/api/users", headers=headers)
users = response.json()
```

### JavaScript 示例
```javascript
// 使用 fetch API
const response = await fetch('https://api.example.com/api/products', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});
const products = await response.json();
```

### cURL 示例
```bash
# 获取令牌
curl -X POST https://api.example.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'

# 调用 API
curl -H "Authorization: Bearer <token>" \
  https://api.example.com/api/users
```

## 🧪 测试端点

### 健康检查
```http
GET /health
```

**响应**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "2.0.0",
  "services": {
    "database": "connected",
    "cache": "connected",
    "queue": "connected"
  }
}
```

### 版本信息
```http
GET /version
```

## 🔗 相关资源

- **Swagger UI**: `/docs` (开发环境)
- **ReDoc**: `/redoc` (开发环境)
- **OpenAPI 规范**: `/openapi.json`
- **API 状态页面**: https://status.example.com

## 📋 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | {{TIMESTAMP}} | 初始 API 版本 |

---

**API 版本**: v1.0.0  
**认证方式**: Bearer Token / API Key  
**速率限制**: 已启用  
**文档状态**: ✅ 完整

*文档版本: v2.0.0 | 更新日期: {{TIMESTAMP}}*
