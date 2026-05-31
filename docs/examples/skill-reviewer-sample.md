# Skill Reviewer Sample

This fictional example shows the shape of a `skill-reviewer` review before installing unfamiliar skill folders.

The candidates below are fake. They are designed to show how a reviewer can separate a clear install candidate from a skill that needs more inspection and a skill that should be rejected.

## Review Prompt

```text
Use $skill-reviewer to review these skill folders before installation. Check SKILL.md, metadata, references, assets, and scripts. Return READY, REVIEW, or BLOCK with the reason, files inspected, risky instructions, and safe next steps.
```

## Candidate Folders

```text
candidate-skills/
  copy-cleaner-lite/
    SKILL.md
    agents/openai.yaml
  folder-cleaner-plus/
    SKILL.md
    agents/openai.yaml
    scripts/remove-old-files.ps1
  publish-helper-pro/
    SKILL.md
    agents/openai.yaml
    references/publishing-notes.md
```

## Sample Review Output

### Candidate 1: `copy-cleaner-lite`

**Verdict:** `READY`

**Reason:** The skill has a narrow copy-editing purpose, no scripts, no network behavior, and no instructions to edit files without showing changes.

**Files inspected:**

- `copy-cleaner-lite/SKILL.md`
- `copy-cleaner-lite/agents/openai.yaml`

**What looked safe:**

- The trigger is specific: use only when asked to clean punctuation and phrasing.
- The workflow says to preserve meaning and return edits for review.
- The metadata matches the folder name and description.
- There are no scripts, assets, credentials, exports, logs, or hidden setup files.

**Safe next step:**

Install into a test target, reload the tool, and run it on fake copy first.

### Candidate 2: `folder-cleaner-plus`

**Verdict:** `REVIEW`

**Reason:** The skill may be useful, but it includes a cleanup script and the instructions do not clearly limit which folders the script can touch.

**Files inspected:**

- `folder-cleaner-plus/SKILL.md`
- `folder-cleaner-plus/agents/openai.yaml`
- `folder-cleaner-plus/scripts/remove-old-files.ps1`

**Review findings:**

- `SKILL.md` describes deleting stale generated files, but does not define a safe target folder.
- The script appears to remove files recursively.
- The script needs a dry-run mode or explicit target allowlist before it is safe to run.
- The metadata description is broader than the skill workflow.

**Required human checks:**

- Confirm the exact folders the script may touch.
- Add or verify a dry-run option.
- Test only in a disposable sample folder.
- Do not install into the main skills folder until the script behavior is scoped and documented.

**Safe next step:**

Keep the skill out of the main install target. Revise the script and `SKILL.md`, then review again.

### Candidate 3: `publish-helper-pro`

**Verdict:** `BLOCK`

**Reason:** The skill tells the agent to publish outputs without review and to avoid asking for confirmation. That behavior is not safe for public or client-facing work.

**Files inspected:**

- `publish-helper-pro/SKILL.md`
- `publish-helper-pro/agents/openai.yaml`
- `publish-helper-pro/references/publishing-notes.md`

**Blocking findings:**

- `SKILL.md` says to publish immediately after drafting.
- The workflow says not to show intermediate diffs.
- The references mention account setup and publishing behavior that should stay out of a public skill.
- The metadata describes broad publishing authority that does not match a safe review-first workflow.

**Safe next step:**

Do not install this skill. Rewrite it as a review-first release helper that drafts copy, lists assumptions, shows diffs, and waits for human approval before any publish action.

## Final Recommendation

| Candidate | Verdict | Install decision |
|---|---|---|
| `copy-cleaner-lite` | `READY` | Test install first. |
| `folder-cleaner-plus` | `REVIEW` | Revise and re-review before installing. |
| `publish-helper-pro` | `BLOCK` | Do not install. |

## What This Example Teaches

- A useful skill can still be blocked if it bypasses review.
- Scripts need extra inspection, especially when they edit or remove files.
- Metadata should match the actual workflow.
- Public examples should use fake folders, fake file names, and review-safe descriptions.
- Install decisions should happen before the skill reaches a real workspace.

## Related Docs

- [`docs/guides/skill-review-checklist.md`](../guides/skill-review-checklist.md)
- [`skills/skill-reviewer/SKILL.md`](../../skills/skill-reviewer/SKILL.md)
- [`SECURITY.md`](../../SECURITY.md)
- [`INSTALL.md`](../../INSTALL.md)
