# Offline Snapshot Contract, Version 1

Both source and local inputs are JSON objects with exactly these keys:

Keep inputs on a local disk. UNC paths and linked input files or directories are refused; do not use network-mounted drives for an offline review.

    {
      "schema_version": 1,
      "captured_at": "2026-01-01T12:00:00Z",
      "complete": true,
      "max_age_hours": 24,
      "compare_fields": ["status", "title"],
      "records": [
        {
          "id": "sample-001",
          "values": {"status": "ready", "title": "Example item"},
          "content_hash": "fictional-content-a"
        }
      ]
    }

Dates and values above are fictional. Use actual capture times and a task-appropriate age limit when exporting current private state. Timezones are required. Future-dated and expired snapshots need review.

`complete` describes coverage of the agreed scope, not collection success alone. A filtered export is not a complete source inventory. Both inputs must select the same top-level `compare_fields`. Additional values are rejected to minimize accidental disclosure. Missing selected values make the record ambiguous. No dotted-path inference or schema discovery occurs.

`content_hash` is optional and must use the same hashing method and content normalization across inputs. Example labels are not actual digests. Changed or missing hashes between matching IDs are reported as a change.

## Receipt input

    {
      "schema_version": 1,
      "records": [
        {"id": "sample-001", "status": "published", "observed_at": "2026-01-01T12:05:00Z"}
      ]
    }

Supported normalized receipt states: `scheduled`, `published`, `verified`, `failed`. Map a provider's states explicitly before export. The latest observation determines the reported state; simultaneous conflicting states or future timestamps are ambiguous. Any scheduling or delivery evidence protects history, even if a later attempt failed.

## Classifications

- `unchanged`: selected values and supplied hashes agree for the same ID.
- `new`: source-only ID, complete fresh local coverage, and no orphan receipt.
- `changed`: matching ID with changed selected values or hash.
- `duplicate`: matching supplied content hashes across distinct IDs.
- `missing-from-source`: local-only ID with complete fresh source coverage; this never produces a delete instruction.
- `ambiguous`: repeated IDs, missing fields, stale/future evidence, incomplete absence evidence, conflicting receipts, or orphan receipt history.

Ambiguity takes precedence over duplicate and difference classifications. All input history stays untouched. The report includes classification counts, per-record reasons, capture coverage, and `mutations_performed: false`. Values are not echoed, but IDs may still be sensitive.
