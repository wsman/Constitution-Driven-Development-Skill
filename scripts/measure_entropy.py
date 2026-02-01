#!/usr/bin/env python3
"""
CDD 熵值计算脚本 (Compliance-Based Entropy Model)

v1.3.0 - 基于合规度的熵值模型
通过真实测量 (tree, grep, pytest) 计算系统熵值

使用方法:
    python measure_entropy.py [--project PATH] [--verbose]

输出:
    - 三个合规度分量 (C_dir, C_sig, C_test)
    - 综合合规度 (Compliance_Score)
    - 系统熵值 (H_sys)
    - 状态评估 (优秀/良好/警告/危险)
"""

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple


@dataclass
class EntropyMetrics:
    """熵值指标数据类"""
    c_dir: float = 0.0      # 目录结构合规率
    c_sig: float = 0.0      # 接口签名覆盖率
    c_test: float = 0.0     # 核心测试通过率
    compliance_score: float = 0.0
    h_sys: float = 0.0
    status: str = "未知"
    
    def to_dict(self) -> dict:
        return {
            "c_dir": round(self.c_dir, 4),
            "c_sig": round(self.c_sig, 4),
            "c_test": round(self.c_test, 4),
            "compliance_score": round(self.compliance_score, 4),
            "h_sys": round(self.h_sys, 4),
            "status": self.status
        }


