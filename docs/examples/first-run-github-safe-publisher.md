# First Run: GitHub Safe Publisher

This example shows what a first `github-safe-publisher` run should feel like after installing the skill.

It uses fake files and fake content. Do not treat it as a scan result for your own repo. Use it as an output shape to compare against when you run the skill locally.

## Fake Scenario

You have a small public candidate with three files:

```text
README.md
docs/example-release-note.md
docs/example-workflow-summary.md
```

The files describe a fictional workflow called `Example Review Queue`. They do not include real account data, unpublished source code, raw logs, exports, or screenshots.

## Prompt

After installing `github-safe-publisher`, run:

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

## Expected Output Shape

~~~markdown
Verdict: READY

Public artifact type and target repo/folder:
README and docs update for a public GitHub repo.

Files inspected:
- README.md
- docs/example-release-note.md
- docs/example-workflow-summary.md

Scanner result summary:
- `python skills/github-safe-publisher/scripts/scan_public_safety.py docs`
- READY: no common safety risks found.

Manual checks still required:
- Confirm the example business and workflow names are fictional.
- Confirm links point only to public pages.
- Confirm no screenshots, exports, logs, account menus, or internal dashboards are included.
- Review `git diff` and `git diff --cached` before any commit.

Exact next commands:

```bash
git status --short
git diff -- README.md docs/example-release-note.md docs/example-workflow-summary.md
python skills/github-safe-publisher/scripts/scan_public_safety.py docs
git add README.md docs/example-release-note.md docs/example-workflow-summary.md
git diff --cached
```

Do not push until the staged diff is intentional and a human has approved publication.
~~~

## What Good Looks Like

A useful first run should make four things obvious:

- Whether the candidate is `READY`, `REVIEW`, or `BLOCK`.
- Which files were inspected.
- What the scanner found.
- What manual checks remain before publishing.

The skill should not skip the review gate. A clean scanner result is a guardrail, not full approval.

## If You Get `REVIEW`

`REVIEW` usually means the content might be publishable, but a human should check something specific before release.

Common examples:

- A phrase sounds like it may refer to a real account or organization.
- A screenshot needs to be replaced with a public-safe mockup.
- A file name looks like it might contain an export or local-only artifact.
- A note mentions implementation detail that should be generalized.

Fix the issue, scan again, and review the diff before staging.

## If You Get `BLOCK`

Stop and remove the risky material before continuing.

Do not rewrite around real secrets, account identifiers, raw exports, logs, or sensitive source files inside the public repo. Remove them from the candidate first, then create a safe summary from scratch.

## Next Steps

- Install the skill with [`docs/guides/one-minute-install.md`](../guides/one-minute-install.md).
- Compare this example with the `github-safe-publisher` sample review: [`github-safe-publisher-sample-review.md`](github-safe-publisher-sample-review.md).
- Use the public publishing bundle when a release also needs a case study or launch note: [`workflow-bundles.md`](workflow-bundles.md).
