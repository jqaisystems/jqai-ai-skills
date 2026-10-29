# One-minute install

Start with one skill. Preview the destination before writing files.

## Before you start

You need Python 3.11+, Git, PowerShell on Windows or Bash on macOS/Linux, and a tool that loads local skills. The installer does not install dependencies automatically.

```bash
git clone https://github.com/jqaisystems/jqai-ai-skills.git
cd jqai-ai-skills
```

Read [github-safe-publisher](../../skills/github-safe-publisher/SKILL.md). The commands below target Codex's user skills folder. For Claude Code, replace `.agents/skills` with `.claude/skills` in both commands. For another scope, [choose its target first](../../INSTALL.md#choose-the-discovery-target).

## Windows PowerShell

Preview, inspect the plan, then apply:

```powershell
.\install.ps1 github-safe-publisher -Target "$HOME/.agents/skills" -DryRun
.\install.ps1 github-safe-publisher -Target "$HOME/.agents/skills"
```

## macOS or Linux

```bash
bash ./install.sh --target "$HOME/.agents/skills" --dry-run github-safe-publisher
bash ./install.sh --target "$HOME/.agents/skills" github-safe-publisher
```

The dry run must not create the target. After applying, the chosen folder contains `github-safe-publisher/SKILL.md` and `.jqai-install.json`. If the installer refuses an existing copy, follow the [update and migration guide](update-installed-skills.md); do not force-copy over it.

<a id="reload-and-run-a-first-prompt"></a>
<a id="verify-the-skill-folder"></a>

## Reload and try it

Reload your coding tool and check that it lists the skill. In a test folder:

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

Compare the result with the [fictional first-run example](../examples/first-run-github-safe-publisher.md). For more detail, use the [installation guide](../../INSTALL.md), [verification checklist](install-verification.md), [catalogue](../catalog.md) or [troubleshooting](../../TROUBLESHOOTING.md).

The legacy installer default is retained for compatibility. These examples deliberately select the target.

## Safe First-Run Rules

- Start with one skill.
- Use a test folder before using the skill on production work.
- Do not paste credentials, tokens, account data, raw logs, database exports, or unpublished prompt notes into a tool unless you understand where they will go.
- Use `skill-reviewer` before installing skills from unknown sources.
- Use `github-safe-publisher` before publishing anything derived from private work.

## Next Steps

- Pick a different first skill with the [`skill selection guide`](skill-selection.md).
- Answer common install questions with the [`install FAQ`](install-faq.md).
- Fix install or reload issues with [`TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md).
- Browse all skills in the [`public catalog`](../catalog.md).
- Try multi-skill flows in [`workflow bundles`](../examples/workflow-bundles.md).
