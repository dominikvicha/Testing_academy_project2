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

