# T0-T3 Practical Guide

This guide defines the lightweight documentation-governance model used by the
CDD skill. It is intentionally independent of editor, runtime, storage, and
delivery tooling.

## Authority layers

| Layer | Purpose | May do | Must not do |
|---|---|---|---|
| T0 | Law and current state | Define intent, constraints, status, and approved baselines | Delegate authority silently |
| T1 | Supporting context | Explain patterns, behavior, and technology context | Override T0 |
| Support | Coverage contract | Map each module to T0, T1, active T2, and its T3 archive root | Become product authority |
| T2 | Standards and protocols | Define reusable rules and executable coordination | Promote status or rewrite T0/T1 |
| T3 | Historical evidence | Preserve reviews, reports, captures, and superseded material | Govern current behavior |

Resolve conflicts in that order. A catalog, index, or archive location is a
routing aid, not semantic authority.

## Minimal project shape

```text
memory_bank/
├── README.md
├── module_support_map.yaml
├── t0_core/
├── t1_axioms/
├── t2_standards/       # DS-*.md
├── t2_protocols/       # WF-*.md
└── t3_archives/        # module-owned historical evidence
```

Standards state reusable constraints. Protocols state an executable sequence,
inputs, outputs, stop conditions, and evidence destination. Do not combine
these responsibilities merely to reduce file count.

## Support contract

Each module must have:

- three T0 anchors: landscape, status, and baseline;
- three T1 anchors: system patterns, behavior context, and technology context;
- at least one active T2 standard or protocol;
- combined T2 coverage for `constraint`, `t1-support`, `execution`,
  `validation`, and `evidence`;
- one module-owned T3 archive root.

Every root-level active T2 document must be routed by at least one module.
Unrouted T2 is a stale execution route, not harmless documentation clutter.

## Decision Ladder and Gates

Evaluate from authority to archive:

1. **Gate 1 — T0 authority:** required laws and current-state anchors exist.
2. **Gate 2 — T1 context:** the three supporting context surfaces exist.
3. **Gate 3 — Support:** the module map is parseable and closed.
4. **Gate 4 — T2 closure:** active standards and protocols are separated,
   routed, and cover the required facets.
5. **Gate 5 — Execution:** the operation has one supported protocol and an
   evidence destination.
6. **Gate 6 — Dependent delivery:** enter only when the preceding Gate whose
   result the delivery consumes is healthy.
7. **Gate 7 — Archive hygiene:** archive issues are concerns unless T3 content
   has leaked into current truth.

Report the first weak layer, but scope the block by dependency rather than by
layer proximity.

## Operational simplicity

For a local governed operation, the default complexity budget is:

- one reviewed operator entrypoint;
- one transaction;
- zero or one necessary child process;
- one authoritative verdict;
- one automatically populated evidence location.

Add a layer only when it closes a named threat or failure and can be exercised
through the released invocation. Failures before a material side effect are
preparation rejections. Correct the same path instead of multiplying IDs,
manifests, transports, approval steps, or evidence copies.

Identity checks should cover properties that can alter execution semantics.
Branch attachment, equivalent access-entry order, or JSON field order are not
blocking merely because their representation differs.

## Impact-proportional blocking

A check blocks only work that consumes its result, shares its side effects, or
depends on its safety claim.

- Local residue and archive hygiene do not block unrelated development.
- Missing T3 evidence is nonblocking when current truth does not cite it.
- A failed destructive-action safety check blocks that operation only.
- When live work depends on reviewed code, prefer merging the code and running
  the operation from stable `main`.
- Diff-unrelated roles and platforms are `NOT_IMPACTED`.

Behavioral regression scenarios:

1. **Merge-first:** cleanup is incomplete, but a governance-code change does
   not consume the residue. Merge after the code's own Gates; keep cleanup in a
   separate operations lane.
2. **Archive-only:** an attachment is missing and no current-truth document
   references it. Record archive hygiene without blocking development.
3. **Direct safety dependency:** a check decides whether a destructive command
   is safe. Its failure blocks that command and no unrelated action.

## Diagnosis output

A useful diagnosis names:

1. layer and Gate status;
2. concrete file or support-map evidence;
3. actions directly blocked by each issue;
4. the smallest next repair;
5. surfaces that must remain unchanged.

Use `PASS`, `CONCERNS`, and `FAIL`. Avoid ceremonial review, duplicated evidence,
and broad stop conditions without a dependency path.
