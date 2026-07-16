from typing import List

from change_predictor.graph.dependency_graph import DependencyGraph


class ImpactEngine:
    """
    Predicts the impact of changes using the dependency graph.
    """

    def __init__(self, dependency_graph: DependencyGraph) -> None:
        self.dependency_graph = dependency_graph

    def find_direct_impacts(self, target: str) -> List[str]:
        """
        Find all files that directly depend on the target file.

        Args:
            target: Target filename (e.g. "repository.py")

        Returns:
            List of directly affected files.
        """

        impacted_files = []

        graph = self.dependency_graph.get_all_dependencies()

        for source, dependencies in graph.items():

            for dependency in dependencies:

                if dependency.target == target:
                    impacted_files.append(source)

        return sorted(set(impacted_files))