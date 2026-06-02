# Public Proof Index

Use this page when you want one place to inspect the public evidence behind JQ AI Skills.

The goal is quick evaluation: what can a visitor inspect without reading the entire repo, installing every skill, or trusting a marketing claim?

All linked examples use fictional, public, or generalized material. They do not include customer records, private exports, account setup, deployment details, local machine paths, raw prompts, logs, credentials, or sensitive implementation notes.

## Fast Review Path

| Question | Open |
|---|---|
| What is this repo? | [`../../START_HERE.md`](../../START_HERE.md) |
| What can I do quickly? | [`../../QUICK_REFERENCE.md`](../../QUICK_REFERENCE.md) |
| Which route fits me? | [`visitor-paths.md`](visitor-paths.md) |
| How do I evaluate trust and install readiness? | [`../guides/evaluate-skill-library.md`](../guides/evaluate-skill-library.md) |
| Which skill should I install first? | [`../guides/first-skill-scorecard.md`](../guides/first-skill-scorecard.md) |
| How do I run the selected skill safely? | [`first-skill-walkthrough.md`](first-skill-walkthrough.md) |
| What skills exist? | [`../catalog.md`](../catalog.md) |
| How mature are the skills? | [`../skill-quality-matrix.md`](../skill-quality-matrix.md) |
| How do I install safely? | [`../guides/one-minute-install.md`](../guides/one-minute-install.md) |
| How do I verify an install? | [`install-smoke-test-sample.md`](install-smoke-test-sample.md) |

Good stopping point: after five minutes, a visitor should know what the repo contains, which skill they would try first, and which sample output they can compare against.

## Install And First-Use Proof

| Proof asset | What it shows |
|---|---|
| [`../../INSTALL.md`](../../INSTALL.md) | Install one skill, all skills, or a custom temporary target. |
| [`../guides/install-faq.md`](../guides/install-faq.md) | Common first-install, target, reload, update, and removal questions. |
| [`../guides/install-verification.md`](../guides/install-verification.md) | Checks for repo root, skill list, copied folder, reload, and first prompt. |
| [`../guides/update-installed-skills.md`](../guides/update-installed-skills.md) | Refresh one installed skill or a reviewed set of installed skills. |
| [`quick-reference-walkthrough.md`](quick-reference-walkthrough.md) | Clone-to-first-prompt walkthrough using the quick reference. |
| [`first-skill-walkthrough.md`](first-skill-walkthrough.md) | Complete fake-data first skill run after scoring `github-safe-publisher`. |
| [`install-smoke-test-sample.md`](install-smoke-test-sample.md) | Expected output shape for a disposable temporary-target install check. |
| [`first-run-github-safe-publisher.md`](first-run-github-safe-publisher.md) | First safe prompt and expected review shape for `github-safe-publisher`. |

## Public-Safe Publishing Proof

| Proof asset | What it shows |
|---|---|
| [`github-safe-publisher-sample-review.md`](github-safe-publisher-sample-review.md) | A fictional safety review with `READY`, scanner summary, manual checks, and next commands. |
| [`case-study-writer-sample.md`](case-study-writer-sample.md) | A public-safe case study shape using a fictional review queue workflow. |
| [`release-announcement-writer-sample.md`](release-announcement-writer-sample.md) | Release notes, website copy, and short launch post from a fake changelog. |
| [`skill-request-example.md`](skill-request-example.md) | A safe request shape for proposing a new skill with fictional material. |
| [`../../SECURITY.md`](../../SECURITY.md) | Responsible-use, install-safety, sensitive issue, and public publishing boundaries. |
| [`../../RELEASE_CHECKLIST.md`](../../RELEASE_CHECKLIST.md) | The safe release routine for validation, scans, diff review, tagging, profile update, and website handoff. |

## Skill Output Samples

