# Campaign approval package

Use fictional examples only in public proof. Real packages and receipt records remain private.

## package.json

    {
      "schema_version": 1,
      "provider": "example-provider",
      "destination": "example-studio",
      "scheduled_at": null,
      "posts": [
        {"copy": "Build with evidence.", "title": "Example update", "media": []}
      ]
    }

For media, add ordered objects containing path, role and alt_text, for example a relative path of cover.png, a role of cover, and a useful description of the image.

Run the auditor and show the finished package to the human. Do not invent an approval.

## Approval record, only after an actual decision

    {
      "schema_version": 1,
      "fingerprint": "REPLACE_WITH_MEASURED_FINGERPRINT",
      "decision": "approved",
      "approved_at": "2026-10-28T12:00:00+00:00"
    }

The placeholder is intentionally invalid. Replace it only with the exact measured fingerprint and the real approval timestamp after approval.

## Receipt projection

    {
      "schema_version": 1,
      "records": []
    }

An empty record set is not evidence that nothing was scheduled or published. Add minimal supplied observations using the publication-state reference; preserve conflicting observations instead of silently replacing them.

## Review

- Exact text, title, media, order, roles and alt text:
- Provider, destination, time and timezone:
- Fingerprint reviewed:
- Human decision and evidence location:
- Observed publication state and provider coverage:
- Conflicts / unknowns:
- Reconciliation required before retry:
- Actual platform preview:
