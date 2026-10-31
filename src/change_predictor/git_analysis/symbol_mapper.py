
import ast
from pathlib import Path
from typing import List, Optional, Tuple

from change_predictor.git_analysis.line_changes import (
    FileLineChanges,
    LineRange,
)
from change_predictor.symbols.symbol import Symbol


class ChangedSymbolMapper:
    """Map changed lines to Python functions and classes."""

    def __init__(self, repository_path: str = "."):
        self.repository_path = Path(repository_path).resolve()

    def _read_python_file(self, relative_path: str) -> Optional[str]:
        file_path = (self.repository_path / relative_path).resolve()

        try:
            file_path.relative_to(self.repository_path)
        except ValueError:
            return None

        if not file_path.is_file() or file_path.suffix != ".py":
            return None

        try:
            return file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return None

    def _extract_symbols(
        self, relative_path: str, source: str
    ) -> List[Tuple[Symbol, int]]:
        try:
            tree = ast.parse(source, filename=relative_path)
        except (SyntaxError, ValueError):
            return []

        symbols: List[Tuple[Symbol, int]] = []

        def visit(node, parents: List[str]) -> None:
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.ClassDef):
                    name = child.name
                    qualified_name = ".".join(parents + [name])
                    end_line = getattr(child, "end_lineno", child.lineno)

                    symbol = Symbol(
                        name=name,
                        symbol_type="class",
                        file=relative_path,
                        line=child.lineno,
                        qualified_name=qualified_name,
                        parent=parents[-1] if parents else None,
                    )
                    symbols.append((symbol, end_line))
                    visit(child, parents + [name])

                elif isinstance(
                    child, (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    name = child.name
                    qualified_name = ".".join(parents + [name])
                    end_line = getattr(child, "end_lineno", child.lineno)

                    symbol = Symbol(
                        name=name,
                        symbol_type=(
                            "async_function"
                            if isinstance(child, ast.AsyncFunctionDef)
                            else "function"
                        ),
                        file=relative_path,
                        line=child.lineno,
                        qualified_name=qualified_name,
                        parent=parents[-1] if parents else None,
                    )
                    symbols.append((symbol, end_line))
                    visit(child, parents + [name])

                else:
                    visit(child, parents)

        visit(tree, [])
        return symbols

    @staticmethod
    def _overlaps(
        changed_range: LineRange, start: int, end: int
    ) -> bool:
        if changed_range.count <= 0:
            return False

        changed_start = changed_range.start
        changed_end = changed_start + changed_range.count - 1

        return changed_start <= end and start <= changed_end

    def map_changes(
        self, changes: List[FileLineChanges]
    ) -> List[Symbol]:
        """Return symbols whose source ranges overlap added lines."""

        matched = {}

        for file_change in changes:
            source = self._read_python_file(file_change.path)
            if source is None:
                # Deleted files have no current source to parse.
                continue

            symbols = self._extract_symbols(file_change.path, source)

            for symbol, end_line in symbols:
                if any(
                    self._overlaps(changed_range, symbol.line, end_line)
                    for changed_range in file_change.added
                ):
                    key = (
                        symbol.file,
                        symbol.qualified_name,
                        symbol.symbol_type,
                    )
                    matched[key] = symbol

        return sorted(
            matched.values(),
            key=lambda symbol: (
                symbol.file,
                symbol.line,
                symbol.qualified_name,
            ),
        )
