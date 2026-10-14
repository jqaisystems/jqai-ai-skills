# JQ AI Skills Catalog

This catalog gives a public, client-readable view of the skills in this repo: what each skill does, who it helps, when to use it, and how to install it.

If you are new to the repo, start with [`START_HERE.md`](../START_HERE.md). For visitor routes, use [`docs/examples/visitor-paths.md`](examples/visitor-paths.md). For one page of public proof assets, use [`docs/examples/public-proof-index.md`](examples/public-proof-index.md). For one end-to-end first install proof, use [`docs/examples/first-install-proof.md`](examples/first-install-proof.md). For one post-release update proof, use [`docs/examples/update-after-release-proof.md`](examples/update-after-release-proof.md). For utility skill output proof, use [`docs/examples/utility-skill-proof-pack.md`](examples/utility-skill-proof-pack.md). For a responsive demo output shape, use [`docs/examples/demo-animation-v2-walkthrough-sample.md`](examples/demo-animation-v2-walkthrough-sample.md). For release-to-showcase handoff proof, use [`docs/examples/release-showcase-handoff-sample.md`](examples/release-showcase-handoff-sample.md). To evaluate trust and install readiness, use [`docs/guides/evaluate-skill-library.md`](guides/evaluate-skill-library.md). To score one safe first install, use [`docs/guides/first-skill-scorecard.md`](guides/first-skill-scorecard.md). To run the selected skill with fake input, use [`docs/examples/first-skill-walkthrough.md`](examples/first-skill-walkthrough.md), [`docs/examples/first-skill-candidate/README.md`](examples/first-skill-candidate/README.md), and [`docs/examples/first-skill-candidate/expected-review.md`](examples/first-skill-candidate/expected-review.md). For install commands, use [`INSTALL.md`](../INSTALL.md). To review a skill before install, use [`docs/guides/skill-review-checklist.md`](guides/skill-review-checklist.md). To confirm a copied folder, reload, and first prompt, use [`docs/guides/install-verification.md`](guides/install-verification.md). To refresh an installed skill, use [`docs/guides/update-installed-skills.md`](guides/update-installed-skills.md). For install or reload issues, use [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md). For a guided first install, use [`docs/guides/one-minute-install.md`](guides/one-minute-install.md). For a clone-to-first-prompt route, use [`docs/examples/quick-reference-walkthrough.md`](examples/quick-reference-walkthrough.md). For a shorter first-choice guide, use [`docs/guides/skill-selection.md`](guides/skill-selection.md). To understand the folder contract, use [`docs/guides/skill-anatomy.md`](guides/skill-anatomy.md). For current maturity, visible proof, install notes, and safety sensitivity, use [`docs/skill-quality-matrix.md`](skill-quality-matrix.md). For public-safe output examples, including a safe skill request shape, use [`docs/examples/README.md`](examples/README.md).

## At A Glance

Inventory: 47 skills in v0.13.0, up from 46 in v0.12.0.

### Backup readiness

[backup-readiness-auditor](../skills/backup-readiness-auditor/SKILL.md) evaluates supplied verification metadata, not backup contents. It reports coverage, freshness, capacity, integrity, and recovery-test gaps without copying, restoring, or authorizing source retirement. See the [fictional sample](examples/backup-readiness-auditor-sample.md).

