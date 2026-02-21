#!/bin/bash

# ============================================================================
# CDD 高级使用示例 01: 熵值优化和监控
# ============================================================================
# 
# 目的: 展示如何分析和优化项目熵值
# 宪法依据: §102§300.3 (熵值监控公理)
# 
# 本脚本演示以下功能:
# 1. 计算项目熵值并评估状态
# 2. 分析熵值热点（问题最严重的文件/目录）
# 3. 生成优化计划（模拟运行）
# 4. 执行优化操作
# 5. 验证优化结果
#
# 使用方法:
# 1. 修改 CDD_SKILL_ROOT 为实际的CDD技能路径
# 2. 修改 TARGET_PROJECT 为目标项目路径
# 3. 给脚本执行权限: chmod +x 01_entropy_optimization.sh
# 4. 运行脚本: ./01_entropy_optimization.sh
# 
# ============================================================================

set -e  # 遇到错误时退出脚本

# ============================================================================
# 配置变量 - 根据您的环境修改这些值
# ============================================================================

# CDD技能根目录 (必须修改)
CDD_SKILL_ROOT="/path/to/cdd"  # 请修改为实际的CDD技能路径

# 目标项目路径 (必须修改)
TARGET_PROJECT="/path/to/your/project"  # 请修改为需要优化的项目路径

# 脚本运行的工作目录 (默认为脚本所在目录)
WORKING_DIR="$(pwd)"

# 输出详细日志 (true/false)
VERBOSE=true

# 优化操作的确认模式 (true:需要人工确认, false:自动执行)
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
    
    # 检查熵值计算脚本
    ENTROPY_SCRIPT="$CDD_SKILL_ROOT/scripts/cdd_entropy.py"
    if [ ! -f "$ENTROPY_SCRIPT" ]; then
        log_error "找不到熵值计算脚本: $ENTROPY_SCRIPT"
        exit 1
    fi
    
    # 检查目标项目目录
    if [ ! -d "$TARGET_PROJECT" ]; then
        log_error "目标项目目录不存在: $TARGET_PROJECT"
        log_error "请修改脚本中的 TARGET_PROJECT 变量为正确的项目路径"
        exit 1
    fi
    
    # 检查Python可用性
    if ! command -v python3 &> /dev/null; then
        log_error "找不到 python3 命令"
        exit 1
    fi
    
    log_success "环境验证通过"
    log_info "CDD技能目录: $CDD_SKILL_ROOT"
    log_info "目标项目目录: $TARGET_PROJECT"
}

# ============================================================================
# 熵值计算函数
# ============================================================================

calculate_entropy() {
    log_substep "正在计算系统熵值..."
    
    local cmd="python3 \"$CDD_SKILL_ROOT/scripts/cdd_entropy.py\" calculate --project \"$TARGET_PROJECT\""
    
    if [ "$VERBOSE" = "true" ]; then
        cmd="$cmd --verbose"
    fi
    
    # 执行计算
    if ! python3 "$CDD_SKILL_ROOT/scripts/cdd_entropy.py" calculate --project "$TARGET_PROJECT" --json > /tmp/cdd_entropy_result.json; then
        log_error "熵值计算失败"
        return 1
    fi
    
    # 解析结果
    local result_file="/tmp/cdd_entropy_result.json"
    if [ ! -f "$result_file" ] || [ ! -s "$result_file" ]; then
        log_error "熵值计算结果文件无效"
        return 1
    fi
    
    # 提取熵值信息
    local h_sys=$(python3 -c "import json; data=json.load(open('$result_file')); print(data.get('entropy_metrics', {}).get('h_sys', '0'))" 2>/dev/null || echo "0")
    local status=$(python3 -c "import json; data=json.load(open('$result_file')); print(data.get('entropy_metrics', {}).get('status', 'unknown'))" 2>/dev/null || echo "unknown")
    local compliance=$(python3 -c "import json; data=json.load(open('$result_file')); print(data.get('constitutional_compliance', 'false'))" 2>/dev/null || echo "false")
    
    # 显示结果
    echo "   熵值计算完成:"
    echo "     H_sys (系统熵值): $h_sys"
    echo "     状态: $status"
    echo "     宪法合规: $compliance"
    
    # 状态评估
    case "$status" in
        "normal")
            log_success "系统熵值正常 (H_sys = $h_sys)"
            return 0
            ;;
        "warning")
            log_warning "系统熵值警告 (H_sys = $h_sys) - 建议优化"
            return 2
            ;;
        "critical")
            log_error "系统熵值紧急 (H_sys = $h_sys) - 需要立即优化"
            return 3
            ;;
        *)
            log_warning "未知熵值状态: $status (H_sys = $h_sys)"
            return 4
            ;;
    esac
}

