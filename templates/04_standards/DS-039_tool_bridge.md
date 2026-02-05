# DS-039 工具调用桥接器标准 (Tool Bridge Standard)

**标准编号**: DS-039
**关联条款**: 技术法 §438, §300.1, §302
**版本**: v1.0.0
**状态**: 🟢 活跃
**最后更新**: 2026-02-06
**生效日期**: 2026-02-06

## 1. 核心定义

**工具桥接器 (ToolBridge)** 是 CDD 系统中所有 I/O 操作的**唯一合法代理**。任何绕过桥接器直接使用原生 API (如 `open()`, `os.remove()`, `Path.read_text()`, `Path.write_text()`) 的行为均视为**严重违宪** (CRITICAL Violation)。

### 1.1 桥接器角色
- **数字气闸 (Digital Airlock)**: 隔离宿主系统与 CDD 项目文件空间
- **安全代理 (Security Proxy)**: 强制执行孢子协议 (§300.1) 的路径隔离
- **原子协调器 (Atomic Coordinator)**: 保障文件写入的原子性 (§302)
- **审计记录器 (Audit Logger)**: 记录所有 I/O 操作供司法审查

### 1.2 适用范围
- 所有文件读/写操作
- 目录遍历与列表
- 文件存在性检查
- 临时文件创建与管理

## 2. 宪法依据

### 2.1 §438 工具调用公理
> "所有工具调用必须通过桥接器进行，实现操作的统一拦截与审计。严禁直接实例化外部工具。"

**桥接器实现**:
- 提供统一的 `read_file()`, `write_file()`, `list_files()` 接口
- 拦截所有对文件系统的直接访问
- 记录操作审计日志

### 2.2 §300.1 孢子协议 (基本法版本)
> "防止工具链对自己进行操作（递归污染），实现智能隔离。"

**桥接器实现**:
- **根目录锁定**: 所有操作限制在 `PROJECT_ROOT` 范围内
- **路径遍历防护**: 检测并阻止 `../` 等路径遍历攻击
- **符号链接防护**: 禁止跟随指向根目录外部的符号链接

### 2.3 §302 原子写入原则 (技术法版本)
> "文件写入必须遵循 'Write-to-Temp-and-Rename' 模式，杜绝中间状态。"

**桥接器实现**:
- 临时文件创建于同目录 (`*.tmp.*`)
- 完整写入后执行 `fsync` 强制落盘
- 原子重命名 (`rename()`) 确保操作原子性

## 3. 实现规范

### 3.1 路径安全 (Path Safety)

#### 3.1.1 根目录验证
```python
def _validate_path(self, relative_path: str) -> Path:
    """
    强制执行孢子协议: 防止路径遍历攻击。
    
    步骤:
    1. 解析路径: PROJECT_ROOT / relative_path
    2. 规范化: resolve() 处理 `.`, `..`, 符号链接
    3. 前缀检查: 确保目标路径在项目根目录内
    
    违宪示例:
    - 相对路径: "../../etc/passwd"
    - 绝对路径: "/etc/passwd"
    - 符号链接: "./symlink -> /etc"
    """
    try:
        target_path = (self.project_root / relative_path).resolve()
        
        # 字符串前缀检查 (跨平台安全)
        if not str(target_path).startswith(str(self.project_root)):
            raise PermissionError(
                f"孢子协议违宪: 路径 '{relative_path}' 试图逃离项目边界。"
            )
            
        return target_path
    except Exception as e:
        self._log_security_violation(f"安全拦截: {e}")
        raise
```

#### 3.1.2 符号链接策略
- **创建**: 允许在项目内创建符号链接
- **跟随**: 禁止跟随指向项目外的符号链接
- **检测**: 解析路径时检测符号链接边界

### 3.2 原子写入 (Atomic Write)

#### 3.2.1 写入算法
`write_file(path, content)` 必须遵循以下原子步骤:

1. **路径验证**: `P_target = validate_path(path)`
2. **目录准备**: `mkdir -p parent(P_target)`
3. **临时文件**: `P_temp = P_target.parent / f"{P_target.name}.tmp.{uuid4()}"`
4. **写入内容**: `write(P_temp, content, encoding='utf-8')`
5. **强制落盘**: `fsync(P_temp)`
6. **原子重命名**: `rename(P_temp, P_target)`

#### 3.2.2 故障恢复
- **写入失败**: 删除临时文件，保持原文件不变
- **重命名失败**: 保留临时文件，记录错误，人工干预
- **并发保护**: 同一路径的并发写入按时间顺序序列化

### 3.3 审计日志 (Audit Logging)

#### 3.3.1 日志格式
```json
{
  "timestamp": "2026-02-06T12:34:56Z",
  "operation": "WRITE",
  "path": "scripts/semantic_audit.py",
  "relative_path": "semantic_audit.py",
  "size_bytes": 20480,
  "agent": "semantic_audit.py",
  "checksum": "sha256:abc123...",
  "atomic_id": "tmp.abc123-def456"
}
```

#### 3.3.2 日志级别
- **DEBUG**: 读取操作、列表操作
- **INFO**: 成功写入、原子重命名
- **WARNING**: 文件不存在、权限问题
- **ERROR**: 违宪尝试、写入失败、安全违规

### 3.4 接口规范

#### 3.4.1 必需方法
```python
class ToolBridge:
    def __init__(self, project_root: Union[str, Path]): ...
    
    def read_file(self, path: str) -> str: ...
    
    def write_file(self, path: str, content: str) -> bool: ...
    
    def list_files(self, path: str = ".", recursive: bool = False, 
                   extension: Optional[str] = None) -> List[str]: ...
    
    def file_exists(self, path: str) -> bool: ...
```

