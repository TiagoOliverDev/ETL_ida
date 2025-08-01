import sys
sys.path.append('/opt/airflow')

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.main import executar_etl_main

default_args = {
    'owner': 'paulo',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def executar_etl_airflow():
    executar_etl_main()

with DAG(
    'ida_etl',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    task_etl = PythonOperator(
        task_id='executar_etl',
        python_callable=executar_etl_airflow
    )
