import mysql.connector
from datetime import date
import pytest
from main import pridat_ukol

def connect_test_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="ta_project2_test_db"
    )

def test_pridat_ukol_positive(monkeypatch):
    conn = connect_test_db()
    cursor = conn.cursor(buffered=True)


    inputs = iter(["Test úkol", "Popis úkolu"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    pridat_ukol(conn)

    cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Test úkol",))
    result = cursor.fetchone()
    assert result is not None

    cursor.execute("DELETE FROM ukoly WHERE nazev = %s", ("Test úkol",))
    conn.commit()
    conn.close()
    
def test_pridat_ukol_negative(monkeypatch):
    conn = connect_test_db()
    cursor = conn.cursor(buffered=True)

    monkeypatch.setattr("builtins.input", lambda _: "q")

    pridat_ukol(conn)

    cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Test úkol",))
    result = cursor.fetchone()
    assert result is None

    cursor.close()
    conn.close()

