[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ArtifactDirectory,
    [Parameter(Mandatory = $true)][ValidatePattern('^\d+\.\d+\.\d+$')][string]$Version,
    [ValidateSet("x64", "arm64")][string]$Architecture = "x64"
)

$ErrorActionPreference = "Stop"
$artifacts = (Resolve-Path -LiteralPath $ArtifactDirectory).Path
$installer = Join-Path $artifacts "leomoon-jalalitray-$Version-windows-$Architecture-setup.exe"
$checksums = Join-Path $artifacts "SHA256SUMS"
if (-not (Test-Path -LiteralPath $installer -PathType Leaf)) { throw "Windows installer is missing" }
if (-not (Test-Path -LiteralPath $checksums -PathType Leaf)) { throw "SHA256SUMS is missing" }
foreach ($line in Get-Content -LiteralPath $checksums) {
    if ($line -notmatch '^([0-9a-f]{64}) \*(.+)$') { throw "Invalid SHA256SUMS entry: $line" }
    $actual = (Get-FileHash -LiteralPath (Join-Path $artifacts $Matches[2]) -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $Matches[1]) { throw "Checksum mismatch for $($Matches[2])" }
}

function Invoke-CheckedProcess([string]$FilePath, [string[]]$Arguments, [int]$TimeoutSeconds = 60) {
    $process = Start-Process -FilePath $FilePath -ArgumentList $Arguments -PassThru
    if (-not $process.WaitForExit($TimeoutSeconds * 1000)) { $process.Kill($true); throw "$FilePath did not finish within $TimeoutSeconds seconds" }
    if ($process.ExitCode -ne 0) { throw "$FilePath failed with exit code $($process.ExitCode)" }
}

$testRoot = Join-Path $env:RUNNER_TEMP "leomoon-jalalitray-windows-installer-smoke"
$installDirectory = Join-Path $testRoot "application"
$startupKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$startupValue = "LeoMoon JalaliTray"
try {
    Remove-Item -LiteralPath $testRoot -Recurse -Force -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path $startupKey -Name $startupValue -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Path $testRoot | Out-Null
    $installArguments = @("/SP-", "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/DIR=`"$installDirectory`"", "/TASKS=`"startup`"")
    Invoke-CheckedProcess $installer $installArguments 600
    $application = Join-Path $installDirectory "LeoMoon JalaliTray.exe"
    if (-not (Test-Path -LiteralPath $application -PathType Leaf)) { throw "Installed application is missing" }
    if ((Get-ItemProperty -Path $startupKey -Name $startupValue -ErrorAction Stop).$startupValue -notmatch [regex]::Escape("LeoMoon JalaliTray.exe")) { throw "Startup task was not installed" }

    $applicationProcess = Start-Process -FilePath $application -PassThru
    Start-Sleep -Seconds 3
    if ($applicationProcess.HasExited) { throw "Installed application did not remain running" }
    $applicationProcess.Kill($true)
    $applicationProcess.WaitForExit()

    Invoke-CheckedProcess $installer $installArguments 600
    $uninstaller = Join-Path $installDirectory "unins000.exe"
    if (-not (Test-Path -LiteralPath $uninstaller -PathType Leaf)) { throw "Windows uninstaller is missing" }
    Invoke-CheckedProcess $uninstaller @("/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART") 600
    if (Test-Path -LiteralPath $installDirectory) { throw "Application directory remains after uninstall" }
    if (Get-ItemProperty -Path $startupKey -Name $startupValue -ErrorAction SilentlyContinue) { throw "Startup task remains after uninstall" }
} finally {
    Remove-Item -LiteralPath $testRoot -Recurse -Force -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path $startupKey -Name $startupValue -ErrorAction SilentlyContinue
}

Write-Host "Windows installer install, startup, upgrade, launch, and uninstall checks passed"
