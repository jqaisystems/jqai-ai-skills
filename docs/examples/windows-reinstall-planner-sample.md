# Windows Reinstall Planner: Fictional Inventory

This sample uses synthetic evidence only. No machine inventory was collected during development.

| Evidence ID | Source | Name | Version | Publisher | Meaning |
|---|---|---|---|---|---|
| SW-00001 | registry-user | Example Editor | 1.01 | Example Studio | Registered, runtime unverified |
| SW-00002 | registry-machine | Example Editor | 2.00 | Example Studio | Same display group; retain both versions |
| SW-00003 | start-menu | Example Editor | unknown | unknown | Separate uncertain shortcut record |
| SW-00004 | registry-user | Crème Sketch | unknown | Example Studio | Unknown version stays blank in CSV |

Coverage: Registry complete with three records, StartMenu complete with one record, Store unavailable with zero records. Unavailable collection is not proof of no Store apps.

Given a schema-compatible synthetic inventory:

```text
python scripts/build_reinstall_plan.py --input sample-inventory.json --output-dir private-plan
```

Expected artifacts:

- `software-inventory.csv` retains all four evidence rows with Undecided and Not started.
- `reinstall-checklist.md` creates three conservative display groups and links their evidence IDs.
- `coverage-report.md` exposes Store collection failure and unverified runtime state.

No licence values, configuration files, browser profiles, install paths, or discovered commands are included. Formula-like CSV cells receive an apostrophe prefix. Reports refuse overwrite; regeneration into a new folder does not silently carry over manually edited decisions.

Before actual maintenance, separately verify file/settings backups and human reinstall choices. This skill never installs, removes, or formats anything.
