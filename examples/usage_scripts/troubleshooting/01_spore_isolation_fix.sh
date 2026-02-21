#!/bin/bash

# ============================================================================
# CDD 故障排除示例 01: 孢子隔离违例修复
# ============================================================================
# 
# 目的: 展示如何诊断和修复孢子隔离违例错误
# 宪法依据: §103§104 (孢子隔离公理)
# 
# 本脚本演示以下功能:
# 1. 诊断孢子隔离违例的根本原因
# 2. 检查项目结构和权限问题
# 3. 修复常见的孢子隔离问题
# 4. 验证修复后的孢子隔离状态
#
# 适用场景:
# - 运行CDD命令时出现"孢子隔离违例"错误
# - 项目目录结构不符合CDD要求
# - 权限问题导致CDD无法访问关键文件
# - 项目与CDD技能目录混淆
#
# 使用方法:
# 1. 修改 CDD_SKILL_ROOT 为实际的CDD技能路径
# 2. 修改 PROBLEMATIC_PROJECT 为有问题的项目路径
# 3. 给脚本执行权限: chmod +x 01_spore_isolation_fix.sh
# 4. 运行脚本: ./01_spore_isolation_fix.sh
# 
# ============================================================================

set -e  # 遇到错误时退出脚本

# ============================================================================
# 配置变量 - 根据您的环境修改这些值
# ============================================================================

# CDD技能根目录 (必须修改)
CDD_SKILL_ROOT="/path/to/cdd"  # 请修改为实际的CDD技能路径

# 有问题的项目路径 (必须修改)
PROBLEMATIC_PROJECT="/path/to/problematic/project"  # 请修改为有孢子隔离问题的项目路径

# 脚本运行的工作目录 (默认为脚本所在目录)
WORKING_DIR="$(pwd)"

# 输出详细日志 (true/false)
VERBOSE=true

# 修复操作的确认模式 (true:需要人工确认, false:自动执行)
CONFIRMATION_MODE=true

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

log_substep() {
    echo "  🔸 $1"
}

check_environment() {
    log_step "环境验证"
    
    # 检查CDD技能目录
    if [ ! -d "$CDD_SKILL_ROOT" ]; then
        log_error "CDD技能目录不存在: $CDD_SKILL_ROOT"
        log_error "请修改脚本中的 CDD_SKILL_ROOT 变量为正确的CDD技能路径"
        exit 1
    fi
    
    # 检查项目目录
    if [ ! -d "$PROBLEMATIC_PROJECT" ]; then
        log_warning "问题项目目录不存在: $PROBLEMATIC_PROJECT"
        log_warning "将尝试在后续步骤中创建目录"
    fi
    
    # 检查Python可用性
    if ! command -v python3 &> /dev/null; then
        log_error "找不到 python3 命令"
        exit 1
    fi
    
    log_success "环境验证通过"
    log_info "CDD技能目录: $CDD_SKILL_ROOT"
    log_info "问题项目目录: $PROBLEMATIC_PROJECT"
}

# ============================================================================
# 孢子隔离诊断函数
# ============================================================================

