# 模板变量说明 (Template Variables Reference)

## 📋 概述

本文档详细说明了CDD模板中使用的所有占位符变量。这些变量在模板初始化时会被替换为实际值，确保生成的文档具有项目特定的上下文信息。

**版本**: v1.0.0
**最后更新**: 2026-02-21
**宪法依据**: §202 (模板引擎规范)

## 📊 变量分类

### 1. 基础项目变量 (Basic Project Variables)

这些变量定义了项目的核心身份信息。

| 变量名 | 格式 | 描述 | 默认值/来源 | 使用模板 |
|--------|------|------|-------------|----------|
| **{{PROJECT_NAME}}** | 字符串 | 项目名称，用于标识项目 | 用户输入，部署时指定 | 所有模板 |
| **{{PROJECT_MAINTAINER}}** | 字符串 | 项目维护者姓名或团队 | 用户输入 | active_context.md |
| **{{project_version}}** | 语义版本号 | 项目版本号 | 从pyproject.toml或package.json读取 | DS-050, DS-051, DS-052 |
| **{{project_name}}** | 小写字符串 | 项目名称（小写，用于数据库等） | PROJECT_NAME的小写形式 | unified_docs.md |
| **{{project_user}}** | 小写字符串 | 项目数据库用户 | project_name + "_user" | unified_docs.md |

### 2. 时间相关变量 (Time-related Variables)

用于记录时间戳和日期信息。

| 变量名 | 格式 | 描述 | 默认值/来源 | 使用模板 |
|--------|------|------|-------------|----------|
| **{{TIMESTAMP}}** | ISO 8601格式 | 文档最后更新时间 | 自动生成：`datetime.now().isoformat()` | 所有模板 |
| **{{timestamp}}** | ISO 8601格式 | 小写版本的时间戳 | 同{{TIMESTAMP}} | DS-050, DS-051等 |
| **{{DATE}}** | 日期格式 | 简化的日期 | `datetime.now().strftime("%Y-%m-%d")` | DS-060 |
| **{{NEXT_UPDATE}}** | 日期时间 | 下次计划更新时间 | 基于当前时间计算（如+7天） | active_context.md |

### 3. 特性相关变量 (Feature-related Variables)

用于特性规格文档的变量。

| 变量名 | 格式 | 描述 | 默认值/来源 | 使用模板 |
|--------|------|------|-------------|----------|
| **{{feature_name}}** | 字符串 | 特性名称 | 用户输入，创建特性时指定 | DS-050, DS-051, DS-052 |
| **{{feature_id}}** | 字符串 | 特性ID（如"001-hello-world"） | 自动生成：序号+特性名 | DS-050, DS-051, DS-052 |
| **{{feature_description}}** | 字符串 | 特性描述 | 用户输入 | DS-050 |
| **{{git_branch}}** | 字符串 | Git分支名称 | 自动生成：`feature/{{feature_id}}` | DS-050, DS-051, DS-052 |
| **{{author}}** | 字符串 | 文档作者 | 系统用户名或用户输入 | DS-050, DS-051, DS-052 |

### 4. 熵值相关变量 (Entropy-related Variables)

用于活动上下文中的熵值监控。

| 变量名 | 格式 | 描述 | 默认值/来源 | 使用模板 |
|--------|------|------|-------------|----------|
| **{{Hc_VALUE}}** | 浮点数 (0.0-1.0) | 认知负载熵值 | 通过`cdd_entropy.py`计算 | active_context.md |
| **{{Hs_VALUE}}** | 浮点数 (0.0-1.0) | 结构离散熵值 | 通过`cdd_entropy.py`计算 | active_context.md |
| **{{Ha_VALUE}}** | 浮点数 (0.0-1.0) | 同构偏离熵值 | 通过`cdd_entropy.py`计算 | active_context.md |
| **{{H_SYS_VALUE}}** | 浮点数 (0.0-1.0) | 系统综合熵值 | 通过`cdd_entropy.py`计算 | active_context.md |
| **{{Hc_STATUS}}** | 状态图标 | H_cog状态 | 根据值自动计算：🟢/🟡/🟠/🔴 | active_context.md |
| **{{Hs_STATUS}}** | 状态图标 | H_struct状态 | 根据值自动计算：🟢/🟡/🟠/🔴 | active_context.md |
| **{{Ha_STATUS}}** | 状态图标 | H_align状态 | 根据值自动计算：🟢/🟡/🟠/🔴 | active_context.md |
| **{{H_SYS_STATUS}}** | 状态图标 | H_sys状态 | 根据值自动计算：🟢/🟡/🟠/🔴 | active_context.md |

### 5. 组织架构变量 (Organization Variables)

用于定义项目中的角色和模型分配。

