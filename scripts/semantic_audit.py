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

def load_three_tier_laws() -> dict:
    """Load the three-tier legal system from the constitution files"""
    laws = {
        "basic_law": "",
        "technical_law": "", 
        "procedural_law": ""
    }
    
    # 1. Basic Law (Constitutional Core)
    basic_law_paths = [
        PROJECT_ROOT / "memory_bank/core/basic_law_index.md",
        PROJECT_ROOT / "templates/01_core/basic_law_index.md"
    ]
    
    for path in basic_law_paths:
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8")
                laws["basic_law"] = f"\n--- BASIC LAW: {path.name} ---\n{content}\n"
                break
            except Exception:
                continue
    
    # 2. Technical Law (Technical Standards)
    tech_law_paths = [
        PROJECT_ROOT / "memory_bank/core/technical_law_index.md",
        PROJECT_ROOT / "templates/01_core/technical_law_index.md"
    ]
    
    for path in tech_law_paths:
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8")
                laws["technical_law"] = f"\n--- TECHNICAL LAW: {path.name} ---\n{content}\n"
                break
            except Exception:
                continue
    
    # 3. Procedural Law (Workflow Protocols)
    proc_law_paths = [
        PROJECT_ROOT / "memory_bank/core/procedural_law_index.md",
        PROJECT_ROOT / "templates/01_core/procedural_law_index.md"
    ]
    
    for path in proc_law_paths:
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8")
                laws["procedural_law"] = f"\n--- PROCEDURAL LAW: {path.name} ---\n{content}\n"
                break
            except Exception:
                continue
    
    return laws

def load_text(path: Path) -> str:
    if not path.exists(): return ""
    try:
        return f"\n--- DOCUMENT: {path.name} ---\n{path.read_text(encoding='utf-8')}\n"
    except Exception:
        return "" # Skip binary files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="src", help="Code directory to audit")
    parser.add_argument("--spec", help="Specific spec file to validate against")
    args = parser.parse_args()
    
    bridge = LLMBridge(PROJECT_ROOT)
    
    # 1. Load the Three-Tier Legal System
    print("⚖️  Loading Three-Tier Legal System...")
    laws = load_three_tier_laws()
    
    if not laws["basic_law"]:
        print("⛔ FATAL: Basic Law (Constitution) not found. Cannot proceed with judicial review.")
        sys.exit(1)
    
    print(f"   - Basic Law Length: {len(laws['basic_law'])} chars")
    print(f"   - Technical Law Length: {len(laws['technical_law'])} chars") 
    print(f"   - Procedural Law Length: {len(laws['procedural_law'])} chars")

    # 2. Load the "Contract" (Spec)
    spec_text = ""
    if args.spec:
        spec_text = load_text(Path(args.spec))
    else:
        # Smart Context: Find the most recently active spec
        specs_dir = PROJECT_ROOT / "templates/04_standards" # Default to standards for demo
        # Check actual specs dir if exists
        real_specs = PROJECT_ROOT / "specs"
        if real_specs.exists(): specs_dir = real_specs
        
        candidates = sorted(specs_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
        if candidates:
            # Skip templates/indexes usually
            target_spec = next((f for f in candidates if "template" not in f.name), candidates[0])
            print(f"📜 Auto-selected Contract: {target_spec.name}")
            spec_text = load_text(target_spec)

    # 3. Load the "Evidence" (Code)
    code_text = ""
    target_path = PROJECT_ROOT / args.target
    
    # Check if target exists
    if not target_path.exists():
        # Check for alternative source directories
        alt_paths = [PROJECT_ROOT / "scripts", PROJECT_ROOT]
        for alt_path in alt_paths:
            if alt_path.exists():
                target_path = alt_path
                print(f"⚠️  Target '{args.target}' not found, using alternative: {alt_path}")
                break
    
    if target_path.exists():
        # Limit evidence size for context window efficiency
        extensions = {".py", ".ts", ".js", ".go", ".java"}
        # If it's a file, just load it
        if target_path.is_file():
            code_text = load_text(target_path)
        else:
            # It's a directory, sample files
            files = []
            for ext in extensions:
                files.extend(target_path.rglob(f"*{ext}"))
            # Filter out test files
            files = [f for f in files[:10] if "test" not in f.name and "__pycache__" not in str(f)]
            for f in files:
                code_text += load_text(f)
    
    if not code_text:
        print("⚠️  No evidence (code) found. Case dismissed.")
        sys.exit(0)

    # 4. Court Session
    print(f"\n⚖️  Supreme Court in session. Docket: {target_path.relative_to(PROJECT_ROOT)}")
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
    
    result = bridge.call_judge(prompt, "Please render your verdict based on the three-tier legal system.")

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