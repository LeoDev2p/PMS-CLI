from src.models.sqlite import BaseModels


class UsersModels(BaseModels):
    """
    Handles user models.
    """

    def select_all(self):
        """
        Selects all users.

        Returns:
            list[tuple]: List of id, username, email, role and create_by.
        """
        query = "SELECT id, username, email, role, create_by FROM users"

        return self._execute_query(query, select=True)

    def insert(self, params) -> bool:
        """
        Inserts a new user.

        Returns:
            bool: True if the user was inserted successfully.
        """
        query = """
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
            """

        return self._execute_query(query, params)

    def update_profile(self, params):
        """
        Updates the profile of a user.
        """
        query = """
            UPDATE users
            SET username = ?, password_hash = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    def update_username(self, params):
        """
        Updates the username of a user.
        """
        query = """
            UPDATE users
            SET username = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    def update_email(self, params):
        """
        Updates the email of a user.
        """
        query = """
            UPDATE users
            SET email = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    def update_password(self, params):
        """
        Updates the password of a user.
        """
        query = """
            UPDATE users
            SET password = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    def update_role(self, params):
        """
        Updates the role of a user.
        """
        query = """
            UPDATE users
            SET role = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    def delete(self, params):
        """
        Deletes a user.
        """
        query = """
            DELETE FROM users
            WHERE id = ?
        """

        self._execute_query(query, params)

    # filters
    def select_by_email(self, email):
        """
        Selects a user by email.

        Returns:
            tuple: User data.
        """
        query = """
            SELECT * FROM users
            WHERE email = ?
        """

        return self._execute_query(query, (email,), select=True, single=True)

    def select_by_users(self, id):
        """
        Selects a user by id.

        Returns:
            tuple: User data.
        """
        query = """
            SELECT username, email, password_hash FROM users
            WHERE id = ?
        """

        return self._execute_query(query, (id,), select=True, single=True)

    def like_by_username(self, username):
        """
        Selects a user by username.

        Returns:
            list[tuple]: List of id, username and email.
        """
        query = """
            SELECT id, username, email FROM users
            WHERE username LIKE ?
        """

        return self._execute_query(query, (f"%{username}%",), select=True)

    def like_by_email(self, email):
        """
        Selects a user by email.

        Returns:
            list[tuple]: List of id, username and email.
        """
        query = """
            SELECT id, username, email FROM users
            WHERE email LIKE ?
        """

        return self._execute_query(query, (f"%{email}%",), select=True)
