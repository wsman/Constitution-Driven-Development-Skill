from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_script(name: str, *arguments: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *arguments],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def scaffold(project: Path) -> dict[str, object]:
    result = run_script("scaffold_t0_t3.py", "--project", str(project), "--json")
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout.count("\n") == 1
    return json.loads(result.stdout)


def validate(project: Path) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    result = run_script("validate_t0_t3.py", "--project", str(project), "--json")
    assert result.stderr == ""
    assert result.stdout.count("\n") == 1
    return result, json.loads(result.stdout)


def established_project(tmp_path: Path, *, newline: str = "\n") -> Path:
    project = tmp_path / "established"
    memory_bank = project / "memory_bank"
    t0 = memory_bank / "t0_core"
    t1 = memory_bank / "t1_axioms"
    t2 = memory_bank / "t2_execution"
    t3 = memory_bank / "t3_archive"
    protocol = project / "production" / "epics" / "example-module"
    archive = project / "design" / "cdd" / "reviews"
    for directory in (t0, t1, t2, t3, protocol, archive):
        directory.mkdir(parents=True, exist_ok=True)

    def write(path: Path, text: str) -> None:
        path.write_text(text, encoding="utf-8", newline=newline)

    write(memory_bank / "README.md", "# Memory Bank\n\nEstablished schema 3.0 layout.\n")
    for name in (
        "active_context.md",
        "amendment_log.md",
        "basic_law_index.md",
        "current_state.md",
        "release_state.md",
    ):
        write(t0 / name, f"# {name}\n")
    for name in ("behavior_context.md", "knowledge_graph.md", "system_patterns.md", "tech_context.md"):
        write(t1 / name, f"# {name}\n")
    write(t2 / "workflow_contract.md", "# Workflow contract\n")
    write(protocol / "story-001-example.md", "# Story protocol\n")
    write(archive / "README.md", "# Reviews\n")
    support = {
        "schemaVersion": "3.0",
        "coreThesis": "Established project",
        "moduleOrder": ["example-module"],
        "modules": {
            "example-module": {
                "t0Refs": {
                    "landscape": "memory_bank/t1_axioms/knowledge_graph.md#example",
                    "status": "memory_bank/t0_core/active_context.md#status",
                    "baseline": "memory_bank/t0_core/current_state.md#baseline",
                },
                "t1Refs": {
                    "systemPatterns": "memory_bank/t1_axioms/system_patterns.md#example",
                    "behaviorContext": "memory_bank/t1_axioms/behavior_context.md#example",
                    "techContext": "memory_bank/t1_axioms/tech_context.md#example",
                },
                "t2Refs": [
                    {
                        "path": "memory_bank/t2_execution/workflow_contract.md",
                        "kind": "standard",
                        "coverage": ["constraint", "t1-support"],
                        "t1Anchors": [
                            "memory_bank/t1_axioms/system_patterns.md#example",
                            "memory_bank/t1_axioms/behavior_context.md#example",
                            "memory_bank/t1_axioms/tech_context.md#example",
                        ],
                    },
                    {
                        "path": "production/epics/example-module/story-001-example.md",
                        "kind": "protocol",
                        "coverage": ["execution", "validation", "evidence"],
                    },
                ],
                "archiveRoot": "design/cdd/reviews/",
            }
        },
    }
    write(t1 / "module_support_map.yaml", yaml.safe_dump(support, sort_keys=False))
    return project


def test_scaffold_validate_and_diagnose_happy_path(tmp_path: Path) -> None:
    project = tmp_path / "project"
    payload = scaffold(project)
    assert payload["schema"] == "cdd.t0-t3.scaffold.v1"
    assert payload["created"]

    validation, validation_payload = validate(project)
    assert validation.returncode == 0
    assert validation_payload["verdict"] == "PASS"

    diagnosis = run_script("diagnose_t0_t3.py", "--project", str(project), "--json")
    assert diagnosis.returncode == 0
    parsed = json.loads(diagnosis.stdout)
    assert parsed["schema"] == "cdd.t0-t3.diagnosis.v1"
    assert parsed["verdict"] == "PASS"
    assert parsed["weakestLayer"] == "none"
    assert [gate["status"] for gate in parsed["gates"]] == ["PASS"] * 5 + ["READY", "PASS"]


def test_scaffold_is_create_only_until_force(tmp_path: Path) -> None:
    project = tmp_path / "project"
    scaffold(project)
    active = project / "memory_bank" / "t0_core" / "active_context.md"
    active.write_text("local content\n", encoding="utf-8", newline="\n")

    second = scaffold(project)
    assert active.read_text(encoding="utf-8") == "local content\n"
    assert "memory_bank/t0_core/active_context.md" in second["skipped"]

    forced = run_script("scaffold_t0_t3.py", "--project", str(project), "--force", "--json")
    assert forced.returncode == 0
    assert active.read_text(encoding="utf-8").startswith("# Active Context")
    assert "memory_bank/t0_core/active_context.md" in json.loads(forced.stdout)["replaced"]


def test_established_schema3_layout_accepts_crlf_and_external_routes(tmp_path: Path) -> None:
    project = established_project(tmp_path, newline="\r\n")
    result, payload = validate(project)
    assert result.returncode == 0
    assert payload["verdict"] == "PASS"
    layout = next(check for check in payload["checks"] if check["name"] == "layout_profile")
    assert layout["detail"] == "established-schema3"


