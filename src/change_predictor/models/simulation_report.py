from dataclasses import dataclass
from typing import List


@dataclass
class SimulationReport:
    """
    Represents the simulated outcome of changing a file.
    """

    target: str
    affected_files: List[str]
    estimated_effort: str
    confidence: int
    recommendations: List[str]