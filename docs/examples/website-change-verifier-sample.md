# Website Change Verifier Sample

This fictional example verifies a homepage update for `sample-project` without using a production account or private URL.

## Expected Change

- `/` returns 200.
- The new heading `Workflows your team can trust.` is present.
- The previous heading `Automation for everyone.` is absent.
- `/old-preview` returns 404.
- Metadata and sitemap continue to reference the canonical homepage.

## Deterministic Route Checks

```text
PASS 200 http://127.0.0.1:8766/
  PASS status: 200
  PASS contains: Workflows your team can trust.
  PASS not-contains: Automation for everyone.
PASS 404 http://127.0.0.1:8766/old-preview
  PASS status: 404
```

## Verification Summary

- Production build: pass
- Homepage route and exact text: pass
- Removed preview route: pass
- Desktop rendering: pass
- Narrow mobile rendering: pass
- Canonical metadata and sitemap: pass
- Deployment: not requested

Highest supported state: `verified locally`.
