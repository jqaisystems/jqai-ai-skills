# Quick Reference

Use this page when you want the shortest command and link map for JQ AI Skills.

For the guided path, start with [`START_HERE.md`](START_HERE.md). For full install details, use [`INSTALL.md`](INSTALL.md). For install questions, use [`docs/guides/install-faq.md`](docs/guides/install-faq.md).

## First Choice

| Need | Use |
|---|---|
| Try one safe first skill | [`github-safe-publisher`](skills/github-safe-publisher/SKILL.md) |
| Choose a visitor route | [`docs/examples/visitor-paths.md`](docs/examples/visitor-paths.md) |
| Inspect public proof assets | [`docs/examples/public-proof-index.md`](docs/examples/public-proof-index.md) |
| Prove the first install path | [`docs/examples/first-install-proof.md`](docs/examples/first-install-proof.md) |
| Prove a post-release update path | [`docs/examples/update-after-release-proof.md`](docs/examples/update-after-release-proof.md) |
| Inspect utility output examples | [`docs/examples/utility-skill-proof-pack.md`](docs/examples/utility-skill-proof-pack.md) |
| Inspect verified image-metadata cleanup output | [`docs/examples/remove-ai-image-metadata-sample.md`](docs/examples/remove-ai-image-metadata-sample.md) |
| Inspect responsive demo output | [`docs/examples/demo-animation-v2-walkthrough-sample.md`](docs/examples/demo-animation-v2-walkthrough-sample.md) |
| Inspect release-to-showcase handoff | [`docs/examples/release-showcase-handoff-sample.md`](docs/examples/release-showcase-handoff-sample.md) |
| Evaluate trust and install readiness | [`docs/guides/evaluate-skill-library.md`](docs/guides/evaluate-skill-library.md) |
| Score one first skill | [`docs/guides/first-skill-scorecard.md`](docs/guides/first-skill-scorecard.md) |
| Run the selected skill with fake input | [`docs/examples/first-skill-walkthrough.md`](docs/examples/first-skill-walkthrough.md) |
| Use ready fake first-run files | [`docs/examples/first-skill-candidate/README.md`](docs/examples/first-skill-candidate/README.md) |
| Compare expected first review | [`docs/examples/first-skill-candidate/expected-review.md`](docs/examples/first-skill-candidate/expected-review.md) |
| Choose by job | [`docs/guides/skill-selection.md`](docs/guides/skill-selection.md) |
| Browse every skill | [`docs/catalog.md`](docs/catalog.md) |
| Compare current maturity and proof coverage | [`docs/skill-quality-matrix.md`](docs/skill-quality-matrix.md) |
| Understand folder shape | [`docs/guides/skill-anatomy.md`](docs/guides/skill-anatomy.md) |
| Review before install | [`docs/guides/skill-review-checklist.md`](docs/guides/skill-review-checklist.md) |

## Install Commands

List skills:

```powershell
.\install.ps1 -List
```

```bash
chmod +x ./install.sh
./install.sh --list
```

Install the recommended first skill:

```powershell
.\install.ps1 github-safe-publisher
```

```bash
./install.sh github-safe-publisher
```

