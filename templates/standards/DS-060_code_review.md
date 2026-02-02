# DS-060: 代码审查标准 (Code Review Standard)

**ID**: DS-060
**类型**: T2 (Standard)
**版本**: v1.6.0
**日期**: 2026-02-02
**用途**: 定义 AI 或人工进行代码审查时的标准输出格式与检查维度

---

## 1. 审查报告模板

当执行 Review 任务时，请严格遵循以下输出格式：

```markdown
# Code Review Report

**Target**: {{TARGET_FILES}}
**Reviewer**: AI Agent / {{REVIEWER_NAME}}
**Date**: {{DATE}}
**Compliance**: Checks against `system_patterns.md` & `tech_context.md`

## 1. 摘要 (Summary)
{{SUMMARY}}

## 2. 阻断性问题 (Blockers) 🛑
| Severity | File | Line | Issue | Recommendation |
|----------|------|------|-------|----------------|
| 🔴 Critical | | | | |
| 🟠 Major | | | | |

## 3. 优化建议 (Suggestions) ⚠️
| Category | File | Line | Issue | Recommendation |
|----------|------|------|-------|----------------|
| 🟡 Style | | | | |
| 🟢 Performance | | | | |
| 🔵 Docs | | | | |

## 4. 重构推荐 (Refactoring) 🛠️
{{REFACTORING_NOTES}}

## 5. 审查评分
**Score**: {{SCORE}}/100
**Overall**: {{ASSESSMENT}}
```

---

## 2. 审查维度 (Checklist)

### 2.1 安全性 (Security)

- [ ] 是否存在 SQL 注入、XSS 或未授权访问风险？
- [ ] 是否硬编码了敏感信息 (Secrets)？
- [ ] 是否遵循安全编码规范 (OWASP)？

### 2.2 架构一致性 (Architecture)

- [ ] 代码是否遵循 `system_patterns.md` 定义的分层结构？
- [ ] 是否引入了未在 `tech_context.md` 中声明的外部依赖？
- [ ] 是否符合 Clean Code 原则？

### 2.3 健壮性 (Robustness)

- [ ] 是否处理了边缘情况 (Edge Cases)？
- [ ] 错误处理 (Error Handling) 是否完善？
- [ ] 是否有性能瓶颈？

### 2.4 合规性 (Constitution)

- [ ] 是否符合 CDD 工作流规范？
- [ ] 是否遵循 T0/T1/T2 文档体系？

---

## 3. 严重等级定义

| 等级 | 标记 | 说明 | 处理要求 |
|------|------|------|----------|
| **Critical** | 🔴 | 安全漏洞、逻辑错误、阻断性问题 | 立即修复 |
| **Major** | 🟠 | 架构违规、性能问题 | 合并前修复 |
| **Minor** | 🟡 | 代码风格、文档缺失 | 建议修复 |
| **Suggestion** | 🟢 | 优化建议 | 可选实现 |

---

## 4. 输出规则

1. **必须**引用具体代码行号
2. **必须**提供可操作的修复建议
3. **必须**在发现 Blocker 时在顶部醒目提示
4. **必须**计算审查评分 (0-100)

---

## 5. 相关文档

- `templates/protocols/WF-review.md`: 审查协议
- `templates/axioms/system_patterns.md`: 架构约束
- `templates/axioms/tech_context.md`: 技术栈约束

---

*此标准遵循 CDD v1.6.0 Toolkit Expansion 规范*
