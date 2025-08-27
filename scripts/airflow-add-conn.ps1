. .\.venv\Scripts\Activate.ps1
$env:AIRFLOW_HOME = (Resolve-Path ".\.airflow").Path
./scripts/load-dotenv.ps1
if (-not $env:AIRFLOW_CONN_WAREHOUSE_POSTGRES) {
  Write-Host "AIRFLOW_CONN_WAREHOUSE_POSTGRES non impostata. Controlla .env"
  exit 1
}
airflow connections add "warehouse_postgres" --conn-uri $env:AIRFLOW_CONN_WAREHOUSE_POSTGRES
