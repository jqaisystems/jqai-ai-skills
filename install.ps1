[CmdletBinding()]
param(
  [string]$Skill = "web-scraper",
  [string]$Target = $(Join-Path $HOME ".codex\skills"),
  [switch]$All,
  [switch]$List
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsRoot = Join-Path $RepoRoot "skills"

function Get-PublicSkills {
  Get-ChildItem -LiteralPath $SkillsRoot -Directory |
    Where-Object { $_.Name -ne "_template" -and (Test-Path (Join-Path $_.FullName "SKILL.md")) } |
    Sort-Object Name
}

if ($List) {
  Get-PublicSkills | ForEach-Object { $_.Name }
  exit 0
}

if (-not (Test-Path -LiteralPath $SkillsRoot)) {
  throw "Could not find skills folder at $SkillsRoot"
}

$selected = if ($All) {
  Get-PublicSkills
} else {
  $source = Join-Path $SkillsRoot $Skill
  if (-not (Test-Path -LiteralPath (Join-Path $source "SKILL.md"))) {
    $available = (Get-PublicSkills | ForEach-Object { $_.Name }) -join ", "
    throw "Skill '$Skill' was not found. Available skills: $available"
  }
  @(Get-Item -LiteralPath $source)
}

New-Item -ItemType Directory -Force -Path $Target | Out-Null

foreach ($skillDir in $selected) {
  $destination = Join-Path $Target $skillDir.Name
  if (Test-Path -LiteralPath $destination) {
    Remove-Item -LiteralPath $destination -Recurse -Force
  }
  Copy-Item -LiteralPath $skillDir.FullName -Destination $destination -Recurse -Force
  Write-Host "Installed $($skillDir.Name) -> $destination"
}

Write-Host "Restart Codex or reload your AI coding tool so the skill list refreshes."
