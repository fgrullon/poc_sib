import psycopg2
import pandas as pd

class DataLoader:
    """
    Clase para cargar datos a PostgreSQL.
    """
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def _get_connection(self):
        """Establece y devuelve una conexión a la base de datos."""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def load_company_overview(self, data: dict):
        """Carga datos de Company Overview a la tabla de staging."""
        if not data:
            print("Datos de Company Overview vacíos, no se cargará.")
            return

        df = pd.DataFrame([data])
                
        new_columns = []
        for col in df.columns:
            sanitized_col = col.replace(' ', '_').replace('.', '').lower()
            if sanitized_col and sanitized_col[0].isdigit():
                sanitized_col = '_' + sanitized_col
            new_columns.append(sanitized_col)
        df.columns = new_columns
        
        df = df.replace(['None', '-'], pd.NA)

        numeric_cols_company_overview = [
            'marketcapitalization', 'ebitda', 'peratio', 'pegratio', 'bookvalue',
            'dividendpershare', 'dividendyield', 'eps', 'revenuepersharettm',
            'profitmargin', 'operatingmarginttm', 'returnonassetsttm',
            'returnonequityttm', 'revenuettm', 'grossprofitttm', 'dilutedepsttm',
            'quarterlyearningsgrowthyoy', 'quarterlyrevenuegrowthyoy',
            'analysttargetprice', 'trailingpe', 'forwardpe',
            'pricetosalesratiottm', 'pricetobookratio', 'evtorevenue',
            'evtoebitda', 'analystratingstrongbuy', 'analystratingbuy',
            'analystratinghold', 'analystratingsell', 'analystratingstrongsell',
            'beta', '_52weekhigh', '_52weeklow', '_50daymovingaverage',
            '_200daymovingaverage', 'sharesoutstanding'
        ]

        for col in numeric_cols_company_overview:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            columns = ', '.join(df.columns)
            values_placeholder = ', '.join(['%s'] * len(df.columns))
            insert_statement = f"INSERT INTO raw_data.company_overview ({columns}) VALUES ({values_placeholder})"

            symbol_val = data.get('Symbol', 'N/A')
            for index, row in df.iterrows():
                try:
                    cursor.execute(insert_statement, row.values.tolist())
                except Exception as e:
                    print(f"Error al insertar fila para {symbol_val}: {e}")
                    conn.rollback()
                    continue

            conn.commit()
            print(f"Datos de Company Overview cargados exitosamente para {symbol_val}.")

        except Exception as e:
            print(f"Error general en la carga de Company Overview: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                cursor.close()
                conn.close()

    def load_income_statement(self, data: dict):
        """Carga datos de Income Statement a la tabla de staging."""
        if not data or not data.get('quarterlyReports'):
            print("Datos de Income Statement vacíos o incompletos, no se cargará.")
            return

        reports = data.get('quarterlyReports', [])
        symbol = data.get('symbol')

        if not reports:
            print("No hay informes trimestrales o anuales para Income Statement.")
            return

        for report in reports:
            report['symbol'] = symbol
            
        df = pd.DataFrame(reports)
        
        symbol = data.get("symbol", "UNKNOWN")
        df['symbol'] = symbol # Add symbol as a new column (by default, it will be at the end)


        desired_db_columns_order = [
            'symbol', 'fiscaldateending', 'reportedcurrency', 'grossProfit',
            'totalRevenue', 'costOfRevenue', 'costofGoodsAndServicesSold',
            'operatingIncome', 'sellingGeneralAndAdministrative', 'researchAndDevelopment',
            'operatingExpenses', 'investmentIncomeNet', 'netInterestIncome',
            'otherNonOperatingIncome', 'incomeBeforeTax', 'incomeTaxExpense',
            'interestAndDebtExpense', 'netIncomeFromContinuingOperations',
            'comprehensiveIncomeNetOfTax', 'ebit', 'ebitda', 'netIncome',
            'nontaxableInterestIncome', 'interestIncome', 'interestExpense',
            'nonInterestIncome', 'depreciation', 'depreciationAndAmortization'
        ]
        
        sanitized_df_columns = []
        for col in df.columns:
            sanitized_col_name = col.replace(' ', '_').replace('.', '').lower()
            if sanitized_col_name and sanitized_col_name[0].isdigit():
                sanitized_col_name = '_' + sanitized_col_name
            sanitized_df_columns.append(sanitized_col_name)
        df.columns = sanitized_df_columns
        print(f"DEBUG: DataFrame columns AFTER sanitization: {df.columns.tolist()}")

        df = df.reindex(columns=desired_db_columns_order)

        df = df.replace(['None', '-'], pd.NA)
        
        numeric_cols_income_statement = [
            'grossprofit', 'totalrevenue', 'costofrevenue', 'costofgoodsandservicessold',
            'operatingincome', 'sellinggeneralandadministrative', 'researchanddevelopment',
            'operatingexpenses', 'investmentincomenet', 'netinterestincome',
            'othernonoperatingincome', 'incomebeforetax', 'incometaxexpense',
            'interestanddebtexpense', 'netincomefromcontinuingoperations',
            'comprehensiveincomenetoftax', 'ebit', 'ebitda', 'netincome',
            'nontaxableinterestincome', 'interestincome', 'interestexpense',
            'noninterestincome', 'depreciation', 'depreciationandamortization'
        ]

        for col in numeric_cols_income_statement:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            insert_columns = [col for col in df.columns if col != '_load_timestamp']
            
            columns_str = ', '.join(insert_columns)
            values_placeholder = ', '.join(['%s'] * len(insert_columns))
            insert_statement = f"INSERT INTO raw_data.income_statement ({columns_str}) VALUES ({values_placeholder})"

            for index, row in df.iterrows():
                try:
                    row_values = row[insert_columns].tolist()
                    cursor.execute(insert_statement, row_values)
                except Exception as e:
                    print(f"Error al insertar fila para Income Statement ({symbol}, {row.get('fiscaldateending')}): {e}. Row data: {row.values.tolist()}")
                    conn.rollback()
                    continue
            
            conn.commit()
            print(f"Datos de Income Statement cargados exitosamente para {symbol}.")

        except Exception as e:
            print(f"Error general en la carga de Income Statement: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                cursor.close()
                conn.close()

