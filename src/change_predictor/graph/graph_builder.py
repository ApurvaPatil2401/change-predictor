from pathlib import Path

from change_predictor.graph.dependency_graph import DependencyGraph
from change_predictor.models import repository
from change_predictor.models.dependency import Dependency
from change_predictor.models.repository import Repository


class GraphBuilder:
    """
    Builds a dependency graph from an analyzed repository.
    """

    def build(self, repository: Repository) -> DependencyGraph:
        """
        Build a dependency graph from the repository.

        Args:
            repository: Repository model containing parsed files.

        Returns:
            DependencyGraph containing import relationships.
        """

        graph = DependencyGraph()

        repository_modules = {
            Path(file.path).stem: Path(file.path).name
            for file in repository.files
        }

        for file in repository.files:

            source = Path(file.path).name

            for imported_module in file.imports:

                # Example:
                # change_predictor.models.repository
                # becomes
                # repository
                module_name = imported_module.split(".")[-1]

                if module_name in repository_modules:

                    graph.add_dependency(
                        Dependency(
                            source=source,
                            target=repository_modules[module_name],
                            dependency_type="import",
                        )
                    )
        return graph