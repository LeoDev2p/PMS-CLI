import sqlite3

from src.core.exceptions import handle_sqlite_error
from src.core.logging import get_logger
from src.core.setting import DB_PATH


class BaseModels:
    """
    Base class for database management.
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.log_error = get_logger("error", self.__class__.__name__)

        # noqa: E402
        from .create_tables import CreateTables
        if not isinstance(self, CreateTables):
            self.create_tables = CreateTables()
            self.create_tables.create_all_tables()

    def _execute_query(self, query, params: tuple = (), select=False, single=False, is_many=False):
        """
        Execute a query.

        Args:
            query (str): The query to execute.
            params (tuple): The parameters to use in the query.
            select (bool): Whether to select data from the query.
            single (bool): when fetchone
            is_many (bool): when multiple data points are to be recorded executemany

        Returns:
            tuple: The data from the query
            list[tuple]: The data from the query.
        """
        try:
            with sqlite3.connect(self.db_path) as con:
                con.execute("PRAGMA foreign_keys = ON;")

                cursor = con.cursor()

                if is_many:
                    cursor.executemany(query, params)
                else:
                    cursor.execute(query, params)

                if select:
                    return cursor.fetchone() if single else cursor.fetchall()

                con.commit()
            return True

        except sqlite3.Error as e:
            handle_sqlite_error(e, sqlite3)
