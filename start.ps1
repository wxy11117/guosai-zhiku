param(
  [int]$Port = 4186,
  [switch]$Foreground,
  [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'
$PythonExe = 'C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $PythonExe)) {
  $PythonExe = (Get-Command python -ErrorAction Stop).Source
}

$Url = "http://127.0.0.1:$Port/app.html"
$HealthUrl = "http://127.0.0.1:$Port/api/health"

function Test-ModelScoreService {
  try {
    $health = Invoke-RestMethod -Uri $HealthUrl -TimeoutSec 2
    return $health.status -eq 'ok'
  } catch {
    return $false
  }
}

if (Test-ModelScoreService) {
  Write-Host "模评云服务已在运行：$Url"
  if (-not $NoBrowser) { Start-Process -FilePath $Url }
  return
}

$listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($listener) {
  throw "端口 $Port 已被进程 $($listener.OwningProcess) 占用，但该进程不是可用的模评云服务。"
}

if ($Foreground) {
  if (-not $NoBrowser) { Start-Process -FilePath $Url }
  & $PythonExe "$PSScriptRoot\server.py" --host 127.0.0.1 --port $Port
  return
}

$stdout = Join-Path $PSScriptRoot ".server-$Port.log"
$stderr = Join-Path $PSScriptRoot ".server-$Port.err.log"
$process = Start-Process -FilePath $PythonExe `
  -ArgumentList @('server.py', '--host', '127.0.0.1', '--port', $Port) `
  -WorkingDirectory $PSScriptRoot `
  -WindowStyle Hidden `
  -RedirectStandardOutput $stdout `
  -RedirectStandardError $stderr `
  -PassThru

for ($attempt = 0; $attempt -lt 24; $attempt++) {
  Start-Sleep -Milliseconds 250
  if (Test-ModelScoreService) {
    Write-Host "模评云服务启动成功（PID $($process.Id)）：$Url"
    if (-not $NoBrowser) { Start-Process -FilePath $Url }
    return
  }
  if ($process.HasExited) { break }
}

throw "服务启动失败，请查看 $stderr"
