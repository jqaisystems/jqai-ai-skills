# Expected Review: Example Review Queue

This is the expected `github-safe-publisher` review shape for the ready [`first-skill candidate pack`](README.md).

Use it as a comparison after running the first prompt on the fake `Example Review Queue` files. The exact wording can differ, but the review should preserve the same decision, file list, scanner summary, manual checks, and no-publish-before-approval gate.

## Prompt Reviewed

```text
Use $github-safe-publisher to review this fake README and docs folder before public release.
```

## Verdict

READY

## Public Artifact Type And Target Folder

Public-safe README and docs candidate for a fictional GitHub workflow example.

Target folder:

```text
docs/examples/first-skill-candidate/
```

## Files Inspected

- `README.md`
- `docs/example-release-note.md`
- `docs/example-workflow-summary.md`

## Scanner Result Summary

Command:

```bash
python skills/github-safe-publisher/scripts/scan_public_safety.py docs/examples/first-skill-candidate
```

Expected result:

```text
READY: no common safety risks found.
```

## Manual Checks Still Required

- Confirm `Example Review Queue` is fictional.
- Confirm all workflow details are generalized and safe for public examples.
- Confirm no screenshots, logs, exports, account data, private source, or local machine paths are included.
- Confirm the final public diff contains only the intended fake candidate files.
- Confirm a human has reviewed the unstaged and staged diffs before any commit, push, upload, send, or publish action.

## Exact Next Commands

Run these commands from the repository root after reviewing the candidate manually:

```bash
git status --short
git diff -- docs/examples/first-skill-candidate/README.md docs/examples/first-skill-candidate/docs/example-release-note.md docs/examples/first-skill-candidate/docs/example-workflow-summary.md
python skills/github-safe-publisher/scripts/scan_public_safety.py docs/examples/first-skill-candidate
git add docs/examples/first-skill-candidate/README.md docs/examples/first-skill-candidate/docs/example-release-note.md docs/examples/first-skill-candidate/docs/example-workflow-summary.md
git diff --cached
```

Do not commit or push until the staged diff is intentional and a human has approved publication.

## Why This Is READY

| Check | Result |
|---|---|
| Fictional project name | READY |
| Generalized workflow | READY |
| Fake release note | READY |
| Fake workflow summary | READY |
| Human approval gate | READY |
| Sensitive material | READY: none found in the candidate |

## Stop Conditions

Use `BLOCK` instead of `READY` if a real first-run candidate includes access values, account exports, customer records, screenshots from private tools, copied private conversations, unpublished project notes, private source, local machine paths, or files outside the intended candidate folder.

Use `REVIEW` if the wording may be safe but still needs a human check, such as a product name that could be real, a link that needs confirmation, or a screenshot note that must be replaced with a recreated public-safe example.