Test an install target first:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\skill-install-smoke"
```

```bash
./install.sh --target .tmp/skill-install-smoke github-safe-publisher
```

Install all skills only after review:

```powershell
.\install.ps1 -All
```

```bash
./install.sh --all
```

## After Install

| Step | Link |
|---|---|
| Prove clone to expected review | [`docs/examples/first-install-proof.md`](docs/examples/first-install-proof.md) |
| Walk from clone to first prompt | [`docs/examples/quick-reference-walkthrough.md`](docs/examples/quick-reference-walkthrough.md) |
| Run the selected skill with fake input | [`docs/examples/first-skill-walkthrough.md`](docs/examples/first-skill-walkthrough.md) |
| Use ready fake candidate files | [`docs/examples/first-skill-candidate/README.md`](docs/examples/first-skill-candidate/README.md) |
| Compare expected first review | [`docs/examples/first-skill-candidate/expected-review.md`](docs/examples/first-skill-candidate/expected-review.md) |
| Answer install questions | [`docs/guides/install-faq.md`](docs/guides/install-faq.md) |
| Verify folder, reload, and first prompt | [`docs/guides/install-verification.md`](docs/guides/install-verification.md) |
| Update installed skills | [`docs/guides/update-installed-skills.md`](docs/guides/update-installed-skills.md) |
| Prove update after release | [`docs/examples/update-after-release-proof.md`](docs/examples/update-after-release-proof.md) |
| Compare expected terminal output | [`docs/examples/install-smoke-test-sample.md`](docs/examples/install-smoke-test-sample.md) |
| Fix install or reload issues | [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) |
| See a first-run output shape | [`docs/examples/first-run-github-safe-publisher.md`](docs/examples/first-run-github-safe-publisher.md) |

First prompt:

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

## Common Skill Prompts

```text
Use $github-safe-publisher to prepare this repo for a public release.
Use $case-study-writer to turn this private project summary into a public-safe case study.
Use $release-announcement-writer to turn this changelog into release notes and a launch post.
Use $github-profile-proof-updater to refresh my GitHub profile assets and prepare the proof trail.
Use $social-campaign-proof-tracker to turn this project update into LinkedIn/X copy, alt text, and follow-up notes.
Use $skill-reviewer to audit this downloaded skill before installing it.
Use $web-scraper to create a browser console script for this public demo directory.
Use $code-deduplicator to consolidate repeated formatting helpers in this sample.
Use $em-dash-remover to clean this short product note without changing meaning.
Use $research-brief-curator to turn public links into a safe weekly research brief.
Use $verify-public-claims to check this public copy against the supplied evidence and flag unsupported claims.
Use $research-to-article to turn these sources into a traceable, publication-ready article package.
Use $write-evidence-backed-profile to draft this profile copy from the approved evidence pack.
Use $demo-animation-v2 to create a responsive animated walkthrough.
Use $proposal-writer to draft a proposal for this client from my pricing config and their brief.
Use $follow-up-radar to scan my outreach folder and show me what follow-ups are overdue.
Use $client-workspace-scaffolder to set up a folder for my new client.
Use $discovery-brief to run discovery for this client project.
Use $implement-client-feedback to turn these revision notes into scoped changes and verify every item.
Use $client-delivery-auditor to audit this final package and draft a clear handoff.
Use $website-change-verifier to verify this website change across routes, rendering, metadata, and discovery surfaces.
Use $skill-builder to turn the workflow we just did into a reusable skill.
Use $session-handoff to wrap up this session into a START_HERE.md.
Use $agents-md-writer to register my local skills for both Claude Code and Codex.
Use $ops-status-report to generate this week's status snapshot of my workspace.
Use $screen-recorder to record a region of my screen.
Use $remove-ai-image-metadata to inspect these images, create verified clean copies, and report which explicit AI provenance metadata was removed.
```

## Local Verification And Recovery

The v0.12.0 candidate contains 46 skills. These utilities work independently; generated inventories, reports, snapshots, and receipts stay private by default.

```text
Use $media-spec-checker to check these local files against my JSON rules without modifying them.
Use $automation-state-reconciler to compare these offline snapshots and receipts and draft a repair plan only.
Use $windows-reinstall-planner to prepare a private reinstall checklist from this approved inventory.
```

Proof samples: [media](docs/examples/media-spec-checker-sample.md), [reconciliation](docs/examples/automation-state-reconciler-sample.md), [reinstall planning](docs/examples/windows-reinstall-planner-sample.md).

The inventory also includes four skills added to main in August:

```text
Use $ai-image-run-pacing to plan a generation batch within the service's current limits.
Use $thumbnail-set-designer to draft distinct thumbnail concepts from this title and hook.
Use $thumbnail-legibility-check to compare these candidates at small display sizes.
Use $local-app-public-demo to plan a read-only public demo from this local app.
```

For `research-to-article`, request separate source/video and article dates, credits, embed decisions, and a publication hold for unresolved evidence.

## Public-Safe Publishing

Before publishing public artifacts:

1. Keep the release small.
2. Use fake or approved public examples.
3. Validate the skill folders.
4. Scan changed public files.
5. Review unstaged and staged diffs.
6. Commit, push, tag, and release only after the diff is intentional.

Useful links:

| Need | Link |
|---|---|
| Release routine | [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) |
| Responsible-use policy | [`SECURITY.md`](SECURITY.md) |
| Release history | [`CHANGELOG.md`](CHANGELOG.md) |
| Public examples | [`docs/examples/README.md`](docs/examples/README.md) |
| Public proof index | [`docs/examples/public-proof-index.md`](docs/examples/public-proof-index.md) |
| First install proof | [`docs/examples/first-install-proof.md`](docs/examples/first-install-proof.md) |
| Update after release proof | [`docs/examples/update-after-release-proof.md`](docs/examples/update-after-release-proof.md) |
| Utility skill proof pack | [`docs/examples/utility-skill-proof-pack.md`](docs/examples/utility-skill-proof-pack.md) |
| Demo animation v2 sample | [`docs/examples/demo-animation-v2-walkthrough-sample.md`](docs/examples/demo-animation-v2-walkthrough-sample.md) |
| Release showcase handoff sample | [`docs/examples/release-showcase-handoff-sample.md`](docs/examples/release-showcase-handoff-sample.md) |
| GitHub profile proof updater sample | [`docs/examples/github-profile-proof-updater-sample.md`](docs/examples/github-profile-proof-updater-sample.md) |
| Social campaign proof tracker sample | [`docs/examples/social-campaign-proof-tracker-sample.md`](docs/examples/social-campaign-proof-tracker-sample.md) |
| Evaluation checklist | [`docs/guides/evaluate-skill-library.md`](docs/guides/evaluate-skill-library.md) |
| First skill scorecard | [`docs/guides/first-skill-scorecard.md`](docs/guides/first-skill-scorecard.md) |
| First skill walkthrough | [`docs/examples/first-skill-walkthrough.md`](docs/examples/first-skill-walkthrough.md) |
| First-skill candidate pack | [`docs/examples/first-skill-candidate/README.md`](docs/examples/first-skill-candidate/README.md) |
| First-skill expected review | [`docs/examples/first-skill-candidate/expected-review.md`](docs/examples/first-skill-candidate/expected-review.md) |
| Current quality matrix | [`docs/skill-quality-matrix.md`](docs/skill-quality-matrix.md) |
| Workflow bundles | [`docs/examples/workflow-bundles.md`](docs/examples/workflow-bundles.md) |

Core checks:

```powershell
python tools\validate_skills.py
python skills\github-safe-publisher\scripts\scan_public_safety.py README.md
git diff --check
git status --short
```

## Visitor Links

| Need | Link |
|---|---|
| Start here | [`START_HERE.md`](START_HERE.md) |
| Visitor paths | [`docs/examples/visitor-paths.md`](docs/examples/visitor-paths.md) |
| Public proof index | [`docs/examples/public-proof-index.md`](docs/examples/public-proof-index.md) |
| First install proof | [`docs/examples/first-install-proof.md`](docs/examples/first-install-proof.md) |
| Evaluation checklist | [`docs/guides/evaluate-skill-library.md`](docs/guides/evaluate-skill-library.md) |
| First skill scorecard | [`docs/guides/first-skill-scorecard.md`](docs/guides/first-skill-scorecard.md) |
| First skill walkthrough | [`docs/examples/first-skill-walkthrough.md`](docs/examples/first-skill-walkthrough.md) |
| First-skill candidate pack | [`docs/examples/first-skill-candidate/README.md`](docs/examples/first-skill-candidate/README.md) |
| First-skill expected review | [`docs/examples/first-skill-candidate/expected-review.md`](docs/examples/first-skill-candidate/expected-review.md) |
| Quick reference walkthrough | [`docs/examples/quick-reference-walkthrough.md`](docs/examples/quick-reference-walkthrough.md) |
| Install commands | [`INSTALL.md`](INSTALL.md) |
| Install FAQ | [`docs/guides/install-faq.md`](docs/guides/install-faq.md) |
| Update installed skills | [`docs/guides/update-installed-skills.md`](docs/guides/update-installed-skills.md) |
| Update after release proof | [`docs/examples/update-after-release-proof.md`](docs/examples/update-after-release-proof.md) |
| Utility skill proof pack | [`docs/examples/utility-skill-proof-pack.md`](docs/examples/utility-skill-proof-pack.md) |
| Demo animation v2 sample | [`docs/examples/demo-animation-v2-walkthrough-sample.md`](docs/examples/demo-animation-v2-walkthrough-sample.md) |
| Release showcase handoff sample | [`docs/examples/release-showcase-handoff-sample.md`](docs/examples/release-showcase-handoff-sample.md) |
| Catalog | [`docs/catalog.md`](docs/catalog.md) |
| Quality matrix | [`docs/skill-quality-matrix.md`](docs/skill-quality-matrix.md) |
| Roadmap | [`ROADMAP.md`](ROADMAP.md) |
| Support | [`SUPPORT.md`](SUPPORT.md) |
