# Media Spec Checker: Fictional Delivery

Example Studio supplies local files and a version 1 rule profile. This sample is an output shape, not a claim about a platform's current upload requirements.

```json
{"schema_version":1,"image":{"formats":["png"],"width":{"min":80,"max":80},"height":{"min":40,"max":40},"max_bytes":50000,"animated":false}}
```

Run from the installed skill folder:

```text
python scripts/check_media.py sample-project --rules sample-rules.json --json
```

| Fictional input | Evidence | Result |
|---|---|---|
| sample.png | 80 by 40, static PNG, below size limit | pass |
| wide.png | 100 by 40 | fail: width exceeds 80 |
| damaged.png | Image cannot be inspected | unverified, not pass |

For this three-file case, counts are one pass, one fail, one unverified, `has_unverified` is true, and exit status is 2. A separate valid H.264 video can be measured using local ffprobe and a supplied video section. Missing ffprobe or a timeout yields unverified measurements, never success.

An image with a width failure and unknown duration retains both facts: file status fail, an unverified duration check, and exit 2. Originals are not converted, uploaded, or edited. Reports omit absolute input roots but relative filenames can still be private.

The automated tests generate synthetic files and compare input hashes. See [verification scope](v0.12.0-verification.md).
