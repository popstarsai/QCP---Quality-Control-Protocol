# QCP — Quality Content Protocol

QCP is an early, open, JSON-based protocol for creators and AI agents to declare source-media quality, preferred upload settings, and expectations about platform processing. It can describe the intended quality of a video; **a valid QCP document does not, by itself, prove that the media has that quality or that a platform preserved it**.

## Status

**v0.1 (experimental).** The published v0.1 schema remains permissive to support early experimentation. Fields and semantics for independent quality measurements are under discussion.

## Quick start

1. Read [`schema/qcp-v0.1.schema.json`](schema/qcp-v0.1.schema.json).
2. Copy [`examples/basic-video.json`](examples/basic-video.json), replacing its example identifiers and values with your own.
3. Install and run the reference validator (Python 3.11+):

```sh
python -m pip install -r requirements-dev.txt
python -m qcp examples/basic-video.json
python -m qcp --json examples/basic-video.json
```

The CLI accepts multiple documents and an optional `--schema PATH`. It exits with `0` when all documents validate, `1` for invalid or unreadable documents, and `2` for schema setup errors. The `--json` output is intended for automation and future MCP tools. Validation includes RFC 3339 `date-time` format checks.

4. Publish your QCP document alongside your media, in a repository, or through a registry. No centralized registry is required.

## What QCP v0.1 describes

- `content_id`: creator-supplied identifier, preferably linked to the original media
- `original`: source properties such as codec, resolution, frame rate, and bitrate
- `expected_processing`: anticipated platform processing and upload guidance
- `quality_claims`: optional claims, **not independently verified by the validator**
- `timestamp`: document timestamp

Schema validation checks the document's shape, types, required fields, and declared formats. It does **not** inspect video bytes, recompute checksums, verify signatures, test upload compatibility, or measure transcoding quality. The example checksum is intentionally a placeholder and is not proof of file integrity.

## Platform notes

- [X / Twitter](docs/platforms/x.md) — initial community-maintained observations, not platform guarantees

Upload policies depend on account, upload surface, location, and date. Treat platform guidance as time-sensitive and provide sources when proposing changes.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Particularly useful contributions: additional platform notes with dated evidence, measurements comparing source and delivered files, and additive proposals for QCP v0.2.

## License

[MIT](LICENSE)
