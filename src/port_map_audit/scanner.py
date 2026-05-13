from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path

from .models import PortHit, ScanReport

DEFAULT_IGNORE_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "target",
    "venv",
}

DEFAULT_EXTENSIONS = {
    ".conf",
    ".env",
    ".ini",
    ".json",
    ".mk",
    ".properties",
    ".service",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

DEFAULT_FILENAMES = {
    "Dockerfile",
    "Makefile",
    "Procfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "compose.yml",
    "compose.yaml",
}

PATTERNS = (
    ("url", re.compile(r"\b(?:https?|wss?|tcp|udp)://[^\s'\"<>:]+:(?P<port>\d{2,5})\b")),
    ("assignment", re.compile(r"\b[A-Z0-9_]*PORT[A-Z0-9_]*\s*[:=]\s*[\"']?(?P<port>\d{2,5})[\"']?", re.IGNORECASE)),
    ("docker-map", re.compile(r"(?<![\d.])(?P<port>\d{2,5})\s*:\s*\d{1,5}(?![\d.])")),
    ("listen", re.compile(r"\b(?:listen|bind|address)\b[^#\n;]*(?::|\s)(?P<port>\d{2,5})\b", re.IGNORECASE)),
)


def scan_path(
    root: Path | str,
    *,
    include_hidden: bool = False,
    max_size: int = 256_000,
    extra_extensions: Iterable[str] = (),
) -> ScanReport:
    scan_root = Path(root).resolve()
    report = ScanReport(root=scan_root)
    extensions = DEFAULT_EXTENSIONS | {ext if ext.startswith(".") else f".{ext}" for ext in extra_extensions}

    for file_path in iter_candidate_files(scan_root, include_hidden=include_hidden, extensions=extensions):
        try:
            if file_path.stat().st_size > max_size:
                report.skipped.append(file_path)
                continue
            text = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            report.skipped.append(file_path)
            continue

        report.files_scanned += 1
        report.hits.extend(extract_ports(text, file_path.relative_to(scan_root)))

    return report


def iter_candidate_files(root: Path, *, include_hidden: bool, extensions: set[str]) -> Iterable[Path]:
    if root.is_file():
        yield root
        return

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if should_ignore(path, root, include_hidden=include_hidden):
            continue
        if path.name in DEFAULT_FILENAMES or path.name.startswith(".env") or path.suffix in extensions:
            yield path


def should_ignore(path: Path, root: Path, *, include_hidden: bool) -> bool:
    relative_parts = path.relative_to(root).parts
    for part in relative_parts[:-1]:
        if part in DEFAULT_IGNORE_DIRS:
            return True
        if part.startswith(".") and not include_hidden:
            return True
    if path.name.startswith(".env"):
        return False
    return path.name.startswith(".") and not include_hidden


def extract_ports(text: str, relative_file: Path) -> list[PortHit]:
    hits: list[PortHit] = []
    seen: set[tuple[int, int, str]] = set()

    for line_number, line in enumerate(text.splitlines(), start=1):
        for source, pattern in PATTERNS:
            for match in pattern.finditer(line):
                port = int(match.group("port"))
                if not is_valid_port(port):
                    continue
                key = (line_number, match.start("port"), source)
                if key in seen:
                    continue
                seen.add(key)
                hits.append(
                    PortHit(
                        port=port,
                        file=relative_file,
                        line=line_number,
                        column=match.start("port") + 1,
                        source=source,
                        context=line.strip(),
                    )
                )

    return hits


def is_valid_port(port: int) -> bool:
    return 1 <= port <= 65535
