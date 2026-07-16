from dataclasses import dataclass
from typing import List


@dataclass
class RiskReport:
    """
    Represents the risk analysis for changing a file.
    """

    target: str
    direct_impacts: List[str]
    transitive_impacts: List[str]
    risk_level: str
    score: int
    reasons: List[str]