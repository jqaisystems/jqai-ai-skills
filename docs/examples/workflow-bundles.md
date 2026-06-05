# Workflow Bundles

Use these bundles when one skill is useful, but the job naturally needs a small sequence of repeatable workflows.

Each bundle below is public-safe and uses generic examples. Adapt the prompts to your own workspace after reviewing what each skill does.

## Bundle 1: Public GitHub Publishing

Use this bundle when you are turning private project work into public-safe GitHub proof.

### Install

```powershell
.\install.ps1 github-safe-publisher
.\install.ps1 case-study-writer
.\install.ps1 release-announcement-writer
```

### When To Use It

- You have a repo, README, example, release note, or case study that came from real project work.
- You want to publish the pattern without exposing source-only details.
- You need a release note, website blurb, or short launch post after the artifact is safe.

### Suggested Flow

1. Run `github-safe-publisher` on the candidate public artifact.
2. If the work needs a proof story, run `case-study-writer` from sanitized notes.
3. After the public artifact is ready, run `release-announcement-writer` from the final diff or changelog.

### Example Prompts

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

```text
Use $case-study-writer to turn this sanitized project summary into a public-safe case study.
```

```text
Use $release-announcement-writer to turn this changelog into GitHub release notes, a website blurb, and a short launch post.
```

### Expected Outputs

- Safety verdict with blocking issues, review notes, and ready state.
- Public-safe case study draft, if needed.
- Release notes and short launch copy.

### Review Gate

Do not publish until the safety review is `READY`, the diff is manually reviewed, and the final artifact contains only public-safe material.

## Bundle 2: Content And Research

Use this bundle when you collect public sources, extract page data, organize notes, and clean copy.

### Install

```powershell
.\install.ps1 research-brief-curator
.\install.ps1 web-scraper
.\install.ps1 em-dash-remover
```

### When To Use It

- You are collecting public links or saved notes into a daily or weekly brief.
- You need structured extraction from public or authorized pages.
- You want a final copy pass that removes one common AI-writing tell.

### Suggested Flow

1. Use `web-scraper` only when page extraction is authorized and useful.
2. Use `research-brief-curator` to turn approved links and notes into a brief with source tracking.
3. Use `em-dash-remover` on the final public copy if the style needs cleanup.

### Example Prompts

```text
Use $web-scraper to create a browser console script for this public paginated directory.
```

```text
Use $research-brief-curator to turn these public links into a weekly research brief with source labels.
```

```text
Use $em-dash-remover to clean this brief without changing the meaning.
```

### Expected Outputs

- Browser console extraction script, when needed.
- Source-aware brief with visibility labels.
- Cleaned final copy.

### Review Gate

Confirm source access is allowed, keep source links visible, and review the final brief before posting, sending, or archiving it publicly.

## Bundle 3: Demo And Launch

Use this bundle when you need to show a workflow and then announce it clearly.

### Install

```powershell
.\install.ps1 demo-animation-v2
.\install.ps1 release-announcement-writer
```

### When To Use It

- You have a tool, workflow, or system that benefits from a short visual walkthrough.
- You need a lightweight demo asset for GitHub, a website page, or a launch note.
- You want the release copy to match what the demo actually shows.

### Suggested Flow

1. Compare the target shape with [`demo-animation-v2-walkthrough-sample.md`](demo-animation-v2-walkthrough-sample.md).
2. Use `demo-animation-v2` to create the responsive walkthrough.
3. Review the demo for accuracy, readable text, and public-safe visuals.
4. Use `release-announcement-writer` from the final demo notes and shipped changes.

### Example Prompts

```text
Use $demo-animation-v2 to create a responsive walkthrough for this public workflow.
```

```text
Use $release-announcement-writer to write a GitHub release note and short launch post from this demo summary.
```

### Expected Outputs

- Responsive HTML walkthrough demo.
- Public-safe demo review notes.
- Release notes, website blurb, and short launch copy.
- Checklist of links or assets to verify before publishing.

### Review Gate

Check the demo at desktop and mobile sizes, confirm all on-screen text is public-safe, and verify that the launch copy only claims what the demo shows.

## Choosing A Bundle

| If your goal is... | Start with |
|---|---|
| Publish proof from real project work | Public GitHub Publishing |
| Turn public sources into a brief | Content And Research |
| Show a workflow and launch it | Demo And Launch |

If you are not sure, start with one skill from [`docs/guides/skill-selection.md`](../guides/skill-selection.md) before installing a bundle.
