import ast
from pathlib import Path

from change_predictor.models.file import File


class PythonParser:
    """
    Parses a Python source file using Python's built-in AST module.
    """

    def parse(self, file_path: Path) -> File:
        """
        Parse a Python file and extract imports, classes, and functions.
        """

        source = file_path.read_text(encoding="utf-8")

        tree = ast.parse(source)

        imports = []
        classes = []
        functions = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            elif isinstance(node, ast.AsyncFunctionDef):
                functions.append(node.name)

        return File(
            path=str(file_path),
            imports=sorted(imports),
            classes=sorted(classes),
            functions=sorted(functions),
        )