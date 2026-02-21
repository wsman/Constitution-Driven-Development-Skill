"""
CDD Core Module v2.0.0
=====================
Core module: Constants, Exceptions, Constitution and Services.

Constitution Reference: §101

Module Structure:
- constants.py: Global constants
- constitution.py: Constitution definitions
- exceptions.py: Exception classes
- error_codes.py: Unified error codes
- asset_service.py: Technical asset management service
- audit_service.py: Audit service
- entropy_service.py: Entropy service
- feature_service.py: Feature service
- state_transition_service.py: State transition service
- state_validation_service.py: State validation service
"""

from .constants import *
from .exceptions import *

# Service modules (lazy import)
__services__ = [
    "asset_service",      # Technical asset management service
    "audit_service",      # Audit service
    "entropy_service",    # Entropy service 
    "feature_service",    # Feature service
    "state_transition_service",  # State transition service
    "state_validation_service",  # State validation service
]

__all__ = [
    # Constants
    "SKILL_ROOT", "VERSION", "DEFAULT_ENCODING",
    "REQUIRED_DIRS_PROJECT", "REQUIRED_DIRS_SKILL", "OPTIONAL_DIRS",
    "W_DIR", "W_SIG", "W_TEST", "THRESHOLD_WARNING", "THRESHOLD_DANGER",
    "CACHE_DIR_NAME", "CACHE_FILE", "CACHE_TTL",
    "TOOL_PREFIX", "TOOL_CATEGORIES",
    "CONSTITUTION_SECTION_PATTERN", "CONSTITUTION_REFERENCE_FORMAT",
    "STATE_ACTIVE", "STATE_SUSPENDED", "STATE_ARCHIVED",
    "ERROR_LEVEL_INFO", "ERROR_LEVEL_WARNING", "ERROR_LEVEL_ERROR", "ERROR_LEVEL_CRITICAL",
    "GATES",
    # Exceptions
    "CDDError", "SporeIsolationViolation", "EntropyThresholdExceeded", "ToolExecutionError",
    "CacheError", "ConstitutionViolation", "VersionDriftError", "DependencyError",
    "ServiceUnavailableError", "ConfigurationError", "ValidationError",
    # Service modules
    "__services__"
]


def get_service(name: str):
    """
    Get service module (lazy import)
    
    Args:
        name: Service name (audit, entropy, feature, state_transition, state_validation)
        
    Returns:
        Corresponding service module
    """
    import importlib
    module_name = f"{name}_service"
    if module_name not in __services__:
        raise ImportError(f"Unknown service: {name}")
    return importlib.import_module(f".{module_name}", package="core")