# Rules Contract, Version 1

The top-level object contains `schema_version: 1` and an `image` section, a `video` section, or both. Unknown keys and empty sections are rejected.

The [machine-readable schema](../assets/rules.schema.json) documents the structure. The bundled validator additionally checks finite bounds, min not exceeding max, and Python regular-expression syntax. No schema library or remote schema fetch is needed.

| Rule | Value | Meaning |
|---|---|---|
| formats | Nonempty list of names | Detected image format or an ffprobe container alias; not the filename extension |
| width, height | Object with min and/or max | Display-oriented pixel dimensions; bounds are inclusive |
| aspect_ratio | Object with min and/or max | Display width divided by display height, including video sample aspect ratio |
| duration | Object with min and/or max | Seconds; unavailable timing is unverified |
| max_bytes | Positive integer | Maximum file size in bytes |
| filename_pattern | Regex, at most 256 characters | Full match against the basename |
| animated | Boolean, images only | Whether the image contains more than one frame |
| codecs | Nonempty list, videos only | Main video codec name, for example h264 |

Use a narrow numerical interval for aspect-ratio tolerance. The example is a fictional delivery specification, not a platform preset. Rule files are trusted local configuration.

If ffprobe does not provide a usable sample aspect ratio, display aspect ratio is unverified rather than guessed to use square pixels. Other available measurements can still be checked.

## Supported routing

Images: PNG, JPEG, WebP, GIF, BMP, TIFF. Videos: MP4/M4V/MOV, WebM/MKV, AVI. One non-cover video stream is required. Container aliases reported by ffprobe may overlap; use `codecs` as well when that matters. Extension routing is conservative; an incorrectly named file may be unverified.

No URL input, network protocols, playlists, linked files, or linked directories are accepted. ffprobe receives an argument list, a local-protocol allowlist, a container allowlist, and a timeout. Its diagnostics are not copied into reports.

## Result

JSON has `schema_version`, file-level `counts`, per-rule `check_counts`, `has_unverified`, `files`, and `scope`. Each file includes a relative `file` identifier, `kind`, `status`, selected `measurements`, and per-rule `checks`. Status is `pass`, `fail`, or `unverified`. A file with both a failed and an unavailable check retains its failed status, while `has_unverified` and exit 2 expose the unknown check. No measurements are invented to satisfy a rule.

A pass means only the configured checks passed. Full decoding/playback and human review may still be needed.

## Sources

- [ffprobe output and stream documentation](https://ffmpeg.org/ffprobe.html)
- [Pillow image inspection](https://pillow.readthedocs.io/en/stable/reference/Image.html)
