# Screenshot review before public handoff

A clean text scan says nothing about the pixels of a screenshot. Enumerate **all** images, including thumbnails, animated frames, linked originals, embedded screenshots and repeated placements. If none exist, record the scope and "no screenshots" privately; do not invent a review receipt.

1. Start with a synthetic recreation or a permanently flattened, sanitized derivative. Never include the original just to explain a redaction. Use local inspection only; no external OCR or uploads.
2. Inspect the actual proposed bytes at normal size and zoomed in. Check tabs, menus, notifications, address bars, sidebars, avatars, QR codes, status bars, filenames and background windows. Inspect alt text, links and captions too. Describe a problem by category and placement, never by quoting what was exposed.
3. Inspect the **final artifact as rendered** and what ships underneath: source assets, alternate sizes, attachments, editable layers, selectable text, HTML-hidden content, cached previews and links to originals. A CSS box, blur, clipping mask or PDF annotation is not evidence of irreversible removal. Block recoverable sensitive content even when the visible render looks clean. If layers, frames or originals cannot be inspected, keep REVIEW.
4. Use the [private ledger template](../assets/screenshot-review.md) per placement. Fingerprint the exact screenshot, actual final container and placement together. For a standalone screenshot use the same file as image and artifact. For a directory or multi-file site enumerate every shipped dependency; binding a README does not bind its linked assets. Review shared dependencies separately or bind an exact finalized archive in addition. A local preview does not verify a remote render.
5. Only a person who inspected that exact version may mark the placement reviewed and clear. The optional local helper measures a review key; it does not inspect pixels, authenticate consent, detect hidden text or approve publication.

       python scripts/check_visual_review.py --image screen.png --artifact guide.html --placement figure-1

   Record the returned key privately after inspection. Recheck using the same arguments plus `--state reviewed --finding clear --recorded-key HEX`. Unchecked/skipped, changed bytes, unknown findings, inaccessible files or missing receipts remain REVIEW; exposed or recoverable material is BLOCK. Exit 0 means matching evidence, 1 BLOCK, 2 REVIEW. Keys and receipts are private working records. No key grants publication authority.

Return READY only after all placements match, all underlying assets are accounted for, and the normal scanner and diff gates pass. Missing inventory is REVIEW. A confirmed exposure overrides a matching receipt. Recreate unsafe images with fictional data, replace affected containers, and repeat inspection.
