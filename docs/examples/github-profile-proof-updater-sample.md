# GitHub Profile Proof Updater Sample

This sample uses fictional paths and public-safe placeholders. It shows the expected output shape after refreshing profile visuals.

## Input

Target repo: `example-profile`

Source assets:

- `01_Workflow Map.png`
- `02_1_What_I_Build_AI_Systems.png`
- `02_2_What_I_Build_Reusable_Skills.png`

Preserve existing README paths:

- `assets/profile/workflow-map.png`
- `assets/profile/ai-systems-tile.png`
- `assets/profile/reusable-skills-tile.png`

Keep unchanged:

- `assets/profile/profile-hero.png`

## Expected Review Output

Verdict: `READY`

Target repo and files changed:

- `assets/profile/workflow-map.png`
- `assets/profile/ai-systems-tile.png`
- `assets/profile/reusable-skills-tile.png`

Validation performed:

- Confirmed the unchanged hero remained untouched.
- Confirmed all replacement PNGs were readable.
- Confirmed README still referenced the preserved filenames.
- Ran `git status --short` and saw only the intended image files.

Live verification result:

- GitHub profile rendered the updated non-hero visuals.
- No broken images found.

Proof trail update:

- Added commit hash.
- Added updated profile URL.
- Added public post links when available.

Next recommended action:

- Draft LinkedIn/X proof copy with alt text and a short follow-up checklist.

## Safety Notes

- Do not include local machine paths in public notes.
- Do not publish screenshots showing private account menus, browser tabs, analytics, email, billing, or file paths.
- Keep source asset folders private unless they are intentionally public.
