#!/bin/bash

# ============================================================================
# CDD 基础使用示例 01: 环境检查和修复
# ============================================================================
# 
# 目的: 展示如何检查和修复CDD环境依赖
# 宪法依据: §100.3 (版本一致性检查)
# 
# 本脚本演示以下功能:
# 1. 检查Python、pytest、PyYAML等必需依赖
# 2. 自动修复发现的依赖问题
# 3. 验证环境配置结果
#
# 使用方法:
# 1. 修改 CDD_SKILL_ROOT 为实际的CDD技能路径
# 2. 给脚本执行权限: chmod +x 01_environment_check.sh
# 3. 运行脚本: ./01_environment_check.sh
# 
# ============================================================================

set -e  # 遇到错误时退出脚本

# ============================================================================
# 配置变量 - 根据您的环境修改这些值
# ============================================================================

# CDD技能根目录 (必须修改)
CDD_SKILL_ROOT="/path/to/cdd"  # 请修改为实际的CDD技能路径

# 脚本运行的工作目录 (默认为脚本所在目录)
WORKING_DIR="$(pwd)"

# 输出详细日志 (true/false)
VERBOSE=true

# ============================================================================
# 初始化函数
# ============================================================================

log_info() {
    echo "ℹ️  $1"
}

log_success() {
    echo "✅ $1"
}

log_warning() {
    echo "⚠️  $1"
}

log_error() {
    echo "❌ $1"
}

log_step() {
    echo ""
    echo "📋 $1"
    echo "="$(printf '=%.0s' {1..50})
}

check_cdd_root() {
    # 检查CDD技能根目录是否存在
    if [ ! -d "$CDD_SKILL_ROOT" ]; then
        log_error "CDD技能目录不存在: $CDD_SKILL_ROOT"
        log_error "请修改脚本中的 CDD_SKILL_ROOT 变量为正确的CDD技能路径"
        exit 1
    fi
    
    # 检查必要的脚本文件
    CHECK_ENV_SCRIPT="$CDD_SKILL_ROOT/scripts/cdd_check_env.py"
    if [ ! -f "$CHECK_ENV_SCRIPT" ]; then
        log_error "找不到环境检查脚本: $CHECK_ENV_SCRIPT"
        log_error "请确保CDD技能目录结构完整"
        exit 1
    fi
    
    log_success "CDD技能目录验证通过: $CDD_SKILL_ROOT"
}

# ============================================================================
# 主执行流程
# ============================================================================

