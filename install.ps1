[CmdletBinding()]
param(
  [string]$Skill = "web-scraper",
  [string]$Target = $(Join-Path $HOME ".codex\skills"),
  [switch]$All,
  [switch]$List,
  [switch]$DryRun,
  [switch]$Replace
)
$ErrorActionPreference = "Stop"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { throw "Python 3.11 or newer is required. No dependency will be installed automatically." }
& $python.Source -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"
if ($LASTEXITCODE -ne 0) { throw "Python 3.11 or newer is required." }
$arguments = @("-B", (Join-Path $PSScriptRoot "tools/install_skills.py"), $Skill, "--target", $Target)
if ($All) { $arguments += "--all" }
if ($List) { $arguments += "--list" }
if ($DryRun) { $arguments += "--dry-run" }
if ($Replace) { $arguments += "--replace" }
& $python.Source @arguments
if ($LASTEXITCODE -ne 0) { throw "Installation stopped. No existing installation is silently replaced." }
