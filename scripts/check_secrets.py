"""Portable source/staged-blob scan. Findings contain paths/line numbers, never values.

This heuristic is a release gate, not a comprehensive secret or vulnerability audit.
Use --staged from a git checkout to examine the actual index, including root files.
"""
import argparse
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
PRIVATE_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".pem", ".key", ".crt", ".pfx", ".p12", ".dump", ".backup", ".bak"}
PATTERN = re.compile(
    r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{10,}|(?:AKIA|ASIA)[0-9A-Z]{16}|"
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|[0-9]{8,12}:AA[A-Za-z0-9_-]{30,}|"
    r"sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}|"
    r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"
)


def private_path(path):
    name = path.name.lower()
    return ((name.startswith(".env") and name != ".env.example")
            or path.suffix.lower() in PRIVATE_SUFFIXES
            or any(s in name for s in (".sqlite-wal", ".sqlite-shm", ".sqlite3-wal", ".sqlite3-shm", ".db-wal", ".db-shm", ".db-journal"))
            or ".private." in name or bool({"backups", "credentials", ".ssh"} & set(path.parts)))


def scan_blob(path, blob):
    findings = []
    if private_path(path):
        findings.append(f"{path.as_posix()}: private/runtime file")
    text = blob.decode("utf-8", errors="replace")
    for i, line in enumerate(text.splitlines(), 1):
        if PATTERN.search(line):
            findings.append(f"{path.as_posix()}:{i}: potential credential material")
    return findings


def scan_tree(root):
    findings = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if EXCLUDED.intersection(rel.parts):
            continue
        if path.is_symlink():
            findings.append(f"{rel.as_posix()}: symlink not allowed in source release")
        elif path.is_file():
            findings.extend(scan_blob(rel, path.read_bytes()))
    return findings


def scan_staged():
    top = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    raw = subprocess.check_output(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"], cwd=top)
    paths = [p.decode("utf-8") for p in raw.split(b"\0") if p]
    findings = []
    for name in paths:
        path = Path(name)
        if EXCLUDED.intersection(path.parts):
            findings.append(f"{path.as_posix()}: cache/environment is staged")
        blob = subprocess.check_output(["git", "show", ":" + name], cwd=top)
        findings.extend(scan_blob(path, blob))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("Scan root must be an existing directory")
    try:
        findings = scan_staged() if args.staged else scan_tree(args.root.resolve())
    except (OSError, subprocess.CalledProcessError):
        print("Secret scan could not read all requested files/index; scan failed.")
        return 2
    if findings:
        print("Potential secrets/private runtime artifacts found:")
        print("\n".join(findings))
        return 1
    print("Portable heuristic secret scan passed (not a full security audit).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
