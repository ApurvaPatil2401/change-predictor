from dataclasses import dataclass

from change_predictor.models.risk_report import RiskReport
from change_predictor.models.simulation_report import SimulationReport


@dataclass
class ImpactReport:
    """
    Final report generated for a requested change.
    """

    target: str

    risk: RiskReport

    simulation: SimulationReport