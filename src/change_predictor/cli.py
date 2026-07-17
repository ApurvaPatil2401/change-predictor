import sys
from pathlib import Path

from change_predictor.analyzer.scanner import RepositoryScanner
from change_predictor.analyzer.python_parser import PythonParser
from change_predictor.graph.graph_builder import GraphBuilder
from change_predictor.impact.impact_engine import ImpactEngine
from change_predictor.models.repository import Repository
from change_predictor.simulation.simulation_engine import SimulationEngine


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

    if len(sys.argv) not in (2, 4):
        print(
            "Usage:\n"
            "  python -m change_predictor.cli <repository_path>\n"
            "  python -m change_predictor.cli <repository_path> --impact <file>\n"
            "  python -m change_predictor.cli <repository_path> --simulate <file>"
        )
        sys.exit(1)

    repository_path = Path(sys.argv[1])

    if not repository_path.exists():
        print(f"Error: '{repository_path}' does not exist.")
        sys.exit(1)

    repository = build_repository(repository_path)

    graph_builder = GraphBuilder()
    dependency_graph = graph_builder.build(repository)

    # =====================================================
    # IMPACT ANALYSIS
    # =====================================================

    if len(sys.argv) == 4 and sys.argv[2] == "--impact":

        target_file = sys.argv[3]

        engine = ImpactEngine(dependency_graph)
        report = engine.analyze(target_file)

        print("=" * 60)
        print("Impact Analysis")
        print("=" * 60)
        print(f"Target File: {target_file}")
        print()

        print("Direct Impact")
        print("-" * 60)

        if report.direct_impacts:
            for file in report.direct_impacts:
                print(f"✔ {file}")
        else:
            print("None")

        print()

        print("Transitive Impact")
        print("-" * 60)

        if report.transitive_impacts:
            for file in report.transitive_impacts:
                print(f"✔ {file}")
        else:
            print("None")

        print()
        print(f"Total Impacted Files: {len(report.transitive_impacts)}")

        print()
        print("Risk Assessment")
        print("-" * 60)
        print(f"Risk Level : {report.risk_level}")
        print(f"Risk Score : {report.score}")

        print()

        print("Reasons")
        print("-" * 60)

        for reason in report.reasons:
            print(f"• {reason}")

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
        print("No internal dependencies found.")
    else:
        for source, dependencies in all_dependencies.items():

            print(f"\n{source}")

            for dependency in dependencies:
                print(f"  └──> {dependency.target}")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()