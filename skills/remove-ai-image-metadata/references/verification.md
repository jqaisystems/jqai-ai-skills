# Read-only cleanup verification

    python scripts/verify_image_cleanup.py before.png after.png --json

Python 3.11+; Pillow 12.x is required for decoded-image checks. It is never installed automatically. The original cleaner remains standard-library-only and its flags are unchanged.

The helper is intended for before/after pairs from the bundled default selective cleaner. It reads local regular files only, rejects links/reparse points and network paths, and writes nothing. Inputs are limited to 64 MiB each; decoding is limited to 1000 frames and 100 million total frame pixels. Unsupported or over-limit work is unverified, never passed.

Each check is pass, fail or unverified:

- Supported targeted metadata is absent under the cleaner's known-marker policy.
- The result equals the default cleaner's expected selective output, protecting unrelated metadata.
- Encoded image data is unchanged, including animated PNG frame payloads/control.
- Dimensions and display orientation match.
- Container colour information matches.
- Decoded composited frames and alpha match.
- Frame timing and loop behaviour match.

Overall pass requires every check to pass. A failure takes precedence over unverified checks. Exit 0 means pass, 1 means fail, and 2 means unverified. Missing Pillow, decoder errors, malformed containers, and unsupported metadata cannot yield a full pass. Decoder error text and raw metadata values are not exported.

An externally edited file with equivalent pixels but different metadata serialization may fail the selective-output comparison. This is a conservative limitation, not proof that the external tool corrupted the image. Review separately rather than bypassing a failed check.

Mixed/split JPEG JUMBF, unsupported EXIF edits, and unsupported formats remain outside the cleaner's removal capability. The verifier does not repair them. Explicit all-metadata cleanup is not certified by this default-selective verifier.

Preserve a before-copy for verification when in-place cleanup was separately approved. Compare the final derivative before and after metadata cleanup, not an earlier differently sized design source. Also inspect the rendered output. No check establishes authenticity, invisibility to classifiers, or exemption from disclosure requirements.
