import os
from api_client import AlphaVantageAPIClient
from data_loader import DataLoader
from config import Config

def run_ingestion():
    """
    Función principal para la ingesta de datos.
    Orquestada por Airflow.
    """
    api_key = Config.ALPHA_VANTAGE_API_KEY
    db_config = {
        "host": Config.POSTGRES_HOST,
        "user": Config.POSTGRES_USER,
        "password": Config.POSTGRES_PASSWORD,
        "database": Config.POSTGRES_DB
    }

    client = AlphaVantageAPIClient(api_key)
    loader = DataLoader(db_config)

    bank_tickers = ["JPM", "BNS"]

    print("Iniciando ingesta de Company Overview...")
    for ticker in bank_tickers:
        overview_data = client.get_company_overview(ticker)
        if overview_data:
            loader.load_company_overview(overview_data)
            print(f"Cargado Company Overview para {ticker}")
        else:
            print(f"No se pudo obtener Company Overview para {ticker}")

    print("Iniciando ingesta de Income Statement...")
    for ticker in bank_tickers:
        income_data = client.get_income_statement(ticker)
        if income_data:
            loader.load_income_statement(income_data)
            print(f"Cargado Income Statement para {ticker}")
        else:
            print(f"No se pudo obtener Income Statement para {ticker}")
    
    print("Ingesta de datos finalizada (parcialmente, resto a implementar).")

if __name__ == "__main__":
    run_ingestion()
