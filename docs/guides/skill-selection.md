# Skill Selection Guide

Use this guide when you want to install one useful skill first instead of browsing every folder.

For the fastest guided install, see [`docs/guides/one-minute-install.md`](one-minute-install.md). If two or three skills look useful and you need to choose one first, use [`first-skill-scorecard.md`](first-skill-scorecard.md). For the complete skill list with recommended bundles and safe install defaults, see [`docs/catalog.md`](../catalog.md).

## Start With Your Job

| Job | Best first skill | Use it when |
|---|---|---|
| Publish safely | [`github-safe-publisher`](../../skills/github-safe-publisher/SKILL.md) | You are preparing a repo, case study, README, demo note, or example for public GitHub. |
| Turn work into proof | [`case-study-writer`](../../skills/case-study-writer/SKILL.md) | You need a public-safe story from private project work, an automation, or an internal system. |
| Announce a release | [`release-announcement-writer`](../../skills/release-announcement-writer/SKILL.md) | You have a changelog, shipped feature list, diff, or version update to turn into public copy. |
| Review a skill | [`skill-reviewer`](../../skills/skill-reviewer/SKILL.md) | You downloaded or wrote a skill and want to inspect it before installing. |
| Build a sales workflow | [`outreach-pipeline-designer`](../../skills/outreach-pipeline-designer/SKILL.md) | You need a human-reviewed prospecting, scoring, draft, or follow-up process. |
| Improve marketplace copy | [`etsy-listing-optimizer`](../../skills/etsy-listing-optimizer/SKILL.md) | You are auditing listing titles, tags, descriptions, or keyword fit using public-safe data. |
| Curate public research | [`research-brief-curator`](../../skills/research-brief-curator/SKILL.md) | You have public links, saved notes, newsletters, or source snippets to turn into a brief. |
| Extract public page data | [`web-scraper`](../../skills/web-scraper/SKILL.md) | You need browser console scripts for public or authorized paginated extraction. |
| Clean AI-ish punctuation | [`em-dash-remover`](../../skills/em-dash-remover/SKILL.md) | You want to remove em dashes from copy without changing the meaning. |
| Reduce repeated code | [`code-deduplicator`](../../skills/code-deduplicator/SKILL.md) | You touched code with repeated low-risk patterns that may be safe to consolidate. |
| Build a responsive demo | [`demo-animation-v2`](../../skills/demo-animation-v2/SKILL.md) | You want a responsive product walkthrough with controls, touch support, and a template asset. |
| Build a legacy demo | [`demo-animation`](../../skills/demo-animation/SKILL.md) | You specifically want the older desktop-oriented demo style. |

## Recommended Starter Sets

For practical multi-skill examples, see [`docs/examples/workflow-bundles.md`](../examples/workflow-bundles.md).

### Public GitHub Publishing

Install:

```powershell
.\install.ps1 github-safe-publisher
.\install.ps1 case-study-writer
.\install.ps1 release-announcement-writer
```

Use this set when your main workflow is turning private work into public-safe GitHub proof.

### Content And Research

Install:

```powershell
.\install.ps1 research-brief-curator
.\install.ps1 web-scraper
.\install.ps1 em-dash-remover
```

Use this set when you work with public sources, saved links, copy cleanup, and structured notes.

### Demo And Launch

Install:

```powershell
.\install.ps1 demo-animation-v2
.\install.ps1 release-announcement-writer
```

Use this set when you need to show a workflow and then announce it clearly.

## Safe Defaults

- Install one skill first if you are evaluating the repo.
- Use `skill-reviewer` before installing skills from an unknown source.
- Use [`first-skill-scorecard.md`](first-skill-scorecard.md) when several skills look useful and you want to pick one safe first test.
- Use `github-safe-publisher` before publishing any repo, example, case study, screenshot, or release note that came from private work.
- Use `demo-animation-v2` for new demos unless you specifically need the legacy desktop style.

## List Or Install

One-minute install path:

```powershell
.\install.ps1 github-safe-publisher
```

List available skills:

```powershell
.\install.ps1 -List
```

Install all skills only after you have reviewed what they do:

```powershell
.\install.ps1 -All
```
