from typing import List, Set

from change_predictor.graph.dependency_graph import DependencyGraph
from change_predictor.models.risk_report import RiskReport


class ImpactEngine:
    """
    Predicts the impact of changes using the dependency graph.
    """

    def __init__(self, dependency_graph: DependencyGraph) -> None:
        self.dependency_graph = dependency_graph

    def find_direct_impacts(self, target: str) -> List[str]:
        impacted_files = []

        graph = self.dependency_graph.get_all_dependencies()

        for source, dependencies in graph.items():
            for dependency in dependencies:
                if dependency.target == target:
                    impacted_files.append(source)

        return sorted(set(impacted_files))

    def find_transitive_impacts(self, target: str) -> List[str]:
        visited: Set[str] = set()
        impacted: Set[str] = set()

        def dfs(current_target: str):
            for source in self.find_direct_impacts(current_target):
                if source not in visited:
                    visited.add(source)
                    impacted.add(source)
                    dfs(source)

        dfs(target)

        return sorted(impacted)

    def analyze(self, target: str) -> RiskReport:
        direct = self.find_direct_impacts(target)
        transitive = self.find_transitive_impacts(target)

        score = len(direct) * 10 + len(transitive) * 5

        if score <= 20:
            risk_level = "LOW"
        elif score <= 50:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        reasons = [
            f"{len(direct)} direct dependencies",
            f"{len(transitive)} total impacted files",
        ]

        return RiskReport(
            target=target,
            direct_impacts=direct,
            transitive_impacts=transitive,
            risk_level=risk_level,
            score=score,
            reasons=reasons,
        )