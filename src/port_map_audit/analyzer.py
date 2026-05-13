from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .models import AuditResult, PortFinding, PortHit, ScanReport

PRIVILEGED_LIMIT = 1024
COMMON_INFRA_PORTS = {
    3306: "mysql default port",
    5432: "postgres default port",
    6379: "redis default port",
    9200: "elasticsearch default port",
    11211: "memcached default port",
    27017: "mongodb default port",
}


def analyze_hits(report: ScanReport) -> AuditResult:
    by_port: dict[int, list[PortHit]] = defaultdict(list)
    for hit in report.hits:
        by_port[hit.port].append(hit)

    findings: list[PortFinding] = []
    for port, hits in sorted(by_port.items()):
        unique_files = {hit.file for hit in hits}
        unique_contexts = {hit.context for hit in hits}

        if len(unique_files) > 1 or len(unique_contexts) > 1:
            findings.append(
                PortFinding(
                    port=port,
                    level="conflict",
                    reason="port appears in multiple files or contexts",
                    hits=tuple(hits),
                )
            )
            continue

        if port < PRIVILEGED_LIMIT:
            findings.append(
                PortFinding(
                    port=port,
                    level="risk",
                    reason="privileged port usually requires elevated permissions",
                    hits=tuple(hits),
                )
            )
            continue

        if port in COMMON_INFRA_PORTS:
            findings.append(
                PortFinding(
                    port=port,
                    level="risk",
                    reason=COMMON_INFRA_PORTS[port],
                    hits=tuple(hits),
                )
            )

    return AuditResult(
        root=Path(report.root),
        files_scanned=report.files_scanned,
        hits=tuple(sorted(report.hits, key=lambda hit: (hit.port, str(hit.file), hit.line))),
        findings=tuple(findings),
    )
