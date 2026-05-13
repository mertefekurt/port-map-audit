from unittest import TestCase

from port_map_audit.cli import should_fail
from port_map_audit.models import AuditResult, PortFinding, PortHit


class CliTests(TestCase):
    def test_fail_policy_respects_selected_level(self) -> None:
        hit = PortHit(
            port=5432,
            file="compose.yml",
            line=1,
            column=1,
            source="docker-map",
            context="5432:5432",
        )
        result = AuditResult(
            root=".",
            files_scanned=1,
            hits=(hit,),
            findings=(PortFinding(port=5432, level="risk", reason="postgres default port", hits=(hit,)),),
        )

        self.assertFalse(should_fail(result, "conflict"))
        self.assertTrue(should_fail(result, "risk"))
