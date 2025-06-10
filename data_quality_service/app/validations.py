import great_expectations as ge
import pandas as pd
import psycopg2
import great_expectations.core.expectation_validation_result as evr
import json

class DataQualityValidator:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def _get_datasource(self, query: str):
        conn = None
        try:
            conn = psycopg2.connect(**self.db_config)
            df = pd.read_sql(query, conn)
            ge_df = ge.from_pandas(df)
            return ge_df
        except Exception as e:
            print(f"Error al obtener datos para validación: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def validate_company_overview(self):
        query = "SELECT * FROM raw_data.company_overview;"
        batch = self._get_datasource(query)
        
        if batch is None:
            print("No se pudo obtener el batch para Company Overview.")
            return

        print("Definiendo expectativas para Company Overview...")
        batch.expect_column_to_exist("symbol")
        batch.expect_column_values_to_be_of_type("symbol", "str")
        batch.expect_column_values_to_not_be_null("symbol")
        batch.expect_column_values_to_be_unique("symbol")
        batch.expect_column_to_exist("marketcapitalization")
        batch.expect_column_values_to_be_between("marketcapitalization", min_value=0, max_value=1_000_000_000_000_000, mostly=0.95)
        batch.expect_column_values_to_be_in_set("currency", ["USD", "EUR", "GBP"], mostly=0.99)

        print("Ejecutando validaciones para Company Overview...")
        results = batch.validate()

        self._record_validation_results(results, "company_overview_suite")
        
        if results.success:
            print("Validaciones de Company Overview pasaron exitosamente.")
        else:
            print(results)

    def validate_income_statement(self):
        query = "SELECT * FROM raw_data.income_statement;"
        batch = self._get_datasource(query)
        
        if batch is None:
            return

        print("Definiendo expectativas para Income Statement...")
        batch.expect_column_to_exist("symbol")
        batch.expect_column_to_exist("fiscaldateending")
        batch.expect_column_values_to_not_be_null("totalrevenue")
        batch.expect_column_values_to_be_between("totalrevenue", min_value=0)

        results = batch.validate()
        self._record_validation_results(results, "income_statement_suite")

        if results.success:
            print("Validaciones de Income Statement pasaron exitosamente.")
        else:
            print("¡Algunas validaciones de Income Statement fallaron!")
            print(results)

    def _record_validation_results(self, ge_results: evr.ExpectationSuiteValidationResult, suite_name: str):
        conn = None
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            results_to_store = ge_results.to_json_dict()

            insert_query = """
            INSERT INTO data_quality.validation_results (batch_id, expectation_suite_name, success, results, meta)
            VALUES (%s, %s, %s, %s, %s);
            """
            
            batch_id = ge_results.meta.get("active_batch_definition", {}).get("batch_identifiers", {}).get("query_string", "unknown_batch")
            
            results_json = json.dumps(ge_results.to_json_dict())
            meta_json = json.dumps(ge_results.meta)
            json_string_results = json.dumps(results_to_store)

            cursor.execute(insert_query, (
                batch_id,
                suite_name,
                ge_results.success,
                json_string_results,
                meta_json
            ))
            conn.commit()
            print(f"Resultados de validación registrados para {suite_name}.")
        except Exception as e:
            print(f"Error al registrar resultados de validación en la base de datos: {e}")
        finally:
            if conn:
                conn.close()
