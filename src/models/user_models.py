from src.models.sqlite import BaseModels


class UsersModels(BaseModels):
    def select(self):
        query = "SELECT * FROM users"

        return self._execute_query(query, select=True)

    def insert(self, params) -> bool:
        query = """
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
            """

        return self._execute_query(query, params)

    def update(self, params):
        query = """
            UPDATE users (username, password_hash, role)
            SET (?, ?, ?)
            WHERE id = ?
        """

        self._execute_query(query, params)

    def delete(self, params):
        query = """
            DELETE FROM users
            WHERE id = ?
        """

        self._execute_query(query, params)
    
    # filters
    def select_by_email(self, email):
        query = """
            SELECT * FROM users
            WHERE email = ?
        """

        return self._execute_query(query, (email,), select=True, fetch=1)
