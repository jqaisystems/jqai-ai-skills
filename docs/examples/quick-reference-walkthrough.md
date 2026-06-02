# Quick Reference Walkthrough

This walkthrough shows how a new visitor can use `QUICK_REFERENCE.md` to move from clone to first safe prompt without reading the whole repo first.

Scenario: a builder wants to try one skill, confirm it copies correctly, and ask for a public-release review on a small README and docs folder.

## 1. Clone The Repo

Windows PowerShell:

```powershell
git clone https://github.com/jqaisystems/jqai-ai-skills.git
cd jqai-ai-skills
```

macOS/Linux:

```bash
git clone https://github.com/jqaisystems/jqai-ai-skills.git
cd jqai-ai-skills
```

## 2. Open The Short Map

Open [`../../QUICK_REFERENCE.md`](../../QUICK_REFERENCE.md).

That page gives you the shortest route through:

- first skill choice;
- install commands;
- temporary install checks;
- first prompt;
- public-safe publishing checks;
- useful follow-up links.

## 3. List Available Skills

Windows PowerShell:

```powershell
.\install.ps1 -List
```

macOS/Linux:

```bash
chmod +x ./install.sh
./install.sh --list
```

Expected result: the command prints installable skill folder names, including `github-safe-publisher`.

## 4. Test A Temporary Install Target

Use a disposable target before installing into your normal tool folder.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher -Target ".tmp\skill-install-smoke"
Test-Path ".tmp\skill-install-smoke\github-safe-publisher\SKILL.md"
```

macOS/Linux:

```bash
./install.sh --target .tmp/skill-install-smoke github-safe-publisher
test -f .tmp/skill-install-smoke/github-safe-publisher/SKILL.md && echo "installed"
```

Expected result: the skill folder is copied and `SKILL.md` exists in the temporary target.

## 5. Install The First Skill

After the smoke test looks right, install the recommended first skill.

Windows PowerShell:

```powershell
.\install.ps1 github-safe-publisher
```

macOS/Linux:

```bash
./install.sh github-safe-publisher
```

Restart or reload your AI coding tool so it can discover the copied skill folder.

## 6. Run The First Prompt

Use a small public-release candidate first, such as a README and docs folder. If you do not have fake files ready, use the [`first-skill candidate pack`](first-skill-candidate/README.md) and compare your result with its [`expected review`](first-skill-candidate/expected-review.md).

```text
Use $github-safe-publisher to review this README and docs folder before public release.
```

A good first result should include:

- a `READY`, `REVIEW`, or `BLOCK` verdict;
- which files were inspected;
- scanner summary;
- manual review checks;
- exact next steps before publishing.

## 7. Compare Expected Output

Use these examples to understand what a healthy result looks like:

- [`first-skill-walkthrough.md`](first-skill-walkthrough.md)
- [`first-skill-candidate/README.md`](first-skill-candidate/README.md)
- [`first-skill-candidate/expected-review.md`](first-skill-candidate/expected-review.md)
- [`install-smoke-test-sample.md`](install-smoke-test-sample.md)
- [`first-run-github-safe-publisher.md`](first-run-github-safe-publisher.md)
- [`github-safe-publisher-sample-review.md`](github-safe-publisher-sample-review.md)

## 8. Clean Up The Smoke Test

Remove only the temporary install target after you no longer need it.

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force ".tmp\skill-install-smoke"
```

macOS/Linux:

```bash
rm -rf .tmp/skill-install-smoke
```

## What This Teaches

- Start with one skill.
- Confirm install behavior in a disposable target.
- Reload before expecting the skill to appear.
- Use a small public-release candidate for the first prompt.
- Compare the result with public-safe examples before using the workflow on larger releases.

## Related Links

- [`../../QUICK_REFERENCE.md`](../../QUICK_REFERENCE.md)
- [`first-skill-walkthrough.md`](first-skill-walkthrough.md)
- [`first-skill-candidate/README.md`](first-skill-candidate/README.md)
- [`first-skill-candidate/expected-review.md`](first-skill-candidate/expected-review.md)
- [`../../INSTALL.md`](../../INSTALL.md)
- [`../guides/install-verification.md`](../guides/install-verification.md)
- [`install-smoke-test-sample.md`](install-smoke-test-sample.md)
- [`first-run-github-safe-publisher.md`](first-run-github-safe-publisher.md)
- [`../../TROUBLESHOOTING.md`](../../TROUBLESHOOTING.md)
