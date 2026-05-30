# Troubleshooting JQ AI Skills

Use this page when a skill was installed but does not appear, does not run, or landed in the wrong folder.

If you have not installed a skill yet, start with [`INSTALL.md`](INSTALL.md). If you are new to the repo, start with [`START_HERE.md`](START_HERE.md).

## Quick Checks

Most install issues come from one of these:

1. The AI tool was not restarted or reloaded after installation.
2. The skill was copied to a different folder than the tool reads.
3. Only `SKILL.md` was copied instead of the whole skill folder.
4. The skill name in the prompt does not match the folder name.
5. The shell command was run from outside the repo root.

## Skill Does Not Appear

After installing, restart Codex or reload your AI coding tool so the skill list refreshes.

Then check that the installed folder exists:

Windows PowerShell:

```powershell
Get-ChildItem "$env:USERPROFILE\.codex\skills"
```

macOS or Linux:

```bash
ls ~/.codex/skills
```

The folder should look like this:

```text
github-safe-publisher/
  SKILL.md
  agents/
  references/
  scripts/
```

If you only see a single Markdown file, reinstall the whole folder.

## Wrong Install Target

The install scripts default to:

```text
~/.codex/skills
```

If your tool uses a different skill folder, pass a custom target:

```powershell
.\install.ps1 github-safe-publisher -Target "path\to\your\skills"
```

```bash
./install.sh --target path/to/your/skills github-safe-publisher
```

Use a temporary target when testing:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\skill-install-smoke"
```

```bash
./install.sh --target .tmp/skill-install-smoke github-safe-publisher
```

## Command Was Run From The Wrong Folder

Run install commands from the repo root, where `install.ps1`, `install.sh`, and `skills/` live:

```powershell
cd jqai-ai-skills
.\install.ps1 -List
```

```bash
cd jqai-ai-skills
./install.sh --list
```

If the list command works, the installer can see the skill folders.

## PowerShell Issues

If PowerShell blocks script execution, run the installer with the current-process policy:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1 github-safe-publisher
```

If a skill name is misspelled, list the available skills:

```powershell
.\install.ps1 -List
```

Then reinstall using the exact folder name.

## macOS Or Linux Permission Issue

If `install.sh` is not executable, run:

```bash
chmod +x ./install.sh
./install.sh github-safe-publisher
```

If the script still cannot find the skill, list the available skills:

```bash
./install.sh --list
```

## Reinstall A Skill

The install scripts replace the existing destination folder for the selected skill.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher
```

macOS or Linux:

```bash
./install.sh github-safe-publisher
```

Reinstalling is useful after pulling a new release:

```powershell
git pull
.\install.ps1 github-safe-publisher
```

```bash
git pull
./install.sh github-safe-publisher
```

## Remove A Skill

Remove only the skill folder you installed. Do not remove the entire skills directory unless you know what else is inside it.

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.codex\skills\github-safe-publisher"
```

macOS or Linux:

```bash
rm -rf ~/.codex/skills/github-safe-publisher
```

Restart or reload your AI tool after removing a skill.

## Skill Runs But Output Looks Wrong

Check these before changing the skill:

- Did you invoke the exact folder name, such as `$github-safe-publisher`?
- Did you give the skill a small test folder first?
- Did you read the skill's `SKILL.md` before using it on sensitive work?
- Does the task actually match the skill's purpose?
- Does the skill need supporting files from `references/`, `scripts/`, or `assets/`?

For the expected first-run shape, see [`docs/examples/first-run-github-safe-publisher.md`](docs/examples/first-run-github-safe-publisher.md).

## Review A Skill Before Installing

Use [`skill-reviewer`](skills/skill-reviewer/SKILL.md) before installing skill folders from unknown sources.

Example prompt:

```text
Use $skill-reviewer to inspect this skill folder before I install it.
```

For public-release work, use [`github-safe-publisher`](skills/github-safe-publisher/SKILL.md) before publishing artifacts derived from sensitive material.

## Still Stuck

Open these files in order:

1. [`START_HERE.md`](START_HERE.md)
2. [`INSTALL.md`](INSTALL.md)
3. [`docs/guides/one-minute-install.md`](docs/guides/one-minute-install.md)
4. The target skill's `SKILL.md`

Then rerun the list command:

```powershell
.\install.ps1 -List
```

```bash
./install.sh --list
```
