# First Skill Scorecard

Use this worksheet when the repo looks useful but you are not sure which skill to install first.

The goal is to pick one safe, testable first skill. Do not install every skill just because the library looks interesting.

After choosing the winner, use the [`first skill walkthrough`](../examples/first-skill-walkthrough.md), the ready [`first-skill candidate pack`](../examples/first-skill-candidate/README.md), and the [`expected review`](../examples/first-skill-candidate/expected-review.md) to run it with fake input before touching real work.

## Quick Rule

If your work touches public GitHub, release notes, case studies, screenshots, examples, or anything derived from private project work, start with [`github-safe-publisher`](../../skills/github-safe-publisher/SKILL.md).

If your work does not touch public publishing, use the scorecard below.

## Score A Candidate

Pick up to three skills from the [`skill selection guide`](skill-selection.md) or the [`catalog`](../catalog.md). Score each candidate from `0` to `2`.

| Check | 0 | 1 | 2 |
|---|---|---|---|
| Job match | The job is unclear. | It partly matches. | It directly matches the work. |
| Safe first test | Needs real or sensitive material. | Can be tested after rewriting input. | Can be tested with fake or public-safe input. |
| Output clarity | You do not know what output to expect. | Output is described but no sample exists. | Output shape or sample is easy to inspect. |
| Install confidence | You are unsure what folder to copy. | Install path is clear after reading more. | Install command and verification path are obvious. |
| Reuse value | You may use it once. | You may use it occasionally. | You expect to reuse it often. |

Decision:

```text
Skill:
Score out of 10:
Verdict: READY / REVIEW / BLOCK
First safe input:
Expected output to compare:
Next step:
```

## Recommended Starting Points

| If the highest-score job is... | Start with | First safe input |
|---|---|---|
| Public release, repo cleanup, README, case study, or screenshot review | [`github-safe-publisher`](../../skills/github-safe-publisher/SKILL.md) | [`A fake README and docs folder`](../examples/first-skill-candidate/README.md), plus an [`expected review`](../examples/first-skill-candidate/expected-review.md) |
| Turning project work into public proof | [`case-study-writer`](../../skills/case-study-writer/SKILL.md) | A fictional project summary |
| Changelog, launch post, or release copy | [`release-announcement-writer`](../../skills/release-announcement-writer/SKILL.md) | A fake changelog |
| Reviewing a downloaded or modified skill | [`skill-reviewer`](../../skills/skill-reviewer/SKILL.md) | A copied test skill folder |
| Public research links or saved notes | [`research-brief-curator`](../../skills/research-brief-curator/SKILL.md) | Public URLs and fictional notes |
| Authorized page extraction | [`web-scraper`](../../skills/web-scraper/SKILL.md) | A public page you are allowed to inspect |
| Marketplace listing copy | [`etsy-listing-optimizer`](../../skills/etsy-listing-optimizer/SKILL.md) | A fictional listing |
| Review-first outreach workflow design | [`outreach-pipeline-designer`](../../skills/outreach-pipeline-designer/SKILL.md) | Fake prospect records |
| Demo walkthrough | [`demo-animation-v2`](../../skills/demo-animation-v2/SKILL.md) | A fictional product flow |
| Copy cleanup | [`em-dash-remover`](../../skills/em-dash-remover/SKILL.md) | A short public-safe paragraph |
| Development cleanup | [`code-deduplicator`](../../skills/code-deduplicator/SKILL.md) | A small public-safe code example |

## Tie Breakers

If two skills have the same score:

1. Choose the skill with the safest fake-data test.
2. Choose the skill with a sample output you can compare against.
3. Choose the skill you will reuse this week.
4. Choose `github-safe-publisher` if any public release or sensitive review boundary is involved.

## Install Only The Winner

Use a temporary target first:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\first-skill-test"
```

Replace `github-safe-publisher` with the winning skill name.

Then verify the copied folder with [`install-verification.md`](install-verification.md), run the selected skill with fake input using [`../examples/first-skill-walkthrough.md`](../examples/first-skill-walkthrough.md) and [`../examples/first-skill-candidate/README.md`](../examples/first-skill-candidate/README.md), compare output with [`../examples/first-skill-candidate/expected-review.md`](../examples/first-skill-candidate/expected-review.md) or a relevant sample from [`../examples/README.md`](../examples/README.md), and install into your real skill target only after the test is clear.

## Stop Conditions

Use `BLOCK` and install nothing if:

- the first test requires real credentials, tokens, exports, account data, logs, customer data, or local private paths;
- you cannot describe the expected output;
- the skill has scripts or permissions you have not reviewed;
- the skill came from outside this repo and has not been checked with [`skill-review-checklist.md`](skill-review-checklist.md).

When in doubt, review before install.
