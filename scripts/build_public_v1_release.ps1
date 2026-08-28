param(
  [string]$DesktopPath = 'C:\Users\Lenovo\Desktop'
)

$ErrorActionPreference = 'Stop'
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$releaseName = '模评云官网与国赛智库_V1.0_不含智能体'
$releaseFolder = [System.IO.Path]::GetFullPath((Join-Path $DesktopPath $releaseName))
$releaseZip = [System.IO.Path]::GetFullPath((Join-Path $DesktopPath "$releaseName.zip"))

if (-not $releaseFolder.StartsWith([System.IO.Path]::GetFullPath($DesktopPath), [System.StringComparison]::OrdinalIgnoreCase)) {
  throw '发布目录不在指定桌面路径内。'
}
if (Test-Path -LiteralPath $releaseFolder) {
  throw "发布目录已存在，请先确认后再处理：$releaseFolder"
}
if (Test-Path -LiteralPath $releaseZip) {
  throw "发布压缩包已存在，请先确认后再处理：$releaseZip"
}

$siteFiles = @(
  'index.html',
  'download.html',
  'knowledge.html',
  'styles.css',
  'script.js',
  'knowledge.css',
  'knowledge.js'
)
$assetFiles = @(
  'assets\logo-mark.svg',
  'assets\hero-dashboard.png',
  'assets\reference-paper-page-1.png',
  'assets\reference-paper-page-2.png',
  'assets\reference-paper-page-3.png',
  'assets\reference-paper-page-4.png',
  'assets\reference-paper-page-5.png',
  'assets\reference-paper-page-6.png'
)
$referencePdf = 'output\pdf\reference-paper.pdf'
$learningPacksDirectory = 'assets\learning-packs'

$requiredSources = @($siteFiles + $assetFiles + $referencePdf)
foreach ($relativePath in $requiredSources) {
  $sourcePath = Join-Path $projectRoot $relativePath
  if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
    throw "缺少发布所需文件：$relativePath"
  }
}
if (-not (Test-Path -LiteralPath (Join-Path $projectRoot $learningPacksDirectory) -PathType Container)) {
  throw "缺少课程资料目录：$learningPacksDirectory"
}

New-Item -ItemType Directory -Path $releaseFolder | Out-Null
New-Item -ItemType Directory -Path (Join-Path $releaseFolder 'assets') | Out-Null

foreach ($relativePath in $siteFiles) {
  Copy-Item -LiteralPath (Join-Path $projectRoot $relativePath) -Destination (Join-Path $releaseFolder $relativePath)
}
foreach ($relativePath in $assetFiles) {
  Copy-Item -LiteralPath (Join-Path $projectRoot $relativePath) -Destination (Join-Path $releaseFolder $relativePath)
}
Copy-Item -LiteralPath (Join-Path $projectRoot $referencePdf) -Destination (Join-Path $releaseFolder 'assets\reference-paper.pdf')
Copy-Item -LiteralPath (Join-Path $projectRoot $learningPacksDirectory) -Destination (Join-Path $releaseFolder 'assets') -Recurse

Copy-Item -LiteralPath (Join-Path $projectRoot 'index.html') -Destination (Join-Path $releaseFolder '双击这里打开_模评云官网.html')

$readme = @'
模评云官网与国赛智库 V1.0（不含智能体）
发布日期：2026-08-24

一、如何打开
1. 解压压缩包后，请保持文件夹结构不变。
2. 双击“ 双击这里打开_模评云官网.html ”进入模评云官网。
3. 如需直接查看知识库，可双击“ knowledge.html ”。

二、本版本包含
- 模评云官网展示页
- 国赛智库（2015—2025）
- 61 个常用数学建模方法
- 92 篇优秀论文索引
- 参考论文 PDF 及页面预览
- 18 讲数学建模课程资料包
- 智能算法课程包与保命指南
- 页面所需的图片、样式和交互脚本

三、本版本不包含
- 模评云智能体
- 论文上传、自动评分和在线诊断服务
- 语料库后台、服务器、数据库、API 和密钥

四、使用说明
- 官网和知识库主体可以在电脑浏览器中直接打开。
- 历年赛题、优秀论文等官方来源链接需要联网访问。
- 课程资料可在“课程资料下载”模块或相应模型知识点内直接下载。
- 顶部与智能体或语料库有关的入口属于后续版本预留，本版本不提供对应功能。
- 对外发布前，请确认资料、品牌标识、QQ 号及邮箱等内容均已获得公开发布许可。
'@
[System.IO.File]::WriteAllText((Join-Path $releaseFolder '使用说明.txt'), $readme.TrimStart(), [System.Text.UTF8Encoding]::new($true))

$forbiddenFiles = @('app.html', 'app.css', 'app.js', 'corpus.html', 'corpus.css', 'corpus.js', 'server.py')
foreach ($forbiddenFile in $forbiddenFiles) {
  if (Test-Path -LiteralPath (Join-Path $releaseFolder $forbiddenFile)) {
    throw "发布包误包含非公开模块：$forbiddenFile"
  }
}

$hashLines = Get-ChildItem -LiteralPath $releaseFolder -File -Recurse |
  Where-Object { $_.Name -ne 'SHA256SUMS.txt' } |
  Sort-Object FullName |
  ForEach-Object {
    $relative = [System.IO.Path]::GetRelativePath($releaseFolder, $_.FullName).Replace('\', '/')
    $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "$hash  $relative"
  }
[System.IO.File]::WriteAllLines((Join-Path $releaseFolder 'SHA256SUMS.txt'), $hashLines, [System.Text.UTF8Encoding]::new($false))

Compress-Archive -LiteralPath $releaseFolder -DestinationPath $releaseZip -CompressionLevel Optimal

Write-Host "RELEASE_FOLDER=$releaseFolder"
Write-Host "RELEASE_ZIP=$releaseZip"
