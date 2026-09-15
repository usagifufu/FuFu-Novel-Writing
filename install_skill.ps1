# 安装 / 更新 FuFu 小说创作助手技能
#
# 用法：
#   powershell -ExecutionPolicy Bypass -File install_skill.ps1
#   powershell -ExecutionPolicy Bypass -File install_skill.ps1 -SkillsRoot "D:\my\skills"
#
# 行为：自动定位技能根目录 -> 备份旧版本 -> 全量同步本包内容 -> 报告结果

param(
    [string]$SkillsRoot
)

$ErrorActionPreference = "Stop"

$SkillName = "fufu-novel-assistant"
$Src = $PSScriptRoot

# ---------- 1. 定位技能根目录 ----------
if (-not $SkillsRoot) {
    $candidates = @(
        (Join-Path $env:USERPROFILE ".workbuddy\skills"),
        (Join-Path $env:USERPROFILE ".codex\skills"),
        (Join-Path $env:USERPROFILE ".claude\skills")
    )
    foreach ($c in $candidates) {
        if (Test-Path -LiteralPath $c) { $SkillsRoot = $c; break }
    }
}
if (-not $SkillsRoot) {
    $SkillsRoot = Join-Path $env:USERPROFILE ".workbuddy\skills"
}

$Dst = Join-Path $SkillsRoot $SkillName
Write-Host "[目标] $Dst" -ForegroundColor Cyan

# ---------- 2. 备份旧版本 ----------
if (Test-Path -LiteralPath $Dst) {
    $stamp  = Get-Date -Format "yyyyMMdd-HHmmss"
    $Backup = Join-Path (Split-Path $SkillsRoot -Parent) ("skill-backups\" + $SkillName + "-" + $stamp)
    New-Item -ItemType Directory -Path $Backup -Force | Out-Null
    Copy-Item -Path (Join-Path $Dst "*") -Destination $Backup -Recurse -Force
    Write-Host "[备份] $Dst -> $Backup" -ForegroundColor Green
} else {
    New-Item -ItemType Directory -Path $Dst -Force | Out-Null
    Write-Host "[新建] $Dst" -ForegroundColor Green
}

# ---------- 3. 全量同步（排除缓存与临时文件）----------
$ExcludeDirs  = @("__pycache__", "node_modules", ".git", ".pytest_cache", ".vscode", ".idea")
$ExcludeFiles = @(".DS_Store", "Thumbs.db", "desktop.ini")

$count = 0
$skipCount = 0

foreach ($file in (Get-ChildItem -LiteralPath $Src -Recurse -File)) {
    $rel = $file.FullName.Substring($Src.Length).TrimStart('\')

    $skip = $false
    foreach ($d in $ExcludeDirs) {
        if ($rel -like "$d\*" -or $rel -like "*\$d\*") { $skip = $true; break }
    }
    if (-not $skip) {
        if ($ExcludeFiles -contains $file.Name -or $file.Extension -eq ".pyc") { $skip = $true }
    }
    if ($skip) { $skipCount++; continue }

    $target = Join-Path $Dst $rel
    $parent = Split-Path $target -Parent
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    Copy-Item -LiteralPath $file.FullName -Destination $target -Force
    $count++
}

Write-Host ""
Write-Host "[完成] 已同步 $count 个文件（跳过 $skipCount 个缓存/临时文件）。" -ForegroundColor Green
Write-Host "新技能在下次新会话中生效；当前已打开的会话可能仍使用旧缓存。"
