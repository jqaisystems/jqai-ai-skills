---
name: publication-ledger
description: Reconcile a selected inventory of works, editions and destinations with supplied publication observations to build an offline publication history and a queue of unresolved checks across projects.
---

# Publication ledger

Use this when someone asks “What has gone out, where, and how do we know?” For approval of an individual campaign package, use a package review instead. A ledger entry is not permission to publish.

1. Ask for the selected inventory and matching observations, not access to a workspace or account. Give every work a stable ID across projects; enumerate the intended edition and destination explicitly. Keep provider-specific destinations distinct when their records are not interchangeable. Titles are labels, never join keys.
2. Prepare the [version 1 evidence pack](references/evidence-format.md). Keep original sources private. Use short evidence aliases whose meanings the user can resolve privately. Never promote a schedule to a delivery or a publication report to an independent verification.
3. Render both Markdown views with the standard-library helper. From the installed skill folder in a shell supporting input redirection:

       python scripts/publication_ledger.py < assets/example-ledger.json

   PowerShell example for this ASCII [fictional pack](assets/example-ledger.json):

       Get-Content -Raw assets/example-ledger.json | python scripts/publication_ledger.py

   For other inputs, pipe UTF-8 bytes (configure PowerShell's outgoing encoding to UTF-8 for non-ASCII titles). No path or URL is resolved by the helper. It reads stdin and writes only to stdout/stderr.
4. Return the history and review queue. Explain any contradictions with both evidence references. Keep a work with the same title separate, and an edition with no evidence unknown. Do not infer a cancellation, recommend reposting, contact providers or change the records.

Filled reports contain the supplied labels, titles and observations: keep them private by default. The tool does not authenticate records or inspect the live destinations.
