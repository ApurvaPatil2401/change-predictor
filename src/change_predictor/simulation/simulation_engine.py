from change_predictor.models.risk_report import RiskReport
from change_predictor.models.simulation_report import SimulationReport


class SimulationEngine:
    """
    Simulates the likely outcome of changing a file based on
    deterministic repository analysis.
    """

    def simulate(self, report: RiskReport) -> SimulationReport:
        """
        Simulate the impact of changing a file.

        Args:
            report: Risk analysis report.

        Returns:
            SimulationReport
        """

        affected_files = report.transitive_impacts

        total = len(affected_files)

        # -----------------------------------------
        # Estimate effort
        # -----------------------------------------

        if total <= 2:
            effort = "SMALL"
        elif total <= 5:
            effort = "MEDIUM"
        else:
            effort = "LARGE"

        # -----------------------------------------
        # Confidence score
        # -----------------------------------------

        confidence = max(50, 100 - total * 5)

        # -----------------------------------------
        # Recommendations
        # -----------------------------------------

        recommendations = []

        if report.direct_impacts:
            recommendations.append(
                "Review modules that directly import the target file."
            )

        if len(report.transitive_impacts) > len(report.direct_impacts):
            recommendations.append(
                "Run regression tests for downstream dependencies."
            )

        recommendations.append(
            "Verify public APIs remain backward compatible."
        )

        recommendations.append(
            "Review generated dependency graph before merging."
        )

        return SimulationReport(
            target=report.target,
            affected_files=affected_files,
            estimated_effort=effort,
            confidence=confidence,
            recommendations=recommendations,
        )