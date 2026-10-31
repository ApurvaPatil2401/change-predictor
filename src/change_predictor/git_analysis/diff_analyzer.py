
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class ChangedFile:
    """Represents a changed file between two Git revisions."""

    path: str
    status: str
    added_lines: int
    deleted_lines: int
    old_path: Optional[str] = None


class GitDiffAnalyzer:
    """Extract Python file changes and line counts between revisions."""

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
        self,
        base: str = "HEAD~1",
        head: str = "HEAD",
    ) -> List[ChangedFile]:
        """Return Python file changes, including rename information."""

        self._run_git("rev-parse", "--verify", f"{base}^{{commit}}")
        self._run_git("rev-parse", "--verify", f"{head}^{{commit}}")

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
                    raise RuntimeError("Incomplete Git rename record.")

                old_path = status_parts[index]
                new_path = status_parts[index + 1]
                index += 2

                status_by_path[new_path] = (
                    status[0],
                    old_path,
                )
            else:
                if index >= len(status_parts):
                    raise RuntimeError("Incomplete Git status record.")

                path = status_parts[index]
                index += 1

                status_by_path[path] = (status, None)

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

            if path == "":
                if index + 1 >= len(records):
                    raise RuntimeError("Incomplete Git numstat rename record.")

                old_path = records[index]
                new_path = records[index + 1]
                index += 2
                path = new_path
            else:
                old_path = None

            status, recorded_old_path = status_by_path.get(
                path,
                ("M", None),
            )

            if recorded_old_path is not None:
                old_path = recorded_old_path

            changed_files.append(
                ChangedFile(
                    path=path,
                    status=status,
                    added_lines=0 if added == "-" else int(added),
                    deleted_lines=0 if deleted == "-" else int(deleted),
                    old_path=old_path,
                )
            )

        return changed_files
