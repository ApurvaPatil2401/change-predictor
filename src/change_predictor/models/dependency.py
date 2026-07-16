from dataclasses import dataclass


@dataclass(frozen=True)
class Dependency:
    """
    Represents a dependency relationship between two files.
    """

    source: str
    target: str
    dependency_type: str = "import"