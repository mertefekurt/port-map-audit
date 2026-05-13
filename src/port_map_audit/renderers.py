from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import AuditResult, PortFinding, PortHit


def render_table(result: AuditResult) -> str:
    lines = [
        "port-map-audit",
        f"root: {result.root}",
        f"files scanned: {result.files_scanned}",
        f"ports found: {len(result.hits)}",
        "",
    ]

    if not result.findings:
        lines.append("status: no conflicts or risky bindings found")
        return "\n".join(lines)

    rows = [
        ("PORT", "LEVEL", "REASON", "LOCATIONS"),
        *[
            (
                str(finding.port),
                finding.level,
                finding.reason,
                ", ".join(hit.location for hit in finding.hits[:3]),
            )
            for finding in result.findings
        ],
    ]
    widths = [max(len(row[index]) for row in rows) for index in range(4)]

    for index, row in enumerate(rows):
        lines.append("  ".join(value.ljust(widths[col]) for col, value in enumerate(row)))
        if index == 0:
            lines.append("  ".join("-" * width for width in widths))

    return "\n".join(lines)


def render_json(result: AuditResult) -> str:
    payload = {
        "root": str(result.root),
        "files_scanned": result.files_scanned,
        "hits": [serialize_hit(hit) for hit in result.hits],
        "findings": [serialize_finding(finding) for finding in result.findings],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def serialize_hit(hit: PortHit) -> dict[str, object]:
    data = asdict(hit)
    data["file"] = str(Path(hit.file))
    return data


def serialize_finding(finding: PortFinding) -> dict[str, object]:
    return {
        "port": finding.port,
        "level": finding.level,
        "reason": finding.reason,
        "hits": [serialize_hit(hit) for hit in finding.hits],
    }
