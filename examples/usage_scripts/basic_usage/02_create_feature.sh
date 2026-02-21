#!/bin/bash
# =============================================================================
# CDD 示例：创建新特性
# =============================================================================
# 
# 本脚本演示如何使用 cdd_feature.py 创建新特性
#
# 宪法依据: §101, §102, §200

set -e

CDD_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
source_project="${1:-.}"
feature_name="${2:-demo-feature}"
feature_desc="${3:-这是一个演示特性}"

echo "=========================================="
echo "CDD 特性创建示例"
echo "=========================================="
echo ""
echo "目标项目: $source_project"
echo "特性名称: $feature_name"
echo "特性描述: $feature_desc"
echo ""

# 步骤1：检查孢子隔离
echo "📋 步骤1：检查目标项目..."
if [ "$source_project" = "." ]; then
    echo "⚠️  注意：使用当前目录作为目标"
    echo "   如果这是CDD技能库自身，操作会被阻止"
fi

# 步骤2：创建特性
echo ""
echo "📋 步骤2：创建特性..."
python3 "$CDD_ROOT/scripts/cdd_feature.py" create "$feature_name" \
    --description "$feature_desc" \
    --target "$source_project"

# 步骤3：查看创建结果
echo ""
echo "📋 步骤3：查看创建的特性..."
python3 "$CDD_ROOT/scripts/cdd_feature.py" list --target "$source_project"

echo ""
echo "✅ 特性创建完成！"
echo ""
echo "后续步骤："
echo "  1. 编辑 specs/*-$feature_name/ 目录下的文档"
echo "  2. 运行 'python scripts/cdd_auditor.py --gate 1' 验证版本"
echo "  3. 开始实现特性代码"