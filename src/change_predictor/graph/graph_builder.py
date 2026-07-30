from pathlib import Path

from change_predictor.graph.dependency_graph import DependencyGraph
from change_predictor.models.dependency import Dependency
from change_predictor.models.repository import Repository


class GraphBuilder:
    """
    Builds a dependency graph from repository imports.
    """

    def build(self, repository: Repository) -> DependencyGraph:

        graph = DependencyGraph()

        # Build lookup table for every repository module
        repository_modules = {}

        for file in repository.files:

            path = Path(file.path)

            filename = path.name
            stem = path.stem

            # repository
            repository_modules[stem] = filename

            # change_predictor.models.repository
            qualified = ".".join(
                path.with_suffix("").parts[-3:]
            )

            repository_modules[qualified] = filename

        for file in repository.files:

            source = Path(file.path).name

            for imported_module in file.imports:

                target = None

                # Exact match
                if imported_module in repository_modules:
                    target = repository_modules[imported_module]

                # Last module name
                elif imported_module.split(".")[-1] in repository_modules:
                    target = repository_modules[
                        imported_module.split(".")[-1]
                    ]

                if (
                    target
                    and target != source
                ):
                    graph.add_dependency(
                        Dependency(
                            source=source,
                            target=target,
                            dependency_type="import",
                        )
                    )

        return graph