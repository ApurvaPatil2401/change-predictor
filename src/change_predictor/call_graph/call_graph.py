from collections import defaultdict
from typing import Dict, List


class CallGraph:
    """
    Represents function call relationships.
    """

    def __init__(self) -> None:
        self.graph: Dict[str, List[str]] = defaultdict(list)

    def add_call(self, caller: str, callee: str) -> None:

        if callee not in self.graph[caller]:
            self.graph[caller].append(callee)

    def get_calls(self, caller: str) -> List[str]:

        return self.graph.get(caller, [])

    def get_graph(self):

        return self.graph