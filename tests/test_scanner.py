from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from port_map_audit.analyzer import analyze_hits
from port_map_audit.scanner import extract_ports, scan_path


class ScannerTests(TestCase):
    def test_extracts_ports_from_common_config_shapes(self) -> None:
        text = "\n".join(
            [
                "APP_PORT=8080",
                "api: http://localhost:8080/health",
                'ports: ["9090:80"]',
                "listen 127.0.0.1:443;",
            ]
        )

        hits = extract_ports(text, Path("compose.yml"))

        self.assertEqual([hit.port for hit in hits], [8080, 8080, 9090, 443])
        self.assertEqual(hits[0].source, "assignment")

    def test_scan_detects_conflicts_across_files(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docker-compose.yml").write_text('ports: ["8080:80"]\n', encoding="utf-8")
            (root / ".env").write_text("WEB_PORT=8080\n", encoding="utf-8")

            result = analyze_hits(scan_path(root))

            self.assertTrue(result.has_conflicts)
            self.assertEqual(result.findings[0].port, 8080)

    def test_scan_skips_ignored_directories(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ignored = root / "node_modules"
            ignored.mkdir()
            (ignored / "package.json").write_text('{"port": 3000}\n', encoding="utf-8")
            (root / "service.env").write_text("PORT=3001\n", encoding="utf-8")

            report = scan_path(root)

            self.assertEqual([hit.port for hit in report.hits], [3001])
