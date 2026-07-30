import json
from dataclasses import asdict
from pathlib import Path


class JsonExporter:
    """
    Exports analysis reports as JSON.
    """

    def export(self, report, output_file: str) -> None:

        Path(output_file).write_text(
            json.dumps(asdict(report), indent=4),
            encoding="utf-8",
        )