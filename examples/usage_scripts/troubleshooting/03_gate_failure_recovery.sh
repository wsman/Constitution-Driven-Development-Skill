#!/bin/bash
# =============================================================================
# CDD 故障排除：Gate 失败恢复
# =============================================================================
# 
# 当审计 Gate 失败时的通用恢复步骤
#
# 宪法依据: §101, §102, §300

set -e

CDD_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
TARGET="${1:-.}"
GATE="${2:-all}"

echo "=========================================="
echo "CDD 故障排除：Gate 失败恢复"
echo "=========================================="
echo ""
echo "目标项目: $TARGET"
echo "检查 Gate: $GATE"
echo ""

# 运行诊断
echo "📋 运行综合诊断..."
python3 "$CDD_ROOT/scripts/cdd_diagnose.py" --target "$TARGET" --verbose || true

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Gate 失败解决方案"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Gate 1 失败 (版本不一致):"
echo "  原因: 项目中的版本号不一致"
echo "  解决: python scripts/cdd_auditor.py --gate 1 --fix"
echo ""

echo "Gate 2 失败 (测试失败):"
echo "  原因: 测试用例未通过"
echo "  解决: pytest tests/ -v 查看详情，修复失败的测试"
echo ""

echo "Gate 3 失败 (熵值过高):"
echo "  原因: 系统熵值超过阈值"
echo "  解决: bash examples/usage_scripts/troubleshooting/02_entropy_high_fix.sh"
echo ""

echo "Gate 4 失败 (语义审计):"
echo "  原因: 宪法引用覆盖率不足或主题不合规"
echo "  解决: 添加更多 §格式的宪法引用到代码中"
echo ""

echo "Gate 5 失败 (引用格式错误):"
echo "  原因: 宪法引用格式不正确或引用了不存在的条款"
echo "  解决: 确保引用格式为 §NNN 或 §NNN.N，且条款存在"
echo ""

# 尝试自动修复
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "自动修复"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "是否尝试自动修复？[y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "运行自动修复..."
    python3 "$CDD_ROOT/scripts/cdd_auditor.py" --gate "$GATE" --fix --target "$TARGET" || true
    
    echo ""
    echo "重新运行审计..."
    python3 "$CDD_ROOT/scripts/cdd_auditor.py" --gate "$GATE" --target "$TARGET" || true
else
    echo "⏭️  跳过自动修复"
fi

echo ""
echo "=========================================="
echo "恢复流程完成"
echo "=========================================="