| Skill area | Sample |
|---|---|
| Research brief | [`research-brief-curator-sample.md`](research-brief-curator-sample.md) |
| Research sample data | [`research-brief-curator-sample-items.json`](research-brief-curator-sample-items.json) |
| Human-reviewed outreach | [`outreach-pipeline-designer-sample.md`](outreach-pipeline-designer-sample.md) |
| Marketplace listing optimization | [`etsy-listing-optimizer-sample.md`](etsy-listing-optimizer-sample.md) |
| Skill review | [`skill-reviewer-sample.md`](skill-reviewer-sample.md) |
| Multi-skill workflows | [`workflow-bundles.md`](workflow-bundles.md) |

## System And Library Proof

| Asset | What it proves |
|---|---|
| [`../catalog.md`](../catalog.md) | Every public skill has a job, target user, output shape, and install command. |
| [`../guides/evaluate-skill-library.md`](../guides/evaluate-skill-library.md) | A checklist for identity, license, install path, folder shape, examples, safety boundaries, releases, and first-skill choice. |
| [`../guides/first-skill-scorecard.md`](../guides/first-skill-scorecard.md) | A worksheet for choosing one safe, testable first skill instead of installing everything at once. |
| [`first-skill-walkthrough.md`](first-skill-walkthrough.md) | A public-safe walkthrough for scoring, installing, prompting, and interpreting one first skill run. |
| [`../skill-quality-matrix.md`](../skill-quality-matrix.md) | Skill maturity, examples, and safety sensitivity are visible instead of implied. |
| [`../guides/skill-anatomy.md`](../guides/skill-anatomy.md) | The folder contract is documented for maintainers and reviewers. |
| [`../../CHANGELOG.md`](../../CHANGELOG.md) | Release history is versioned and inspectable. |
| [`../../ROADMAP.md`](../../ROADMAP.md) | Near-term direction is public-safe and scoped. |
| [`../../SUPPORT.md`](../../SUPPORT.md) | Support requests have public posting boundaries. |

## Visual Proof Assets

| Asset | What it shows |
|---|---|
| [`../../assets/skill-library-overview.png`](../../assets/skill-library-overview.png) | Overview of the reusable workflow library. |
| [`../../assets/skill-folder-structure.png`](../../assets/skill-folder-structure.png) | The folder structure behind an installable skill. |
| [`../../assets/skill-packaging-demo.gif`](../../assets/skill-packaging-demo.gif) | A workflow being packaged into a reviewable skill. |
| [`../../assets/skill-install-demo.gif`](../../assets/skill-install-demo.gif) | A skill install and invocation flow. |
| [`../../assets/jq-ai-skills-launch-preview.gif`](../../assets/jq-ai-skills-launch-preview.gif) | Launch motion preview for the public library. |
| [`../../assets/jq-ai-skills-launch-video-with-music.mp4`](../../assets/jq-ai-skills-launch-video-with-music.mp4) | Short launch video. |
| [`../../assets/github-social-preview.png`](../../assets/github-social-preview.png) | Stable 2026 GitHub social preview. |

## What This Page Does Not Prove

This page does not prove that every private use case is safe to publish. It proves that the public repo has a visible review habit, public-safe samples, install checks, and versioned release discipline.

Before adapting any sample to real work:

- remove credentials, tokens, account data, logs, exports, database content, local paths, raw prompts, and private implementation details;
- replace real people, organizations, domains, and project names with approved public material or fictional examples;
- run `github-safe-publisher` before publishing anything derived from private work;
- review diffs before committing or releasing public artifacts.

## Best Next Step

If you are evaluating the repo, open [`visitor-paths.md`](visitor-paths.md), [`../guides/evaluate-skill-library.md`](../guides/evaluate-skill-library.md), and [`../guides/first-skill-scorecard.md`](../guides/first-skill-scorecard.md).

If you are ready to try one skill, open [`first-skill-walkthrough.md`](first-skill-walkthrough.md) or [`quick-reference-walkthrough.md`](quick-reference-walkthrough.md).

If you are publishing a public artifact, open [`github-safe-publisher-sample-review.md`](github-safe-publisher-sample-review.md) and [`../../RELEASE_CHECKLIST.md`](../../RELEASE_CHECKLIST.md).
