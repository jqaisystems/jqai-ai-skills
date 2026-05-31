# One-Minute Install

Use this guide when you want to try one JQ AI Skill quickly instead of browsing the full catalog first.

For the full visitor path, start with [`START_HERE.md`](../../START_HERE.md). For the short command reference, use [`INSTALL.md`](../../INSTALL.md). For common install questions, use [`install-faq.md`](install-faq.md). If the skill does not appear after install, use [`TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md).

The safest first install is `github-safe-publisher` because it teaches the review habit this library is built around: inspect the public artifact, scan for common risks, review the diff, then publish only when the result is safe.

## Before You Start

You need:

- A local copy of this repo.
- PowerShell on Windows, or a shell on macOS/Linux.
- A Codex or Claude-style tool that can load local skill folders.

If you do not have the repo locally yet:

```powershell
git clone https://github.com/jqaisystems/jqai-ai-skills.git
cd jqai-ai-skills
```

## Windows PowerShell

List available skills:

```powershell
.\install.ps1 -List
```

Install one skill:

```powershell
.\install.ps1 github-safe-publisher
```

Expected result:

```text
Installed github-safe-publisher -> <your-local-skills-folder>\github-safe-publisher
Restart Codex or reload your AI coding tool so the skill list refreshes.
```

## macOS Or Linux

List available skills:

```bash
chmod +x ./install.sh
./install.sh --list
```

Install one skill:

```bash
./install.sh github-safe-publisher
```

Expected result:

```text
Installed github-safe-publisher -> <your-local-skills-folder>/github-safe-publisher
Restart Codex or reload your AI coding tool so the skill list refreshes.
```

## Reload And Run A First Prompt

Restart or reload your AI coding tool so it can see the new skill.

Then try this prompt in a test repo or draft folder:

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

For a fake first-run output shape, see [`docs/examples/first-run-github-safe-publisher.md`](../examples/first-run-github-safe-publisher.md).

For a content or release workflow, install a different first skill:

```powershell
.\install.ps1 release-announcement-writer
```

Then run:

```text
Use $release-announcement-writer to turn this changelog into GitHub release notes and a short launch post.
```

## Verify The Skill Folder

After installation, the copied folder should contain:

```text
github-safe-publisher/
  SKILL.md
  agents/
  references/
  scripts/
```

Open `SKILL.md` before using the skill on sensitive work. These files are public instructions, but your local project data may still be private.

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
