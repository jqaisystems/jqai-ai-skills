# Choosing how to run a batch of image generations

Five broad paths, in the order worth trying. Providers change; the shape of the
trade-offs does not.

## 1. Native or first-party integration

The provider's own desktop app, CLI, or agent generating images directly.

- No browser in the loop, so nothing to break when a web interface is redesigned.
- Usually writes files straight to disk, with the filenames you asked for.
- Reference-image caps are commonly higher than the chat interface.
- Often supports higher output resolution.
- Trade-off: image turns consume plan quota several times faster than text turns.

Best default when it exists. The one thing to get right: if each generation runs
in a fresh context, **every image needs its references attached again**. There is
no conversation carrying them.

## 2. Scripted browser session through an existing subscription

A deterministic script driving a logged-in browser profile.

- No API spend and no agent tokens. Nothing is reasoning, it is plain code.
- On an unlimited or generous consumer plan, this is effectively free at volume.
- Trade-off: breaks whenever the interface changes. Budget for maintenance.
- Requires the persistent-profile login pattern. Never a stored password.

Best when quota on the native path runs out and volume is high.

## 3. An agent driving the browser

An assistant with browser control operating the interface.

- The most adaptable. It reads the page, adjusts to changes, recovers from
  surprises, and can fix problems mid-run.
- Trade-off: costs tokens per image, which adds up fast across a set.

Best for one-off runs, unfamiliar interfaces, or when something has broken and
you need adaptability more than efficiency.

## 4. A paid API

- Headless, portable, runs anywhere, exact cost reporting.
- No login, no session, no interface to break.
- Trade-off: pay per image, and the model available through the API is not
  always the same one the consumer product uses.

Best when handing the system to someone else, or running on a server.

## 5. A local or custom generator

A local model or any CLI, wired behind a template.

- No cloud dependency, no per-image cost, full control.
- Trade-off: quality and setup effort vary enormously.

Best for privacy-sensitive work or high volume where cloud cost dominates.

## Always available

Manual copy and paste. Slow, but it works when everything else is broken, and it
is the fallback that makes a system honest: if a run can only happen through
automation, the automation is a dependency, not a convenience.

## Designing for all five

Write the run instructions once, in plain language, in a file. Have every path
read that same file. Then switching paths is a decision, not a rewrite, and a
broken path is an inconvenience rather than a stoppage.
