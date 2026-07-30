from pathlib import Path


class MermaidExporter:
    """
    Exports the dependency graph as a Mermaid diagram.
    """

    def export(self, dependency_graph, output_file="repository_graph.md"):

        graph = dependency_graph.get_all_dependencies()

        lines = [
            "# Repository Dependency Graph",
            "",
            "```mermaid",
            "graph TD",
        ]

        for source in sorted(graph):

            source_node = Path(source).stem

            if not graph[source]:
                lines.append(f"    {source_node}")

            for dependency in sorted(
                graph[source],
                key=lambda d: d.target,
            ):

                target_node = Path(dependency.target).stem

                lines.append(
                    f"    {source_node} --> {target_node}"
                )

        lines.append("```")

        Path(output_file).write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return output_file