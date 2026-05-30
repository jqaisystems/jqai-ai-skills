# Example Outreach Pipeline

Sample only. This fake example shows the output shape expected from `outreach-pipeline-designer`.

This sample is fictional and includes no live outreach records.

## Scenario

Example Studio wants a review-first workflow for finding possible workshop partners.

The team does not want automated sending. They want an organized queue where AI can help summarize public information, suggest fit, draft a first message, and wait for a human to approve or reject the item.

## Public-Safe Inputs

- Public website URL for a fictional organization.
- Public description of the organization's work.
- Human-written fit criteria.
- Approved message style notes.
- Manual reviewer decision labels.

## Pipeline

1. Add a fictional organization to the review queue.
2. Capture only public summary fields: name, website, category, public description, and why it might fit.
3. Score fit against approved criteria: audience match, likely need, timing, and relevance.
4. Write a short reviewer summary with the reason for the score.
5. Draft a first message using approved style notes.
6. Mark the item as ready for review, needs more context, not a fit, or archive.
7. Wait for a human to approve, edit, or reject the draft.
8. Only after approval, move the final human-reviewed message to the team's chosen sending workflow.

## Example Review Record

| Field | Example |
|---|---|
| Organization | Example Learning Lab |
| Public URL | https://example.com/learning-lab |
| Category | Professional education |
| Fit score | 72 / 100 |
| Fit reason | The public page suggests a good audience match, but timing is unknown. |
| Suggested label | Needs human review |
| Draft status | Draft only, not sent |

## Draft Message

Hello Example Learning Lab,

I saw your public workshop page and thought there might be a fit for a short session on practical AI workflow design.

If useful, I can send a concise outline for a review-first session that shows teams how to use AI drafts while keeping approvals in human hands.

Best,
Example Studio

## Human Review Gates

- Approve the source and fit score.
- Edit or reject the draft message.
- Confirm the contact route is appropriate.
- Confirm the message should be sent.
- Log the final decision.

## Safety Notes

- Do not send messages automatically.
- Do not use private prospect files, account exports, or hidden profile data.
- Do not claim personalization that was not reviewed by a human.
- Keep a human decision step before any message leaves the queue.

## Expected Output From The Skill

- Pipeline map.
- Fit scoring rubric.
- Review queue fields.
- Drafting boundaries.
- Human approval gates.
- Handoff notes for the system that sends or records the final message.
