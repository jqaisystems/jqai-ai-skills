# Release Workflow

Use this workflow for safe public GitHub publishing.

## 1. Pick One Candidate

Choose one small public contribution:

- A reusable skill.
- A sanitized case study.
- A README improvement.
- A fake-data example prompt.
- A public demo note or screenshot made with fake data.

Do not publish raw work directly from a private workspace.

## 2. Create A Sanitized Draft

Copy only the public idea, not the full private source. Rewrite the artifact with fake examples and public-safe language.

Good draft habits:

- Explain the workflow instead of copying raw prompts.
- Use fake names, fake domains, and fake IDs.
- Remove logs, databases, exports, local paths, and screenshots with private UI.
- Keep the artifact useful to someone who does not know the private project.

## 3. Scan The Draft

Run:

```bash
python scripts/scan_public_safety.py path/to/sanitized-draft
```

If findings appear, fix them before moving into a public repo. Use `--json` when another tool needs structured results.

## 4. Move To Public Repo

Move or copy only the reviewed draft files into the intended public repository.

Do not move private parent folders, build outputs, archives, databases, browser profiles, or raw exports.

## 5. Review Git State

Before staging:

```bash
git status --short
git diff -- path/to/changed-file
```

Stage specific files only:

```bash
git add path/to/changed-file
```

Before committing:

```bash
git diff --cached
```

Do not commit until every staged line is intentional and public-safe.

## 6. Commit And Push Only After Approval

The skill may recommend commands, but it must not auto-commit or auto-push. A human should approve the final diff and explicitly request publication.

## Stop Conditions

Stop immediately if:

- A scanner flags a real secret or private path.
- Git status shows files you did not intend to publish.
- The artifact includes client-identifying material.
- You are unsure whether a detail is approved for public release.
- The staged diff includes source code, logs, database files, exports, credentials, screenshots, or generated archives unexpectedly.
