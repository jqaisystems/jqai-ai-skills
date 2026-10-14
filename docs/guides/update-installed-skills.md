# Update Installed Skills

Use this guide for reviewed upgrades, not forced replacement. Both entrypoints require Python 3.11+; no dependencies are installed automatically.

## Review before changing anything

1. Check `git status --short` and preserve local work.
2. Update the repository only when requested; `git pull --ff-only` stops on divergent history.
3. Read the changelog, inspect the selected skill, and test it in a fresh disposable target outside the repository.
4. Identify the tool's actual discovery directory using [safe installation](safe-installation.md). Inspect existing copies and links before choosing a target.

## Preview and upgrade one managed copy

These examples explicitly select the current Codex user scope. Change the target only after verifying your tool and installation.

```powershell
.\install.ps1 github-safe-publisher -Target "$HOME/.agents/skills" -Replace -DryRun
.\install.ps1 github-safe-publisher -Target "$HOME/.agents/skills" -Replace
```

```bash
./install.sh --target "$HOME/.agents/skills" --replace --dry-run github-safe-publisher
./install.sh --target "$HOME/.agents/skills" --replace github-safe-publisher
```

Run the second command only after reviewing the first. An identical managed copy is unchanged. A changed source replaces only an installed copy that still matches its receipt; the old folder is retained as a unique sibling backup. No files are deleted.

For a reviewed full-library upgrade, use `-All -Replace -DryRun` or `--all --replace --dry-run` first. Preflight checks the whole selection. A later I/O failure can still leave earlier skills installed and staging retained.

## Legacy copies, edits, and shared links

An installation from an older release has no receipt and is refused, even with Replace. Edited copies, junctions, symlinks, dangling links, and overlapping targets are also refused.

Preserve the original and use a fresh target for comparison, or request a separate manual migration with exact source/destination checks. Do not manufacture receipts or force-copy around a refusal. The installer is not a link-repair or deletion tool.

## Verify and retain evidence

Reload or refresh the tool, confirm actual discovery, and run a fictional prompt. Keep backups until the new version is verified and a separate cleanup has been reviewed. Before removing any disposable test directory, resolve its exact absolute path, confirm containment and ownership, and inspect it for links and unexpected files.

See [install verification](install-verification.md), [synthetic safety proof](../examples/safer-skills-recovery-sample.md), and [troubleshooting](../../TROUBLESHOOTING.md).
