from pathlib import Path
from typing import List


class RepositoryScanner:
    """
    Scans a repository and discovers Python source files.
    """

    IGNORED_DIRECTORIES = {
        ".git",
        "__pycache__",
        "venv",
        ".venv",
        "env",
        "node_modules",
        ".pytest_cache",
        ".mypy_cache",
        ".idea",
        ".vscode",
    }

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)

    def scan(self) -> List[Path]:
        """
        Return a list of Python source files.
        """
        python_files = []

        for file_path in self.root_path.rglob("*.py"):
            if any(
                ignored in file_path.parts
                for ignored in self.IGNORED_DIRECTORIES
            ):
                continue

            python_files.append(file_path)

        return sorted(python_files)