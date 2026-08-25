# Constitution-Driven Development (CDD)

CDD is a lightweight T0-T3 documentation-governance skill for Codex. It helps
projects scaffold a governance memory bank, diagnose authority and routing
gaps, and validate current-truth, execution, and archive boundaries.

CDD does not own editor configuration, runtime integration, agent execution,
session persistence, analytics, or product implementation.

## What it provides

- T0 authority and current-state templates
- T1 explanatory-context templates
- A module support-map contract
- Separate T2 standards and protocols
- A non-authoritative T3 archive boundary
- Read-only diagnosis and validation
- Impact-proportional Gate decisions

The operating rules are defined in [SKILL.md](SKILL.md). For the authority
model, Decision Ladder, and practical examples, see
[the T0-T3 practical guide](references/t0-t3-practical-guide.md).

## Requirements

- Python 3.10 or later
- PyYAML 6.x
- pytest 8.x for development tests only

Install the minimal runtime dependency:

```powershell
python -m pip install -r requirements.txt
```

## Commands

Run the scripts directly from this repository. `--project` defaults to the
current directory.

```powershell
python scripts/scaffold_t0_t3.py --project <path> [--force] [--json]
python scripts/diagnose_t0_t3.py --project <path> [--json]
python scripts/validate_t0_t3.py --project <path> [--json]
```

- `scaffold_t0_t3.py` is the only write entry. It creates missing managed
  files and overwrites them only when `--force` is supplied.
- `diagnose_t0_t3.py` is read-only and reports T0, T1, Support, T2, T3, and
  Gate 1-7 status.
- `validate_t0_t3.py` is read-only and checks structure, support closure, T2
  separation, coverage, T3 authority leakage, and UTF-8/LF rules.

Exit codes are `0` for success, `1` for governance or validation failure, and
`2` for command-line usage errors. With `--json`, stdout contains exactly one
versioned JSON object.

There is no installed Python package, global `cdd` command, or
`python -m cdd` entrypoint.

## Install as a Codex skill

Clone the repository into the Codex skills directory:

```powershell
git clone https://github.com/wsman/Constitution-Driven-Development-Skill.git `
  "$HOME/.codex/skills/cdd"
```

The skill remains automatically discoverable through its `SKILL.md`
frontmatter.

## Development

```powershell
python -m pip install -r requirements-test.txt
$env:PYTHONUTF8 = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
python -m pytest -q tests
```

The regression suite covers the public CLI, scaffolding idempotence, malformed
governance input, support closure, T3 authority leakage, and the
impact-proportional blocking scenarios.

## Repository layout

```text
.
|-- SKILL.md
|-- README.md
|-- scripts/
|-- references/
|-- assets/templates/
`-- tests/
```
