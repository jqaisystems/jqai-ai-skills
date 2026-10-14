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
python scripts/scan_public_safety.py path/to/sanitized-draft --no-baseline
```

If findings appear, fix them before moving into a public repo. Use `--json` when another tool needs structured results.

For a public repo with a committed `.public-safety-baseline.json`, a normal folder scan suppresses known review findings and reports only new risks. Use `--no-baseline` before release when you want the complete raw review list.

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

Maintain a private release manifest containing exact relative paths, hashes, reviewed findings, and test results. Recheck after every edit, including whitespace corrections. Compare the staged file list to that allowlist: a clean unstaged diff does not check untracked files or prove the index matches review. Inspect author/committer identity, release notes, and attachment lists separately. Keep private reports and validation environments outside the public repository.

## 6. Commit And Push Only After Approval

The skill may recommend commands, but it must not auto-commit or auto-push. A human should approve the final diff and explicitly request publication.

For candidate-only work, leave changes unstaged and unpublished. Remote CI remains pending until a separately authorized push.

After publication approval, verify the remote destination and exact reviewed commit. Push with normal fast-forward protection. Wait for all required CI jobs on that commit, not merely the latest green run. Only then tag the tested commit and publish reviewed notes. Verify tag target, release state, links, and attachments. Authentication failures never justify copying access values into project files or changing accounts without approval.

## Stop Conditions

Stop immediately if:

- A scanner flags a real secret or private path.
- Git status shows files you did not intend to publish.
- The artifact includes client-identifying material.
- You are unsure whether a detail is approved for public release.
- The staged diff includes source code, logs, database files, exports, credentials, screenshots, or generated archives unexpectedly.