| Area | Skill | Best for | Install |
|---|---|---|---|
| Local media | [`media-spec-checker`](../skills/media-spec-checker/SKILL.md) | Dimensions, display ratio, duration, format, codec, size, and naming against local rules. | `.\install.ps1 media-spec-checker` |
| Offline operations | [`automation-state-reconciler`](../skills/automation-state-reconciler/SKILL.md) | Snapshot and receipt drift review with history preservation, no live actions. | `.\install.ps1 automation-state-reconciler` |
| Recovery planning | [`windows-reinstall-planner`](../skills/windows-reinstall-planner/SKILL.md) | Metadata-only inventory and private reinstall checklist. | `.\install.ps1 windows-reinstall-planner` |
| Image workflow | [`ai-image-run-pacing`](../skills/ai-image-run-pacing/SKILL.md) | Plan image-generation sessions within provider limits. | `.\install.ps1 ai-image-run-pacing` |
| Public demos | [`local-app-public-demo`](../skills/local-app-public-demo/SKILL.md) | Prepare static, read-only public demonstrations of local tools. | `.\install.ps1 local-app-public-demo` |
| Thumbnail design | [`thumbnail-set-designer`](../skills/thumbnail-set-designer/SKILL.md) | Develop genuinely distinct thumbnail concepts. | `.\install.ps1 thumbnail-set-designer` |
| Thumbnail review | [`thumbnail-legibility-check`](../skills/thumbnail-legibility-check/SKILL.md) | Compare candidates at their intended viewing size. | `.\install.ps1 thumbnail-legibility-check` |
| Safety and publishing | [`github-safe-publisher`](../skills/github-safe-publisher/SKILL.md) | Preparing public GitHub artifacts without leaking private details. | `.\install.ps1 github-safe-publisher` |
| Safety and review | [`skill-reviewer`](../skills/skill-reviewer/SKILL.md) | Auditing downloaded or newly written skills before installing them. | `.\install.ps1 skill-reviewer` |
| Public proof | [`case-study-writer`](../skills/case-study-writer/SKILL.md) | Turning private project work into public-safe case studies. | `.\install.ps1 case-study-writer` |
| Public proof | [`release-announcement-writer`](../skills/release-announcement-writer/SKILL.md) | Turning shipped changes into release notes and launch copy. | `.\install.ps1 release-announcement-writer` |
| Public proof | [`github-profile-proof-updater`](../skills/github-profile-proof-updater/SKILL.md) | Refreshing GitHub profile visuals, live checks, and proof trails. | `.\install.ps1 github-profile-proof-updater` |
| Public proof | [`social-campaign-proof-tracker`](../skills/social-campaign-proof-tracker/SKILL.md) | Planning LinkedIn/X proof campaigns, links, alt text, and follow-ups. | `.\install.ps1 social-campaign-proof-tracker` |
| Growth and outreach | [`outreach-pipeline-designer`](../skills/outreach-pipeline-designer/SKILL.md) | Designing review-first prospecting and lead workflows. | `.\install.ps1 outreach-pipeline-designer` |
| Growth and outreach | [`cold-outreach-writer`](../skills/cold-outreach-writer/SKILL.md) | Drafting one personalised cold email, subject lines, LinkedIn note, and follow-up. | `.\install.ps1 cold-outreach-writer` |
| Growth and outreach | [`lead-scorer`](../skills/lead-scorer/SKILL.md) | Ranking a lead list into hot, warm, and cold tiers against your own rubric. | `.\install.ps1 lead-scorer` |
| Growth and outreach | [`follow-up-radar`](../skills/follow-up-radar/SKILL.md) | Finding overdue outreach follow-ups and drafting them, oldest first. | `.\install.ps1 follow-up-radar` |
| Client work | [`client-workspace-scaffolder`](../skills/client-workspace-scaffolder/SKILL.md) | Scaffolding a client project folder from your reusable structure template. | `.\install.ps1 client-workspace-scaffolder` |
| Client work | [`discovery-brief`](../skills/discovery-brief/SKILL.md) | Running a discovery interview and writing the brief plus a strategy starter. | `.\install.ps1 discovery-brief` |
| Client work | [`proposal-writer`](../skills/proposal-writer/SKILL.md) | Drafting a client proposal from your own service tiers and terms. | `.\install.ps1 proposal-writer` |
| Client work | [`implement-client-feedback`](../skills/implement-client-feedback/SKILL.md) | Turning revision notes into traceable, verified implementation decisions. | `.\install.ps1 implement-client-feedback` |
| Client work | [`client-delivery-auditor`](../skills/client-delivery-auditor/SKILL.md) | Auditing a final package against promised deliverables and preparing an unsent handoff. | `.\install.ps1 client-delivery-auditor` |
| Development | [`website-change-verifier`](../skills/website-change-verifier/SKILL.md) | Verifying website changes across source, build, routes, content, and browser behavior. | `.\install.ps1 website-change-verifier` |
| Agent workflow | [`skill-builder`](../skills/skill-builder/SKILL.md) | Authoring a scoped skill with current discovery guidance and safe installation checks. | `.\install.ps1 skill-builder` |
| Agent workflow | [`session-handoff`](../skills/session-handoff/SKILL.md) | Freezing session state into a start-here doc for instant resume. | `.\install.ps1 session-handoff` |
| Agent workflow | [`agents-md-writer`](../skills/agents-md-writer/SKILL.md) | Generating the AGENTS.md plus CLAUDE.md contract that shares skills across agents. | `.\install.ps1 agents-md-writer` |
| Agent workflow | [`ops-status-report`](../skills/ops-status-report/SKILL.md) | Compiling a workspace status snapshot with an Attention Needed section. | `.\install.ps1 ops-status-report` |
| Demo and presentation | [`screen-recorder`](../skills/screen-recorder/SKILL.md) | Recording a drag-selected region of the Windows desktop to a clean MP4. | `.\install.ps1 screen-recorder` |
| Growth and marketplace | [`etsy-listing-optimizer`](../skills/etsy-listing-optimizer/SKILL.md) | Improving marketplace listing copy and keyword fit safely. | `.\install.ps1 etsy-listing-optimizer` |
| Content and research | [`research-brief-curator`](../skills/research-brief-curator/SKILL.md) | Turning public links and approved notes into research briefs. | `.\install.ps1 research-brief-curator` |
| Content and evidence | [`verify-public-claims`](../skills/verify-public-claims/SKILL.md) | Checking public claims against current evidence and producing defensible rewrites. | `.\install.ps1 verify-public-claims` |
| Content and research | [`research-to-article`](../skills/research-to-article/SKILL.md) | Turning verified sources into a finished article package with a visible claim map. | `.\install.ps1 research-to-article` |
| Professional writing | [`write-evidence-backed-profile`](../skills/write-evidence-backed-profile/SKILL.md) | Drafting bios, applications, and profile copy from approved evidence. | `.\install.ps1 write-evidence-backed-profile` |
| Content and AI search | [`llms-txt-generator`](../skills/llms-txt-generator/SKILL.md) | Generating a spec-compliant llms.txt map of a website for AI assistants. | `.\install.ps1 llms-txt-generator` |
| Content and extraction | [`web-scraper`](../skills/web-scraper/SKILL.md) | Generating browser console scripts for public or authorized paginated extraction. | `.\install.ps1 web-scraper` |
| Media and provenance | [`remove-ai-image-metadata`](../skills/remove-ai-image-metadata/SKILL.md) | Inspecting and removing explicit AI provenance metadata from owned or authorized images without re-encoding supported picture data. | `.\install.ps1 remove-ai-image-metadata` |
| Content cleanup | [`em-dash-remover`](../skills/em-dash-remover/SKILL.md) | Cleaning em dashes from copy without changing meaning. | `.\install.ps1 em-dash-remover` |
| Content cleanup | [`brand-voice-linter`](../skills/brand-voice-linter/SKILL.md) | Linting copy against a brand voice guide with suggested rewrites. | `.\install.ps1 brand-voice-linter` |
| Development | [`code-deduplicator`](../skills/code-deduplicator/SKILL.md) | Consolidating repeated code patterns safely. | `.\install.ps1 code-deduplicator` |
| Development | [`php-form-mailer`](../skills/php-form-mailer/SKILL.md) | Wiring any HTML form to a two-email PHP handler with no form SaaS. | `.\install.ps1 php-form-mailer` |
| Development | [`client-intake-builder`](../skills/client-intake-builder/SKILL.md) | Generating a branded single-file client intake questionnaire. | `.\install.ps1 client-intake-builder` |
| Development | [`vault-janitor`](../skills/vault-janitor/SKILL.md) | Finding folder junk and reporting it with sizes before any cleanup. | `.\install.ps1 vault-janitor` |
| Notes and productivity | [`obsidian-daily-note`](../skills/obsidian-daily-note/SKILL.md) | Appending to today's Obsidian daily note from the terminal. | `.\install.ps1 obsidian-daily-note` |
| Notes and productivity | [`idea-inbox`](../skills/idea-inbox/SKILL.md) | Capturing raw ideas as dated, tagged, indexed markdown files. | `.\install.ps1 idea-inbox` |
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

