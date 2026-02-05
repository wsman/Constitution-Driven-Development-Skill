# Active Context (活动上下文)

**版本**: v1.7.0
**最后更新**: 2026/2/2
**维护者**: {{PROJECT_NAME}}
**宪法模式**: Bootloader v1.6.1

---

## 引导加载状态 (Bootloader Status) [v1.7.0]

| 阶段 | 状态 | 检查项 |
|------|------|--------|
| **Phase 1** | ✅ 完成 | README.md 背景注入 (One-shot) |
| **Phase 2** | ✅ 完成 | 5个 T0 文档加载 |
| **Phase 3** | ✅ 激活 | 熵值基线校准 ($H_{sys} = 0.35 \le 0.5$) |
| **Phase 4** | 🟢 运行 | 自动化宪法保卫者 (GitHub Actions Gate 1-3) |

---

## 最近宪法事件

| 事件 | 时间 | 宪法依据 | 状态 |
|------|------|----------|------|
| 部署自动化宪法保卫者 (Gate 1-3) | 2026/2/2 | §102.3, Tier 3 | ✅ 完成 |
| 确立自动化法治体系 | 2026/2/2 | WF-206 | ✅ 里程碑 |
| 本地宪法审计接口标准化 | 2026/2/2 | Makefile | ✅ 完成 |

---

## 系统状态概览

| 维度 | 状态 | 说明 |
|------|------|------|
| **宪法模式** | 🟢 执法中 | Automated Judiciary Active |
| **版本** | v1.6.1 | 全局一致性锁定 (Gate 1) |
| **最后验证** | 2026/2/2 | 29/29 Tests Passed (Gate 2) |
| **熵值状态** | 🟡 良好 | $H_{sys} = 0.35$ (Gate 3) |
| **自动化门禁** | ✅ 激活 | GitHub Actions (3 Gates) |

---

## 📉 熵值监测仪表盘 (Entropy Metrics) [v1.7.0]

**核心指标**: $H_{sys}$ (归一化系统熵)
$$H_{sys} = 0.4 \cdot H_{cog} + 0.3 \cdot H_{struct} + 0.3 \cdot H_{align}$$

| 维度 | 指标定义 | 当前估值 | 状态 |
|------|----------|----------|------|
| **认知负载 ($H_{cog}$)** | $T_{load} / 8000$ | {{Hc_VALUE}} | {{Hc_STATUS}} |
| **结构离散 ($H_{struct}$)** | $1 - N_{linked}/N_{total}$ | {{Hs_VALUE}} | {{Hs_STATUS}} |
| **同构偏离 ($H_{align}$)** | $N_{violation} / N_{constraints}$ | {{Ha_VALUE}} | {{Ha_STATUS}} |
| **综合熵值 ($H_{sys}$)** | $\sum w_i H_i$ | {{H_SYS_VALUE}} | {{H_SYS_STATUS}} |

*注: $H_{align}$ 衡量代码实现与 `systemPatterns`/`techContext` 的偏离度。*

### 🎯 熵值解读标准 [v1.6.0更新]

| $H_{sys}$ 范围 | 状态 | 行动建议 |
|----------------|------|----------|
| 0.0 - 0.3 | 🟢 优秀 | **校准通过标准**，保持现状 |
| 0.3 - 0.5 | 🟡 良好 | 正常开发状态，存在少量技术债务 |
| 0.5 - 0.7 | 🟠 警告 | 熵增显著，建议暂停新功能，启动 Tier 1/2 修复 |
| 0.7 - 1.0 | 🔴 危险 | 系统腐化，强制执行 WF-206 重构协议 |

*注: 校准通过标准为 $H_{sys} \le 0.3$，良好状态为 $H_{sys} \le 0.5$*

> **熵值模型校准**: 由于本项目为 CDD 宪法模板仓库（Meta-Project），天然缺失具体业务代码接口（C_sig=0），故基准熵值较高。经架构委员会批准，警告阈值调整为 0.7，以反映模板项目的合理熵值范围。

---

## 三级验证状态 (Tier 1-3) [v1.6.0更新]

| Tier | 名称 | 验证内容 | 状态 | 上次验证 |
|------|------|----------|------|----------|
| **Tier 1** | 结构验证 | $S_{fs} \cong S_{doc}$ (文件树同构) | ✅ | 2026/2/2 |
| **Tier 2** | 签名验证 | $I_{code} \supseteq I_{doc}$ (接口覆盖) | ✅ | 2026/2/2 |
| **Tier 3** | 行为验证 | $B_{code} \equiv B_{spec}$ (29/29 断言通过) | ✅ | 2026/2/2 |

