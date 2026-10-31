
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PROJECT_SRC))

from change_predictor.git_analysis.change_impact_analyzer import (
    ChangeImpactAnalyzer,
)


def run_git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()

    run_git(repo, "init")
    run_git(repo, "config", "user.name", "Test User")
    run_git(repo, "config", "user.email", "test@example.com")

    helper = repo / "helper.py"
    helper.write_text(
        "def calculate(value):\n    return value + 1\n",
        encoding="utf-8",
    )

    run_git(repo, "add", ".")
    run_git(repo, "commit", "-m", "initial commit")

    return repo


def test_change_impact_report_detects_rename(
    git_repo: Path,
) -> None:
    old_file = git_repo / "helper.py"
    new_file = git_repo / "calculator.py"

    old_file.rename(new_file)

    run_git(git_repo, "add", "-A")
    run_git(git_repo, "commit", "-m", "rename helper")

    impact_engine = Mock()
    impact_engine.analyze.return_value = Mock()

    analyzer = ChangeImpactAnalyzer(
        str(git_repo),
        impact_engine,
    )

    report = analyzer.analyze("HEAD~1", "HEAD")

    renamed_entries = [
        change
        for change in report.changed_files
        if change.status == "R"
    ]

    assert len(renamed_entries) == 1
    assert renamed_entries[0].path == "calculator.py"
    assert renamed_entries[0].old_path == "helper.py"
