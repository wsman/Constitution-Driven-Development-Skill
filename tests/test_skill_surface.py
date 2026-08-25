from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_only_governance_surface_remains() -> None:
    expected = {
        "README.md",
        "SKILL.md",
        "assets",
        "references",
        "requirements-test.txt",
        "requirements.txt",
        "scripts",
        "tests",
    }
    visible = {path.name for path in ROOT.iterdir() if not path.name.startswith(".")}
    assert visible == expected
    assert {path.name for path in (ROOT / "scripts").glob("*.py")} == {
        "_governance.py",
        "diagnose_t0_t3.py",
        "scaffold_t0_t3.py",
        "validate_t0_t3.py",
    }


def test_obsolete_runtime_terms_are_absent_from_active_skill() -> None:
    forbidden = (
        "ven" + "dor",
        "duck" + "db",
        "lake" + "house",
        "en" + "tropy",
        "sp" + "ore",
        "evo" + "lution",
        "refl" + "exion",
        "python -m " + "cdd",
        "cdd " + "session",
    )
    files = [ROOT / "SKILL.md", *sorted((ROOT / "scripts").glob("*.py")), *sorted((ROOT / "references").glob("*.md"))]
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in files)
    for term in forbidden:
        assert term not in combined
