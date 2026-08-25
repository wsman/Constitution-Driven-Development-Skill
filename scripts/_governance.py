"""Shared T0-T3 governance primitives for the standalone CDD scripts."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml


T0_FILES = (
    "active_context.md",
    "basic_law_index.md",
    "knowledge_graph.md",
    "operational_law_index.md",
    "tools_law_index.md",
)
T1_FILES = ("behavior_context.md", "system_patterns.md", "tech_context.md")
T1_ANCHORS = (
    "memory_bank/t1_axioms/system_patterns.md",
    "memory_bank/t1_axioms/behavior_context.md",
    "memory_bank/t1_axioms/tech_context.md",
)
REQUIRED_COVERAGE = {"constraint", "t1-support", "execution", "validation", "evidence"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json"}
AUTHORITY_LEAK_RE = re.compile(
    r"\b(?:t3|archive(?:d|s)?)\b.{0,80}\b(?:is|are|as|becomes?)\b.{0,40}"
    r"\b(?:authoritative|authority|current[- ]truth|source of truth|governing)\b",
    re.IGNORECASE,
)
NEGATION_RE = re.compile(r"\b(?:not|never|non-authoritative|cannot|must not)\b", re.IGNORECASE)


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    path: str | None = None
    blocks: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.path is not None:
            result["path"] = self.path
        result["blocks"] = list(self.blocks)
        return result


@dataclass
class Validation:
    project: Path
    errors: list[Issue] = field(default_factory=list)
    warnings: list[Issue] = field(default_factory=list)
    checks: list[dict[str, str]] = field(default_factory=list)
    support_map: dict[str, Any] | None = None
    routed_t2: set[str] = field(default_factory=set)

    @property
    def ok(self) -> bool:
        return not self.errors

    def add_check(self, name: str, status: str, detail: str) -> None:
        self.checks.append({"name": name, "status": status, "detail": detail})


def resolve_project(value: str | Path | None) -> Path:
    candidate = Path.cwd() if value is None else Path(value)
    return candidate.expanduser().resolve()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def read_utf8(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is not allowed")
    if b"\x00" in data:
        raise ValueError("NUL is not allowed")
    if b"\r" in data:
        raise ValueError("CR/CRLF is not allowed; use LF")
    return data.decode("utf-8", errors="strict")


def _relative(path: Path, project: Path) -> str:
    return path.relative_to(project).as_posix()


def _add_missing(
    result: Validation, path: Path, code: str, message: str, blocks: tuple[str, ...]
) -> bool:
    if path.exists():
        return False
    result.errors.append(Issue(code, message, _relative(path, result.project), blocks))
    return True


def _load_support_map(result: Validation, path: Path) -> dict[str, Any] | None:
    try:
        text = read_utf8(path)
        loaded = yaml.safe_load(text)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        result.errors.append(
            Issue("SUPPORT_PARSE", f"support map cannot be parsed: {exc}", _relative(path, result.project), ("governance",))
        )
        return None
    if not isinstance(loaded, dict):
        result.errors.append(
            Issue("SUPPORT_SHAPE", "support map must be a YAML mapping", _relative(path, result.project), ("governance",))
        )
        return None
    return loaded


def _validate_text_files(result: Validation, memory_bank: Path) -> None:
    if not memory_bank.is_dir():
        return
    failures = 0
    for path in sorted(memory_bank.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            read_utf8(path)
        except (OSError, UnicodeError, ValueError) as exc:
            failures += 1
            result.errors.append(
                Issue("TEXT_ENCODING", str(exc), _relative(path, result.project), ("governance",))
            )
    result.add_check(
        "utf8_text",
        "PASS" if failures == 0 else "FAIL",
        f"{failures} governed text file(s) violate strict UTF-8/LF rules",
    )


def _validate_t2_layout(result: Validation, memory_bank: Path) -> tuple[set[str], set[str]]:
    standards = memory_bank / "t2_standards"
    protocols = memory_bank / "t2_protocols"
    standard_paths: set[str] = set()
    protocol_paths: set[str] = set()
    failures = 0
    for root, prefix, destination in (
        (standards, "DS-", standard_paths),
        (protocols, "WF-", protocol_paths),
    ):
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            rel = _relative(path, result.project)
            destination.add(rel)
            if path.parent != root or not path.name.startswith(prefix):
                failures += 1
                result.errors.append(
                    Issue(
                        "T2_LAYOUT",
                        f"T2 file must be a root-level {prefix}*.md document",
                        rel,
                        ("governance", "dependent-delivery"),
                    )
                )
    result.add_check(
        "t2_standard_protocol_split",
        "PASS" if failures == 0 else "FAIL",
        f"{len(standard_paths)} standard(s), {len(protocol_paths)} protocol(s)",
    )
    return standard_paths, protocol_paths


def _validate_support_map(
    result: Validation,
    support: dict[str, Any],
    standard_paths: set[str],
    protocol_paths: set[str],
) -> None:
    path = result.project / "memory_bank" / "module_support_map.yaml"
    rel_path = _relative(path, result.project)
    if support.get("schemaVersion") != "3.0":
        result.errors.append(Issue("SUPPORT_VERSION", "schemaVersion must be '3.0'", rel_path, ("governance",)))
    if not isinstance(support.get("coreThesis"), str) or not support["coreThesis"].strip():
        result.errors.append(Issue("SUPPORT_THESIS", "coreThesis must be a non-empty string", rel_path, ("governance",)))
    order = support.get("moduleOrder")
    modules = support.get("modules")
    if not isinstance(order, list) or not all(isinstance(item, str) and item for item in order):
        result.errors.append(Issue("SUPPORT_ORDER", "moduleOrder must be a non-empty string list", rel_path, ("governance",)))
        return
    if not isinstance(modules, dict) or not modules:
        result.errors.append(Issue("SUPPORT_MODULES", "modules must be a non-empty mapping", rel_path, ("governance",)))
        return
    if order != list(modules):
        result.errors.append(
            Issue("SUPPORT_ORDER", "moduleOrder must exactly match modules key order", rel_path, ("governance",))
        )

    all_t2 = standard_paths | protocol_paths
    for module_name, module in modules.items():
        module_path = f"{rel_path}#modules.{module_name}"
        if not isinstance(module, dict):
            result.errors.append(Issue("SUPPORT_MODULE", "module entry must be a mapping", module_path, ("governance",)))
            continue
        t0 = module.get("t0Refs")
        t1 = module.get("t1Refs")
        refs = module.get("t2Refs")
        archive_root = module.get("archiveRoot")
        if not isinstance(t0, dict) or set(t0) != {"landscape", "status", "baseline"}:
            result.errors.append(Issue("SUPPORT_T0", "t0Refs must contain landscape/status/baseline", module_path, ("governance",)))
        if not isinstance(t1, dict) or set(t1) != {"systemPatterns", "behaviorContext", "techContext"}:
            result.errors.append(Issue("SUPPORT_T1", "t1Refs must contain the three T1 anchors", module_path, ("governance",)))
        if not isinstance(archive_root, str) or not archive_root.startswith("memory_bank/t3_archives/") or not archive_root.endswith("/"):
            result.errors.append(Issue("SUPPORT_ARCHIVE", "archiveRoot must be a module directory under T3", module_path, ("archive",)))
        if not isinstance(refs, list) or not refs:
            result.errors.append(Issue("SUPPORT_T2", "t2Refs must be a non-empty list", module_path, ("governance", "dependent-delivery")))
            continue
        coverage: set[str] = set()
        support_anchors: set[str] = set()
        for index, ref in enumerate(refs):
            ref_path = f"{module_path}.t2Refs[{index}]"
            if not isinstance(ref, dict):
                result.errors.append(Issue("SUPPORT_T2", "T2 reference must be a mapping", ref_path, ("governance",)))
                continue
            document = ref.get("path")
            kind = ref.get("kind")
            facets = ref.get("coverage")
            if not isinstance(document, str) or document not in all_t2:
                result.errors.append(Issue("SUPPORT_T2_PATH", "T2 path is missing or not an active root T2 document", ref_path, ("governance", "dependent-delivery")))
            else:
                result.routed_t2.add(document)
                expected_kind = "standard" if document in standard_paths else "protocol"
                if kind != expected_kind:
                    result.errors.append(Issue("SUPPORT_T2_KIND", f"kind must be {expected_kind}", ref_path, ("governance",)))
            if not isinstance(facets, list) or not all(isinstance(item, str) for item in facets):
                result.errors.append(Issue("SUPPORT_COVERAGE", "coverage must be a string list", ref_path, ("governance",)))
            else:
                coverage.update(facets)
            if isinstance(facets, list) and "t1-support" in facets:
                anchors = ref.get("t1Anchors")
                if isinstance(anchors, list):
                    support_anchors.update(item for item in anchors if isinstance(item, str))
        missing = sorted(REQUIRED_COVERAGE - coverage)
        if missing:
            result.errors.append(Issue("SUPPORT_COVERAGE", f"missing coverage facets: {', '.join(missing)}", module_path, ("governance", "dependent-delivery")))
        missing_anchors = sorted(set(T1_ANCHORS) - support_anchors)
        if missing_anchors:
            result.errors.append(Issue("SUPPORT_T1_ANCHORS", f"t1-support must anchor all T1 files: {', '.join(missing_anchors)}", module_path, ("governance",)))

    unrouted = sorted(all_t2 - result.routed_t2)
    for document in unrouted:
        result.errors.append(Issue("T2_STALE_ROUTE", "active T2 document is not routed by the support map", document, ("governance", "dependent-delivery")))


def _validate_t3_authority(result: Validation, memory_bank: Path) -> None:
    roots = [
        memory_bank / "t0_core",
        memory_bank / "t1_axioms",
        memory_bank / "t2_standards",
        memory_bank / "t2_protocols",
    ]
    leaks = 0
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            try:
                text = read_utf8(path)
            except (OSError, UnicodeError, ValueError):
                continue
            for line_number, line in enumerate(text.splitlines(), 1):
                if AUTHORITY_LEAK_RE.search(line) and not NEGATION_RE.search(line):
                    leaks += 1
                    result.errors.append(
                        Issue(
                            "T3_AUTHORITY_LEAK",
                            f"current truth promotes T3/archive content to authority at line {line_number}",
                            _relative(path, result.project),
                            ("current-truth-consumers",),
                        )
                    )
    result.add_check("t3_authority_leakage", "PASS" if leaks == 0 else "FAIL", f"{leaks} authority leak(s)")


def validate_project(project: Path) -> Validation:
    project = project.resolve()
    result = Validation(project)
    memory_bank = project / "memory_bank"
    if not project.is_dir():
        result.errors.append(Issue("PROJECT_MISSING", "project directory does not exist", str(project), ("all",)))
        return result
    if _add_missing(result, memory_bank, "MEMORY_BANK_MISSING", "memory_bank directory is missing", ("governance",)):
        return result

    required_dirs = (
        memory_bank / "t0_core",
        memory_bank / "t1_axioms",
        memory_bank / "t2_standards",
        memory_bank / "t2_protocols",
        memory_bank / "t3_archives",
    )
    for directory in required_dirs:
        _add_missing(result, directory, "STRUCTURE_MISSING", "required governance directory is missing", ("governance",))
    for name in T0_FILES:
        _add_missing(result, memory_bank / "t0_core" / name, "T0_MISSING", "required T0 document is missing", ("governance", "dependent-delivery"))
    for name in T1_FILES:
        _add_missing(result, memory_bank / "t1_axioms" / name, "T1_MISSING", "required T1 document is missing", ("governance", "dependent-delivery"))

    _validate_text_files(result, memory_bank)
    standards, protocols = _validate_t2_layout(result, memory_bank)
    support_path = memory_bank / "module_support_map.yaml"
    if not _add_missing(result, support_path, "SUPPORT_MISSING", "module support map is missing", ("governance",)):
        support = _load_support_map(result, support_path)
        result.support_map = support
        if support is not None:
            _validate_support_map(result, support, standards, protocols)
    _validate_t3_authority(result, memory_bank)
    result.add_check("validation", "PASS" if result.ok else "FAIL", f"{len(result.errors)} error(s), {len(result.warnings)} warning(s)")
    return result


def _has_code(validation: Validation, prefixes: Iterable[str]) -> bool:
    wanted = tuple(prefixes)
    return any(issue.code.startswith(wanted) for issue in validation.errors)


def diagnose_project(project: Path) -> dict[str, Any]:
    validation = validate_project(project)
    t0_fail = _has_code(validation, ("PROJECT_", "MEMORY_", "STRUCTURE_", "T0_", "TEXT_"))
    t1_fail = _has_code(validation, ("T1_",))
    support_fail = _has_code(validation, ("SUPPORT_",))
    t2_fail = _has_code(validation, ("T2_",)) or support_fail
    t3_leak = _has_code(validation, ("T3_AUTHORITY_LEAK",))
    t3_root_missing = any(
        issue.code == "STRUCTURE_MISSING" and issue.path and issue.path.endswith("t3_archives")
        for issue in validation.errors
    )

    layers = [
        {"layer": "T0", "status": "FAIL" if t0_fail else "HEALTHY"},
        {"layer": "T1", "status": "FAIL" if t1_fail else "HEALTHY"},
        {"layer": "Support", "status": "FAIL" if support_fail else "HEALTHY"},
        {"layer": "T2", "status": "STALE_ROUTE" if t2_fail else "HEALTHY"},
        {"layer": "T3", "status": "AUTHORITY_LEAK" if t3_leak else ("ARCHIVE_HYGIENE" if t3_root_missing else "HEALTHY")},
    ]
    prerequisite_fail = t0_fail or t1_fail or support_fail or t2_fail
    gates = [
        {"gate": 1, "name": "T0 authority", "status": "FAIL" if t0_fail else "PASS"},
        {"gate": 2, "name": "T1 context", "status": "FAIL" if t1_fail else "PASS"},
        {"gate": 3, "name": "support contract", "status": "FAIL" if support_fail else "PASS"},
        {"gate": 4, "name": "T2 closure", "status": "FAIL" if t2_fail else "PASS"},
        {"gate": 5, "name": "execution route", "status": "FAIL" if t2_fail else "PASS"},
        {"gate": 6, "name": "dependent delivery", "status": "BLOCKED" if prerequisite_fail else "READY"},
        {"gate": 7, "name": "archive hygiene", "status": "FAIL" if t3_leak else ("CONCERNS" if t3_root_missing else "PASS")},
    ]
    if t0_fail:
        weakest = "T0"
    elif t1_fail:
        weakest = "T1"
    elif support_fail:
        weakest = "Support"
    elif t2_fail:
        weakest = "T2"
    elif t3_leak or t3_root_missing:
        weakest = "T3"
    else:
        weakest = "none"
    return {
        "schema": "cdd.t0-t3.diagnosis.v1",
        "project": str(validation.project),
        "verdict": "FAIL" if validation.errors else ("CONCERNS" if validation.warnings else "PASS"),
        "weakestLayer": weakest,
        "layers": layers,
        "gates": gates,
        "blockers": [issue.as_dict() for issue in validation.errors],
        "warnings": [issue.as_dict() for issue in validation.warnings],
        "nextStep": _next_step(weakest),
    }


def _next_step(weakest: str) -> str:
    return {
        "T0": "Restore the missing or invalid T0 authority documents.",
        "T1": "Restore the T1 context anchors consumed by the support contract.",
        "Support": "Close the module support map before dependent delivery work.",
        "T2": "Route and cover every active standard and protocol.",
        "T3": "Remove archive authority leakage; archive-only hygiene remains nonblocking.",
        "none": "No governance repair is required.",
    }[weakest]


def validation_payload(validation: Validation) -> dict[str, Any]:
    return {
        "schema": "cdd.t0-t3.validation.v1",
        "project": str(validation.project),
        "verdict": "PASS" if validation.ok else "FAIL",
        "checks": validation.checks,
        "errors": [issue.as_dict() for issue in validation.errors],
        "warnings": [issue.as_dict() for issue in validation.warnings],
    }


def assess_blocking(
    issue_kind: str,
    *,
    direct_action: str | None = None,
    current_truth_consumes: bool = False,
) -> dict[str, Any]:
    """Apply the impact-proportional blocking guard to common governance cases."""
    if issue_kind == "local_residue":
        if direct_action:
            return {"decision": "BLOCK_DIRECT_ACTION", "blockedActions": [direct_action]}
        return {"decision": "MERGE_FIRST", "blockedActions": []}
    if issue_kind == "t3_attachment":
        if current_truth_consumes:
            return {"decision": "BLOCK_CURRENT_TRUTH_CONSUMERS", "blockedActions": ["current-truth-consumers"]}
        return {"decision": "ARCHIVE_HYGIENE", "blockedActions": []}
    if issue_kind == "safety_check":
        if not direct_action:
            raise ValueError("safety_check requires direct_action")
        return {"decision": "BLOCK_DIRECT_ACTION", "blockedActions": [direct_action]}
    raise ValueError(f"unsupported issue kind: {issue_kind}")


def scaffold_project(project: Path, template_root: Path, force: bool) -> dict[str, Any]:
    project = project.resolve()
    project.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    replaced: list[str] = []
    skipped: list[str] = []
    for source in sorted(path for path in template_root.rglob("*") if path.is_file()):
        relative = source.relative_to(template_root)
        destination = project / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and not force:
            skipped.append(relative.as_posix())
            continue
        existed = destination.exists()
        shutil.copyfile(source, destination)
        (replaced if existed else created).append(relative.as_posix())
    (project / "memory_bank" / "t3_archives").mkdir(parents=True, exist_ok=True)
    return {
        "schema": "cdd.t0-t3.scaffold.v1",
        "project": str(project),
        "status": "PASS",
        "force": force,
        "created": created,
        "replaced": replaced,
        "skipped": skipped,
    }


def emit(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
        return
    verdict = payload.get("verdict", payload.get("status", "UNKNOWN"))
    print(f"{verdict}: {payload.get('project', '')}", file=sys.stderr)
    for issue in payload.get("errors", []):
        location = f" [{issue['path']}]" if "path" in issue else ""
        print(f"- {issue['code']}{location}: {issue['message']}", file=sys.stderr)
