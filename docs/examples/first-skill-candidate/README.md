# Example Review Queue

This is a fictional public-release candidate for a first `github-safe-publisher` test.

Use it with the [`first skill walkthrough`](../first-skill-walkthrough.md) when you want a ready fake folder instead of writing your own test files. After running the first prompt, compare your result with [`expected-review.md`](expected-review.md).

## What This Candidate Is

`Example Review Queue` is a fake workflow for routing draft release notes through a human approval step before publication.

The candidate is intentionally small:

```text
first-skill-candidate/
  README.md
  docs/
    example-release-note.md
    example-workflow-summary.md
```

## Why It Is Safe For A First Run

- The project name is fictional.
- The workflow is generalized.
- The docs use fake facts and no customer details.
- The files do not include screenshots, logs, exports, private source, account data, or local machine paths.
- The release process keeps a human approval gate before anything is published.

## Suggested First Prompt

After installing `github-safe-publisher`, point your AI coding tool at this folder and run:

```text
Use $github-safe-publisher to review this fake README and docs folder before public release.
```

## Expected Review Shape

A useful first result should include:

- `READY`, `REVIEW`, or `BLOCK`;
- files inspected;
- scanner result summary;
- manual checks before publication;
- exact next commands for reviewing diffs;
- no commit, push, upload, send, or publish action before human approval.

For a concrete output shape for this exact candidate, use [`expected-review.md`](expected-review.md).

## Related Files

- [`expected-review.md`](expected-review.md)
- [`docs/example-release-note.md`](docs/example-release-note.md)
- [`docs/example-workflow-summary.md`](docs/example-workflow-summary.md)
- [`../first-run-github-safe-publisher.md`](../first-run-github-safe-publisher.md)
- [`../github-safe-publisher-sample-review.md`](../github-safe-publisher-sample-review.md)
