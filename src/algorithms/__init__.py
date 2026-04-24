__version__ = "1.0.0"
__author__ = "Rudransh Kumar"
from .main import (
    init,
    run,
    set_algorithm,
    build_maze,
    Pathfinding_Algorithm_types,
    Pathfinding_Algorithm_index,
    NoPathFoundError,
    InvalidAlgorithmError,
    interval,
)

__all__ = [
    "init",
    "run",
    "set_algorithm",
    "build_maze",
    "Pathfinding_Algorithm_types",
    "Pathfinding_Algorithm_index",
    "NoPathFoundError",
    "InvalidAlgorithmError",
    "interval",
]