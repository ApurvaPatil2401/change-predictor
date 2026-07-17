from dataclasses import dataclass, field
from typing import List

from change_predictor.symbols.symbol import Symbol


@dataclass
class File:
    """
    Represents a parsed Python source file.
    """

    path: str

    imports: List[str] = field(default_factory=list)

    classes: List[str] = field(default_factory=list)

    functions: List[str] = field(default_factory=list)

    symbols: List[Symbol] = field(default_factory=list)