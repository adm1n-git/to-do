# import Python in-built modules

import sqlite3

class sqlite_database:

    def __init__(self, path: str):
        
        self.path = path
        # initialize an SQLite connection and cursor to interact with the database

        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def exec_query(self, query: str, parameters: dict = {}):

        self.query = query.strip()

        if (
            self.query.startswith("SELECT")
        ):
            with self.connection:
                self.cursor.execute(query, parameters)

            # return all records matched with the SQL query

            return [dict(record) for record in self.cursor.fetchall()]

        else:
            with self.connection:
                self.cursor.execute(query, parameters)

            return None

    def close(self):
        # close an SQLite connection gracefully

        self.connection.close()
