#!/usr/bin/env python3
"""
CDD Gate 4: Semantic Auditor (LLM-as-a-Judge)
=============================================
Usage: python scripts/semantic_audit.py [--target src/] [--spec specs/DS-050.md]
"""

import sys
import argparse
from pathlib import Path

# Ensure we can import utils
sys.path.append(str(Path(__file__).parent.parent))
from scripts.utils.llm_bridge import LLMBridge
from scripts.utils.tool_bridge import ToolBridge

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 司法系统提示词 (The Judicial Constitution) - 更新为三级法律体系
JUDGE_PROMPT = """
You are the Supreme Court Justice of a Constitution-Driven Development (CDD) system.
Your VERDICT must be based strictly on the alignment between the LAWS (three-tier legal system), the CONTRACT (Spec), and the EVIDENCE (Code).

### 🏛️ The Legal System (Three-Tier Constitutional Law)
CDD follows a **three-tier legal system** with constitutional hierarchy:

#### 1. Basic Law (Constitutional Core) §1-§299
**Nature**: Core axioms, fundamental principles, highest authority
**Examples**: §102.3 (Constitutional Synchronization), §152 (Single Source of Truth), §300.1 (Spore Protocol)
**Force**: Supreme - all other laws must comply with Basic Law

#### 2. Technical Law §300-§499
**Nature**: Mathematical axioms, technical standards, implementation specifications
**Examples**: §300.1 (Core Mathematical Axioms), §301-§309 (Input/Output), §438 (Tool Invocation)
**Force**: Medium - defines technical implementation within Basic Law framework

#### 3. Procedural Law §500-§599
**Nature**: Workflow protocols, operational procedures, collaboration standards
**Examples**: §500-§599 (Workflow Protocols), WF-xxx (Workflow Implementation)
**Force**: Specific - defines development process steps and collaboration

#### ⚖️ Legal Conflict Resolution Principles
1. **Constitutional Supremacy**: Basic Law prevails over Technical and Procedural Law
2. **Lex posterior derogat priori**: Within same tier, later law prevails
3. **Lex specialis derogat generali**: Specific provisions prevail over general ones
4. **Legal Reservation**: Only Basic Law may restrict fundamental rights

### Basic Law (Constitutional Core)
{basic_law}

### Technical Law (Technical Standards)
{technical_law}

### Procedural Law (Workflow Protocols)
{procedural_law}

### 📄 The Contract (Feature Specification)
{specification}

### 🕵️ The Evidence (Implementation Code)
{code}

### ⚖️ Judicial Task
Analyze the Evidence for **SEMANTIC COMPLIANCE** with the THREE-TIER LEGAL SYSTEM.
Do not focus on syntax (linters do that). Focus on INTENT, LOGIC, SAFETY, and LEGAL HIERARCHY.

Violations to look for:
1. **Constitutional Breach**: Does the code violate Basic Law principles (e.g., Single Source of Truth, Spore Protocol)?
2. **Technical Law Violation**: Does the code violate Technical Law standards (e.g., mathematical axioms, technical specifications)?
3. **Procedural Non-compliance**: Does the code violate Procedural Law workflows?
4. **Contract Breach**: Does the code fail to implement a requirement in the Spec?
5. **Ghost Features**: Does the code implement features NOT in the Spec? (Entropy increase!)

**Special Attention**: §300.1 exists in BOTH Basic Law (Spore Protocol) and Technical Law (Core Mathematical Axioms). This is a LEGAL LAYERING example.

### 📝 Verdict Format (JSON Only)
Output strictly valid JSON:
{{
  "verdict": "PASS" | "FAIL",
  "score": <0-100>,
  "summary": "<Executive summary of the ruling>",
  "violations": [
    {{
      "severity": "CRITICAL" | "MAJOR" | "MINOR",
      "law_tier": "BASIC" | "TECHNICAL" | "PROCEDURAL" | "CONTRACT",
      "location": "<filename:line>",
      "reference": "<Law §X or Spec Requirement Y>",
      "reasoning": "<Legal reasoning for the violation>"
    }}
  ]
}}
"""

