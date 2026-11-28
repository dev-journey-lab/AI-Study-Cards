import glob
import os
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import verify_ai_guardrails as guardrails  # noqa: E402


class TestGuardrails(unittest.TestCase):
    def test_valid_topic_allowed(self):
        for topic in ["git", "api", "react", "security", "mcp"]:
            ok, _ = guardrails.validate_topic(topic)
            self.assertTrue(ok, f"Expected valid topic {topic!r} to pass")

    def test_invalid_topics_rejected(self):
        for bad in [["git"], {"topic": "git"}, "", "../.env", "git; rm -rf /", "a" * 51, None]:
            ok, _ = guardrails.validate_topic(bad)
            self.assertFalse(ok, f"Expected invalid topic {bad!r} to be rejected")

    def test_readonly_path_bounds(self):
        ok, _ = guardrails.validate_readonly_path(ROOT, "index.html")
        self.assertTrue(ok)
        for bad in ["../.env", ".env", "/etc/passwd", "sub/../../secret.txt", ["index.html"], ""]:
            ok, _ = guardrails.validate_readonly_path(ROOT, bad)
            self.assertFalse(ok, f"Expected unsafe path {bad!r} to be rejected")

    def test_output_secret_redaction(self):
        leaked = "Token sk-live-1234567890abcdef and Bearer eyJhbGciOiJIUzI1NiJ9"
        cleaned = guardrails.redact_output(leaked)
        self.assertNotIn("sk-live-", cleaned)
        self.assertNotIn("eyJhbGci", cleaned)
        self.assertEqual(cleaned.count("[REDACTED_SECRET]"), 2)


class TestStudyCardsSite(unittest.TestCase):
    def test_all_html_pages_and_internal_links(self):
        html_files = sorted(glob.glob(str(ROOT / "*.html")))
        self.assertEqual(len(html_files), 10, f"Unexpected HTML page count: {html_files}")
        for path_str in html_files:
            content = Path(path_str).read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", content, path_str)
            self.assertIn("</html>", content, path_str)
            for href in re.findall(r'href="([^"]+\.html)"', content):
                self.assertTrue((ROOT / href).exists(), f"Broken href {href} in {path_str}")

    def test_all_study_pages_use_hardened_storage_and_sync_with_index(self):
        index_text = (ROOT / "index.html").read_text(encoding="utf-8")
        study_pages = [
            p for p in sorted(ROOT.glob("*.html")) if p.name != "index.html"
        ]
        for page in study_pages:
            text = page.read_text(encoding="utf-8")
            self.assertIn("readJsonMap(", text, page.name)
            self.assertIn("saveCardStatus(", text, page.name)
            self.assertIn("saveUnitDone(", text, page.name)
            self.assertNotIn("saveProgress(", text, page.name)
            m_card = re.search(r'STORAGE_KEY\s*=\s*"([^"]+)"', text)
            m_unit = re.search(r'UNIT_STORAGE_KEY\s*=\s*"([^"]+)"', text)
            self.assertIsNotNone(m_card, page.name)
            self.assertIsNotNone(m_unit, page.name)
            self.assertIn(m_card.group(1), index_text, f"{m_card.group(1)} missing from index.html")
            self.assertIn(m_unit.group(1), index_text, f"{m_unit.group(1)} missing from index.html")


if __name__ == "__main__":
    unittest.main()
