# RSI Console - interactive launcher for doc-automation-tools
# Double-click rsi.bat, or run: pwsh -File rsi.ps1

$ErrorActionPreference = 'Stop'
$toolsRoot = $PSScriptRoot
$reposRoot = Split-Path $toolsRoot -Parent

function Get-DocRepos {
    Get-ChildItem $reposRoot -Directory -ErrorAction SilentlyContinue |
        Where-Object { (Test-Path (Join-Path $_.FullName '.git')) -and $_.Name -ne 'doc-automation-tools' } |
        Where-Object { (Test-Path (Join-Path $_.FullName 'zh')) -or (Test-Path (Join-Path $_.FullName 'en')) } |
        Sort-Object Name
}

function Show-Header {
    Clear-Host
    Write-Host ''
    Write-Host '  ===========================================' -ForegroundColor DarkCyan
    Write-Host '   RSI Console  -  doc automation tools' -ForegroundColor Cyan
    Write-Host '  ===========================================' -ForegroundColor DarkCyan
    Write-Host ''
}

function Invoke-Check {
    param([string]$RepoPath)

    Write-Host ''
    Write-Host "  >> $(Split-Path $RepoPath -Leaf)" -ForegroundColor Yellow
    python (Join-Path $toolsRoot 'scripts\check_translations.py') $RepoPath
}

function Select-Repo {
    $repos = @(Get-DocRepos)
    if ($repos.Count -eq 0) {
        Write-Host '  No bilingual repos found.' -ForegroundColor Red
        return $null
    }

    Show-Header
    Write-Host '  Pick a repo:' -ForegroundColor White
    Write-Host ''
    for ($i = 0; $i -lt $repos.Count; $i++) {
        Write-Host ('   {0,2}. {1}' -f ($i + 1), $repos[$i].Name)
    }
    Write-Host ''
    $pick = Read-Host '  Number (blank to cancel)'
    if ([string]::IsNullOrWhiteSpace($pick)) { return $null }

    $index = 0
    if (-not [int]::TryParse($pick, [ref]$index) -or $index -lt 1 -or $index -gt $repos.Count) {
        Write-Host '  Invalid choice.' -ForegroundColor Red
        return $null
    }
    return $repos[$index - 1].FullName
}

function Invoke-CheckAll {
    $repos = @(Get-DocRepos)
    Show-Header
    Write-Host "  Scanning $($repos.Count) repos..." -ForegroundColor White
    Write-Host ''
    $script = Join-Path $toolsRoot 'scripts\check_translations.py'
    foreach ($repo in $repos) {
        $line = python $script $repo.FullName --summary
        $color = if ($line -match '\bOK\b') { 'Green' } else { 'Yellow' }
        Write-Host "  $line" -ForegroundColor $color
    }
}

while ($true) {
    Show-Header
    $repos = @(Get-DocRepos)
    Write-Host "  $($repos.Count) bilingual repos detected" -ForegroundColor DarkGray
    Write-Host ''
    Write-Host '   1. Check one repo' -ForegroundColor White
    Write-Host '   2. Check all repos' -ForegroundColor White
    Write-Host '   3. List bilingual repos' -ForegroundColor White
    Write-Host '   4. Open roadmap' -ForegroundColor White
    Write-Host '   Q. Quit' -ForegroundColor White
    Write-Host ''

    switch ((Read-Host '  Choice').Trim().ToUpper()) {
        '1' {
            $repo = Select-Repo
            if ($repo) { Invoke-Check -RepoPath $repo }
            Write-Host ''
            Read-Host '  Enter to continue' | Out-Null
        }
        '2' {
            Invoke-CheckAll
            Write-Host ''
            Read-Host '  Enter to continue' | Out-Null
        }
        '3' {
            Show-Header
            $repos | ForEach-Object { Write-Host "   - $($_.Name)" }
            Write-Host ''
            Read-Host '  Enter to continue' | Out-Null
        }
        '4' {
            Invoke-Item (Join-Path $toolsRoot 'ROADMAP.md')
        }
        'Q' { return }
        default { }
    }
}
