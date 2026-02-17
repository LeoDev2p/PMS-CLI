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

    def update_profile(self, params):
        query = """
            UPDATE users
            SET username = ?, password_hash = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    def update_username(self, params):
        query = """UPDATE users
            SET username = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    def update_email(self, params):
        query = """UPDATE users
            SET email = ?
            WHERE id = ?
        """

        self._execute_query(query, params)
    
    def update_password(self, params):
        query = """UPDATE users
            SET password = ?
            WHERE id = ?
        """

        self._execute_query(query, params)
    
    def update_role(self, params):
        query = """UPDATE users
            SET role = ?
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

    def select_by_users(self, id):
        query = """
            SELECT username, email, password_hash FROM users
            WHERE id = ?
        """

        return self._execute_query(query, (id,), select=True, fetch=1)
