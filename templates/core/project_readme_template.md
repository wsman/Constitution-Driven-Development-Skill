# 项目名

**项目类型**: [量化分析系统/Web3 DApp/传统软件等]
**版本**: v1.0.0
**最后更新**: YYYY-MM-DD
**CDD版本**: [v1.6.0 - 使用宪法驱动开发框架]
**宪法模式**: [🟢 引导模式 | 🟡 执法中 | 🔴 重构中]

## 项目描述

[用1-2句话描述项目核心功能和目标]

*基于宪法驱动开发 (CDD) v1.6.0 框架构建，遵循"法律优先于代码"原则，通过三级验证体系和系统熵监控确保架构健康和代码质量。*

## 技术栈

- **后端**: [如 Python FastAPI, Node.js, Go等]
- **前端**: [如 React 19, Vue, Tauri等]
- **数据库**: [如 SQLite, PostgreSQL, TDX DB等]
- **外部API**: [如 DeepSeek API, Yahoo Finance等]
- **CDD工具链** (可选): 
  - `cdd_audit.py` - 宪法审计与三级验证
  - `cdd-feature.py` - 特性脚手架与文档驱动开发
  - `measure_entropy.py` - 系统熵值计算与监控

## 核心功能

1. [功能1]
2. [功能2]
3. [功能3]

*CDD特色功能示例*:
- **宪法同步**: 确保代码实现与法律文档一致
- **熵值审计**: 定期监控系统复杂度变化
- **三级验证**: 结构、签名、行为完整性检查

## 外部依赖

| 服务 | 用途 | 文档位置 |
|------|------|----------|
| [API服务1] | [用途描述] | memory_bank/00_indices/01_basic_law_index.md |
| [数据服务2] | [用途描述] | memory_bank/00_indices/03_technical_law_index.md |
| [数据库3] | [用途描述] | memory_bank/00_indices/03_technical_law_index.md |

*注：外部服务的法律约束和接口定义需在技术法中明确，确保符合宪法§302原子写入和§440通信韧性原则。*

## 项目定位

本项目是一个 **[项目类型]**，基于宪法驱动开发框架构建，核心特性包括：
- [核心业务1]
- [核心业务2]
- **宪法遵从性**: 严格遵循基本法、程序法、技术法约束
- **熵值监控**: 实时跟踪系统复杂度变化，确保 $H_{sys} \le 0.7$
- **三级验证**: 通过结构、签名、行为验证确保代码质量

## 相关文档

- **CDD Memory Bank**: `memory_bank/` - 项目的宪法文档体系（单一真理源）
- **基本法**: `memory_bank/00_indices/01_basic_law_index.md` - 核心公理与宪法约束
- **程序法**: `memory_bank/00_indices/02_procedural_law_index.md` - 工作流与执行协议
- **技术法**: `memory_bank/00_indices/03_technical_law_index.md` - 技术标准与实现规范
- **活跃上下文**: `memory_bank/01_active_state/activeContext.md` - 当前项目状态与熵值监控
- **知识图谱**: `memory_bank/02_systemaxioms/KNOWLEDGE_GRAPH.md` - 高维关联导航与领域知识

*使用三级递进导航*:
1. **SKILL.md** (第一级) - 快速了解CDD工作流和工具链
2. **reference/** (第二级) - 深入理解特定概念和原则  
3. **templates/** (第三级) - 查看具体实现模板和标准

## 快速开始

```bash
# 1. 安装项目依赖
pip install -r requirements.txt

# 2. 宪法初始化与熵值基线校准
python -c "import os; os.makedirs('memory_bank', exist_ok=True)"  # 创建Memory Bank结构
python scripts/cdd_audit.py --gate 1 --format json  # 执行宪法审计

# 3. 启动项目服务
python main.py

# CDD特定命令示例：
# - 创建新特性: python scripts/cdd-feature.py "特性名" "描述"
# - 审计项目状态: python scripts/cdd_audit.py --format json --ai-hint
# - 检查熵值健康: python scripts/cdd_audit.py --gate 3
# - 修复版本漂移: python scripts/cdd_audit.py --fix
```

### 🛡️ 宪法护栏 (开发约束)
1. **法律优先**: 严禁直接修改代码，必须先更新T2规范文档
2. **审计前置**: 任何变更前必须运行 `cdd_audit.py`
3. **熵值阈值**: 当 $H_{sys} > 0.7$ 时，停止功能开发，启动重构
4. **原子一致性**: 代码变更必须同步更新T0/T1文档

### 📊 熵值监控
- **目标状态**: $H_{sys} \le 0.5$ (良好)
- **警告阈值**: $H_{sys} > 0.7$ (需立即重构)
- **监控命令**: `python scripts/measure_entropy.py --format active-context`

---

*本README用于项目背景说明，不属于T0级别文档。*
*T0级别文档（宪法文档）位于 `memory_bank/` 目录下，是项目的"可执行规范"。*

*遵循宪法约束: 代码即法律证明，架构即宪法执行。*
