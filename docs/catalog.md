# JQ AI Skills Catalog

This catalog gives a public, client-readable view of the skills in this repo: what each skill does, who it helps, when to use it, and how to install it.

If you are new to the repo, start with [`START_HERE.md`](../START_HERE.md). For visitor routes, use [`docs/examples/visitor-paths.md`](examples/visitor-paths.md). For install commands, use [`INSTALL.md`](../INSTALL.md). To review a skill before install, use [`docs/guides/skill-review-checklist.md`](guides/skill-review-checklist.md). To confirm a copied folder, reload, and first prompt, use [`docs/guides/install-verification.md`](guides/install-verification.md). To refresh an installed skill, use [`docs/guides/update-installed-skills.md`](guides/update-installed-skills.md). For install or reload issues, use [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md). For a guided first install, use [`docs/guides/one-minute-install.md`](guides/one-minute-install.md). For a clone-to-first-prompt route, use [`docs/examples/quick-reference-walkthrough.md`](examples/quick-reference-walkthrough.md). For a shorter first-choice guide, use [`docs/guides/skill-selection.md`](guides/skill-selection.md). To understand the folder contract, use [`docs/guides/skill-anatomy.md`](guides/skill-anatomy.md). For public-safe output examples, including a safe skill request shape, use [`docs/examples/README.md`](examples/README.md).

## At A Glance

| Area | Skill | Best for | Install |
|---|---|---|---|
| Safety and publishing | [`github-safe-publisher`](../skills/github-safe-publisher/SKILL.md) | Preparing public GitHub artifacts without leaking private details. | `.\install.ps1 github-safe-publisher` |
| Safety and review | [`skill-reviewer`](../skills/skill-reviewer/SKILL.md) | Auditing downloaded or newly written skills before installing them. | `.\install.ps1 skill-reviewer` |
| Public proof | [`case-study-writer`](../skills/case-study-writer/SKILL.md) | Turning private project work into public-safe case studies. | `.\install.ps1 case-study-writer` |
| Public proof | [`release-announcement-writer`](../skills/release-announcement-writer/SKILL.md) | Turning shipped changes into release notes and launch copy. | `.\install.ps1 release-announcement-writer` |
| Growth and outreach | [`outreach-pipeline-designer`](../skills/outreach-pipeline-designer/SKILL.md) | Designing review-first prospecting and lead workflows. | `.\install.ps1 outreach-pipeline-designer` |
| Growth and marketplace | [`etsy-listing-optimizer`](../skills/etsy-listing-optimizer/SKILL.md) | Improving marketplace listing copy and keyword fit safely. | `.\install.ps1 etsy-listing-optimizer` |
| Content and research | [`research-brief-curator`](../skills/research-brief-curator/SKILL.md) | Turning public links and approved notes into research briefs. | `.\install.ps1 research-brief-curator` |
| Content and extraction | [`web-scraper`](../skills/web-scraper/SKILL.md) | Generating browser console scripts for public or authorized paginated extraction. | `.\install.ps1 web-scraper` |
| Content cleanup | [`em-dash-remover`](../skills/em-dash-remover/SKILL.md) | Cleaning em dashes from copy without changing meaning. | `.\install.ps1 em-dash-remover` |
| Development | [`code-deduplicator`](../skills/code-deduplicator/SKILL.md) | Consolidating repeated code patterns safely. | `.\install.ps1 code-deduplicator` |
| Demo and presentation | [`demo-animation-v2`](../skills/demo-animation-v2/SKILL.md) | Building responsive product walkthrough demos. | `.\install.ps1 demo-animation-v2` |
| Demo and presentation | [`demo-animation`](../skills/demo-animation/SKILL.md) | Building the older desktop-oriented demo style. | `.\install.ps1 demo-animation` |

## Recommended Bundles

For a fuller walkthrough of how these bundles work in practice, see [`docs/examples/workflow-bundles.md`](examples/workflow-bundles.md).

### Public GitHub Publishing

Use this bundle when your main job is turning private work into public-safe proof.

```powershell
.\install.ps1 github-safe-publisher
.\install.ps1 case-study-writer
.\install.ps1 release-announcement-writer
```

