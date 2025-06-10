import requests
import time
import os
from config import Config

class AlphaVantageAPIClient:
    """
    Cliente para interactuar con la API de Alpha Vantage.
    Implementa manejo de rate limiting.
    """
    BASE_URL = "https://www.alphavantage.co/query"
    CALL_INTERVAL_SECONDS = 15 # Esperar 15 segundos entre llamadas para respetar el límite de 5/min

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._last_call_time = 0

    def _make_request(self, params: dict):
        """Método helper para hacer la solicitud a la API con manejo de rate limiting."""
        current_time = time.time()
        time_since_last_call = current_time - self._last_call_time

        if time_since_last_call < self.CALL_INTERVAL_SECONDS:
            wait_time = self.CALL_INTERVAL_SECONDS - time_since_last_call
            print(f"Esperando {wait_time:.2f} segundos para respetar el límite de la API...")
            time.sleep(wait_time)

        params['apikey'] = self.api_key
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            self._last_call_time = time.time()
            
            if "Error Message" in data:
                print(f"Alpha Vantage API Error: {data['Error Message']}")
                return None
            if "Information" in data:
                print(f"Alpha Vantage API Information (mensaje de límite de tasa o similar): {data['Information']}")
                return None
            
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con Alpha Vantage: {e}")
            return None

    def get_company_overview(self, symbol: str):
        params = {
            "function": "OVERVIEW",
            "symbol": symbol
        }
        return self._make_request(params)

    def get_income_statement(self, symbol: str):
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": symbol
        }
        return self._make_request(params)

    def get_balance_sheet(self, symbol: str):
        params = {
            "function": "BALANCE_SHEET",
            "symbol": symbol
        }
        return self._make_request(params)

    def get_cash_flow(self, symbol: str):
        params = {
            "function": "CASH_FLOW",
            "symbol": symbol
        }
        return self._make_request(params)

