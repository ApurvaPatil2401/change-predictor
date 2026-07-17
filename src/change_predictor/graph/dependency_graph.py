from collections import defaultdict
from typing import Dict, List

from change_predictor.models.dependency import Dependency


class DependencyGraph:
    """
    Represents dependencies between files in a repository.
    """

    def __init__(self) -> None:
        self._graph: Dict[str, List[Dependency]] = defaultdict(list)

    def add_dependency(self, dependency):

        dependencies = self._graph[dependency.source]

        if dependency not in dependencies:
            dependencies.append(dependency)

    def get_dependencies(self, source: str) -> List[Dependency]:
        """
        Return all dependencies for a source file.

        Args:
            source: Source file name.

        Returns:
            List of Dependency objects.
        """
        return self._graph.get(source, [])

    def get_all_dependencies(self) -> Dict[str, List[Dependency]]:
        """
        Return the complete dependency graph.
        """
        return dict(self._graph)

    def __len__(self) -> int:
        """
        Return the total number of dependency relationships.
        """
        return sum(len(dependencies) for dependencies in self._graph.values())