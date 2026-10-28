
from dataclasses import dataclass
from typing import List


@dataclass
class LineRange:
    """A range of changed lines in the new version of a file."""

    start: int
    count: int


@dataclass
class FileLineChanges:
    """Line-level changes for a single file."""

    path: str
    added: List[LineRange]
    deleted: List[LineRange]
