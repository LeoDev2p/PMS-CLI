from src.models.sqlite import BaseModels


class TaskModels(BaseModels):
    """
    Handles task models.
    """
    # select
    def select_all(self):
        """
        Selects all tasks.

        Returns:
            list[tuple]: List of tasks.
        """
        query = """
        SELECT * FROM task
        """

        return self._execute_query(query, select=True)
    
    def select_all_status(self):
        """
        Selects all task statuses.

        Returns:
            list[tuple]: List of task statuses.
        """
        query = """
            SELECT * FROM task_status
        """

        return self._execute_query(query, select=True)

    def select_task_by_project_task(self, params):
        """
        Selects a task by project and task title.

        Args:
            params (tuple): Tuple of (project_title, task_title).

        Returns:
            tuple: Tuple of (task_title, task_description, task_status, project_title).
        """
        query = """
            SELECT t.title, t.description, ts.name, p.title FROM task t
            JOIN task_status ts ON t.id_status = ts.id
            JOIN projects p ON t.id_projects = p.id
            WHERE p.title = ? AND t.title = ?
        """

        return self._execute_query(query, params, select=True, single=True)

    def select_all_tasks_of_user(self, id):
        """
        Selects all tasks of a user.

        Args:
            id (int): User id.

        Returns:
            list[tuple]: List of tasks.
        """
        query = """
            SELECT t.title, t.description, ts.name, p.title FROM task t
            JOIN task_status ts ON t.id_status = ts.id
            JOIN projects p ON t.id_projects = p.id
            WHERE t.id_assigned_to = ?
        """

        return self._execute_query(query, (id,), select=True)

    def select_by_task_status(self, name):
        """
        Selects a task status by name.

        Args:
            name (str): Task status name.

        Returns:
            tuple: Tuple of (task_status_id,).
        """
        query = "SELECT id FROM task_status WHERE name = ?"

        return self._execute_query(query, (name,), select=True, single=True)
    
    def select_by_system_key(self, system_key):
        """
        Selects a task status by system key.

        Args:
            system_key (str): Task status system key.

        Returns:
            tuple: Tuple of (task_status_id,).
        """
        query = "SELECT id FROM task_status WHERE system_key = ?"

        return self._execute_query(query, (system_key,), select=True, single=True)
    
    def select_all_tasks_of_project(self, id):
        """
        Selects all tasks of a project.

        Args:
            id (int): Project id.

        Returns:
            list[tuple]: List of tasks.
        """
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
    

    def select_by_task_title(self, id_project: int) -> list[tuple]:
        """
        Selects a task by title.

        Returns:
            list[tuple]: List of tasks.
        """
        query = """
            SELECT t.id, t.title, ts.name, p.title, u.username FROM task t
            LEFT JOIN task_status ts ON t.id_status = ts.id
            LEFT JOIN projects p ON t.id_projects = p.id
            LEFT JOIN users u ON t.id_assigned_to = u.id
            WHERE p.id = ?
        """

        return self._execute_query(query, (id_project,), select=True)
    
    # insert
    def insert_task(self, params):
        """
        Inserts a new task.

        Args:
            params (tuple): Tuple of (title, description, id_projects, id_assigned_to).
        """
        query = """
            INSERT INTO task (title, description, id_status, id_projects, id_assigned_to)
            VALUES (?, ?, 1, ?, ?)
        """

        self._execute_query(query, params)

    def insert_task_status(self, params: tuple | list[tuple], is_many = False):
        """
        Inserts a new task status.

        Args:
            params (tuple | list[tuple]): Tuple or list of tuples of task status names.
            is_many (bool): Whether the params is a list of tuples.
        """
        query = """
            INSERT INTO task_status (name, system_key, is_active)
            VALUES (?, ?, ?)
        """

        self._execute_query(query, params, is_many = is_many)

    # update
    def update_by_status_task(self, params):
        """
        Updates the status of a task.

        Args:
            params (tuple): Tuple of (task_status_id, task_title, project_title).
        """
        query = """
            UPDATE task
            SET id_status = ?
            WHERE id = ? AND id_projects = ?
        """

        self._execute_query(query, params)
    
    def update_status(self, params):
        """
        Updates the status of a task status.

        Args:
            params (tuple): Tuple of (task_status_name, task_status_id).
        """
        query = """
            UPDATE task_status
            SET name = ?
            WHERE id = ?
        """

        self._execute_query(query, params)
    
    # delete
    def delete_status(self, id):
        """
        Deletes a task status.

        Args:
            id (int): Task status id.
        """
        query = "DELETE FROM task_status WHERE id = ?"

        self._execute_query(query, (id,))
