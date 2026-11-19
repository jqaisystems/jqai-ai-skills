# Example Tools: post-release review

Supplied public evidence: tag v2.0 and the published release resolve to the same commit; the scoped inventory has four tools. The canonical destination is https://example.com/releases/v2.0. A link observation establishes that the v2.0 destination exists and an old download target is missing.

| Selected passage | Finding | Proposed action |
|---|---|---|
| Current README: “v2.0 coming soon; three tools” | conflicts on status and count | Say “v2.0 is available with four tools.” |
| Current Downloads: “v2.0” links to the v1.9 release, which still exists | conflicts on destination, not availability | Use the canonical v2.0 destination |
| Current Quickstart: old download target | conflicts on availability | Replace only after checking the new destination |
| Roadmap snapshot dated 2025-01-03: “v2.0 is coming soon” | historical: retain | No rewrite |
| Future roadmap section: “v2.1 coming soon” | outside this release | No rewrite |
| Current mirror: no independent reachability evidence | not verified | Record the open check, not a broken link |

If the release commit and resolved tag disagree, report the identity conflict before suggesting current-state copy. The release record alone does not establish that v2.0 is the latest release.
