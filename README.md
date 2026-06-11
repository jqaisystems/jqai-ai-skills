# JQ AI Skills

Reusable AI skills by JQ AI SYSTEMS.

These skills are small, portable instruction folders for Claude/Codex-style workflows. They are published under the MIT License so you can adapt them for your own local setup.

[![Website](https://img.shields.io/badge/Website-ai.joaoqueiros.com-111827?style=for-the-badge)](https://www.ai.joaoqueiros.com)
[![License](https://img.shields.io/badge/License-MIT-059669?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v0.8.0-2563eb?style=for-the-badge)](https://github.com/jqaisystems/jqai-ai-skills/releases/tag/v0.8.0)
[![Validate skills](https://github.com/jqaisystems/jqai-ai-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/jqaisystems/jqai-ai-skills/actions/workflows/validate.yml)

## Start Here

New here? Pick one route:

| Goal | Start with | Then use |
|---|---|---|
| Understand the library quickly | [`START_HERE.md`](START_HERE.md) | [`docs/examples/visitor-paths.md`](docs/examples/visitor-paths.md) |
| Choose one safe first install | [`docs/guides/first-skill-scorecard.md`](docs/guides/first-skill-scorecard.md) | [`docs/examples/first-skill-walkthrough.md`](docs/examples/first-skill-walkthrough.md) |
| Check trust and public proof | [`docs/guides/evaluate-skill-library.md`](docs/guides/evaluate-skill-library.md) | [`docs/examples/public-proof-index.md`](docs/examples/public-proof-index.md) |
| Install or update skills | [`INSTALL.md`](INSTALL.md) | [`docs/guides/install-verification.md`](docs/guides/install-verification.md) |

Need the compact command map? Use [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md). Want the full catalog? Use [`docs/catalog.md`](docs/catalog.md).

## Preview

![JQ AI Skills overview](assets/skill-library-overview.png)

![Skill folder structure](assets/skill-folder-structure.png)

![Skill packaging demo](assets/skill-packaging-demo.gif)

![Skill install demo](assets/skill-install-demo.gif)

### Launch Video

![JQ AI Skills launch motion preview](assets/jq-ai-skills-launch-preview.gif)

[Watch the 30-second launch video with music](assets/jq-ai-skills-launch-video-with-music.mp4).

The launch video is a promotional preview of the public skill library. Skill installation does not require these media assets.

## Quick Start

If you are new here, start with one skill rather than installing everything:

| If your job is... | Install first | Why |
|---|---|---|
| Public-release safety review | [`github-safe-publisher`](skills/github-safe-publisher/SKILL.md) | Checks sensitive project material before public release. |
| Turning work into public proof | [`case-study-writer`](skills/case-study-writer/SKILL.md) | Converts private project context into a public-safe case study shape. |
| Announcing shipped work | [`release-announcement-writer`](skills/release-announcement-writer/SKILL.md) | Turns changelogs and diffs into release notes, website blurbs, and launch posts. |
| Reviewing third-party skills | [`skill-reviewer`](skills/skill-reviewer/SKILL.md) | Audits skill instructions before you install them locally. |

For first-use help, use [`START_HERE.md`](START_HERE.md), [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md), or the route picker in [`docs/examples/visitor-paths.md`](docs/examples/visitor-paths.md). For install details, use [`INSTALL.md`](INSTALL.md), [`docs/guides/one-minute-install.md`](docs/guides/one-minute-install.md), and [`docs/guides/install-verification.md`](docs/guides/install-verification.md).

Install flow:

1. Pick a skill folder from `skills/`.
2. Copy the whole folder into your local skills directory, or use the install scripts below.
3. Restart or reload your AI coding tool.
4. Invoke the skill by name in your prompt.

Example prompts:

```text
Use $github-safe-publisher to prepare this repo for a public release.
Use $case-study-writer to turn this private project summary into a public-safe case study.
Use $outreach-pipeline-designer to design a safe human-reviewed prospecting workflow.
Use $cold-outreach-writer to draft a cold email for this prospect from my research notes.
Use $lead-scorer to score this lead list against my rubric and rank it.
Use $etsy-listing-optimizer to audit and rewrite a marketplace listing safely.
Use $research-brief-curator to turn public links into a safe weekly research brief.
Use $release-announcement-writer to turn this changelog into release notes and a launch post.
Use $skill-reviewer to audit this downloaded skill before installing it.
Use $em-dash-remover to clean this landing page copy.
Use $code-deduplicator to consolidate repeated formatting helpers in this sample.
Use $brand-voice-linter to check this copy against our voice guide.
Use $php-form-mailer to make this contact form send email without a third-party service.
Use $client-intake-builder to create a branded intake questionnaire for this project.
Use $llms-txt-generator to create an llms.txt for this site.
Use $vault-janitor to scan this folder and report what is safe to clean.
Use $obsidian-daily-note to log this to today's daily note.
Use $idea-inbox to capture this idea into my ideas folder.
Use $demo-animation-v2 to create a responsive animated walkthrough.
```

## Example Artifacts

Every skill ships with public-safe proof: fake-data samples, guides, and checklists a visitor can inspect before installing anything. The short list below covers the main entry points; everything else is one click away.

- [`docs/examples/README.md`](docs/examples/README.md) is the full index of public-safe samples, walkthroughs, workflow bundles, and first-run outputs.
- [`docs/examples/public-proof-index.md`](docs/examples/public-proof-index.md) gathers the install, safety, sample, system, and visual proof assets in one place.
- [`docs/catalog.md`](docs/catalog.md) is the complete catalog of all installable skills, recommended bundles, and safe install defaults.
- [`docs/skill-quality-matrix.md`](docs/skill-quality-matrix.md) compares skill maturity, visible proof, safety sensitivity, and safest install notes.
- [`INSTALL.md`](INSTALL.md), [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md), and the guides in [`docs/guides/`](docs/guides/) cover install, verification, update, review, and first-skill selection routines.
- [`CHANGELOG.md`](CHANGELOG.md), [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md), [`SECURITY.md`](SECURITY.md), [`ROADMAP.md`](ROADMAP.md), and [`SUPPORT.md`](SUPPORT.md) document how this repo is maintained and released.

## Skill Folder Structure

Each skill is packaged as a self-contained folder:

```text
skill-name/
  SKILL.md
  agents/
    openai.yaml
  assets/       optional templates, images, or reusable files
  references/   optional supporting docs
  scripts/      optional helper scripts
```

For a field-by-field walkthrough, use [`docs/guides/skill-anatomy.md`](docs/guides/skill-anatomy.md). To create a new skill, copy [`skills/_template/`](skills/_template/) and replace the placeholder names, descriptions, and prompts.

## Skills Included

### Safety & Publishing

| Skill | File | Use |
|---|---|---|
| GitHub Safe Publisher | [`skills/github-safe-publisher/SKILL.md`](skills/github-safe-publisher/SKILL.md) | Prepare private work for public GitHub releases safely. |
| Skill Reviewer | [`skills/skill-reviewer/SKILL.md`](skills/skill-reviewer/SKILL.md) | Review AI skill files or folders for dangerous behavior. |

### Public Proof

| Skill | File | Use |
|---|---|---|
| Case Study Writer | [`skills/case-study-writer/SKILL.md`](skills/case-study-writer/SKILL.md) | Turn private project work into public-safe case studies. |
| Release Announcement Writer | [`skills/release-announcement-writer/SKILL.md`](skills/release-announcement-writer/SKILL.md) | Turn changelogs and shipped changes into release notes, website blurbs, and launch posts. |

### Growth & Outreach

| Skill | File | Use |
|---|---|---|
| Outreach Pipeline Designer | [`skills/outreach-pipeline-designer/SKILL.md`](skills/outreach-pipeline-designer/SKILL.md) | Design safe human-reviewed prospecting and outreach workflows. |
| Cold Outreach Writer | [`skills/cold-outreach-writer/SKILL.md`](skills/cold-outreach-writer/SKILL.md) | Draft a personalised cold email, subject lines, LinkedIn note, and follow-up from research notes. |
| Lead Scorer | [`skills/lead-scorer/SKILL.md`](skills/lead-scorer/SKILL.md) | Rank a lead list into hot, warm, and cold tiers against your own rubric. |
| Etsy Listing Optimizer | [`skills/etsy-listing-optimizer/SKILL.md`](skills/etsy-listing-optimizer/SKILL.md) | Audit, rewrite, batch, and monitor marketplace listings. |

### Content & Research

| Skill | File | Use |
|---|---|---|
| Research Brief Curator | [`skills/research-brief-curator/SKILL.md`](skills/research-brief-curator/SKILL.md) | Turn public links and notes into source-aware research briefs with review gates. |
| llms.txt Generator | [`skills/llms-txt-generator/SKILL.md`](skills/llms-txt-generator/SKILL.md) | Generate a spec-compliant llms.txt map of a website for AI assistants. |
| Web Scraper | [`skills/web-scraper/SKILL.md`](skills/web-scraper/SKILL.md) | Extract public page content safely into structured notes. |
| Em Dash Remover | [`skills/em-dash-remover/SKILL.md`](skills/em-dash-remover/SKILL.md) | Clean one common AI-writing tell from copy. |
| Brand Voice Linter | [`skills/brand-voice-linter/SKILL.md`](skills/brand-voice-linter/SKILL.md) | Lint copy against a brand voice guide: buzzwords, hedging, superlatives, AI tells. |

### Dev Workflow

| Skill | File | Use |
|---|---|---|
| Code Deduplicator | [`skills/code-deduplicator/SKILL.md`](skills/code-deduplicator/SKILL.md) | Safely consolidate repeated code patterns. |
| PHP Form Mailer | [`skills/php-form-mailer/SKILL.md`](skills/php-form-mailer/SKILL.md) | Wire any HTML form to a two-email PHP handler with no form SaaS. |
| Client Intake Builder | [`skills/client-intake-builder/SKILL.md`](skills/client-intake-builder/SKILL.md) | Generate a branded single-file client intake questionnaire. |
| Vault Janitor | [`skills/vault-janitor/SKILL.md`](skills/vault-janitor/SKILL.md) | Find folder junk and report it with sizes; deletes only what you approve. |

### Notes & Productivity

| Skill | File | Use |
|---|---|---|
| Obsidian Daily Note | [`skills/obsidian-daily-note/SKILL.md`](skills/obsidian-daily-note/SKILL.md) | Append to today's Obsidian daily note from the terminal. |
| Idea Inbox | [`skills/idea-inbox/SKILL.md`](skills/idea-inbox/SKILL.md) | Capture raw ideas as dated, tagged, indexed markdown files. |

### Demo & Presentation

| Skill | File | Use |
|---|---|---|
| Demo Animation | [`skills/demo-animation/SKILL.md`](skills/demo-animation/SKILL.md) | Build legacy desktop-oriented product/demo walkthroughs. |
| Demo Animation V2 | [`skills/demo-animation-v2/SKILL.md`](skills/demo-animation-v2/SKILL.md) | Build recommended responsive demo walkthroughs. Includes [`assets/template.html`](skills/demo-animation-v2/assets/template.html). |

## Which Skill Should I Use?

For the fastest guided install, see [`docs/guides/one-minute-install.md`](docs/guides/one-minute-install.md). To score the safest first install, see [`docs/guides/first-skill-scorecard.md`](docs/guides/first-skill-scorecard.md). To prove the full first-install path, see [`docs/examples/first-install-proof.md`](docs/examples/first-install-proof.md). To run the selected skill with fake input, see [`docs/examples/first-skill-walkthrough.md`](docs/examples/first-skill-walkthrough.md), the [`first-skill candidate pack`](docs/examples/first-skill-candidate/README.md), and its [`expected review`](docs/examples/first-skill-candidate/expected-review.md). For the detailed visitor guide, see [`docs/guides/skill-selection.md`](docs/guides/skill-selection.md). To understand the folder contract, see [`docs/guides/skill-anatomy.md`](docs/guides/skill-anatomy.md). To review an unfamiliar skill before install, see [`docs/guides/skill-review-checklist.md`](docs/guides/skill-review-checklist.md). For the complete catalog, see [`docs/catalog.md`](docs/catalog.md).

| If you want to... | Start with |
|---|---|
| Publish private work without leaking secrets | [`github-safe-publisher`](skills/github-safe-publisher/SKILL.md) |
| Turn internal work into client-readable proof | [`case-study-writer`](skills/case-study-writer/SKILL.md) |
| Design a review-first sales or prospecting workflow | [`outreach-pipeline-designer`](skills/outreach-pipeline-designer/SKILL.md) |
| Draft a personalised cold email from research notes | [`cold-outreach-writer`](skills/cold-outreach-writer/SKILL.md) |
| Decide which leads to contact first | [`lead-scorer`](skills/lead-scorer/SKILL.md) |
| Improve a marketplace listing safely | [`etsy-listing-optimizer`](skills/etsy-listing-optimizer/SKILL.md) |
| Turn public links into a reviewed research brief | [`research-brief-curator`](skills/research-brief-curator/SKILL.md) |
| Package release notes or a launch post | [`release-announcement-writer`](skills/release-announcement-writer/SKILL.md) |
| Review a downloaded skill before installing it | [`skill-reviewer`](skills/skill-reviewer/SKILL.md) |
| Extract structured data from public pages | [`web-scraper`](skills/web-scraper/SKILL.md) |
| Clean AI-ish punctuation from copy | [`em-dash-remover`](skills/em-dash-remover/SKILL.md) |
| Enforce a full brand voice guide on copy | [`brand-voice-linter`](skills/brand-voice-linter/SKILL.md) |
| Reduce repeated code patterns | [`code-deduplicator`](skills/code-deduplicator/SKILL.md) |
| Make a static-site form send email without a service | [`php-form-mailer`](skills/php-form-mailer/SKILL.md) |
| Onboard clients with a branded questionnaire | [`client-intake-builder`](skills/client-intake-builder/SKILL.md) |
| Make a website readable and citable by AI assistants | [`llms-txt-generator`](skills/llms-txt-generator/SKILL.md) |
| Find out what is eating a folder's disk space | [`vault-janitor`](skills/vault-janitor/SKILL.md) |
| Log work and thoughts to an Obsidian daily note | [`obsidian-daily-note`](skills/obsidian-daily-note/SKILL.md) |
| Capture ideas without losing them in the repo root | [`idea-inbox`](skills/idea-inbox/SKILL.md) |
| Build a responsive walkthrough demo | [`demo-animation-v2`](skills/demo-animation-v2/SKILL.md) |
| Build a legacy desktop-only walkthrough demo | [`demo-animation`](skills/demo-animation/SKILL.md) |

## Why This Matters

The skills repo is the technical credibility layer behind the client-facing systems. It shows how JQ AI SYSTEMS packages repeatable AI workflows into reusable instructions, review steps, and safety checks instead of relying on one-off prompts.

## Installation

For the short command reference, see [`INSTALL.md`](INSTALL.md). After installing, confirm the setup with [`docs/guides/install-verification.md`](docs/guides/install-verification.md). If a skill does not show up after install, see [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

For Claude Code/Codex-style local skills:

1. Create a local skills folder if you do not already have one.
2. Copy the selected skill folder from `skills/`.
3. Place the whole folder in your local skills directory.
4. Restart or reload your AI coding tool if needed.
5. Ask the tool to use the skill by name.

Only install skills you understand. Review the instructions before using them on private projects.

## Codex Install

Copy a whole skill folder into your Codex skills directory, then restart Codex so the skill list reloads.

Fast install from this repo:

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher
.\install.ps1 case-study-writer
.\install.ps1 outreach-pipeline-designer
.\install.ps1 etsy-listing-optimizer
.\install.ps1 research-brief-curator
.\install.ps1 -All
```

macOS/Linux:

```bash
chmod +x ./install.sh
./install.sh github-safe-publisher
./install.sh case-study-writer
./install.sh outreach-pipeline-designer
./install.sh etsy-listing-optimizer
./install.sh research-brief-curator
./install.sh --all
```

List available skills:

```powershell
.\install.ps1 -List
```

```bash
./install.sh --list
```

Manual install:

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\web-scraper" "$env:USERPROFILE\.codex\skills\web-scraper"
```

macOS/Linux:

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/web-scraper ~/.codex/skills/web-scraper
```

Then invoke it by name:

```text
Use $web-scraper to build a browser console scraper for this public paginated website.
```

## Contributing

Use [`CONTRIBUTING.md`](CONTRIBUTING.md) for the expected folder format, metadata requirements, safety rules, and pre-submission checklist. For a public-safe proposal shape, use [`docs/examples/skill-request-example.md`](docs/examples/skill-request-example.md).

## Safety Notes

- These files are instructions, not secrets.
- Do not paste sensitive keys, sign-in material, customer records, account exports, or unreleased project notes into prompts unless you fully understand where they will go.
- Use [`SECURITY.md`](SECURITY.md) for responsible-use rules and sensitive issue reporting.
- The `skill-reviewer` skill exists to help inspect third-party skill files before installing them.
- Use [`docs/guides/skill-review-checklist.md`](docs/guides/skill-review-checklist.md) before installing unfamiliar or modified skill folders.
- Run new skills on a test folder before using them in production work.

## License

Released under the [MIT License](LICENSE).

More systems and case studies: [ai.joaoqueiros.com/systems](https://www.ai.joaoqueiros.com/systems)

Want a custom workflow built around your team? Start here: [ai.joaoqueiros.com/contact](https://www.ai.joaoqueiros.com/contact)
