import os
import sqlite3 as sql
import traceback as tb

#import pandas as pd

class State:
    
    DB_NAME = "state.db"
    
    def __init__(self, app_data, debug: bool = False):
        self._conn, self._c = self.connect(debug)
        self._app_data = app_data

    def dump_to_app(self):
        raise NotImplementedError

    def dump_to_db(self):
        raise NotImplementedError

    @classmethod
    def connect(cls, debug: bool = False):
        conn = sql.connect(cls.DB_NAME if not debug else ":memory:")
        c = conn.cursor()
        return conn, c

    def _execute(self, query: str) -> bool:
        try:
            self._c.execute(query)
            self._conn.commit()
        except Exception as e:
            print(tb.print_tb(e.__traceback__))
            return False
        return True

def reset_database():
    """
    Run this function to reset the database to its original/empty/ state or regenerate it
    :return: None
    """

    try:
        os.remove(State.DB_NAME)
    except FileNotFoundError as e:
        print(tb.print_tb(e.__traceback__))

    with open("sql_init.sql", "r") as f:
        sql_init = f.read()
        con, c = State.connect(False)
        c.executescript(sql_init)
        con.commit()

reset_database()