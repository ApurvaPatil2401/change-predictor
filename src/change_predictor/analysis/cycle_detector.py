from typing import Dict, List, Set

from change_predictor.graph.dependency_graph import DependencyGraph


class CycleDetector:
    """
    Detects circular dependencies in the dependency graph.
    """

    def __init__(self, graph: DependencyGraph) -> None:
        self.graph = graph

    def find_cycles(self) -> List[List[str]]:
        """
        Returns a list of dependency cycles.
        """

        graph = self.graph.get_all_dependencies()

        adjacency: Dict[str, List[str]] = {}

        for source, dependencies in graph.items():
            adjacency[source] = [dependency.target for dependency in dependencies]

        visited: Set[str] = set()
        stack: List[str] = []
        cycles: List[List[str]] = []

        def dfs(node: str):

            if node in stack:
                start = stack.index(node)
                cycle = stack[start:] + [node]

                if cycle not in cycles:
                    cycles.append(cycle)

                return

            if node in visited:
                return

            visited.add(node)
            stack.append(node)

            for neighbor in adjacency.get(node, []):
                dfs(neighbor)

            stack.pop()

        for node in adjacency:
            dfs(node)

        return cycles