# Remove AI Image Metadata Sample

This fictional example shows the expected report shape for owned or authorized sample images. It contains no real client files, private paths, or source images.

## Inspection

| Fictional input | Expected handling |
|---|---|
| PNG text containing a known generator marker | Propose removal of that supported text record. |
| JPEG standard XMP with generator and rights properties | Propose selective field editing; preserve rights. |
| JPEG JUMBF | Refuse automatic cleanup; require a metadata-aware editor. |
| WebP mixed XMP | Edit supported targeted fields, not the whole mixed parent. |
| GIF supported generator comment | Propose removal of that comment; preserve animation. |

The inspection writes nothing. A human reviews the proposed removals before choosing a write mode.

## Verified Copies

The cleaner's PASS establishes its existing container and encoded-payload checks. It is not a full decoded-rendering result. The separate read-only verifier compares a preserved pre-clean copy with the cleaned derivative.

## v0.14.0 verification proof

Synthetic PNG/APNG, JPEG, WebP and GIF pairs exercised supported marker absence, selective-only changes, encoded data, dimensions, orientation, colour information, decoded frames, alpha, timing and looping. Unchanged pairs passed. Modified pixels, dimensions, rights, orientation, colour profiles, timing or loop settings did not receive a full pass.

Missing Pillow, malformed data, unsupported TIFF/JUMBF, and configured decoding limits produced unverified checks rather than a false pass. Reports omitted raw metadata and local paths. Both input files remained unchanged.

Run `python scripts/verify_image_cleanup.py before.png after.png --json` from the skill folder. See [verification scope](../../skills/remove-ai-image-metadata/references/verification.md). Overall pass requires every check to pass; it is limited to supported default-selective cleanup, not authenticity or platform-label detection.

## Safety Boundary

- Prefer clean copies over replacing originals.
- Use in-place mode only after explicit approval and keep backups outside the publish folder.
- Preserve rendering data such as color profiles and animation controls.
- Process only images you own or are authorized to modify.
- Do not use metadata removal to misrepresent an image's origin or bypass platform disclosure requirements.
- Report only which explicit metadata was removed. Do not claim that a cleaned image is undetectable or no longer AI-generated.

## Selective Upgrade Proof

Synthetic JPEG, WebP, and PNG iTXt packets place a generator attribute next to unrelated rights, orientation, and title records. Default cleanup removes the targeted field, not its mixed parent. Compressed PNG XMP is also checked.

Supported descriptor-free Photoshop version 6 slice strings use same-length Unicode replacements. Binary fields, resource sizes, unrelated resources, and encoded image bytes remain unchanged. Unsupported versions or descriptors stop.

Truncated JPEGs and matched EXIF requiring a selective editor are refused. Progressive JPEGs and GIF frame timing remain intact. Repeated cleanup is idempotent. Source hashes remain unchanged when using inspect/copy modes.
