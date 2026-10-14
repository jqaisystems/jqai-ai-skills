# Inventory Contract and Coverage

## Version 1

The collector emits `schema_version: 1`, a timezone-aware `captured_at`, `coverage`, and `records`.

Every record has string fields:

| Field | Purpose |
|---|---|
| record_id | Unique evidence reference within this inventory |
| source | registry-machine, registry-machine-32, registry-user, store-current-user, or start-menu |
| name | Source-reported display name |
| version | Source-reported version, blank when unknown |
| publisher | Source-reported publisher, not independently verified |
| package_id | Store package family identifier when available |
| evidence | registered or shortcut-only |

Coverage accounts for `Registry`, `Store`, and `StartMenu`, each with `complete` or `unavailable` and its record count. Counts must reconcile to records. Adapter failure is visible; missing collection is not an empty successful inventory.

No install paths, user identifiers, uninstall commands, or application configuration contents are included. The collector does not execute discovered applications or follow their shortcuts.

Use a private local disk for input and output. UNC and linked input/output paths are refused. Network-mounted locations are outside this offline workflow.

## Grouping and decisions

Group matching package IDs, or exact normalized names and publishers when package IDs are absent. Retain every source row and version. Uncertain aliases, missing publishers, and different publishers are not guessed into one application.

Output files:

- `software-inventory.csv`: all source rows plus Undecided reinstall choice and Not started completion status.
- `reinstall-checklist.md`: display groups linked to original record IDs.
- `coverage-report.md`: collection status, counts, and limitations.

CSV cells that could be interpreted as formulas are prefixed with an apostrophe. Import version and identifier columns as text. Human edits are not read back by the builder; regenerating into a new folder does not preserve edited decisions automatically.

## Exclusions and sources

Other user profiles, arbitrary portable folders, drivers, browser extensions, remote environments, and package-manager environments are outside this collector's coverage. Do not infer absence from these omissions.

- [Microsoft: querying uninstall registry keys and installer query risks](https://learn.microsoft.com/en-us/powershell/scripting/samples/working-with-software-installations)
- [Microsoft: current-user Store package collection](https://learn.microsoft.com/en-us/powershell/module/appx/get-appxpackage)

Prefer publisher-owned download pages when enriching selected entries. Date link reviews, distinguish verified links from suggestions, and never treat an old installed version as a recommendation.
