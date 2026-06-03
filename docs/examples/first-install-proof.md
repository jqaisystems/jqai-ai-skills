# First Install Proof

Use this page when you want one end-to-end proof trail before installing JQ AI Skills into your normal AI coding tool.

The goal is simple: a visitor should be able to clone the repo, choose one safe first skill, install it into a disposable target, verify the copied folder, run a fake candidate review, and compare the result with the expected output.

This proof trail uses `github-safe-publisher` because it teaches the core safety pattern used across the library:

```text
choose one skill -> test the install -> use fake files -> inspect the verdict -> publish only after review
```

## What This Proves

| Step | Proof |
|---|---|
| Clone works | The repo contains install scripts, skill folders, examples, and validation docs. |
| First choice is clear | The first skill scorecard recommends one safe, testable skill. |
| Install is inspectable | The installer can copy one whole skill folder to a temporary target. |
| Folder contract is visible | The copied folder includes `SKILL.md`, metadata, references, and scripts where needed. |
| First run is safe | The first prompt uses fictional files, not real project material. |
| Output can be checked | The expected review shows the target verdict shape and manual approval gate. |

## 1. Clone The Repo

Windows PowerShell:

```powershell
git clone https://github.com/jqaisystems/jqai-ai-skills.git
cd jqai-ai-skills
```

macOS/Linux:

```bash
git clone https://github.com/jqaisystems/jqai-ai-skills.git
cd jqai-ai-skills
```

Open the short map:

- [`../../QUICK_REFERENCE.md`](../../QUICK_REFERENCE.md)
- [`quick-reference-walkthrough.md`](quick-reference-walkthrough.md)

## 2. Choose One First Skill

Use the first skill scorecard:

- [`../guides/first-skill-scorecard.md`](../guides/first-skill-scorecard.md)

Recommended first skill:

```text
github-safe-publisher
```

Why: it has a clear job, uses fake files for the first test, returns a `READY`, `REVIEW`, or `BLOCK` verdict, and requires human review before any public action.

## 3. Inspect The Skill Before Installing

Open the skill folder:

- [`../../skills/github-safe-publisher/SKILL.md`](../../skills/github-safe-publisher/SKILL.md)
- [`../../skills/github-safe-publisher/references/public-safety-boundaries.md`](../../skills/github-safe-publisher/references/public-safety-boundaries.md)
- [`../../skills/github-safe-publisher/references/release-workflow.md`](../../skills/github-safe-publisher/references/release-workflow.md)
- [`../../skills/github-safe-publisher/scripts/scan_public_safety.py`](../../skills/github-safe-publisher/scripts/scan_public_safety.py)

Confirm that the skill explains:

- when to use it;
- what it should inspect;
- what material must stay out of public artifacts;
- how scanner results and manual review work together;
- why commit, push, upload, send, or publish actions require human approval.

## 4. Install To A Temporary Target

Use a disposable target first. This proves the installer copies the whole folder before you touch your normal skills directory.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\skill-install-smoke"
Test-Path ".tmp\skill-install-smoke\github-safe-publisher\SKILL.md"
Get-ChildItem ".tmp\skill-install-smoke\github-safe-publisher"
```

macOS/Linux:

```bash
chmod +x ./install.sh
./install.sh --target .tmp/skill-install-smoke github-safe-publisher
test -f .tmp/skill-install-smoke/github-safe-publisher/SKILL.md
ls .tmp/skill-install-smoke/github-safe-publisher
```

Expected folder contents for this skill:

```text
agents
references
scripts
SKILL.md
```

Compare with:

- [`install-smoke-test-sample.md`](install-smoke-test-sample.md)
- [`../guides/install-verification.md`](../guides/install-verification.md)

## 5. Install To Your Tool Target

After the temporary target looks right, install the same skill into your normal skills target.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher
```

macOS/Linux:

```bash
./install.sh github-safe-publisher
```

Restart or reload your AI coding tool so it can discover the copied skill folder.

## 6. Run The Fake Candidate

Use the ready fictional candidate pack:

- [`first-skill-candidate/README.md`](first-skill-candidate/README.md)
- [`first-skill-candidate/docs/example-release-note.md`](first-skill-candidate/docs/example-release-note.md)
- [`first-skill-candidate/docs/example-workflow-summary.md`](first-skill-candidate/docs/example-workflow-summary.md)

Prompt:

```text
Use $github-safe-publisher to review this fake README and docs folder before public release.
```

The first run should use only the fake `Example Review Queue` candidate. Do not use account exports, raw logs, screenshots, unpublished notes, or real project files for the first proof run.

## 7. Compare The Expected Review

Expected comparison file:

- [`first-skill-candidate/expected-review.md`](first-skill-candidate/expected-review.md)

The exact wording can differ, but a good result should include:

- `READY`, `REVIEW`, or `BLOCK`;
- artifact type and target folder;
- files inspected;
- scanner summary;
- manual checks;
- exact next commands for review;
- no commit, push, upload, send, or publish action before human approval.

## 8. Decide Pass, Review, Or Stop

| Result | Meaning | Next step |
|---|---|---|
| `PASS` | The temporary install copied the whole skill and the fake candidate review matches the expected shape. | Keep the skill installed and try one small public-safe task. |
| `REVIEW` | The install worked, but the first result is missing key parts or the wrong folder was reviewed. | Reload the tool, rerun with the fake candidate, and compare again. |
| `STOP` | The copied folder is incomplete, the skill is not visible after reload, or the first output skips the review gate. | Use [`../../TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md) before using the skill. |

## 9. Clean Up The Temporary Target

Only remove the disposable target:

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force ".tmp\skill-install-smoke"
```

macOS/Linux:

```bash
rm -rf .tmp/skill-install-smoke
```

Do not remove your normal skills directory unless you know what else is installed there.

## Related Links

- [`../../START_HERE.md`](../../START_HERE.md)
- [`../../QUICK_REFERENCE.md`](../../QUICK_REFERENCE.md)
- [`visitor-paths.md`](visitor-paths.md)
- [`public-proof-index.md`](public-proof-index.md)
- [`../guides/first-skill-scorecard.md`](../guides/first-skill-scorecard.md)
- [`quick-reference-walkthrough.md`](quick-reference-walkthrough.md)
- [`first-skill-walkthrough.md`](first-skill-walkthrough.md)
- [`first-skill-candidate/README.md`](first-skill-candidate/README.md)
- [`first-skill-candidate/expected-review.md`](first-skill-candidate/expected-review.md)
- [`install-smoke-test-sample.md`](install-smoke-test-sample.md)
- [`../guides/install-verification.md`](../guides/install-verification.md)
- [`../../TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md)
