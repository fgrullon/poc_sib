from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

with DAG(
    dag_id='alpha_vantage_data_pipeline',
    default_args=default_args,
    description='DAG para la ingesta, calidad y transformación de datos de Alpha Vantage.',
    schedule_interval=None,
    catchup=False,
    tags=['data_governance', 'alpha_vantage', 'financial'],
) as dag:
    ingest_data_task = DockerOperator(
        task_id='ingest_alpha_vantage_data',
        image='ingestion_service:latest',
        command='python main.py',
        network_mode='project_root_default',
        environment={
            'ALPHA_VANTAGE_API_KEY': "{{ dag_run.conf.get('alpha_vantage_api_key', 'YOUR_DEFAULT_API_KEY') }}",
            'POSTGRES_HOST': 'postgres_db',
            'POSTGRES_USER': '{{ var.value.get("postgres_user", "myuser") }}',
            'POSTGRES_PASSWORD': '{{ var.value.get("postgres_password", "mypassword") }}',
            'POSTGRES_DB': '{{ var.value.get("postgres_db", "datagovernance_db") }}'
        },
    )

    data_quality_task = DockerOperator(
        task_id='run_data_quality_checks',
        image='data_quality_service:latest',
        command='python main.py --action run_checks',
        network_mode='project_root_default',
        environment={
            'POSTGRES_HOST': 'postgres_db',
            'POSTGRES_USER': '{{ var.value.get("postgres_user", "myuser") }}',
            'POSTGRES_PASSWORD': '{{ var.value.get("postgres_password", "mypassword") }}',
            'POSTGRES_DB': '{{ var.value.get("postgres_db", "datagovernance_db") }}'
        },
        depends_on_past=False,
    )

    run_dbt_models_task = DockerOperator(
        task_id='run_dbt_transformation',
        image='transformation_service:latest',
        command='dbt run --project-dir /app/dbt_project',
        network_mode='project_root_default',
        environment={
            'POSTGRES_HOST': 'postgres_db',
            'POSTGRES_USER': '{{ var.value.get("postgres_user", "myuser") }}',
            'POSTGRES_PASSWORD': '{{ var.value.get("postgres_password", "mypassword") }}',
            'POSTGRES_DB': '{{ var.value.get("postgres_db", "datagovernance_db") }}'
        },
    )


    ingest_data_task >> data_quality_task >> run_dbt_models_task