### Proof Campaign Handoff

Use this bundle when shipped work needs a profile update, public proof trail, and LinkedIn/X campaign follow-up.

```powershell
.\install.ps1 github-profile-proof-updater
.\install.ps1 social-campaign-proof-tracker
.\install.ps1 release-announcement-writer
```

Typical output:

- GitHub profile asset refresh checklist.
- Live profile verification notes.
- Social post copy, alt text, published links, reply bank, and follow-up windows.

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

### Evidence-Based Writing

Use this bundle when public copy must be researched, defensible, and tailored without invented claims.

```powershell
.\install.ps1 verify-public-claims
.\install.ps1 research-to-article
.\install.ps1 write-evidence-backed-profile
```

Typical output:

- A claim ledger with supported, qualified, inferred, unsupported, and stale statements.
- A source-traceable article package with metadata, Link Map, and verification notes.
- Audience-specific profile writing with qualifications and omitted unsupported claims.

### Freelance Client Flow

Use this bundle when you run client work end to end: onboard, discover, propose, implement revisions, verify the website, audit delivery, and chase follow-ups.

```powershell
.\install.ps1 client-workspace-scaffolder
.\install.ps1 discovery-brief
.\install.ps1 proposal-writer
.\install.ps1 implement-client-feedback
.\install.ps1 website-change-verifier
.\install.ps1 client-delivery-auditor
.\install.ps1 follow-up-radar
```

