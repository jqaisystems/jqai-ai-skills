# GitHub Safe Publisher Sample Review

Date: 2026-05-29
Artifact type: Public README update and workflow note
Target repo: `example-public-tools`
Candidate folder: `public-candidate/`
Safety verdict: REVIEW

This fake review shows the output shape expected from `github-safe-publisher`. It uses invented project names, fake domains, and generalized risk descriptions only.

## Files Inspected

- `README.md`
- `docs/workflow-overview.md`
- `examples/sample-config.template`
- `docs/public-demo-notes.md`

## Scanner Summary

Command:

```bash
python skills/github-safe-publisher/scripts/scan_public_safety.py public-candidate
```

Result:

- Blocking findings: 0
- Review findings: 2
- Scanner verdict: REVIEW

Review notes:

- `docs/workflow-overview.md`: replace customer-specific wording with `Example Studio`.
- `docs/public-demo-notes.md`: confirm the screenshot notes describe a recreated demo screen, not a real account screen.

## Decision Table

| Item | Sample decision | Reason |
|---|---|---|
| `README.md` | READY | Uses fake project names, public links, and a generalized workflow summary. |
| `docs/workflow-overview.md` | REVIEW | Useful public explanation, but wording should be generalized before release. |
| `examples/sample-config.template` | READY | Contains placeholders only and no live access values. |
| Private configuration file | BLOCK | A real settings file does not belong in a public candidate. |
| Database or spreadsheet export | BLOCK | Raw operational data should stay out of public repos. |
| Runtime transcript or copied private conversation | BLOCK | Rewrite the lesson as public documentation instead of copying raw material. |

## Required Fixes Before Publishing

1. Replace customer-specific wording with neutral examples such as `Example Studio` and `example.com`.
2. Confirm demo notes describe recreated screens with fake data.
3. Re-run the safety scanner on the candidate folder.
4. Inspect the unstaged diff for every edited file.
5. Stage named files only after review.
6. Inspect the staged diff before commit.

## Commands To Review

```bash
git status --short
git diff -- README.md docs/workflow-overview.md docs/public-demo-notes.md
git add -- README.md docs/workflow-overview.md docs/public-demo-notes.md examples/sample-config.template
git diff --cached
```

## Manual Review Checklist

- No real people, accounts, customers, emails, phone numbers, or private domains.
- No account screens, admin screens, browser tabs, dashboards, exports, or machine-specific paths.
- No private source excerpts, copied conversations, raw operational records, or unreleased strategy.
- All examples use fake names, fake domains, placeholders, or high-level workflow descriptions.
- A human reviewed `git status`, the unstaged diff, the staged diff, and scanner output before commit or push.

## Final Next Step

After the fixes above, the expected final verdict would be:

```text
READY: public-safe documentation example, fake data only, scanner reviewed, manual diff review complete.
```
