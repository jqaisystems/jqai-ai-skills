# Brief Template

Use this shape for daily or weekly research briefs unless the destination has a stronger house style.

## Record Schema

Each source item should be normalized into:

- `title`: short item title.
- `source`: publisher, site, project, or channel name.
- `url`: public link or citation.
- `date`: source date or local review date.
- `topic`: one concise category.
- `visibility`: `public_ready`, `needs_review`, `private_research`, or `archive`.
- `summary`: one or two sentence neutral summary.
- `why_it_matters`: practical relevance for the audience.
- `next_action`: brief, verify, hold, archive, or adapt.

## Markdown Shape

```markdown
# Brief Title

Date: YYYY-MM-DD
Audience: example audience
Sources reviewed: N
Safety verdict: READY | REVIEW | BLOCK

## Executive Summary

One short paragraph describing the pattern across the items.

## Public-Ready Highlights

### Item Title

- Source: [Source Name](https://example.com/item)
- Topic: Topic
- Summary: ...
- Why it matters: ...
- Next action: ...

## Needs Review

- Item title: reason it is held.

## Private Research / Archive

- Item title: private, archive, duplicate, stale, or internal-only reason.

## Manual Checks

- Confirm all source links are public.
- Confirm claims are supported by sources.
- Remove private notes, raw prompts, logs, datasets, and local paths.
- Approve wording before publishing, sending, or adding to a public repo.
```

## Writing Rules

- Keep the executive summary under five sentences.
- Prefer specific, practical relevance over hype.
- Do not make claims that are not supported by a public source.
- Use fake examples when demonstrating the workflow.
- Keep public briefs short enough for a human to review quickly.
