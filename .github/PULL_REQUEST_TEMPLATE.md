## Summary

Describe the change and the public value.

## Public Safety

- [ ] I did not include credentials, tokens, client data, private links, raw prompts, logs, exports, or local machine paths.
- [ ] Examples use fictional, public, or approved material.
- [ ] Screenshots or media, if any, contain only public-safe content.
- [ ] New or changed skills were reviewed across `SKILL.md`, agent metadata, scripts, references, and assets for unexpected access or destructive behavior.
- [ ] The sanitized candidate received a `READY` public-safety verdict before it was copied into the repo.

## Validation

- [ ] `python tools/validate_skills.py`
- [ ] `git diff --check`
- [ ] `python skills/github-safe-publisher/scripts/scan_public_safety.py <changed-public-file-or-folder>`
- [ ] Named-file unstaged and staged diffs were reviewed and explicitly approved before publication.

## Notes

Add links, screenshots, release notes, or follow-up context if relevant.
