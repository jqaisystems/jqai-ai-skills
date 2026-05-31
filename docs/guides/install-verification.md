# Install Verification

Use this guide after installation to confirm that a skill copied correctly, your tool reloaded it, and the first prompt produces the expected kind of output.

This guide uses `github-safe-publisher` because it is the safest first skill for public-release work. You can replace that folder name with any skill from [`docs/catalog.md`](../catalog.md).

For a public-safe example of the full temporary-target check, see [`docs/examples/install-smoke-test-sample.md`](../examples/install-smoke-test-sample.md).

## What This Verifies

- You are running commands from the repo root.
- The installer can see the skill folders.
- A selected skill can be copied into a test target.
- The copied folder contains the whole skill, not only `SKILL.md`.
- Your local AI coding tool can reload and invoke the skill.
- The first output has the expected review shape before you use the skill on real work.

## 1. Confirm The Repo Root

Windows PowerShell:

```powershell
Test-Path .\install.ps1
Test-Path .\skills\github-safe-publisher\SKILL.md
```

macOS or Linux:

```bash
test -f ./install.sh
test -f ./skills/github-safe-publisher/SKILL.md
```

Both checks should return success. If not, move to the folder where you cloned `jqai-ai-skills`.

## 2. List Available Skills

Windows PowerShell:

```powershell
.\install.ps1 -List
```

macOS or Linux:

```bash
chmod +x ./install.sh
./install.sh --list
```

Confirm that `github-safe-publisher` appears in the list.

## 3. Smoke-Test A Temporary Target

Use a temporary target first if you want to confirm what the installer copies before touching your actual local skills folder.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\skill-install-smoke"
```

macOS or Linux:

```bash
./install.sh --target .tmp/skill-install-smoke github-safe-publisher
```

## 4. Confirm The Copied Folder

Windows PowerShell:

```powershell
Test-Path ".tmp\skill-install-smoke\github-safe-publisher\SKILL.md"
Get-ChildItem ".tmp\skill-install-smoke\github-safe-publisher"
```

macOS or Linux:

```bash
test -f .tmp/skill-install-smoke/github-safe-publisher/SKILL.md
ls .tmp/skill-install-smoke/github-safe-publisher
```

You should see the whole skill folder. For `github-safe-publisher`, that includes `SKILL.md`, `agents/`, `references/`, and `scripts/`.

## 5. Install To Your Local Tool Target

After the smoke test looks right, install the skill normally.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher
```

macOS or Linux:

```bash
./install.sh github-safe-publisher
```

## 6. Confirm The Default Target

Windows PowerShell:

```powershell
Get-ChildItem "$env:USERPROFILE\.codex\skills\github-safe-publisher"
```

macOS or Linux:

```bash
ls ~/.codex/skills/github-safe-publisher
```

If your tool uses a different skills directory, pass that directory with `-Target` or `--target`.

## 7. Reload And Run A First Prompt

Restart or reload your AI coding tool so the skill list refreshes.

Then run this prompt on a small public-safe test folder:

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

Good output should include:

- A `READY`, `REVIEW`, or `BLOCK` verdict.
- The files or folders inspected.
- A scanner result summary.
- Manual checks before commit or release.
- Exact next commands only when they are safe and relevant.

For a sample of the expected shape, see [`docs/examples/first-run-github-safe-publisher.md`](../examples/first-run-github-safe-publisher.md).

For a sample terminal pass through the temporary target check, see [`docs/examples/install-smoke-test-sample.md`](../examples/install-smoke-test-sample.md).

## 8. Clean Up The Temporary Target

Only remove the temporary smoke-test folder. Do not remove your real skills directory.

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force ".tmp\skill-install-smoke"
```

macOS or Linux:

```bash
rm -rf .tmp/skill-install-smoke
```

## If Something Fails

| Symptom | Check |
|---|---|
| The list command fails | Confirm you are in the repo root with `install.ps1`, `install.sh`, and `skills/`. |
| The copied folder only has one file | Reinstall the whole skill folder, not only `SKILL.md`. |
| The skill does not appear in your tool | Restart or reload the tool after installing. |
| The skill appears but output looks wrong | Confirm you invoked the exact folder name, such as `$github-safe-publisher`. |
| The default target is wrong | Install again with `-Target` or `--target` for your tool's skills folder. |

For deeper fixes, use [`TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md).

## Safety Boundary

Do not use real credentials, private customer data, account exports, logs, or unpublished prompt notes for your first test. Use a small public folder or fake files until the install and first-run behavior are clear.
