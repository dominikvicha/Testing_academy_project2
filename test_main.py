import mysql.connector
from datetime import date
import pytest
from main import pridat_ukol
from main import aktualizovat_ukol
from main import odstranit_ukol

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


def test_aktualizovat_ukol_positive(monkeypatch):
    conn = connect_test_db()
    cursor = conn.cursor(buffered=True)

    cursor.execute("""
        INSERT INTO ukoly (nazev, popis, stav, datum_vytvoreni)
        VALUES (%s, %s, %s, CURDATE())
    """, ("Test aktualizace", "Popis", "nezahájeno"))
    conn.commit()
    
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Test aktualizace",))
    task_id = cursor.fetchone()[0]

    inputs = iter([str(task_id), '1'])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    aktualizovat_ukol(conn)

    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (task_id,))
    updated_status = cursor.fetchone()[0]
    assert updated_status == 'probíhá'

    cursor.execute("DELETE FROM ukoly WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()

def test_aktualizovat_ukol_negative(monkeypatch):
    conn = connect_test_db()
    cursor = conn.cursor(buffered=True)

    cursor.execute("""
        INSERT INTO ukoly (nazev, popis, stav, datum_vytvoreni)
        VALUES (%s, %s, %s, CURDATE())
    """, ("Untouched Task", "This should not be changed", "nezahájeno"))
    conn.commit()

    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Untouched Task",))
    untouched_id = cursor.fetchone()[0]

    inputs = iter(["9999", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    aktualizovat_ukol(conn)

    conn = connect_test_db()
    cursor = conn.cursor(buffered=True)

    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (untouched_id,))
    status = cursor.fetchone()[0]
    assert status == "nezahájeno"

    cursor.execute("DELETE FROM ukoly WHERE id = %s", (untouched_id,))
    conn.commit()
    conn.close()


def test_odstranit_ukol_positive(monkeypatch):
    conn = connect_test_db()
    cursor = conn.cursor(buffered=True)

    cursor.execute("""
        INSERT INTO ukoly (nazev, popis, stav, datum_vytvoreni)
        VALUES (%s, %s, %s, CURDATE())
    """, ("ToDelete", "Enter", "nezahájeno"))
    conn.commit()

    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("ToDelete",))
    task_id = cursor.fetchone()[0]
    print(f"testing deletion task_id = {task_id}")

    inputs = iter([str(task_id), 'a', 'q'])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    odstranit_ukol(conn)

    #cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (task_id,))
    result = cursor.fetchone()
    assert result is None, f"Task id {task_id} was not deleted"
    
    conn.close()

def test_odstranit_ukol_negative(monkeypatch):
    conn = connect_test_db()
    cursor = conn.cursor(buffered=True)

    cursor.execute("""
        INSERT INTO ukoly (nazev, popis, stav, datum_vytvoreni)
        VALUES (%s, %s, %s, CURDATE())
    """, ("Untouchable", "This task should survive", "nezahájeno"))
    conn.commit()

    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Untouchable",))
    untouched_id = cursor.fetchone()[0]

    inputs = iter(["9999", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    odstranit_ukol(conn)

    conn = connect_test_db()
    cursor = conn.cursor(buffered=True)

    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (untouched_id,))
    result = cursor.fetchone()
    assert result is not None, f"Task id {untouched_id} should not have been deleted."

    cursor.execute("DELETE FROM ukoly WHERE id = %s", (untouched_id,))
    conn.commit()
    conn.close()
