from src.models.sqlite import BaseModels


class UsersModels(BaseModels):
    def select_all(self):
        query = "SELECT id, username, email, role, create_by FROM users"

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
        query = """
            UPDATE users
            SET username = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    def update_email(self, params):
        query = """
            UPDATE users
            SET email = ?
            WHERE id = ?
        """

        self._execute_query(query, params)
    
    def update_password(self, params):
        query = """
            UPDATE users
            SET password = ?
            WHERE id = ?
        """

        self._execute_query(query, params)
    
    def update_role(self, params):
        query = """
            UPDATE users
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

        return self._execute_query(query, (email,), select=True, single=True)

    def select_by_users(self, id):
        query = """
            SELECT username, email, password_hash FROM users
            WHERE id = ?
        """

        return self._execute_query(query, (id,), select=True, single=True)
    
    def like_by_username(self, username):
        query = """
            SELECT id, username, email FROM users
            WHERE username LIKE ?
        """

        return self._execute_query(query, (f"%{username}%",), select=True)
    
    def like_by_email(self, email):
        query = """
            SELECT id, username, email FROM users
            WHERE email LIKE ?
        """

        return self._execute_query(query, (f"%{email}%",), select=True)
