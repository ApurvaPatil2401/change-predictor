
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from change_predictor.git_analysis.diff_analyzer import GitDiffAnalyzer
from change_predictor.git_analysis.line_change_parser import (
    GitLineChangeParser,
)
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
    status: str
    old_path: Optional[str] = None


@dataclass
class ChangeImpactReport:
    """Combined impact report for a Git revision diff."""

    base_revision: str
    head_revision: str
    changed_files: List[ChangedFileImpact]
    changed_symbols: List[str]


class ChangeImpactAnalyzer:
    """Connect Git changes, symbol mapping, and risk analysis."""

    def __init__(
        self,
        repository_path: str,
        impact_engine: ImpactEngine,
    ):
        self.repository_path = repository_path
        self.impact_engine = impact_engine

        self.line_parser = GitLineChangeParser(repository_path)
        self.diff_analyzer = GitDiffAnalyzer(repository_path)
        self.symbol_mapper = ChangedSymbolMapper(repository_path)

    def analyze(
        self,
        base: str = "HEAD~1",
        head: str = "HEAD",
    ) -> ChangeImpactReport:

        line_changes = self.line_parser.parse(base, head)
        diff_changes = self.diff_analyzer.analyze(base, head)

        symbols = self.symbol_mapper.map_changes(line_changes)

        symbols_by_file = {}
        for symbol in symbols:
            symbols_by_file.setdefault(symbol.file, []).append(
                symbol.qualified_name
            )

        diff_by_path = {
            change.path: change
            for change in diff_changes
        }

        file_impacts = []

        for change in line_changes:
            diff_change = diff_by_path.get(change.path)

            status = diff_change.status if diff_change else "M"
            old_path = diff_change.old_path if diff_change else None

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
                    status=status,
                    old_path=old_path,
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
