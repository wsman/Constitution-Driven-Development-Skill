# {{PROJECT_NAME}} 开发环境配置指南

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
    "version": "0.2.0",
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

*文档版本: v1.0.0 | 更新日期: {{TIMESTAMP}}*