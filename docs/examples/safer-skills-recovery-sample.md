# Safer skill maintenance: fictional proof

Example Studio has one public skill copy, one locally edited copy, and a shared link.

| Action | Expected outcome |
|---|---|
| Dry-run a missing destination | Plan only; no folder created. |
| Install into a fresh private test target | Complete copy plus content-hash receipt. |
| Repeat without source changes | Unchanged; no replacement. |
| Upgrade an unchanged managed copy with explicit replace | New copy installed; prior copy retained as a unique sibling backup. |
| Upgrade a locally edited or unmanaged copy | Stop; preserve original. |
| Encounter a correct, conflicting, or broken link | Stop; do not repair or replace the link. |
| Copy fails before swap | Original remains intact; staging retained for private review. |

The same safety core is invoked by PowerShell and Bash. Do not run installers concurrently against the same target.

Scanner proof uses a synthetic access-like value generated only inside a disposable test. Text and JSON reports identify the finding type and relative location, but never repeat that value. The baseline file is scanned too, and a forged baseline cannot suppress blocking findings. A protected junction root is never followed to read its baseline.

Relative filenames can still disclose project information. Keep reports and install receipts private. These tests establish local behavior, not a guarantee that every possible sensitive pattern is detected.
