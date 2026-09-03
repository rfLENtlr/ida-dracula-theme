[CmdletBinding()]
param(
    [string]$IdaUserDir,
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'
$repoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceTheme = Join-Path $repoDir 'themes\dracula\theme.css'

if (-not $IdaUserDir) {
    if ($env:IDA_USER_DIR) {
        $IdaUserDir = $env:IDA_USER_DIR
    }
    elseif ($env:IDAUSR) {
        $IdaUserDir = ($env:IDAUSR -split ';')[0]
    }
    elseif ($env:APPDATA) {
        $IdaUserDir = Join-Path $env:APPDATA 'Hex-Rays\IDA Pro'
    }
    else {
        throw 'Unable to locate the IDA user directory. Pass -IdaUserDir explicitly.'
    }
}

if ([string]::IsNullOrWhiteSpace($IdaUserDir)) {
    throw 'IDA user directory is empty.'
}

$themeDir = Join-Path $IdaUserDir 'themes\dracula'
$themeFile = Join-Path $themeDir 'theme.css'
$backupFile = Join-Path $themeDir 'theme.css.pre-dracula-ida-theme'

if ($Uninstall) {
    if (Test-Path -LiteralPath $backupFile -PathType Leaf) {
        Move-Item -LiteralPath $backupFile -Destination $themeFile -Force
        Write-Host "Restored the previous theme: $themeFile"
    }
    elseif (Test-Path -LiteralPath $themeFile -PathType Leaf) {
        Remove-Item -LiteralPath $themeFile -Force
        Write-Host "Removed: $themeFile"
    }
    else {
        Write-Host "Dracula theme is not installed at: $themeFile"
    }
    Write-Host 'Any user.css overrides were preserved. Restart IDA to refresh themes.'
    exit 0
}

if (-not (Test-Path -LiteralPath $sourceTheme -PathType Leaf)) {
    throw "Missing source theme: $sourceTheme"
}

New-Item -ItemType Directory -Path $themeDir -Force | Out-Null

if ((Test-Path -LiteralPath $themeFile -PathType Leaf) -and
    -not (Test-Path -LiteralPath $backupFile)) {
    $sourceHash = (Get-FileHash -LiteralPath $sourceTheme -Algorithm SHA256).Hash
    $installedHash = (Get-FileHash -LiteralPath $themeFile -Algorithm SHA256).Hash
    if ($sourceHash -ne $installedHash) {
        Copy-Item -LiteralPath $themeFile -Destination $backupFile
        Write-Host "Backed up the previous theme to: $backupFile"
    }
}

Copy-Item -LiteralPath $sourceTheme -Destination $themeFile -Force
Write-Host "Installed Dracula theme: $themeFile"
Write-Host 'Restart IDA, then choose Options -> Colors... -> Current theme -> dracula'
