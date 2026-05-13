from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze_hits
from .renderers import render_json, render_table
from .scanner import scan_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="port-map-audit",
        description="Scan project config files for local port conflicts and risky bindings.",
    )
    parser.add_argument("path", nargs="?", default=".", help="project directory or single file to scan")
    parser.add_argument("--format", choices=("table", "json"), default="table", help="output format")
    parser.add_argument(
        "--fail-on",
        choices=("none", "risk", "conflict"),
        default="conflict",
        help="exit with code 1 when the selected finding level is present",
    )
    parser.add_argument("--include-hidden", action="store_true", help="include hidden folders and files")
    parser.add_argument("--max-size", type=int, default=256_000, help="maximum file size in bytes")
    parser.add_argument(
        "--extension",
        action="append",
        default=[],
        help="extra extension to include, repeatable",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    target = Path(args.path)

    if not target.exists():
        parser.error(f"path does not exist: {target}")

    report = scan_path(
        target,
        include_hidden=args.include_hidden,
        max_size=args.max_size,
        extra_extensions=args.extension,
    )
    result = analyze_hits(report)
    output = render_json(result) if args.format == "json" else render_table(result)
    print(output)

    if should_fail(result, args.fail_on):
        return 1
    return 0


def should_fail(result, fail_on: str) -> bool:
    if fail_on == "none":
        return False
    if fail_on == "risk":
        return result.has_risks
    return result.has_conflicts
