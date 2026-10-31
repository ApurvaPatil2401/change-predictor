
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PROJECT_SRC))

from change_predictor.git_analysis.diff_analyzer import GitDiffAnalyzer
from change_predictor.git_analysis.line_change_parser import (
    GitLineChangeParser,
)


def run_git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()

    run_git(repo, "init")
    run_git(repo, "config", "user.name", "Test User")
    run_git(repo, "config", "user.email", "test@example.com")

    write_file(
        repo / "helper.py",
        "def calculate(value):\n    return value + 1\n",
    )
    run_git(repo, "add", ".")
    run_git(repo, "commit", "-m", "initial commit")

    return repo


def test_detects_modified_lines(git_repo: Path) -> None:
    write_file(
        git_repo / "helper.py",
        "def calculate(value):\n    return value + 2\n",
    )
    run_git(git_repo, "add", ".")
    run_git(git_repo, "commit", "-m", "modify helper")

    changes = GitLineChangeParser(str(git_repo)).parse(
        "HEAD~1", "HEAD"
    )

    assert len(changes) == 1
    assert changes[0].path == "helper.py"
    assert sum(r.count for r in changes[0].added) == 1
    assert sum(r.count for r in changes[0].deleted) == 1


def test_detects_deleted_file(git_repo: Path) -> None:
    (git_repo / "helper.py").unlink()
    run_git(git_repo, "add", "-A")
    run_git(git_repo, "commit", "-m", "delete helper")

    changes = GitLineChangeParser(str(git_repo)).parse(
        "HEAD~1", "HEAD"
    )

    assert len(changes) == 1
    assert changes[0].path == "helper.py"
    assert sum(r.count for r in changes[0].added) == 0
    assert sum(r.count for r in changes[0].deleted) == 2


def test_detects_renamed_file_as_old_and_new_paths(
    git_repo: Path,
) -> None:
    (git_repo / "helper.py").rename(git_repo / "calculator.py")
    run_git(git_repo, "add", "-A")
    run_git(git_repo, "commit", "-m", "rename helper")

    changes = GitLineChangeParser(str(git_repo)).parse(
        "HEAD~1", "HEAD"
    )

    paths = {change.path for change in changes}
    assert paths == {"helper.py", "calculator.py"}


def test_diff_analyzer_detects_modified_file(git_repo: Path) -> None:
    write_file(
        git_repo / "helper.py",
        "def calculate(value):\n    return value + 2\n",
    )
    run_git(git_repo, "add", ".")
    run_git(git_repo, "commit", "-m", "modify helper")

    changes = GitDiffAnalyzer(str(git_repo)).analyze(
        "HEAD~1", "HEAD"
    )

    assert len(changes) == 1
    assert changes[0].status == "M"
    assert changes[0].path == "helper.py"
    assert changes[0].old_path is None
    assert changes[0].added_lines == 1
    assert changes[0].deleted_lines == 1


def test_diff_analyzer_detects_added_file(git_repo: Path) -> None:
    write_file(
        git_repo / "new_module.py",
        "def greet():\n    return 'hello'\n",
    )
    run_git(git_repo, "add", ".")
    run_git(git_repo, "commit", "-m", "add module")

    changes = GitDiffAnalyzer(str(git_repo)).analyze(
        "HEAD~1", "HEAD"
    )

    assert len(changes) == 1
    assert changes[0].status == "A"
    assert changes[0].path == "new_module.py"
    assert changes[0].added_lines == 2


def test_diff_analyzer_detects_deleted_file(git_repo: Path) -> None:
    (git_repo / "helper.py").unlink()
    run_git(git_repo, "add", "-A")
    run_git(git_repo, "commit", "-m", "delete helper")

    changes = GitDiffAnalyzer(str(git_repo)).analyze(
        "HEAD~1", "HEAD"
    )

    assert len(changes) == 1
    assert changes[0].status == "D"
    assert changes[0].path == "helper.py"
    assert changes[0].deleted_lines == 2


def test_diff_analyzer_detects_rename_with_both_paths(
    git_repo: Path,
) -> None:
    (git_repo / "helper.py").rename(git_repo / "calculator.py")
    run_git(git_repo, "add", "-A")
    run_git(git_repo, "commit", "-m", "rename helper")

    changes = GitDiffAnalyzer(str(git_repo)).analyze(
        "HEAD~1", "HEAD"
    )

    assert len(changes) == 1
    assert changes[0].status == "R"
    assert changes[0].old_path == "helper.py"
    assert changes[0].path == "calculator.py"
