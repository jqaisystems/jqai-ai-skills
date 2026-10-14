# Backup readiness: fictional proof

Example Studio provides a version-1 evidence pack for sample-project. It is metadata, not an actual backup.

Run the packaged [example](../../skills/backup-readiness-auditor/assets/example-evidence.json):

```bash
python skills/backup-readiness-auditor/scripts/audit_backup.py --input skills/backup-readiness-auditor/assets/example-evidence.json --as-of 2026-10-14T12:00:00Z --json
```

Expected result: EVIDENCE_COMPLETE, one record, no reasons, independently_verified false, destructive_action_authorized false.

| Changed synthetic evidence | Result | Meaning |
|---|---|---|
| Required second dataset has no row | BLOCKED | Missing scope is not an approved exclusion. |
| Hash mismatches despite equal counts | BLOCKED | Counts and sizes do not establish integrity. |
| Evidence is older than the chosen freshness window | REVIEW | Old evidence cannot establish current readiness. |
| Restore test has not run | REVIEW | Recovery remains unverified; do not run a restore without permission. |
| Duplicate IDs, extra fields, or invalid counts | Input error | Repair the evidence pack rather than guessing. |

Even a complete pack does not justify retiring the original. Independent recovery acceptance and separate authorization remain necessary. The helper leaves input bytes unchanged and never opens source or destination datasets.
