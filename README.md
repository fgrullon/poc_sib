
# POC para la SB

Este repositorio presenta una Prueba de Concepto (POC) para la plataforma de analítica y reportería de datos de la Superintendencia de Bancos (SB), diseñada para mejorar la calidad y el consumo de la reportería regulatoria.

---

## Estructura y Servicios del Proyecto

La POC se compone de varios servicios Docker interconectados:

### 1. `postgres_db`
    *   Almacena todos los datos del pipeline: raw data, datos en área de staging, y las tablas de resumen. Es la unica fuente de informacion para los datos analíticos.

### 2. `airflow` - `webserver` & `scheduler`
    *   Airflow orquesta el flujo de datos completo, desde la ingesta hasta la generación de resúmenes y catalogación. Permite definir la secuencia de ejecución de cada paso (ingesta, staging, validación, transformación, visualización).

### 3. `ingestion_service` (Servicio de Ingesta)
    *   Se encarga de la conexión con la API de Alpha Vantage y la extracción de los sets de datos requeridos (Company Overview, Income Statement, Balance Sheet, Cash Flow). Los datos se colocan inicialmente en el área de staging en `postgres_db`.

### 4. `data_quality_service` (Servicio de Calidad de Datos)
    *   Ejecuta validaciones de calidad de datos utilizando Great Expectations sobre los datos en el área de staging y/o después de las transformaciones, asegurando que los datos cumplen con las características esperadas.

### 5. `transformation_service` (Servicio de Transformación)
    *   Utiliza dbt para generar tablas de resúmenes anuales y otras transformaciones necesarias a partir de los datos en `postgres_db`, aplicando reglas de negocio y optimizando la estructura para el análisis.

### 6. `superset_app` (Servicio de Reportes y Visualización)
    *   Proporciona la interfaz de usuario para la exploración y visualización de datos, conectándose a las tablas de resumen en `postgres_db`. Permite crear visualizaciones dinámicas que proveen información de relevancia para las áreas que explotan la información.
---

## Estrategias 

Se han considerado las siguientes estrategias para garantizar un alto rendimiento, escalabilidad y tolerancia a fallos:

* **Capas (Layers)**:
    * **Capa de Ingesta/Staging**: Los datos crudos se ingieren y se colocan en un área de staging dedicada en `postgres_db` (tablas crudas o temporales), manteniendo la fidelidad del origen.
    * **Capa de Calidad**: Se ejecutan validaciones en la capa de staging para identificar y gestionar discrepancias antes de la transformación.
    * **Capa de Transformación/Modelado**: dbt crea modelos de datos limpios y agregados (como las tablas de resumen anuales) optimizados para el consumo analítico.
* **Splits (División de Responsabilidades)**:
    * Cada servicio está **encapsulado en un contenedor separado** con una responsabilidad única (ingesta, orquestación, calidad, transformación, reporting). Esto facilita el desarrollo, despliegue y escalado independiente de cada componente.
* **Estructuras de Datos**:
    * Se utilizan esquemas de tablas bien definidos en `postgres_db` para cada capa para asegurar la integridad y la eficiencia de las consultas.
    * Las tablas de resumen se diseñan para el consumo utilizando Superset.
* **Rendimiento y Escalabilidad**:
    * Uso de bases de datos relacionales optimizadas (PostgreSQL).
    * Utilización de dbt para transformaciones eficientes y modulares.


---

## Cómo Ejecutar Esta Prueba de Concepto (POC)

### Requisitos Previos

* **Docker Desktop**: Asegúrate de que Docker Desktop esté instalado y en ejecución en tu sistema.
* **Archivo `.env`**: Crea un archivo `.env` en la **raíz de tu directorio de proyecto** con las siguientes variables de entorno. Estas variables son cruciales para la conectividad entre los servicios y la API externa[cite: 53]:
    ```dotenv
    POSTGRES_USER=your_postgres_user
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_DB=your_database_name
    ALPHA_VANTAGE_API_KEY=tu_alpha_vantage_api_key_aqui # Obtener de Alpha Vantage
    SUPERSET_SECRET_KEY=una_clave_secreta_muy_larga_y_unica_que_debes_cambiar
    ```

### Pasos

1.  **Clona el repositorio**:
    ```bash
    git clone <url-de-tu-repositorio-github>
    cd <nombre-de-tu-repositorio>
    ```
3.  **Construye y levanta los servicios Docker**:
    ```bash
    docker-compose up --build -d
    ```
    * Este comando construirá las imágenes Docker para `airflow_webserver`, `airflow_scheduler`, `ingestion_service`, `data_quality_service`, `transformation_service` y `superset_app`, y luego iniciará todos los contenedores en modo `detached` (segundo plano).

4.  **Verifica que los servicios estén en ejecución y saludables**:
    ```bash
    docker-compose ps
    ```
    * Todos los servicios listados deben mostrar un estado `healthy` o `running` una vez que se hayan inicializado correctamente. 

### Acceso a las Interfaces de Usuario

* **Interfaz de Usuario de Apache Airflow**:
    * Abre tu navegador y navega a `http://localhost:8080`.
    * **Primer inicio**: Es probable que necesites crear un usuario administrador en Airflow. Esto se puede hacer ejecutando un comando Docker una vez que el `airflow_webserver` esté en marcha:
        ```bash
        docker-compose exec airflow_webserver airflow users create \
            --username admin --firstname Admin --lastname User --role Admin \
            --email admin@example.com -p your_admin_password
        ```
* **Interfaz de Usuario de Apache Superset**:
    * Abre tu navegador y navega a `http://localhost:8088`.
    * **Primer inicio**: Superset requiere una inicialización. El `entrypoint` del servicio `superset_app` (`/app/docker-init.sh`) está diseñado para manejar esto, que típicamente incluye:
        * Configurar la base de datos de metadatos de Superset.
        * Crear un usuario administrador (si no existe).
        * Cargar conjuntos de datos y dashboards de ejemplo (opcional, pero útil para una POC).
        * Asegúrate de que este script `docker-init.sh` en el directorio `reporting_service` esté correctamente configurado para estos pasos. Por ejemplo:
            ```bash
            #!/bin/bash
            superset db upgrade
            superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin
            superset load_examples
            superset init
            ```
---

## Consideraciones Adicionales y Futuras Extensiones

* **Monitoreo y logging centralizado**: Implementar una solución de logging centralizado y monitoreo de métricas para todos los servicios.
* **Alertas**: Configurar sistemas de alerta para fallos en los DAGs de Airflow o problemas de calidad de datos.
* **CI/CD**: Integrar el pipeline en un flujo de CI/CD para automatizar pruebas y despliegues.

