# Remove AI Image Metadata Sample

This fictional example shows the expected report shape for owned or authorized sample images. It contains no real client files, private paths, or source images.

## Inspection

```text
Supported image files in scope: 4
[INSPECT] sample.png [PNG 1200x1200]
  remove tEXt (29 bytes): AI metadata marker: openai
[INSPECT] sample.jpg [JPEG 1600x1067]
  remove APP11 (884 bytes): C2PA/JUMBF APP11 provenance segment
[INSPECT] sample.webp [WebP 1080x1350]
  remove XMP  (142 bytes): AI metadata marker: content credentials
[INSPECT] sample.gif [GIF 900x900]
  remove EXT-0xFE (35 bytes): AI metadata marker: generative ai
SUMMARY: inspection PASS; files=4; formats=GIF,JPEG,PNG,WebP; files_with_matches=4; matching_items=4
```

The inspection writes nothing. A human reviews the proposed removals before choosing a write mode.

## Verified Copies

```text
SUMMARY: cleaning PASS; files=4; formats=GIF,JPEG,PNG,WebP; files_with_matches=4; removed_items=4
```

Each changed file reports `PASS` only after the helper reparses the cleaned container, confirms matching metadata is gone, and confirms that the encoded image payload hash is unchanged.

## Safety Boundary

- Prefer clean copies over replacing originals.
- Use in-place mode only after explicit approval and keep backups outside the publish folder.
- Preserve rendering data such as color profiles and animation controls.
- Process only images you own or are authorized to modify.
- Do not use metadata removal to misrepresent an image's origin or bypass platform disclosure requirements.
- Report only which explicit metadata was removed. Do not claim that a cleaned image is undetectable or no longer AI-generated.