# ============================================================================
# 热点分析函数
# ============================================================================

analyze_hotspots() {
    log_substep "正在分析熵值热点..."
    
    # 运行热点分析
    if ! python3 "$CDD_SKILL_ROOT/scripts/cdd_entropy.py" analyze --project "$TARGET_PROJECT" --top-n 10 --json > /tmp/cdd_hotspots_result.json; then
        log_error "热点分析失败"
        return 1
    fi
    
    # 解析结果
    local result_file="/tmp/cdd_hotspots_result.json"
    local hotspots_count=$(python3 -c "import json; data=json.load(open('$result_file')); print(len(data.get('hotspots', [])))" 2>/dev/null || echo "0")
    
    echo "   发现 $hotspots_count 个熵值热点"
    
    # 显示前5个热点
    if [ "$hotspots_count" -gt 0 ]; then
        echo "   前5个热点:"
        python3 -c "
import json
with open('$result_file') as f:
    data = json.load(f)
hotspots = data.get('hotspots', [])[:5]
for i, h in enumerate(hotspots, 1):
    path = h.get('path', '未知')
    entropy = h.get('entropy', 0)
    reason = h.get('reason', '未知原因')
    print(f'      {i}. {path}')
    print(f'         熵值: {entropy:.2f}')
    print(f'         原因: {reason[:60]}...' if len(reason) > 60 else f'         原因: {reason}')
" 2>/dev/null || log_warning "无法解析热点详情"
    fi
    
    if [ "$hotspots_count" -eq 0 ]; then
        log_success "未发现明显的熵值热点"
        return 0
    elif [ "$hotspots_count" -le 5 ]; then
        log_warning "发现 $hotspots_count 个热点，建议关注"
        return 2
    else
        log_error "发现 $hotspots_count 个热点，需要立即处理"
        return 3
    fi
}

# ============================================================================
# 优化计划函数
# ============================================================================

generate_optimization_plan() {
    log_substep "正在生成优化计划..."
    
    # 生成优化计划（模拟运行）
    if ! python3 "$CDD_SKILL_ROOT/scripts/cdd_entropy.py" optimize --project "$TARGET_PROJECT" --dry-run --json > /tmp/cdd_optimization_plan.json; then
        log_error "优化计划生成失败"
        return 1
    fi
    
    # 解析结果
    local result_file="/tmp/cdd_optimization_plan.json"
    local actions_count=$(python3 -c "import json; data=json.load(open('$result_file')); print(data.get('actions_planned', 0))" 2>/dev/null || echo "0")
    local success=$(python3 -c "import json; data=json.load(open('$result_file')); print(data.get('success', 'false'))" 2>/dev/null || echo "false")
    
    if [ "$success" != "true" ] || [ "$actions_count" -eq 0 ]; then
        log_success "无需优化操作"
        return 0
    fi
    
    echo "   生成 $actions_count 个优化建议"
    
    # 显示优化建议
    echo "   前5个优化建议:"
    python3 -c "
import json
with open('$result_file') as f:
    data = json.load(f)
actions = data.get('actions', [])[:5]
for i, a in enumerate(actions, 1):
    desc = a.get('description', '未知')
    action_type = a.get('type', '未知')
    target = a.get('target', '未知')
    print(f'      {i}. {desc}')
    print(f'         类型: {action_type}')
    print(f'         目标: {target}')
" 2>/dev/null || log_warning "无法解析优化建议详情"
    
    return 2
}

# ============================================================================
# 执行优化函数
# ============================================================================

