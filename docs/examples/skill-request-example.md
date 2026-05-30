# Skill Request Example

This example shows a public-safe way to propose a new skill without exposing private project material.

Use it before opening a skill request issue or writing a pull request proposal. The example is fictional and intentionally generic.

## Example Issue

**Title:** `[Skill request]: meeting-notes-cleaner`

### Proposed skill name

`meeting-notes-cleaner`

### Workflow

I often turn messy meeting notes into a cleaner follow-up summary.

The skill should help with this repeatable workflow:

1. Read a pasted note draft or a public-safe Markdown file.
2. Identify decisions, action items, open questions, and follow-up dates.
3. Rewrite the notes into a concise summary.
4. Flag anything that needs human confirmation.
5. Return a clean handoff that can be reviewed before sharing.

### Public-safe inputs

Use fictional or sanitized notes only.

Example input:

```text
Meeting: Example Product Planning
Attendees: Alex, Morgan, Riley

Notes:
- Landing page draft needs a clearer CTA.
- Morgan will review the pricing table by Friday.
- Riley asked whether the demo video should be public or internal.
- Decision: keep the first release small and publish a changelog.
```

### Desired output

The skill should produce:

- short meeting summary;
- decisions;
- action items with owner and due date when available;
- open questions;
- review warnings for unclear or sensitive details.

### Safety boundaries

The skill should not:

- invent decisions or owners;
- publish or send notes automatically;
- include private attendee details, account links, recordings, transcripts, or raw client material in public examples;
- treat uncertain dates or names as confirmed.

The skill should remind the user to review the final summary before sharing it.

## Why This Is Public-Safe

- Names are generic examples.
- No real meeting transcript, client detail, account link, recording, or internal project name is included.
- The workflow explains the shape of the request without copying private notes.
- The output is review-first rather than auto-send.

## Not Public-Safe

Do not open a public issue with:

- real customer names or meeting transcripts;
- private links, call recordings, or file paths;
- screenshots from a private workspace;
- raw prompts or internal instructions;
- credentials, account IDs, exports, or logs.

## Pull Request Shape

If this request became a pull request, a safe first version might include:

```text
skills/meeting-notes-cleaner/
  SKILL.md
  agents/
    openai.yaml
  references/
    summary-format.md
docs/examples/meeting-notes-cleaner-sample.md
docs/announcements/vNEXT.md
```

The sample should use fictional notes like the example above.

## Review Checklist

Before submitting a skill request or pull request:

1. Replace real names, companies, links, transcripts, and account details with fictional examples.
2. Keep the workflow narrow enough to review.
3. Identify where human review should happen.
4. Confirm that any example data is fictional, public, or approved for release.
5. Run the public-safety scanner on new docs before release:

```powershell
python skills\github-safe-publisher\scripts\scan_public_safety.py docs\examples\skill-request-example.md
```

Use [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md), [`../../SECURITY.md`](../../SECURITY.md), and [`../guides/skill-anatomy.md`](../guides/skill-anatomy.md) before proposing a new public skill.
