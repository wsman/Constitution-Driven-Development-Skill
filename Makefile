.PHONY: help audit gate1 gate2 gate3 fix-versions clean clean-cache cache-info

# 默认目标：显示帮助
help:
	@echo "📚 CDD Local Development Interface"
	@echo "================================="
	@echo "⚠️  NOTE: These commands act on the CDD SKILL repository ITSELF, not external projects."
	@echo ""
	@echo "Available commands:"
	@echo "  make audit         : Run full constitutional audit (Gate 1-3)"
	@echo "  make gate1         : Verify Version Consistency (§102.3)"
	@echo "  make gate2         : Verify System Behavior (Tier 3)"
	@echo "  make gate3         : Measure System Entropy (H_sys)"
	@echo "  make fix-versions  : Auto-fix version inconsistencies"
	@echo "  make clean         : Clean up cache and temp files"
	@echo "  make clean-cache   : Clean entropy cache only"
	@echo "  make cache-info    : Show entropy cache information"

# 🛡️ 运行完整宪法审计
audit: gate1 gate2 gate3
	@echo "\n✅ 🏛️  All Constitutional Gates Passed! System is compliant."

# Gate 1: 版本一致性 (§102.3)
gate1:
	@echo "\n🛡️  [Gate 1] Checking Version Consistency (§102.3)..."
	python scripts/cdd_audit.py --gate 1

# Gate 2: 行为验证 (Tier 3)
gate2:
	@echo "\n⚖️  [Gate 2] Verifying Behavior (Tier 3)..."
	python scripts/cdd_audit.py --gate 2

# Gate 3: 熵值监控 (System Thermodynamics)
gate3:
	@echo "\n📉 [Gate 3] Measuring System Entropy..."
	python scripts/cdd_audit.py --gate 3

# 🔧 工具：自动修复版本
fix-versions:
	python scripts/verify_versions.py --fix

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
	python scripts/measure_entropy.py --cache-info
