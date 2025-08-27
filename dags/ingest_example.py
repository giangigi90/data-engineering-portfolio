from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

def load_sample(**context):
    pg = PostgresHook(postgres_conn_id="warehouse_postgres")
    with pg.get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
        create table if not exists public.facts_calls (
            id serial primary key,
            call_id varchar(50),
            operator_id varchar(50),
            duration_seconds int,
            outcome varchar(20),
            ts timestamp default now()
        )
        """)
        cur.execute("insert into public.facts_calls(call_id, operator_id, duration_seconds, outcome) values (%s,%s,%s,%s)",
                    ("c_001","op_01",180,"SUCCESS"))
        conn.commit()

with DAG(
    dag_id="ingest_example",
    start_date=datetime(2024,1,1),
    schedule_interval="@daily",
    catchup=False,
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["demo","ingest"]
) as dag:
    t1 = PythonOperator(
        task_id="load_sample",
        python_callable=load_sample
    )
