param(
    [Parameter(Mandatory = $true)][string]$Completed,
    [Parameter(Mandatory = $true)][string]$Learned,
    [Parameter(Mandatory = $true)][string]$NextSteps,
    [string]$Blockers = 'None'
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$progressPath = Join-Path $projectRoot 'DAILY_PROGRESS.md'
$indiaZone = [TimeZoneInfo]::FindSystemTimeZoneById('India Standard Time')
$entryDate = [TimeZoneInfo]::ConvertTimeFromUtc([DateTime]::UtcNow, $indiaZone).ToString('yyyy-MM-dd')
$entry = @"

## $entryDate

### Completed
$Completed

### Learned
$Learned

### Next steps
$NextSteps

### Blockers
$Blockers
"@
Add-Content -LiteralPath $progressPath -Value $entry -Encoding UTF8
Write-Host "Daily update saved to $progressPath"
Write-Host 'Review the entry, then commit and push it when ready.'
