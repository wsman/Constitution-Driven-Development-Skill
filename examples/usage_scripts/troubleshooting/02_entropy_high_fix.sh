#!/bin/bash
# =============================================================================
# CDD 故障排除：熵值过高修复
# =============================================================================
# 
# 当 Gate 3 失败（熵值超标）时的修复步骤
#
# 宪法依据: §102

set -e

CDD_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
TARGET="${1:-.}"

echo "=========================================="
echo "CDD 故障排除：熵值过高"
echo "=========================================="
echo ""
echo "目标项目: $TARGET"
echo ""

# 步骤1：查看当前熵值
echo "📋 步骤1：分析当前熵值..."
python3 "$CDD_ROOT/scripts/cdd_entropy.py" calculate --target "$TARGET" || true

echo ""

# 步骤2：查看熵值热点
echo "📋 步骤2：识别熵值热点..."
python3 "$CDD_ROOT/scripts/cdd_entropy.py" analyze --target "$TARGET" || true

echo ""

# 步骤3：生成优化建议
echo "📋 步骤3：生成优化建议..."
python3 "$CDD_ROOT/scripts/cdd_entropy.py" optimize --dry-run --target "$TARGET" || true

echo ""

# 步骤4：执行优化（需要确认）
echo "📋 步骤4：执行优化..."
read -p "是否执行熵值优化？[y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 "$CDD_ROOT/scripts/cdd_entropy.py" optimize --target "$TARGET" || true
    echo ""
    echo "✅ 优化完成，重新计算熵值..."
    python3 "$CDD_ROOT/scripts/cdd_entropy.py" calculate --target "$TARGET" || true
else
    echo "⏭️  跳过优化"
fi

echo ""
echo "=========================================="
echo "修复完成"
echo "=========================================="
echo ""
echo "如果熵值仍然过高，请手动检查："
echo "  1. 是否有重复的代码片段"
echo "  2. 是否有未使用的依赖"
echo "  3. 是否有不一致的命名风格"
echo "  4. 是否有缺失的文档"