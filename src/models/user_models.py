from src.models.base import BaseModels


class UsersModels(BaseModels):
    """
    Handles user models.
    """

    def select_all(self) -> list[tuple]:
        """
        Selects all users.

        Returns:
            list[tuple]: List of id, username, email, role and create_by.
        """
        query = """
            SELECT
                id,
                username,
                email,
                role,
                create_by
            FROM users
        """

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

    def update_profile(self, params: tuple):
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
            SET password_hash = ?
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

    def delete(self, id):
        """
        Deletes a user.
        """
        query = """
            DELETE FROM users
            WHERE id = ?
        """

        self._execute_query(query, (id,))

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
            SELECT
                username,
                email,
                password_hash
            FROM users
            WHERE id = ?
        """

        return self._execute_query(query, (id,), select=True, single=True)

    def select_users_without_active_tasks(self) -> list[tuple]:
        query = """
            SELECT
                u.id,
                u.username
            FROM users u
            WHERE u.id NOT IN (
                SELECT t.id_assigned_to
                FROM task t
                JOIN task_status ts ON t.id_status = ts.id
                WHERE ts.system_key != 'COMPLETED'
                AND t.id_assigned_to IS NOT NULL
            ) AND u.role <> 'admin';
        """

        return self._execute_query(query, select=True)

    def select_free_operational_users(self) -> list[tuple]:
        """
        Selects all users operational.

        Returns:
            list[tuple]: List of id, username and email.
        """
        query = """
            SELECT
                u.id,
                u.username,
                t.title
            FROM users u
            LEFT JOIN task t ON u.id = t.id_assigned_to
            WHERE u.role <> 'admin' AND t.title is NULL
        """

        return self._execute_query(query, select=True)
    
    def select_user_by_project(self, id_project):
        """selecionar usuarios por proyecto y tareas"""

        query = """
        SELECT
            u.id,
            u.username,
            p.title
        FROM users u
        JOIN users_projects up ON u.id = up.id_users
        JOIN projects p ON up.id_projects = p.id
        WHERE p.id = ?
        """
        
        return self._execute_query(query, (id_project,), select=True)

    def like_by_username(self, username) -> list[tuple]:
        """
        Selects a user by username.

        Returns:
            list[tuple]: List of id, username and email.
        """
        query = """
            SELECT
                id,
                username,
                email
            FROM users
            WHERE username LIKE ?
        """

        return self._execute_query(query, (f"%{username}%",), select=True)

    def like_by_email(self, email) -> list[tuple]:
        """
        Selects a user by email.

        Returns:
            list[tuple]: List of id, username and email.
        """
        query = """
            SELECT
                id,
                username,
                email
            FROM users
            WHERE email LIKE ?
        """

        return self._execute_query(query, (f"%{email}%",), select=True)

    # stats
    def count_free_vs_assigned_users(self):
        """
        Count free users versus assigned users.

        Returns:
            list[tuple]: List of free users and assigned users.
        """
        query = """
            WITH AssignedCount AS (
                SELECT COUNT(DISTINCT id_users) as assigned
                FROM users_projects
            ),
            FreeCount AS (
                SELECT COUNT(id) as free
                FROM users
                WHERE role <> 'admin'
                AND id NOT IN (SELECT id_users FROM users_projects)
            )
            SELECT
                (SELECT free FROM FreeCount) as free_users,
                (SELECT assigned FROM AssignedCount) as assigned_users;
        """

        return self._execute_query(query, select=True)

    def count_tasks_by_user(self):
        """
        Workload: Count of tasks by status by user.

        Returns:
            list[tuple]: List of user and count.
        """
        query = """
            SELECT
                u.username,
                SUM(CASE WHEN ts.system_key = 'PENDING' THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN ts.system_key = 'IN_PROGRESS' THEN 1 ELSE 0 END) AS in_progress,
                SUM(CASE WHEN ts.system_key = 'REVIEW' THEN 1 ELSE 0 END) AS in_review,
                SUM(CASE WHEN ts.system_key = 'COMPLETED' THEN 1 ELSE 0 END) AS completed,
                SUM(CASE WHEN ts.system_key = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled,
                COUNT(t.id) AS total_tasks
            FROM users u
            INNER JOIN task t ON u.id = t.id_assigned_to
            INNER JOIN task_status ts ON t.id_status = ts.id
            GROUP BY u.id, u.username;
        """

        return self._execute_query(query, select=True)
    
    def productivity_ranking(self):
        """
        Productivity Ranking Top 3 users with the most completed tasks.

        Returns:
            list[tuple]: List of user and count.
        """
        query = """
            SELECT
                u.username,
                COUNT(t.id) AS amount
            FROM users u
            JOIN task t ON u.id = t.id_assigned_to
            JOIN task_status ts ON t.id_status = ts.id
            WHERE ts.system_key = 'COMPLETED'
            AND strftime('%m', t.created) = strftime('%m', 'now', '-1 month')
            AND strftime('%Y', t.created) = strftime('%Y', 'now', '-1 month')
            GROUP BY u.username
            ORDER BY amount DESC
            LIMIT 3;
        """

        return self._execute_query(query, select=True)
