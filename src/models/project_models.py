from src.models.base import BaseModels


class ProjectModels(BaseModels):
    """Handles project CRUD operations."""

    # ── select ──────────────────────────────────────────────
    def get_all(self, search: str = None) -> list[tuple]:
        """Returns all projects with their status."""
        query = """
            SELECT
                p.id,
                p.title,
                ps.name
            FROM projects p
            JOIN projects_status ps ON p.id_status = ps.id
        """
        params = ()
        if search:
            query += " WHERE p.title LIKE ?"
            params = (f"%{search}%",)

        return self._execute_query(query, params, select=True)

    def get_by_title(self, title: str) -> list[tuple]:
        """Returns projects matching title (LIKE)."""
        query = """
            SELECT id, title
            FROM projects
            WHERE title like ?
        """
        return self._execute_query(query, (f"%{title}%",), select=True)

    def search_by_title(self, title: str) -> list[tuple]:
        """Returns projects matching title with description, limit 10."""
        query = """
            SELECT
                id,
                title,
                description
            FROM projects
            WHERE title LIKE ?
            ORDER BY title ASC LIMIT 10;
        """
        return self._execute_query(query, (f"%{title}%",), select=True)

    def count_by_title(self, title: str) -> tuple:
        """Counts projects matching title."""
        query = """
            SELECT COUNT(*)
            FROM projects
            WHERE title LIKE ?;
        """
        return self._execute_query(query, (f"%{title}%",), select=True, single=True)

    def get_new(self) -> list[tuple]:
        """Returns all projects with NEW status."""
        query = """
            SELECT
                p.id,
                p.title,
                ps.system_key
            FROM projects p
            JOIN projects_status ps ON p.id_status = ps.id
            WHERE ps.system_key = 'NEW'
        """
        return self._execute_query(query, select=True)

    def get_new_active(self) -> list[tuple]:
        """Returns all projects with NEW or ACTIVE status."""
        query = """
            SELECT
                p.id,
                p.title
            FROM projects p
            JOIN projects_status ps ON p.id_status = ps.id
            WHERE ps.system_key in ('NEW', 'ACTIVE')
            ORDER BY P.id DESC
        """
        return self._execute_query(query, select=True)

    # ── insert ──────────────────────────────────────────────
    def create(self, params: tuple):
        """Inserts a new project."""
        query = """
            INSERT INTO projects (title, description, id_admin, id_status)
            VALUES (?, ?, ?, ?)
        """
        self._execute_query(query, params)

    # ── update ──────────────────────────────────────────────
    def update_title(self, params: tuple):
        """Updates a project title."""
        query = """
            UPDATE projects
            SET title = ?
            WHERE id = ?
        """
        self._execute_query(query, params)

    def update_status(self, params: tuple):
        """Updates a project's status reference."""
        query = """
            UPDATE projects
            SET id_status = ?
            WHERE id = ?
        """
        self._execute_query(query, params)

    # ── delete ──────────────────────────────────────────────
    def delete(self, id: int):
        """Deletes a project."""
        query = "DELETE FROM projects WHERE id = ?"
        self._execute_query(query, (id,))

    # ── stats ──────────────────────────────────────────────
    def project_progress(self) -> list[tuple]:
        """Returns project progress."""

        query = """
            SELECT
                p.title AS project,
                COUNT(CASE WHEN ts.system_key = 'COMPLETED' THEN 1 END) AS completed,
                COUNT(t.id) AS total_tasks,
                ROUND(
                    (COUNT(CASE WHEN ts.system_key = 'COMPLETED' THEN 1 END) * 1.0 / 
                    NULLIF(COUNT(t.id), 0)) * 100, 
                2) || ' %' AS advance
            FROM projects p
            LEFT JOIN task t ON p.id = t.id_projects
            LEFT JOIN task_status ts ON t.id_status = ts.id
            GROUP BY p.id, p.title;
        """
        return self._execute_query(query, select=True)

    def count_users_by_project(self) -> list[tuple]:
        """Users per Project: Counting people to see if there is a staff shortage."""

        query = """
            SELECT
                p.title,
                count(DISTINCT up.id_users) AS count_users
            FROM projects p
            LEFT JOIN users_projects up ON p.id = up.id_projects
            GROUP BY p.id, p.title
        """
        return self._execute_query(query, select=True)
    
    def critical_projects(self) -> list[tuple]:
        """Returns projects that are not assigned to any user."""
        query = """
            SELECT
                p.title AS proyecto,
                COUNT(CASE WHEN ts.system_key = 'BLOCKED' THEN 1 END) AS tasks_paused,
                COUNT(CASE WHEN ts.system_key = 'IN_PROGRESS' THEN 1 END) AS tasks_in_progress
            FROM projects p
            JOIN task t ON p.id = t.id_projects
            JOIN task_status ts ON t.id_status = ts.id
            GROUP BY p.id
            HAVING tasks_paused > tasks_in_progress;
        """
        return self._execute_query(query, select=True)


