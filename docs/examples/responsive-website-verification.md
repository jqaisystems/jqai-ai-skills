# A page that loads but does not respond

On this fictional two-page site, a visitor opens the menu, dismisses it, then clicks **Reserve sample**. The expected visible result is **Sample reserved**. Both routes returned HTTP 200 before and after the fixture fix. That is availability evidence only.

These were normal pointer clicks in a local browser at measured CSS viewport widths. The narrower run represents a mobile layout, not a test on a physical phone. The chosen widths apply to this fixture only.

| Page | Environment | Width (CSS px) | Interaction tested | Expected | Observed before fix | Status |
|---|---|---:|---|---|---|---|
| Control | Local | 1280 | Dismiss menu, reserve | Sample reserved | Sample reserved | pass |
| Control | Local | 390 | Dismiss menu, reserve | Sample reserved | Sample reserved | pass |
| Affected | Local | 1280 | Dismiss menu, reserve | Sample reserved | Sample reserved | pass |
| Affected | Local | 390 | Dismiss menu, reserve | Sample reserved | Still Ready; overlay received click | fail |

**Before fix:** implemented, not verified locally for the required scope. The failure is the button interaction on the affected narrow page, not a missing route.

**Retest:** only the fictional fixture changed. Its dismissed overlay no longer accepted pointer input. The same browser sequence was repeated on all four combinations.

| Page | Environment | Width (CSS px) | Interaction tested | Expected | Observed after fix | Status |
|---|---|---:|---|---|---|---|
| Control | Local | 1280 | Dismiss menu, reserve | Sample reserved | Sample reserved | pass |
| Control | Local | 390 | Dismiss menu, reserve | Sample reserved | Sample reserved | pass |
| Affected | Local | 1280 | Dismiss menu, reserve | Sample reserved | Sample reserved | pass |
| Affected | Local | 390 | Dismiss menu, reserve | Sample reserved | Sample reserved | pass |

**After fix:** verified locally for those two routes, two widths and that interaction only. **Production: not checked** for either page at either width in both runs. No production URL was accessed. Use the [blank table](../../skills/website-change-verifier/assets/responsive-results.md) for a new review.
