from dataclasses import dataclass, field
from typing import List

from change_predictor.symbols.symbol import Symbol


@dataclass
class SymbolTable:
    """
    Stores every discovered symbol.
    """

    symbols: List[Symbol] = field(default_factory=list)

    def add(self, symbol: Symbol):
        self.symbols.append(symbol)

    def find(self, name: str):
        for symbol in self.symbols:
            if symbol.name == name:
                return symbol
        return None