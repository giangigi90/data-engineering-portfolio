# Data Engineering Portfolio — Windows Lite (no WSL, no Docker)

Questo setup usa solo Windows nativo:
- Python 3.11 (venv)
- Apache Airflow (installato via `pip`)
- Postgres **installato su Windows** (via installer, p.es. 15+)
- MinIO **opzionale** (scarica `minio.exe` e mettilo in `tools/minio/`)

> Nota: Airflow su Windows non è ufficialmente supportato come su Linux/WSL. Per uno studio personale funziona bene se segui questi script PowerShell.

## Requisiti
1. **Python 3.11**: https://www.python.org/downloads/
   - Durante l'installazione spunta **"Add Python to PATH"**
2. **Git**: https://git-scm.com/download/win
3. **VS Code**: https://code.visualstudio.com/
4. **Postgres per Windows**: https://www.postgresql.org/download/windows/
   - Crea un DB chiamato `warehouse` e un utente `warehouse/warehouse`
   - Porta: `5432` (default)

## Setup ambiente Python
Apri **PowerShell** nella root del repo e lancia:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Configura variabili ambiente (crea `.env`)
Copia `.env.example` → `.env` e, se serve, modifica valori.

## Inizializza Airflow
```powershell
# attiva venv prima
.\.venv\Scripts\Activate.ps1
# crea DB sqlite di Airflow nella cartella .airflow
$env:AIRFLOW_HOME = (Resolve-Path ".\.airflow").Path
airflow db init
# crea utente admin
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

## Avvia Airflow (due terminali)
**Terminal 1 (Webserver):**
```powershell
.\.venv\Scripts\Activate.ps1
$env:AIRFLOW_HOME = (Resolve-Path ".\.airflow").Path
airflow webserver --port 8080
```

**Terminal 2 (Scheduler):**
```powershell
.\.venv\Scripts\Activate.ps1
$env:AIRFLOW_HOME = (Resolve-Path ".\.airflow").Path
airflow scheduler
```

Apri http://localhost:8080 (admin/admin).

## Connessione a Postgres (Warehouse)
Airflow userà la variabile `AIRFLOW_CONN_WAREHOUSE_POSTGRES` definita in `.env`.  
Verifica che Postgres sia su `localhost:5432` con DB `warehouse` e user/pass `warehouse`.

Per creare la connessione dentro Airflow via CLI:
```powershell
.\.venv\Scripts\Activate.ps1
$env:AIRFLOW_HOME = (Resolve-Path ".\.airflow").Path
$env:$(Get-Content .env | Where-Object {$_ -match "^AIRFLOW_CONN_WAREHOUSE_POSTGRES"}) | Out-Null
airflow connections add "warehouse_postgres" --conn-uri $env:AIRFLOW_CONN_WAREHOUSE_POSTGRES
```

## MinIO (opzionale, S3-like)
1. Scarica `minio.exe` da https://min.io/download (Windows).
2. Metti il file in `tools/minio/minio.exe`.
3. Avvio:
```powershell
.\.venv\Scripts\Activate.ps1
./tools/minio/start-minio.ps1
```
- Console: http://localhost:9001 (user/pass in `.env`)
- S3 endpoint: http://localhost:9000

## Esegui DAG di esempio
Nel pannello Airflow attiva `ingest_example` e fai un run.  
Il DAG crea una tabella semplice `facts_calls` sul DB `warehouse` e inserisce una riga demo.

## dbt (facoltativo in Week 0)
1. Copia `dbt/profiles-template.yml` in `~\AppData\Roaming\dbt\profiles.yml`
2. Installa `dbt-postgres` (già in `requirements.txt`)
3. Comando test:
```powershell
.\.venv\Scripts\Activate.ps1
cd dbt
dbt debug
```

## Streaming demo (senza Kafka)
In una finestra:
```powershell
.\.venv\Scripts\Activate.ps1
python .\streaming\producer.py | python .\streaming\consumer.py
```
Questo scriverà file Parquet in `streaming\out\` ogni ~60s.

---

### Troubleshooting rapido
- Se il webserver Airflow non parte, assicurati che la porta 8080 sia libera.
- Se la connessione Postgres fallisce, prova con un client (p.es. DBeaver) per verificare credenziali/porta.
- Su Airflow Windows, evita percorsi troppo lunghi o con spazi.

Buon lavoro! 🚀
