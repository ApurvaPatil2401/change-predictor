
import re
import subprocess
from pathlib import Path
from typing import List

from change_predictor.git_analysis.line_changes import (
    FileLineChanges,
    LineRange,
)

HUNK_PATTERN = re.compile(
    r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@"
)


class GitLineChangeParser:
    """Parse Git diffs into line ranges, including deletions and renames."""

    def __init__(self, repository_path: str = "."):
        self.repository_path = Path(repository_path).resolve()

    def _run_git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.repository_path), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or "Git diff command failed."
            )
        return result.stdout

    def parse(
        self,
        base: str = "HEAD~1",
        head: str = "HEAD",
    ) -> List[FileLineChanges]:
        """Return changed line ranges keyed by the available file path."""

        self._run_git("rev-parse", "--verify", f"{base}^{{commit}}")
        self._run_git("rev-parse", "--verify", f"{head}^{{commit}}")

        diff = self._run_git(
            "diff",
            "--no-ext-diff",
            "--no-renames",
            "--unified=0",
            base,
            head,
            "--",
            "*.py",
        )

        results = []
        old_path = None
        new_path = None
        added_ranges = []
        deleted_ranges = []

        def normalize_path(header: str) -> str:
            path = header[2:] if header.startswith(("a/", "b/")) else header
            return path

        def save_current_file():
            if old_path is None and new_path is None:
                return

            # For deleted files retain the old path. Otherwise use the new path.
            path = new_path or old_path
            if path is None:
                return

            if added_ranges or deleted_ranges:
                results.append(
                    FileLineChanges(
                        path=path,
                        added=added_ranges.copy(),
                        deleted=deleted_ranges.copy(),
                    )
                )

        for line in diff.splitlines():
            if line.startswith("--- "):
                save_current_file()
                added_ranges = []
                deleted_ranges = []

                header = line[4:]
                old_path = (
                    None if header == "/dev/null"
                    else normalize_path(header)
                )
                new_path = None
                continue

            if line.startswith("+++ "):
                header = line[4:]
                new_path = (
                    None if header == "/dev/null"
                    else normalize_path(header)
                )
                continue

            match = HUNK_PATTERN.match(line)
            if not match:
                continue

            old_start = int(match.group(1))
            old_count = int(match.group(2) or "1")
            new_start = int(match.group(3))
            new_count = int(match.group(4) or "1")

            if new_count > 0:
                added_ranges.append(
                    LineRange(start=new_start, count=new_count)
                )
            if old_count > 0:
                deleted_ranges.append(
                    LineRange(start=old_start, count=old_count)
                )

        save_current_file()

        return results
