# Security And Responsible Use

JQ AI Skills is a public library of installable AI skill folders. The files in this repo are instructions, examples, scripts, and public documentation; they are not a hosted service.

Use this page to understand what belongs in a security report, what should stay out of public issues, and how to use these skills safely on private work.

## Supported Scope

Security and responsible-use reports are in scope when they involve:

- accidental exposure of credentials, tokens, secrets, account data, or private material in this public repository;
- install scripts that copy, delete, overwrite, or execute more than the documented install path;
- skill instructions that encourage unsafe publication of private data, raw prompts, logs, databases, exports, screenshots, or client-identifying material;
- examples that accidentally use real people, accounts, customer data, internal URLs, or non-public project details;
- metadata or agent instructions that could mislead users about permissions, review gates, or expected output.

General feature requests, copy edits, typo fixes, and documentation improvements can use normal GitHub issues or pull requests.

## How To Report Sensitive Issues

Do not post secrets, credentials, client data, private prompts, logs, exports, screenshots with account UI, or exploit details in a public issue.

For sensitive reports:

1. Use GitHub private vulnerability reporting if it is available on the repository.
2. If private reporting is not available, use the JQ AI SYSTEMS contact page to request a private reporting channel: https://www.ai.joaoqueiros.com/contact
3. Include a short public-safe summary of the issue, affected file path, and suggested severity.
4. Replace any sensitive value with a clear placeholder such as `YOUR_TOKEN_HERE` or `EXAMPLE_CLIENT`.

For public documentation issues that do not include sensitive material, open a normal issue or pull request.

## Responsible Use Rules

Before using any skill on real work:

- Read the skill's `SKILL.md`.
- Start in a test folder.
- Review what files the skill is allowed to inspect or change.
- Do not paste credentials, passwords, tokens, account exports, client data, logs, databases, or private prompts into an AI tool unless you understand where that content will go.
- Review diffs before committing, publishing, sending, or uploading outputs.
- Keep human approval in the loop for outreach, publishing, marketplace, scraping, and client-facing workflows.

The skills are designed to help with repeatable workflows. They do not remove the user's responsibility to review inputs, outputs, permissions, and publication choices.

## Installing Skills Safely

Install only skills you understand.

Before installing a skill:

- Inspect the folder contents.
- Read `SKILL.md`.
- Check any files in `scripts/`, `assets/`, or `references/`.
- Use [`docs/guides/skill-review-checklist.md`](docs/guides/skill-review-checklist.md) to review purpose, permissions, scripts, metadata, sensitive material, and first-run safety.
- Use [`docs/examples/skill-reviewer-sample.md`](docs/examples/skill-reviewer-sample.md) to see a public-safe review shape before installing unfamiliar skills.
- Use [`skill-reviewer`](skills/skill-reviewer/SKILL.md) for third-party skills or unfamiliar instructions.
- Prefer a test target before installing into your main local skills directory.

If a skill contains unclear permissions, hidden data movement, unexpected shell commands, or instructions to bypass review, do not install it.

## Public Publishing Safety

When turning private work into a public GitHub artifact:

- Use [`github-safe-publisher`](skills/github-safe-publisher/SKILL.md).
- Follow [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md).
- Scan public candidates with `skills/github-safe-publisher/scripts/scan_public_safety.py`.
- Use fake data in examples.
- Keep private implementation files, client-specific material, credentials, databases, logs, exports, and raw prompt notes out of public releases.

The scanner is a first pass. A clean scanner result still needs manual diff review.

## Version And Release Notes

Security and responsible-use improvements are documented through:

- [`CHANGELOG.md`](CHANGELOG.md)
- [`docs/announcements/`](docs/announcements/)
- GitHub releases

## No Warranty

This repo is published under the MIT License. The skills are provided as public instructions and helper assets. Review and adapt them for your environment before using them on sensitive, client-facing, or production work.
