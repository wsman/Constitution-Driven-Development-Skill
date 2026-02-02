.PHONY: help audit gate1 gate2 gate3 fix-versions clean

# 默认目标：显示帮助
help:
	@echo "📚 CDD Local Development Interface"
	@echo "================================="
	@echo "Available commands:"
	@echo "  make audit         : Run full constitutional audit (Gate 1-3)"
	@echo "  make gate1         : Verify Version Consistency (§102.3)"
	@echo "  make gate2         : Verify System Behavior (Tier 3)"
	@echo "  make gate3         : Measure System Entropy (H_sys)"
	@echo "  make fix-versions  : Auto-fix version inconsistencies"
	@echo "  make clean         : Clean up cache and temp files"

# 🛡️ 运行完整宪法审计
audit: gate1 gate2 gate3
	@echo "\n✅ 🏛️  All Constitutional Gates Passed! System is compliant."

# Gate 1: 版本一致性 (§102.3)
gate1:
	@echo "\n🛡️  [Gate 1] Checking Version Consistency (§102.3)..."
	python scripts/verify_versions.py --verbose

# Gate 2: 行为验证 (Tier 3)
gate2:
	@echo "\n⚖️  [Gate 2] Verifying Behavior (Tier 3)..."
	pytest --verbose

# Gate 3: 熵值监控 (System Thermodynamics)
gate3:
	@echo "\n📉 [Gate 3] Measuring System Entropy..."
	python scripts/measure_entropy.py

# 🔧 工具：自动修复版本
fix-versions:
	python scripts/verify_versions.py --fix

# 🧹 工具：清理环境
clean:
	rm -rf __pycache__ .pytest_cache
	rm -rf tests/__pycache__ scripts/__pycache__
	@echo "🧹 Environment cleaned."