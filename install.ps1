# 安装 interactive-skill-distiller 到 WorkBuddy skills 目录
param(
    [string]$Dest = "$env:USERPROFILE\.workbuddy\skills"
)

$ErrorActionPreference = "Stop"
$src  = Split-Path -Parent $MyInvocation.MyCommand.Path
$name = "interactive-skill-distiller"

if ([string]::IsNullOrWhiteSpace($Dest) -or $Dest -eq $env:USERPROFILE -or $Dest.TrimEnd('\','/') -eq '') {
    Write-Error "目标路径不安全或为空：$Dest"
    exit 2
}

New-Item -ItemType Directory -Force -Path $Dest | Out-Null
$target = Join-Path $Dest $name

if (Test-Path $target) {
    $backup = "$target.bak.$(Get-Date -Format 'yyyyMMddHHmmss')"
    Move-Item -LiteralPath $target -Destination $backup
    Write-Host "[i] 旧版本已备份 -> $backup"
}

Copy-Item -LiteralPath $src -Destination $target -Recurse -Force
Remove-Item -LiteralPath (Join-Path $target "install.sh")  -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $target "install.ps1") -ErrorAction SilentlyContinue

Write-Host "[+] 已安装 -> $target"
Write-Host "    重启会话或重新索引后生效"
