from typing import List, Set

from change_predictor.call_graph.call_graph import CallGraph


class DeadCodeDetector:
    """
    Detects functions that are never called.
    """

    def __init__(self, call_graph: CallGraph) -> None:
        self.call_graph = call_graph

    def find_unused_functions(self) -> List[str]:
        graph = self.call_graph.get_graph()

        all_functions: Set[str] = set(graph.keys())
        called_functions: Set[str] = set()

        for calls in graph.values():
            called_functions.update(calls)

        unused = []

        for function in sorted(all_functions):

            simple_name = function.split(".")[-1]

            # Ignore dunder methods
            if simple_name.startswith("__"):
                continue

            # Ignore private methods
            if simple_name.startswith("_"):
                continue

            # Ignore AST visitor hooks
            if simple_name.startswith("visit_"):
                continue

            # Ignore recursive helpers
            if simple_name == "dfs":
                continue

            # Ignore CLI entry point
            if simple_name == "main":
                continue

            if function not in called_functions:
                unused.append(function)

        return unused