def load_three_tier_laws(io_bridge: ToolBridge) -> dict:
    """Load the three-tier legal system from the constitution files using ToolBridge"""
    laws = {
        "basic_law": "",
        "technical_law": "", 
        "procedural_law": ""
    }
    
    # 定义加载优先级 (解决单一真理源歧义问题)
    # 优先 memory_bank (Live Truth), 备选 templates (Static Truth)
    
    def try_load(relative_paths):
        for p in relative_paths:
            if io_bridge.file_exists(p):
                content = io_bridge.read_file(p)
                if content:
                    return f"\n--- LAW FILE: {p} ---\n{content}\n"
        return ""
    
    laws["basic_law"] = try_load([
        "memory_bank/core/basic_law_index.md",
        "templates/01_core/basic_law_index.md"
    ])
    
    laws["technical_law"] = try_load([
        "memory_bank/core/technical_law_index.md",
        "templates/01_core/technical_law_index.md"
    ])
    
    laws["procedural_law"] = try_load([
        "memory_bank/core/procedural_law_index.md",
        "templates/01_core/procedural_law_index.md"
    ])
    
    return laws

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="src", help="Code directory to audit")
    parser.add_argument("--spec", help="Specific spec file to validate against")
    args = parser.parse_args()
    
    # 初始化双桥 (Two Bridges)
    llm_bridge = LLMBridge(PROJECT_ROOT)
    io_bridge = ToolBridge(PROJECT_ROOT)  # 新增 IO 桥接器
    
    # 1. Load the Three-Tier Legal System (Using Bridge)
    print("⚖️  Loading Three-Tier Legal System...")
    laws = load_three_tier_laws(io_bridge)
    
    if not laws["basic_law"]:
        print("⛔ FATAL: Basic Law (Constitution) not found. Cannot proceed with judicial review.")
        sys.exit(1)
    
    print(f"   - Basic Law Length: {len(laws['basic_law'])} chars")
    print(f"   - Technical Law Length: {len(laws['technical_law'])} chars") 
    print(f"   - Procedural Law Length: {len(laws['procedural_law'])} chars")

    # 2. Load the "Contract" (Spec)
    spec_text = ""
    if args.spec:
        spec_text = io_bridge.read_file(args.spec)
        if spec_text:
            spec_text = f"\n--- SPECIFICATION: {args.spec} ---\n{spec_text}\n"
    else:
        # Smart Context: Find the most recently active spec
        specs_dir = "templates/04_standards"  # Default to standards for demo
        # Check actual specs dir if exists
        real_specs = "specs"
        if io_bridge.file_exists(real_specs):
            specs_dir = real_specs
        
        candidates = io_bridge.list_files(specs_dir, extension=".md")
        if candidates:
            # Filter out templates and select the most relevant
            filtered = [f for f in candidates if "template" not in f.lower()]
            if filtered:
                target_spec = filtered[0]  # 简化: 选择第一个非模板文件
                print(f"📜 Auto-selected Contract: {target_spec}")
                content = io_bridge.read_file(target_spec)
                if content:
                    spec_text = f"\n--- SPECIFICATION: {target_spec} ---\n{content}\n"

    # 3. Load the "Evidence" (Code)
    code_text = ""
    target_path = args.target
    
    # Check if target exists
    if not io_bridge.file_exists(target_path) and not io_bridge.file_exists(target_path + "/"):  # 检查目录
        # Check for alternative source directories
        alt_paths = ["scripts", "."]
        for alt_path in alt_paths:
            if io_bridge.file_exists(alt_path) or io_bridge.file_exists(alt_path + "/"):
                target_path = alt_path
                print(f"⚠️  Target '{args.target}' not found, using alternative: {alt_path}")
                break
    
    # 收集证据文件
    evidence_files = []
    
    # 如果是文件
    if io_bridge.file_exists(target_path):
        evidence_files = [target_path]
    else:
        # 如果是目录，采样文件
        extensions = [".py", ".ts", ".js", ".go", ".java"]
        for ext in extensions:
            files = io_bridge.list_files(target_path, recursive=True, extension=ext)
            evidence_files.extend(files)
        
        # 过滤测试文件，限制数量
        evidence_files = [
            f for f in evidence_files[:20]  # 限制数量
            if "test" not in f.lower() and "__pycache__" not in f
        ]
    
    for file_path in evidence_files:
        content = io_bridge.read_file(file_path)
        if content:
            code_text += f"\n--- CODE FILE: {file_path} ---\n{content}\n"
    
    if not code_text:
        print("⚠️  No evidence (code) found. Case dismissed.")
        sys.exit(0)

    # 4. Court Session
    print(f"\n⚖️  Supreme Court in session. Docket: {target_path}")
    print(f"   - Total Law Length: {len(laws['basic_law']) + len(laws['technical_law']) + len(laws['procedural_law'])} chars")
    print(f"   - Contract Length: {len(spec_text)} chars")
    print(f"   - Evidence Length: {len(code_text)} chars")
    print("   - Deliberating with Three-Tier Legal System...")

    prompt = JUDGE_PROMPT.format(
        basic_law=laws["basic_law"],
        technical_law=laws["technical_law"],
        procedural_law=laws["procedural_law"],
        specification=spec_text,
        code=code_text
    )
    
    result = llm_bridge.call_judge(prompt, "Please render your verdict based on the three-tier legal system.")

    # 5. Pronounce Judgment
    verdict = result.get("verdict")
    
    if verdict == "PASS":
        print(f"\n✅ VERDICT: PASS (Score: {result.get('score', 100)})")
        print(f"   {result.get('summary')}")
        sys.exit(0)
    elif verdict == "FAIL":
        print(f"\n⛔ VERDICT: FAIL (Score: {result.get('score', 0)})")
        print(f"   {result.get('summary')}")
        print("\n   Violations by Legal Tier:")
        for v in result.get("violations", []):
            law_tier = v.get("law_tier", "UNKNOWN")
            print(f"   - [{law_tier}] [{v.get('severity')}] {v.get('reference')}: {v.get('reasoning')}")
        sys.exit(1)
    elif verdict == "SKIPPED":
        print(f"\n⏭️  VERDICT: SKIPPED")
        print(f"   {result.get('summary', 'Semantic audit is disabled in config.')}")
        sys.exit(0)  # Skipped is not a failure
    elif verdict == "ERROR":
        print(f"\n⚠️  VERDICT: ERROR")
        print(f"   {result.get('error', 'Unknown error occurred during semantic audit.')}")
        sys.exit(1)  # Error is a failure
    else:
        print(f"\n⚠️  VERDICT: UNKNOWN")
        print(f"   {result.get('summary', 'Unexpected verdict format.')}")
        sys.exit(1)

if __name__ == "__main__":
    main()