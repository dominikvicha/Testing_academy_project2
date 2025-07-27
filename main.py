import mysql.connector
from mysql.connector import Error

def connection_db():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1111",
            database = "TA_project2"
        )
        print("Připojení bylo úspěšné.")
        return conn
    
    except mysql.connector.Error as  err:
        print(f"Chyba při připojování: {err}")
        return None
    

def vytvoreni_tabulky(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(50),
                popis TEXT,
                stav ENUM('nezahájeno', 'hotovo', 'probíhá'),
                datum_vytvoreni DATE
            )
        ''')
        print("Tabulka byla vytvořena.")

    except Error as err:
        print(f"Tabulka nebyla vytvořena. {err}")




if __name__ == "__main__":
    conn = connection_db()
    if conn:
        vytvoreni_tabulky(conn)
        conn.close()