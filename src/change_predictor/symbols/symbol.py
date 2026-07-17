from dataclasses import dataclass
from typing import Optional


@dataclass
class Symbol:
    """
    Represents a code symbol.
    """

    name: str
    symbol_type: str      # class, function, method
    file: str
    line: int
    parent: Optional[str] = None