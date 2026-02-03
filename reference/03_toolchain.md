# 03_Toolchain: CLI & Configuration

**Type**: T1 (Technical Reference)
**Purpose**: Comprehensive guide to the CDD Python scripts and configuration.

## 1. Core Scripts

### `cdd-feature.py` (The Scaffolder)
Generates documentation skeletons based on templates.
* **Usage**: `python scripts/cdd-feature.py "feature_name" [description] [--target <path>] [--no-branch]`
* **Function**:
    1.  Reads templates from `templates/04_standards/` (Source).
    2.  Creates `specs/{ID}-{name}/` directory in target project.
    3.  Generates DS-050 (spec), DS-051 (plan), DS-052 (tasks), and a feature README.
    4.  Optionally creates a Git branch with the feature name.

### `cdd_audit.py` (The Judge)
Enforces the Legal Framework (§100-§300).
* **Usage**: `python scripts/cdd_audit.py --gate [1|2|3|all]`
* **Gates**:
    * **Gate 1 (Version Consistency)**: Checks version alignment across all CDD files using `scripts/verify_versions.py`.
    * **Gate 2 (Behavior Verification)**: Runs `pytest` to verify test compliance.
    * **Gate 3 (Entropy Monitoring)**: Calculates system entropy ($H_{sys}$) using `scripts/measure_entropy.py`.

### `measure_entropy.py` (The Meter)
Calculates the system entropy score.
* **Usage**: `python scripts/measure_entropy.py`
* **Output**: JSON report with $H_{cog}$, $H_{struct}$, $H_{align}$.

## 2. Configuration (`cdd_config.yaml`)
Located at project root (or `templates/` for default).
* **`project_name`**: Target project identifier.
* **`llm_model`**: Model used for generation (e.g., Minimax).
* **`entropy_thresholds`**: Custom limits for Red/Yellow/Green states.

## 3. External Auditor Interface
CDD supports external validation hooks.
* **Interface**: Any executable returning standard exit codes (0=Pass, 1=Fail).
* **Integration**: Add script path to `cdd_config.yaml` under `hooks`.