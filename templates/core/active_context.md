# Active Context (活动上下文)

**版本**: v1.2.0
**最后更新**: {{TIMESTAMP}}
**维护者**: {{PROJECT_NAME}}
**宪法模式**: Bootloader v1.2.0

---

## 引导加载状态 (Bootloader Status) [v1.2.0更新]

| 阶段 | 状态 | 检查项 |
|------|------|--------|
| **Phase 1** | ✅ 完成 | README.md 背景注入 (One-shot) |
| **Phase 2** | ✅ 就绪 | 5个 T0 文档加载 |
| **Phase 3** | ⏳ 待定 | 熵值基线校准 ($H_{sys} \le 0.3$) |

---

## 最近宪法事件

| 事件 | 时间 | 宪法依据 | 状态 |
|------|------|----------|------|
| {{RECENT_EVENT_1}} | {{TIME}} | {{CLAUSE}} | {{STATUS}} |
| {{RECENT_EVENT_2}} | {{TIME}} | {{CLAUSE}} | {{STATUS}} |

---

## 系统状态概览

| 维度 | 状态 | 说明 |
|------|------|------|
| **宪法模式** | 🟢 活跃 | Bootloader v1.2.0 |
| **版本** | v1.2.0 | {{PROJECT_VERSION}} |
| **上下文占用** | {{TOKEN_USAGE}} | <8000 tokens |
| **熵值状态** | {{H_SYS_STATUS}} | 目标: $\leq 0.3$ |

---

## 📉 熵值监测仪表盘 (Entropy Metrics) [v1.2.0]

**核心指标**: $H_{sys}$ (归一化系统熵)
$$H_{sys} = 0.4 \cdot H_{cog} + 0.3 \cdot H_{struct} + 0.3 \cdot H_{align}$$

| 维度 | 指标定义 | 当前估值 | 状态 |
|------|----------|----------|------|
| **认知负载 ($H_{cog}$)** | $T_{load} / 8000$ | {{Hc_VALUE}} | {{Hc_STATUS}} |
| **结构离散 ($H_{struct}$)** | $1 - N_{linked}/N_{total}$ | {{Hs_VALUE}} | {{Hs_STATUS}} |
| **同构偏离 ($H_{align}$)** | $N_{violation} / N_{constraints}$ | {{Ha_VALUE}} | {{Ha_STATUS}} |
| **综合熵值 ($H_{sys}$)** | $\sum w_i H_i$ | {{H_SYS_VALUE}} | {{H_SYS_STATUS}} |

*注: $H_{align}$ 衡量代码实现与 `systemPatterns`/`techContext` 的偏离度。*

### 🎯 熵值解读标准 [v1.2.0更新]

| $H_{sys}$ 范围 | 状态 | 行动建议 |
|----------------|------|----------|
| 0.0 - 0.3 | 🟢 优秀 | **校准通过标准**，保持现状 |
| 0.3 - 0.5 | 🟡 良好 | 正常开发状态，存在少量技术债务 |
| 0.5 - 0.7 | 🟠 警告 | 熵增显著，建议暂停新功能，启动 Tier 1/2 修复 |
| 0.7 - 1.0 | 🔴 危险 | 系统腐化，强制执行 WF-206 重构协议 |

*注: 校准通过标准为 $H_{sys} \le 0.3$，良好状态为 $H_{sys} \le 0.5$*
| 0.7 - 1.0 | 🔴 危险 | 立即停止开发，执行重构 |

---

## 三级验证状态 (Tier 1-3) [v1.1.0新增]

| Tier | 名称 | 验证内容 | 状态 | 上次验证 |
|------|------|----------|------|----------|
| **Tier 1** | 结构验证 | $S_{fs} \cong S_{doc}$ (文件树同构) | ⏳ | - |
| **Tier 2** | 签名验证 | $I_{code} \supseteq I_{doc}$ (接口覆盖) | ⏳ | - |
| **Tier 3** | 行为验证 | $B_{code} \equiv B_{spec}$ (断言通过) | ⏳ | - |

---

## 核心能力 (Bootloader v1.1.0)

- **启动协议**: Bootloader Sequence (README input -> T0 Kernel)
- **检索协议**: $O(1)$索引 + $O(\log k)$图谱
- **可用工具**:
  - `judicial_verify_structure` (Tier 1)
  - `judicial_verify_signatures` (Tier 2)
  - `detect_knowledge_drift` (Entropy Check)

---

## 可用工具

| 类别 | 工具 | 说明 |
|------|------|------|
| **法典导航** | 索引检索 | O(1)查找 + O(log k)图谱 |
| **司法验证** | judicial_verify_* | 三级验证 (Tier 1-3) |
| **知识管理** | detect_knowledge_drift | 知识漂移检测 |
| **架构同步** | auto_update_architecture | Tier 2验证 |

---

## 📊 性能基准

| 指标 | 目标 | 当前 |
|------|------|------|
| Bootloader启动时间 | <100ms | {{STARTUP_TIME}} |
| Memory Bank占用 | <8000 tokens | {{TOKEN_USAGE}} |
| 架构同构性 | 100% | {{ARCH_COMPLIANCE}} |

---

**宪法依据**: §171, §125, §102.3, §141, §201  
**状态**: {{PROJECT_STATUS}}

---

## 三级验证状态

| Tier | 验证项 | 状态 | 时间 |
|------|--------|------|------|
| Tier 1 | 结构验证 ($S_{fs} \cong S_{doc}$) | ⏳ | - |
| Tier 2 | 签名验证 ($I_{code} \supseteq I_{doc}$) | ⏳ | - |
| Tier 3 | 行为验证 ($B_{code} \equiv B_{spec}$) | ⏳ | - |

---

## 懒加载示例

### 示例1: UTF-8输出配置
1. **检索**: 技术法索引 §301 → DS-001
2. **加载**: 读取 DS-001 标准文件
3. **执行**: 按照标准配置UTF-8编码

### 示例2: 原子文件写入
1. **检索**: 技术法索引 §302 → DS-002
2. **加载**: 读取 DS-002 标准文件
3. **执行**: 按照标准实现原子写入

---

**宪法依据**: §171, §125, §102.3, §141, §201  
**状态**: {{PROJECT_STATUS}}

---
