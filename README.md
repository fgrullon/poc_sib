# Prueba de Capacidades en Gestión y Gobierno de Datos - POC

Este repositorio contiene la Prueba de Concepto (POC) para la plataforma de analítica de datos, desarrollada como parte del Ejercicio #4 de la evaluación.

## Arquitectura

La solución está construida con microservicios en contenedores Docker, orquestados por Docker Compose. Utiliza PostgreSQL como el motor de base de datos centralizado para todas las capas de datos (staging, curado, OLAP) y para los metadatos de los servicios.

**Servicios:**

- **Ingestion Service:** Responsable de extraer datos de la API de Alpha Vantage.
- **Orchestration Service (Apache Airflow):** Gestiona y programa los flujos de trabajo de datos.
- **PostgreSQL DB:** Almacena todos los datos (crudos, validados, transformados) y metadatos.
- **Data Quality Service:** Realiza validaciones sobre los datos extraídos.
- **Transformation Service (DBT):** Transforma y agrega los datos para el consumo analítico.
- **Reporting Service (Apache Superset):** Provee visualizaciones dinámicas de los datos.
- **Catalog Service (OpenMetadata/DataHub):** Cataloga los activos de información.

## Cómo Ejecutar la Plataforma (POC)

**Requisitos Previos:**

- Docker y Docker Compose instalados.
- Una clave API de Alpha Vantage (se configurará en el archivo `.env`).

**Pasos:**

1.  **Clonar el Repositorio:**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd project_root
    ```

2.  **Configurar Variables de Entorno:**
    Copia el archivo `.env.example` (si existe) a `.env` y edita las variables necesarias, especialmente la clave API de Alpha Vantage y las credenciales de PostgreSQL.

    ```bash
    cp .env.example .env
    # Abre .env y añade/modifica:
    # ALPHA_VANTAGE_API_KEY=TU_API_KEY
    # POSTGRES_USER=your_user
    # POSTGRES_PASSWORD=your_password
    # POSTGRES_DB=your_database
    ```

3.  **Construir y Levantar los Servicios Docker:**

    ```bash
    docker-compose build
    docker-compose up -d
    ```

    Esto construirá las imágenes de Docker y levantará todos los servicios en segundo plano.

4.  **Acceder a los Servicios:**

    - **Apache Airflow UI:** `http://localhost:8080` (usar `airflow` / `airflow` como usuario/contraseña por defecto).
    - **Apache Superset UI:** `http://localhost:8088` (consultar los logs para el usuario/contraseña inicial de Superset).
    - **OpenMetadata/DataHub UI:** (Si se implementa) `http://localhost:<PUERTO_DEL_CATALOGO>`

5.  **Ejecutar el Pipeline de Datos:**

    - En la UI de Airflow, habilita y activa el DAG `alpha_vantage_dag.py`. Este DAG orquestará la extracción, validación y transformación de los datos.

6.  **Explorar Datos y Visualizaciones:**
    - Una vez que el DAG haya completado su ejecución, accede a Superset para explorar las visualizaciones de los datos transformados.
    - Puedes conectarte a la base de datos PostgreSQL (host: `postgres_db`, puerto: `5432`) desde un cliente SQL para inspeccionar las tablas en los diferentes esquemas (`raw`, `validated`, `curated`, `olap`).

## Contacto

Para cualquier consulta o retroalimentación, contactar a [Tu Nombre/Correo].
