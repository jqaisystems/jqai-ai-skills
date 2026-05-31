# Skill Install FAQ

Use this FAQ when you are installing a JQ AI Skill for the first time, updating a skill after a pull, or checking why a skill did not appear after reload.

For commands, use [`INSTALL.md`](../../INSTALL.md). For a full verification pass, use [`install-verification.md`](install-verification.md). For update steps, use [`update-installed-skills.md`](update-installed-skills.md). For a sample temporary-target check, use [`install-smoke-test-sample.md`](../examples/install-smoke-test-sample.md). For install issues, use [`TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md).

## Quick Answers

| Question | Short answer |
|---|---|
| Which skill should I install first? | Start with `github-safe-publisher` if you are unsure. |
| Should I install all skills? | Only after you have reviewed what each skill does. |
| Do I copy only `SKILL.md`? | No. Copy the whole skill folder. |
| Where do skills install by default? | The scripts default to `~/.codex/skills`. |
| Can I test without touching my real skills folder? | Yes. Use a temporary target such as `.tmp\skill-install-smoke`. |
| How do I update later? | Pull the repo, test a temporary target, reinstall, then reload your tool. |
| Why does the skill not appear? | Usually reload, wrong target, partial copy, misspelled skill name, or wrong repo folder. |
| What should I use for the first prompt? | Use fake files, public docs, or a small test folder first. |

## Which Skill Should I Install First?

Use `github-safe-publisher` first if you are evaluating the repo. It teaches the review pattern used across the library:

```text
inspect candidate -> scan common risks -> review diff -> publish only after approval
```

If your job is different:

| Job | Start with |
|---|---|
| Public GitHub safety review | `github-safe-publisher` |
| Public-safe case study | `case-study-writer` |
| Release notes or launch copy | `release-announcement-writer` |
| Public-source research brief | `research-brief-curator` |
| Third-party skill review | `skill-reviewer` |

For a fuller comparison, use [`skill-selection.md`](skill-selection.md).

## Should I Install One Skill Or All Skills?

Install one skill first.

Install all skills only when:

- you have read the skill names and purposes;
- you understand the workflows they trigger;
- you are comfortable with the scripts or references included in each folder;
- you have a reason to keep the full library loaded.

Use the all-skills command only after that review:

```powershell
.\install.ps1 -All
```

```bash
./install.sh --all
```

## What Exactly Gets Copied?

The installer copies the whole selected folder from `skills/`.

For example, `github-safe-publisher` should copy:

```text
github-safe-publisher/
  SKILL.md
  agents/
  references/
  scripts/
```

If the destination only contains `SKILL.md`, reinstall the whole folder.

## Where Does It Install?

The default target is:

```text
~/.codex/skills
```

Use a custom target when testing or when your tool reads a different skills folder:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\skill-install-smoke"
```

```bash
./install.sh --target .tmp/skill-install-smoke github-safe-publisher
```

## How Do I Know The Install Worked?

Run the checks in [`install-verification.md`](install-verification.md).

A good install has four signals:

1. The list command shows the skill.
2. The copied folder contains `SKILL.md` and any needed support folders.
3. The AI coding tool sees the skill after restart or reload.
4. A first prompt returns the expected output shape.

Compare your terminal output with [`install-smoke-test-sample.md`](../examples/install-smoke-test-sample.md).

## Why Does The Skill Not Appear?

Most cases come from one of these:

- the AI coding tool was not restarted or reloaded;
- the skill was installed to a folder the tool does not read;
- only `SKILL.md` was copied;
- the prompt used the wrong skill name;
- the install command was run outside the repo root;
- the local repo was not updated before reinstalling.

Use [`TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md) for the step-by-step fix path.

## What Should My First Prompt Look Like?

Use the exact folder name with a small public-safe test:

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

Good output should include:

- a `READY`, `REVIEW`, or `BLOCK` verdict;
- files or folders inspected;
- scanner or review summary;
- manual checks before commit, push, install, publish, or release;
- exact next commands only when relevant.

For the expected first-run shape, use [`first-run-github-safe-publisher.md`](../examples/first-run-github-safe-publisher.md).

## What Should I Not Use For A First Test?

Do not use:

- real API keys, tokens, cookies, or passwords;
- account exports, logs, databases, or spreadsheets;
- unpublished prompt notes or private strategy;
- client names, customer records, invoices, or support tickets;
- screenshots that show account menus, dashboards, browser tabs, or file paths.

Use fake files or public docs until the install and output shape are clear.

## How Do I Update A Skill?

Use [`update-installed-skills.md`](update-installed-skills.md) for the full update path.

Short version: pull the latest repo changes, test a temporary target, reinstall the selected skill, then reload your tool.

```powershell
git pull --ff-only
.\install.ps1 github-safe-publisher
```

```bash
git pull --ff-only
./install.sh github-safe-publisher
```

## How Do I Remove A Skill?

Remove only the selected skill folder from your local skills target. Do not remove the whole skills directory unless you know what else is inside it.

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.codex\skills\github-safe-publisher"
```

macOS or Linux:

```bash
rm -rf ~/.codex/skills/github-safe-publisher
```

Restart or reload your tool after removing a skill.

## When Should I Use `skill-reviewer`?

Use `skill-reviewer` before installing a skill folder from an unfamiliar source, a modified local folder, or a folder with scripts.

Example:

```text
Use $skill-reviewer to inspect this skill folder before I install it.
```

If the review returns `BLOCK`, do not install the skill. If it returns `REVIEW`, fix or inspect the flagged items before installing.
