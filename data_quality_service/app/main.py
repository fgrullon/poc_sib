import os
import great_expectations as gx
from great_expectations.core.batch import BatchRequest
from great_expectations.checkpoint import Checkpoint

# --- Configuration ---
# Get database credentials from environment variables set in docker-compose.yml
# These are the same variables used in great_expectations.yml
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

# Great Expectations project root (where great_expectations/ directory is)
# In Docker, this is /app, so the GE project is at /app/great_expectations
GE_ROOT_DIR = "/app/great_expectations" # Important: This path is inside the container

# Datasource name as defined in great_expectations.yml
DATASOURCE_NAME = "my_postgres_datasource" # Match the name from great_expectations.yml

# Schema and table name of your dbt model
DBT_MODEL_SCHEMA = "analytics_curated_data" # The schema where dbt builds your view
DBT_MODEL_NAME = "stg_alpha_vantage_company_overview" # Your dbt model name

# Expectation Suite name
EXPECTATION_SUITE_NAME = f"{DBT_MODEL_NAME}_suite"

# Checkpoint name
CHECKPOINT_NAME = f"{DBT_MODEL_NAME}_checkpoint"

# --- Main Logic ---

def run_data_quality_checks():
    print(f"--- Starting Data Quality Checks for {DBT_MODEL_NAME} ---")

    # 1. Get the Great Expectations Data Context
    # This loads the configuration from great_expectations/great_expectations.yml
    context = gx.data_context.DataContext(context_root_dir=GE_ROOT_DIR)
    print("Great Expectations Data Context loaded.")

    # 2. Add Datasource if it doesn't exist (optional, but good for robust automation)
    # This step is mostly handled by great_expectations.yml, but this ensures robustness
    # if you were to dynamically create datasources via script.
    # For now, we assume it's correctly in great_expectations.yml
    if DATASOURCE_NAME not in context.list_datasources():
        print(f"Error: Datasource '{DATASOURCE_NAME}' not found in great_expectations.yml. Please ensure it's configured.")
        return

    # 3. Create or load an Expectation Suite
    # For a fresh start, we'll create a simple one if it doesn't exist.
    # In a real scenario, you'd likely create a more robust suite interactively
    # using 'great_expectations suite new --batch-request <batch_request>'
    # and then save it.
    try:
        suite = context.get_expectation_suite(expectation_suite_name=EXPECTATION_SUITE_NAME)
        print(f"Expectation Suite '{EXPECTATION_SUITE_NAME}' loaded.")
    except Exception:
        print(f"Expectation Suite '{EXPECTATION_SUITE_NAME}' not found. Creating a basic one.")
        batch_request = {
            "datasource_name": DATASOURCE_NAME,
            "data_asset_name": DBT_MODEL_NAME, # This should be the table name
            "data_connector_name": "default_runtime_data_connector", # For SimpleSqlalchemyDatasource
            "data_asset_name": f"{DBT_MODEL_SCHEMA}.{DBT_MODEL_NAME}" # Format: schema.table_name for SQL
        }

        # Create a Validator for the new suite
        validator = context.get_validator(
            batch_request=BatchRequest(**batch_request),
            expectation_suite_name=EXPECTATION_SUITE_NAME,
        )

        # Add some simple expectations (you'll add more later)
        print("Adding basic expectations...")
        validator.expect_column_to_exist("symbol")
        validator.expect_column_to_not_be_null("symbol")
        validator.expect_column_values_to_be_of_type("market_capitalization", "FLOAT") # Assuming FLOAT type
        validator.expect_column_values_to_be_of_type("eps", "FLOAT")
        validator.expect_column_values_to_be_of_type("revenue_ttm", "FLOAT")
        validator.expect_column_values_to_be_in_set("currency", ["USD", "EUR", "CAD", "JPY"]) # Example currencies

        validator.save_expectation_suite(discard_failed_expectations=False)
        print(f"Expectation Suite '{EXPECTATION_SUITE_NAME}' created and saved.")
        suite = context.get_expectation_suite(expectation_suite_name=EXPECTATION_SUITE_NAME)


    # 4. Create a Checkpoint to run the validation
    print(f"Creating/loading Checkpoint '{CHECKPOINT_NAME}'...")
    checkpoint_config = {
        "name": CHECKPOINT_NAME,
        "config_version": 1,
        "class_name": "SimpleCheckpoint",
        "runtime_configuration": {},
        "validations": [
            {
                "batch_request": {
                    "datasource_name": DATASOURCE_NAME,
                    "data_connector_name": "default_runtime_data_connector",
                    "data_asset_name": f"{DBT_MODEL_SCHEMA}.{DBT_MODEL_NAME}", # Format: schema.table_name for SQL
                },
                "expectation_suite_name": EXPECTATION_SUITE_NAME,
            },
        ],
    }

    # Ensure the checkpoint exists in the context
    if CHECKPOINT_NAME not in context.list_checkpoints():
        context.add_checkpoint(**checkpoint_config)
        print(f"Checkpoint '{CHECKPOINT_NAME}' added to context.")
    else:
        # If it already exists, update its configuration (important for changes)
        context.update_checkpoint(**checkpoint_config)
        print(f"Checkpoint '{CHECKPOINT_NAME}' updated in context.")


    # 5. Run the Checkpoint
    print(f"Running Checkpoint '{CHECKPOINT_NAME}'...")
    checkpoint_result = context.run_checkpoint(checkpoint_name=CHECKPOINT_NAME)

    if checkpoint_result.success:
        print("Data quality validation SUCCEEDED!")
    else:
        print("Data quality validation FAILED! Review Data Docs for details.")

    # 6. Build and open Data Docs
    print("Building Data Docs...")
    context.build_data_docs()
    print("Data Docs built.")
    print("To view Data Docs, you can open them manually:")
    print(f"Navigate to './data_quality_service/great_expectations/uncommitted/data_docs/local_site/' on your host and open 'index.html'.")
    print("--- Data Quality Checks Finished ---")

if __name__ == "__main__":
    run_data_quality_checks()
