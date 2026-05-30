# Skill Quality Matrix

Current as of v0.5.0.

Use this matrix to compare the public skills by maturity, example coverage, safety sensitivity, and install notes. It is a practical adoption guide, not a certification.

## Matrix

| Skill | Category | Public maturity | Example coverage | Safety sensitivity | Install notes |
|---|---|---|---|---|---|
| [`github-safe-publisher`](../skills/github-safe-publisher/SKILL.md) | Safety and publishing | Core public skill | First-run sample and fake-file review example | High | Recommended first install for public release work. |
| [`case-study-writer`](../skills/case-study-writer/SKILL.md) | Public proof | Core public skill | Public-safe case study sample | High | Use fictional or approved source material only. |
| [`release-announcement-writer`](../skills/release-announcement-writer/SKILL.md) | Public proof | Core public skill | Release notes archive and template reference | Medium | Pair with changelog and release checklist. |
| [`research-brief-curator`](../skills/research-brief-curator/SKILL.md) | Content and research | Core public skill | Sample brief and sample items | Medium | Use public sources or approved notes only. |
| [`outreach-pipeline-designer`](../skills/outreach-pipeline-designer/SKILL.md) | Growth and outreach | Core public skill | Reference workflow and scoring rubric | High | Human review is required before outreach use. |
| [`etsy-listing-optimizer`](../skills/etsy-listing-optimizer/SKILL.md) | Growth and marketplace | Core public skill | Constraint, keyword, and batch references | Medium | Remove shop exports and private metrics before use. |
| [`skill-reviewer`](../skills/skill-reviewer/SKILL.md) | Safety and publishing | Utility skill | README guidance and catalog entry | High | Use before installing third-party or untrusted skills. |
| [`web-scraper`](../skills/web-scraper/SKILL.md) | Content and research | Utility skill | README prompts and catalog entry | Medium | Use on public pages and respect site rules. |
| [`em-dash-remover`](../skills/em-dash-remover/SKILL.md) | Content and copy | Utility skill | README prompts and catalog entry | Low | Lightweight copy cleanup skill. |
| [`code-deduplicator`](../skills/code-deduplicator/SKILL.md) | Dev workflow | Utility skill | README prompts and catalog entry | Medium | Review diffs carefully before applying code changes. |
| [`demo-animation-v2`](../skills/demo-animation-v2/SKILL.md) | Demo and presentation | Recommended demo skill | Includes responsive HTML template asset | Low | Prefer this for new walkthrough demos. |
| [`demo-animation`](../skills/demo-animation/SKILL.md) | Demo and presentation | Legacy demo skill | Legacy engine reference | Low | Keep for older desktop-oriented demos. |

## Reading The Columns

- Public maturity describes how ready the skill is for general public use.
- Example coverage describes the visible examples or references available in this repo.
- Safety sensitivity describes how careful a user should be with private inputs.
- Install notes explain the safest first-use habit for the skill.

## Recommended Adoption Path

1. Start with [`github-safe-publisher`](../skills/github-safe-publisher/SKILL.md).
2. Install one skill and run it on fake or low-risk material.
3. Use [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) if it does not appear after reload.
4. Use [`SECURITY.md`](../SECURITY.md) before working with sensitive or client-facing material.
5. Use [`docs/examples/workflow-bundles.md`](examples/workflow-bundles.md) when you want a multi-skill path.
