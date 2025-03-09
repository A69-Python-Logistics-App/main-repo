import os
import sqlite3 as sql
import traceback as tb

from core.application_data import ApplicationData

#import pandas as pd

app_data = ApplicationData()

class State:
    
    DB_NAME = "state.db"
    
    def __init__(self, app_data, debug: bool = False):
        self._conn, self._c = self.connect(debug)
        self._conn.row_factory = sql.Row
        self._app_data = app_data

    def dump_to_app(self):
        self._execute("INSERT INTO employees ('username', 'password', 'role') VALUES (:username, :password, :role)",
                      {"username": "test", "password": "testing", "role": "admin"})
        self._execute("INSERT INTO employees ('username', 'password', 'role') VALUES (:username, :password, :role)",
                      {"username": "test1", "password": "testing", "role": "admin"})
        self._execute("INSERT INTO employees ('username', 'password', 'role') VALUES (:username, :password, :role)",
                      {"username": "pesho", "password": "testing", "role": "admin"})

        self._execute("SELECT * FROM employees", {})
        print(self._c.fetchall())

    def dump_to_db(self):
        raise NotImplementedError

    def insert_customer(self, data: dict):
        sample_format = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"] # Unique
        }
        # insert customer in customers

    def insert_package(self, data: dict):
        sample_data = {
            "id": data["id"], # Unique
            "name": data["name"],
            "weight": data["weight"],
            "length": data["length"],
            "width": data["width"],
            "height": data["height"],
            "customer": data["customer"] # Links to customers email
        }
        # insert package in packages
        # insert package in customer_packages

    def insert_employee(self, data: dict):
        sample_format = {
            "username": data["username"], # Unique
            "password": data["password"],
            "role": data["role"]
        }
        # insert into employees

    def insert_route(self, data: dict):
        sample_format = {
            "id": data["id"],
            "takeoff": data["takeoff"], # datetime
            "start": data["start"], # NON NULL
            "stops": data["stops"],
            "destination": data["destination"] # NON NULL
        }
        # insert route in routes

    @classmethod
    def connect(cls, debug: bool = False):
        conn = sql.connect(cls.DB_NAME if not debug else ":memory:")
        c = conn.cursor()
        return conn, c

    def _execute(self, query: str, data: dict) -> bool:
        try:
            self._c.execute(query, data)
            self._conn.commit()
        except Exception as e:
            print(tb.print_tb(e.__traceback__))
            return False
        return True

stt = State(app_data)
stt.dump_to_app()

def reset_database():
    """
    Run this function to reset the database to its original/empty/ state or regenerate it
    :return: None
    """

    try:
        os.remove(State.DB_NAME)
    except FileNotFoundError as e:
        pass # print(tb.print_tb(e.__traceback__))


    with open("sql_init.sql", "r") as f:
        sql_init = f.read()
        conn, c = State.connect(False)
        with conn:
            c.executescript(sql_init)

reset_database()