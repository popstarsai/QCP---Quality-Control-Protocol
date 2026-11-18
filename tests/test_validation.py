"""Conformance tests for the v0.1 reference validator."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from qcp import DEFAULT_SCHEMA, load_schema, validate_qcp

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "basic-video.json"


class QCPValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load_schema(DEFAULT_SCHEMA)
        cls.example = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_published_example_is_valid(self):
        self.assertEqual(validate_qcp(self.example, self.schema), [])

    def test_wrong_protocol_version_is_rejected(self):
        document = {**self.example, "qcp_version": "0.2"}
        self.assertTrue(any(e["path"] == "/qcp_version" for e in validate_qcp(document, self.schema)))

    def test_missing_original_is_rejected(self):
        document = {key: value for key, value in self.example.items() if key != "original"}
        self.assertTrue(any(e["keyword"] == "required" for e in validate_qcp(document, self.schema)))

    def test_invalid_timestamp_is_rejected(self):
        document = {**self.example, "timestamp": "not-a-date"}
        self.assertTrue(any(e["keyword"] == "format" for e in validate_qcp(document, self.schema)))

    def test_extension_fields_are_allowed_in_v01(self):
        document = {**self.example, "x_custom_metadata": {"source": "camera"}}
        self.assertEqual(validate_qcp(document, self.schema), [])

    def test_json_cli_success(self):
        proc = subprocess.run(
            [sys.executable, "-m", "qcp", "--json", str(EXAMPLE)],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(json.loads(proc.stdout)["valid"])

    def test_json_cli_rejects_invalid_document(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"qcp_version": "0.1"}', encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "qcp", "--json", str(path)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(proc.returncode, 1, proc.stderr)
            self.assertFalse(json.loads(proc.stdout)["valid"])

    def test_malformed_json_is_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{bad", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "qcp", "--json", str(path)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(json.loads(proc.stdout)["documents"][0]["errors"][0]["keyword"], "parse")


if __name__ == "__main__":
    unittest.main()
