from src.models.base import BaseModels


class TaskModels(BaseModels):
    """Handles task CRUD operations."""

    # ── select ──────────────────────────────────────────────
    def get_all(self) -> list[tuple]:
        """Returns all tasks."""
        query = "SELECT * FROM task"
        return self._execute_query(query, select=True)

    def get_by_project_and_title(self, params: tuple) -> tuple:
        """Returns a task by project title and task title."""
        query = """
            SELECT
                t.title,
                t.description,
                ts.name,
                p.title
            FROM task t
            JOIN task_status ts ON t.id_status = ts.id
            JOIN projects p ON t.id_projects = p.id
            WHERE p.title = ? AND t.title = ?
        """
        return self._execute_query(query, params, select=True, single=True)

    def get_all_by_user(self, id: int) -> list[tuple]:
        """Returns all tasks assigned to a user."""
        query = """
            SELECT
                t.title,
                t.description,
                ts.name,
                p.title
            FROM task t
            JOIN task_status ts ON t.id_status = ts.id
            JOIN projects p ON t.id_projects = p.id
            WHERE t.id_assigned_to = ?
        """
        return self._execute_query(query, (id,), select=True)

    def get_all_by_project(self, id: int) -> list[tuple]:
        """Returns all tasks of a project with assignment info."""
        query = """
            SELECT
                p.title AS project,
                COALESCE(u.username, 'SIN ASIGNAR (Vacante)') AS responsible,
                t.title AS task_,
                ts.name AS progress
            FROM task t
            JOIN projects p ON t.id_projects = p.id
            JOIN task_status ts ON t.id_status = ts.id
            LEFT JOIN users u ON t.id_assigned_to = u.id
            WHERE p.id = ?
            ORDER BY responsible DESC;
        """
        return self._execute_query(query, (id,), select=True)

    def get_details_by_project(self, params: tuple) -> list[tuple]:
        """Returns task details (id, title, status, project, user) by project."""
        query = """
            SELECT
                t.id,
                t.title,
                ts.name,
                p.title,
                u.username
            FROM task t
            LEFT JOIN task_status ts ON t.id_status = ts.id
            LEFT JOIN projects p ON t.id_projects = p.id
            LEFT JOIN users u ON t.id_assigned_to = u.id
            WHERE t.id_projects = ? AND t.id_assigned_to = ?
        """
        return self._execute_query(query, params, select=True)

    # ── insert ──────────────────────────────────────────────
    def create(self, params: tuple):
        """Inserts a new task."""
        query = """
            INSERT INTO task (title, description, id_status, id_projects, id_assigned_to)
            VALUES (?, ?, 1, ?, ?)
        """
        self._execute_query(query, params)

    # ── update ──────────────────────────────────────────────
    def update_status(self, params: tuple):
        """Updates the status of a task."""
        query = """
            UPDATE task
            SET id_status = ?
            WHERE id = ? AND id_projects = ?
        """
        self._execute_query(query, params)

    def update_assigned_user(self, params: tuple):
        """Updates the assigned user of a task."""
        query = """
            UPDATE task
            SET id_assigned_to = ?
            WHERE id = ?
        """
        self._execute_query(query, params)

    def unassign_tasks_by_user_project(self, params: tuple):
        """Sets id_assigned_to to NULL for all tasks of a user in a specific project.

        Args:
            params: (id_assigned_to, id_projects)
        """
        query = """
            UPDATE task
            SET id_assigned_to = NULL
            WHERE id_assigned_to = ? AND id_projects = ?
        """
        self._execute_query(query, params)
    
    # ── stats ──────────────────────────────────────────────
    def completion_efficiency(self) -> list[tuple]:
        """Completion Efficiency: Tasks completed per week/month."""
        query = """
            SELECT
                strftime('%m', created) as month,
                count(id) as total_tasks
            FROM task
            WHERE strftime('%Y', created) = '2025'
            GROUP BY strftime('%m', created)
            ORDER BY month ASC
        """
        return self._execute_query(query, select=True)


class TaskStatusModels(BaseModels):
    """Handles task_status CRUD operations."""

    # ── select ──────────────────────────────────────────────
    def get_all(self) -> list[tuple]:
        """Returns all task statuses."""
        query = "SELECT * FROM task_status"
        return self._execute_query(query, select=True)

    def get_by_name(self, name: str) -> tuple:
        """Returns a task status id by name."""
        query = """
            SELECT id
            FROM task_status
            WHERE name = ?
        """
        return self._execute_query(query, (name,), select=True, single=True)

    def get_by_system_key(self, system_key: str) -> tuple:
        """Returns a task status id by system key."""
        query = """
            SELECT id
            FROM task_status
            WHERE system_key = ?
        """
        return self._execute_query(query, (system_key,), select=True, single=True)

    # ── insert ──────────────────────────────────────────────
    def create(self, params: tuple | list[tuple], is_many=False):
        """Inserts one or many task statuses.

        Args:
            params: (name, system_key, is_active) or list of tuples.
            is_many: True for bulk insert.
        """
        query = """
            INSERT INTO task_status (name, system_key, is_active)
            VALUES (?, ?, ?)
        """
        self._execute_query(query, params, is_many=is_many)

    # ── update ──────────────────────────────────────────────
    def update(self, params: tuple):
        """Updates a task status name."""
        query = """
            UPDATE task_status
            SET name = ?
            WHERE id = ?
        """
        self._execute_query(query, params)

    # ── delete ──────────────────────────────────────────────
    def delete(self, id: int):
        """Deletes a task status."""
        query = "DELETE FROM task_status WHERE id = ?"
        self._execute_query(query, (id,))
    
    # ── stats ──────────────────────────────────────────────
    def state_distribution(self) -> list[tuple]:
        """State Distribution: How many tasks are in each global state."""
        query = """
            SELECT
                ts.name AS status,
                ts.system_key,
                COUNT(t.id) AS total_tasks
            FROM task_status ts
            LEFT JOIN task t ON ts.id = t.id_status
            GROUP BY ts.id, ts.name, ts.system_key
            ORDER BY ts.id;
        """
        return self._execute_query(query, select=True)
    
    def blocking_rate(self) -> list[tuple]:
        """Blocking Rate: Number of tasks paused or blocked."""
        query = """
            SELECT
                ts.name AS status,
                COUNT(t.id) AS total_locked
            FROM task_status ts
            LEFT JOIN task t ON ts.id = t.id_status
            WHERE ts.system_key = 'BLOCKED'
            GROUP BY ts.id, ts.name;
        """
        return self._execute_query(query, select=True)
