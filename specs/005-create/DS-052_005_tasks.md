# DS-052: 原子任务清单标准 (Atomic Task List Standard)

**类型**: T2 (Executable Standards)  
**版本**: v1.0.0  
**来源**: spec-kit tasks-template.md  
**用途**: State C 执行驱动的原子任务单元  
**依赖**: DS-050 (Spec), DS-051 (Plan)

---

## 1. 文档元数据

```markdown
**特性名称**: create
**特性ID**: 005
**特性分支**: `main`
**创建时间**: 2026-02-02
**引用Spec**: DS-050_005_spec.md
**引用Plan**: DS-051_005_plan.md
**状态**: Draft → In Progress → Done
**作者**: wsman
**项目版本**: 1.5.0
```

---

## 2. 格式说明

### 2.1 任务标识

| 标识 | 含义 | 示例 |
|------|------|------|
| **[P]** | 可并行执行 (不同文件，无依赖) | `[P] T001` |
| **[ID]** | 任务编号 | T001, T002, T003 |
| **[Story]** | 所属用户故事 | US1, US2, US3 |
| **[Core/API/Test]** | 任务类型 | Core, API, Test |

### 2.2 任务格式

```markdown
- [ ] TXXX [P] [USX] [Core/API/Test] [任务描述]
  - 文件: `src/xxx/yyy.py`
  - 依赖: TXXX (如无则写 "无")
  - 验证: `pytest tests/test_xxx.py`
  - 预计时间: X小时
```

---

## 3. 任务分组

### 3.1 按用户故事分组

每个用户故事的任务必须独立，以便实现和测试。

```markdown
## 用户故事 1: [故事标题] (P1 - 最高优先级)

**目标**: [一句话描述]
**验收标准**: [引用 DS-050 中的场景]

- [ ] T001 [P] [US1] [Core] 实现 [核心功能]
  - 文件: `src/core/xxx.py`
  - 依赖: 无
  - 验证: `pytest tests/test_xxx.py`
  
- [ ] T002 [US1] [API] 实现 [API接口]
  - 文件: `src/api/xxx.py`
  - 依赖: T001
  - 验证: `pytest tests/test_api_xxx.py`

---

## 用户故事 2: [故事标题] (P2)

**目标**: [一句话描述]

- [ ] T003 [P] [US2] [Core] 实现 [功能]
  - ...
```

### 3.2 按阶段分组

```markdown
## Phase 1: 基础设施 (共享)

**目的**: 项目初始化和基础结构

- [ ] T000 [P] 创建项目结构
- [ ] T001 [P] 初始化项目配置

## Phase 2: 核心功能 (阻塞所有用户故事)

**目的**: 必须先完成的阻塞性依赖

- [ ] T010 [US1] 实现核心模型
- [ ] T011 [US1] 实现核心服务

## Phase 3: 用户故事实现

**目的**: 按用户故事分组实现

### US1: [故事1]
- [ ] T020 [US1] ...
### US2: [故事2]
- [ ] T030 [US2] ...
```

---

## 4. 任务示例

### 4.1 完整示例

```markdown
# Tasks: 用户登录功能

**Feature**: 用户登录
**Plan**: `specs/user-login/plan.md`
**创建时间**: 2026-02-01

---

## Phase 1: 基础设施

- [ ] T000 [P] 创建项目结构
  - 文件: `src/`, `tests/`
  - 依赖: 无
  - 验证: `ls -la src/`
  - 预计时间: 10分钟

- [ ] T001 [P] 配置认证依赖
  - 文件: `requirements.txt` / `package.json`
  - 依赖: 无
  - 验证: `pip list | grep auth`
  - 预计时间: 15分钟

---

## Phase 2: 核心功能

- [ ] T010 [US1] 实现 User 模型
  - 文件: `src/core/user.py`
  - 依赖: 无
  - 验证: `pytest tests/test_user_model.py`
  - 预计时间: 1小时

- [ ] T011 [US1] 实现 UserRepository
  - 文件: `src/core/user_repository.py`
  - 依赖: T010
  - 验证: `pytest tests/test_user_repository.py`
  - 预计时间: 1小时

---

## Phase 3: API 实现

### US1: 邮箱密码登录

- [ ] T020 [P] [US1] [API] 实现登录接口
  - 文件: `src/api/auth/login.py`
  - 依赖: T011
  - 验证: `pytest tests/test_login_api.py`
  - 预计时间: 2小时

- [ ] T021 [US1] [Test] 登录接口测试
  - 文件: `tests/api/test_login.py`
  - 依赖: T020
  - 验证: `pytest tests/api/test_login.py -v`
  - 预计时间: 1小时

### US2: 第三方 OAuth 登录

- [ ] T030 [P] [US2] [API] 实现 OAuth 接口
  - 文件: `src/api/auth/oauth.py`
  - 依赖: T010
  - 验证: `pytest tests/test_oauth.py`
  - 预计时间: 3小时
```

---

## 5. 任务统计

```markdown
## 任务统计

| 指标 | 数量 |
|------|------|
| 总任务数 | 10 |
| P1 用户故事任务 | 6 |
| P2 用户故事任务 | 2 |
| 基础设施任务 | 2 |
| 可并行任务 | 4 |

## 预计总工时

| 阶段 | 预计时间 |
|------|----------|
| Phase 1 | 25分钟 |
| Phase 2 | 2小时 |
| Phase 3 | 7小时 |
| **总计** | **~10小时** |
```

---

## 6. 进度追踪

### 6.1 任务状态表

| 任务ID | 状态 | 完成时间 | 负责人 | 备注 |
|--------|------|----------|--------|------|
| T000 | ✅ Done | 2026-02-01 16:00 | AI | |
| T001 | ✅ Done | 2026-02-01 16:15 | AI | |
| T010 | 🔄 In Progress | - | AI | 当前任务 |
| T011 | ☐ Todo | - | AI | 等待 T010 |
| T020 | ☐ Todo | - | AI | 等待 T011 |
| ... | | | | |

### 6.2 与 activeContext 集成

在 `activeContext.md` 中添加:

```markdown
## 当前任务 (Current Task) [v1.3.0新增]

| 字段 | 值 |
|------|-----|
| **活动任务** | T010: 实现 User 模型 |
| **所属故事** | US1 |
| **计划文件** | `specs/user-login/tasks.md` |
| **下一步任务** | T011: 实现 UserRepository |
| **前置依赖** | ✅ T000, T001 完成 |
| **预计剩余** | 1小时 |
```

---

## 7. 任务验收标准

每个任务必须定义清晰的验收标准:

```markdown
- [ ] TXXX [任务描述]
  - **文件变更**: [新增/修改的文件列表]
  - **功能验收**: [如何验证功能正确]
  - **代码质量**: [单元测试覆盖率要求]
  - **文档更新**: [需要更新的文档]
```

---

## 8. 与其他标准的关系

```
DS-050 (Spec)
   ↓
DS-051 (Plan)
   ↓
DS-052 (Tasks) ← 本标准
   ↓
activeContext (Current Task)
```

---

**引用标准**: DS-052 v1.0.0  
**最后更新**: 2026-02-02  
**版本**: v1.0.0
