
from dataclasses import dataclass
from typing import List

from anyio import Path

from change_predictor.git_analysis.line_change_parser import (
    GitLineChangeParser,
)
from change_predictor.git_analysis.line_changes import FileLineChanges
from change_predictor.git_analysis.symbol_mapper import ChangedSymbolMapper
from change_predictor.impact.impact_engine import ImpactEngine
from change_predictor.models.risk_report import RiskReport


@dataclass
class ChangedFileImpact:
    """Impact analysis for one file changed between Git revisions."""

    path: str
    added_lines: int
    deleted_lines: int
    changed_symbols: List[str]
    risk_report: RiskReport


@dataclass
class ChangeImpactReport:
    """Combined impact report for a Git revision diff."""

    base_revision: str
    head_revision: str
    changed_files: List[ChangedFileImpact]
    changed_symbols: List[str]


class ChangeImpactAnalyzer:
    """Connect Git line changes and symbol mapping to existing impact analysis."""

    def __init__(
        self,
        repository_path: str,
        impact_engine: ImpactEngine,
    ):
        self.repository_path = repository_path
        self.impact_engine = impact_engine
        self.line_parser = GitLineChangeParser(repository_path)
        self.symbol_mapper = ChangedSymbolMapper(repository_path)

    def analyze(
        self,
        base: str = "HEAD~1",
        head: str = "HEAD",
    ) -> ChangeImpactReport:
        line_changes = self.line_parser.parse(base, head)
        symbols = self.symbol_mapper.map_changes(line_changes)

        symbols_by_file = {}
        for symbol in symbols:
            symbols_by_file.setdefault(symbol.file, []).append(
                symbol.qualified_name
            )

        file_impacts = []

        for change in line_changes:
            target_name = Path(change.path).name
            risk_report = self.impact_engine.analyze(target_name)

            file_impacts.append(
                ChangedFileImpact(
                    path=change.path,
                    added_lines=sum(r.count for r in change.added),
                    deleted_lines=sum(r.count for r in change.deleted),
                    changed_symbols=sorted(
                        set(symbols_by_file.get(change.path, []))
                    ),
                    risk_report=risk_report,
                )
            )

        return ChangeImpactReport(
            base_revision=base,
            head_revision=head,
            changed_files=file_impacts,
            changed_symbols=sorted(
                {
                    symbol.qualified_name
                    for symbol in symbols
                }
            ),
        )
