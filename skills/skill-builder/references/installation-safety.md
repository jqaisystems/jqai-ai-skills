# Installation and shared-source safety

Inventory source and destinations, including dangling links, before writing. Record actual paths and hashes privately.

Classify destinations as absent, matching copy, locally modified copy, correct link, broken link, or conflicting target. Inspect links without following their contents first. Preserve correct links; a broken link is not an absent destination.

The repository installers are conservative copy tools, not link repair tools:

- Python 3.11+ is required; no packages are installed automatically.
- `-DryRun` / `--dry-run` preflights the entire selection without creating folders.
- Fresh installs write a content-hash receipt. A matching managed copy is unchanged on rerun.
- `-Replace` / `--replace` upgrades only a managed copy that still matches its receipt. The old folder is retained beside it under a unique backup name.
- Unmanaged folders, local changes, links, reparse components, network targets, and repository/target overlap stop installation. A receipt detects changes; it is not proof of authorship.
- Legacy copies without receipts need manual review or a new destination. Never fabricate a receipt to bypass protection.
- Runtime failures can leave an earlier selected skill installed and a staging folder retained. Inspect before retrying. Concurrent changes to the same target are unsupported.

For explicitly requested link restoration, compare source hashes to the approved source, check destination absence including dangling links, preserve correct links, and stop on conflicts. Create only missing approved links, then verify their targets and SKILL.md. Never use recursive deletion to repair links, or change execution policies or elevation settings to force success.

Keep operational receipts, backups, staging folders, and reports private. Cleanup is a separate approved action.
