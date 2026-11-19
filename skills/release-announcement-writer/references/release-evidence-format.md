# Offline comparison contract (version 1)

From the skill folder run `python scripts/check_release_claims.py < evidence.json` in a shell supporting input redirection. In PowerShell, use `Get-Content -Raw evidence.json | python scripts/check_release_claims.py`. Python 3.11+, standard library. Input is structured evidence on stdin, not a URL or directory. Nothing is fetched or written.

Provide `version: 1`, a `release` object and an ordered `claims` array. Release fields: `tag` and `release_tag` (observed tag and release record's tag), `tag_commit` and `release_commit` (independently established full hashes), `state` (published, prerelease or draft). Optional: `count` (non-negative inventory size), `url` (canonical release URL). Omit unknown evidence or use null. Do not substitute branch names or invented hashes.

Each claim has `scope` (current, historical, uncertain), `field` (tag, commit, state, count, url or link_status), and `value`. For state, normalize candidate, unreleased or coming-soon wording about this release to draft. For url, compare canonical same-release destinations, not aliases unless their resolution is known. For link_status, use **confirmed-present**, **confirmed-missing**, or **unknown**, based on selected evidence. Do not guess availability. Historical claims need `as_of` (YYYY-MM-DD) and independent human classification as dated snapshots. The date alone is not evidence of historical intent. Keep a location map keyed by 1-based claim number alongside the input.

Example (fictional hash values are identifiers only):

```json
{"version":1,"release":{"tag":"v2.0","release_tag":"v2.0","tag_commit":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","release_commit":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","state":"published","count":4},"claims":[{"scope":"current","field":"count","value":3},{"scope":"historical","as_of":"2025-01-03","field":"state","value":"draft"}]}
```

The helper reports row numbers, not source text. Exit 0 means selected comparisons match or retain dated history, not that all public documents were reviewed; 1 includes conflicts; 2 means incomplete/invalid evidence without a demonstrated conflict. Interpret unknowns even when a conflict determines the exit code.
