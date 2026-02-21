.PHONY: help audit gate1 gate2 gate3 gate4 gate5 fix-versions clean clean-cache cache-info test test-coverage entropy-analyze entropy-optimize

# 默认目标：显示帮助（P1改进版）
help:
	@echo "📚 CDD Local Development Interface (P1改进版)"
	@echo "=========================================="
	@echo ""
	@echo "⚠️  ⚠️  ⚠️  重要说明 ⚠️  ⚠️  ⚠️"
	@echo ""
	@echo "此Makefile操作的是CDD技能库本身，而不是外部项目。"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "✅ 对外部项目的操作（推荐方式）:"
	@echo ""
	@echo "  # 方法1: 在项目目录中使用完整路径"
	@echo "  cd /path/to/your/project"
	@echo "  python /path/to/cdd/scripts/cdd_feature.py deploy \"项目名\""
	@echo "  python /path/to/cdd/scripts/cdd_feature.py create \"特性名\""
	@echo "  python /path/to/cdd/scripts/cdd_auditor.py --gate all"
	@echo ""
	@echo "  # 方法2: 使用 --target 参数（从任意位置）"
	@echo "  python /path/to/cdd/scripts/cdd_feature.py deploy \"项目名\" --target /path/to/your/project"
	@echo "  python /path/to/cdd/scripts/cdd_auditor.py --gate all --target /path/to/your/project"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "🛠️  对CDD技能库本身的操作（仅限开发和维护）:"
	@echo ""
	@echo "  make audit           : 运行完整宪法审计（Gate 1-5）"
	@echo "  make gate1           : 验证版本一致性（§100.3）"
	@echo "  make gate2           : 验证系统行为（Tier 3）"
	@echo "  make gate3           : 测量系统熵值（H_sys）"
	@echo "  make gate4           : 语义审计（需要API密钥）"
	@echo "  make gate5           : 检查宪法引用完整性（§305）"
	@echo "  make fix-versions    : 自动修复版本不一致"
	@echo ""
	@echo "🧹 清理命令:"
	@echo "  make clean           : 清理缓存和临时文件"
	@echo "  make clean-cache     : 仅清理熵值缓存"
	@echo "  make cache-info      : 显示熵值缓存信息"
	@echo ""
	@echo "🧪 测试命令:"
	@echo "  make test            : 运行所有测试"
	@echo "  make test-coverage   : 运行测试并生成覆盖率报告"
	@echo ""
	@echo "📊 熵值命令:"
	@echo "  make entropy-analyze : 分析熵值热点"
	@echo "  make entropy-optimize: 运行熵值优化器（预览模式）"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "📖 需要帮助？查看以下文档:"
	@echo "  • QUICK_REFERENCE.md     - 快速参考指南（1-2分钟）"
	@echo "  • GETTING_STARTED.md     - 快速上手指南（5-10分钟）"
	@echo "  • TROUBLESHOOTING.md     - 故障排除指南"
	@echo ""
	@echo "💡 提示: 首次使用请运行环境检查"
	@echo "   python scripts/cdd_check_env.py --fix"

# 🛡️ 运行完整宪法审计
audit: gate1 gate2 gate3 gate4 gate5
	@echo "\n✅ 🏛️  All Constitutional Gates (1-5) Passed! System is compliant."

# Gate 1: 版本一致性 (§100.3)
gate1:
	@echo "\n🛡️  [Gate 1] Checking Version Consistency (§100.3)..."
	python scripts/cdd_auditor.py --gate 1

# Gate 2: 行为验证 (Tier 3)
gate2:
	@echo "\n⚖️  [Gate 2] Verifying Behavior (Tier 3)..."
	python scripts/cdd_auditor.py --gate 2

# Gate 3: 熵值监控 (System Thermodynamics)
gate3:
	@echo "\n📉 [Gate 3] Measuring System Entropy..."
	python scripts/cdd_auditor.py --gate 3

# Gate 4: 语义审计 (LLM-Judge)
gate4:
	@echo "\n⚖️  [Gate 4] Performing Semantic Audit (LLM-as-a-Judge)..."
	python scripts/cdd_auditor.py --gate 4

# Gate 5: 宪法引用完整性 (§305)
gate5:
	@echo "\n📜 [Gate 5] Checking Constitution Reference Integrity (§305)..."
	python3 scripts/cdd_auditor.py --gate 5

# 🔧 工具：自动修复版本
fix-versions:
	python scripts/cdd_auditor.py --gate 1 --fix

# 🧹 工具：清理环境（包含缓存）
clean:
	rm -rf __pycache__ .pytest_cache
	rm -rf tests/__pycache__ scripts/__pycache__
	rm -f .entropy_cache.json
	@echo "🧹 Environment cleaned (including cache)."

# 🗑️ 专门清理熵值缓存
clean-cache:
	@echo "🗑️  Cleaning entropy cache..."
	rm -f .entropy_cache.json
	@echo "✅ Entropy cache cleaned."

# ℹ️ 显示缓存信息
cache-info:
	@echo "📊 Entropy Cache Information"
	@echo "=========================="
	python scripts/cdd_entropy.py cache-info

# 🧪 运行测试
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v

# 📊 测试覆盖率报告
test-coverage:
	@echo "📊 Running tests with coverage report..."
	python -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated in htmlcov/"

# 🔍 熵值热点分析
entropy-analyze:
	@echo "🔍 Analyzing entropy hotspots..."
	python scripts/cdd_entropy.py analyze --format both

# ⚡ 自动化熵值优化 (干运行)
entropy-optimize:
	@echo "⚡ Running entropy optimizer (dry-run)..."
	python scripts/cdd_entropy.py optimize --dry-run --format markdown
	@echo ""
	@echo "To apply changes, run: python scripts/cdd_entropy.py optimize"