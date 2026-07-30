import ast
from pathlib import Path

from change_predictor.models.file import File
from change_predictor.symbols.symbol import Symbol


class SymbolCollector(ast.NodeVisitor):
    """
    Collect imports, classes, functions, and symbols from a Python file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

        self.imports = []
        self.classes = []
        self.functions = []
        self.symbols = []

        self.current_class = None

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node):
        """
        Record only the imported module, not the imported symbol.

        Example:
            from change_predictor.models.repository import Repository

        becomes

            change_predictor.models.repository
        """

        if node.module:
            self.imports.append(node.module)
    def visit_ClassDef(self, node):

        self.classes.append(node.name)

        self.symbols.append(
            Symbol(
                name=node.name,
                symbol_type="class",
                file=self.file_path,
                line=node.lineno,
                qualified_name=node.name,
            )
        )

        previous = self.current_class
        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = previous

    def visit_FunctionDef(self, node):

        self.functions.append(node.name)

        symbol_type = (
            "method"
            if self.current_class
            else "function"
        )

        qualified_name = (
            f"{self.current_class}.{node.name}"
            if self.current_class
            else node.name
        )

        self.symbols.append(
            Symbol(
                name=node.name,
                symbol_type=symbol_type,
                file=self.file_path,
                line=node.lineno,
                parent=self.current_class,
                qualified_name=qualified_name,
            )
        )

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef


class PythonParser:
    """
    Parses a Python source file.
    """

    def parse(self, file_path: Path) -> File:

        source = file_path.read_text(encoding="utf-8")

        tree = ast.parse(source)

        collector = SymbolCollector(str(file_path))
        collector.visit(tree)

        return File(
            path=str(file_path),
            imports=sorted(collector.imports),
            classes=sorted(collector.classes),
            functions=sorted(collector.functions),
            symbols=collector.symbols,
        )