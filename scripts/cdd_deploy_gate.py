#!/usr/bin/env python3
"""
CDD Deploy Gate (cdd_deploy_gate.py) v1.0.0
===========================================
§306零停机部署协议验证工具，用于检查部署流水线是否符合宪法§306要求。

宪法依据: §306零停机协议公理、§101单一真理源原则、§102熵减原则、§151持久化原则

使用场景:
1. State D验证阶段：检查部署配置是否符合§306零停机要求
2. CI/CD流水线：集成到部署前验证步骤
3. 部署审计：定期检查生产环境部署合规性

Usage:
    python scripts/cdd_deploy_gate.py check [--config CONFIG] [--verbose]
    python scripts/cdd_deploy_gate.py validate <deployment_plan> [--verbose]
    python scripts/cdd_deploy_gate.py audit <environment> [--verbose]
    python scripts/cdd_deploy_gate.py generate-template [--type TYPE] [--output FILE]

示例:
    python scripts/cdd_deploy_gate.py check --config deployment.yaml --verbose
    python scripts/cdd_deploy_gate.py validate k8s/deployment-plan.json
    python scripts/cdd_deploy_gate.py audit production --verbose
    python scripts/cdd_deploy_gate.py generate-template --type kubernetes --output zero-downtime-template.yaml
"""

import sys
import os
import re
import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime
import subprocess

# 添加项目根目录到Python路径
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SKILL_ROOT))

VERSION = "2.0.0"

# -----------------------------------------------------------------------------
# 常量定义
# -----------------------------------------------------------------------------

# §306零停机部署协议要求
ZERO_DOWNTIME_REQUIREMENTS = {
    "deployment_strategies": {
        "required": ["blue_green", "canary", "rolling_update"],
        "minimum_strategies": 1
    },
    "health_checks": {
        "liveness_probe": True,
        "readiness_probe": True,
        "startup_probe": True  # 可选，但推荐
    },
    "rollback_mechanisms": {
        "automated_rollback": True,
        "rollback_timeout": "<10分钟",
        "rollback_triggers": ["health_check_failure", "performance_degradation", "constitution_violation"]
    },
    "monitoring_requirements": {
        "real_time_monitoring": True,
        "alerting_system": True,
        "performance_metrics": ["response_time", "error_rate", "throughput", "resource_usage"],
        "constitution_metrics": True
    },
    "traffic_management": {
        "gradual_traffic_shift": True,
        "session_affinity": False,  # 可选，根据应用决定
        "circuit_breaker": True  # 推荐
    }
}

# 支持的部署配置类型
SUPPORTED_CONFIG_TYPES = [
    "kubernetes",
    "docker_compose",
    "helm",
    "terraform",
    "ansible",
    "github_actions",
    "jenkinsfile",
    "custom"
]

# 部署策略检测模式
DEPLOYMENT_STRATEGY_PATTERNS = {
    "blue_green": [
        r'blue.*green',
        r'green.*blue',
        r'traffic.*shift',
        r'parallel.*deployment'
    ],
    "canary": [
        r'canary',
        r'gradual.*rollout',
        r'percentage.*traffic',
        r'weight.*distribution'
    ],
    "rolling_update": [
        r'rolling.*update',
        r'incremental.*deployment',
        r'pod.*by.*pod',
        r'maxUnavailable',
        r'maxSurge'
    ],
    "feature_toggle": [
        r'feature.*toggle',
        r'feature.*flag',
        r'config.*toggle'
    ]
}

# 健康检查检测模式
HEALTH_CHECK_PATTERNS = {
    "liveness_probe": [
        r'livenessProbe',
        r'liveness.*probe',
        r'health.*check.*liveness',
        r'health.*endpoint.*liveness'
    ],
    "readiness_probe": [
        r'readinessProbe',
        r'readiness.*probe',
        r'health.*check.*readiness',
        r'health.*endpoint.*readiness'
    ],
    "startup_probe": [
        r'startupProbe',
        r'startup.*probe'
    ]
}

# -----------------------------------------------------------------------------
# 核心验证逻辑
# -----------------------------------------------------------------------------

