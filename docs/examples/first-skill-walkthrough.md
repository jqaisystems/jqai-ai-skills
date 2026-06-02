# First Skill Walkthrough

This walkthrough shows the full path after using the [`first skill scorecard`](../guides/first-skill-scorecard.md).

It uses one fictional first skill run: install `github-safe-publisher`, test it with fake public-release files, and compare the result with the expected output shape.

Do not use real credentials, account exports, logs, customer records, screenshots, unpublished prompts, or private project notes for a first run.

## Scenario

A builder wants to publish a tiny README and docs update for a fictional workflow called `Example Review Queue`.

The builder has already evaluated the library and wants one safe, testable first skill rather than installing everything.

## 1. Score The First Skill

Candidate: [`github-safe-publisher`](../../skills/github-safe-publisher/SKILL.md)

| Check | Score | Reason |
|---|---:|---|
| Job match | 2 | The job is public GitHub publishing. |
| Safe first test | 2 | The input can be fake README and docs files. |
| Output clarity | 2 | The expected result is a `READY`, `REVIEW`, or `BLOCK` verdict. |
| Install confidence | 2 | The repo has one-skill install commands and verification docs. |
| Reuse value | 2 | The same review habit applies to future releases, examples, and case studies. |

Decision:

```text
Skill: github-safe-publisher
Score out of 10: 10
Verdict: READY
First safe input: fake README and docs files for Example Review Queue
Expected output to compare: verdict, files inspected, scanner summary, manual checks, next commands
Next step: install to a temporary target, then run the first prompt
```

## 2. Review The Skill Folder

Before installing, open:

- [`../../skills/github-safe-publisher/SKILL.md`](../../skills/github-safe-publisher/SKILL.md)
- [`../../skills/github-safe-publisher/references/public-safety-boundaries.md`](../../skills/github-safe-publisher/references/public-safety-boundaries.md)
- [`../../skills/github-safe-publisher/references/release-workflow.md`](../../skills/github-safe-publisher/references/release-workflow.md)
- [`../../skills/github-safe-publisher/scripts/scan_public_safety.py`](../../skills/github-safe-publisher/scripts/scan_public_safety.py)

Confirm that the skill:

- explains its purpose in plain language;
- names what must not be published;
- uses a scanner as a guardrail, not as the only review;
- requires manual diff review before commit or push;
- does not ask for credentials, account data, logs, exports, or private notes.

## 3. Test A Temporary Install

Use a disposable target before installing into your normal skills folder.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\first-skill-test"
Test-Path ".tmp\first-skill-test\github-safe-publisher\SKILL.md"
```

macOS/Linux:

```bash
./install.sh --target .tmp/first-skill-test github-safe-publisher
test -f .tmp/first-skill-test/github-safe-publisher/SKILL.md && echo "installed"
```

Expected result: the copied folder contains `SKILL.md`, `agents/openai.yaml`, `references/`, and `scripts/`.

Compare with [`install-smoke-test-sample.md`](install-smoke-test-sample.md) if the command output is unclear.

## 4. Prepare A Fake Candidate

Use a tiny fake candidate so the first run tests the workflow shape, not private material.

You can use the ready [`first-skill candidate pack`](first-skill-candidate/README.md), or create the same shape yourself:

```text
public-candidate/
  README.md
  docs/
    example-release-note.md
    example-workflow-summary.md
```

Fake `README.md` content:

```markdown
# Example Review Queue

Example Review Queue is a fictional workflow for routing draft release notes through a human approval step before publication.

The sample uses fake names, fake metrics, and public-safe language. It does not include credentials, account data, logs, screenshots, exports, or private implementation notes.
```

Fake `docs/example-workflow-summary.md` content:

```markdown
# Workflow Summary

1. A draft release note is prepared from approved public facts.
2. A reviewer checks for sensitive details and unclear claims.
3. Approved copy is moved into the public release draft.

Review gate: no public release happens until a human approves the final diff.
```

## 5. Run The First Prompt

After the skill is installed and your AI coding tool is reloaded, run:

```text
Use $github-safe-publisher to review this fake README and docs folder before public release.
```

Give the tool only the fake candidate files or a public-safe repo section.

## 6. Read The Verdict

A good first result should include:

- `READY`, `REVIEW`, or `BLOCK`;
- public artifact type and target folder;
- files inspected;
- scanner result summary;
- remaining manual checks;
- exact next commands;
- a reminder not to commit or push until the staged diff is reviewed and approved.

Use `READY` only when the fake files are public-safe and the manual checks are straightforward. For this exact candidate, compare with [`first-skill-candidate/expected-review.md`](first-skill-candidate/expected-review.md).

Use `REVIEW` if wording, links, screenshots, or file names need a human check.

Use `BLOCK` if the candidate includes secrets, account data, logs, exports, customer records, private source files, or local private paths.

## 7. Compare With Expected Samples

Use these sample outputs:

- [`first-skill-candidate/README.md`](first-skill-candidate/README.md)
- [`first-skill-candidate/expected-review.md`](first-skill-candidate/expected-review.md)
- [`first-run-github-safe-publisher.md`](first-run-github-safe-publisher.md)
- [`github-safe-publisher-sample-review.md`](github-safe-publisher-sample-review.md)
- [`install-smoke-test-sample.md`](install-smoke-test-sample.md)

The exact wording can differ. The important part is the review structure: verdict, files, scanner summary, manual checks, and next commands.

## 8. Install For Real Only After The Test

If the temporary install and fake candidate review are clear, install the same skill into your normal tool target.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher
```

macOS/Linux:

```bash
./install.sh github-safe-publisher
```

Then reload the tool and run a small public-safe candidate before using the workflow on larger releases.

## Stop Conditions

Stop and install nothing if:

- the first run needs real credentials, account data, logs, exports, customer records, screenshots, unpublished prompts, or private notes;
- the skill output skips the `READY`, `REVIEW`, or `BLOCK` verdict;
- the scanner result is unclear;
- you cannot identify which files were inspected;
- the next commands include commit, push, upload, send, or publish actions before human approval.

## Related Links

- [`../guides/first-skill-scorecard.md`](../guides/first-skill-scorecard.md)
- [`../../INSTALL.md`](../../INSTALL.md)
- [`../guides/install-verification.md`](../guides/install-verification.md)
- [`first-skill-candidate/README.md`](first-skill-candidate/README.md)
- [`first-skill-candidate/expected-review.md`](first-skill-candidate/expected-review.md)
- [`install-smoke-test-sample.md`](install-smoke-test-sample.md)
- [`first-run-github-safe-publisher.md`](first-run-github-safe-publisher.md)
- [`github-safe-publisher-sample-review.md`](github-safe-publisher-sample-review.md)
- [`../../SECURITY.md`](../../SECURITY.md)
- [`../../TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md)
