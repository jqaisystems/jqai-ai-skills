# Demo Animation v2 Walkthrough Sample

This sample shows the expected public-safe output shape for `demo-animation-v2`.

It is not a private client demo. It uses a fictional product called **Signal Desk** so visitors can inspect the structure, pacing, and review checks of a completed walkthrough before generating their own `demo/index.html`.

## Fake Input Brief

```text
Product: Signal Desk
Tagline: Turn scattered launch signals into one reviewed daily queue.
Audience: small studio operators and solo consultants
Primary color: #2563eb
Accent color: #14b8a6
Demo goal: show how a user collects sources, reviews AI suggestions, approves output, and exports a client-ready brief.
Output: single-file responsive HTML demo with captions, timeline controls, cursor motion, highlights, music toggle, and mobile support.
```

## Expected Output

The skill should create:

```text
demo/index.html
```

The file should be self-contained except for approved font loading. It should open directly in a browser and show a responsive, self-playing walkthrough with a clear start, visible progress, captions, controls, and an ending screen.

## Rendered Walkthrough Shape

| Step | Screen | What the viewer sees | Motion cue |
|---|---|---|---|
| 1 | Intro | Signal Desk logo, tagline, and start button. | Intro fades in, then the demo begins. |
| 2 | Dashboard | Three queues: Sources, Review, Approved. | Cursor moves to the source queue. |
| 3 | Source intake | Fictional public links appear as cards. | Cards slide into the queue. |
| 4 | AI suggestion | A short summary and confidence label appear. | Highlight frames the suggested brief. |
| 5 | Human review | Reviewer edits one sentence and marks visibility as public-safe. | Cursor clicks the approval control. |
| 6 | Export | Approved brief moves to an export panel. | Progress line advances to Export. |
| 7 | Result | Final brief card shows source count, review status, and publish readiness. | Success toast appears. |
| 8 | Ending | URL, outcome, and replay affordance. | Ending screen fades in. |

## Caption Sample

```text
Step 3 of 8
Review the AI suggestion
Signal Desk drafts a short brief from public links, then waits for a human approval before anything leaves the workspace.
```

## Timeline Sample

```text
Intro -> Intake -> Suggest -> Review -> Approve -> Export -> Result -> Done
```

## Desktop Review Checks

- The mock interface fits without horizontal scrolling at common desktop widths.
- Captions do not overlap the timeline, controls, or highlighted UI.
- Cursor movement points to visible elements that exist in the HTML.
- Timeline progress matches the active caption.
- Highlights disappear before the next step begins.
- Ending screen is reachable without manual clicks.

## Mobile Review Checks

- Controls remain reachable at narrow widths.
- Captions wrap cleanly and do not cover the main action.
- Touch targets are large enough for replay, pause, and fullscreen controls.
- Landscape hint appears only when it helps the viewer.
- Reduced-motion users still get readable step changes.

## Public-Safety Checks

- Use fictional product names, links, source cards, customers, and metrics.
- Do not show browser tabs, account menus, analytics dashboards, emails, invoices, API dashboards, credentials, machine paths, exports, or sensitive business material.
- Keep claims tied to what the demo shows.
- Review the final `demo/index.html` before publishing or embedding it.

## Good First Prompt

```text
Use $demo-animation-v2 to create a responsive walkthrough for this fictional Signal Desk brief. Keep all data fake, show the human review gate clearly, and write the result to demo/index.html.
```

## Expected Human Review Result

```text
READY with review notes:
- Demo uses fictional content only.
- The review gate is visible before export.
- Captions, cursor targets, timeline steps, and mobile controls are present.
- No private screenshots, account data, credentials, local paths, or raw logs are included.
```
