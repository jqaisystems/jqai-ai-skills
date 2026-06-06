# Release Showcase Handoff Sample

This sample shows the expected public-safe handoff after a release is published and needs to be reflected across public showcase surfaces.

It is not a deployment log. It uses a fictional release called **Example Skill Library v1.2.3** so visitors can inspect the operating routine without exposing hosting credentials, account screens, private file paths, deployment configuration, analytics, or unpublished project notes.

## When To Use This

Use this proof shape when a public release needs to move through more than one surface:

```text
GitHub release -> profile update -> website source update -> host upload package -> live verification -> project note
```

The goal is to prove that a release does not stop at a tag. The public surfaces should agree on the latest release, the proof links should work, stale version references should be checked, and the final status should be easy to audit later.

## Fake Release Brief

```text
Release: Example Skill Library v1.2.3
Release theme: Add a public-safe onboarding walkthrough sample.
Primary proof asset: docs/examples/onboarding-walkthrough-sample.md
Stable visual asset: unchanged
Repo release URL: https://github.com/example/example-skill-library/releases/tag/v1.2.3
Website system URL: https://www.example.com/systems/example-skill-library
Website blog URL: https://www.example.com/blog/example-skill-library
Public text file: https://www.example.com/llms.txt
Sitemap: https://www.example.com/sitemap.xml
```

## Expected Handoff Artifacts

| Artifact | Expected public-safe content |
|---|---|
| GitHub release | Version tag, release notes, proof asset links, validation result, stable visual note. |
| Profile update | Short current-release summary and announcement copy with public GitHub links only. |
| Website system page | Current version, proof asset wording, release link, and no stale previous version. |
| Website blog page | Current version, proof asset wording, updated date, and no stale previous version. |
| `llms.txt` | Current version and proof asset summary for machine-readable discovery. |
| `sitemap.xml` | Updated `lastmod` values only for changed public URLs. |
| Upload package | Only the files needed by the host, plus a short upload README. |
| Live verification note | URL status, current version checks, stale version checks, and final verdict. |

## Handoff Checklist

### 1. Confirm The Release Exists

```text
PASS:
- The release tag exists on GitHub.
- The release page is public.
- The release notes link to the new proof asset.
- Validation checks passed for the release commit.
- The stable visual asset is unchanged unless the release explicitly updates it.
```

### 2. Update The Profile Surface

```text
Profile files:
- README.md
- announcements/example-skill-library-v1.2.3.md
```

Profile copy should include:

- the current release version;
- a one-sentence release summary;
- the primary proof asset link;
- the quality or proof index link if useful;
- a safety note when the proof asset uses fictional data.

Avoid:

- private project names;
- account URLs;
- internal release notes;
- local paths;
- screenshots or links from private tools.

### 3. Prepare The Website Source Update

```text
Website files:
- systems/example-skill-library.php
- posts/example-skill-library.php
- llms.txt
- sitemap.xml
```

Website copy should include:

- the current release version;
- the new proof asset wording;
- links to the public GitHub release and proof file;
- a `lastmod` update only for the pages changed in this cycle;
- no stale previous release references in the edited surfaces.

### 4. Build The Host Upload Package

The package should contain only the host-facing files:

```text
example-skill-library-v1.2.3-site-update-YYYYMMDD/
  README_UPLOAD.md
  llms.txt
  sitemap.xml
  posts/
    example-skill-library.php
  systems/
    example-skill-library.php
```

The upload README should say:

- which files to upload;
- which paths to preserve;
- what changed;
- which live URLs to verify after upload.

Do not include:

- raw workspace folders;
- generated archives with extra files;
- screenshots with account UI;
- private hosting notes;
- credentials;
- deployment scripts;
- local machine paths.

### 5. Verify The Live Site

Use public URLs only.

```text
Expected checks:
- /systems/example-skill-library returns 200.
- /systems/example-skill-library includes v1.2.3.
- /systems/example-skill-library includes the new proof wording.
- /systems/example-skill-library does not include v1.2.2.
- /blog/example-skill-library returns 200.
- /blog/example-skill-library includes v1.2.3.
- /blog/example-skill-library includes the new proof wording.
- /blog/example-skill-library does not include v1.2.2.
- /llms.txt includes v1.2.3 and the new proof wording.
- /sitemap.xml includes the changed URLs with the expected lastmod date.
```

If a plain URL still shows stale content, run a cache-busted check before deciding the upload failed:

```text
https://www.example.com/systems/example-skill-library?cb=YYYYMMDD-v123
```

### 6. Record The Final State

The final project note should capture:

- release tag and URL;
- release commit;
- profile commit;
- upload package path;
- live verification results;
- remaining follow-up, if any.

## Result Decision

| Result | Meaning | Next step |
|---|---|---|
| `READY` | GitHub, profile, website package, and live URLs agree on the current release. | Start the next release cycle from this version. |
| `REVIEW` | The release is public, but one public surface is stale or missing a proof link. | Fix that surface, rerun verification, and update the project note. |
| `BLOCK` | Sensitive material, credentials, private paths, account screenshots, or internal deployment details reached the public package. | Stop, remove the material, rebuild the package, and rerun public-safety review. |

## Expected Final Note

```text
READY

Example Skill Library v1.2.3 is published and aligned.

- GitHub release is public.
- Profile announcement is pushed.
- Website package contains only the four host files and upload README.
- Live system page, blog page, llms.txt, and sitemap all verify.
- Previous release v1.2.2 is absent from the checked live surfaces.
- Stable visual asset was intentionally unchanged.
```

## Public-Safety Checks

- Use fictional release names, URLs, and proof assets when creating an example.
- Keep host credentials, account menus, admin URLs, analytics, deployment logs, and local paths out of public docs.
- Do not publish raw chat logs, private prompts, private operational notes, or hidden review details.
- Confirm that upload packages contain only the intended public files.
- Review diffs before committing profile or website copy.
- Treat the final live verification as public evidence, not as a private deployment report.
