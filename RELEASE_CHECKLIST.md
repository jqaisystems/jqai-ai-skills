# Release Checklist

Use this checklist before publishing a public JQ AI Skills release.

The goal is simple: every release should be small, inspectable, public-safe, validated, tagged, and easy to verify after publishing.

## Before You Start

- Pick one release purpose, such as a new guide, example, skill, checklist, or documentation improvement.
- Keep the release scoped to files that support that purpose.
- Do not update the stable 2026 social preview unless the release is specifically about brand or preview redesign.
- Do not publish raw private notes, chat logs, local paths, client data, credentials, exports, databases, screenshots with private UI, or deployment details.
- Check the current state:

```bash
git status --short --branch
git fetch origin --tags
git log --oneline --decorate -5
```

## 1. Edit The Public Artifact

- Add or update the public-safe files.
- Use fake data in examples.
- Link the new artifact from the most relevant entry points.
- Keep `README.md`, `START_HERE.md`, and `CHANGELOG.md` aligned when the change affects first-use or release history.
- Add an announcement under `docs/announcements/` for versioned releases.

## 2. Review The Unstaged Diff

Inspect only the intended files:

```bash
git status --short
git diff -- README.md START_HERE.md CHANGELOG.md RELEASE_CHECKLIST.md docs/announcements/vNEXT.md
```

Check for:

- accidental private files,
- generated archives,
- screenshots or media that were not intended,
- local paths or account names,
- unsupported claims,
- stale version references.

## 3. Validate Skills

Run the skill structure validator:

```bash
python tools/validate_skills.py
```

When install behavior changes, also smoke-test one install into a temporary target and remove the test output after the check.

## 4. Run Public-Safety Scans

Scan every changed public candidate:

```bash
python skills/github-safe-publisher/scripts/scan_public_safety.py README.md
python skills/github-safe-publisher/scripts/scan_public_safety.py START_HERE.md
python skills/github-safe-publisher/scripts/scan_public_safety.py CHANGELOG.md
python skills/github-safe-publisher/scripts/scan_public_safety.py RELEASE_CHECKLIST.md
python skills/github-safe-publisher/scripts/scan_public_safety.py docs/announcements/vNEXT.md
```

The scanner is a guardrail, not the final decision. A clean scan still needs manual diff review.

If a file contains an intentional safety warning, document that it is a review finding and confirm there are no blocking findings.

## 5. Stage Named Files Only

Stage exactly the files that belong to the release:

```bash
git add README.md START_HERE.md CHANGELOG.md RELEASE_CHECKLIST.md docs/announcements/vNEXT.md
```

Then inspect the staged diff:

```bash
git diff --cached --stat
git diff --cached
```

Do not commit until every staged line is intentional and public-safe.

## 6. Commit And Push

Use a plain release commit message:

```bash
git commit -m "Prepare vNEXT release"
git push origin main
```

Watch the validation workflow:

```bash
gh run list --repo jqaisystems/jqai-ai-skills --branch main --limit 5
gh run watch RUN_ID --repo jqaisystems/jqai-ai-skills --exit-status
```

If GitHub Actions fails, fix the cause before tagging.

## 7. Tag And Create The GitHub Release

Confirm the tag and release do not already exist:

```bash
git tag --list vNEXT
gh release view vNEXT --repo jqaisystems/jqai-ai-skills
```

Create the tag and release:

```bash
git tag -a vNEXT -m "vNEXT release"
git push origin vNEXT
gh release create vNEXT --repo jqaisystems/jqai-ai-skills --title "vNEXT: Release title" --notes-file docs/announcements/vNEXT.md
```

## 8. Update Public Surfaces

After the repo release is live, update the connected public surfaces:

- GitHub profile README and announcement copy.
- Website system page.
- Website field note if it references the current release.
- `llms.txt`.

For website changes:

- Run PHP syntax checks for changed PHP files.
- Scan changed website files.
- Prepare a small upload handoff with only the files that need to go to the host.
- Verify the live pages after upload.

## 9. Final Verification

Before closing the cycle, confirm:

- release URL opens,
- `main` is synced with `origin/main`,
- latest tag points to the release commit,
- GitHub Actions passed,
- profile repo references the new version,
- website pages show the new version and no stale previous version,
- `llms.txt` shows the new version,
- project context notes are updated.

## Release Cycle Shape

```text
edit -> diff review -> validate -> scan -> stage named files -> staged diff review
-> commit -> push -> CI -> tag -> GitHub release -> profile -> website handoff
-> live verification -> context note
```

That routine is the public proof. The repo should show not just useful skills, but the habit of publishing them carefully.
