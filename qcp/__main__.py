"""Command line interface: python -m qcp [--json] document.json ..."""

import argparse
import json
import sys
from pathlib import Path

from jsonschema.exceptions import SchemaError

from .validation import DEFAULT_SCHEMA, load_schema, validate_qcp


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate QCP documents against JSON Schema v0.1")
    parser.add_argument("documents", nargs="+", type=Path, help="QCP JSON files to validate")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Local schema file")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results")
    args = parser.parse_args(argv)

    try:
        schema = load_schema(args.schema)
    except (OSError, UnicodeError, ValueError, SchemaError) as exc:
        # Schema setup failures are distinct from invalid QCP documents.
        print(f"Cannot load schema {args.schema}: {exc}", file=sys.stderr)
        return 2

    results = []
    for path in args.documents:
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
            errors = validate_qcp(document, schema)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors = [{"path": "", "keyword": "parse", "message": str(exc)}]
        results.append({"file": str(path), "valid": not errors, "errors": errors})

    valid = all(result["valid"] for result in results)
    if args.json:
        print(json.dumps({"valid": valid, "documents": results}, indent=2))
    else:
        for result in results:
            print(f"{'VALID' if result['valid'] else 'INVALID'} {result['file']}")
            for error in result["errors"]:
                print(f"  {error['path'] or '/'} [{error['keyword']}]: {error['message']}")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
