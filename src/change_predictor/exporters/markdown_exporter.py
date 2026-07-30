from pathlib import Path

from change_predictor.reporting.impact_report import ImpactReport


class MarkdownExporter:
    """
    Exports an ImpactReport as Markdown.
    """

    def export(
        self,
        report: ImpactReport,
        output_file: str,
    ) -> None:

        path = Path(output_file)

        lines = [
            "# Change Predictor Report",
            "",
            f"## Target File",
            f"`{report.target}`",
            "",
            "## Risk Assessment",
            "",
            f"- **Risk Level:** {report.risk.risk_level}",
            f"- **Risk Score:** {report.risk.score}",
            "",
            "## Direct Impact",
        ]

        if report.risk.direct_impacts:
            for file in report.risk.direct_impacts:
                lines.append(f"- {file}")
        else:
            lines.append("- None")

        lines.extend([
            "",
            "## Transitive Impact",
        ])

        if report.risk.transitive_impacts:
            for file in report.risk.transitive_impacts:
                lines.append(f"- {file}")
        else:
            lines.append("- None")

        lines.extend([
            "",
            "## Simulation",
            "",
            f"- **Estimated Effort:** {report.simulation.estimated_effort}",
            f"- **Confidence:** {report.simulation.confidence}%",
            "",
            "## Recommendations",
        ])

        for recommendation in report.simulation.recommendations:
            lines.append(f"- {recommendation}")

        path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )