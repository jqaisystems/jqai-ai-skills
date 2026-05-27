# Pipeline Blueprint

Use this blueprint to design a review-first outreach pipeline.

## Minimal Stages

| Stage | Purpose | Typical Inputs | Typical Output |
|---|---|---|---|
| Source | Collect candidates from approved inputs | Public websites, directories, event lists, manual research, uploaded fake sample CSV | Candidate account list |
| Normalize | Make records consistent | Names, URLs, categories, location, notes | Standard lead record |
| Enrich | Add public context | Website copy, public profile, company category, visible signals | Fit signals and notes |
| Score | Prioritize by transparent criteria | Fit, need, timing, relevance, evidence quality | Score, priority, reason |
| Draft | Prepare reviewable message | Offer, lead context, approved tone | Draft message |
| Review | Keep human control | Score, evidence, draft, notes | Approved, edited, rejected, deferred |
| Handoff | Move approved work forward | Approved record and message | CRM task, export, campaign queue |
| Follow Up | Track next action | Last decision, date, status | Reminder or next-step task |

## Lead Record Fields

Use fake or structural fields in public examples:

```text
account_name
account_url
market
location
source
fit_signals
evidence_notes
score
priority
score_reason
draft_message
review_status
review_notes
next_action
last_reviewed_at
```

Only include contact fields when the user has permission to use and store them.

## Review States

- `new`: collected but not reviewed.
- `needs_context`: missing evidence or unclear fit.
- `qualified`: good fit, ready for draft review.
- `draft_ready`: draft exists but is not approved.
- `approved`: human approved the next action.
- `edited`: human modified the draft or next step.
- `rejected`: not a fit.
- `suppressed`: do not contact.
- `exported`: intentionally handed off.

## Design Principle

AI can reduce research and drafting time, but the pipeline should make evidence, uncertainty, and approval state visible before any outbound action.
