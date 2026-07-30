import sys
from pathlib import Path

from change_predictor.analyzer.scanner import RepositoryScanner
from change_predictor.analyzer.python_parser import PythonParser
from change_predictor.graph.graph_builder import GraphBuilder
from change_predictor.impact.impact_engine import ImpactEngine
from change_predictor.models.repository import Repository
from change_predictor.simulation.simulation_engine import SimulationEngine
from change_predictor.call_graph.call_graph import CallGraph
from change_predictor.call_graph.call_graph_builder import CallGraphBuilder
from change_predictor.reporting.report_generator import ReportGenerator
from change_predictor.simulation.simulation_engine import SimulationEngine
from change_predictor.analysis.cycle_detector import CycleDetector
from change_predictor.analysis.dead_code_detector import DeadCodeDetector
from change_predictor.exporters.json_exporter import JsonExporter
from change_predictor.exporters.markdown_exporter import MarkdownExporter
from change_predictor.exporters.html_exporter import HtmlExporter
from change_predictor.exporters.mermaid_exporter import MermaidExporter
from change_predictor.exporters.pdf_exporter import PdfExporter

def build_repository(repository_path: Path) -> Repository:
    """
    Build the repository model by scanning and parsing Python files.
    """

    scanner = RepositoryScanner(str(repository_path))
    parser = PythonParser()

    repository = Repository(root_path=str(repository_path))

    for file_path in scanner.scan():
        repository.files.append(parser.parse(file_path))

    return repository


def main() -> None:
    """
    Entry point for the Change Predictor CLI.
    """

    if len(sys.argv) not in (2, 3, 4, 5):
        print(
            "Usage:\n"
            "  python -m change_predictor.cli <repository_path>\n"
            "  python -m change_predictor.cli <repository_path> --impact <file>\n"
            "  python -m change_predictor.cli <repository_path> --simulate <file>\n"
            "  python -m change_predictor.cli <repository_path> --call-graph\n"
            "  python -m change_predictor.cli <repository_path> --json <file>\n"
            "  python -m change_predictor.cli <repository_path> --html <file>\n"
            "  python -m change_predictor.cli <repository_path> --mermaid <file>\n"
            "  python -m change_predictor.cli <repository_path> --pdf <file>"
        )
        sys.exit(1)

    repository_path = Path(sys.argv[1])

    if not repository_path.exists():
        print(f"Error: '{repository_path}' does not exist.")
        sys.exit(1)

    repository = build_repository(repository_path)
    

    graph_builder = GraphBuilder()
    dependency_graph = graph_builder.build(repository)

    call_graph_builder = CallGraphBuilder()
    call_graph = call_graph_builder.build(repository)

    # =====================================================
    # IMPACT ANALYSIS
    # =====================================================

    if len(sys.argv) == 4 and sys.argv[2] == "--impact":

            target_file = sys.argv[3]

            impact_engine = ImpactEngine(dependency_graph)
            simulation_engine = SimulationEngine()

            generator = ReportGenerator(
                impact_engine,
                simulation_engine,
            )

            report = generator.generate(target_file)

            print("=" * 60)
            print("Impact Analysis")
            print("=" * 60)

            print(f"Target File : {report.target}")

            print()

            print("Direct Impact")
            print("-" * 60)

            if report.risk.direct_impacts:
                for file in report.risk.direct_impacts:
                    print(f"✔ {file}")
            else:
                print("None")

            print()

            print("Transitive Impact")
            print("-" * 60)

            if report.risk.transitive_impacts:
                for file in report.risk.transitive_impacts:
                    print(f"✔ {file}")
            else:
                print("None")

            print()

            print("Risk Assessment")
            print("-" * 60)
            print(f"Risk Level : {report.risk.risk_level}")
            print(f"Risk Score : {report.risk.score}")

            print()

            print("Reasons")
            print("-" * 60)

            for reason in report.risk.reasons:
                print(f"• {reason}")

            print()

            print("Simulation")
            print("-" * 60)
            print(f"Estimated Effort : {report.simulation.estimated_effort}")
            print(f"Confidence       : {report.simulation.confidence}%")

            print()

            print("Recommendations")
            print("-" * 60)

            for recommendation in report.simulation.recommendations:
                print(f"• {recommendation}")

            print()
            print("=" * 60)

            return
    # =====================================================
    # CHANGE SIMULATION
    # =====================================================

    if len(sys.argv) == 4 and sys.argv[2] == "--simulate":

        target_file = sys.argv[3]

        impact_engine = ImpactEngine(dependency_graph)

        risk_report = impact_engine.analyze(target_file)

        simulation = SimulationEngine().simulate(risk_report)

        print("=" * 60)
        print("Change Simulation")
        print("=" * 60)
        print(f"Target File : {simulation.target}")
        print()

        print(f"Estimated Effort : {simulation.estimated_effort}")
        print(f"Confidence       : {simulation.confidence}%")

        print()

        print("Affected Files")
        print("-" * 60)

        if simulation.affected_files:
            for file in simulation.affected_files:
                print(f"✔ {file}")
        else:
            print("None")

        print()

        print("Recommendations")
        print("-" * 60)

        for recommendation in simulation.recommendations:
            print(f"• {recommendation}")

        print()
        print("=" * 60)

        return

    # =====================================================
