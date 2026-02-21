#!/bin/bash
# =============================================================================
# CDD 示例：完整工作流 (State A -> E)
# =============================================================================
# 
# 本脚本演示CDD的完整5状态工作流：
#   State A (Intake) -> State B (Plan) -> State C (Execute) 
#   -> State D (Verify) -> State E (Close)
#
# 宪法依据: §101, §102, §200, §300

set -e

CDD_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
TARGET_PROJECT="${1:-/tmp/cdd-demo-project}"
PROJECT_NAME="${2:-demo-project}"

echo "=========================================="
echo "CDD 完整工作流演示"
echo "=========================================="
echo ""
echo "目标项目: $TARGET_PROJECT"
echo "项目名称: $PROJECT_NAME"
echo ""

# =============================================================================
# State A: Intake (上下文加载)
# =============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 State A: Intake (上下文加载)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 创建并部署项目
echo "创建项目目录..."
mkdir -p "$TARGET_PROJECT"

echo "部署 CDD Memory Bank 结构..."
python3 "$CDD_ROOT/scripts/cdd_feature.py" deploy "$PROJECT_NAME" \
    --target "$TARGET_PROJECT" --force

echo ""
echo "✅ State A 完成：Memory Bank 已初始化"
echo ""

# =============================================================================
# State B: Plan (规格规划)
# =============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 State B: Plan (规格规划)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "创建新特性..."
python3 "$CDD_ROOT/scripts/cdd_feature.py" create "user-authentication" \
    --description "用户登录和认证功能" \
    --target "$TARGET_PROJECT" \
    --no-branch

echo ""
echo "查看创建的特性规格..."
python3 "$CDD_ROOT/scripts/cdd_feature.py" list --target "$TARGET_PROJECT"

echo ""
echo "✅ State B 完成：特性规格已创建"
echo ""

# =============================================================================
# State C: Execute (代码实现)
# =============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 State C: Execute (代码实现)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "创建示例源代码..."
mkdir -p "$TARGET_PROJECT/src"

cat > "$TARGET_PROJECT/src/auth.py" << 'EOF'
"""用户认证模块

宪法依据: §101, §102
"""

def login(username: str, password: str) -> bool:
    """用户登录验证"""
    # TODO: 实现实际验证逻辑
    return username == "admin" and password == "secret"


def logout() -> None:
    """用户登出"""
    pass
EOF

echo "创建测试代码..."
mkdir -p "$TARGET_PROJECT/tests"

cat > "$TARGET_PROJECT/tests/test_auth.py" << 'EOF'
"""认证模块测试

宪法依据: §101
"""

from src.auth import login, logout


def test_login_success():
    """测试登录成功"""
    assert login("admin", "secret") is True


def test_login_failure():
    """测试登录失败"""
    assert login("admin", "wrong") is False


def test_logout():
    """测试登出"""
    logout()  # 不应抛出异常
EOF

echo ""
echo "✅ State C 完成：代码已实现"
echo ""

# =============================================================================
# State D: Verify (宪法审计)
# =============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 State D: Verify (宪法审计)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "运行测试..."
cd "$TARGET_PROJECT"
python3 -m pytest tests/ -v || true
cd - > /dev/null

echo ""
echo "运行宪法审计..."
python3 "$CDD_ROOT/scripts/cdd_auditor.py" --gate all --target "$TARGET_PROJECT" || true

echo ""
echo "✅ State D 完成：审计已执行"
echo ""

# =============================================================================
# State E: Close (闭环归档)
# =============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 State E: Close (闭环归档)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "生成最终报告..."
python3 "$CDD_ROOT/scripts/cdd_diagnose.py" --target "$TARGET_PROJECT" --summary || true

echo ""
echo "项目结构："
tree "$TARGET_PROJECT" -L 2 2>/dev/null || ls -la "$TARGET_PROJECT"

echo ""
echo "✅ State E 完成：工作流结束"
echo ""

echo "=========================================="
echo "🎉 CDD 完整工作流演示完成！"
echo "=========================================="
echo ""
echo "项目已创建在: $TARGET_PROJECT"
echo ""
echo "后续操作："
echo "  1. 编辑 $TARGET_PROJECT/specs/ 中的规格文档"
echo "  2. 实现 $TARGET_PROJECT/src/ 中的业务代码"
echo "  3. 添加 $TARGET_PROJECT/tests/ 中的测试用例"
echo "  4. 定期运行审计确保合规"