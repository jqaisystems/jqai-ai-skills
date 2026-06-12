# Skill Quality Matrix

Current as of v0.8.1.

Use this matrix to compare the public skills by maturity, visible proof, safety sensitivity, and install notes. It is a practical adoption guide, not a certification. For the browsable examples index, use [`docs/examples/README.md`](examples/README.md). For the folder contract behind every skill, use [`docs/guides/skill-anatomy.md`](guides/skill-anatomy.md). For the complete first-install trust path, use [`docs/examples/first-install-proof.md`](examples/first-install-proof.md). For the post-release refresh path, use [`docs/examples/update-after-release-proof.md`](examples/update-after-release-proof.md). For smaller utility skill examples, use [`docs/examples/utility-skill-proof-pack.md`](examples/utility-skill-proof-pack.md). For responsive demo output proof, use [`docs/examples/demo-animation-v2-walkthrough-sample.md`](examples/demo-animation-v2-walkthrough-sample.md). For release-to-showcase handoff proof, use [`docs/examples/release-showcase-handoff-sample.md`](examples/release-showcase-handoff-sample.md).

## Matrix

| Skill | Category | Public maturity | Visible proof | Safety sensitivity | Safest install note |
|---|---|---|---|---|---|
| [`github-safe-publisher`](../skills/github-safe-publisher/SKILL.md) | Safety and publishing | Core first-install skill | First-run sample, fake-file review example, first-skill candidate pack, expected review, first install proof, and update-after-release proof | High | Recommended first install. Run it first on fake files, then review diffs before publishing. |
| [`case-study-writer`](../skills/case-study-writer/SKILL.md) | Public proof | Core public skill | Public-safe case study sample and workflow bundle coverage | High | Use fictional, generalized, or explicitly approved source material only. |
| [`release-announcement-writer`](../skills/release-announcement-writer/SKILL.md) | Public proof | Core public skill | Template reference, fake changelog sample, release announcement archive, release handoff proof, and demo launch bundle coverage | Medium | Pair with changelog facts and release checklist; avoid unsupported claims. |
| [`github-profile-proof-updater`](../skills/github-profile-proof-updater/SKILL.md) | Public proof | New public skill | Profile proof refresh sample, public proof index, catalog entry, and quick reference prompt | Medium | Fetch first, preserve README image paths, verify live GitHub rendering, and avoid local/private paths in proof notes. |
| [`social-campaign-proof-tracker`](../skills/social-campaign-proof-tracker/SKILL.md) | Public proof | New public skill | Social campaign tracker sample, public proof index, catalog entry, and quick reference prompt | Medium | Track only public links and human-reviewed replies; do not invent engagement or store private analytics exports. |
| [`research-brief-curator`](../skills/research-brief-curator/SKILL.md) | Content and research | Core public skill | Sample brief, sample items JSON, and content/research bundle coverage | Medium | Use public sources or approved notes; label anything that needs human review. |
| [`outreach-pipeline-designer`](../skills/outreach-pipeline-designer/SKILL.md) | Growth and outreach | Core public skill | Reference workflow, scoring rubric, fake review-gated pipeline sample, and workflow bundle coverage | High | Keep prospect data, credentials, and sending actions outside the skill output. |
| [`etsy-listing-optimizer`](../skills/etsy-listing-optimizer/SKILL.md) | Growth and marketplace | Core public skill | Constraint reference, keyword workflow, batch notes, and fictional listing audit sample | Medium | Remove shop exports, private metrics, customer data, and live account details before use. |
| [`skill-reviewer`](../skills/skill-reviewer/SKILL.md) | Safety and review | Utility skill | Review checklist, sample `READY`/`REVIEW`/`BLOCK` decisions, catalog entry, and quick reference links | High | Use before installing third-party, downloaded, or modified skill folders. |
| [`web-scraper`](../skills/web-scraper/SKILL.md) | Content and extraction | Utility skill | Utility proof pack, catalog entry, workflow bundle coverage, and public-page usage notes | Medium | Use only on public or authorized pages and respect site rules. |
| [`em-dash-remover`](../skills/em-dash-remover/SKILL.md) | Content and copy | Utility skill | Utility proof pack, catalog entry, and common prompt examples | Low | Lightweight copy cleanup; preserve meaning and review edited copy. |
| [`code-deduplicator`](../skills/code-deduplicator/SKILL.md) | Development workflow | Utility skill | Utility proof pack, catalog entry, and common prompt examples | Medium | Review diffs carefully before applying code changes. |
| [`demo-animation-v2`](../skills/demo-animation-v2/SKILL.md) | Demo and presentation | Recommended demo skill | Responsive HTML template asset, rendered walkthrough sample, catalog entry, and demo launch bundle coverage | Low | Prefer this for new walkthrough demos; review the sample for pacing, captions, mobile controls, and safety checks. |
| [`demo-animation`](../skills/demo-animation/SKILL.md) | Demo and presentation | Legacy demo skill | Legacy engine reference and catalog entry | Low | Keep for older desktop-oriented demos; use v2 for new responsive demos. |
| [`php-form-mailer`](../skills/php-form-mailer/SKILL.md) | Development workflow | New public skill | Catalog entry and README prompt examples | Medium | Configure your own addresses via the ask-once config; test with a curl POST before going live. |
| [`client-intake-builder`](../skills/client-intake-builder/SKILL.md) | Development workflow | New public skill | Catalog entry and README prompt examples | Low | Review the generated form in a browser before sending it to a client. |
| [`cold-outreach-writer`](../skills/cold-outreach-writer/SKILL.md) | Growth and outreach | New public skill | Catalog entry and README prompt examples | High | Drafts only; a human reviews and sends every message from their own inbox. |
| [`lead-scorer`](../skills/lead-scorer/SKILL.md) | Growth and outreach | New public skill | Catalog entry and README prompt examples | High | Keep lead data local; write the rubric before scoring and audit reasons, not just numbers. |
| [`brand-voice-linter`](../skills/brand-voice-linter/SKILL.md) | Content and copy | New public skill | Catalog entry and README prompt examples | Low | Run report-only first; apply fixes after reviewing the suggested rewrites. |
| [`obsidian-daily-note`](../skills/obsidian-daily-note/SKILL.md) | Notes and productivity | New public skill | Catalog entry and README prompt examples | Low | Confirm the vault path on first run; the skill is append-only by rule. |
| [`idea-inbox`](../skills/idea-inbox/SKILL.md) | Notes and productivity | New public skill | Catalog entry and README prompt examples | Low | Point it at a dedicated ideas folder; it never edits or deletes existing ideas. |
| [`llms-txt-generator`](../skills/llms-txt-generator/SKILL.md) | Content and AI search | New public skill | Catalog entry and README prompt examples | Medium | Review the summary blockquote personally; it is the line AIs will quote. |
| [`vault-janitor`](../skills/vault-janitor/SKILL.md) | Development workflow | New public skill | Catalog entry and README prompt examples | High | Run the read-only scan first; approve specific groups and prefer the archive over hard deletion. |

