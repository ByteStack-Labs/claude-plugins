#!/usr/bin/env python3
"""
finalize.py - the single deterministic authority for placing an autopsy receipt.

The skill (an agent) writes its findings wherever it likes. This script, and only
this script, decides where the receipt lands, what it is named, and whether it is
allowed to ship. Paths resolve relative to the target repo root, so placement is
rename-proof and independent of operator memory or model behavior. Standard library
only: no shell, no git binary, no non-stdlib imports. Runs identically on Windows,
macOS, and Linux.

Usage:
    python3 finalize.py <fixture> <report-src> <verify-src>

Override the output root (default: receipts):
    AR_OUT_DIR=diagnostics python3 finalize.py ...
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def repo_root(start: Path) -> Path:
    """Nearest ancestor containing .git; fall back to CWD. No git binary needed."""
    for d in (start, *start.parents):
        if (d / ".git").exists():
            return d
    return Path.cwd()


def fail(msg: str) -> None:
    print(f"finalize: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) != 4:
        fail("usage: finalize.py <fixture> <report-src> <verify-src>")

    fixture, report_src, verify_src = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    out_dir = os.environ.get("AR_OUT_DIR", "receipts")

    if not report_src.is_file():
        fail(f"report source not found: {report_src}")
    if not verify_src.is_file():
        fail(f"verify source not found: {verify_src}")

    root = repo_root(report_src.resolve())
    dest = root / out_dir / fixture
    dest.mkdir(parents=True, exist_ok=True)

    report_dst = dest / "REPORT.md"
    verify_dst = dest / "verify.py"
    shutil.move(str(report_src), str(report_dst))
    shutil.move(str(verify_src), str(verify_dst))

    # Guard: the report must reference verify.py relatively, never repo-rooted.
    rooted = re.compile(r"(receipts|recipes|diagnostics)/\S+/verify\.py")
    if rooted.search(report_dst.read_text(encoding="utf-8")):
        fail(
            "REPORT.md references a repo-rooted verify path; use a path relative to "
            "the report itself (e.g. 'python3 verify.py')."
        )

    # Certify: the receipt must reproduce before it is allowed to ship.
    result = subprocess.run(
        [sys.executable, "verify.py"],
        cwd=dest,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        fail("verify.py did not reproduce; receipt NOT certified.")

    print(
        f"finalize: receipt placed and certified at {dest.relative_to(root).as_posix()}/"
    )


if __name__ == "__main__":
    main()