Typical output:

- A ready client folder with a filled brief and feedback log.
- A discovery brief and strategy starter document.
- A reviewed proposal with an investment table.
- A traceable feedback matrix with implementation and verification status.
- A website verification report covering source, build, routes, content, and browser behavior.
- A delivery audit, generic handoff, and unsent email draft.
- A follow-up radar report with drafts for everything overdue.

### Agent Workflow Setup

Use this bundle when you want your AI-assisted work itself to be repeatable across sessions, workspaces, and agents.

```powershell
.\install.ps1 skill-builder
.\install.ps1 session-handoff
.\install.ps1 agents-md-writer
```

Typical output:

- A new skill folder in the right tier, registered and verified.
- A START_HERE.md that resumes the next session in minutes.
- An AGENTS.md plus CLAUDE.md contract serving Claude Code and Codex from one skill set.

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

**First install proof:** [`docs/examples/first-install-proof.md`](examples/first-install-proof.md)

**First candidate pack:** [`docs/examples/first-skill-candidate/README.md`](examples/first-skill-candidate/README.md)

**Expected candidate review:** [`docs/examples/first-skill-candidate/expected-review.md`](examples/first-skill-candidate/expected-review.md)

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

**Release handoff proof:** [`docs/examples/release-showcase-handoff-sample.md`](examples/release-showcase-handoff-sample.md)

**Install:**

```powershell
.\install.ps1 release-announcement-writer
```

### `github-profile-proof-updater`

**Use it for:** refreshing a GitHub profile or public proof layer, replacing visual assets while preserving README paths, validating live GitHub rendering, and recording proof-trail links.

**Who it helps:** builders who use GitHub as a public credibility surface and want profile updates to be reviewable, safe, and repeatable.

**Typical output:** changed asset list, image-reference verification, live profile check, proof-trail update, and next social handoff.

**Sample:** [`docs/examples/github-profile-proof-updater-sample.md`](examples/github-profile-proof-updater-sample.md)

**Install:**

```powershell
.\install.ps1 github-profile-proof-updater
```

### `social-campaign-proof-tracker`

**Use it for:** turning a project update into LinkedIn/X proof copy, image or video order, alt text, published-link tracking, reply bank notes, and follow-up windows.

**Who it helps:** builders who want public proof campaigns to become reusable evidence, not one-off posts that disappear into the feed.

**Typical output:** platform-specific campaign recommendation, copy, alt text, proof-trail updates, and follow-up checklist.

**Sample:** [`docs/examples/social-campaign-proof-tracker-sample.md`](examples/social-campaign-proof-tracker-sample.md)

**Install:**

