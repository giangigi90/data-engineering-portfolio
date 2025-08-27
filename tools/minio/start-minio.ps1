. .\.venv\Scripts\Activate.ps1
./scripts/load-dotenv.ps1
$minioExe = Join-Path (Resolve-Path ".\tools\minio").Path "minio.exe"
if (!(Test-Path $minioExe)) {
  Write-Host "minio.exe non trovato. Mettilo in tools\minio\minio.exe"
  exit 1
}
& $minioExe server .\tools\minio\data --address $env:MINIO_ADDRESS --console-address $env:MINIO_CONSOLE_ADDRESS
