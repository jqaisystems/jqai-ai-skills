# Scrub checklist for a public demo build

Run every item. Verify each one against the **built output**, not the source
tree. Generated files are exactly where leaks hide.

## Never include

| What | Why it is easy to miss |
|---|---|
| Settings or config files | Often hold an API key even when the repo looks clean |
| Browser profile directories | A logged-in session is a live credential |
| Usage, analytics, or billing data | Reveals volume, spend, and working patterns |
| Third-party images gathered by search | Fine to use privately, not yours to republish |
| Debug screenshots | Capture whatever else was on screen, including other work |
| Intermediate build folders and archives | Frequently contain full-resolution originals |

## Sanitise, do not delete

| What | How |
|---|---|
| Absolute paths in API responses | Replace the base with a neutral placeholder and drop any root field |
| Absolute paths shown in the interface | Have the server report its base path; build display paths from it |
| Personal defaults compiled into source | Blank the default and move the real value to ignored local config |
| Account or project URLs | Blank them; they identify a person even without a key |

## Grep the built output for

- Your drive letters and home directory: `C:\Users\`, `/Users/`, `/home/`
- Your username, in every case form
- Key prefixes for every provider you use
- Session and profile directory names
- Any account, workspace, or project identifier

Zero matches, or it does not ship.

## Confirm absent

- Every private directory listed above.
- Any file the version-control ignore rules exclude. If it is not safe to commit,
  it is not safe to publish.

## After deploying

- Open the URL in a private window with no session. It should load.
- Confirm images render, rather than assuming they do.
- Click one control that writes. It must refuse in plain language.
- Confirm any hidden-by-design control is genuinely absent from the markup, not
  merely hidden with CSS.

## The one that catches people

A debug artifact committed weeks earlier, showing a sidebar, a file tree, or a
notification containing unrelated private work. Screenshots and recordings made
during development are the highest-risk files in any repository, and they are
almost never reviewed before publishing. Search for image files in unexpected
directories and open every one before the repository goes public.
