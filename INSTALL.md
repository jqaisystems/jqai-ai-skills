# Install JQ AI Skills

Use this page when you already know which skill you want to install and need the commands.

New to the repo? Start with [`START_HERE.md`](START_HERE.md). Need the short command map? Use [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md). Want a guided first run? Use [`docs/guides/one-minute-install.md`](docs/guides/one-minute-install.md). Have install questions? Use [`docs/guides/install-faq.md`](docs/guides/install-faq.md). Reviewing an unfamiliar skill? Use [`docs/guides/skill-review-checklist.md`](docs/guides/skill-review-checklist.md). Want to confirm the install worked? Use [`docs/guides/install-verification.md`](docs/guides/install-verification.md). If a skill does not appear after install, use [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

## Before You Start

You need a local copy of this repo:

```powershell
git clone https://github.com/jqaisystems/jqai-ai-skills.git
cd jqai-ai-skills
```

You also need a Codex or Claude-style tool that can load local skill folders.

## List Available Skills

Windows PowerShell:

```powershell
.\install.ps1 -List
```

macOS or Linux:

```bash
chmod +x ./install.sh
./install.sh --list
```

## Install One Skill

Recommended first skill:

```powershell
.\install.ps1 github-safe-publisher
```

```bash
./install.sh github-safe-publisher
```

Other examples:

```powershell
.\install.ps1 case-study-writer
.\install.ps1 release-announcement-writer
.\install.ps1 research-brief-curator
```

```bash
./install.sh case-study-writer
./install.sh release-announcement-writer
./install.sh research-brief-curator
```

## Install All Skills

Install all public skill folders only after you have reviewed what they do.

Windows PowerShell:

```powershell
.\install.ps1 -All
```

macOS or Linux:

```bash
./install.sh --all
```

## Custom Install Target

The default target is your local Codex skills folder:

```text
~/.codex/skills
```

Use a custom target when testing:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\skill-install-smoke"
```

```bash
./install.sh --target .tmp/skill-install-smoke github-safe-publisher
```

## Reload Your Tool

After installing, restart Codex or reload your AI coding tool so the skill list refreshes.

For a step-by-step verification pass, use [`docs/guides/install-verification.md`](docs/guides/install-verification.md).
For a sample temporary-target check, use [`docs/examples/install-smoke-test-sample.md`](docs/examples/install-smoke-test-sample.md).

Then run a first prompt:

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

Compare the expected output shape with [`docs/examples/first-run-github-safe-publisher.md`](docs/examples/first-run-github-safe-publisher.md).

If the skill does not appear after reload, use [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

## Manual Install

If you do not want to use the scripts, copy the whole skill folder into your local skills folder.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\github-safe-publisher" "$env:USERPROFILE\.codex\skills\github-safe-publisher"
```

macOS or Linux:

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/github-safe-publisher ~/.codex/skills/github-safe-publisher
```

## Safe Install Defaults

- Start with one skill.
- Read the skill's `SKILL.md` before using it on real work.
- Use [`docs/guides/skill-review-checklist.md`](docs/guides/skill-review-checklist.md) before installing unfamiliar or modified skill folders.
- Use a test folder for the first run.
- Use [`skill-reviewer`](skills/skill-reviewer/SKILL.md) before installing skill folders from unknown sources.
- Use [`github-safe-publisher`](skills/github-safe-publisher/SKILL.md) before publishing work derived from sensitive material.

## Next Steps

- Choose the right first skill with [`docs/guides/skill-selection.md`](docs/guides/skill-selection.md).
- Keep the main commands and links close with [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md).
- Answer common install, update, target, reload, and removal questions with [`docs/guides/install-faq.md`](docs/guides/install-faq.md).
- Review unfamiliar skill folders with [`docs/guides/skill-review-checklist.md`](docs/guides/skill-review-checklist.md).
- Verify the copied folder, reload, and first prompt with [`docs/guides/install-verification.md`](docs/guides/install-verification.md).
- Fix install or reload issues with [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).
- Browse every skill in [`docs/catalog.md`](docs/catalog.md).
- Try multi-skill paths in [`docs/examples/workflow-bundles.md`](docs/examples/workflow-bundles.md).
