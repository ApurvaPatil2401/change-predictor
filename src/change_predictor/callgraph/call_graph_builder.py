import ast
from pathlib import Path

from change_predictor.callgraph.call_graph import CallGraph
from change_predictor.models.repository import Repository
from change_predictor.symbols.symbol_builder import SymbolBuilder


class FunctionCallVisitor(ast.NodeVisitor):
    """
    Visits function bodies and records only internal function calls.
    """

    def __init__(self, repository_symbols):

        self.current_function = None
        self.call_graph = CallGraph()

        # Store names of all symbols in the repository
        self.repository_symbols = repository_symbols

    def visit_FunctionDef(self, node):

        previous = self.current_function
        self.current_function = node.name

        self.generic_visit(node)

        self.current_function = previous

    def visit_AsyncFunctionDef(self, node):

        self.visit_FunctionDef(node)

    def visit_Call(self, node):

        if self.current_function:

            callee = None

            if isinstance(node.func, ast.Name):
                callee = node.func.id

            elif isinstance(node.func, ast.Attribute):
                callee = node.func.attr

            # Keep only repository symbols
            if (
                callee
                and callee in self.repository_symbols
                and callee != self.current_function
            ):
                self.call_graph.add_call(
                    self.current_function,
                    callee,
                )

        self.generic_visit(node)

class CallGraphBuilder:
    """
    Builds a function call graph from a repository.
    """

    def build(self, repository: Repository) -> CallGraph:

        # Build symbol table
        symbol_table = SymbolBuilder().build(repository)

        repository_symbols = {
            symbol.name
            for symbol in symbol_table.symbols
            if symbol.symbol_type in ("function", "method")
        }

        visitor = FunctionCallVisitor(repository_symbols)

        for file in repository.files:

            source = Path(file.path).read_text(encoding="utf-8")

            tree = ast.parse(source)

            visitor.visit(tree)

        return visitor.call_graph