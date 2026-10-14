# Update After Release Proof

Use this page when you already installed one or more JQ AI Skills and want a public-safe proof trail for refreshing them after a new release.

The goal is simple: a visitor should be able to pull the latest repo, inspect what changed, test the skill copy in a temporary target, reinstall the selected skill, reload the tool, and run a fake first check before using the refreshed skill on real work.

This proof trail uses `github-safe-publisher` because it is the recommended first skill and it has a clear fake-file review path.

```text
pull latest release -> inspect changes -> test temporary copy -> reinstall selected skill -> reload -> run fake check
```

## What This Proves

| Step | Proof |
|---|---|
| Repo update is explicit | The visitor pulls with `git pull --ff-only` instead of mixing local edits with release updates. |
| Change review is visible | The changelog, announcement, and quality matrix can be inspected before reinstalling. |
| Reinstall is testable | The skill is copied into a disposable target before the normal tool target is touched. |
| Folder contract still holds | The refreshed folder still includes `SKILL.md`, metadata, references, and scripts where expected. |
| Reload is deliberate | The local AI coding tool is reloaded before the refreshed skill is used. |
| First check stays safe | The first post-update prompt uses the fake candidate pack, not private project material. |

## 1. Pull The Latest Repo

Work from the repo root.

Windows PowerShell:

```powershell
git status --short
git pull --ff-only
git tag --list "v0.7.*"
```

macOS/Linux:

```bash
git status --short
git pull --ff-only
git tag --list "v0.7.*"
```

If `git status --short` shows local edits, stop and decide whether to save them before pulling. Do not overwrite local changes just to update an installed skill.

## 2. Inspect What Changed

Open the release notes and proof pages before reinstalling:

- [`../../CHANGELOG.md`](../../CHANGELOG.md)
- [`../announcements/v0.7.2.md`](../announcements/v0.7.2.md)
- [`../skill-quality-matrix.md`](../skill-quality-matrix.md)
- [`../guides/update-installed-skills.md`](../guides/update-installed-skills.md)

Confirm that the update is relevant to the skill you plan to reinstall.

## 3. Test The Copy In A Temporary Target

Use a disposable target first.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher -Target "$env:TEMP\jqai-skill-update-check"
Test-Path "$env:TEMP\jqai-skill-update-check\github-safe-publisher\SKILL.md"
Get-ChildItem "$env:TEMP\jqai-skill-update-check\github-safe-publisher"
```

macOS/Linux:

```bash
chmod +x ./install.sh
./install.sh --target "${TMPDIR:-/tmp}/jqai-skill-update-check" github-safe-publisher
test -f "${TMPDIR:-/tmp}/jqai-skill-update-check/github-safe-publisher/SKILL.md"
ls "${TMPDIR:-/tmp}/jqai-skill-update-check/github-safe-publisher"
```

Expected folder contents for this skill:

```text
agents
references
scripts
SKILL.md
```

Compare with:

- [`install-smoke-test-sample.md`](install-smoke-test-sample.md)
- [`../guides/install-verification.md`](../guides/install-verification.md)

## 4. Upgrade The Selected Managed Copy

Follow the [current upgrade guide](../guides/update-installed-skills.md). Preview the explicit target with `-Replace -DryRun` or `--replace --dry-run`; remove the dry-run flag only after review. Identical copies are unchanged and old managed copies are retained as backups. Legacy copies, local edits, and shared links require a separate migration, not forced replacement.

## 5. Reload And Run A Fake Check

Restart or reload your AI coding tool so it can discover the refreshed skill folder.

Use the ready fictional candidate pack:

- [`first-skill-candidate/README.md`](first-skill-candidate/README.md)
- [`first-skill-candidate/expected-review.md`](first-skill-candidate/expected-review.md)

Prompt:

```text
Use $github-safe-publisher to review this fake README and docs folder before public release.
```

The first post-update check should use only the fake `Example Review Queue` candidate. Do not use account exports, raw logs, screenshots, unpublished notes, or real project files for this proof run.

## 6. Decide Pass, Review, Or Stop

| Result | Meaning | Next step |
|---|---|---|
| `PASS` | The temporary copy worked, the normal reinstall completed, and the fake review still returns the expected shape. | Keep the refreshed skill installed and use it on one small public-safe task. |
| `REVIEW` | The copy worked, but the refreshed skill is not visible after reload or the fake review is missing key sections. | Reload the tool, rerun with the fake candidate, and compare with the expected review. |
| `STOP` | The copied folder is incomplete, the update replaced local edits unexpectedly, or the first output skips the safety gate. | Use [`../../TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md) before using the refreshed skill. |

## 7. Clean Up The Temporary Target

Only remove the disposable target:

Inspect the exact absolute temporary target, confirm it is outside the repository and contains only this test, and check for links before a separately reviewed cleanup. No automatic removal is required.

Do not remove your normal skills directory unless you know what else is installed there.

## Related Links

- [`../../START_HERE.md`](../../START_HERE.md)
- [`../../QUICK_REFERENCE.md`](../../QUICK_REFERENCE.md)
- [`public-proof-index.md`](public-proof-index.md)
- [`first-install-proof.md`](first-install-proof.md)
- [`../guides/update-installed-skills.md`](../guides/update-installed-skills.md)
- [`../guides/install-verification.md`](../guides/install-verification.md)
- [`install-smoke-test-sample.md`](install-smoke-test-sample.md)
- [`first-skill-candidate/README.md`](first-skill-candidate/README.md)
- [`first-skill-candidate/expected-review.md`](first-skill-candidate/expected-review.md)
- [`../../TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md)
