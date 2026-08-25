---
name: cdd-governance
description: "Lightweight T0-T3 documentation governance: scaffold a memory bank, diagnose authority and support gaps, and validate current-truth, execution, and archive boundaries."
allowed-tools: Read, Glob, Grep, Bash, Write, AskUserQuestion
---

# CDD Governance

Use this skill to build, inspect, or repair a project's T0-T3 documentation
system. It owns documentation governance only. Tool configuration, execution
integration, persistence, and analytics belong to their dedicated owners.

## Operating contract

1. Establish the project root and read its local instructions.
2. Inspect current T0, T1, support-map, T2, and T3 surfaces before proposing a
   change.
3. Apply the Decision Ladder in `references/t0-t3-practical-guide.md`.
4. Report the weakest layer, the action it actually blocks, and the smallest
   corrective step.
5. Keep diagnosis and validation read-only. Write only when the user explicitly
   asks for scaffolding or approves a concrete governance edit.
6. After a write, run `validate_t0_t3.py` and state the next hand-off.

The verdict vocabulary is `PASS`, `CONCERNS`, or `FAIL`. A `FAIL` blocks only
the action that consumes the failed result or shares its side effects.

## Supported commands

Run the scripts directly; there is no package installation and no `cdd` CLI.

```powershell
python scripts/scaffold_t0_t3.py --project <path> [--force] [--json]
python scripts/diagnose_t0_t3.py --project <path> [--json]
python scripts/validate_t0_t3.py --project <path> [--json]
```

- `scaffold_t0_t3.py` is the only write entry. It creates missing managed
  templates and overwrites them only with `--force`.
- `diagnose_t0_t3.py` is read-only and reports T0, T1, Support, T2, T3, and
  Gate 1-7 health with impact-scoped blockers.
- `validate_t0_t3.py` is read-only and checks structure, support closure, T2
  separation, coverage, T3 authority leakage, and UTF-8 text rules.
- Exit codes are `0` for success, `1` for governance/validation failure, and
  `2` for CLI usage errors.
- With `--json`, stdout contains exactly one versioned JSON object. Human
  diagnostics go to stderr.

## Operational simplicity guard

For a governed local operation, prefer one reviewed entrypoint, one
transaction, zero or one necessary child, one authoritative verdict, and one
automatically populated evidence location. Every launcher, manifest, hash pin,
approval boundary, evidence copy, or process hop needs a concrete threat or
failure that it closes and a realistic test proving the benefit.

Test the released checkout shape and the actual invocation. An internal helper
test alone does not prove an operator workflow. Treat a failure before the first
material side effect as a preparation rejection; correct or simplify the same
entrypoint instead of layering on new identities, transports, reviewers, or
approvals.

## Impact-proportional blocking guard

A Gate may block only an action that consumes its result, shares its side
effects, or depends on its safety conclusion.

- Local residue, missing unreferenced T3 attachments, archive hygiene, and
  evidence-directory readability do not block independent development or
  merge work.
- T3 becomes blocking only when archive content leaks into a current-truth
  surface.
- If an operation depends on code in a pull request, prefer merging reviewed
  code and running from stable `main` instead of binding live work to a moving
  PR head.
- A destructive-action safety check blocks that action, not unrelated work.
- Unchanged languages, platforms, and review roles are `NOT_IMPACTED`; do not
  require ceremonial validation without a dependency path.

Regression scenarios:

1. Incomplete local cleanup plus an independent governance-code PR recommends
   merge-first; cleanup remains a separate operational lane.
2. A missing T3 attachment that current truth does not reference is recorded as
   archive hygiene and does not block development.
3. A failed check that directly controls a destructive command blocks that
   command while unrelated work remains available.

## Output and hand-off

For advisory work, return:

1. layer and Gate status;
2. evidence-backed findings with concrete paths;
3. impact-scoped blockers;
4. the smallest recommended next step;
5. explicit surfaces that must not change yet.

Hand off configuration, implementation, release, and product architecture work
to their dedicated project skills after the governance prerequisite they
actually depend on is healthy.
