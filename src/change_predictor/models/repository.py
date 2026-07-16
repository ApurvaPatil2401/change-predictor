from dataclasses import dataclass, field
from typing import List

from .file import File


@dataclass
class Repository:
    """
    Represents an analyzed repository.
    """

    root_path: str
    files: List[File] = field(default_factory=list)

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def total_functions(self) -> int:
        return sum(len(file.functions) for file in self.files)

    @property
    def total_classes(self) -> int:
        return sum(len(file.classes) for file in self.files)

    @property
    def total_imports(self) -> int:
        return sum(len(file.imports) for file in self.files)