# Active Context (活动上下文)

**版本**: v1.0.0
**最后更新**: {{TIMESTAMP}}
**维护者**: {{PROJECT_NAME}}
**宪法模式**: Bootloader v1.1.0 (Neural Graph Navigation)

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
| **宪法模式** | 🟢 活跃 | Bootloader v1.1.0 Neural Graph Navigation |
| **版本** | v1.0.0 | {{PROJECT_VERSION}} |
| **索引系统** | ✅ 就绪 | 基本法/程序法/技术法索引 |
| **上下文占用** | {{TOKEN_USAGE}} | <8000 tokens |
| **熵值状态** | {{H_SYS_STATUS}} | $\Delta H > 0$ |

---

## 核心能力 (Bootloader v1.1.0)

- **启动协议**: 加载索引内核 (3文件) + activeContext.md
- **检索协议**: 双模式检索 - $O(1)$索引 + $O(\log k)$图谱
- **标准索引**: DS-xxx 标准通过技术法索引访问
- **法典完整性**: 三卷法典内核化，版本统一
- **神经网络导航**: 支持模糊问题图谱推理，最大跳数=3

---

## 可用工具

| 类别 | 工具 | 说明 |
|------|------|------|
| **法典导航** | 索引检索 | O(1)查找 + O(log k)图谱 |
| **司法验证** | judicial_verify_* | 三级验证 (Tier 1-3) |
| **知识管理** | detect_knowledge_drift | 知识漂移检测 |
| **架构同步** | auto_update_architecture | Tier 2验证 |

---

## 📉 熵值监测仪表盘 (Entropy Metrics)

**核心指标**: $H_{sys}$ (归一化系统熵)
$$H_{sys} = 0.4 \cdot \frac{T_{load}}{8000} + 0.3 \cdot \left(1 - \frac{N_{linked}}{N_{total}}\right) + 0.3 \cdot \frac{F_{drift}}{F_{total}}$$

| 维度 | 指标定义 | 当前估值 | 状态 |
|------|----------|----------|------|
| **认知负载 ($H_c$)** | $T_{load} / 8000$ | {{Hc_VALUE}} | {{Hc_STATUS}} |
| **结构连接 ($H_s$)** | $1 - N_{linked}/N_{total}$ | {{Hs_VALUE}} | {{Hs_STATUS}} |
| **版本一致 ($H_v$)** | $F_{drift} / F_{total}$ | {{Hv_VALUE}} | {{Hv_STATUS}} |
| **综合熵值 ($H_{sys}$)** | $\sum w_i H_i$ | {{H_SYS_VALUE}} | {{H_SYS_STATUS}} |

### 🎯 熵值解读

| $H_{sys}$ 范围 | 状态 | 行动建议 |
|----------------|------|----------|
| 0.0 - 0.3 | 🟢 优秀 | 保持现状 |
| 0.3 - 0.5 | 🟡 良好 | 关注负载 |
| 0.5 - 0.7 | 🟠 警告 | 优化结构 |
| 0.7 - 1.0 | 🔴 危险 | 立即整理，启动WF-206 |

### 📊 性能基准

| 指标 | 目标 | 当前 |
|------|------|------|
| Bootloader启动时间 | <100ms | {{STARTUP_TIME}} |
| Memory Bank占用 | <8000 tokens | {{TOKEN_USAGE}} |
| 架构同构性 | 100% | {{ARCH_COMPLIANCE}} |

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
