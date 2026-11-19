# Static Site Handoff: fictional proof

Example Studio supplies a completed static export containing index.html and assets/app.js. The helper is run only on disposable local fixtures.

| Scenario | Observed result |
| --- | --- |
| First preparation | Both files appear under upload; the build bytes remain unchanged. |
| Preparation without confirmation | No confirmed baseline is created. |
| Confirmed package, timestamps changed only | Next upload subset is empty. |
| Page changed, two packages prepared without upload confirmation | Both contain the page change; the older pending ID cannot confirm. |
| Added, missing, or edited payload file | Verification refuses the package. |
| Edited manifest | Package identity mismatch is refused. |
| Removed script | Removal is reported; the earlier package remains untouched. |
| Reintroduced script | The script is included again. |
| Copy or state-write failure | Previous confirmed state is preserved; an orphan package cannot confirm. |
| Temporary Windows junction | Refused without reading or modifying the external target. |

Confirmation records only an explicit human acknowledgement for the exact package. It does not establish that example.com changed, that remote obsolete files were removed, or that an upload completed.

The synthetic tests use no hosting accounts and make no network calls. No fixture is a real deployment record. See [the skill](../../skills/static-site-handoff/SKILL.md).
