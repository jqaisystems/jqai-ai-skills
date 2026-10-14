# Offline Reconciliation: Fictional Review

Example Studio compares two approved, normalized snapshots using schema version 1. In this fictional case both were captured within the accepted 24-hour window, have complete agreed-scope coverage, and compare `status` and `title`.

| Record | Source/local evidence | Classification | Review |
|---|---|---|---|
| sample-001 | Same ID, values, and content hash | unchanged | No proposed repair |
| sample-002 | Source-only, no receipt | new | Review whether to add locally |
| sample-003 | Same ID, changed title | changed | Compare authoritative evidence |
| sample-004 | Distinct ID sharing a supplied content hash | duplicate | Confirm identity; never merge automatically |
| sample-005 | Local-only; historical published receipt | missing-from-source | Retain delivery history, investigate absence |
| sample-006 | Repeated ID or conflicting latest receipts | ambiguous | Resolve identity or evidence first |

If source coverage is incomplete or expired, sample-005 becomes ambiguous, not a removal candidate. An orphan receipt for a source-only item also makes it ambiguous before duplicate classification. A later failed receipt does not erase earlier published history.

```text
python scripts/reconcile_snapshots.py --source source.json --local local.json --receipts receipts.json --json
```

The report sets `mutations_performed: false`. Exit 1 requests review; it is not permission to execute a repair. Empty but incomplete snapshots also require review. Input files are unchanged and the helper has no live connector.

## Repair-plan excerpt

Proposed action: investigate sample-005 against a fresh, complete scoped export. Preserve its local record and all receipt history. Before any separately authorized implementation, record the specific change, backup, dry-run, approval, and verification evidence. No delete, reschedule, or resend action is authorized by this report.

Actual snapshots, IDs, receipts, and generated plans stay private.
