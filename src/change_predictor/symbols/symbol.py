from dataclasses import dataclass
from typing import Optional


@dataclass
class Symbol:
    """
    Represents a code symbol.
    """

    name: str
    symbol_type: str
    file: str
    line: int
    qualified_name: str
    parent: Optional[str] = None