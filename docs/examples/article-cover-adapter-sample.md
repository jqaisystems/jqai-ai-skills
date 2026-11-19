# Article Cover Adapter: fictional proof

Two synthetic images carry "Build with evidence" and the visible credit "Example Studio". The target brief requests a 1920 by 1080 PNG and 96-pixel editorial margins. These are example choices, not platform requirements.

| Case | Source | Placement on target | Result |
| --- | --- | --- | --- |
| Wide artwork | 2400 by 800 | Whole artwork scaled to 1728 by 576, placed at (96, 252) | No crop; wording, credit and complete artwork preserved. |
| Tall artwork | 800 by 1600 | Whole artwork scaled to 444 by 888, placed at (738, 96) | No crop; wording and credit preserved, with generous side space. |

Both sources remained byte-identical. Local full-size inspection confirmed the complete lettering, credit, border and central shape. The tall layout remains a design-review choice: fitting everything does not guarantee good feed-scale readability.

The target dimensions and margins passed local checks. Adapted pre-clean and final exports passed the separate metadata/rendering verifier. No targeted metadata was present, so no removal was claimed.

Actual platform preview remains pending. No image was uploaded, no paid generation was used, and no publication approval was inferred. Fictional fixtures and local validation images are not part of the release.

See [the skill](../../skills/article-cover-adapter/SKILL.md) and its [verification checklist](../../skills/article-cover-adapter/references/verification-checklist.md).
