from src.models.sqlite import BaseModels


class UsersModels(BaseModels):
    @staticmethod
    def select():
        query = "SELECT * FROM users"

        return BaseModels._execute_query(query)

    @staticmethod
    def insert(params):
        query = """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """

        BaseModels._execute_query(query, params)

    @staticmethod
    def update(params):
        query = """
            UPDATE users (username, password_hash, role)
            SET (?, ?, ?)
            WHERE id = ?
        """

        BaseModels._execute_query(query, params)

    @staticmethod
    def delete(params):
        query = """
            DELETE FROM users
            WHERE id = ?
        """

        BaseModels._execute_query(query, params)
