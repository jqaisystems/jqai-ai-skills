# Evidence contract, version 1

The helper accepts a single UTF-8 JSON object of at most 1 MiB. Python 3.11 or newer is required, with no packages or network access. Input must be a local, ordinary file with no linked/reparse path components. No other path is opened. Unknown fields and duplicate JSON keys are rejected so operational exports are not silently accepted.

Top-level fields:

- `version`: integer 1.
- `scope_complete`: true, false, or null. True means the human has explicitly accounted for the full intended scope, including any approved exclusions. False/null requires review.
- `required_ids`: nonempty, unique list of fictional or private dataset IDs.
- `destination`: `independent` (boolean/null), `free_bytes`, `remaining_bytes`, and `reserve_bytes` (nonnegative integers). Remaining bytes means work still required, not the size already stored. These are supplied measurements, not live disk checks.
- `records`: evidence rows, each with the fields shown in the fictional [example pack](../assets/example-evidence.json). Dataset IDs use 1-64 lowercase letters, digits, or hyphens; do not use names or paths.

Each row has a timezone-aware `captured_at`, nonnegative integer counts, `snapshot_consistent` (boolean/null), and `restore_test` (`passed`, `failed`, or `not_run`). A count of zero is an explicit assertion, not a substitute for unknown measurement. If counts are unknown, omit that dataset's row and explain the gap in the private report. Duplicate IDs or impossible verified counts invalidate the pack.

The supplied evidence timestamp should describe the actual verification, not the report-writing date. Use `--as-of` for a reproducible cutoff and `--max-age-days` for an explicitly chosen freshness window (default 7). Stale or future-dated evidence cannot pass. The helper cannot detect a dishonest timestamp or later source changes absent from the pack.

Known failures block: insufficient remaining capacity including reserve, non-independent destination, missing required row, mismatches, read errors, cloud-only items, unresolved links, incomplete verification counts, inconsistent snapshot, or failed restore test. Unknown independence/consistency, incomplete scope, missing restore test, and stale/future evidence require review. Extra records remain visible and are evaluated too.

Matching hashes concern integrity for the measured snapshot, not ongoing freshness. A restore test must be a separately authorized isolated test; never initiate one merely to satisfy this report. File metadata and cloud placeholders alone do not prove local file contents are available.

Exit codes: 0 = evidence complete, 1 = blocked/review, 2 = invalid or unreadable input. Output includes only validated IDs, reason codes, counts, and the cutoff, not source text or host paths. It remains private operational evidence.