@pytest.mark.parametrize("force", [False, True])
def test_scaffold_refuses_to_reorganize_established_layout(tmp_path: Path, force: bool) -> None:
    project = established_project(tmp_path)
    arguments = ["--project", str(project), "--json"]
    if force:
        arguments.append("--force")
    before = (project / "memory_bank" / "README.md").read_bytes()
    result = run_script("scaffold_t0_t3.py", *arguments)
    assert result.returncode == 1
    assert json.loads(result.stdout)["failureReason"] == "ESTABLISHED_LAYOUT"
    assert (project / "memory_bank" / "README.md").read_bytes() == before
    assert not (project / "memory_bank" / "t2_standards").exists()


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("support_path", "SUPPORT_PATH"),
        ("coverage", "SUPPORT_COVERAGE"),
        ("archive_root", "SUPPORT_ARCHIVE"),
        ("authority", "T3_AUTHORITY_LEAK"),
        ("bare_cr", "TEXT_ENCODING"),
    ],
)
def test_established_schema3_drift_is_rejected(tmp_path: Path, mutation: str, expected_code: str) -> None:
    project = established_project(tmp_path)
    support_path = project / "memory_bank" / "t1_axioms" / "module_support_map.yaml"
    support = yaml.safe_load(support_path.read_text(encoding="utf-8"))
    module = support["modules"]["example-module"]
    if mutation == "support_path":
        module["t2Refs"][1]["path"] = "production/epics/example-module/story-missing.md"
    elif mutation == "coverage":
        module["t2Refs"][1]["coverage"].remove("evidence")
    elif mutation == "archive_root":
        module["archiveRoot"] = "design/cdd/missing/"
    elif mutation == "authority":
        path = project / "memory_bank" / "t0_core" / "active_context.md"
        path.write_text(path.read_text(encoding="utf-8") + "T3 is authoritative for release.\n", encoding="utf-8")
    elif mutation == "bare_cr":
        path = project / "memory_bank" / "t0_core" / "active_context.md"
        path.write_bytes(b"# Active\rbare\n")
    if mutation in {"support_path", "coverage", "archive_root"}:
        support_path.write_text(yaml.safe_dump(support, sort_keys=False), encoding="utf-8", newline="\n")
    result, payload = validate(project)
    assert result.returncode == 1
    assert expected_code in {issue["code"] for issue in payload["errors"]}


@pytest.mark.parametrize(
    "payload",
    [
        b"\xef\xbb\xbf# BOM\n",
        b"# NUL\x00\n",
        b"# invalid \xff\n",
    ],
)
def test_established_schema3_rejects_invalid_text_bytes(tmp_path: Path, payload: bytes) -> None:
    project = established_project(tmp_path)
    (project / "memory_bank" / "t0_core" / "active_context.md").write_bytes(payload)
    result, parsed = validate(project)
    assert result.returncode == 1
    assert "TEXT_ENCODING" in {issue["code"] for issue in parsed["errors"]}


def test_project_defaults_to_current_directory(tmp_path: Path) -> None:
    result = run_script("scaffold_t0_t3.py", "--json", cwd=tmp_path)
    assert result.returncode == 0
    assert json.loads(result.stdout)["project"] == str(tmp_path.resolve())


def test_usage_error_is_exit_two_and_does_not_emit_json(tmp_path: Path) -> None:
    result = run_script("validate_t0_t3.py", "--project", str(tmp_path), "--unknown")
    assert result.returncode == 2
    assert result.stdout == ""
    assert "unrecognized arguments" in result.stderr


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("missing_t0", "T0_MISSING"),
        ("malformed_yaml", "SUPPORT_PARSE"),
        ("stale_t2", "T2_STALE_ROUTE"),
        ("incomplete_support", "SUPPORT_COVERAGE"),
        ("t3_authority_leak", "T3_AUTHORITY_LEAK"),
    ],
)
def test_validation_failures_are_specific(tmp_path: Path, mutation: str, expected_code: str) -> None:
    project = tmp_path / mutation
    scaffold(project)
    support_path = project / "memory_bank" / "module_support_map.yaml"
    if mutation == "missing_t0":
        (project / "memory_bank" / "t0_core" / "active_context.md").unlink()
    elif mutation == "malformed_yaml":
        support_path.write_text("modules: [\n", encoding="utf-8", newline="\n")
    elif mutation == "stale_t2":
        (project / "memory_bank" / "t2_standards" / "DS-999_unrouted.md").write_text(
            "# Unrouted\n", encoding="utf-8", newline="\n"
        )
    elif mutation == "incomplete_support":
        support = yaml.safe_load(support_path.read_text(encoding="utf-8"))
        support["modules"]["example-module"]["t2Refs"][1]["coverage"].remove("evidence")
        support_path.write_text(yaml.safe_dump(support, sort_keys=False), encoding="utf-8", newline="\n")
    elif mutation == "t3_authority_leak":
        path = project / "memory_bank" / "t0_core" / "active_context.md"
        path.write_text(path.read_text(encoding="utf-8") + "T3 is authoritative for release.\n", encoding="utf-8", newline="\n")

    result, payload = validate(project)
    assert result.returncode == 1
    assert payload["verdict"] == "FAIL"
    assert expected_code in {issue["code"] for issue in payload["errors"]}


def test_plain_output_uses_stderr_only(tmp_path: Path) -> None:
    project = tmp_path / "project"
    scaffold(project)
    result = run_script("validate_t0_t3.py", "--project", str(project))
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr.startswith("PASS:")
