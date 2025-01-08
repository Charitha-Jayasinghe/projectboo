import pyodbc
import logging
from static.constants import mediumwait
import time

class DatabaseClient:
    def __init__(self):
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"  #change to your odbc driver
            "SERVER=2056.168.212.101;"
            "DATABASE=opera_name_db;"
            "UID=scott;"
            "PWD=yourpw;"
        )
        self.conn = None

    def connect(self):
        if self.conn is None:
            try:
                print("Connecting to database...")
                self.conn = pyodbc.connect(self.connection_string)
                print("Connection successful.")
            except pyodbc.Error as e:
                print(f"Error connecting to the database: {e}")
                self.conn = None

    def get_db_data_as_dict(self, query):
        self.connect()

        try:
            cursor = self.conn.cursor()
            while True:
                time.sleep(mediumwait)
                cursor.execute(query)
                rows = cursor.fetchall()
                row_count = len(rows)

                if row_count <= 1:
                    logging.info(f"Data fetched successfully")
                    column_names = [column[0] for column in cursor.description]     
                    break
                else:
                    return "No data found"

            return [dict(zip(column_names, row)) for row in rows]
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")
            return []
        
        
    def execute_query(self, query):
        self.connect()

        try:
            cursor = self.conn.cursor()   
            while True:
                time.sleep(mediumwait)
                cursor.execute(query)

                if cursor.rowcount > 0:
                    
                    break
                else:
                    return "No data found"    
            
            self.conn.commit()
         

            
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
