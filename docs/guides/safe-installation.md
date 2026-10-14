# Safe installation and discovery

Both installers require Python 3.11+ and use the same standard-library implementation. They do not install dependencies. Existing command names and the legacy default `~/.codex/skills` are retained for compatibility; this default is not a claim about every current tool's discovery behavior.

For a new setup, select the appropriate location explicitly:

| Tool | Repository scope | User scope |
|---|---|---|
| Codex | `.agents/skills` in applicable repository directories | `~/.agents/skills` |
| Claude Code | `.claude/skills` | `~/.claude/skills` |

Checked 2026-10-14 against [Codex documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) and [Claude Code documentation](https://code.claude.com/docs/en/skills). Codex supports linked skill folders. Inspect existing compatibility paths and duplicates before migrating; no automatic migration is performed.

```powershell
.\install.ps1 backup-readiness-auditor -Target "$HOME/.agents/skills" -DryRun
.\install.ps1 backup-readiness-auditor -Target "$HOME/.agents/skills"
```

```bash
./install.sh --target "$HOME/.agents/skills" --dry-run backup-readiness-auditor
./install.sh --target "$HOME/.agents/skills" backup-readiness-auditor
```

## Existing copies

Fresh installations include a receipt recording relative files and hashes, not machine paths. Rerunning an identical managed installation is a no-op. Updating a changed source requires `-Replace` or `--replace` after review, and only works if the installed copy still matches its receipt. The old folder is renamed to a unique sibling backup; nothing is deleted.

Unmanaged legacy copies, edited copies, linked paths (including dangling links), and source/target overlap are refused. Use a new target or separately review a manual migration. Do not fabricate receipts, delete private variants, or use force-copy commands to bypass refusal.

The whole selection is preflighted before writes. A later I/O failure can leave earlier selections installed and a staging folder retained. Review the private target before retrying. Concurrent mutation of the target is unsupported; receipts are not a security signature.

## Shared sources

The copy installer deliberately does not repair links. For a separately requested repair, verify the intended source, ownership, hashes, and destination absence before creating a missing link. Preserve correct links and stop on conflicts. Do not enable Developer Mode, elevate, or change execution policy merely to force installation.

After installation, use the tool's supported refresh/reload and verify actual discovery with a fictional prompt. Keep operational reports, backups, and staging private. Removing a link or an old copy requires its own reviewed action; never recursively delete an uninspected discovery directory.
