import mysql.connector
from mysql.connector import Error

def connection_db():
    try:
        conn = mysql.connectorconnector.connect(
            host = "localhost",
            user = "root",
            password = "1111",
            database = "Testing_academy_projekt2"
        )

        print("Připojení bylo úspěšné.")
        return conn
    
    except mysql.connector.Error as  err:
        print(f"Chyba při připojování: {err}")
        return None