param(
  [string]$SourceDirectory = 'F:\数学建模'
)

$ErrorActionPreference = 'Stop'
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$targetDirectory = Join-Path $projectRoot 'assets\learning-packs'

$resources = @(
  @{ Order = 1; Source = '第1讲 教材和参考资料.rar'; Target = 'lesson-01-textbooks.rar'; Title = '第1讲 教材和参考资料' },
  @{ Order = 2; Source = '第2讲 层次分析法.rar'; Target = 'lesson-02-ahp.rar'; Title = '第2讲 层次分析法' },
  @{ Order = 3; Source = '第3讲 模糊综合评价.rar'; Target = 'lesson-03-fuzzy-evaluation.rar'; Title = '第3讲 模糊综合评价' },
  @{ Order = 4; Source = '第4讲 熵权法.rar'; Target = 'lesson-04-entropy-weight.rar'; Title = '第4讲 熵权法' },
  @{ Order = 5; Source = '第5讲 Topsis.rar'; Target = 'lesson-05-topsis.rar'; Title = '第5讲 TOPSIS' },
  @{ Order = 6; Source = '第6讲 灰色关联分析.rar'; Target = 'lesson-06-grey-relational-analysis.rar'; Title = '第6讲 灰色关联分析' },
  @{ Order = 7; Source = '第7讲 线性规划.rar'; Target = 'lesson-07-linear-programming.rar'; Title = '第7讲 线性规划' },
  @{ Order = 8; Source = '第8讲 整数规划.rar'; Target = 'lesson-08-integer-programming.rar'; Title = '第8讲 整数规划' },
  @{ Order = 9; Source = '第9讲 非线性规划.rar'; Target = 'lesson-09-nonlinear-programming.rar'; Title = '第9讲 非线性规划' },
  @{ Order = 10; Source = '第10讲 图论与最短路径算法.rar'; Target = 'lesson-10-graph-shortest-path.rar'; Title = '第10讲 图论与最短路径算法' },
  @{ Order = 11; Source = '第11讲 网络最大流问题.rar'; Target = 'lesson-11-maximum-flow.rar'; Title = '第11讲 网络最大流问题' },
  @{ Order = 12; Source = '第12讲 最小费用最大流问题.rar'; Target = 'lesson-12-min-cost-max-flow.rar'; Title = '第12讲 最小费用最大流问题' },
  @{ Order = 13; Source = '第13讲 旅行商(TSP)问题.rar'; Target = 'lesson-13-tsp.rar'; Title = '第13讲 旅行商（TSP）问题' },
  @{ Order = 14; Source = '第14讲 插值算法.rar'; Target = 'lesson-14-interpolation.rar'; Title = '第14讲 插值算法' },
  @{ Order = 15; Source = '第15讲 拟合算法.rar'; Target = 'lesson-15-curve-fitting.rar'; Title = '第15讲 拟合算法' },
  @{ Order = 16; Source = '第16讲 微分方程.rar'; Target = 'lesson-16-differential-equations.rar'; Title = '第16讲 微分方程' },
  @{ Order = 17; Source = '第17讲 时间序列.rar'; Target = 'lesson-17-time-series.rar'; Title = '第17讲 时间序列' },
  @{ Order = 18; Source = '第18讲 聚类分析.rar'; Target = 'lesson-18-clustering.rar'; Title = '第18讲 聚类分析' },
  @{ Order = 19; Source = '智能算法.rar'; Target = 'intelligent-algorithms.rar'; Title = '智能算法课程包' },
  @{ Order = 20; Source = '智能算法与保命指南_20260824204507.pdf'; Target = 'intelligent-algorithms-survival-guide.pdf'; Title = '智能算法与保命指南' }
)

if (-not (Test-Path -LiteralPath $SourceDirectory -PathType Container)) {
  throw "资料源目录不存在：$SourceDirectory"
}

New-Item -ItemType Directory -Path $targetDirectory -Force | Out-Null

$manifest = foreach ($resource in $resources) {
  $sourcePath = Join-Path $SourceDirectory $resource.Source
  $targetPath = Join-Path $targetDirectory $resource.Target
  if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
    throw "缺少课程资料：$($resource.Source)"
  }

  $sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
  $copyRequired = -not (Test-Path -LiteralPath $targetPath -PathType Leaf)
  if (-not $copyRequired) {
    $targetHash = (Get-FileHash -LiteralPath $targetPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $copyRequired = $targetHash -ne $sourceHash
  }
  if ($copyRequired) {
    Copy-Item -LiteralPath $sourcePath -Destination $targetPath -Force
  }

  $file = Get-Item -LiteralPath $targetPath
  [ordered]@{
    order = $resource.Order
    title = $resource.Title
    original_file = $resource.Source
    file = $resource.Target
    bytes = $file.Length
    sha256 = $sourceHash
  }
}

$manifestPath = Join-Path $targetDirectory 'resources.json'
$manifestJson = $manifest | ConvertTo-Json -Depth 4
[System.IO.File]::WriteAllText($manifestPath, $manifestJson, [System.Text.UTF8Encoding]::new($false))

Write-Host "Synced $($resources.Count) learning resources to $targetDirectory"
