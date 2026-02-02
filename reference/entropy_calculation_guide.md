# Appendix A: Entropy Calculation Implementation

`measure_entropy.py` 的实现逻辑参考。

## 计算流程
1. **扫描**: 遍历目录树，忽略 .gitignore。
2. **结构分析 ($C_{dir}$)**:
   - 检查 `src/`, `docs/`, `tests/` 是否存在。
   - 对比 `system_patterns.md` 中的定义。
3. **接口分析 ($C_{sig}$)**:
   - 提取代码中的 class/def 签名。
   - 对比 `tech_context.md` 中的接口定义。
4. **测试分析 ($C_{test}$)**:
   - 解析 pytest 输出 XML/JSON。
   - 计算通过率。

## 缓存机制
为了性能，计算结果会缓存于 `.entropy_cache.json`，基于文件 Hash 更新。

## 🔧 相关模板 (Related Templates)

### 系统公理模板
- **`axioms/behavior_context.md`**
- **`axioms/system_patterns.md`**
- **`axioms/tech_context.md`**

### 使用说明
1. **阅读顺序**: 先阅读本概念文件，再查阅相关模板
2. **模板实例化**: 使用 `cdd-feature.py` 自动生成具体实现
3. **层级对应**: 这些模板对应T0-T3文档体系的不同层级
