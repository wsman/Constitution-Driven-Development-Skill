# {{PROJECT_NAME}} 快速入门指南

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
# 应该返回: {"status": "ok", "version": "1.0.0"}

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

*文档版本: v1.0.0 | 更新日期: {{TIMESTAMP}}*