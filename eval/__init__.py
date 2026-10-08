"""Independent evaluation: instances, reference execution, coverage and fault detection.

Keep evaluation code and reference tests outside the Agent workspace. Measurement
policies are selected by callers; reported results and limitations are documented
in docs/evaluation.md.
"""

from .dataset import Instance, load_dataset
from .metrics import Metrics, collect_metrics, run_pytest_on

__all__ = [
    "Instance",
    "Metrics",
    "collect_metrics",
    "load_dataset",
    "run_pytest_on",
]