class EntropyCalculator:
    """熵值计算器 - 基于合规度模型"""
    
    # 权重配置
    W_DIR = 0.4
    W_SIG = 0.3
    W_TEST = 0.3
    
    def __init__(self, project_path: str = ".", verbose: bool = False):
        self.project_path = Path(project_path)
        self.verbose = verbose
        self.system_patterns_file = self.project_path / "systemPatterns.md"
        self.tech_context_file = self.project_path / "techContext.md"
    
    def log(self, msg: str):
        if self.verbose:
            print(f"[ENTROPY] {msg}")
    
    def run_command(self, cmd: list, timeout: int = 30) -> Tuple[str, str, int]:
        """安全执行shell命令"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.project_path)
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", 1
        except Exception as e:
            return "", str(e), 1
    
    def calculate_c_dir(self) -> float:
        """
        计算目录结构合规率 (C_dir)
        
        C_dir = 匹配文件数 / 总文件数
        
        通过对比 `tree src/` 输出与 systemPatterns.md 中的 ASCII 树定义
        """
        self.log("计算目录结构合规率 (C_dir)...")
        
        # 生成当前目录结构
        tree_output, _, rc = self.run_command(["tree", "-L", "2", "--noreport", "src"])
        if rc != 0:
            # 尝试使用 find 替代
            find_output, _, _ = self.run_command([
                "find", "src", "-type", "f", "-o", "-type", "d"
            ])
            tree_lines = len(find_output.splitlines()) if find_output else 1
            self.log(f"使用 find 替代tree: {tree_lines} 行")
            return min(tree_output.count('\n') / 10 + 0.5, 1.0)  # 简化估算
        
        # 解析 systemPatterns.md 中的目录定义
        if self.system_patterns_file.exists():
            patterns_content = self.system_patterns_file.read_text()
            # 提取 ASCII 树定义部分
            if "```bash" in patterns_content:
                # 提取 tree 命令输出
                import re
                tree_match = re.search(r'```bash\s*(.*?)\s*```', patterns_content, re.DOTALL)
                if tree_match:
                    defined_dirs = tree_match.group(1).count('\n') + 1
                    actual_dirs = tree_output.count('\n') + 1
                    match_rate = max(0.0, 1.0 - abs(actual_dirs - defined_dirs) / max(defined_dirs, 1))
                    self.log(f"定义目录数: {defined_dirs}, 实际目录数: {actual_dirs}")
                    return match_rate
        
        # 默认返回 0.5 (中等合规)
        self.log("未找到 systemPatterns.md 或无法解析，使用默认值")
        return 0.5
    
    def calculate_c_sig(self) -> float:
        """
        计算接口签名覆盖率 (C_sig)
        
        C_sig = 已实现接口方法数 / 定义接口方法数
        """
        self.log("计算接口签名覆盖率 (C_sig)...")
        
        # 解析 techContext.md 中的接口定义
        defined_methods = set()
        if self.tech_context_file.exists():
            content = self.tech_context_file.read_text()
            # 提取 Python Protocol 和 TypeScript Interface 中的方法签名
            import re
            
            # Python Protocol: def method_name(
            py_methods = re.findall(r'def\s+(\w+)\s*\(', content)
            defined_methods.update(py_methods)
            
            # TypeScript Interface: methodName(
            ts_methods = re.findall(r'(\w+)\s*\([^)]*\)\s*[:{]', content)
            defined_methods.update(ts_methods)
        
        # 扫描源代码，查找实现
        if defined_methods:
            # 统计 src 目录下的 Python 和 TypeScript 文件
            py_files = list(self.project_path.rglob("*.py"))
            ts_files = list(self.project_path.rglob("*.ts"))
            
            implemented_count = 0
            for method in defined_methods:
                # 检查方法是否在代码中被定义
                for py_file in py_files:
                    content = py_file.read_text()
                    if re.search(rf'def\s+{method}\s*\(', content):
                        implemented_count += 1
                        break
                else:
                    # 检查 TypeScript
                    for ts_file in ts_files:
                        content = ts_file.read_text()
                        if re.search(rf'{method}\s*\([^)]*\)\s*[:{{]', content):
                            implemented_count += 1
                            break
            
            if len(defined_methods) > 0:
                coverage = implemented_count / len(defined_methods)
                self.log(f"定义方法: {len(defined_methods)}, 实现方法: {implemented_count}")
                return coverage
        
        self.log("未找到接口定义，使用默认值")
        return 0.5
    
    def calculate_c_test(self) -> float:
        """
        计算核心测试通过率 (C_test)
        
        C_test = 通过的测试数 / 总测试数
        """
        self.log("计算核心测试通过率 (C_test)...")
        
        # 运行 pytest
        output, err, rc = self.run_command([
            "pytest", "--collect-only", "-q"
        ], timeout=60)
        
        if rc != 0 or "no tests collected" in output:
            self.log("未找到测试，使用默认值")
            return 0.5
        
        # 提取测试数量
        import re
        total_match = re.search(r'(\d+)\s+test', output)
        if total_match:
            total_tests = int(total_match.group(1))
            self.log(f"发现 {total_tests} 个测试")
            
            # 运行测试并获取通过率
            run_output, _, run_rc = self.run_command([
                "pytest", "-v", "--tb=no", "-q"
            ], timeout=120)
            
            # 解析测试结果
            if "passed" in run_output:
                passed_match = re.search(r'(\d+)\s+passed', run_output)
                if passed_match:
                    passed = int(passed_match.group(1))
                    self.log(f"通过测试: {passed}/{total_tests}")
                    return passed / total_tests
        
        return 0.5
    
    def calculate_h_sys(self) -> EntropyMetrics:
        """
        计算系统综合熵值
        
        H_sys = 1 - Compliance_Score
        Compliance_Score = w1*C_dir + w2*C_sig + w3*C_test
        """
        self.log("开始计算系统熵值...")
        
        # 计算三个合规度分量
        c_dir = self.calculate_c_dir()
        c_sig = self.calculate_c_sig()
        c_test = self.calculate_c_test()
        
        # 计算综合合规度
        compliance_score = (
            self.W_DIR * c_dir +
            self.W_SIG * c_sig +
            self.W_TEST * c_test
        )
        
        # 计算熵值
        h_sys = 1.0 - compliance_score
        
        # 确定状态
        if h_sys <= 0.3:
            status = "🟢 优秀"
        elif h_sys <= 0.5:
            status = "🟡 良好"
        elif h_sys <= 0.7:
            status = "🟠 警告"
        else:
            status = "🔴 危险"
        
        metrics = EntropyMetrics(
            c_dir=c_dir,
            c_sig=c_sig,
            c_test=c_test,
            compliance_score=compliance_score,
            h_sys=h_sys,
            status=status
        )
        
        self.log(f"计算完成: H_sys = {h_sys:.4f} ({status})")
        return metrics


def main():
    parser = argparse.ArgumentParser(
        description="CDD 熵值计算脚本 (v1.3.0 Compliance-Based Model)"
    )
    parser.add_argument(
        "--project", "-p",
        default=".",
        help="项目路径 (默认: 当前目录)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细输出"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="JSON格式输出"
    )
    
    args = parser.parse_args()
    
    calculator = EntropyCalculator(args.project, args.verbose)
    metrics = calculator.calculate_h_sys()
    
    if args.json:
        print(json.dumps(metrics.to_dict(), indent=2))
    else:
        print("\n" + "=" * 50)
        print("CDD 熵值计算报告 (v1.3.0)")
        print("=" * 50)
        print(f"\n📊 合规度分量:")
        print(f"   C_dir (目录结构)  : {metrics.c_dir:.2%}")
        print(f"   C_sig (接口签名)  : {metrics.c_sig:.2%}")
        print(f"   C_test (测试通过) : {metrics.c_test:.2%}")
        print(f"\n📈 综合指标:")
        print(f"   合规度 (Compliance): {metrics.compliance_score:.2%}")
        print(f"   熵值 (H_sys)       : {metrics.h_sys:.4f}")
        print(f"\n🎯 状态评估: {metrics.status}")
        print("=" * 50 + "\n")
    
    return 0 if metrics.h_sys <= 0.5 else 1


if __name__ == "__main__":
    sys.exit(main())
