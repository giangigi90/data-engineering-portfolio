param([string]$envFilePath = ".env")

if (!(Test-Path $envFilePath)) {
  Write-Host "File $envFilePath non trovato. Crea .env partendo da .env.example"
  exit 1
}

Get-Content $envFilePath | ForEach-Object {
  if ($_ -match "^[#\s]") { return }
  $parts = $_.Split("=",2)
  if ($parts.Length -eq 2) {
    [System.Environment]::SetEnvironmentVariable($parts[0], $parts[1])
    Write-Host "Set $($parts[0])"
  }
}
