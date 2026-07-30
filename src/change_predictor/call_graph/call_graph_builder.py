import ast
from pathlib import Path

from change_predictor.call_graph.call_graph import CallGraph
from change_predictor.models.repository import Repository
from change_predictor.symbols.symbol_builder import SymbolBuilder


class FunctionCallVisitor(ast.NodeVisitor):
    """
    Visits Python AST nodes and records calls between repository functions.
    """

    def __init__(self, symbol_lookup: dict[str, str]) -> None:
        self.symbol_lookup = symbol_lookup

        self.call_graph = CallGraph()

        self.current_class = None
        self.current_function = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        previous = self.current_class
        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = previous

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        previous = self.current_function

        if self.current_class:
            self.current_function = (
                f"{self.current_class}.{node.name}"
            )
        else:
            self.current_function = node.name

        self.generic_visit(node)

        self.current_function = previous

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Call(self, node: ast.Call) -> None:
        if not self.current_function:
            self.generic_visit(node)
            return

        callee = None

        # foo()
        if isinstance(node.func, ast.Name):
            callee = self.symbol_lookup.get(node.func.id)

        # obj.foo()
        elif isinstance(node.func, ast.Attribute):
            callee = self.symbol_lookup.get(node.func.attr)

        if (
            callee
            and callee != self.current_function
        ):
            self.call_graph.add_call(
                self.current_function,
                callee,
            )

        self.generic_visit(node)


class CallGraphBuilder:
    """
    Builds a repository-wide function call graph.
    """

    def build(
        self,
        repository: Repository,
    ) -> CallGraph:

        # Build repository symbol table
        symbol_table = SymbolBuilder().build(repository)

        # Map simple name -> qualified name
        symbol_lookup = {}

        for symbol in symbol_table.symbols:

            if symbol.symbol_type not in (
                "function",
                "method",
            ):
                continue

            symbol_lookup[symbol.name] = (
                symbol.qualified_name
            )

        visitor = FunctionCallVisitor(symbol_lookup)

        for file in repository.files:

            source = Path(file.path).read_text(
                encoding="utf-8"
            )

            tree = ast.parse(source)

            visitor.visit(tree)

        return visitor.call_graph