# CALL GRAPH
# =====================================================

    if len(sys.argv) == 3 and sys.argv[2] == "--call-graph":

        print("=" * 60)
        print("Call Graph")
        print("=" * 60)

        graph = call_graph.get_graph()

        if not graph:
            print("No function calls found.")
            return

        internal_prefixes = (
            "visit_",
            "dfs",
            "__",
        )

        internal_classes = (
            "FunctionCallVisitor",
        )

        for caller in sorted(graph):

            if (
                any(caller.startswith(prefix) for prefix in internal_prefixes)
                or caller.split(".")[0] in internal_classes
            ):
                continue

            visible = []

            for callee in sorted(graph[caller]):

                if (
                    any(callee.startswith(prefix) for prefix in internal_prefixes)
                    or callee.split(".")[0] in internal_classes
                ):
                    continue

                if callee == caller:
                    continue

                visible.append(callee)

            if not visible:
                continue

            print(f"\n{caller}")

            for callee in visible:
                print(f"  └──> {callee}")

        print()
        print("=" * 60)

        return

    # =====================================================
# JSON EXPORT
# =====================================================

    if len(sys.argv) == 4 and sys.argv[2] == "--json":

        target_file = sys.argv[3]

        impact_engine = ImpactEngine(dependency_graph)
        simulation_engine = SimulationEngine()

        generator = ReportGenerator(
            impact_engine,
            simulation_engine,
        )

        report = generator.generate(target_file)

        exporter = JsonExporter()

        output = f"{Path(target_file).stem}_report.json"

        exporter.export(report, output)

        print("=" * 60)
        print("JSON Report")
        print("=" * 60)
        print(f"Saved to: {output}")
        print("=" * 60)

        return

    if len(sys.argv) == 4 and sys.argv[2] == "--md":

        target = sys.argv[3]

        impact_engine = ImpactEngine(dependency_graph)
        simulation_engine = SimulationEngine()

        generator = ReportGenerator(
            impact_engine,
            simulation_engine,
        )

        report = generator.generate(target)

        MarkdownExporter().export(
            report,
            f"{Path(target).stem}_report.md",
        )

        print("=" * 60)
        print("Markdown Report")
        print("=" * 60)
        print(
            f"Saved to: {Path(target).stem}_report.md"
        )
        print("=" * 60)

        return

    # =====================================================
    # HTML EXPORT
    # =====================================================

    if len(sys.argv) == 3 and sys.argv[2] == "--html":

        cycle_detector = CycleDetector(dependency_graph)
        cycles = cycle_detector.find_cycles()

        dead_detector = DeadCodeDetector(call_graph)
        unused = dead_detector.find_unused_functions()

        HtmlExporter().export(
            "repository_report.html",
            repository,
            dependency_graph,
            cycles,
            unused,
        )

        print("=" * 60)
        print("HTML Report")
        print("=" * 60)
        print("Saved to: repository_report.html")
        print("=" * 60)

        return


    # =====================================================
    # MERMAID EXPORT
    # =====================================================

    if len(sys.argv) == 3 and sys.argv[2] == "--mermaid":

        exporter = MermaidExporter()

        filename = exporter.export(dependency_graph)

        print("=" * 60)
        print("Mermaid Graph")
        print("=" * 60)
        print(f"Saved to: {filename}")
        print("=" * 60)

        return

    if len(sys.argv) == 4 and sys.argv[2] == "--pdf":

        exporter = PdfExporter()

        exporter.export(
            report,
            "repository_report.pdf",
        )

        print("=" * 60)
        print("PDF Report")
        print("=" * 60)
        print("Saved to: repository_report.pdf")
        print("=" * 60)

        return

    # =====================================================
    # PDF EXPORT
    # =====================================================

    if len(sys.argv) == 3 and sys.argv[2] == "--pdf":

        dependency_graph_data = dependency_graph.get_all_dependencies()

        cycle_detector = CycleDetector(dependency_graph)
        cycles = cycle_detector.find_cycles()

        dead_detector = DeadCodeDetector(call_graph)
        dead_code = dead_detector.find_unused_functions()

        report = {
            "summary": {
                "python_files": repository.total_files,
                "classes": repository.total_classes,
                "functions": repository.total_functions,
                "imports": repository.total_imports,
            },
            "dependencies": dependency_graph_data,
            "cycles": cycles,
            "dead_code": dead_code,
        }

        PdfExporter().export(
            report,
            "repository_report.pdf",
        )

        print("=" * 60)
        print("PDF Report")
        print("=" * 60)
        print("Saved to: repository_report.pdf")
        print("=" * 60)

        return
    # =====================================================
    # REPOSITORY ANALYSIS
    # =====================================================

    print("=" * 60)
    print("Change Predictor")
    print("=" * 60)
    print(f"Analyzing repository: {repository_path}")
    print()

    print("Repository Summary")
    print("-" * 60)
    print(f"Python Files : {repository.total_files}")
    print(f"Classes      : {repository.total_classes}")
    print(f"Functions    : {repository.total_functions}")
    print(f"Imports      : {repository.total_imports}")
    

    print()

    print("Dependency Graph")
    print("-" * 60)

    all_dependencies = dependency_graph.get_all_dependencies()

    if not all_dependencies:
        print("No internal module dependencies detected.")
    else:
        for source in sorted(all_dependencies):

            print(f"\n{source}")

            for dependency in sorted(
                all_dependencies[source],
                key=lambda d: d.target,
            ):
                print(f"  └──> {dependency.target}")
    """print()
    print()
    print("Call Graph")
    print("-" * 60)

    graph = call_graph.get_graph()

    if not graph:
        print("No function calls found.")
    else:
        internal_prefixes = (
        "visit_",
        "dfs",
        "__",
        )

        internal_classes = (
            "FunctionCallVisitor",
        )

        graph = call_graph.get_graph()

        for caller in sorted(graph):

            # Skip internal callers
            if (
                any(caller.startswith(prefix) for prefix in internal_prefixes)
                or caller.split(".")[0] in internal_classes
            ):
                continue

            # Filter internal callees
            visible = []

            for callee in sorted(graph[caller]):

                if (
                    any(callee.startswith(prefix) for prefix in internal_prefixes)
                    or callee.split(".")[0] in internal_classes
                ):
                    continue

                visible.append(callee)

            if not visible:
                continue

            print(f"\n{caller}")

            for callee in visible:
                print(f"  └──> {callee}")"""
    print("=" * 60)
    print()
    print("Circular Dependencies")
    print("-" * 60)

    cycle_detector = CycleDetector(dependency_graph)

    cycles = cycle_detector.find_cycles()

    if not cycles:
        print("No circular dependencies found.")
    else:
        for cycle in cycles:
            print(" -> ".join(cycle))

    print()
    print("Dead Code Detection")
    print("-" * 60)

    dead_detector = DeadCodeDetector(call_graph)

    unused = dead_detector.find_unused_functions()

    public_unused = [
        f for f in unused
        if not (
            f.endswith(".build")
            or ".dfs" in f
            or "visit_" in f
        )
    ]

    if not public_unused:
        print("No obvious unused public functions found.")
    else:
        for function in public_unused:
            print(f"⚠ {function}")

    print()
    print("=" * 60)
    print("Analysis Complete")
    print("=" * 60)
    print(f"Files Analyzed : {repository.total_files}")
    print(f"Dependencies   : {sum(len(v) for v in all_dependencies.values())}")
    print(f"Circular Cycles: {len(cycles)}")
    print(f"Unused APIs    : {len(public_unused)}")

if __name__ == "__main__":
    main()