# Selective handling boundaries

Default mode edits supported XMP properties individually in JPEG APP1, WebP XMP, and PNG iTXt. Protected authorship, rights, orientation, and embedded thumbnail properties remain intact. Unmatched packets remain byte-identical; edited XML may use different namespace prefixes or padding.

Photoshop APP13 support follows the [Adobe image resource specification](https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/). Only descriptor-free version 6 slice Unicode fields are parsed for targeted strings. Replacements preserve UTF-16 lengths, resource sizes, binary fields, and other resources. Matched newer versions, descriptors, malformed layouts, and unsupported resources stop. Unmatched resources are retained.

The JPEG parser checks marker framing through EOI, including progressive scans. It refuses metadata after the first scan rather than silently overlooking it. Container checks and unchanged encoded-payload hashes are not a full decoder or authenticity test. Use a decoder for additional visual verification.

Default mode refuses matched EXIF that requires selective editing. Explicit all-metadata mode is broader and may remove orientation. Inspect first; do not treat provenance removal as permission to misrepresent origin or ignore disclosure requirements.

Default mode also refuses JPEG JUMBF and matching unknown JPEG/WebP structures. A marker alone does not establish that an entire mixed or split metadata container is disposable. Use a format-aware editor for those cases instead of deleting an unknown parent.
