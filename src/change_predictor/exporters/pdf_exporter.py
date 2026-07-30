from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


class PdfExporter:
    """
    Export repository analysis to PDF.
    """

    def export(self, report: dict, output_file: str):

        styles = getSampleStyleSheet()

        doc = SimpleDocTemplate(output_file)

        story = []

        story.append(
            Paragraph("<b>Change Predictor Report</b>", styles["Title"])
        )

        story.append(
            Paragraph(
                "<b>Repository Summary</b>",
                styles["Heading2"],
            )
        )

        summary = report["summary"]

        story.append(
            Paragraph(
                f"Python Files : {summary['python_files']}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Classes : {summary['classes']}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Functions : {summary['functions']}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Imports : {summary['imports']}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                "<br/><b>Dependencies</b>",
                styles["Heading2"],
            )
        )

        for source, deps in report["dependencies"].items():

            story.append(
                Paragraph(
                    f"<b>{source}</b>",
                    styles["Heading3"],
                )
            )

            for dep in deps:

                # Handle Dependency object or plain string
                target = dep.target if hasattr(dep, "target") else str(dep)

                story.append(
                    Paragraph(
                        f"&nbsp;&nbsp;&nbsp;&nbsp;• {target}",
                        styles["BodyText"],
                    )
                )

            story.append(Paragraph("<br/>", styles["BodyText"]))
            
        story.append(
            Paragraph(
                "<br/><b>Circular Dependencies</b>",
                styles["Heading2"],
            )
        )

        cycles = report["cycles"]

        if cycles:

            for cycle in cycles:
                story.append(
                    Paragraph(
                        " → ".join(cycle),
                        styles["BodyText"],
                    )
                )

        else:

            story.append(
                Paragraph(
                    "None",
                    styles["BodyText"],
                )
            )

        story.append(
            Paragraph(
                "<br/><b>Unused Functions</b>",
                styles["Heading2"],
            )
        )

        unused = report["dead_code"]

        if unused:

            for func in unused:
                story.append(
                    Paragraph(
                        f"• {func}",
                        styles["BodyText"],
                    )
                )

        else:

            story.append(
                Paragraph(
                    "None",
                    styles["BodyText"],
                )
            )

        doc.build(story)