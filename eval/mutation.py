"""Compatibility imports: the standard-library mutation engine lives in the package."""
from code_agent.faults import (
    DEFAULT_MAX_MUTANTS, Mutant, default_operators, generate_mutants, mutation_summary,
)

__all__ = ["DEFAULT_MAX_MUTANTS", "Mutant", "default_operators", "generate_mutants", "mutation_summary"]
