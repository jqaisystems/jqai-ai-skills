# Approval packages and publication evidence

Use one package per provider, destination and scheduled time. Ordered posts may represent a thread or sequence. Changing any copy, title, media bytes, relative path, alt text, order, role, destination, provider or time changes its fingerprint.

## Local auditor

    python scripts/audit_campaign_package.py --package package.json --approval approval.json --receipts receipts.json --json

Approval and receipts are optional. Python 3.11+, standard library only. The helper reads supplied local records and relative media files; it writes nothing and makes no network calls. JSON records are limited to 1 MiB, packages to 100 posts and 100 media per post, receipt sets to 1000 records. Links/reparse points, network paths, escaping media paths, and non-media extensions are refused.

Exit codes: 0 means matching approval evidence with no unresolved audit finding; 2 means review is required; 1 means invalid/unreadable input. None authorizes external action.

A version 1 package has exactly schema_version, provider, destination, scheduled_at (null or an offset-aware ISO timestamp), and posts. Each post has copy, title, and ordered media. Each media item has path, role, and alt_text. Empty alt text is a review finding. Paths are relative to the package file. No path, copy, media content, account identifier, or raw decoder diagnostic is emitted by the auditor.

The fingerprint is SHA-256 of canonical JSON with sorted keys, compact separators and ASCII escapes, augmenting each media item with its measured sha256 and size. List order and exact strings are preserved. This is change detection, not a digital signature. Freeze controlled local files and re-audit immediately before any separately approved external step.

Approval version 1 has schema_version, fingerprint, decision (approved/rejected), and approved_at. A matching record is supplied evidence, not independently authenticated consent. The helper never creates an approval record. Only record an actual human decision for the exact package.

Receipt version 1 has schema_version and records. Every record has provider, destination, fingerprint, state, observed_at, and receipt_id. The receipt_id identifies one delivery across its observed state progression. Preserve the original evidence privately; this minimal projection does not replace it.

## State interpretation

| State | Meaning |
| --- | --- |
| prepared | A package exists without matching approval evidence. |
| approved | An approval record matches; human consent was not independently authenticated. |
| scheduled | Supplied matching evidence reports a scheduled item. |
| published | Supplied matching evidence reports publication. |
| verified | Supplied matching evidence reports a completed verification; this auditor did not perform it. |
| failed | Matching evidence reports failure; retry still requires reconciliation. |
| uncertain | Identity conflicts, conflicting states, duplicate delivery evidence, future observations, or uncertain results need investigation. |

Normal scheduled -> published -> verified observations for the same delivery can coexist. Different delivery identities, state regressions, or contradictory observations require review. A receipt for a changed fingerprint or another provider/destination does not prove this package was delivered.

A missing record, empty receipt set, unavailable queue, or scheduler view that omits a native-platform queue never proves cancellation. Preserve provider distinctions. Do not delete, cancel or retry based on text similarity or missing evidence.

Old scheduled times are not instructions to post now. Use explicit offsets and review timezone/DST intent before approval. Unknown metrics remain unknown, not zero. Missing platform alt-text controls must be reported, not described as successful uploads.

Keep reports private by default. No connector, scheduling, cancellation, retry or automatic publishing is implemented.
