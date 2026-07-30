from pathlib import Path


class HtmlExporter:
    """
    Exports repository analysis as an HTML report.
    """

    def export(
        self,
        output_path: str,
        repository,
        dependency_graph,
        cycles,
        unused,
    ):

        dependencies = dependency_graph.get_all_dependencies()

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<title>Change Predictor Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin:40px;
    background:#f4f6f9;
}}

h1 {{
    color:#1f4e79;
}}

.section {{
    background:white;
    padding:20px;
    margin-bottom:20px;
    border-radius:8px;
    box-shadow:0 2px 6px rgba(0,0,0,.1);
}}

table {{
    border-collapse:collapse;
    width:100%;
}}

th,td {{
    border:1px solid #ddd;
    padding:8px;
}}

th {{
    background:#1f4e79;
    color:white;
}}

ul {{
    margin-top:8px;
}}

</style>

</head>

<body>

<h1>Change Predictor Report</h1>

<div class="section">

<h2>Repository Summary</h2>

<table>

<tr><th>Metric</th><th>Value</th></tr>

<tr><td>Python Files</td><td>{repository.total_files}</td></tr>
<tr><td>Classes</td><td>{repository.total_classes}</td></tr>
<tr><td>Functions</td><td>{repository.total_functions}</td></tr>
<tr><td>Imports</td><td>{repository.total_imports}</td></tr>

</table>

</div>

<div class="section">

<h2>Dependency Graph</h2>

<ul>
"""

        for source in sorted(dependencies):

            html += f"<li><b>{source}</b><ul>"

            for dep in sorted(
                dependencies[source],
                key=lambda d: d.target,
            ):
                html += f"<li>{dep.target}</li>"

            html += "</ul></li>"

        html += """
</ul>

</div>

<div class="section">

<h2>Circular Dependencies</h2>

<ul>
"""

        if cycles:

            for cycle in cycles:
                html += "<li>" + " → ".join(cycle) + "</li>"

        else:
            html += "<li>None</li>"

        html += """
</ul>

</div>

<div class="section">

<h2>Dead Code</h2>

<ul>
"""

        if unused:

            for func in unused:
                html += f"<li>{func}</li>"

        else:
            html += "<li>None</li>"

        html += """

</ul>

</div>

</body>
</html>
"""

        Path(output_path).write_text(
            html,
            encoding="utf-8",
        )