$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '../skills/windows-reinstall-planner/scripts/collect_software.ps1')

function Assert($Condition, $Message) { if (-not $Condition) { throw $Message } }
function Get-RegistrySoftware {
    [pscustomobject]@{ source='registry-user';name='Example Editor';version='1.0';publisher='Example Studio';package_id='';evidence='registered' }
}
function Get-StoreSoftware {
    [pscustomobject]@{ source='store-current-user';name='Example Player';version='2.0';publisher='Example Studio';package_id='sample.package';evidence='registered' }
}
function Get-StartMenuSoftware {
    [pscustomobject]@{ source='start-menu';name='Example Shortcut';version='';publisher='';package_id='';evidence='shortcut-only' }
}
$data = Get-SoftwareInventory
Assert ($data.records.Count -eq 3) 'Expected three synthetic records'
Assert (@($data.records.record_id | Select-Object -Unique).Count -eq 3) 'IDs must be unique'
Assert (@($data.coverage | Where-Object { $_.status -eq 'complete' }).Count -eq 3) 'Coverage must be complete'
Assert ($data.records[2].version -eq '') 'Unknown versions must stay blank'
Assert ($data.records[2].evidence -eq 'shortcut-only') 'Shortcuts are not verified installs'

function Get-StoreSoftware { throw 'Synthetic adapter failure with undisclosed diagnostics' }
$data = Get-SoftwareInventory
Assert ($data.records.Count -eq 2) 'Expected two records on partial collection'
Assert (($data.coverage | Where-Object { $_.source -eq 'Store' }).status -eq 'unavailable') 'Missing adapter must be visible'
Assert (($data | ConvertTo-Json -Depth 6) -notmatch 'undisclosed diagnostics') 'Raw errors must not leak'

$temp = Join-Path ([IO.Path]::GetTempPath()) ('reinstall-fixture-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($temp) | Out-Null
$destination = Join-Path $temp 'inventory.json'
Save-SoftwareInventory -Destination $destination
$saved = Get-Content -LiteralPath $destination -Raw | ConvertFrom-Json
Assert ($saved.records.Count -eq 2) 'Saved fixture must match collection'
$blocked = $false
try { Save-SoftwareInventory -Destination $destination } catch { $blocked = $true }
Assert $blocked 'Existing output must not be overwritten'
# Only the uniquely generated fixture directory is removed.
$resolved = [IO.Path]::GetFullPath($temp)
$expectedParent = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
Assert ($resolved.StartsWith($expectedParent, [StringComparison]::OrdinalIgnoreCase)) 'Cleanup outside temp root'
Remove-Item -LiteralPath $resolved -Recurse -Force
Write-Output 'PASS: synthetic collector, partial coverage, unique IDs, privacy, and overwrite protection'
