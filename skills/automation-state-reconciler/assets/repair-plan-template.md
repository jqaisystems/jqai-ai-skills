# Offline Reconciliation Repair Plan

System and agreed scope: <generic description>
Source of truth and evidence: <source, capture time, completeness>
Local evidence: <capture time, completeness>
Receipt evidence and limitations: <coverage or unavailable>
Freshness policy: <chosen window and reason>

## Findings

| ID | Classification | Changed fields / evidence | Proposed action | Approval needed |
|---|---|---|---|---|
| sample-001 | ambiguous | <missing evidence> | Refresh evidence; no mutation | <reviewer> |

## Recovery and Verification

- Preserve stable IDs, review decisions, scheduling evidence, and delivery history.
- Identify the application's supported backup and restore procedures.
- Verify a backup on a disposable copy before any later repair.
- List dependent exports, dashboards, and derived files that would need rebuilding.
- Define before/after counts and exact record-level assertions.
- Separate a code rollback from a data rollback.
- Record unresolved items and the authorized scope before execution.

Execution state: Plan only. No records, schedules, or external systems changed.
