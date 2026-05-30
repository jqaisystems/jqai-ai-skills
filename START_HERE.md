# Start Here

Use this page if you are opening JQ AI Skills for the first time and want the shortest path from overview to first useful run.

## What This Repo Is

JQ AI Skills is a public MIT-licensed library of reusable skill folders for Codex, Claude Code, and similar agentic coding tools.

Each skill packages a repeatable AI workflow as a folder with instructions, metadata, and optional references, scripts, examples, or assets. The goal is simple: turn useful AI work into something inspectable, installable, and reusable.

## Who It Is For

This repo is useful if you:

- publish GitHub proof from real project work and need a safety review habit;
- turn internal work into public-safe case studies or release notes;
- collect public sources into research briefs;
- design human-reviewed outreach, marketplace, demo, or copy workflows;
- want reusable agent routines instead of one-off prompts.

## The Fast Path

Follow this path if you want to try one skill before reading the whole repo.

1. Pick the safest first skill: [`github-safe-publisher`](skills/github-safe-publisher/SKILL.md).
2. Install it with [`INSTALL.md`](INSTALL.md) or the [`one-minute install guide`](docs/guides/one-minute-install.md).
3. Reload your AI coding tool.
4. Run the first prompt:

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

5. Compare the result with the [`first-run sample`](docs/examples/first-run-github-safe-publisher.md).
6. Use [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) if the skill does not appear after install.
7. Use the [`skill selection guide`](docs/guides/skill-selection.md) if your first job is not public GitHub publishing.
8. Use the [`skill anatomy guide`](docs/guides/skill-anatomy.md) when you want to understand what each folder file does.
9. Use the [`catalog`](docs/catalog.md) when you want the full list.

## What To Read First

| Need | Start with |
|---|---|
| Try one skill fast | [`docs/guides/one-minute-install.md`](docs/guides/one-minute-install.md) |
| Install command reference | [`INSTALL.md`](INSTALL.md) |
| Fix install or reload issues | [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) |
| Review release history | [`CHANGELOG.md`](CHANGELOG.md) |
| Publish a release safely | [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) |
| Understand security and responsible use | [`SECURITY.md`](SECURITY.md) |
| See the public roadmap | [`ROADMAP.md`](ROADMAP.md) |
| Get help or report an issue | [`SUPPORT.md`](SUPPORT.md) |
| Compare skill maturity | [`docs/skill-quality-matrix.md`](docs/skill-quality-matrix.md) |
| Understand a skill folder | [`docs/guides/skill-anatomy.md`](docs/guides/skill-anatomy.md) |
| Understand first-run output | [`docs/examples/first-run-github-safe-publisher.md`](docs/examples/first-run-github-safe-publisher.md) |
| Browse public-safe examples | [`docs/examples/README.md`](docs/examples/README.md) |
| Choose the right first skill | [`docs/guides/skill-selection.md`](docs/guides/skill-selection.md) |
| Browse every skill | [`docs/catalog.md`](docs/catalog.md) |
| Combine skills into a workflow | [`docs/examples/workflow-bundles.md`](docs/examples/workflow-bundles.md) |

## Recommended First Skill

Start with `github-safe-publisher` if you are unsure.

It teaches the core review pattern used across this library:

```text
inspect candidate -> scan for common risks -> review diff -> publish only after approval
```

That pattern matters because reusable AI workflows should not just be clever. They should be reviewable.

## Safe First-Run Rules

- Start with one skill.
- Read `SKILL.md` before using a skill on sensitive work.
- Use a test folder first.
- Do not paste credentials, tokens, account data, logs, exports, or unpublished prompt notes into a tool unless you understand where they will go.
- Review diffs before committing public artifacts.

## After The First Run

Once the first skill makes sense:

- Use [`docs/examples/workflow-bundles.md`](docs/examples/workflow-bundles.md) for multi-skill paths.
- Use [`docs/examples/README.md`](docs/examples/README.md) to browse public-safe examples by job.
- Use [`docs/catalog.md`](docs/catalog.md) to browse the full library.
- Use [`docs/guides/skill-anatomy.md`](docs/guides/skill-anatomy.md) before adapting or creating a skill folder.
- Use [`CHANGELOG.md`](CHANGELOG.md) to see what changed across public releases.
- Use [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) before publishing a new public release.
- Use [`SECURITY.md`](SECURITY.md) before using skills on sensitive or client-facing work.
- Use [`ROADMAP.md`](ROADMAP.md) to see where the public library is going next.
- Use [`SUPPORT.md`](SUPPORT.md) when you need install help, want to report a problem, or have a public-safe question.
- Use [`docs/skill-quality-matrix.md`](docs/skill-quality-matrix.md) to compare maturity, examples, and safety sensitivity.
- Use [`skills/_template/`](skills/_template/) if you want to create a new skill folder.
- Use [`CONTRIBUTING.md`](CONTRIBUTING.md) before proposing changes.

## Repo Map

```text
skills/                 installable skill folders
docs/guides/            first-use and selection guides
docs/examples/          sample outputs, examples index, and workflow examples
docs/announcements/     release notes
docs/skill-quality-matrix.md  maturity and safety comparison
CHANGELOG.md            public release history
RELEASE_CHECKLIST.md    safe public release routine
SECURITY.md             security and responsible-use policy
ROADMAP.md              public-safe direction of travel
SUPPORT.md              help, issue, and sensitive-reporting guidance
.github/ISSUE_TEMPLATE/ public issue forms
.github/PULL_REQUEST_TEMPLATE.md
assets/                 public visual and demo assets
```

The public onboarding path is now:

```text
START_HERE -> understand anatomy -> choose -> INSTALL -> troubleshoot or support if needed -> SECURITY if sensitive -> run -> understand output -> release checklist if publishing -> use bundles, catalog, or quality matrix
```
