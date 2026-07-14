# Implement Client Feedback Sample

This fictional example shows how feedback for Example Studio's `sample-project` becomes a traceable revision contract.

## Feedback Received

1. Change the homepage headline to `Workflows your team can trust.`
2. Keep the navy and cream color palette.
3. Remove the three pricing cards.
4. Do not add the chatbot concept shown in the earlier mockup.
5. Make the page feel more premium.
6. Consider a multilingual version later.

## Feedback Matrix

| ID | Type | Literal instruction | Minimal interpretation | Acceptance evidence | Status |
|---|---|---|---|---|---|
| F-01 | change | Change the homepage headline to `Workflows your team can trust.` | Replace only the existing H1 text. | New H1 present; previous H1 absent. | verified |
| F-02 | keep | Keep the navy and cream color palette. | Preserve the approved palette across edited sections. | Color tokens unchanged. | verified |
| F-03 | remove | Remove the three pricing cards. | Remove the cards and their navigation anchor. | Cards and anchor absent. | verified |
| F-04 | exclude | Do not add the chatbot concept shown in the earlier mockup. | Keep chatbot UI and scripts out of the revision. | No chatbot markup, assets, or scripts. | verified |
| F-05 | question | Make the page feel more premium. | A visual direction decision is required before implementation. | Client chooses a direction. | awaiting client |
| F-06 | future | Consider a multilingual version later. | Record for a later scope. | No multilingual work in this revision. | verified |

## Review State

- Required literal changes are verified.
- The approved palette is preserved.
- The rejected chatbot concept remains excluded.
- The subjective premium direction is awaiting a client decision and is not silently interpreted.