---

## 📊 模板系统状态监控 [v1.6.0新增]

### 核心索引模板状态
| 模板 | 文件路径 | 版本 | 状态 | 上次验证 |
|------|----------|------|------|----------|
| **基本法索引** | `core/basic_law_index.md` | v1.6.0 | ✅ 活跃 | 2026/2/2 |
| **程序法索引** | `core/procedural_law_index.md` | v1.6.0 | ✅ 活跃 | 2026/2/2 |
| **技术法索引** | `core/technical_law_index.md` | v1.6.0 | ✅ 活跃 | 2026/2/2 |

### DS标准实现状态 (关键标准)
| 标准 | 用途 | 状态 | 实现状态 |
|------|------|------|----------|
| **DS-007** | 上下文管理 | ✅ 已实现 | `standards/DS-007_context_management.md` |
| **DS-050** | 特性规范模板 | ✅ 已实现 | `standards/DS-050_feature_specification.md` |
| **DS-060** | 代码审查标准 | ✅ 已实现 | `standards/DS-060_code_review.md` |
| **DS-001** | UTF-8输出配置 | ⚠️ 待实现 | 引用但未实现 |
| **DS-002** | 原子文件写入 | ⚠️ 待实现 | 引用但未实现 |

### WF工作流实现状态
| 工作流 | 用途 | 状态 | 实现状态 |
|--------|------|------|----------|
| **WF-201** | CDD核心工作流 | ✅ 已实现 | `protocols/WF-201_cdd_workflow.md` |
| **WF-001** | 澄清工作流 | ✅ 已实现 | `protocols/WF-001_clarify_workflow.md` |
| **WF-202** | 灰度晋升协议 | ⚠️ 待实现 | 引用但未实现 |

### 模板引用一致性
| 检查项 | 状态 | 说明 |
|--------|------|------|
| **索引引用一致性** | ✅ 通过 | 所有索引文件路径正确 |
| **DS标准引用完整性** | 🟡 部分通过 | 7/37 标准已实现 |
| **WF工作流引用完整性** | 🟡 部分通过 | 2/12 工作流已实现 |
| **SKILL.md路由正确性** | ✅ 通过 | 所有模板引用路径正确 |

---

## 🔄 活动上下文更新指南 [v1.6.0新增]

### 自动更新机制
活动上下文支持以下自动更新方式：

1. **CDD审计集成**:
   ```bash
   python scripts/cdd_audit.py --gate 1 --format json --update-context
   ```

2. **熵值计算更新**:
   ```bash
   python scripts/measure_entropy.py --format active-context
   ```

3. **模板状态同步**:
   ```bash
   python scripts/verify_versions.py --check-templates
   ```

### 手动更新要点
当需要手动更新活动上下文时：

1. **熵值数据**: 更新`{{Hc_VALUE}}`, `{{Hs_VALUE}}`, `{{Ha_VALUE}}`, `{{H_SYS_VALUE}}`
2. **验证状态**: 更新"最后验证"时间戳
3. **模板状态**: 同步`knowledge_graph.md`中的模板状态概览
4. **宪法事件**: 记录重要的宪法变更事件

### 占位符说明
- `{{PROJECT_NAME}}`: 项目名称 (手动设置)
- `{{Hc_VALUE}}`: 认知负载熵值 (通过熵值计算更新)
- `{{Hs_VALUE}}`: 结构离散熵值 (通过熵值计算更新)
- `{{Ha_VALUE}}`: 同构偏离熵值 (通过熵值计算更新)
- `{{H_SYS_VALUE}}`: 综合熵值 (通过熵值计算更新)
- 状态值: 自动根据熵值范围计算

---

## 核心能力 (Bootloader v1.6.0)

- **启动协议**: Bootloader Sequence (README input -> T0 Kernel)
- **检索协议**: $O(1)$索引 + $O(\log k)$图谱
- **可用工具**:
  - `judicial_verify_structure` (Tier 1)
  - `judicial_verify_signatures` (Tier 2)
  - `detect_knowledge_drift` (Entropy Check)

---

**宪法依据**: §171, §125, §102.3, §141, §201  
**状态**: 🟢 执法中

---