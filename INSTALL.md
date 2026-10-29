# Install JQ AI Skills

Choose one skill, inspect it, preview the installation, then apply the same command without the preview flag.

<a id="before-you-start"></a>

## Requirements

- Python 3.11 or newer, available as `python` or `python3`.
- Git and PowerShell on Windows, or Bash on macOS/Linux.
- A tool that loads local skills. No Python dependencies are installed automatically.

```bash
git clone https://github.com/jqaisystems/jqai-ai-skills.git
cd jqai-ai-skills
```

Read [safe installation and discovery](docs/guides/safe-installation.md) before copying into an existing target. For a shorter walkthrough, use [One-minute install](docs/guides/one-minute-install.md).

## Choose the discovery target

| Tool / scope | Target |
|---|---|
| Codex, your user account | `~/.agents/skills` |
| Codex, one repository | `<your-repository>/.agents/skills` |
| Claude Code, your user account | `~/.claude/skills` |

Codex's locations are documented in [official OpenAI guidance](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills). Check your tool's discovery settings before choosing a different target. The examples below use the user target; the installer accepts a repository or temporary target too.

## List available skills

PowerShell:

```powershell
.\install.ps1 -List
```

Bash:

```bash
bash ./install.sh --list
```

<a id="install-one-skill"></a>

## Install one skill for Codex

Read [github-safe-publisher](skills/github-safe-publisher/SKILL.md) first. From the repository root, preview the write without creating a target:

```powershell
.\install.ps1 github-safe-publisher -Target "$HOME/.agents/skills" -DryRun
```

```bash
bash ./install.sh --target "$HOME/.agents/skills" --dry-run github-safe-publisher
```

Review the planned destination. If it is correct, apply the installation:

```powershell
.\install.ps1 github-safe-publisher -Target "$HOME/.agents/skills"
```

```bash
bash ./install.sh --target "$HOME/.agents/skills" github-safe-publisher
```

An existing managed copy is not silently overwritten. Stop if the installer reports an unmanaged copy or local edits, then follow [managed updates and migration](docs/guides/update-installed-skills.md).

## Install one skill for Claude Code

Use the same workflow with Claude Code's target. Preview first, then apply:

```powershell
.\install.ps1 github-safe-publisher -Target "$HOME/.claude/skills" -DryRun
.\install.ps1 github-safe-publisher -Target "$HOME/.claude/skills"
```

```bash
bash ./install.sh --target "$HOME/.claude/skills" --dry-run github-safe-publisher
bash ./install.sh --target "$HOME/.claude/skills" github-safe-publisher
```

<a id="install-all-skills"></a>

## Install another skill or a bundle

Replace `github-safe-publisher` with a reviewed folder name from the [catalogue](docs/catalog.md). Keep the chosen target and preview flag. Catalogue commands are previews; apply only the workflows you have inspected.

To preview all public skills after reviewing the library:

```powershell
.\install.ps1 -All -Target "$HOME/.agents/skills" -DryRun
```

```bash
bash ./install.sh --target "$HOME/.agents/skills" --dry-run --all
```

Remove the dry-run flag only after reviewing that plan. For Claude Code, substitute its target in both the preview and apply commands.

<a id="reload-your-tool"></a>

## Verify discovery

1. Confirm `<chosen-target>/github-safe-publisher/SKILL.md` and `.jqai-install.json` exist after applying.
2. Reload or restart your coding tool.
3. Open a test folder and ask it to list the available skills, then try:

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

Compare with the [fictional first-run sample](docs/examples/first-run-github-safe-publisher.md). See [installation verification](docs/guides/install-verification.md) or [troubleshooting](TROUBLESHOOTING.md) if discovery fails. Installing a folder is not evidence that a tool has loaded it.

<a id="custom-install-target"></a>

<details>
<summary>Legacy default and temporary targets</summary>

The installer retains `~/.codex/skills` as its legacy default for compatibility. A bare command still uses that default; it is not the recommended example for a new Codex or Claude Code setup. The installer behaviour has not changed.

For a disposable test, choose a new empty target explicitly:

```powershell
.\install.ps1 github-safe-publisher -Target "$env:TEMP/jqai-skill-install-smoke" -DryRun
```

```bash
bash ./install.sh --target "${TMPDIR:-/tmp}/jqai-skill-install-smoke" --dry-run github-safe-publisher
```

</details>

## Manual Install

Copy only into a verified absent destination, after inspecting every ancestor for links and confirming ownership. Never merge into an existing skill or overwrite a private variant. Manual and older installations have no managed receipt and are intentionally not upgraded by the new installer. Prefer a fresh target and the [reviewed migration guidance](docs/guides/safe-installation.md).

## Safe Install Defaults

- Start with one skill and `-DryRun` or `--dry-run`.
- Existing identical managed copies are unchanged. Reviewed managed upgrades require `-Replace` or `--replace` and retain a backup.
- Unmanaged folders, edited copies, links, and source/target overlap are refused.
- Read the skill's `SKILL.md` before using it on real work.
- Use [`docs/guides/skill-review-checklist.md`](docs/guides/skill-review-checklist.md) before installing unfamiliar or modified skill folders.
- Use a test folder for the first run.
- Use [`skill-reviewer`](skills/skill-reviewer/SKILL.md) before installing skill folders from unknown sources.
- Use [`github-safe-publisher`](skills/github-safe-publisher/SKILL.md) before publishing work derived from sensitive material.

## Next Steps

- Choose the right first skill with [`docs/guides/skill-selection.md`](docs/guides/skill-selection.md).
- Keep the main commands and links close with [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md).
- Answer common install, update, target, reload, and removal questions with [`docs/guides/install-faq.md`](docs/guides/install-faq.md).
- Update installed skills safely with [`docs/guides/update-installed-skills.md`](docs/guides/update-installed-skills.md).
- Review unfamiliar skill folders with [`docs/guides/skill-review-checklist.md`](docs/guides/skill-review-checklist.md).
- Verify the copied folder, reload, and first prompt with [`docs/guides/install-verification.md`](docs/guides/install-verification.md).
- Fix install or reload issues with [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).
- Browse every skill in [`docs/catalog.md`](docs/catalog.md).
- Try multi-skill paths in [`docs/examples/workflow-bundles.md`](docs/examples/workflow-bundles.md).
