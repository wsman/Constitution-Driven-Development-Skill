from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _governance import assess_blocking  # noqa: E402


def test_local_residue_does_not_block_independent_merge() -> None:
    decision = assess_blocking("local_residue")
    assert decision == {"decision": "MERGE_FIRST", "blockedActions": []}


def test_unreferenced_t3_attachment_is_archive_hygiene() -> None:
    decision = assess_blocking("t3_attachment", current_truth_consumes=False)
    assert decision == {"decision": "ARCHIVE_HYGIENE", "blockedActions": []}


def test_safety_check_blocks_only_destructive_action() -> None:
    decision = assess_blocking("safety_check", direct_action="delete-residue")
    assert decision == {
        "decision": "BLOCK_DIRECT_ACTION",
        "blockedActions": ["delete-residue"],
    }


def test_t3_leak_blocks_only_current_truth_consumers() -> None:
    decision = assess_blocking("t3_attachment", current_truth_consumes=True)
    assert decision == {
        "decision": "BLOCK_CURRENT_TRUTH_CONSUMERS",
        "blockedActions": ["current-truth-consumers"],
    }