class ZeroDowntimeValidator:
    """§306零停机部署验证器"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = {
            "validation_time": datetime.now().isoformat(),
            "version": VERSION,
            "constitutional_basis": ["§306", "§101", "§102", "§151"],
            "requirements_checked": 0,
            "requirements_passed": 0,
            "requirements_failed": 0,
            "compliance_score": 0,
            "details": []
        }
    
    def check_configuration(self, config_path: Path, config_type: Optional[str] = None) -> Dict[str, Any]:
        """
        检查部署配置文件是否符合§306要求
        
        Args:
            config_path: 配置文件路径
            config_type: 配置类型（自动检测如果未提供）
        
        Returns:
            检查结果字典
        """
        if not config_path.exists():
            return {
                "success": False,
                "error": f"配置文件不存在: {config_path}",
                "config_path": str(config_path)
            }
        
        # 确定配置类型
        if config_type is None:
            config_type = self._detect_config_type(config_path)
        
        # 读取配置文件
        config_content = self._read_config_file(config_path)
        if config_content is None:
            return {
                "success": False,
                "error": "无法读取或解析配置文件",
                "config_path": str(config_path)
            }
        
        # 执行检查
        checks = self._perform_config_checks(config_content, config_type, config_path)
        
        # 计算合规分数
        total_checks = len(checks)
        passed_checks = sum(1 for check in checks if check.get("passed", False))
        compliance_score = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        self.results.update({
            "config_path": str(config_path),
            "config_type": config_type,
            "requirements_checked": total_checks,
            "requirements_passed": passed_checks,
            "requirements_failed": total_checks - passed_checks,
            "compliance_score": compliance_score,
            "details": checks
        })
        
        return {
            "success": True,
            "compliance_score": compliance_score,
            "config_type": config_type,
            "checks_performed": total_checks,
            "checks_passed": passed_checks,
            "detailed_results": checks,
            "summary": self._generate_summary(checks, compliance_score)
        }
    
    def validate_deployment_plan(self, plan_path: Path) -> Dict[str, Any]:
        """
        验证部署计划是否符合§306要求
        
        Args:
            plan_path: 部署计划文件路径
        
        Returns:
            验证结果字典
        """
        if not plan_path.exists():
            return {
                "success": False,
                "error": f"部署计划文件不存在: {plan_path}",
                "plan_path": str(plan_path)
            }
        
        # 读取部署计划
        plan_content = self._read_config_file(plan_path)
        if plan_content is None:
            return {
                "success": False,
                "error": "无法读取或解析部署计划",
                "plan_path": str(plan_path)
            }
        
        # 执行部署计划验证
        checks = self._validate_deployment_plan_content(plan_content, plan_path)
        
        # 计算合规分数
        total_checks = len(checks)
        passed_checks = sum(1 for check in checks if check.get("passed", False))
        compliance_score = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        return {
            "success": True,
            "compliance_score": compliance_score,
            "plan_valid": compliance_score >= 80,  # 至少80%合规
            "checks_performed": total_checks,
            "checks_passed": passed_checks,
            "detailed_checks": checks,
            "recommendations": self._generate_deployment_recommendations(checks)
        }
    
    def audit_environment(self, environment: str, kubeconfig: Optional[str] = None) -> Dict[str, Any]:
        """
        审计运行环境是否符合§306要求
        
        Args:
            environment: 环境名称（production, staging等）
            kubeconfig: Kubernetes配置文件路径（可选）
        
        Returns:
            审计结果字典
        """
        audit_results = {
            "environment": environment,
            "audit_time": datetime.now().isoformat(),
            "k8s_available": False,
            "deployments_found": 0,
            "compliance_by_deployment": {},
            "overall_compliance": 0
        }
        
        # 尝试检查Kubernetes环境
        k8s_available = self._check_kubernetes_availability(kubeconfig)
        audit_results["k8s_available"] = k8s_available
        
        if k8s_available:
            # 获取部署列表并检查
            deployments = self._get_k8s_deployments(kubeconfig)
            audit_results["deployments_found"] = len(deployments)
            
            compliance_scores = []
            for deployment in deployments:
                deployment_compliance = self._audit_k8s_deployment(deployment, kubeconfig)
                audit_results["compliance_by_deployment"][deployment] = deployment_compliance
                compliance_scores.append(deployment_compliance.get("compliance_score", 0))
            
            if compliance_scores:
                audit_results["overall_compliance"] = sum(compliance_scores) / len(compliance_scores)
        
        # 添加宪法合规检查
        audit_results["constitutional_checks"] = self._perform_constitutional_checks(environment)
        
        return {
            "success": True,
            "audit_results": audit_results,
            "environment_compliant": audit_results.get("overall_compliance", 0) >= 80,
            "recommendations": self._generate_environment_recommendations(audit_results)
        }
    
    def generate_template(self, template_type: str = "kubernetes", output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        生成符合§306要求的部署模板
        
        Args:
            template_type: 模板类型
            output_file: 输出文件路径（可选）
        
        Returns:
            模板生成结果
        """
        if template_type not in SUPPORTED_CONFIG_TYPES:
            return {
                "success": False,
                "error": f"不支持的模板类型: {template_type}",
                "supported_types": SUPPORTED_CONFIG_TYPES
            }
        
        # 生成模板
        template = self._generate_zero_downtime_template(template_type)
        
        # 输出到文件或返回内容
        if output_file:
            output_path = Path(output_file)
            try:
                if template_type in ["kubernetes", "helm"]:
                    output_path.write_text(yaml.dump(template, indent=2, default_flow_style=False))
                else:
                    output_path.write_text(json.dumps(template, indent=2))
                
                return {
                    "success": True,
                    "message": f"模板已保存到: {output_file}",
                    "template_type": template_type,
                    "file_path": output_file,
                    "template_preview": self._get_template_preview(template)
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"保存模板失败: {e}",
                    "template_type": template_type
                }
        else:
            return {
                "success": True,
                "template_type": template_type,
                "template": template
            }
    
    # -------------------------------------------------------------------------
    # 内部辅助方法
    # -------------------------------------------------------------------------
    
    def _detect_config_type(self, config_path: Path) -> str:
        """检测配置文件类型"""
        filename = config_path.name.lower()
        
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            content = config_path.read_text(encoding='utf-8', errors='ignore')
            if 'apiVersion:' in content and 'kind:' in content:
                return 'kubernetes'
            elif 'version:' in content and 'services:' in content:
                return 'docker_compose'
            elif 'chart:' in content:
                return 'helm'
        
        elif filename.endswith('.json'):
            content = config_path.read_text(encoding='utf-8', errors='ignore')
            if 'terraform' in content:
                return 'terraform'
        
        elif filename.endswith('.Jenkinsfile') or 'jenkins' in filename:
            return 'jenkinsfile'
        
        elif filename == 'deploy.yml' or filename == 'deploy.yaml':
            return 'github_actions'
        
        return 'custom'
    
    def _read_config_file(self, config_path: Path) -> Any:
        """读取配置文件"""
        try:
            content = config_path.read_text(encoding='utf-8', errors='ignore')
            
            if config_path.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(content)
            elif config_path.suffix == '.json':
                return json.loads(content)
            else:
                return content
        except Exception as e:
            if self.verbose:
                print(f"读取配置文件失败: {e}")
            return None
    
    def _perform_config_checks(self, config_content: Any, config_type: str, config_path: Path) -> List[Dict[str, Any]]:
        """执行配置检查"""
        checks = []
        
        # 1. 检查部署策略
        deployment_strategy_check = self._check_deployment_strategies(config_content, config_type)
        checks.append(deployment_strategy_check)
        
        # 2. 检查健康检查
        health_check_check = self._check_health_checks(config_content, config_type)
        checks.append(health_check_check)
        
        # 3. 检查回滚机制
        rollback_check = self._check_rollback_mechanisms(config_content, config_type)
        checks.append(rollback_check)
        
        # 4. 检查监控要求
        monitoring_check = self._check_monitoring_requirements(config_content, config_type)
        checks.append(monitoring_check)
        
        # 5. 检查流量管理
        traffic_check = self._check_traffic_management(config_content, config_type)
        checks.append(traffic_check)
        
        # 6. 检查宪法引用（§306）
        constitution_check = self._check_constitution_references(config_content, config_type)
        checks.append(constitution_check)
        
        return checks
    
    def _check_deployment_strategies(self, config_content: Any, config_type: str) -> Dict[str, Any]:
        """检查部署策略"""
        strategies_found = []
        
        # 根据配置类型使用不同的检测方法
        config_text = str(config_content).lower() if not isinstance(config_content, dict) else json.dumps(config_content).lower()
        
        for strategy, patterns in DEPLOYMENT_STRATEGY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, config_text, re.IGNORECASE):
                    strategies_found.append(strategy)
                    break
        
        # 评估结果
        required_strategies = ZERO_DOWNTIME_REQUIREMENTS["deployment_strategies"]["required"]
        min_strategies = ZERO_DOWNTIME_REQUIREMENTS["deployment_strategies"]["minimum_strategies"]
        
        has_minimum = len(set(strategies_found)) >= min_strategies
        has_required = any(strategy in strategies_found for strategy in required_strategies[:min_strategies])
        
        passed = has_minimum and has_required
        
        return {
            "check_type": "deployment_strategies",
            "passed": passed,
            "strategies_found": list(set(strategies_found)),
            "required_strategies": required_strategies[:min_strategies],
            "minimum_required": min_strategies,
            "suggestion": "确保配置包含至少一种零停机部署策略（蓝绿部署、金丝雀发布或滚动更新）"
        }
    
    def _check_health_checks(self, config_content: Any, config_type: str) -> Dict[str, Any]:
        """检查健康检查"""
        checks_found = []
        
        config_text = str(config_content).lower() if not isinstance(config_content, dict) else json.dumps(config_content).lower()
        
        for check_type, patterns in HEALTH_CHECK_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, config_text, re.IGNORECASE):
                    checks_found.append(check_type)
                    break
        
        # 评估结果
        requirements = ZERO_DOWNTIME_REQUIREMENTS["health_checks"]
        has_liveness = "liveness_probe" in checks_found
        has_readiness = "readiness_probe" in checks_found
        
        passed = has_liveness and has_readiness
        
        return {
            "check_type": "health_checks",
            "passed": passed,
            "checks_found": checks_found,
            "requirements": {
                "liveness_probe_required": requirements["liveness_probe"],
                "readiness_probe_required": requirements["readiness_probe"],
                "startup_probe_recommended": requirements["startup_probe"]
            },
            "suggestion": "配置必须包含livenessProbe和readinessProbe以确保零停机部署"
        }
    
    def _check_rollback_mechanisms(self, config_content: Any, config_type: str) -> Dict[str, Any]:
        """检查回滚机制"""
        config_text = str(config_content).lower() if not isinstance(config_content, dict) else json.dumps(config_content).lower()
        
        # 检查回滚相关关键词
        rollback_keywords = [
            r'rollback',
            r'roll.*back',
            r'revert',
            r'undo.*deployment',
            r'automated.*rollback',
            r'failure.*policy'
        ]
        
        found_keywords = []
        for keyword in rollback_keywords:
            if re.search(keyword, config_text, re.IGNORECASE):
                found_keywords.append(keyword)
        
        # 简单评估：是否包含回滚相关配置
        passed = len(found_keywords) > 0
        
        return {
            "check_type": "rollback_mechanisms",
            "passed": passed,
            "keywords_found": found_keywords,
            "requirements": ZERO_DOWNTIME_REQUIREMENTS["rollback_mechanisms"],
            "suggestion": "配置应包含自动化回滚机制，在部署失败时自动恢复"
        }
    
    def _check_monitoring_requirements(self, config_content: Any, config_type: str) -> Dict[str, Any]:
        """检查监控要求"""
        config_text = str(config_content).lower() if not isinstance(config_content, dict) else json.dumps(config_content).lower()
        
        # 检查监控相关关键词
        monitoring_keywords = [
            r'monitor',
            r'metrics',
            r'alert',
            r'prometheus',
            r'grafana',
            r'performance',
            r'health.*dashboard'
        ]
        
        found_keywords = []
        for keyword in monitoring_keywords:
            if re.search(keyword, config_text, re.IGNORECASE):
                found_keywords.append(keyword)
        
        # 简单评估：是否包含监控相关配置
        passed = len(found_keywords) > 0
        
        return {
            "check_type": "monitoring_requirements",
            "passed": passed,
            "keywords_found": found_keywords,
            "requirements": ZERO_DOWNTIME_REQUIREMENTS["monitoring_requirements"],
            "suggestion": "配置应包含监控和告警设置，确保部署过程可观察"
        }
    
    def _check_traffic_management(self, config_content: Any, config_type: str) -> Dict[str, Any]:
        """检查流量管理"""
        config_text = str(config_content).lower() if not isinstance(config_content, dict) else json.dumps(config_content).lower()
        
        # 检查流量管理相关关键词
        traffic_keywords = [
            r'traffic.*shift',
            r'gradual.*rollout',
            r'weight',
            r'percentage',
            r'load.*balancer',
            r'ingress',
            r'circuit.*breaker'
        ]
        
        found_keywords = []
        for keyword in traffic_keywords:
            if re.search(keyword, config_text, re.IGNORECASE):
                found_keywords.append(keyword)
        
        # 简单评估：是否包含流量管理相关配置
        passed = len(found_keywords) > 0
        
        return {
            "check_type": "traffic_management",
            "passed": passed,
            "keywords_found": found_keywords,
            "requirements": ZERO_DOWNTIME_REQUIREMENTS["traffic_management"],
            "suggestion": "配置应包含流量管理策略，支持渐进式流量切换"
        }
    
    def _check_constitution_references(self, config_content: Any, config_type: str) -> Dict[str, Any]:
        """检查宪法引用（§306）"""
        config_text = str(config_content) if not isinstance(config_content, dict) else json.dumps(config_content)
        
        # 检查§306引用
        has_section_306 = "§306" in config_text or "零停机" in config_text or "zero.downtime" in config_text.lower()
        
        return {
            "check_type": "constitution_references",
            "passed": has_section_306,
            "found": has_section_306,
            "required_article": "§306",
            "suggestion": "在部署配置中添加§306宪法引用，明确零停机部署要求"
        }
    
    def _validate_deployment_plan_content(self, plan_content: Any, plan_path: Path) -> List[Dict[str, Any]]:
        """验证部署计划内容"""
        checks = []
        
        # 转换为文本进行检查
        if isinstance(plan_content, dict):
            plan_text = json.dumps(plan_content)
        else:
            plan_text = str(plan_content)
        
        # 1. 检查是否有明确的部署阶段
        has_phases = any(keyword in plan_text.lower() for keyword in ["stage", "phase", "step", "environment"])
        checks.append({
            "check": "deployment_phases",
            "passed": has_phases,
            "description": "部署计划应包含明确的阶段划分",
            "suggestion": "将部署计划分为开发、测试、预生产、生产等阶段"
        })
        
        # 2. 检查是否有验证步骤
        has_validation = any(keyword in plan_text.lower() for keyword in ["validate", "verify", "check", "test", "approval"])
        checks.append({
            "check": "validation_steps",
            "passed": has_validation,
            "description": "部署计划应包含验证步骤",
            "suggestion": "在每个部署阶段后添加验证步骤，确保部署质量"
        })
        
        # 3. 检查是否有回滚计划
        has_rollback = any(keyword in plan_text.lower() for keyword in ["rollback", "revert", "backout", "recovery"])
        checks.append({
            "check": "rollback_plan",
            "passed": has_rollback,
            "description": "部署计划应包含回滚方案",
            "suggestion": "为每个部署阶段定义明确的回滚条件和步骤"
        })
        
        # 4. 检查是否有监控计划
        has_monitoring = any(keyword in plan_text.lower() for keyword in ["monitor", "alert", "metric", "dashboard", "observability"])
        checks.append({
            "check": "monitoring_plan",
            "passed": has_monitoring,
            "description": "部署计划应包含监控方案",
            "suggestion": "定义部署后的监控指标和告警阈值"
        })
        
        # 5. 检查宪法合规性
        has_constitution = "§306" in plan_text or "宪法" in plan_text
        checks.append({
            "check": "constitution_compliance",
            "passed": has_constitution,
            "description": "部署计划应引用§306零停机协议",
            "suggestion": "在部署计划中明确引用§306宪法条款"
        })
        
        return checks
    
    def _check_kubernetes_availability(self, kubeconfig: Optional[str] = None) -> bool:
        """检查Kubernetes可用性"""
        try:
            cmd = ["kubectl"]
            if kubeconfig:
                cmd.extend(["--kubeconfig", kubeconfig])
            cmd.extend(["cluster-info"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def _get_k8s_deployments(self, kubeconfig: Optional[str] = None) -> List[str]:
        """获取Kubernetes部署列表"""
        try:
            cmd = ["kubectl"]
            if kubeconfig:
                cmd.extend(["--kubeconfig", kubeconfig])
            cmd.extend(["get", "deployments", "-o", "jsonpath='{.items[*].metadata.name}'"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                deployments = result.stdout.strip().strip("'").split()
                return deployments
        except Exception:
            pass
        
        return []
    
    def _audit_k8s_deployment(self, deployment_name: str, kubeconfig: Optional[str] = None) -> Dict[str, Any]:
        """审计Kubernetes部署"""
        try:
            cmd = ["kubectl"]
            if kubeconfig:
                cmd.extend(["--kubeconfig", kubeconfig])
            cmd.extend(["get", "deployment", deployment_name, "-o", "yaml"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                deployment_config = yaml.safe_load(result.stdout)
                return self._check_k8s_deployment_config(deployment_config, deployment_name)
        except Exception as e:
            if self.verbose:
                print(f"审计部署 {deployment_name} 失败: {e}")
        
        return {
            "deployment": deployment_name,
            "audit_success": False,
            "compliance_score": 0
        }
    
    def _check_k8s_deployment_config(self, config: Dict[str, Any], deployment_name: str) -> Dict[str, Any]:
        """检查Kubernetes部署配置"""
        checks = []
        
        # 检查部署策略
        strategy = config.get("spec", {}).get("strategy", {})
        has_strategy = bool(strategy)
        checks.append({
            "check": "deployment_strategy",
            "passed": has_strategy,
            "details": strategy
        })
        
        # 检查健康检查
        containers = config.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
        health_checks_found = False
        for container in containers:
            if "livenessProbe" in container or "readinessProbe" in container:
                health_checks_found = True
                break
        
        checks.append({
            "check": "health_checks",
            "passed": health_checks_found,
            "details": {"containers_with_health_checks": health_checks_found}
        })
        
        # 检查副本数
        replicas = config.get("spec", {}).get("replicas", 0)
        has_multiple_replicas = replicas > 1
        checks.append({
            "check": "multiple_replicas",
            "passed": has_multiple_replicas,
            "details": {"replicas": replicas}
        })
        
        # 计算合规分数
        total_checks = len(checks)
        passed_checks = sum(1 for check in checks if check.get("passed", False))
        compliance_score = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        return {
            "deployment": deployment_name,
            "audit_success": True,
            "compliance_score": compliance_score,
            "checks": checks,
            "total_checks": total_checks,
            "passed_checks": passed_checks
        }
    
    def _perform_constitutional_checks(self, environment: str) -> List[Dict[str, Any]]:
        """执行宪法合规检查"""
        checks = [
            {
                "article": "§306",
                "check": "zero_downtime_capability",
                "description": "环境是否支持零停机部署",
                "status": "unknown",  # 需要更详细的检查
                "recommendation": "实施蓝绿部署或金丝雀发布策略"
            },
            {
                "article": "§101",
                "check": "configuration_sync",
                "description": "部署配置是否同步更新",
                "status": "unknown",
                "recommendation": "确保代码和配置变更同步"
            },
            {
                "article": "§102",
                "check": "entropy_reduction",
                "description": "部署是否降低系统熵值",
                "status": "unknown",
                "recommendation": "优化部署流程，减少复杂度"
            },
            {
                "article": "§151",
                "check": "audit_logging",
                "description": "部署过程是否有审计日志",
                "status": "unknown",
                "recommendation": "记录所有部署操作和变更"
            }
        ]
        
        return checks
    
    def _generate_zero_downtime_template(self, template_type: str) -> Dict[str, Any]:
        """生成零停机部署模板"""
        if template_type == "kubernetes":
            return {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {
                    "name": "app-zero-downtime",
                    "labels": {
                        "app": "example",
                        "constitution.article.306": "true"
                    },
                    "annotations": {
                        "deployment.strategy": "blue-green",
                        "zero.downtime.enabled": "true",
                        "constitution.reference": "§306"
                    }
                },
                "spec": {
                    "replicas": 3,
                    "strategy": {
                        "type": "RollingUpdate",
                        "rollingUpdate": {
                            "maxSurge": "25%",
                            "maxUnavailable": "0"
                        }
                    },
                    "selector": {
                        "matchLabels": {
                            "app": "example"
                        }
                    },
                    "template": {
                        "metadata": {
                            "labels": {
                                "app": "example",
                                "version": "2.0.0"
                            }
                        },
                        "spec": {
                            "containers": [
                                {
                                    "name": "app",
                                    "image": "example/app:latest",
                                    "ports": [
                                        {
                                            "containerPort": 8080
                                        }
                                    ],
                                    "livenessProbe": {
                                        "httpGet": {
                                            "path": "/health",
                                            "port": 8080
                                        },
                                        "initialDelaySeconds": 30,
                                        "periodSeconds": 10
                                    },
                                    "readinessProbe": {
                                        "httpGet": {
                                            "path": "/ready",
                                            "port": 8080
                                        },
                                        "initialDelaySeconds": 5,
                                        "periodSeconds": 5
                                    },
                                    "resources": {
                                        "requests": {
                                            "memory": "128Mi",
                                            "cpu": "100m"
                                        },
                                        "limits": {
                                            "memory": "256Mi",
                                            "cpu": "200m"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        else:
            # 通用模板
            return {
                "template_type": template_type,
                "constitution_compliant": True,
                "zero_downtime_requirements": ZERO_DOWNTIME_REQUIREMENTS,
                "configuration_notes": f"根据§306零停机协议要求配置{template_type}部署",
                "implementation_guide": [
                    "1. 选择部署策略：蓝绿部署、金丝雀发布或滚动更新",
                    "2. 配置健康检查：livenessProbe和readinessProbe",
                    "3. 设置自动化回滚机制",
                    "4. 实现渐进式流量切换",
                    "5. 配置监控和告警",
                    "6. 记录部署审计日志"
                ]
            }
    
    def _generate_summary(self, checks: List[Dict[str, Any]], compliance_score: float) -> Dict[str, Any]:
        """生成检查摘要"""
        passed_checks = [c for c in checks if c.get("passed", False)]
        failed_checks = [c for c in checks if not c.get("passed", False)]
        
        summary = {
            "compliance_score": compliance_score,
            "compliance_status": "compliant" if compliance_score >= 80 else "non_compliant",
            "total_checks": len(checks),
            "passed_checks": len(passed_checks),
            "failed_checks": len(failed_checks),
            "critical_checks": [
                check for check in checks 
                if check.get("check_type") in ["deployment_strategies", "health_checks"]
            ]
        }
        
        if failed_checks:
            summary["improvement_areas"] = [
                {
                    "area": check.get("check_type", "unknown"),
                    "suggestion": check.get("suggestion", "请参考§306要求改进")
                }
                for check in failed_checks
            ]
        
        return summary
    
    def _generate_deployment_recommendations(self, checks: List[Dict[str, Any]]) -> List[str]:
        """生成部署建议"""
        recommendations = []
        
        for check in checks:
            if not check.get("passed", False):
                suggestion = check.get("suggestion")
                if suggestion:
                    recommendations.append(suggestion)
        
        # 添加通用建议
        if not recommendations:
            recommendations.append("部署计划基本符合§306要求，继续保持")
        else:
            recommendations.insert(0, "请根据以下建议改进部署计划以符合§306零停机协议：")
        
        return recommendations
    
    def _generate_environment_recommendations(self, audit_results: Dict[str, Any]) -> List[str]:
        """生成环境建议"""
        recommendations = []
        
        overall_compliance = audit_results.get("overall_compliance", 0)
        
        if overall_compliance < 80:
            recommendations.append(f"环境合规率较低 ({overall_compliance:.1f}%)，建议优化部署配置")
        
        if not audit_results.get("k8s_available", False):
            recommendations.append("Kubernetes环境不可用，无法进行深度审计")
        
        # 检查每个部署的合规性
        for deployment, compliance in audit_results.get("compliance_by_deployment", {}).items():
            deployment_score = compliance.get("compliance_score", 0)
            if deployment_score < 80:
                recommendations.append(f"部署 '{deployment}' 合规率较低 ({deployment_score:.1f}%)，建议检查配置")
        
        if not recommendations:
            recommendations.append("环境审计通过，部署配置基本符合§306要求")
        
        return recommendations
    
    def _get_template_preview(self, template: Dict[str, Any]) -> str:
        """获取模板预览"""
        if isinstance(template, dict) and "apiVersion" in template:
            # Kubernetes YAML模板
            return yaml.dump(template, indent=2, default_flow_style=False)
        else:
            # 其他类型模板
            return json.dumps(template, indent=2, ensure_ascii=False)

# -----------------------------------------------------------------------------
# CLI接口
# -----------------------------------------------------------------------------

def format_check_result(result: Dict[str, Any], verbose: bool = False) -> str:
    """格式化检查结果输出"""
    output = []
    
    output.append(f"🚀 CDD Deploy Gate v{VERSION}")
    output.append(f"📅 检查时间: {result.get('validation_time', datetime.now().isoformat())}")
    output.append("=" * 40)
    
    if not result.get("success", False):
        output.append(f"❌ 检查失败: {result.get('error', 'Unknown error')}")
        return "\n".join(output)
    
    # 显示基本信息
    output.append(f"📄 配置文件: {result.get('config_path', 'N/A')}")
    output.append(f"📋 配置类型: {result.get('config_type', 'unknown')}")
    output.append(f"📊 合规分数: {result.get('compliance_score', 0):.1f}%")
    
    # 显示检查结果摘要
    summary = result.get("summary", {})
    compliance_status = summary.get("compliance_status", "unknown")
    status_emoji = "✅" if compliance_status == "compliant" else "❌"
    
    output.append(f"📋 合规状态: {compliance_status.upper()} {status_emoji}")
    output.append(f"🔍 检查总数: {summary.get('total_checks', 0)}")
    output.append(f"✅ 通过检查: {summary.get('passed_checks', 0)}")
    output.append(f"❌ 失败检查: {summary.get('failed_checks', 0)}")
    
    # 显示关键检查结果（详细模式）
    if verbose and "detailed_results" in result:
        output.append("\n🔍 详细检查结果:")
        for check in result["detailed_results"]:
            check_type = check.get("check_type", "unknown")
            passed = check.get("passed", False)
            icon = "✅" if passed else "❌"
            
            output.append(f"\n  {icon} {check_type}:")
            output.append(f"     状态: {'通过' if passed else '失败'}")
            
            if "strategies_found" in check:
                output.append(f"     找到策略: {', '.join(check['strategies_found'])}")
            
            if "checks_found" in check:
                output.append(f"     找到检查: {', '.join(check['checks_found'])}")
            
            if "keywords_found" in check:
                output.append(f"     相关关键词: {', '.join(check['keywords_found'])}")
            
            if "suggestion" in check and not passed:
                output.append(f"     建议: {check['suggestion']}")
    
    # 显示建议
    if "summary" in result and "improvement_areas" in result["summary"]:
        output.append("\n💡 改进建议:")
        for area in result["summary"]["improvement_areas"]:
            output.append(f"  • {area.get('area')}: {area.get('suggestion', '请参考§306要求')}")
    
    return "\n".join(output)

def format_validation_result(result: Dict[str, Any]) -> str:
    """格式化验证结果输出"""
    output = []
    
    output.append(f"📋 CDD Deployment Plan Validator v{VERSION}")
    output.append("=" * 40)
    
    if not result.get("success", False):
        output.append(f"❌ 验证失败: {result.get('error', 'Unknown error')}")
        return "\n".join(output)
    
    output.append(f"📊 合规分数: {result.get('compliance_score', 0):.1f}%")
    output.append(f"✅ 计划有效性: {'有效' if result.get('plan_valid', False) else '无效'}")
    output.append(f"🔍 检查总数: {result.get('checks_performed', 0)}")
    output.append(f"✅ 通过检查: {result.get('checks_passed', 0)}")
    
    if result.get("plan_valid", False):
        output.append("\n🎉 部署计划符合§306零停机协议要求")
    else:
        output.append("\n⚠️  部署计划需要改进以符合§306要求")
    
    # 显示建议
    recommendations = result.get("recommendations", [])
    if recommendations:
        output.append("\n💡 建议:")
        for rec in recommendations:
            output.append(f"  • {rec}")
    
    return "\n".join(output)

def format_audit_result(result: Dict[str, Any]) -> str:
    """格式化审计结果输出"""
    output = []
    
    output.append(f"🔍 CDD Environment Auditor v{VERSION}")
    output.append("=" * 40)
    
    if not result.get("success", False):
        output.append(f"❌ 审计失败: {result.get('error', 'Unknown error')}")
        return "\n".join(output)
    
    audit_results = result.get("audit_results", {})
    
    output.append(f"🌍 审计环境: {audit_results.get('environment', 'N/A')}")
    output.append(f"📅 审计时间: {audit_results.get('audit_time', 'N/A')}")
    output.append(f"🐳 Kubernetes可用: {'✅' if audit_results.get('k8s_available', False) else '❌'}")
    
    if audit_results.get("k8s_available", False):
        output.append(f"📦 找到部署: {audit_results.get('deployments_found', 0)} 个")
        output.append(f"📊 环境合规率: {audit_results.get('overall_compliance', 0):.1f}%")
        
        # 显示部署合规详情
        compliance_by_deployment = audit_results.get("compliance_by_deployment", {})
        if compliance_by_deployment:
            output.append("\n📋 部署合规详情:")
            for deployment, compliance in compliance_by_deployment.items():
                score = compliance.get("compliance_score", 0)
                status_emoji = "✅" if score >= 80 else "❌"
                output.append(f"  {status_emoji} {deployment}: {score:.1f}%")
    
    # 宪法检查
    constitutional_checks = audit_results.get("constitutional_checks", [])
    if constitutional_checks:
        output.append("\n⚖️ 宪法合规检查:")
        for check in constitutional_checks:
            article = check.get("article", "?")
            description = check.get("description", "")
            status = check.get("status", "unknown")
            
            status_emoji = {
                "passed": "✅",
                "failed": "❌",
                "warning": "⚠️",
                "unknown": "❓"
            }.get(status, "❓")
            
            output.append(f"  {status_emoji} {article}: {description}")
    
    output.append(f"\n📋 环境合规状态: {'✅ 合规' if result.get('environment_compliant', False) else '❌ 不合规'}")
    
    # 显示建议
    recommendations = result.get("recommendations", [])
    if recommendations:
        output.append("\n💡 建议:")
        for rec in recommendations:
            output.append(f"  • {rec}")
    
    return "\n".join(output)

def format_template_result(result: Dict[str, Any]) -> str:
    """格式化模板生成结果"""
    output = []
    
    output.append(f"📄 CDD Template Generator v{VERSION}")
    output.append("=" * 40)
    
    if not result.get("success", False):
        output.append(f"❌ 模板生成失败: {result.get('error', 'Unknown error')}")
        return "\n".join(output)
    
    output.append(f"📋 模板类型: {result.get('template_type', 'unknown')}")
    
    if "file_path" in result:
        output.append(f"💾 保存位置: {result.get('file_path')}")
        output.append(f"✅ 模板已成功保存")
    else:
        output.append("📝 生成的模板内容:")
        output.append("-" * 40)
        
        template = result.get("template", {})
        if isinstance(template, dict) and "apiVersion" in template:
            output.append(yaml.dump(template, indent=2, default_flow_style=False))
        else:
            output.append(json.dumps(template, indent=2, ensure_ascii=False))
    
    return "\n".join(output)

# -----------------------------------------------------------------------------
# 主函数
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=f"CDD Deploy Gate v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/cdd_deploy_gate.py check --config deployment.yaml --verbose
  python scripts/cdd_deploy_gate.py validate k8s/deployment-plan.json
  python scripts/cdd_deploy_gate.py audit production --verbose
  python scripts/cdd_deploy_gate.py generate-template --type kubernetes --output zero-downtime.yaml
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="检查部署配置")
    check_parser.add_argument("--config", "-c", required=True, help="配置文件路径")
    check_parser.add_argument("--type", "-t", choices=SUPPORTED_CONFIG_TYPES, 
                              help="配置类型（自动检测如果未提供）")
    check_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    check_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # validate 命令
    validate_parser = subparsers.add_parser("validate", help="验证部署计划")
    validate_parser.add_argument("plan", help="部署计划文件路径")
    validate_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    validate_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # audit 命令
    audit_parser = subparsers.add_parser("audit", help="审计运行环境")
    audit_parser.add_argument("environment", help="环境名称（production, staging等）")
    audit_parser.add_argument("--kubeconfig", "-k", help="Kubernetes配置文件路径")
    audit_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    audit_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    # generate-template 命令
    template_parser = subparsers.add_parser("generate-template", help="生成部署模板")
    template_parser.add_argument("--type", "-t", choices=SUPPORTED_CONFIG_TYPES, 
                                 default="kubernetes", help="模板类型")
    template_parser.add_argument("--output", "-o", help="输出文件路径")
    template_parser.add_argument("--json", "-j", action="store_true", help="JSON输出格式")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    validator = ZeroDowntimeValidator(verbose=args.verbose)
    
    try:
        if args.command == "check":
            config_path = Path(args.config).resolve()
            result = validator.check_configuration(config_path, args.type)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_check_result(result, args.verbose))
            
            # 退出码：合规率<80%则返回1
            compliance_score = result.get("compliance_score", 0) if result.get("success", False) else 0
            sys.exit(0 if compliance_score >= 80 else 1)
        
        elif args.command == "validate":
            plan_path = Path(args.plan).resolve()
            result = validator.validate_deployment_plan(plan_path)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_validation_result(result))
            
            # 退出码：计划无效则返回1
            sys.exit(0 if result.get("plan_valid", False) else 1)
        
        elif args.command == "audit":
            result = validator.audit_environment(args.environment, args.kubeconfig)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_audit_result(result))
            
            # 退出码：环境不合规则返回1
            sys.exit(0 if result.get("environment_compliant", False) else 1)
        
        elif args.command == "generate-template":
            result = validator.generate_template(args.type, args.output)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_template_result(result))
            
            sys.exit(0 if result.get("success", False) else 1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  操作被用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

# -----------------------------------------------------------------------------
# Claude Code桥梁接口
# -----------------------------------------------------------------------------

def check_deploy_config_claude(config_path: str, config_type: Optional[str] = None, **kwargs) -> dict:
    """Claude Code部署配置检查接口"""
    config_path_obj = Path(config_path).resolve()
    if not config_path_obj.exists():
        return {"success": False, "error": f"配置文件不存在: {config_path}"}
    
    validator = ZeroDowntimeValidator(kwargs.get('verbose', False))
    result = validator.check_configuration(config_path_obj, config_type)
    
    result["tool_version"] = VERSION
    
    return result

def validate_deploy_plan_claude(plan_path: str, **kwargs) -> dict:
    """Claude Code部署计划验证接口"""
    plan_path_obj = Path(plan_path).resolve()
    if not plan_path_obj.exists():
        return {"success": False, "error": f"部署计划文件不存在: {plan_path}"}
    
    validator = ZeroDowntimeValidator(kwargs.get('verbose', False))
    result = validator.validate_deployment_plan(plan_path_obj)
    
    result["tool_version"] = VERSION
    
    return result

def audit_environment_claude(environment: str, kubeconfig: Optional[str] = None, **kwargs) -> dict:
    """Claude Code环境审计接口"""
    validator = ZeroDowntimeValidator(kwargs.get('verbose', False))
    result = validator.audit_environment(environment, kubeconfig)
    
    result["tool_version"] = VERSION
    
    return result

def generate_template_claude(template_type: str = "kubernetes", output_file: Optional[str] = None, **kwargs) -> dict:
    """Claude Code模板生成接口"""
    validator = ZeroDowntimeValidator(kwargs.get('verbose', False))
    result = validator.generate_template(template_type, output_file)
    
    result["tool_version"] = VERSION
    
    return result

if __name__ == "__main__":
    main()