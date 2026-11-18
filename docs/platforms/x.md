# X (Twitter) – Platform notes

X automatically re-encodes uploaded videos for adaptive streaming and bandwidth efficiency. Some detail loss is normal and expected.

Observed behavior (community-maintained, not official):
- Videos are re-processed after upload.
- Higher-quality source files (solid bitrate H.264, 1080p) generally fare better.
- There is currently no platform notification when re-encoding occurs or about the resulting quality drop.
- Premium accounts may have access to higher upload/playback options.

Recommended upload settings for better results:
- Codec: H.264
- Resolution: 1080p (where allowed)
- Use a solid/constant bitrate rather than very aggressive compression
- Export at a high enough bitrate so the platform has good material to work with

QCP usage tip: Record the original specs and preferred upload settings in the `original` and `expected_processing` fields so agents and tools can reference them later.