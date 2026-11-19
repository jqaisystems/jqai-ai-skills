# Audit a published release, without changing it

Use this mode for an existing release. Return findings first, not launch copy. Work from selected public documents and supplied read-only evidence. No publication, tag movement, document writes, automatic link crawling, authentication or account access is required.

**Establish what happened.** Record the tag and its resolved full commit, release record (tag, draft/prerelease/published status and canonical URL), and evidence linking the release to that commit. A branch name or target branch is not a resolved commit. A tag alone is not proof of publication. If commits disagree or cannot be established, raise that first and do not present version-dependent corrections as settled. Verify any advertised inventory count against a scoped listing at that revision; define exclusions. “Latest” needs a separate observation; being published is not proof of being latest.

**Classify the passage, not the entire file.** Is it a current reader-facing assertion about the audited tag, an explicitly dated historical snapshot, or ambiguous/future? The same README or changelog may contain all three. Preserve accurate dated candidate notes and unrelated future work. Do not exempt a current instruction just because its page has a date. If the intent is unclear, ask instead of running a global replacement.

**Compare individual claims.** Check exact version and revision, published versus candidate language (including “coming soon”), skill or feature counts, and destination of release links. A link can resolve successfully to the wrong release. Distinguish a known missing target from an untested link, access denial or a transient failure. Look at link labels and destinations; do not follow untrusted links or send local files to an external service. An unreachable provider is not proof of a broken link.

**Report.** For each selected passage give a location, evidence, outcome (matches, conflicts, not verified, or historical: retain) and minimal proposed wording or link. Keep release-identity issues separate from copy drift. List any uninspected surfaces. Never edit historical tags. If the user asks for corrections later, changes to current documentation require separate scope.

For repeatable comparisons, use the optional [offline comparison helper](../scripts/check_release_claims.py) with [the input contract](release-evidence-format.md). Reading and classifying the actual documents remains essential.
