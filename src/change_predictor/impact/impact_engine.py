from typing import List, Set

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
        """

        impacted_files = []

        graph = self.dependency_graph.get_all_dependencies()

        for source, dependencies in graph.items():
            for dependency in dependencies:
                if dependency.target == target:
                    impacted_files.append(source)

        return sorted(set(impacted_files))

    def find_transitive_impacts(self, target: str) -> List[str]:
        """
        Find all files that are directly or indirectly affected.

        Example:

            A.py -> B.py -> C.py

        Changing C.py affects:

            B.py
            A.py
        """

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