## Coverage Signals

| Signal | Where to inspect it |
|---|---|
| First install path | [`docs/examples/first-install-proof.md`](examples/first-install-proof.md) |
| Update after release path | [`docs/examples/update-after-release-proof.md`](examples/update-after-release-proof.md) |
| First skill choice | [`docs/guides/first-skill-scorecard.md`](guides/first-skill-scorecard.md) |
| Fake first-run files | [`docs/examples/first-skill-candidate/README.md`](examples/first-skill-candidate/README.md) |
| Expected first review | [`docs/examples/first-skill-candidate/expected-review.md`](examples/first-skill-candidate/expected-review.md) |
| Public proof map | [`docs/examples/public-proof-index.md`](examples/public-proof-index.md) |
| Visitor routes | [`docs/examples/visitor-paths.md`](examples/visitor-paths.md) |
| Install verification | [`docs/guides/install-verification.md`](guides/install-verification.md) |
| Public-safe samples | [`docs/examples/README.md`](examples/README.md) |
| Utility proof pack | [`docs/examples/utility-skill-proof-pack.md`](examples/utility-skill-proof-pack.md) |
| Demo walkthrough sample | [`docs/examples/demo-animation-v2-walkthrough-sample.md`](examples/demo-animation-v2-walkthrough-sample.md) |
| Release showcase handoff | [`docs/examples/release-showcase-handoff-sample.md`](examples/release-showcase-handoff-sample.md) |
| Full catalog | [`docs/catalog.md`](catalog.md) |

## Reading The Columns

- Public maturity describes how ready the skill is for general public use.
- Visible proof describes the examples, references, or proof assets a visitor can inspect before installing.
- Safety sensitivity describes how careful a user should be with private inputs.
- Safest install note explains the safest first-use habit for the skill.

## Recommended Adoption Path

1. Start with [`github-safe-publisher`](../skills/github-safe-publisher/SKILL.md).
2. Follow the [`first install proof`](examples/first-install-proof.md) from clone to expected review.
3. Use the [`first-skill candidate pack`](examples/first-skill-candidate/README.md) so the first run uses fake files.
4. Compare your result with the [`expected first review`](examples/first-skill-candidate/expected-review.md).
5. Use the [`update after release proof`](examples/update-after-release-proof.md) when refreshing an installed skill after a new release.
6. Use [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) if the skill does not appear after reload.
7. Use [`SECURITY.md`](../SECURITY.md) before working with sensitive or client-facing material.
8. Use [`docs/examples/workflow-bundles.md`](examples/workflow-bundles.md) when you want a multi-skill path.
9. Use [`docs/examples/release-showcase-handoff-sample.md`](examples/release-showcase-handoff-sample.md) when a release needs profile, website, upload package, and live verification alignment.
10. Use [`docs/guides/skill-anatomy.md`](guides/skill-anatomy.md) before adapting or creating a skill folder.

## Current Gaps To Watch

- Utility skills now have a shared fake-output proof pack. Future releases can split those into separate per-skill samples if the public library needs deeper proof.
- `demo-animation-v2` now has a public-safe walkthrough sample. Future releases can add a real rendered media artifact if the library needs visual proof beyond the sample page.
- Release handoff now has a public-safe sample. Future releases can add a shorter operator checklist if the handoff routine needs a compact daily-use version.

These are not blockers. They are the next places to improve if the public library needs more proof depth.
