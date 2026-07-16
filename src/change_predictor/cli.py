import sys
from pathlib import Path

from change_predictor.analyzer.scanner import RepositoryScanner
from change_predictor.analyzer.python_parser import PythonParser
from change_predictor.graph.graph_builder import GraphBuilder
from change_predictor.impact.impact_engine import ImpactEngine
from change_predictor.models.repository import Repository


def build_repository(repository_path: Path) -> Repository:
    scanner = RepositoryScanner(str(repository_path))
    parser = PythonParser()

    repository = Repository(root_path=str(repository_path))

    for file_path in scanner.scan():
        repository.files.append(parser.parse(file_path))

    return repository


def main() -> None:

    if len(sys.argv) not in (2, 4):
        print(
            "Usage:\n"
            "  python -m change_predictor.cli <repository_path>\n"
            "  python -m change_predictor.cli <repository_path> --impact <file>"
        )
        sys.exit(1)

    repository_path = Path(sys.argv[1])

    if not repository_path.exists():
        print(f"Error: '{repository_path}' does not exist.")
        sys.exit(1)

    repository = build_repository(repository_path)

    graph_builder = GraphBuilder()
    dependency_graph = graph_builder.build(repository)

    # Impact Mode
    if len(sys.argv) == 4 and sys.argv[2] == "--impact":

        target_file = sys.argv[3]

        engine = ImpactEngine(dependency_graph)

        impacted = engine.find_direct_impacts(target_file)

        print("=" * 60)
        print("Impact Analysis")
        print("=" * 60)
        print(f"Target File: {target_file}")
        print()

        if impacted:
            print("Directly Affected Files")
            print("-" * 60)

            for file in impacted:
                print(f"✔ {file}")

            print()
            print(f"Total Direct Impact: {len(impacted)}")

        else:
            print("No direct impacts found.")

        print("=" * 60)
        return

    # Normal Analysis Mode
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