main() {
    log_step "CDD 环境检查示例脚本 v2.0.0"
    echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "工作目录: $WORKING_DIR"
    echo "CDD技能目录: $CDD_SKILL_ROOT"
    
    # 步骤1: 验证CDD技能目录
    log_step "步骤1: 验证CDD技能目录"
    check_cdd_root
    
    # 步骤2: 运行基本环境检查 (不修复)
    log_step "步骤2: 运行基础环境检查"
    log_info "检查必需依赖: Python, pytest, PyYAML"
    
    if [ "$VERBOSE" = "true" ]; then
        python3 "$CHECK_ENV_SCRIPT" --verbose
    else
        python3 "$CHECK_ENV_SCRIPT"
    fi
    
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        log_success "环境检查通过! 所有必需依赖已安装"
    else
        log_warning "环境检查发现问题 (退出码: $EXIT_CODE)"
        log_info "建议运行自动修复..."
    fi
    
    # 步骤3: 询问是否运行自动修复
    log_step "步骤3: 自动修复环境问题"
    
    if [ $EXIT_CODE -eq 0 ]; then
        log_info "环境已正常，跳过修复"
    else
        echo ""
        read -p "🔧 是否运行自动修复? (Y/n): " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
            log_info "正在运行自动修复..."
            
            if [ "$VERBOSE" = "true" ]; then
                python3 "$CHECK_ENV_SCRIPT" --fix --verbose
            else
                python3 "$CHECK_ENV_SCRIPT" --fix
            fi
            
            FIX_EXIT_CODE=$?
            
            if [ $FIX_EXIT_CODE -eq 0 ]; then
                log_success "自动修复完成!"
            else
                log_warning "自动修复完成，但可能仍有问题 (退出码: $FIX_EXIT_CODE)"
            fi
            
            # 重新检查环境
            log_info "重新检查修复后的环境..."
            python3 "$CHECK_ENV_SCRIPT" --quiet
            
            if [ $? -eq 0 ]; then
                log_success "✅ 环境修复成功! 所有必需依赖现在都已安装"
            else
                log_error "❌ 环境仍然存在问题"
                log_info "请手动检查并安装缺失的依赖"
            fi
        else
            log_info "跳过自动修复"
        fi
    fi
    
    # 步骤4: 验证修复后的环境
    log_step "步骤4: 验证环境功能"
    
    log_info "1. 验证Python版本..."
    PYTHON_VERSION=$(python3 --version 2>&1 || echo "未知")
    log_info "   Python: $PYTHON_VERSION"
    
    log_info "2. 验证pytest可用性..."
    if command -v pytest >/dev/null 2>&1; then
        PYTEST_VERSION=$(pytest --version 2>&1 | head -n 1 || echo "未知")
        log_success "   pytest: $PYTEST_VERSION"
    else
        log_warning "   pytest: 未安装或不在PATH中"
    fi
    
    log_info "3. 验证PyYAML可用性..."
    if python3 -c "import yaml; print('PyYAML可用')" 2>/dev/null; then
        log_success "   PyYAML: 可用"
    else
        log_warning "   PyYAML: 无法导入"
    fi
    
    # 步骤5: 运行CDD技能验证
    log_step "步骤5: CDD技能完整性验证"
    
    VERIFY_SCRIPT="$CDD_SKILL_ROOT/scripts/cdd_verify.py"
    if [ -f "$VERIFY_SCRIPT" ]; then
        log_info "验证CDD技能完整性..."
        python3 "$VERIFY_SCRIPT" --quiet
        
        if [ $? -eq 0 ]; then
            log_success "CDD技能完整性验证通过"
        else
            log_warning "CDD技能完整性验证发现问题"
            log_info "建议运行: python $VERIFY_SCRIPT --fix"
        fi
    else
        log_warning "找不到技能验证脚本: $VERIFY_SCRIPT"
    fi
    
    # 完成总结
    log_step "脚本执行完成"
    echo "✅ 环境检查流程完成!"
    echo ""
    echo "📋 下一步建议:"
    echo "   1. 如果所有检查通过，可以继续使用CDD"
    echo "   2. 如果有问题未解决，请查看上面的错误信息"
    echo "   3. 手动安装缺失的依赖:"
    echo "      - Python: 确保版本 ≥ 3.8"
    echo "      - pytest: pip install pytest"
    echo "      - PyYAML: pip install pyyaml"
    echo ""
    echo "宪法依据: §100.3 (版本一致性检查)"
    echo "完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
}

# ============================================================================
# 异常处理
# ============================================================================

handle_error() {
    log_error "脚本执行出错!"
    log_error "错误发生在第 $1 行"
    log_error "退出码: $2"
    
    echo ""
    echo "💡 故障排除建议:"
    echo "   1. 检查 CDD_SKILL_ROOT 路径是否正确"
    echo "   2. 确保您有Python执行权限"
    echo "   3. 手动运行: python $CDD_SKILL_ROOT/scripts/cdd_check_env.py"
    echo "   4. 查看详细日志: 设置 VERBOSE=true"
    
    exit 1
}

# ============================================================================
# 脚本入口
# ============================================================================

# 设置错误处理
trap 'handle_error ${LINENO} $?' ERR

# 检查是否直接运行脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # 检查必需命令
    if ! command -v python3 &> /dev/null; then
        log_error "找不到 python3 命令"
        log_error "请先安装 Python 3.8 或更高版本"
        exit 1
    fi
    
    # 运行主函数
    main
    
    # 检查最终状态
    if [ $? -eq 0 ]; then
        echo ""
        log_success "✅ 环境检查脚本执行成功!"
    else
        echo ""
        log_error "❌ 环境检查脚本执行失败"
        exit 1
    fi
fi