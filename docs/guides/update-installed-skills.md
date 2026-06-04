# Update Installed Skills

Use this guide when you already installed one or more JQ AI Skills and want to refresh them from the latest repo version.

For a full public-safe proof trail after a new release, use [`../examples/update-after-release-proof.md`](../examples/update-after-release-proof.md).

The short version:

1. Update your local repo.
2. Test the skill copy in a temporary target.
3. Reinstall the selected skill or the reviewed set of skills.
4. Restart or reload your AI coding tool.
5. Confirm the copied folder still contains the expected files.

## Before You Update

Work from the repo root:

```powershell
git pull --ff-only
.\install.ps1 -List
```

```bash
git pull --ff-only
chmod +x ./install.sh
./install.sh --list
```

If `git pull --ff-only` stops, inspect the local repo state before continuing. Resolve or save local edits first.

## Update One Skill

Recommended pattern: test the copy into a temporary target first.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\skill-update-check"
Test-Path ".tmp\skill-update-check\github-safe-publisher\SKILL.md"
```

macOS/Linux:

```bash
./install.sh --target .tmp/skill-update-check github-safe-publisher
test -f .tmp/skill-update-check/github-safe-publisher/SKILL.md && echo "installed"
```

If the temporary target looks right, reinstall into your normal target:

```powershell
.\install.ps1 github-safe-publisher
```

```bash
./install.sh github-safe-publisher
```

Restart or reload your AI coding tool after reinstalling.

## Update All Skills

Use the all-skills command only after reviewing what each skill does.

Windows PowerShell:

```powershell
.\install.ps1 -All
```

macOS/Linux:

```bash
./install.sh --all
```

Restart or reload your tool after the update.

## If You Edited A Local Skill

The install scripts copy from this repo into your target folder. If you changed a skill inside your local target, reinstalling can replace that local version.

Before updating:

1. Open the installed skill folder in your target directory.
2. Decide whether your local edits are still needed.
3. Save your local version somewhere outside the target folder if you want to compare it later.
4. Reinstall from the repo only after the local version is safe to replace.

Prefer keeping reusable improvements in the repo copy, then reinstalling from there.

## Confirm The Update

Check the copied folder:

```powershell
Test-Path "$env:USERPROFILE\.codex\skills\github-safe-publisher\SKILL.md"
```

```bash
test -f ~/.codex/skills/github-safe-publisher/SKILL.md && echo "installed"
```

Then run a small first prompt:

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

Expected result: the tool recognizes the skill and returns a structured review shape.

## Clean Up Temporary Checks

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force ".tmp\skill-update-check"
```

macOS/Linux:

```bash
rm -rf .tmp/skill-update-check
```

## Related Links

- [`../../INSTALL.md`](../../INSTALL.md)
- [`install-faq.md`](install-faq.md)
- [`install-verification.md`](install-verification.md)
- [`../examples/update-after-release-proof.md`](../examples/update-after-release-proof.md)
- [`../examples/install-smoke-test-sample.md`](../examples/install-smoke-test-sample.md)
- [`../../TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md)
