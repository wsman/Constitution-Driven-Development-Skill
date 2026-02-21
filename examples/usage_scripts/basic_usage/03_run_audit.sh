#!/bin/bash
# =============================================================================
# CDD 示例：运行审计
# =============================================================================
# 
# 本脚本演示如何使用 cdd_auditor.py 运行宪法审计
#
# 宪法依据: §101, §102, §300

set -e

CDD_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

echo "=========================================="
echo "CDD 宪法审计示例"
echo "=========================================="
echo ""

# 步骤1：运行所有Gate
echo "📋 步骤1：运行完整审计 (Gate 1-5)..."
echo ""

echo "Gate 1: 版本一致性检查"
python3 "$CDD_ROOT/scripts/cdd_auditor.py" --gate 1 --verbose
echo ""

echo "Gate 2: 行为验证（测试）"
python3 "$CDD_ROOT/scripts/cdd_auditor.py" --gate 2 --verbose
echo ""

echo "Gate 3: 熵值监控"
python3 "$CDD_ROOT/scripts/cdd_auditor.py" --gate 3 --verbose
echo ""

echo "Gate 4: 语义审计"
python3 "$CDD_ROOT/scripts/cdd_auditor.py" --gate 4 --verbose
echo ""

echo "Gate 5: 宪法引用完整性"
python3 "$CDD_ROOT/scripts/cdd_auditor.py" --gate 5 --verbose
echo ""

# 步骤2：综合诊断
echo "📋 步骤2：运行综合诊断..."
python3 "$CDD_ROOT/scripts/cdd_diagnose.py" --summary

echo ""
echo "✅ 审计完成！"
echo ""
echo "常见问题解决："
echo "  - Gate 1 失败: 运行 --fix 自动修复版本漂移"
echo "  - Gate 2 失败: 检查测试用例，运行 pytest -v 查看详情"
echo "  - Gate 3 失败: 运行 cdd_entropy.py optimize 优化熵值"
echo "  - Gate 4 失败: 添加更多宪法引用或检查主题合规"
echo "  - Gate 5 失败: 检查宪法引用格式是否正确"