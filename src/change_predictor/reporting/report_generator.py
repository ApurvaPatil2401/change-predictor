from change_predictor.impact.impact_engine import ImpactEngine
from change_predictor.simulation.simulation_engine import SimulationEngine
from change_predictor.reporting.impact_report import ImpactReport


class ReportGenerator:
    """
    Combines all analysis engines into a single report.
    """

    def __init__(
        self,
        impact_engine: ImpactEngine,
        simulation_engine: SimulationEngine,
    ) -> None:

        self.impact_engine = impact_engine
        self.simulation_engine = simulation_engine

    def generate(self, target: str) -> ImpactReport:

        risk_report = self.impact_engine.analyze(target)

        simulation_report = self.simulation_engine.simulate(risk_report)

        return ImpactReport(
            target=target,
            risk=risk_report,
            simulation=simulation_report,
        )