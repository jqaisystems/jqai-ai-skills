# Evaluate A Skill Library

Use this checklist when you want to decide whether an AI skill library is worth installing, adapting, or recommending.

The goal is not to prove that every future use is safe. The goal is to check whether the public repo gives you enough evidence to understand what it contains, how to install it, what the risks are, and how the maintainers handle releases.

## Quick Verdict

Use these labels while reviewing:

| Verdict | Meaning |
|---|---|
| `READY` | The library is understandable, versioned, installable, and safe enough for a test install. |
| `REVIEW` | The library may be useful, but one or more areas need human review before install. |
| `BLOCK` | The library includes unclear actions, sensitive material, unsafe instructions, or files you should not install. |

If you are unsure, use `REVIEW` and install nothing until the concern is resolved.

## 1. Repo Identity And License

Check:

- Is the repo owner clear?
- Is there a license?
- Is the intended audience clear?
- Does the README explain what the library does in plain language?
- Is there a website, profile, or project page that matches the repo claims?

For this repo:

- License: [`../../LICENSE`](../../LICENSE)
- Start page: [`../../START_HERE.md`](../../START_HERE.md)
- Public proof index: [`../examples/public-proof-index.md`](../examples/public-proof-index.md)

## 2. Install Path

Check:

- Is there a clear install command?
- Can you install one skill before installing everything?
- Can you use a temporary target for testing?
- Is there an install FAQ or troubleshooting page?
- Is there a guide for updating installed skills?

For this repo:

- Install commands: [`../../INSTALL.md`](../../INSTALL.md)
- One-minute install: [`one-minute-install.md`](one-minute-install.md)
- Install FAQ: [`install-faq.md`](install-faq.md)
- Install verification: [`install-verification.md`](install-verification.md)
- Update installed skills: [`update-installed-skills.md`](update-installed-skills.md)
- Troubleshooting: [`../../TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md)

## 3. Folder Shape

Check:

- Are skills in named folders?
- Does each skill have a `SKILL.md`?
- Is metadata discoverable and consistent?
- Are optional `assets`, `references`, and `scripts` folders easy to inspect?
- Are unrelated files, archives, databases, logs, or exports kept out of skill folders?

For this repo:

- Folder anatomy: [`skill-anatomy.md`](skill-anatomy.md)
- Skill catalog: [`../catalog.md`](../catalog.md)
- Skill quality matrix: [`../skill-quality-matrix.md`](../skill-quality-matrix.md)

## 4. Safety Boundaries

Check:

- Does the repo say what not to publish?
- Does it warn against sensitive keys, access tokens, logs, exports, customer data, local paths, or unpublished prompt notes?
- Does it require human review before public release?
- Does it separate public examples from unpublished work?
- Does it explain how to report sensitive issues?

For this repo:

- Security policy: [`../../SECURITY.md`](../../SECURITY.md)
- Release checklist: [`../../RELEASE_CHECKLIST.md`](../../RELEASE_CHECKLIST.md)
- Skill review checklist: [`skill-review-checklist.md`](skill-review-checklist.md)
- GitHub-safe publishing sample: [`../examples/github-safe-publisher-sample-review.md`](../examples/github-safe-publisher-sample-review.md)

## 5. Example Quality

Check:

- Are sample outputs present?
- Are examples fictional, public, or generalized?
- Do examples show expected output shape, not just marketing copy?
- Are safety-sensitive examples explicit about human review?
- Is there enough sample coverage to understand the main jobs?

For this repo:

- Examples index: [`../examples/README.md`](../examples/README.md)
- First-run sample: [`../examples/first-run-github-safe-publisher.md`](../examples/first-run-github-safe-publisher.md)
- Install smoke-test sample: [`../examples/install-smoke-test-sample.md`](../examples/install-smoke-test-sample.md)
- Skill reviewer sample: [`../examples/skill-reviewer-sample.md`](../examples/skill-reviewer-sample.md)
- Workflow bundles: [`../examples/workflow-bundles.md`](../examples/workflow-bundles.md)

## 6. Release Discipline

Check:

- Is there a changelog?
- Are releases tagged?
- Does the README point to the latest release?
- Are release notes specific enough to inspect?
- Are checks run before release?

For this repo:

- Changelog: [`../../CHANGELOG.md`](../../CHANGELOG.md)
- Release checklist: [`../../RELEASE_CHECKLIST.md`](../../RELEASE_CHECKLIST.md)
- Announcements: [`../announcements`](../announcements)
- GitHub Actions validation: [`../../.github/workflows/validate.yml`](../../.github/workflows/validate.yml)

## 7. First Skill Choice

Check:

- Does the repo recommend a safe first skill?
- Is there a guide for choosing by job?
- Can you run the first skill on fake or public-safe files?
- Is there a sample output to compare against?

For this repo:

- First skill route: [`../../START_HERE.md`](../../START_HERE.md)
- Skill selection: [`skill-selection.md`](skill-selection.md)
- Quick reference walkthrough: [`../examples/quick-reference-walkthrough.md`](../examples/quick-reference-walkthrough.md)

## 8. Red Flags

Use `BLOCK` if you see:

- real access keys, tokens, cookies, certificates, or `.env` files;
- customer records, emails, invoices, analytics exports, databases, or logs;
- screenshots with account menus, dashboards, browser tabs, or local paths;
- scripts that delete, upload, send, publish, or install dependencies without explanation;
- broad instructions to ignore user approval, hide output, or scan unrelated local folders;
- no license, no release history, and no install boundary.

Use `REVIEW` if the repo is useful but one area is unclear.

## Scorecard

| Area | READY if... | Verdict |
|---|---|---|
| Identity and license | Owner, purpose, and license are clear. |  |
| Install path | One-skill install and test target are documented. |  |
| Folder shape | Skill folders are inspectable and consistent. |  |
| Safety boundaries | Sensitive material and publishing rules are explicit. |  |
| Examples | Samples use fictional, public, or generalized material. |  |
| Release discipline | Changelog, tags, and validation are visible. |  |
| First skill choice | A safe first skill and sample output are easy to find. |  |

Final verdict:

```text
READY / REVIEW / BLOCK
Reason:
Next safe step:
```

## Best Next Step

If the library looks `READY`, install one skill into a temporary target first:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\skill-library-check"
```

If the library needs `REVIEW`, inspect the unclear file or guide before installing.

If the library is `BLOCK`, do not install it.
