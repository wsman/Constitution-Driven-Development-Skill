# External Auditor Interface (`cdd_audit.py`)

审计器是 CDD 的最高执法机构。

## 使用方法
```bash
python scripts/cdd_audit.py [OPTIONS]
```

### 参数详解
- `--gate [1|2|3|all]`: 指定检查级别。
- `--fix`: 自动修复 Gate 1 (版本) 问题。
- `--clean`: 清理 specs/ 下的临时测试文件。
- `--format json`: 输出机器可读报告 (CI/CD 集成)。
- `--ai-hint`: 在 JSON 中包含针对 AI 的修复建议。

### 错误码
- `101`: 版本不一致。
- `102`: 行为测试失败。
- `103`: 熵值过高。

## 🔧 相关模板 (Related Templates)

### 工作流协议模板
- **`protocols/WF-review.md`**

### 执行标准模板
- **`standards/DS-060_code_review.md`**

### 使用说明
1. **阅读顺序**: 先阅读本概念文件，再查阅相关模板
2. **模板实例化**: 使用 `cdd-feature.py` 自动生成具体实现
3. **层级对应**: 这些模板对应T0-T3文档体系的不同层级