```powershell
.\install.ps1 social-campaign-proof-tracker
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

### `verify-public-claims`

**Use it for:** fact-checking public website copy, release notes, case studies, marketing claims, reports, articles, product descriptions, and profiles against supplied evidence and current public sources.

**Who it helps:** writers, founders, marketers, researchers, and reviewers who need to know which claims are supported, qualified, inferred, unsupported, or stale before publication.

**Typical output:** a dated claim ledger, defensible revised copy, sources checked, unresolved conflicts, and held claims.

**Sample:** [`docs/examples/verify-public-claims-sample.md`](examples/verify-public-claims-sample.md)

**Install:**

```powershell
.\install.ps1 verify-public-claims
```

### `research-to-article`

**Use it for:** turning a topic and public sources into a finished article rather than a brief or reading queue.

**Who it helps:** builders, researchers, educators, and small teams that need a practical article with claim mapping, metadata, source credits, and a visible evidence cutoff.

**Typical output:** title, slug, meta description, claim map, outline, finished article, Link Map, and verification report. The skill does not publish or modify websites.

**Sample:** [`docs/examples/research-to-article-sample.md`](examples/research-to-article-sample.md)

**Install:**

```powershell
.\install.ps1 research-to-article
```

### `write-evidence-backed-profile`

**Use it for:** bios, applications, portfolio introductions, proposal introductions, cover notes, and professional profile copy that must remain grounded in approved evidence.

**Who it helps:** independent professionals, teams, applicants, and organizations that need audience-specific positioning without invented experience, credentials, relationships, or results.

**Typical output:** a compact evidence map, finished draft, qualifications, omitted claims, sources checked, and facts that still need confirmation.

**Sample:** [`docs/examples/write-evidence-backed-profile-sample.md`](examples/write-evidence-backed-profile-sample.md)

**Install:**

```powershell
.\install.ps1 write-evidence-backed-profile
```

### `web-scraper`

**Use it for:** browser console scripts that extract public or authorized paginated website data into structured JSON.

**Who it helps:** users who need repeatable extraction for listings, portfolios, directories, or public page collections while staying inside authorized access.

**Typical output:** browser console scraper, localStorage accumulation pattern, and processing notes.

**Utility proof pack:** [`docs/examples/utility-skill-proof-pack.md`](examples/utility-skill-proof-pack.md)

**Install:**

```powershell
.\install.ps1 web-scraper
```

### `em-dash-remover`

**Use it for:** removing em dashes from copy and replacing them with natural alternatives.

**Who it helps:** writers and operators cleaning AI-ish punctuation from public copy while preserving the original meaning.

**Typical output:** edited copy with em dashes replaced by commas, periods, parentheses, or rewritten sentences where needed.

**Utility proof pack:** [`docs/examples/utility-skill-proof-pack.md`](examples/utility-skill-proof-pack.md)

**Install:**

```powershell
.\install.ps1 em-dash-remover
```

### `code-deduplicator`

**Use it for:** duplicated code introduced or touched in the current session, especially exact or low-risk repeated patterns.

**Who it helps:** developers who want small consolidation passes without broad refactors or behavior changes.

**Typical output:** proposed duplicates, scoped consolidation, and verification notes.

**Utility proof pack:** [`docs/examples/utility-skill-proof-pack.md`](examples/utility-skill-proof-pack.md)

**Install:**

```powershell
.\install.ps1 code-deduplicator
```

### `demo-animation-v2`

**Use it for:** responsive, self-playing HTML product demos with intro screen, dashboard mockup, captions, controls, cursor animation, touch support, fullscreen behavior, and reduced-motion support.

**Who it helps:** builders who need a polished workflow walkthrough that works across desktop and mobile contexts.

**Typical output:** single-file responsive demo based on the packaged template.

**Walkthrough sample:** [`docs/examples/demo-animation-v2-walkthrough-sample.md`](examples/demo-animation-v2-walkthrough-sample.md)

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

### `php-form-mailer`

**Use it for:** wiring an HTML form to a two-email PHP system: a structured notification to the site owner and a branded confirmation to the submitter.

**Who it helps:** anyone running static or hand-coded sites on cPanel or shared PHP hosting who does not want a third-party form service.

**Typical output:** one self-contained PHP handler with sanitisation and a honeypot, an updated form action and JS handler with a mailto fallback, and a live curl test.

**Install:**

```powershell
.\install.ps1 php-form-mailer
```

### `client-intake-builder`

**Use it for:** generating a branded, single-file HTML client intake questionnaire from one of four question banks: brand identity, web design, automation, or pre-call brief.

**Who it helps:** freelancers and studios who want the client's first touchpoint to look like the work they sell, not a default form builder.

**Typical output:** one production-ready HTML file with validation, progress, a honeypot, and a success state, ready to pair with `php-form-mailer`.

**Install:**

```powershell
.\install.ps1 client-intake-builder
```

### `cold-outreach-writer`

**Use it for:** drafting one personalised cold email under 180 words from a research block, plus three subject lines, a LinkedIn note, and a 7-day follow-up.

**Who it helps:** freelancers and small studios doing targeted outreach to a researched shortlist, not mass sends.

**Typical output:** a draft package for human review. The skill never sends anything and never fabricates claims.

**Install:**

```powershell
.\install.ps1 cold-outreach-writer
```

### `lead-scorer`

**Use it for:** ranking a lead list 0 to 100 into hot, warm, and cold tiers against a rubric you define once and reuse.

**Who it helps:** anyone whose lead list is bigger than their outreach capacity and who wants reasons behind every score.

**Typical output:** a ranked CSV with score, tier, reason, and next action per lead, plus a summary with per-tier counts and observed patterns. Thin-data leads get flagged for research, not guessed.

**Install:**

```powershell
.\install.ps1 lead-scorer
```

### `brand-voice-linter`

**Use it for:** linting copy against a voice guide: buzzword clusters, hedge language, vague superlatives, passive voice, exclamation marks, and AI-tell phrases.

**Who it helps:** writers and brand owners who want their writing rules enforced on every draft, not remembered occasionally.

**Typical output:** a violation report with line numbers, severity, and suggested rewrites. Report-only by default; fixes applied only on request.

**Install:**

```powershell
.\install.ps1 brand-voice-linter
```

### `obsidian-daily-note`

**Use it for:** creating or appending to today's daily note in an Obsidian vault without leaving the terminal.

**Who it helps:** terminal-heavy workers whose daily logging habit dies on the context switch to a notes app.

**Typical output:** a titled section appended to the correct dated note, using the vault's own folder and date format. Append-only by rule.

**Install:**

```powershell
.\install.ps1 obsidian-daily-note
```

### `idea-inbox`

**Use it for:** capturing a raw idea as a dated, tagged markdown file in a dedicated ideas folder with an index kept up to date.

**Who it helps:** anyone whose ideas arrive mid-task and die in untitled files or memory.

**Typical output:** one idea file with frontmatter plus an index entry under a category heading with a one-line hook. Never saves to the project root.

**Install:**

```powershell
.\install.ps1 idea-inbox
```

### `llms-txt-generator`

**Use it for:** generating a spec-compliant `llms.txt` so AI assistants and answer engines can understand and cite a website accurately.

**Who it helps:** site owners who want AI systems to describe their business correctly instead of approximately.

**Typical output:** an `llms.txt` for the site root with an accurate summary blockquote, sectioned page links with one honest line each, validated URLs, and private endpoints excluded.

**Install:**

```powershell
.\install.ps1 llms-txt-generator
```

### `vault-janitor`

**Use it for:** scanning a folder tree for accumulated junk: dependency folders, build caches, stray backups, logs, and OS litter.

**Who it helps:** anyone with a working folder that feels heavy, before a backup, migration, or cleanup.

**Typical output:** a `cleanup-report.md` with sized groups, top offenders, judgment-call flags, and recommendations ordered by most space per least risk. Report-only by default; archive-first when a cleanup list is approved.

**Install:**

```powershell
.\install.ps1 vault-janitor
```

### `proposal-writer`

**Use it for:** client proposals and quotes built from your own service tiers, terms, and process, saved once in an ask-once pricing config.

**Who it helps:** freelancers and studios who quote the same services repeatedly and want proposals that open with a specific read of the client, not filler.

**Typical output:** a one-page proposal markdown with situation read, scoped line items, investment table, process phases, and terms. Drafts only; nothing is ever sent.

**Install:**

```powershell
.\install.ps1 proposal-writer
```

### `follow-up-radar`

**Use it for:** scanning a folder of outreach or CRM markdown files for overdue follow-ups, then drafting them oldest first.

**Who it helps:** anyone doing manual outreach whose second touch dies in a busy week. The radar finds what is owed; a human sends every message.

**Typical output:** an overdue/due-soon report, follow-up drafts under 80 words each, and confirmed frontmatter updates after the user says a message went out.

**Install:**

```powershell
.\install.ps1 follow-up-radar
```

### `client-workspace-scaffolder`

**Use it for:** creating a complete client project folder (subfolders, filled brief, feedback log) from a structure template you define once.

**Who it helps:** freelancers and studios where every engagement starts with the same folder dance and half the clients end up with no brief at all.

**Typical output:** a ready client folder with the standard tree, a brief with status and scope filled in, and a feedback-round log. Never overwrites existing work.

**Install:**

```powershell
.\install.ps1 client-workspace-scaffolder
```

### `discovery-brief`

**Use it for:** running a structured discovery interview (business, audience, competitors, personality, style, deliverables, timeline and budget) and writing the results into documents.

**Who it helps:** anyone scoping creative or consulting projects who wants discovery answers captured as a brief and a first strategy pass, not scattered across chat.

**Typical output:** a completed brief plus a strategy starter with a draft positioning sentence, direction hypotheses, and honest open questions.

**Install:**

```powershell
.\install.ps1 discovery-brief
```

### `implement-client-feedback`

**Use it for:** turning mixed client revision notes into explicit change, keep, remove, exclude, question, and future decisions, then verifying every implemented item.

**Who it helps:** freelancers, studios, and delivery teams that need an auditable bridge between feedback and the final build.

**Typical output:** a feedback implementation brief with source wording, interpreted action, scope state, implementation evidence, verification result, and open questions.

**Sample:** [`docs/examples/implement-client-feedback-sample.md`](examples/implement-client-feedback-sample.md)

**Install:**

```powershell
.\install.ps1 implement-client-feedback
```

### `client-delivery-auditor`

**Use it for:** comparing promised deliverables with a final package before handoff.

**Who it helps:** anyone who needs to distinguish complete, partial, missing, unverified, and awaiting-client items without overstating delivery readiness.

**Typical output:** a delivery audit, unresolved-item list, generic handoff document, and unsent email draft. The skill never sends, uploads, or changes permissions.

**Sample:** [`docs/examples/client-delivery-auditor-sample.md`](examples/client-delivery-auditor-sample.md)

**Install:**

```powershell
.\install.ps1 client-delivery-auditor
```

### `website-change-verifier`

**Use it for:** framework-neutral website verification across source changes, automated checks, builds, routes, content assertions, and browser behavior.

**Who it helps:** developers and delivery teams that need evidence for website changes without assuming a specific framework or claiming a deployment happened.

**Typical output:** a verification matrix with pass, fail, blocked, and not-run states. The included route checker supports status, required-text, forbidden-text, timeout, and JSON checks against user-specified HTTP or HTTPS URLs.

**Sample:** [`docs/examples/website-change-verifier-sample.md`](examples/website-change-verifier-sample.md)

**Install:**

```powershell
.\install.ps1 website-change-verifier
```

### `skill-builder`

**Use it for:** turning a repeated workflow into a scoped skill with a clear trigger, reusable resources, fictional tests, and current discovery guidance.

**Who it helps:** anyone who has repeated the same instructions to their AI tool three times and wants the fourth time to be one command.

**Typical output:** a validated skill candidate, explicit installation plan, and fictional first-run evidence. Linking or installation requires a separate requested step.

**Install:**

```powershell
.\install.ps1 skill-builder
```

### `session-handoff`

**Use it for:** ending a work session with a start-here document capturing state, decisions and why, ordered next steps, and the gotchas that burned time.

**Who it helps:** anyone whose next session starts with twenty minutes of "where was I", or who hands work to teammates or a fresh AI session.

**Typical output:** a `START_HERE.md` readable with zero context, with the first next step precise enough to start typing immediately.

**Install:**

```powershell
.\install.ps1 session-handoff
```

### `agents-md-writer`

**Use it for:** writing a concise repository contract with scoped rules, commands, safety boundaries, and a compatible CLAUDE.md pointer when needed.

**Who it helps:** people running both Claude Code and Codex (or any AGENTS.md-reading agent) on the same workspace who want one skill set serving both.

**Typical output:** a focused AGENTS.md, preserved existing instructions, optional CLAUDE.md pointer, and verification of applicable scope. Skill discovery is kept separate from repository policy.

**Install:**

```powershell
.\install.ps1 agents-md-writer
```

### `ops-status-report`

**Use it for:** a recurring status snapshot of a folder-based workspace: tracked items and their statuses, overdue dates, recent activity, and read-only tool health checks.

**Who it helps:** solo operators and small teams whose workspace holds an honest status report nobody compiles until something is a month overdue.

**Typical output:** a dated ops report ending in an Attention Needed section of three to five bullets ordered by the cost of ignoring them. Read-only except the report file.

**Install:**

```powershell
.\install.ps1 ops-status-report
```

### `screen-recorder`

**Use it for:** recording a drag-selected region of the Windows desktop to a clean, seekable MP4 using FFmpeg, with a floating stop button.

**Who it helps:** anyone making quick demo clips or bug recordings without installing a screen capture suite. Windows only in v1; video only, silent by default.

**Typical output:** a timestamped MP4 in a recordings folder, recorded from a drag-to-crop overlay that stays aligned under display scaling.

**Install:**

```powershell
.\install.ps1 screen-recorder
```

### `remove-ai-image-metadata`

**Use it for:** inspecting and removing explicit C2PA, Content Credentials, or AI-generator metadata from PNG, JPEG, WebP, and GIF files while preserving encoded picture data.

**Who it helps:** creators and operators cleaning owned or authorized image files for privacy, publishing, or asset hygiene without a generic re-save that may alter pixels, animation, orientation, or color behavior.

**Typical output:** a report-first inspection followed by verified clean copies. The helper reparses each written container, confirms matching metadata is gone, and checks that encoded image payload hashes are unchanged.

**Safety boundary:** use only on files you own or are authorized to modify. Removing explicit metadata does not change how an image was created and must not be used to misrepresent provenance or bypass disclosure requirements.

**Install:**

```powershell
.\install.ps1 remove-ai-image-metadata
```

## Safe Install Defaults

- Start with one skill if you are evaluating the library.
- Use the [`visitor paths`](examples/visitor-paths.md) when you want to choose between evaluation, install, and public-proof routes.
- Use the [`public proof index`](examples/public-proof-index.md) when you want one page of install, safety, sample, system, and visual proof assets.
- Use the [`first install proof`](examples/first-install-proof.md) when you want one path from clone to expected review before touching real work.
- Use the [`evaluation checklist`](guides/evaluate-skill-library.md) when you want to score trust, safety, examples, and install readiness before installing.
- Use the [`first skill scorecard`](guides/first-skill-scorecard.md) when several skills look useful and you want to choose one safe first test.
- Use the [`first skill walkthrough`](examples/first-skill-walkthrough.md) when you want to run the selected skill with fake input before touching real work.
- Use the [`first-skill candidate pack`](examples/first-skill-candidate/README.md) when you want ready fake README and docs files for that first review.
- Use the [`first-skill expected review`](examples/first-skill-candidate/expected-review.md) when you want to compare the expected output for that review.
- Use [`QUICK_REFERENCE.md`](../QUICK_REFERENCE.md) when you want one short command and link map.
- Use the [`quick reference walkthrough`](examples/quick-reference-walkthrough.md) when you want clone-to-first-prompt steps.
- Use [`INSTALL.md`](../INSTALL.md) when you need the short command reference.
- Use the [`install FAQ`](guides/install-faq.md) for first skill choice, install-all, target, reload, update, and removal questions.
- Use the [`skill review checklist`](guides/skill-review-checklist.md) before installing unfamiliar or modified skill folders.
- Use the [`install verification guide`](guides/install-verification.md) to confirm the target folder, copied files, reload, and first prompt.
- Use the [`update installed skills guide`](guides/update-installed-skills.md) when you need to refresh a copied skill folder.
- Use the [`update after release proof`](examples/update-after-release-proof.md) when you want to test pull, temporary copy, reinstall, reload, and fake post-update check.
- Use the [`utility skill proof pack`](examples/utility-skill-proof-pack.md) when you want fake output shapes for `web-scraper`, `code-deduplicator`, and `em-dash-remover`.
- Use the [`demo animation v2 walkthrough sample`](examples/demo-animation-v2-walkthrough-sample.md) when you want a public-safe finished demo shape.
- Use the [`release showcase handoff sample`](examples/release-showcase-handoff-sample.md) when you want to align GitHub release, profile copy, website package, live verification, and final status.
- Use the [`GitHub profile proof updater sample`](examples/github-profile-proof-updater-sample.md) when you want a profile asset refresh and proof-trail output shape.
- Use the [`social campaign proof tracker sample`](examples/social-campaign-proof-tracker-sample.md) when you want a LinkedIn/X proof campaign output shape.
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
