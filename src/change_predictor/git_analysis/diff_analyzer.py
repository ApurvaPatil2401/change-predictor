
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class ChangedFile:
    path: str
    status: str
    added_lines: int
    deleted_lines: int


class GitDiffAnalyzer:
    """Extract changed Python files and line counts between Git revisions."""

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
            message = result.stderr.strip() or "Git command failed."
            raise RuntimeError(message)

        return result.stdout

    def analyze(
        self, base: str = "HEAD~1", head: str = "HEAD"
    ) -> List[ChangedFile]:
        """Return Python file changes with added/deleted line counts."""

        self._run_git("rev-parse", "--verify", f"{base}^{{commit}}")
        self._run_git("rev-parse", "--verify", f"{head}^{{commit}}")

        raw = self._run_git(
            "diff",
            "--numstat",
            "-z",
            "-M",
            base,
            head,
            "--",
            "*.py",
        )

        records = raw.split("\0")
        changed_files = []
        index = 0

        while index < len(records):
            record = records[index]
            index += 1

            if not record:
                continue

            parts = record.split("\t", 2)
            if len(parts) != 3:
                continue

            added, deleted, path = parts

            # With -z, a rename/copy record has an empty path field,
            # followed by the old path and then the new path.
            if path == "":
                if index + 1 >= len(records):
                    break

                old_path = records[index]
                new_path = records[index + 1]
                index += 2

                changed_files.append(
                    ChangedFile(
                        path=new_path,
                        status="R",
                        added_lines=0 if added == "-" else int(added),
                        deleted_lines=0 if deleted == "-" else int(deleted),
                    )
                )
                continue

            changed_files.append(
                ChangedFile(
                    path=path,
                    status="M",
                    added_lines=0 if added == "-" else int(added),
                    deleted_lines=0 if deleted == "-" else int(deleted),
                )
            )

        # Ask Git for statuses separately, using NUL-delimited output.
        status_output = self._run_git(
            "diff",
            "--name-status",
            "-z",
            "-M",
            base,
            head,
            "--",
            "*.py",
        )
        status_parts = status_output.split("\0")
        status_by_path = {}
        index = 0

        while index < len(status_parts):
            status = status_parts[index]
            index += 1

            if not status:
                continue

            if status.startswith(("R", "C")):
                if index + 1 >= len(status_parts):
                    break

                old_path = status_parts[index]
                new_path = status_parts[index + 1]
                index += 2
                status_by_path[new_path] = status[0]
            else:
                if index >= len(status_parts):
                    break

                path = status_parts[index]
                index += 1
                status_by_path[path] = status

        # Ensure added/deleted/renamed status is accurate.
        for item in changed_files:
            item.status = status_by_path.get(item.path, item.status)

        return changed_files
