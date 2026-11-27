# One cut, two reviews

Use the [video cut reviewer](../../skills/video-cut-reviewer/SKILL.md) with the [approved Paper Signals brief](video-cut-brief.md). The cut and grid were reviewed separately; the grid reviewer did not receive the video, audio, fixture recipe or expected findings.

| Requirement | Full cut | Ordered grid alone |
|---|---|---|
| OPEN first, then FOLD | **Differs.** 0–2 s shows FOLD; 2–4 s shows OPEN. Swap those two cards. | **Differs.** Left reads FOLD, middle reads OPEN. These cells show order, not elapsed time. |
| PLACE third | **Matches.** PLACE is visible from 4–6 s. | **Matches** in the right cell. |
| “Made by Example Studio” throughout PLACE | **Differs.** No credit in any of the 24 PLACE frames. Add it for the full card. | **Differs** in the right cell. This disproves continuous visibility; visibility in all other PLACE frames is **not checked**. |
| Three consecutive two-second cards | **Matches.** All 72 frames were decoded at 12 fps. The visual changes occur at 2 and 4 s; the cut ends at 6 s. | **Not checked.** No timecodes, cut boundaries or evidence of what happens between cells. |
| One short tone at PLACE onset; none on earlier cards | **Matches.** The decoded waveform has a single tone at about 4.00–4.25 s. | **Not checked.** The grid contains no audio evidence. |

Both reviews call for revision. Only the full-cut review supports keeping the existing timing and cue. Neither review authorizes publication.

## Reproduce the exercise

With Pillow 12 and FFmpeg (including the H.264 encoder) already available locally, run the [fixture maker](make_video_cut_fixture.py) from the repository root:

```text
python docs/examples/make_video_cut_fixture.py paper-signals-test
```

Use a new output directory. The fixture maker draws three fictional cards, synthesizes a tone, and samples the encoded cut to make an untimed grid. It does not read project assets. For a blind repeat, give each reviewer only the skill, the brief and **one** artifact: `edition-a.mp4` or `ordered-grid.png`. Withhold this worked answer and the fixture maker.