execute_optimization() {
    log_substep "正在执行优化..."
    
    # 确认执行
    if [ "$CONFIRMATION_MODE" = "true" ]; then
        echo ""
        read -p "🚀 是否执行优化操作? (Y/n): " -n 1 -r
        echo ""
        
        if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ -n $REPLY ]]; then
            log_info "跳过优化执行"
            return 0
        fi
    fi
    
    # 执行优化
    log_info "开始执行优化操作..."
    
    if python3 "$CDD_SKILL_ROOT/scripts/cdd_entropy.py" optimize --project "$TARGET_PROJECT" --json > /tmp/cdd_optimization_result.json; then
        local result_file="/tmp/cdd_optimization_result.json"
        local success=$(python3 -c "import json; data=json.load(open('$result_file')); print(data.get('success', 'false'))" 2>/dev/null || echo "false")
        
        if [ "$success" = "true" ]; then
            log_success "优化执行成功"
            
            # 显示执行结果
            local actions_executed=$(python3 -c "import json; data=json.load(open('$result_file')); print(data.get('actions_executed', 0))" 2>/dev/null || echo "0")
            echo "   执行了 $actions_executed 个优化操作"
            
            return 0
        else
            log_error "优化执行失败"
            return 1
        fi
    else
        log_error "优化执行过程出错"
        return 1
    fi
}

# ============================================================================
# 验证优化结果函数
# ============================================================================

