from datetime import datetime
from airflow import DAG
from docker.types import Mount

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator

CONN_ID = 'your_string_here'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'elt_with_dbt',
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2024, 4, 11),
    catchup=False,
)

task1 = AirbyteTriggerSyncOperator(
    task_id='airbyte_postgres_postgres',
    airbyte_conn_id='airbyte',
    connection_id=CONN_ID,
    asynchronous=False,
    timeout=3600,
    wait_seconds=3,
    dag=dag
)

task2 = DockerOperator(
    task_id = 'dbt_run',
    image = 'ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command = [
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt",
        "--full-refresh"
    ],
    auto_remove = True,
    docker_url = "unix://var/run/docker.sock",
    network_mode = "bridge",
    monts = [
        Mount(source = '/home/majdi/Desktop/ELT_pipeline/elt_dbt', target = '/dbt', type = 'bind'),
        Mount(source = '/home/majdi/.dbt', target = '/root', type = 'bind'),
    ],
    dag = dag
)

task1 >> task2