FROM apache/airflow:2.7.2-python3.9

RUN pip install --no-cache-dir --timeout 300 psycopg2-binary apache-airflow-providers-cncf-kubernetes apache-airflow-providers-docker

ENV AIRFLOW_HOME=/opt/airflow

COPY ./app/dags /opt/airflow/dags

USER root
COPY airflow-init.sh /usr/local/bin/airflow-init.sh
RUN chmod +x /usr/local/bin/airflow-init.sh

USER airflow

ENTRYPOINT ["/usr/local/bin/airflow-init.sh"]

EXPOSE 8080