verify_optimization_result() {
    log_substep "验证优化结果..."
    
    # 重新计算熵值
    if python3 "$CDD_SKILL_ROOT/scripts/cdd_entropy.py" calculate --project "$TARGET_PROJECT" --json > /tmp/cdd_post_optimization.json; then
        local result_file="/tmp/cdd_post_optimization.json"
        local h_sys_post=$(python3 -c "import json; data=json.load(open('$result_file')); print(data.get('entropy_metrics', {}).get('h_sys', '0'))" 2>/dev/null || echo "0")
        local status_post=$(python3 -c "import json; data=json.load(open('$result_file')); print(data.get('entropy_metrics', {}).get('status', 'unknown'))" 2>/dev/null || echo "unknown")
        
        # 获取优化前的熵值
        local h_sys_pre=$(python3 -c "import json; data=json.load(open('/tmp/cdd_entropy_result.json')); print(data.get('entropy_metrics', {}).get('h_sys', '0'))" 2>/dev/null || echo "0")
        
        echo "   优化前后对比:"
        echo "     优化前 H_sys: $h_sys_pre"
        echo "     优化后 H_sys: $h_sys_post"
        
        # 计算改进百分比
        local improvement=$(python3 -c "
pre = float('$h_sys_pre')
post = float('$h_sys_post')
if pre > 0:
    improvement = ((pre - post) / pre) * 100
    print(f'{improvement:.2f}%')
else:
    print('0%')
" 2>/dev/null || echo "0%")
        
        echo "     改进: $improvement"
        
        if [ "$(echo "$h_sys_post < $h_sys_pre" | bc -l 2>/dev/null || echo "0")" = "1" ]; then
            log_success "熵值降低 $improvement，优化有效"
            return 0
        else
            log_warning "熵值无明显改善 ($improvement)"
            return 1
        fi
    else
        log_warning "无法验证优化结果"
        return 2
    fi
}

# ============================================================================
# 主执行流程
# ============================================================================

main() {
    log_step "CDD 熵值优化和监控示例脚本 v2.0.0"
    echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "工作目录: $WORKING_DIR"
    echo "CDD技能目录: $CDD_SKILL_ROOT"
    echo "目标项目: $TARGET_PROJECT"
    echo "宪法依据: §102§300.3 (熵值监控公理)"
    
    # 步骤1: 环境验证
    check_environment
    
    # 步骤2: 计算熵值
    log_step "步骤2: 计算项目熵值"
    local entropy_status=0
    calculate_entropy || entropy_status=$?
    
    # 根据熵值状态决定后续步骤
    case $entropy_status in
        0)  # normal
            log_info "熵值正常，跳过深度分析"
            skip_deep_analysis=true
            ;;
        2)  # warning
            log_warning "熵值警告，建议进行分析和优化"
            skip_deep_analysis=false
            ;;
        3)  # critical
            log_error "熵值紧急，必须进行优化"
            skip_deep_analysis=false
            ;;
        *)  # unknown/error
            log_warning "熵值状态未知，继续进行后续步骤"
            skip_deep_analysis=false
            ;;
    esac
    
    # 步骤3: 热点分析（如果熵值不正常）
    if [ "${skip_deep_analysis:-false}" = "false" ]; then
        log_step "步骤3: 分析熵值热点"
        analyze_hotspots
        
        # 步骤4: 生成优化计划
        log_step "步骤4: 生成优化计划"
        if generate_optimization_plan; then
            # 步骤5: 执行优化
            log_step "步骤5: 执行优化"
            execute_optimization
            
            # 步骤6: 验证优化结果
            log_step "步骤6: 验证优化结果"
            verify_optimization_result
        else
            log_info "无需优化操作"
        fi
    else
        log_step "步骤3-6: 跳过（熵值正常）"
        log_info "由于熵值状态正常，跳过热点分析和优化步骤"
    fi
    
    # 步骤7: 最终熵值计算
    log_step "步骤7: 最终状态评估"
    log_info "计算最终熵值状态..."
    calculate_entropy
    
    # 完成总结
    log_step "脚本执行完成"
    echo "✅ 熵值优化流程完成!"
    echo ""
    echo "📋 下一步建议:"
    
    case $entropy_status in
        0)
            echo "   1. ✅ 保持良好实践，定期监控熵值"
            echo "   2. 建议每周运行一次熵值检查"
            echo "   3. 在新特性开发中继续遵循CDD标准"
            ;;
        2)
            echo "   1. 🔧 建议在本周内进行进一步优化"
            echo "   2. 分析具体热点，制定改进计划"
            echo "   3. 使用交互式向导: python $CDD_SKILL_ROOT/scripts/cdd_entropy.py guided"
            ;;
        3)
            echo "   1. 🚨 立即处理熵值超标问题"
            echo "   2. 根据热点分析结果制定紧急修复计划"
            echo "   3. 运行深度诊断: python $CDD_SKILL_ROOT/scripts/cdd_diagnose.py --fix"
            ;;
    esac
    
    echo ""
    echo "💡 相关命令:"
    echo "   python $CDD_SKILL_ROOT/scripts/cdd_entropy.py calculate --project \"$TARGET_PROJECT\""
    echo "   python $CDD_SKILL_ROOT/scripts/cdd_entropy.py analyze --project \"$TARGET_PROJECT\""
    echo "   python $CDD_SKILL_ROOT/scripts/cdd_entropy.py optimize --project \"$TARGET_PROJECT\""
    echo ""
    echo "宪法依据: §102 (熵值监控公理), §300.3 (行为验证标准)"
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
    echo "   1. 检查 CDD_SKILL_ROOT 和 TARGET_PROJECT 路径是否正确"
    echo "   2. 确保目标项目是有效的CDD项目"
    echo "   3. 检查项目权限: ls -la \"$TARGET_PROJECT\""
    echo "   4. 手动运行命令: python \"$CDD_SKILL_ROOT/scripts/cdd_entropy.py\" calculate --project \"$TARGET_PROJECT\""
    echo "   5. 使用详细模式: 设置 VERBOSE=true"
    
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
        log_success "✅ 熵值优化脚本执行成功!"
    else
        echo ""
        log_error "❌ 熵值优化脚本执行失败"
        exit 1
    fi
fi

# ============================================================================
# 脚本使用示例
# ============================================================================
#
# 1. 基本使用:
#    ./01_entropy_optimization.sh
#
# 2. 修改配置后使用:
#    export CDD_SKILL_ROOT="/opt/cdd"
#    export TARGET_PROJECT="/home/user/myproject"
#    export VERBOSE=false
#    export CONFIRMATION_MODE=false
#    ./01_entropy_optimization.sh
#
# 3. 在CI/CD中使用:
#    # 自动执行所有优化
#    CONFIRMATION_MODE=false ./01_entropy_optimization.sh
#
# 4. 仅分析不执行:
#    # 修改脚本第46行: CONFIRMATION_MODE=true
#    # 然后在确认时输入 n
#    ./01_entropy_optimization.sh
#
# ============================================================================