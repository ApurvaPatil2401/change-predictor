
from pathlib import Path
import sys

from change_predictor.cli import build_repository
from change_predictor.graph.graph_builder import GraphBuilder
from change_predictor.impact.impact_engine import ImpactEngine
from change_predictor.git_analysis.change_impact_analyzer import (
    ChangeImpactAnalyzer,
)


def main() -> None:
    if len(sys.argv) not in (2, 4):
        print(
            "Usage:\n"
            "  python -m change_predictor.git_analysis.run_git_impact <repo>\n"
            "  python -m change_predictor.git_analysis.run_git_impact "
            "<repo> <base_revision> <head_revision>"
        )
        raise SystemExit(1)

    repository_path = Path(sys.argv[1]).resolve()

    if not repository_path.is_dir():
        print(f"Error: repository directory not found: {repository_path}")
        raise SystemExit(1)

    base = sys.argv[2] if len(sys.argv) == 4 else "HEAD~1"
    head = sys.argv[3] if len(sys.argv) == 4 else "HEAD"

    repository = build_repository(repository_path)
    dependency_graph = GraphBuilder().build(repository)
    impact_engine = ImpactEngine(dependency_graph)

    analyzer = ChangeImpactAnalyzer(
        str(repository_path),
        impact_engine,
    )
    report = analyzer.analyze(base, head)

    print("=" * 65)
    print("CHANGE PREDICTOR — GIT CHANGE IMPACT")
    print("=" * 65)
    print(f"Base revision: {report.base_revision}")
    print(f"Head revision: {report.head_revision}")
    print(f"Changed Python files: {len(report.changed_files)}")
    print(f"Changed symbols detected: {len(report.changed_symbols)}")

    for item in report.changed_files:
        print()
        print(f"File: {item.path}")
        print(
            f"Added lines: {item.added_lines} | "
            f"Deleted lines: {item.deleted_lines}"
        )
        print(f"Risk: {item.risk_report.risk_level} "
              f"(score {item.risk_report.score})")

        print("Changed symbols:")
        if item.changed_symbols:
            for symbol in item.changed_symbols:
                print(f"  - {symbol}")
        else:
            print("  - No enclosing function/class detected")

        print("Potentially impacted files:")
        impacted = item.risk_report.transitive_impacts
        if impacted:
            for path in impacted:
                print(f"  - {path}")
        else:
            print("  - None detected")

    print()
    print("=" * 65)
    print("Analysis complete. Results are heuristic, not a guarantee.")
    print("=" * 65)


if __name__ == "__main__":
    main()