class ProjectStatusModels(BaseModels):
    """Handles projects_status CRUD operations."""

    # ── select ──────────────────────────────────────────────
    def get_all(self) -> list[tuple]:
        """Returns all project statuses."""
        query = "SELECT * FROM projects_status"
        return self._execute_query(query, select=True)

    def get_by_system_key(self, system_key: str) -> tuple:
        """Returns a project status id by system key."""
        query = """
            SELECT id
            FROM projects_status
            WHERE system_key = ?
        """
        return self._execute_query(query, (system_key,), select=True, single=True)

    def get_default_id(self) -> tuple:
        """Returns the minimum (default) status id."""
        query = """
            SELECT MIN(id)
            FROM projects_status
        """
        return self._execute_query(query, select=True, single=True)

    # ── insert ──────────────────────────────────────────────
    def create(self, params: tuple | list[tuple], is_many=False):
        """Inserts one or many project statuses.

        Args:
            params: (name, system_key, is_active) or list of tuples.
            is_many: True for bulk insert.
        """
        query = """
            INSERT INTO projects_status (name, system_key, is_active)
            VALUES (?, ?, ?)
        """
        self._execute_query(query, params, is_many=is_many)

    # ── update ──────────────────────────────────────────────
    def update(self, params: tuple):
        """Updates a project status name."""
        query = """
            UPDATE projects_status
            SET name = ?
            WHERE id = ?
        """
        self._execute_query(query, params)

    # ── delete ──────────────────────────────────────────────
    def delete(self, id: int):
        """Deletes a project status."""
        query = "DELETE FROM projects_status WHERE id = ?"
        self._execute_query(query, (id,))


class UserProjectModels(BaseModels):
    """Handles users_projects junction table operations."""

    # ── select ──────────────────────────────────────────────
    def exists(self, id_user: int, id_project: int) -> tuple:
        """Checks if a user-project membership exists."""
        query = """
            SELECT
                id_users,
                id_projects
            FROM users_projects
            WHERE id_users = ? AND id_projects = ?
        """
        return self._execute_query(
            query, (id_user, id_project), select=True, single=True
        )

    # ── insert ──────────────────────────────────────────────
    def create(self, id_user: int, id_project: int):
        """Adds a user to a project."""
        query = """
            INSERT INTO users_projects (id_users, id_projects)
            VALUES (?, ?)
        """
        self._execute_query(query, (id_user, id_project))

    def create_many(self, params: list[tuple]):
        """Adds multiple user-project relationships."""
        query = """
            INSERT INTO users_projects (id_users, id_projects)
            VALUES (?, ?)
        """
        self._execute_query(query, params, is_many=True)

    # ── delete ──────────────────────────────────────────────
    def delete(self, params: tuple):
        """Removes a user-project membership."""
        query = """
            DELETE FROM users_projects
            WHERE id_users = ? AND id_projects = ?
        """
        self._execute_query(query, params)