| 变量名 | 格式 | 描述 | 默认值/来源 | 使用模板 |
|--------|------|------|-------------|----------|
| **{{PRIMARY_MODEL}}** | 字符串 | 主要AI模型名称 | 用户配置，如"Claude Opus 4.5" | active_context.md |
| **{{PRIMARY_ROLE}}** | 字符串 | 主要模型职责 | 用户配置，如"规划协调" | active_context.md |
| **{{SECONDARY_MODEL}}** | 字符串 | 辅助AI模型名称 | 用户配置，如"MiniMax M2.1" | active_context.md |
| **{{SECONDARY_ROLE}}** | 字符串 | 辅助模型职责 | 用户配置，如"执行管理" | active_context.md |

### 6. 控制论架构变量 (Cybernetic Architecture Variables)

用于三层控制论架构状态监控。

| 变量名 | 格式 | 描述 | 默认值/来源 | 使用模板 |
|--------|------|------|-------------|----------|
| **{{T0_STATUS}}** | 状态图标 | 治理层状态 | 自动检测：🟢正常/🟡警告/🔴异常 | active_context.md |
| **{{T1_STATUS}}** | 状态图标 | 控制层状态 | 自动检测：🟢正常/🟡警告/🔴异常 | active_context.md |
| **{{T2_STATUS}}** | 状态图标 | 执行层状态 | 自动检测：🟢正常/🟡警告/🔴异常 | active_context.md |
| **{{OBSERVE_STATUS}}** | 状态图标 | 观测回路状态 | 自动检测：🟢运行/🟡降级/🔴停止 | active_context.md |
| **{{CONTROL_STATUS}}** | 状态图标 | 控制回路状态 | 自动检测：🟢运行/🟡降级/🔴停止 | active_context.md |
| **{{MEMORY_STATUS}}** | 状态图标 | 记忆回路状态 | 自动检测：🟢运行/🟡降级/🔴停止 | active_context.md |

### 7. 状态监控变量 (Status Monitoring Variables)

用于系统状态监控和事件记录。

| 变量名 | 格式 | 描述 | 默认值/来源 | 使用模板 |
|--------|------|------|-------------|----------|
| **{{SYNC_STATUS}}** | 状态图标 | 同步状态 | 自动检测：✅正常/🟡延迟/🔴异常 | active_context.md |
| **{{EVENT_DATE_1}}** | 日期 | 最近宪法事件1的日期 | 从历史记录中提取 | active_context.md |
| **{{EVENT_DESCRIPTION_1}}** | 字符串 | 最近宪法事件1的描述 | 从历史记录中提取 | active_context.md |
| **{{EVENT_STATUS_1}}** | 状态图标 | 最近宪法事件1的状态 | 从历史记录中提取 | active_context.md |
| **{{TODO_ITEM_1}}** | 字符串 | 待办事项1的内容 | 用户输入或自动生成 | active_context.md |

### 8. 代码审查变量 (Code Review Variables)

用于代码审查文档。

| 变量名 | 格式 | 描述 | 默认值/来源 | 使用模板 |
|--------|------|------|-------------|----------|
| **{{TARGET_FILES}}** | 字符串 | 审查目标文件列表 | 用户输入或自动检测 | DS-060 |
| **{{REVIEWER_NAME}}** | 字符串 | 审查者姓名 | 用户输入或系统用户名 | DS-060 |
| **{{SUMMARY}}** | 字符串 | 审查摘要 | 自动生成或用户输入 | DS-060 |
| **{{REFACTORING_NOTES}}** | 字符串 | 重构建议 | 自动分析生成 | DS-060 |
| **{{SCORE}}** | 整数 (0-100) | 审查评分 | 自动计算 | DS-060 |
| **{{ASSESSMENT}}** | 字符串 | 总体评估 | 基于评分自动生成 | DS-060 |

### 9. 文档版本变量 (Document Version Variables)

用于文档版本管理。

| 变量名 | 格式 | 描述 | 默认值/来源 | 使用模板 |
|--------|------|------|-------------|----------|
| **{{active_context_version}}** | 语义版本号 | 活动上下文版本 | 从active_context.md读取 | DS-050, DS-051 |
| **{{system_patterns_version}}** | 语义版本号 | 系统模式版本 | 从system_patterns.md读取 | DS-050 |

## 🔧 变量解析机制

### 自动解析的变量

以下变量由CDD工具自动解析和填充：

1. **时间相关变量**：在文档生成时自动填充当前时间
2. **熵值相关变量**：通过`cdd_entropy.py`计算后自动更新
3. **状态变量**：根据系统状态自动计算
4. **版本变量**：从相应文件读取

### 用户提供的变量

以下变量需要用户提供：

