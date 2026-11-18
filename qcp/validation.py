"""Validate QCP documents against their published JSON Schema."""

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

DEFAULT_SCHEMA = Path(__file__).resolve().parents[1] / "schema" / "qcp-v0.1.schema.json"


def load_schema(path: Path = DEFAULT_SCHEMA) -> dict[str, Any]:
    """Load a local JSON Schema and check that the schema itself is valid."""
    schema = json.loads(Path(path).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def validate_qcp(document: Any, schema: dict[str, Any]) -> list[dict[str, str]]:
    """Return machine-readable validation errors (empty list means valid).

    JSON Pointer paths follow RFC 6901. Format checking is explicitly enabled,
    so invalid RFC 3339 timestamps fail validation rather than being ignored.
    """
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(document),
        key=lambda error: (tuple(str(part) for part in error.absolute_path), error.message),
    )
    return [
        {
            "path": "".join(
                "/" + str(part).replace("~", "~0").replace("/", "~1")
                for part in error.absolute_path
            ),
            "keyword": str(error.validator),
            "message": error.message,
        }
        for error in errors
    ]
