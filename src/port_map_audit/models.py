from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class PortHit:
    port: int
    file: Path
    line: int
    column: int
    source: str
    context: str

    @property
    def location(self) -> str:
        return f"{self.file}:{self.line}:{self.column}"


@dataclass(frozen=True)
class PortFinding:
    port: int
    level: str
    reason: str
    hits: tuple[PortHit, ...]


@dataclass
class ScanReport:
    root: Path
    files_scanned: int = 0
    hits: list[PortHit] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)


@dataclass(frozen=True)
class AuditResult:
    root: Path
    files_scanned: int
    hits: tuple[PortHit, ...]
    findings: tuple[PortFinding, ...]

    @property
    def has_conflicts(self) -> bool:
        return any(finding.level == "conflict" for finding in self.findings)

    @property
    def has_risks(self) -> bool:
        return any(finding.level in {"conflict", "risk"} for finding in self.findings)