Typical output:

- Public-safe README or release copy.
- Sanitized case study draft.
- GitHub release notes, website blurb, and short launch post.

### Content And Research

Use this bundle when you work with public sources, saved links, notes, and copy cleanup.

```powershell
.\install.ps1 research-brief-curator
.\install.ps1 web-scraper
.\install.ps1 em-dash-remover
```

Typical output:

- Source-aware research brief.
- Browser console extraction script for public or authorized pages.
- Cleaned copy with meaning preserved.

### Demo And Launch

Use this bundle when you need to show a workflow and then announce it.

```powershell
.\install.ps1 demo-animation-v2
.\install.ps1 release-announcement-writer
```

Typical output:

- Responsive HTML walkthrough demo.
- Launch notes and short public announcement copy.

## Skill Details

### `github-safe-publisher`

**Use it for:** public release preparation, README updates, GitHub artifacts, demo notes, examples, and case study material that came from private work.

**Who it helps:** builders who publish sanitized proof without exposing credentials, raw prompts, logs, local paths, databases, client material, or private implementation details.

**Typical output:** `READY`, `REVIEW`, or `BLOCK` verdict; scanner summary; manual review checklist; exact next steps before publishing.

**First-run sample:** [`docs/examples/first-run-github-safe-publisher.md`](examples/first-run-github-safe-publisher.md)

**Install:**

```powershell
.\install.ps1 github-safe-publisher
```

### `skill-reviewer`

**Use it for:** checking a skill folder or `SKILL.md` before installing it locally.

**Who it helps:** anyone testing third-party skills or reviewing a newly written skill for risky behavior.

**Typical output:** safety verdict, risky patterns, required human checks, and install recommendation.

**Review checklist:** [`docs/guides/skill-review-checklist.md`](guides/skill-review-checklist.md)

**Sample:** [`docs/examples/skill-reviewer-sample.md`](examples/skill-reviewer-sample.md)

**Install:**

```powershell
.\install.ps1 skill-reviewer
```

### `case-study-writer`

**Use it for:** turning private project work, automations, agent workflows, internal tools, demos, or client-facing systems into public-safe case studies.

**Who it helps:** studios, consultants, and builders who need proof of work without publishing source code, credentials, identifying details, raw prompts, logs, databases, or sensitive implementation detail.

**Typical output:** public-safe case study with problem, workflow, safeguards, outcome, and adaptation value.

**Install:**

```powershell
.\install.ps1 case-study-writer
```

### `release-announcement-writer`

**Use it for:** release notes, GitHub release copy, website update blurbs, changelogs, and short launch posts.

**Who it helps:** builders who ship frequent changes and need clear public communication that stays accurate to the diff or shipped feature list.

**Typical output:** GitHub release notes, website copy, social post variants, and assumptions or open checks.

**Sample:** [`docs/examples/release-announcement-writer-sample.md`](examples/release-announcement-writer-sample.md)

**Install:**

```powershell
.\install.ps1 release-announcement-writer
```

### `outreach-pipeline-designer`

**Use it for:** prospecting workflows, lead qualification, enrichment, scoring, outreach drafts, follow-up systems, CRM handoff, and review queues.

**Who it helps:** teams that want AI-assisted outreach architecture without unattended sending or exposure of credentials, private data, prospect lists, scraped exports, or raw prompts.

**Typical output:** human-reviewed pipeline design with gates for data use, drafting, approval, and system-of-record changes.

**Sample:** [`docs/examples/outreach-pipeline-designer-sample.md`](examples/outreach-pipeline-designer-sample.md)

**Install:**

```powershell
.\install.ps1 outreach-pipeline-designer
```

### `etsy-listing-optimizer`

**Use it for:** marketplace SEO, listing title and tag improvements, description rewrites, keyword fit, shop audits, and listing refresh workflows.

**Who it helps:** sellers and operators who need better marketplace copy while keeping shop exports, private metrics, customer data, credentials, raw CSVs, and live shop configuration private.

**Typical output:** prioritized listing recommendations, revised titles/tags/descriptions, and review notes.

