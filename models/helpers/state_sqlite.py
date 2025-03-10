import json
import os
import sqlite3 as sql
import traceback as tb
import prettyprinter as pt

from core.application_data import ApplicationData

#import pandas as pd
#import numpy as np

class State:
    
    DB_NAME = "state.db"
    
    def __init__(self, app_data, debug: bool = False):
        self._conn, self._c = self.connect(debug)
        self._app_data = app_data

    @property
    def app_data(self):
        return self._app_data

    @property
    def conn(self):
        return self._conn

    @property
    def c(self):
        return self._c

    def dump_to_app(self):
        # Username must be unique
        self.insert_employee({"username": "pesho", "password": "testing", "role": "admin"})
        self.insert_employee({"username": "pesho1", "password": "testing", "role": "supervisor"})
        self.insert_employee({"username": "pesho2", "password": "testing", "role": "manager"})
        self.insert_employee({"username": "pesho3", "password": "testing", "role": "user"})

        self._execute("SELECT * FROM employees", {})
        result = [dict(row) for row in self.c.fetchall()]
        pt.pprint(result)

        # Email must be unique, ID is auto-increment integer and also unique - not mentioned in the query
        self.insert_customer({"first_name": "Pesho", "last_name": "Georgiev", "email": "pesho.g@gmail.com"})
        self.insert_customer({"first_name": "Pesho1", "last_name": "Georgiev", "email": "pesho1.g@gmail.com"})
        self.insert_customer({"first_name": "Pesho2", "last_name": "Georgiev", "email": "pesho2.g@gmail.com"})
        self.insert_customer({"first_name": "Pesho3", "last_name": "Georgiev", "email": "pesho3.g@gmail.com"})
        self.remove_customer({"email": "pesho1.g@gmail.com"})
        self._execute("SELECT * FROM customers", {})
        result = [dict(row) for row in self.c.fetchall()]
        pt.pprint(result)


        #pt.pprint(self.get_routes())
        self.insert_route\
            ({"takeoff":"Mar 01 2025 08:00", "start": "Sofia", "stops": ["Plovdiv", "Stara Zagora"], "destination": "Burgas"})
        self.insert_route\
            ({"takeoff":"Mar 03 2025 08:00", "start": "Plovidv", "stops": ["Stara Zagora"], "destination": "Burgas"})
        self.insert_route\
            ({"takeoff":"Mar 05 2025 08:00", "start": "Burgas", "stops": ["Stara Zagora", "Plovdiv"], "destination": "Sofia"})
        pt.pprint(self.get_routes())

    def dump_to_db(self):
        raise NotImplementedError

    def insert_customer(self, data: dict):
        # sample_format = {
        #     "first_name": data["first_name"],
        #     "last_name": data["last_name"],
        #     "email": data["email"] # Unique
        # }
        query = "INSERT INTO customers ('first_name', 'last_name', 'email') VALUES (:first_name, :last_name, :email)"
        if self._execute(query, data):
            self._log(f"Inserted customer: {data['first_name']} {data['last_name']}")
        else:
            raise ValueError(f"Failed to insert customer: {data['first_name']} {data['last_name']}")

    def insert_package(self, data: dict):
        sample_format = {
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
        pass

    def insert_employee(self, data: dict):
        # sample_format = {
        #     "username": data["username"], # Unique
        #     "password": data["password"],
        #     "role": data["role"]
        # }
        # insert into employees
        query = "INSERT INTO employees ('username', 'password', 'role') VALUES (:username, :password, :role)"
        if self._execute(query, data):
            self._log(f"Inserted employee: {data['username']}")
        else:
            raise ValueError(f"Failed to insert employee: {data['username']}")

    def insert_route(self, data: dict):
        # sample_format = {
        #     "takeoff": data["takeoff"], # datetime
        #     "start": data["start"], # NON NULL
        #     "stops": data["stops"],
        #     "destination": data["destination"] # NON NULL
        # }
        query = "INSERT INTO routes ('takeoff', 'start', 'stops', 'destination') VALUES (:takeoff, :start, :stops, :destination)"
        data["stops"] = json.dumps(data["stops"])
        if self._execute(query, data):
            self._log(f"Inserted route from {data['start']} to {data['destination']} taking off at {data['takeoff']}")
        else:
            raise ValueError(f"Failed to insert route from {data['start']} to {data['destination']} taking off at {data['takeoff']}")

    def get_routes(self):
        tc = self.conn.cursor()
        tc.execute("SELECT * FROM routes")
        routes = [dict(row) for row in tc.fetchall()]
        for route in routes:
            route["stops"] = json.loads(route["stops"])
        return routes

    def remove_customer(self, data: dict):
        # sample_format = {
        #     "email": data["email"]
        # }
        # TODO: remove customer from customer_packages
        tc = self.conn.cursor()
        tc.execute("DELETE FROM customers WHERE email = :email", data)
        return tc.rowcount

    @classmethod
    def connect(cls, debug: bool = False) -> (sql.Connection, sql.Cursor):
        conn = sql.connect(cls.DB_NAME if not debug else ":memory:")
        conn.row_factory = sql.Row # Must setup conn.row_factory before cursor
        c = conn.cursor()
        return conn, c

    def _execute(self, query: str, data: dict) -> bool:
        try:
            self.c.execute(query, data)
            self.conn.commit()
            self._log(f"Executed query: {query}") # this has to be before request queries because it overrides the result
        except sql.OperationalError:
            return False
        except Exception as e:
            pt.pprint(tb.print_tb(e.__traceback__))
            return False
        return True

    def _log(self, log_entry: str):
        self.conn.cursor().\
            execute("INSERT INTO system_log (log_entry) VALUES (:log_entry)", {"log_entry": log_entry})

    def _get_all(self, table_name: str):
        query = f"SELECT * FROM {table_name}"
        self._execute(query, {})
        result = [dict(row) for row in self.c.fetchall()]
        return result


def reset_database():
    """
    Run this function to reset the database to its original/empty/ state or regenerate it
    :return: None
    """

    try:
        os.remove(State.DB_NAME)
    except FileNotFoundError as e:
        pass # pt.pprint(tb.print_tb(e.__traceback__))


    with open("sql_init.sql", "r") as f:
        sql_init = f.read()
        conn, c = State.connect(False)
        with conn:
            c.executescript(sql_init)

if __name__ == "__main__":
    reset_database()
    stt = State(ApplicationData())
    stt.dump_to_app()

    # Currently prints 4 test employees, 3 test customers and 3 test routes