1. **项目身份变量**：在初始化项目时提供
2. **特性相关变量**：在创建特性时提供
3. **组织架构变量**：在配置项目时提供

### 动态生成的变量

以下变量根据其他变量动态生成：

1. **{{feature_id}}**：基于特性计数自动生成
2. **{{git_branch}}**：基于feature_id生成
3. **{{project_name}}**：PROJECT_NAME的小写形式
4. **{{project_user}}**：基于project_name生成

## 📝 使用示例

### 示例1：初始化项目时

```bash
# 部署项目，提供项目名称
python scripts/cdd_feature.py deploy "我的电商平台" --target /path/to/project
```

**填充的变量**：
- {{PROJECT_NAME}} = "我的电商平台"
- {{project_name}} = "我的电商平台" (小写转换)
- {{project_user}} = "我的电商平台_user"

### 示例2：创建特性时

```bash
# 创建特性，提供特性名称和描述
python scripts/cdd_feature.py create "用户注册功能" --description "实现用户注册和验证功能"
```

**填充的变量**：
- {{feature_name}} = "用户注册功能"
- {{feature_description}} = "实现用户注册和验证功能"
- {{feature_id}} = "001-用户注册功能" (自动生成)
- {{git_branch}} = "feature/001-用户注册功能" (自动生成)

### 示例3：更新活动上下文

```bash
# 运行熵值计算，自动更新熵值变量
python scripts/cdd_entropy.py calculate --update-context
```

**更新的变量**：
- {{Hc_VALUE}}, {{Hs_VALUE}}, {{Ha_VALUE}}, {{H_SYS_VALUE}}
- {{Hc_STATUS}}, {{Hs_STATUS}}, {{Ha_STATUS}}, {{H_SYS_STATUS}}
- {{TIMESTAMP}} (最后更新时间)

## 🛠️ 工具支持

### 1. 变量检查工具

```bash
# 检查模板中未解析的变量
python -c "
import re
import sys
from pathlib import Path

def find_template_variables(file_path):
    content = Path(file_path).read_text(encoding='utf-8')
    variables = re.findall(r'\{\{([^}]+)\}\}', content)
    return set(variables)

# 检查特定文件
variables = find_template_variables('templates/t0_core/active_context.md')
print(f'Found {len(variables)} unique variables:')
for var in sorted(variables):
    print(f'  - {{{{ {var} }}}}')
"
```

### 2. 批量替换示例

```python
# Python脚本示例：批量替换模板变量
import re
from pathlib import Path

def render_template(template_path, context):
    """渲染模板文件"""
    content = Path(template_path).read_text(encoding='utf-8')
    
    for key, value in context.items():
        placeholder = f'{{{{{key}}}}}'
        content = content.replace(placeholder, str(value))
    
    return content

# 使用示例
context = {
    'PROJECT_NAME': '我的项目',
    'TIMESTAMP': '2026-02-21T10:30:00',
    'feature_name': '用户登录'
}

rendered = render_template('templates/t0_core/active_context.md', context)
```

## 🔍 故障排除

### 常见问题

#### 问题1：变量未被替换
**症状**：生成的文档中仍包含`{{VARIABLE_NAME}}`
**可能原因**：
1. 变量名称拼写错误
2. 上下文数据中缺少该变量
3. 模板渲染逻辑错误

**解决方案**：
1. 检查变量名称是否与本文档一致
2. 确保提供了所有必需的变量
3. 检查模板渲染工具的逻辑

#### 问题2：变量值不正确
**症状**：变量被替换，但值不正确
**可能原因**：
1. 变量来源数据错误
2. 变量转换逻辑错误
3. 默认值设置不当

**解决方案**：
1. 检查变量来源数据（如项目配置、熵值计算）
2. 验证变量转换逻辑
3. 检查默认值设置

#### 问题3：状态图标不显示
**症状**：状态变量显示为文本而非图标
**可能原因**：
1. 终端不支持Unicode字符
2. 字体配置问题

**解决方案**：
1. 确保终端支持Unicode
2. 使用支持图标的字体
3. 回退到文本表示：✅ → [OK], 🟡 → [WARN], 🔴 → [ERROR]

## 📚 相关文档

- [CDD参考手册](../reference.md) - 完整的使用指南
- [active_context.md模板](t0_core/active_context.md) - 主要使用模板变量的文件
- [DS-050模板](t2_standards/DS-050_feature_specification.md) - 特性规格模板

## 📄 更新历史

| 版本 | 日期 | 变更描述 |
|------|------|----------|
| v1.0.0 | 2026-02-21 | 初始版本，包含所有模板变量说明 |

---

**宪法依据**: §202 (模板引擎规范)、§101 (单一真理源公理)

**维护者**: CDD技能维护团队

**最后验证**: 通过Gate 1-5审计 ✅