#### 3.4.2 可选扩展
```python
def copy_file(self, src: str, dst: str) -> bool: ...
def delete_file(self, path: str) -> bool: ...
def get_file_stats(self, path: str) -> Dict[str, Any]: ...
def ensure_directory(self, path: str) -> bool: ...
```

## 4. 违规示例与修正

### 4.1 违宪代码示例
```python
# ❌ 严重违宪 (CRITICAL Violation)
from pathlib import Path

# 直接文件操作
content = Path("src/main.py").read_text()
Path("output.txt").write_text("data")

# 目录遍历风险
shutil.copy2("../sensitive.txt", "project/")
```

### 4.2 合宪代码示例
```python
# ✅ 宪法合规 (Constitutional Compliance)
from scripts.utils.tool_bridge import ToolBridge

bridge = ToolBridge(PROJECT_ROOT)

# 安全读取
content = bridge.read_file("src/main.py")

# 原子写入
success = bridge.write_file("output.txt", "data")

# 安全列表
files = bridge.list_files("docs/", recursive=True, extension=".md")
```

### 4.3 违宪检测模式
Gate 4 语义审计将检测以下模式:
- `Path(...).read_text()` / `.write_text()`
- `open(...)` / `with open(...)`
- `shutil.copy*()`, `os.rename()` 
- `os.listdir()`, `os.walk()` 等直接系统调用

## 5. 豁免条款

### 5.1 自举阶段豁免
**适用场景**: `deploy_cdd.py` 在桥接器尚未建立时
**条件**: 
1. 仅用于部署桥接器自身或宪法文件
2. 必须最小化使用范围
3. 部署完成后立即切换到桥接器模式

```python
# deploy_cdd.py 自举逻辑
if not bridge_available:
    # 临时豁免: 部署桥接器
    Path("scripts/utils/tool_bridge.py").write_text(bridge_code)
else:
    # 正常使用桥接器
    bridge.write_file("config.yaml", config)
```

### 5.2 底层测试豁免
**适用场景**: 专门测试文件系统边缘情况的测试代码
**条件**:
1. 文件名明确包含 `test_io_` 或 `test_filesystem_`
2. 测试目的明确是验证系统边界
3. 测试完成后立即清理

```python
# tests/test_io_edge_cases.py (豁免)
def test_path_traversal_protection():
    # 直接操作以测试防护机制
    with open("/tmp/test.txt", "w") as f:
        f.write("test")
```

### 5.3 宪法文件加载豁免
**适用场景**: ToolBridge 自身加载宪法文件时
**条件**: 仅用于初始化阶段的宪法文件读取
```python
def _load_constitution(self):
    # 豁免: 加载定义自身的宪法
    try:
        return Path(__file__).parent.parent.parent.joinpath(
            "templates/01_core/technical_law_index.md"
        ).read_text()
    except:
        # 回退到桥接器
        return self.read_file("templates/01_core/technical_law_index.md")
```

## 6. 迁移指南

### 6.1 优先级顺序
1. **司法系统**: `semantic_audit.py` (大法官必须先守法)
2. **部署脚本**: `deploy_cdd.py`, `verify_versions.py`
3. **核心工具**: `measure_entropy.py`, `constitution_validator.py`
4. **其他脚本**: 按使用频率逐步迁移

### 6.2 迁移步骤
```python
# 迁移前
content = Path("file.txt").read_text()

# 迁移后
from scripts.utils.tool_bridge import ToolBridge
bridge = ToolBridge(Path(__file__).parent.parent)
content = bridge.read_file("file.txt")
```

### 6.3 回滚策略
如桥接器出现严重缺陷:
1. 立即修复桥接器实现
2. 临时恢复原生操作 (需记录豁免)
3. 修复后重新迁移

## 7. 验证与测试

### 7.1 合规性验证
```bash
# 运行宪法验证
python scripts/constitution_validator.py --target scripts/

# 运行 Gate 4 语义审计
python scripts/cdd_audit.py --gate 4

# 专门测试桥接器
python -m pytest tests/test_tool_bridge.py -v
```

### 7.2 性能基准
```bash
# 原子写入性能
python benchmarks/atomic_write_benchmark.py

# 路径验证开销
python benchmarks/path_validation_benchmark.py

# 审计日志性能
python benchmarks/audit_logging_benchmark.py
```

## 8. 附录

### 8.1 版本历史
- **v1.0.0** (2026-02-06): 初始标准发布，响应 Gate 4 §438 违宪发现

### 8.2 相关标准
- **DS-001**: UTF-8 输出编码标准
- **DS-002**: 原子文件写入标准
- **DS-003**: 弹性通信标准
- **DS-028**: Markdown 解析器标准

### 8.3 实施状态
| 组件 | 状态 | 负责人 | 完成日期 |
|------|------|--------|----------|
| ToolBridge 实现 | 🟢 已实现 | CDD 司法系统 | 2026-02-06 |
| semantic_audit.py 迁移 | 🟢 已完成 | CDD 司法系统 | 2026-02-06 |
| 其他脚本迁移 | 🟡 进行中 | 开发团队 | TBD |
| 豁免条款实施 | 🟢 已定义 | CDD 立法机构 | 2026-02-06 |

---

**宪法誓言**: 我宣誓遵守 DS-039 标准，通过桥接器进行所有工具调用，维护系统的安全性与原子性，捍卫孢子协议的文件边界。

*遵循宪法约束: 标准即法律，合规即自由。*