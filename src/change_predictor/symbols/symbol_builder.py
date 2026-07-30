from change_predictor.models.repository import Repository
from change_predictor.symbols.symbol_table import SymbolTable


class SymbolBuilder:
    """
    Builds a repository-wide symbol table.
    """

    def build(self, repository: Repository) -> SymbolTable:

        table = SymbolTable()

        for file in repository.files:
            for symbol in file.symbols:
                table.add(symbol)

        return table