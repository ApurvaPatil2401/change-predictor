from dataclasses import dataclass, field
from typing import List


@dataclass
class File:
    """
    Represents a Python source file.
    """

    path: str
    imports: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)