**Sample:** [`docs/examples/etsy-listing-optimizer-sample.md`](examples/etsy-listing-optimizer-sample.md)

**Install:**

```powershell
.\install.ps1 etsy-listing-optimizer
```

### `research-brief-curator`

**Use it for:** public-source links, saved notes, newsletters, documentation updates, release notes, market signals, and research snippets.

**Who it helps:** people who collect public information and need a safe daily or weekly brief with source tracking, visibility labels, and archive decisions.

**Typical output:** source-aware research brief with public/private visibility labels and human review checkpoints.

**Install:**

```powershell
.\install.ps1 research-brief-curator
```

### `web-scraper`

**Use it for:** browser console scripts that extract public or authorized paginated website data into structured JSON.

**Who it helps:** users who need repeatable extraction for listings, portfolios, directories, or public page collections while staying inside authorized access.

**Typical output:** browser console scraper, localStorage accumulation pattern, and processing notes.

**Install:**

```powershell
.\install.ps1 web-scraper
```

### `em-dash-remover`

**Use it for:** removing em dashes from copy and replacing them with natural alternatives.

**Who it helps:** writers and operators cleaning AI-ish punctuation from public copy while preserving the original meaning.

**Typical output:** edited copy with em dashes replaced by commas, periods, parentheses, or rewritten sentences where needed.

**Install:**

```powershell
.\install.ps1 em-dash-remover
```

### `code-deduplicator`

**Use it for:** duplicated code introduced or touched in the current session, especially exact or low-risk repeated patterns.

**Who it helps:** developers who want small consolidation passes without broad refactors or behavior changes.

**Typical output:** proposed duplicates, scoped consolidation, and verification notes.

**Install:**

```powershell
.\install.ps1 code-deduplicator
```

### `demo-animation-v2`

**Use it for:** responsive, self-playing HTML product demos with intro screen, dashboard mockup, captions, controls, cursor animation, touch support, fullscreen behavior, and reduced-motion support.

**Who it helps:** builders who need a polished workflow walkthrough that works across desktop and mobile contexts.

**Typical output:** single-file responsive demo based on the packaged template.

**Install:**

```powershell
.\install.ps1 demo-animation-v2
```

### `demo-animation`

**Use it for:** the older desktop-oriented HTML walkthrough style.

**Who it helps:** projects that specifically need the legacy demo format rather than the responsive `demo-animation-v2` template.

**Typical output:** simple self-playing desktop demo with captions, timeline controls, cursor animation, highlights, and ending screen.

**Install:**

```powershell
.\install.ps1 demo-animation
```

## Safe Install Defaults

- Start with one skill if you are evaluating the library.
- Use the [`visitor paths`](examples/visitor-paths.md) when you want to choose between evaluation, install, and public-proof routes.
- Use [`QUICK_REFERENCE.md`](../QUICK_REFERENCE.md) when you want one short command and link map.
- Use the [`quick reference walkthrough`](examples/quick-reference-walkthrough.md) when you want clone-to-first-prompt steps.
- Use [`INSTALL.md`](../INSTALL.md) when you need the short command reference.
- Use the [`install FAQ`](guides/install-faq.md) for first skill choice, install-all, target, reload, update, and removal questions.
- Use the [`skill review checklist`](guides/skill-review-checklist.md) before installing unfamiliar or modified skill folders.
- Use the [`install verification guide`](guides/install-verification.md) to confirm the target folder, copied files, reload, and first prompt.
- Use the [`update installed skills guide`](guides/update-installed-skills.md) when you need to refresh a copied skill folder.
- Compare with the [`install smoke-test sample`](examples/install-smoke-test-sample.md) when you want a disposable temporary-target example.
- Use [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) if a skill does not appear after install.
- Use the [`one-minute install guide`](guides/one-minute-install.md) if you want the shortest verified path.
- Review a skill before installing it into a private workspace.
- Use `github-safe-publisher` before publishing any artifact derived from private work.
- Use `demo-animation-v2` for new demos unless you specifically need the legacy desktop style.
- Install all skills only after you understand what each one does.

List available skills:

```powershell
.\install.ps1 -List
```

Install all skills:

```powershell
.\install.ps1 -All
```
