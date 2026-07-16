import sys
from pathlib import Path

from change_predictor.analyzer.scanner import RepositoryScanner
from change_predictor.analyzer.python_parser import PythonParser
from change_predictor.models.repository import Repository


def main() -> None:
    """
    Entry point for the Change Predictor CLI.
    """

    if len(sys.argv) != 2:
        print("Usage: python -m change_predictor.cli <repository_path>")
        sys.exit(1)

    repository_path = Path(sys.argv[1])

    if not repository_path.exists():
        print(f"Error: '{repository_path}' does not exist.")
        sys.exit(1)

    print("=" * 50)
    print("Change Predictor")
    print("=" * 50)
    print(f"Analyzing repository: {repository_path}")
    print()

    scanner = RepositoryScanner(str(repository_path))
    parser = PythonParser()

    repository = Repository(root_path=str(repository_path))

    python_files = scanner.scan()

    for file_path in python_files:
        file_model = parser.parse(file_path)
        repository.files.append(file_model)

    print("Analysis Complete")
    print("-" * 50)
    print(f"Python Files : {repository.total_files}")
    print(f"Classes      : {repository.total_classes}")
    print(f"Functions    : {repository.total_functions}")
    print(f"Imports      : {repository.total_imports}")
    print("=" * 50)


if __name__ == "__main__":
    main()