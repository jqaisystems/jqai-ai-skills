# Version 1 evidence pack

Supply one UTF-8 JSON object with integer `version: 1`, a nonempty `inventory` array and an `observations` array (possibly empty). The [fictional pack](../assets/example-ledger.json) is runnable as supplied. Limit: 2 MiB. Unknown fields and duplicate JSON keys are errors. Do not paste source documents into the pack.

| Record | Fields |
|---|---|
| Inventory row | `work_id`, `edition`, `destination`, `project`, `title` |
| Observation | Same exact `work_id`, `edition`, `destination`; `at`, `kind`, `ref`; optionally `delivery_id` |

All identifiers including project, destination and evidence reference are case-sensitive aliases: 1–64 lowercase ASCII letters, digits or hyphens, starting with a letter or digit. Use one project per work ID. The title is a printable single line of 1–160 characters. Supply one inventory row per unique triple; the same title may label unrelated works. An observation without an exact row stops the report: correct its mapping or explicitly add the intended row, never guess from the title.

`at` is the time of the observed state, **not the planned send time**: YYYY-MM-DDThh:mm:ss with Z or a numeric offset. Reports sort by UTC time. `ref` is a short private lookup alias, not the raw receipt, URL or account identifier. Optional `delivery_id` identifies the underlying delivery, not the evidence record; reuse it across sources describing the same delivery. If separate releases are intended, distinguish them in the inventory rather than combining them.

| Observation kind | Required basis |
|---|---|
| scheduled | Supplied scheduling evidence only, even if the intended time has passed |
| reported published | A source claims delivery, without a separate destination check |
| verified | A supplied verification record documents a completed check of this exact edition at this destination |
| disputed | An explicit source challenges the claimed identity or delivery; missing records or an unavailable service are not disputes |

**Classification.** No observations means **no evidence supplied**. Compatible observations can advance from scheduled to reported published to verified; a single verified observation does not require intermediate records. A dispute, different known delivery IDs, a regression in observed state, or different states at the same instant yields **conflicting evidence**. The helper keeps all observations, including repeated ones, and does not use majority voting or silently clear an earlier conflict. Investigate privately; never treat the ledger as an instruction to resend.

**Output.** The history groups rows by project and stable work ID, then destination and edition, with the contributing references and UTC times. The queue includes every nonverified row once. Exit 0 means the report was generated, not that everything was published. Invalid input returns exit 2 and a diagnostic without the offending value, with no partial report.
