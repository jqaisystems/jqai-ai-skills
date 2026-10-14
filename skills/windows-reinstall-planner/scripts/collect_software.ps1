[CmdletBinding()]
param([string]$OutputPath)

# Dot-source to test the adapters without inspecting the current machine.
function Get-RegistrySoftware {
    $roots = @(
        @{ Path = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'; Source = 'registry-machine' },
        @{ Path = 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'; Source = 'registry-machine-32' },
        @{ Path = 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'; Source = 'registry-user' }
    )
    foreach ($root in $roots) {
        if (-not (Test-Path -LiteralPath $root.Path)) { continue }
        foreach ($entry in Get-ChildItem -LiteralPath $root.Path -ErrorAction Stop) {
            $name = [string]$entry.GetValue('DisplayName')
            if ([string]::IsNullOrWhiteSpace($name)) { continue }
            [pscustomobject]@{
                source = $root.Source; name = $name
                version = [string]$entry.GetValue('DisplayVersion')
                publisher = [string]$entry.GetValue('Publisher')
                package_id = ''; evidence = 'registered'
            }
        }
    }
}

function Get-StoreSoftware {
    if (-not (Get-Command Get-AppxPackage -ErrorAction SilentlyContinue)) { throw 'Store adapter unavailable' }
    Get-AppxPackage -ErrorAction Stop | ForEach-Object {
        [pscustomobject]@{
            source = 'store-current-user'; name = [string]$_.Name
            version = [string]$_.Version; publisher = [string]$_.Publisher
            package_id = [string]$_.PackageFamilyName; evidence = 'registered'
        }
    }
}

function Get-StartMenuSoftware {
    if (-not (Get-Command Get-StartApps -ErrorAction SilentlyContinue)) { throw 'Start menu adapter unavailable' }
    Get-StartApps -ErrorAction Stop | ForEach-Object {
        [pscustomobject]@{
            source = 'start-menu'; name = [string]$_.Name
            version = ''; publisher = ''; package_id = ''; evidence = 'shortcut-only'
        }
    }
}

function Get-SoftwareInventory {
    $records = New-Object System.Collections.Generic.List[object]
    $coverage = New-Object System.Collections.Generic.List[object]
    foreach ($adapter in @('Registry', 'Store', 'StartMenu')) {
        $before = $records.Count
        try {
            $rows = switch ($adapter) {
                'Registry' { @(Get-RegistrySoftware) }
                'Store' { @(Get-StoreSoftware) }
                'StartMenu' { @(Get-StartMenuSoftware) }
            }
            foreach ($row in $rows) {
                if ([string]::IsNullOrWhiteSpace($row.name)) { continue }
                $records.Add([ordered]@{
                    record_id = ('SW-{0:D5}' -f ($records.Count + 1))
                    source = [string]$row.source; name = [string]$row.name
                    version = [string]$row.version; publisher = [string]$row.publisher
                    package_id = [string]$row.package_id; evidence = [string]$row.evidence
                })
            }
            $coverage.Add([ordered]@{ source = $adapter; status = 'complete'; count = $records.Count - $before })
        } catch {
            # Do not include provider diagnostics or machine-specific values.
            $coverage.Add([ordered]@{ source = $adapter; status = 'unavailable'; count = $records.Count - $before })
        }
    }
    return [ordered]@{
        schema_version = 1; captured_at = [DateTime]::UtcNow.ToString('o')
        coverage = @($coverage.ToArray()); records = @($records.ToArray())
    }
}

function Save-SoftwareInventory {
    param([Parameter(Mandatory = $true)][string]$Destination)
    $full = [IO.Path]::GetFullPath($Destination)
    if ($full.StartsWith('\\')) { throw 'Choose a local output file' }
    if (Test-Path -LiteralPath $full) { throw 'Output already exists; choose a new filename' }
    $parent = Split-Path -Parent $full
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) { throw 'Output parent directory must already exist' }
    $cursor = Get-Item -LiteralPath $parent -Force
    while ($null -ne $cursor) {
        if (($cursor.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw 'Linked output directories are not supported'
        }
        $cursor = $cursor.Parent
    }
    $inventory = Get-SoftwareInventory
    $json = $inventory | ConvertTo-Json -Depth 6
    $bytes = (New-Object Text.UTF8Encoding($false)).GetBytes($json)
    $stream = [IO.File]::Open($full, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($bytes, 0, $bytes.Length) } finally { $stream.Dispose() }
    Write-Output ('Saved private inventory: {0} records. No software was changed.' -f $inventory.records.Count)
    if (@($inventory.coverage | Where-Object { $_.status -ne 'complete' }).Count -gt 0) {
        Write-Warning 'Collection is partial. Review coverage before making a reinstall plan.'
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    if ([string]::IsNullOrWhiteSpace($OutputPath)) { throw '-OutputPath is required' }
    Save-SoftwareInventory -Destination $OutputPath
}
