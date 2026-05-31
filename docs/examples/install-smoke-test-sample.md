# Install Smoke-Test Sample

This fictional sample shows a disposable install check after choosing one skill.

It mirrors the flow in the [`install verification guide`](../guides/install-verification.md): list skills, copy one folder into a temporary target, inspect the copied files, reload the tool, run a first prompt on fake material, and clean up the temporary target.

## Goal

Use this sample when you want to know what a good first install check should look like before using a skill on real work.

The smoke test should confirm:

- the install command runs from the repo root;
- the selected skill appears in the list command;
- the whole skill folder is copied, not only `SKILL.md`;
- the copied folder includes supporting files such as `agents/`, `references/`, or `scripts/` when the skill needs them;
- the first prompt produces the expected review shape;
- the temporary target can be removed without touching your real skills folder.

## Sample Terminal Pass

### Windows PowerShell

```powershell
.\install.ps1 -List
```

Expected list excerpt:

```text
case-study-writer
github-safe-publisher
release-announcement-writer
skill-reviewer
web-scraper
```

Install one skill into a disposable target:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\skill-install-smoke"
```

Expected result:

```text
Installed github-safe-publisher -> .tmp\skill-install-smoke\github-safe-publisher
Restart Codex or reload your AI coding tool so the skill list refreshes.
```

Confirm the copied folder:

```powershell
Test-Path ".tmp\skill-install-smoke\github-safe-publisher\SKILL.md"
Get-ChildItem ".tmp\skill-install-smoke\github-safe-publisher"
```

Expected result:

```text
True

agents
references
scripts
SKILL.md
```

### macOS Or Linux

```bash
chmod +x ./install.sh
./install.sh --list
```

Expected list excerpt:

```text
case-study-writer
github-safe-publisher
release-announcement-writer
skill-reviewer
web-scraper
```

Install one skill into a disposable target:

```bash
./install.sh --target .tmp/skill-install-smoke github-safe-publisher
```

Expected result:

```text
Installed github-safe-publisher -> .tmp/skill-install-smoke/github-safe-publisher
Restart Codex or reload your AI coding tool so the skill list refreshes.
```

Confirm the copied folder:

```bash
test -f .tmp/skill-install-smoke/github-safe-publisher/SKILL.md
ls .tmp/skill-install-smoke/github-safe-publisher
```

Expected result:

```text
agents
references
scripts
SKILL.md
```

## First Prompt Check

After copying the skill into your real tool target and reloading the tool, run a first prompt against fake or public-safe files:

```text
Use $github-safe-publisher to review this small fake README and docs folder before public release.
```

Expected output shape:

- `READY`, `REVIEW`, or `BLOCK` verdict;
- files or folders inspected;
- scanner result summary;
- manual checks before commit, push, or release;
- exact next commands only when they are safe and relevant.

For a fuller first-run output shape, compare with [`first-run-github-safe-publisher.md`](first-run-github-safe-publisher.md).

## Pass, Review, Or Stop

| Result | Meaning | Next step |
|---|---|---|
| `PASS` | The folder copied correctly and the first prompt returns the expected shape. | Install normally, reload, and use the skill on a small test folder first. |
| `REVIEW` | The folder exists, but output is incomplete or the wrong skill name was invoked. | Check the folder name, read `SKILL.md`, reload the tool, and run the first prompt again. |
| `STOP` | The copied folder is missing required files or the installer cannot find the skill. | Return to [`INSTALL.md`](../../INSTALL.md) or [`TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md) before using the skill. |

## Clean Up

Only remove the disposable target:

```powershell
Remove-Item -Recurse -Force ".tmp\skill-install-smoke"
```

```bash
rm -rf .tmp/skill-install-smoke
```

Do not remove your real skills folder unless you know exactly what else is installed there.

## Safety Boundary

Use fake folders, public-safe docs, or tiny sample files for the first prompt. Keep account exports, raw logs, unpublished notes, and private project material out of the first smoke test.
