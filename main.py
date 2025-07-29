import mysql.connector
from mysql.connector import Error
from datetime import date 

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


def hlavni_menu():
    while True:
        zadani = """
        Vítejte v programu Task manager. 
        Task manager - hlavní menu: 
        1. Přidat nový úkol.
        2. Zobraz všechny úkoly. 
        3. Aktualizovat úkol. 
        4. Odstraň úkol. 
        5. Konec programu.
        Vyberte možnost (1-5).
        """

        spravny_vstup = range(1,6)
        volba_uzivatele = input(zadani)

        if volba_uzivatele.isdigit():
            volba_uzivatele = int(volba_uzivatele)

            if volba_uzivatele in spravny_vstup:
                print("Vybrali jste možnost:", volba_uzivatele)
                return volba_uzivatele
            else:
                print("Neplatná volba. Zadejte číslo 1 až 5.")

        else:
            print("Vstup musí být číselný.")


def pridat_ukol():
    while True:
        nazev = input("Zadejte název úkolu (nebo 'q' pro návrat).: ").strip()
        if not nazev:
            print("Název úkolu nesmí být prázdný.")
            continue
        if nazev.lower() == 'q':
            print("Vracím se do hlavního menu.")
            return
        
        popis = input("Zadejte popis úkolu (nebo 'q' pro návrat do návrat).: ").strip()
        if not popis:
            print("Vracím se hlavního menu.")
            return

        print("Vstupy jsou validní. Ukládám úkoly do databáze...")
        break

    stav = 'nezahájeno'
    datum_vytvoreni = date.today()

    conn = connection_db()
    if not conn:
        print("Nepodařilo se připojit k databázi.")
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ukoly (nazev, popis, stav, datum_vytvoreni)
            VALUES (%s, %s, %s, %s)
        ''', (nazev, popis, stav, datum_vytvoreni))
        conn.commit()
        print("Úkol byl úspěšně přidán.")

    except mysql.connector.Error as err:
        print("Chyba při přidávání úkolu:", err)
    finally:
        conn.close()

def zobrazit_ukoly():
    conn = connection_db()
    if not conn:
        print("Nepodařilo se připojit k databázi.")
        return

    cursor = conn.cursor()

    while True:
        zobrazeni_stavu_ukolu = """
        Zobrazení úkolů podle stavu:  
            a) - pro zobrazení všech úkolů,
            b) - pro zobrazení úkolů se stavem 'Nezahájeno',
            c) - pro zobrazení úkolů se stavem 'Probíhá',
            q) - pro návrat do hlavního menu. 
        Vyberte možnost (a, b, c, q):
        """

        filtr_ukolu = input(zobrazeni_stavu_ukolu).strip().lower()

        if filtr_ukolu == 'a':
            cursor.execute("SELECT id, nazev, popis, stav FROM ukoly")

        elif filtr_ukolu == 'b':
            cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav = 'nezahájeno'")

        elif filtr_ukolu == 'c':
            cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav = 'probíhá'")

        elif filtr_ukolu == 'q':
            print("Vracím se do hlavního menu.")
            conn.close()
            return

        else:
            print("Neplatná volba. Zvolte prosím a, b, c nebo q")
            continue

        ukoly = cursor.fetchall()

        if not ukoly:
            print("Seznam úkolů je prázdný.")
        else:
            print("\n--- Seznam úkolů ---")
            for i, ukol in enumerate(ukoly, 1):
                id, nazev, popis, stav = ukol
                print(f"{i} | Název: {nazev} | Popis: {popis} | Stav: {stav}")    


def aktualizovat_ukol():
    conn = connection_db()
    if not conn:
        print("Nepodařilo se připojit k databázi.")
        return
    
    cursor = conn.cursor()

    cursor.execute("SELECT id, nazev, popis, stav FROM ukoly")
    list_ukolu = cursor.fetchall()

    if not list_ukolu:
        print("Seznam úkolů je prázdný")
        conn.close()
        return
    else:
        print("\n--- Seznam úkolů ---")
        for id, nazev, popis, stav in list_ukolu:
            print(f"ID: {id} | Název: {nazev} | Popis: {popis} | Stav: {stav}")

    while True:
        vybrane_id = input("Zadejte ID úkolu, který chcete aktualizovat (nebo 'q' pro návrat:) ").strip()

        if vybrane_id.lower() == 'q':
            print("Vracím se do hlavního menu.")
            conn.close()
            return
        
        if not vybrane_id.isdigit():
            print("Zadejte prosím platné číslo ID.")
            continue

        vybrane_id = int(vybrane_id)

        cursor.execute("SELECT id from ukoly WHERE id = %s", (vybrane_id,))
        vysledek = cursor.fetchone()

        if vysledek is None:
            print("Úkol se zadaným ID neexistuje, zkuste to prosím znovu.")
        else:
            break

    while True:
        moznosti_aktualizace = """
        Vyber nový stav úkolu: 
        1 - aktualizovat úkol na stav 'probíhá',
        2 - aktualizovat úkol na stav 'dokončeno',
        q - pro vrácení se do hlavního menu 
        """
        status_ukolu = input(moznosti_aktualizace).strip()

        if status_ukolu == '1':
            novy_status = 'probíhá'
            break
        elif status_ukolu == '2':
            novy_status = 'dokončeno'
            break
        elif status_ukolu == 'q':
            print("Vracím se do hlavního menu.")
            break
        else:
            print("Neplatná volba. Zadejte prosím 1, 2 nebo q.")

    try:
        cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_status, vybrane_id))

        conn.commit()
        print("Stav úkolu byl aktualizováb.")

    except mysql.connector.Error as err:
        print("Chyba při aktualizaci úkolu: ", err)
    finally:
        conn.close()


def odstranit_ukol():
    conn = connection_db()  #udelat funkci na připojeni do databaze
    if not conn:
        print("Nepodařilo se připojit k databázi.")
        return

    cursor = conn.cursor()

    cursor.execute("SELECT id, nazev, popis, stav FROM ukoly")
    list_ukolu = cursor.fatchall()

    if not list_ukolu:
        print("Seznam úkolů je prázdný.")
        conn.close()
        return
    else:
        print("\n--- Seznam úkolů ---")
        for id, nazev, popis, stav in list_ukolu:
            print(f"ID: {id} | Název: {nazev} | Popis: {popis} | Stav: {stav}")

    
    





def main():

    while True: 
        volba = hlavni_menu()

        if volba == 1:
            pridat_ukol()
        elif volba == 2:
            zobrazit_ukoly()
        elif volba == 3:
            aktualizovat_ukol()    
        #elif volba == 4:
            #odstranit_ukol()
        elif volba == 5:
            print("Ukončuji program.")
            break

if __name__ == "__main__":
    conn = connection_db()
    if conn:
        vytvoreni_tabulky(conn)
        conn.close()
        main()