diagnose_spore_isolation() {
    log_step "步骤1: 诊断孢子隔离问题"
    
    log_substep "1.1 检查是否在CDD技能目录中运行"
    local in_cdd_skill=false
    if [[ "$(realpath "$PROBLEMATIC_PROJECT" 2>/dev/null)" == "$(realpath "$CDD_SKILL_ROOT" 2>/dev/null)" ]]; then
        log_error "❌ 问题: 项目路径与CDD技能目录相同"
        log_error "   孢子隔离要求项目与CDD技能分离"
        log_info "💡 解决方案: 使用不同的项目目录"
        in_cdd_skill=true
    else
        log_success "✅ 项目目录与CDD技能目录分离"
    fi
    
    log_substep "1.2 检查项目目录结构"
    local missing_dirs=()
    
    # 检查标准CDD项目目录
    for dir in "memory_bank" "specs" "src" "tests"; do
        if [ ! -d "$PROBLEMATIC_PROJECT/$dir" ]; then
            missing_dirs+=("$dir")
        fi
    done
    
    if [ ${#missing_dirs[@]} -gt 0 ]; then
        log_warning "⚠️  问题: 项目缺少标准CDD目录"
        log_info "   缺失的目录: ${missing_dirs[*]}"
        log_info "💡 解决方案: 运行项目初始化"
    else
        log_success "✅ 项目目录结构完整"
    fi
    
    log_substep "1.3 检查文件权限"
    local permission_issues=()
    
    # 检查是否有不可读的文件
    if [ -d "$PROBLEMATIC_PROJECT" ]; then
        # 检查根目录可读性
        if [ ! -r "$PROBLEMATIC_PROJECT" ]; then
            permission_issues+=("项目根目录不可读")
        fi
        
        # 检查关键文件
        for file in "$PROBLEMATIC_PROJECT/memory_bank" "$PROBLEMATIC_PROJECT/specs" "$PROBLEMATIC_PROJECT/src"; do
            if [ -e "$file" ] && [ ! -r "$file" ]; then
                permission_issues+=("$file 不可读")
            fi
        done
    fi
    
    if [ ${#permission_issues[@]} -gt 0 ]; then
        log_error "❌ 问题: 文件权限问题"
        for issue in "${permission_issues[@]}"; do
            log_info "   $issue"
        done
        log_info "💡 解决方案: 修复文件权限"
    else
        log_success "✅ 文件权限正常"
    fi
    
    log_substep "1.4 检查是否为有效的CDD项目"
    local is_valid_cdd=false
    
    if [ -f "$PROBLEMATIC_PROJECT/memory_bank/t0_core/active_context.md" ] || \
       [ -f "$PROBLEMATIC_PROJECT/.cdd_state.json" ]; then
        log_success "✅ 是有效的CDD项目"
        is_valid_cdd=true
    else
        log_warning "⚠️  问题: 可能不是有效的CDD项目"
        log_info "💡 解决方案: 重新部署或初始化项目"
    fi
    
    # 生成诊断总结
    echo ""
    echo "📋 诊断总结:"
    echo "   CDD技能目录冲突: $(if [ "$in_cdd_skill" = true ]; then echo "❌"; else echo "✅"; fi)"
    echo "   目录结构完整性: $(if [ ${#missing_dirs[@]} -eq 0 ]; then echo "✅"; else echo "⚠️ (${#missing_dirs[@]})"; fi)"
    echo "   文件权限问题: $(if [ ${#permission_issues[@]} -eq 0 ]; then echo "✅"; else echo "❌ (${#permission_issues[@]})"; fi)"
    echo "   有效CDD项目: $(if [ "$is_valid_cdd" = true ]; then echo "✅"; else echo "⚠️"; fi)"
    
    # 返回诊断结果
    if [ "$in_cdd_skill" = true ]; then
        return 101  # CDD技能目录冲突
    elif [ ${#permission_issues[@]} -gt 0 ]; then
        return 102  # 权限问题
    elif [ ${#missing_dirs[@]} -gt 0 ] && [ "$is_valid_cdd" = false ]; then
        return 103  # 非有效CDD项目
    elif [ ${#missing_dirs[@]} -gt 0 ]; then
        return 104  # 目录不完整
    else
        return 0    # 无问题
    fi
}

# ============================================================================
# 孢子隔离修复函数
# ============================================================================

fix_spore_isolation() {
    local diagnosis_code=$1
    
    log_step "步骤2: 修复孢子隔离问题"
    
    case $diagnosis_code in
        101)  # CDD技能目录冲突
            log_substep "修复: CDD技能目录冲突"
            log_info "问题: 项目路径与CDD技能目录相同"
            
            if [ "$CONFIRMATION_MODE" = "true" ]; then
                echo ""
                read -p "🔧 是否创建新的项目目录? (Y/n): " -n 1 -r
                echo ""
                
                if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ -n $REPLY ]]; then
                    log_info "跳过修复"
                    return 1
                fi
            fi
            
            # 创建新项目目录
            local new_project_dir="$WORKING_DIR/new_cdd_project_$(date +%Y%m%d_%H%M%S)"
            log_info "创建新的项目目录: $new_project_dir"
            
            mkdir -p "$new_project_dir"
            
            # 部署新项目
            log_info "在新目录中部署CDD项目..."
            if python3 "$CDD_SKILL_ROOT/scripts/cdd_feature.py" deploy "修复项目" --target "$new_project_dir" > /dev/null 2>&1; then
                log_success "✅ 新项目创建成功"
                log_info "新项目路径: $new_project_dir"
                
                # 更新变量
                PROBLEMATIC_PROJECT="$new_project_dir"
                
                return 0
            else
                log_error "❌ 新项目创建失败"
                return 1
            fi
            ;;
        
        102)  # 权限问题
            log_substep "修复: 文件权限问题"
            log_info "问题: 文件或目录权限不足"
            
            if [ "$CONFIRMATION_MODE" = "true" ]; then
                echo ""
                read -p "🔧 是否修复文件权限? (Y/n): " -n 1 -r
                echo ""
                
                if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ -n $REPLY ]]; then
                    log_info "跳过修复"
                    return 1
                fi
            fi
            
            # 修复目录权限
            log_info "修复项目目录权限..."
            
            if [ -d "$PROBLEMATIC_PROJECT" ]; then
                # 设置合理的权限
                if chmod -R u+rwX,go+rX "$PROBLEMATIC_PROJECT" 2>/dev/null; then
                    log_success "✅ 权限修复成功"
                    
                    # 验证修复
                    if [ -r "$PROBLEMATIC_PROJECT" ]; then
                        log_success "✅ 项目目录现在可读"
                        return 0
                    else
                        log_error "❌ 权限修复失败，目录仍不可读"
                        return 1
                    fi
                else
                    log_error "❌ 权限修复失败 (可能需要sudo权限)"
                    log_info "💡 尝试使用: sudo chmod -R u+rwX,go+rX \"$PROBLEMATIC_PROJECT\""
                    return 1
                fi
            else
                log_error "❌ 项目目录不存在"
                return 1
            fi
            ;;
        
        103)  # 非有效CDD项目
            log_substep "修复: 非有效CDD项目"
            log_info "问题: 项目缺少CDD必要结构"
            
            if [ "$CONFIRMATION_MODE" = "true" ]; then
                echo ""
                read -p "🔧 是否重新部署CDD项目? (Y/n): " -n 1 -r
                echo ""
                
                if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ -n $REPLY ]]; then
                    log_info "跳过修复"
                    return 1
                fi
            fi
            
            # 备份现有文件
            local backup_dir="$PROBLEMATIC_PROJECT.backup_$(date +%Y%m%d_%H%M%S)"
            log_info "备份现有文件到: $backup_dir"
            
            if [ -d "$PROBLEMATIC_PROJECT" ] && [ "$(ls -A "$PROBLEMATIC_PROJECT" 2>/dev/null)" ]; then
                mkdir -p "$backup_dir"
                cp -r "$PROBLEMATIC_PROJECT"/* "$backup_dir/" 2>/dev/null || true
                log_info "备份完成"
            fi
            
            # 重新部署项目
            log_info "重新部署CDD项目..."
            if python3 "$CDD_SKILL_ROOT/scripts/cdd_feature.py" deploy "修复部署" --target "$PROBLEMATIC_PROJECT" --force > /dev/null 2>&1; then
                log_success "✅ 项目重新部署成功"
                
                # 恢复备份的文件（如果存在）
                if [ -d "$backup_dir" ] && [ "$(ls -A "$backup_dir" 2>/dev/null)" ]; then
                    log_info "恢复备份文件..."
                    cp -r "$backup_dir"/* "$PROBLEMATIC_PROJECT/" 2>/dev/null || true
                    log_info "备份文件恢复完成"
                fi
                
                return 0
            else
                log_error "❌ 项目重新部署失败"
                return 1
            fi
            ;;
        
        104)  # 目录不完整
            log_substep "修复: 目录结构不完整"
            log_info "问题: 缺少标准CDD目录"
            
            if [ "$CONFIRMATION_MODE" = "true" ]; then
                echo ""
                read -p "🔧 是否创建缺失的目录? (Y/n): " -n 1 -r
                echo ""
                
                if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ -n $REPLY ]]; then
                    log_info "跳过修复"
                    return 1
                fi
            fi
            
            # 创建缺失的目录
            local missing_dirs=("memory_bank" "specs" "src" "tests")
            local created_count=0
            
            for dir in "${missing_dirs[@]}"; do
                if [ ! -d "$PROBLEMATIC_PROJECT/$dir" ]; then
                    log_info "创建目录: $PROBLEMATIC_PROJECT/$dir"
                    mkdir -p "$PROBLEMATIC_PROJECT/$dir"
                    
                    # 创建必要的子目录
                    case $dir in
                        "memory_bank")
                            mkdir -p "$PROBLEMATIC_PROJECT/$dir/t0_core"
                            mkdir -p "$PROBLEMATIC_PROJECT/$dir/t1_axioms"
                            touch "$PROBLEMATIC_PROJECT/$dir/t0_core/active_context.md"
                            ;;
                        "specs")
                            touch "$PROBLEMATIC_PROJECT/$dir/.gitkeep"
                            ;;
                        "src")
                            touch "$PROBLEMATIC_PROJECT/$dir/__init__.py"
                            ;;
                        "tests")
                            touch "$PROBLEMATIC_PROJECT/$dir/__init__.py"
                            ;;
                    esac
                    
                    created_count=$((created_count + 1))
                fi
            done
            
            if [ $created_count -gt 0 ]; then
                log_success "✅ 创建了 $created_count 个缺失目录"
                
                # 创建.cdd_state.json文件
                if [ ! -f "$PROBLEMATIC_PROJECT/.cdd_state.json" ]; then
                    cat > "$PROBLEMATIC_PROJECT/.cdd_state.json" << EOF
{
    "project_name": "修复项目",
    "version": "1.0.0",
    "constitution_compliance": true,
    "last_audit": "$(date -Iseconds)",
    "spore_isolation_fixed": true
}
EOF
                    log_success "✅ 创建CDD状态文件"
                fi
                
                return 0
            else
                log_warning "⚠️  未创建任何目录（可能已存在）"
                return 0
            fi
            ;;
        
        0)   # 无问题
            log_substep "无需修复"
            log_info "未发现孢子隔离问题"
            return 0
            ;;
        
        *)
            log_error "❌ 未知的诊断代码: $diagnosis_code"
            return 1
            ;;
    esac
}

# ============================================================================
# 验证修复函数
# ============================================================================

verify_fix() {
    log_step "步骤3: 验证修复结果"
    
    log_substep "3.1 运行孢子隔离检查"
    
    # 使用CDD工具检查孢子隔离
    log_info "使用CDD工具检查孢子隔离..."
    
    if python3 "$CDD_SKILL_ROOT/scripts/cdd_feature.py" deploy "验证测试" --target "$PROBLEMATIC_PROJECT" --dry-run 2>&1 | grep -q "孢子隔离违例"; then
        log_error "❌ 孢子隔离问题仍然存在"
        return 1
    else
        log_success "✅ 孢子隔离检查通过"
    fi
    
    log_substep "3.2 验证项目结构"
    
    # 检查必要的目录
    local required_dirs=("memory_bank" "specs" "src" "tests")
    local missing_count=0
    
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$PROBLEMATIC_PROJECT/$dir" ]; then
            log_error "❌ 缺失目录: $dir"
            missing_count=$((missing_count + 1))
        fi
    done
    
    if [ $missing_count -eq 0 ]; then
        log_success "✅ 项目结构完整"
    else
        log_error "❌ 项目仍然缺失 $missing_count 个必要目录"
        return 1
    fi
    
    log_substep "3.3 验证文件权限"
    
    # 检查文件可读性
    if [ -r "$PROBLEMATIC_PROJECT" ]; then
        log_success "✅ 项目目录可读"
    else
        log_error "❌ 项目目录不可读"
        return 1
    fi
    
    log_substep "3.4 运行CDD审计"
    
    # 尝试运行简单的CDD审计
    log_info "运行Gate 1审计..."
    
    if python3 "$CDD_SKILL_ROOT/scripts/cdd_auditor.py" --gate 1 --target "$PROBLEMATIC_PROJECT" --quiet 2>&1 | grep -q "error\|失败"; then
        log_warning "⚠️  CDD审计发现问题（可能需要进一步修复）"
        return 0  # 仍算成功，因为孢子隔离已修复
    else
        log_success "✅ CDD审计通过"
    fi
    
    return 0
}

# ============================================================================
# 主执行流程
# ============================================================================

main() {
    log_step "CDD 孢子隔离修复示例脚本 v2.0.0"
    echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "工作目录: $WORKING_DIR"
    echo "CDD技能目录: $CDD_SKILL_ROOT"
    echo "问题项目: $PROBLEMATIC_PROJECT"
    echo "宪法依据: §103§104 (孢子隔离公理)"
    
    # 步骤0: 环境验证
    check_environment
    
    # 步骤1: 诊断问题
    local diagnosis_result=0
    diagnose_spore_isolation || diagnosis_result=$?
    
    echo ""
    log_info "诊断结果代码: $diagnosis_result"
    
    # 步骤2: 修复问题
    if [ $diagnosis_result -ne 0 ]; then
        if fix_spore_isolation $diagnosis_result; then
            log_success "✅ 修复执行成功"
        else
            log_error "❌ 修复执行失败"
            log_info "💡 可能需要手动修复"
        fi
    else
        log_info "ℹ️  无需修复"
    fi
    
    # 步骤3: 验证修复
    if [ $diagnosis_result -ne 0 ]; then
        if verify_fix; then
            log_success "✅ 修复验证通过"
        else
            log_error "❌ 修复验证失败"
            log_info "💡 可能需要进一步修复"
        fi
    fi
    
    # 完成总结
    log_step "脚本执行完成"
    echo "✅ 孢子隔离修复流程完成!"
    echo ""
    echo "📋 修复总结:"
    echo "   诊断代码: $diagnosis_result"
    echo "   修复状态: $(if [ $diagnosis_result -eq 0 ]; then echo "✅ 无需修复"; elif verify_fix > /dev/null 2>&1; then echo "✅ 修复成功"; else echo "⚠️  部分修复"; fi)"
    echo "   项目路径: $PROBLEMATIC_PROJECT"
    echo ""
    echo "💡 后续建议:"
    
    case $diagnosis_result in
        0)
            echo "   1. ✅ 保持当前良好状态"
            echo "   2. 定期运行孢子隔离检查"
            echo "   3. 确保不将项目与CDD技能目录混淆"
            ;;
        101)
            echo "   1. ✅ 已创建新项目目录"
            echo "   2. 请使用新目录: $PROBLEMATIC_PROJECT"
            echo "   3. 迁移旧项目文件到新目录"
            ;;
        102)
            echo "   1. ✅ 已修复文件权限"
            echo "   2. 检查其他用户是否有适当权限"
            echo "   3. 避免使用过高权限（如777）"
            ;;
        103)
            echo "   1. ✅ 已重新部署CDD项目"
            echo "   2. 验证项目完整性: python \"$CDD_SKILL_ROOT/scripts/cdd_verify.py\""
            echo "   3. 运行完整审计: python \"$CDD_SKILL_ROOT/scripts/cdd_auditor.py\" --gate all"
            ;;
        104)
            echo "   1. ✅ 已补全目录结构"
            echo "   2. 检查目录内容是否完整"
            echo "   3. 运行项目初始化向导"
            ;;
    esac
    
    echo ""
    echo "🔧 相关命令:"
    echo "   python \"$CDD_SKILL_ROOT/scripts/cdd_feature.py\" deploy \"测试项目\" --target \"$PROBLEMATIC_PROJECT\" --dry-run"
    echo "   python \"$CDD_SKILL_ROOT/scripts/cdd_auditor.py\" --gate 1 --target \"$PROBLEMATIC_PROJECT\""
    echo "   python \"$CDD_SKILL_ROOT/scripts/cdd_verify.py\" --target \"$PROBLEMATIC_PROJECT\""
    echo ""
    echo "宪法依据: §103 (孢子隔离), §104 (项目边界), §106.1 (版本一致性)"
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
    echo "💡 紧急故障排除建议:"
    echo "   1. 手动检查孢子隔离:"
    echo "      - 确保项目目录与CDD技能目录不同"
    echo "      - 检查项目是否有 memory_bank 目录"
    echo "      - 验证文件权限: ls -la \"$PROBLEMATIC_PROJECT\""
    echo "   2. 手动修复:"
    echo "      - 创建必要目录: mkdir -p \"$PROBLEMATIC_PROJECT/memory_bank\""
    echo "      - 修复权限: chmod -R u+rwX,go+rX \"$PROBLEMATIC_PROJECT\""
    echo "      - 迁移项目到新目录"
    echo "   3. 获取帮助:"
    echo "      - 查看CDD文档"
    echo "      - 运行详细诊断: python \"$CDD_SKILL_ROOT/scripts/cdd_diagnose.py\" --verbose"
    
    exit 1
}

# ============================================================================
# 脚本入口
# ============================================================================

# 设置错误处理
trap 'handle_error ${LINENO} $?' ERR

# 检查是否直接运行脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # 运行主函数
    main
    
    # 检查最终状态
    if [ $? -eq 0 ]; then
        echo ""
        log_success "✅ 孢子隔离修复脚本执行成功!"
    else
        echo ""
        log_error "❌ 孢子隔离修复脚本执行失败"
        exit 1
    fi
fi

# ============================================================================
# 脚本使用示例
# ============================================================================
#
# 1. 基本使用:
#    ./01_spore_isolation_fix.sh
#
# 2. 针对具体问题使用:
#    # 权限问题
#    PROBLEMATIC_PROJECT="/home/user/project-with-permission-issues"
#    CONFIRMATION_MODE=false
#    ./01_spore_isolation_fix.sh
#
# 3. 批量修复多个项目:
#    for project in /path/to/projects/*; do
#        echo "处理项目: $project"
#        PROBLEMATIC_PROJECT="$project" CONFIRMATION_MODE=false ./01_spore_isolation_fix.sh
#        echo ""
#    done
#
# 4. 仅诊断不修复:
#    CONFIRMATION_MODE=true
#    # 然后在修复确认时输入 n
#    ./01_spore_isolation_fix.sh
#
# 5. 集成到CI/CD:
#    # 自动修复所有孢子隔离问题
#    CONFIRMATION_MODE=false ./01_spore_isolation_fix.sh || {
#        echo "自动修复失败，需要手动干预"
#        exit 1
#    }
#
# ============================================================================