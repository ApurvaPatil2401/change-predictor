import ast
from pathlib import Path

from change_predictor.models.file import File
from change_predictor.symbols.symbol import Symbol


class PythonParser:
    """
    Parses a Python source file using Python AST.
    """

    def parse(self, file_path: Path) -> File:

        source = file_path.read_text(encoding="utf-8")

        tree = ast.parse(source)

        imports = []
        classes = []
        functions = []
        symbols = []

        for node in tree.body:

            # -------------------------
            # Imports
            # -------------------------

            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")

            # -------------------------
            # Classes
            # -------------------------

            elif isinstance(node, ast.ClassDef):

                classes.append(node.name)

                symbols.append(
                    Symbol(
                        name=node.name,
                        symbol_type="class",
                        file=file_path.name,
                        line=node.lineno,
                    )
                )

                # -------------------------
                # Methods
                # -------------------------

                for child in node.body:

                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):

                        symbols.append(
                            Symbol(
                                name=child.name,
                                symbol_type="method",
                                file=file_path.name,
                                line=child.lineno,
                                parent=node.name,
                            )
                        )

            # -------------------------
            # Top-level Functions
            # -------------------------

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                functions.append(node.name)

                symbols.append(
                    Symbol(
                        name=node.name,
                        symbol_type="function",
                        file=file_path.name,
                        line=node.lineno,
                    )
                )

        return File(
            path=str(file_path),
            imports=sorted(imports),
            classes=sorted(classes),
            functions=sorted(functions),
            symbols=symbols,
        )