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
    
    def select_user_free():
        pass
    
    # insert
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
            WHERE title = ? AND id_projects = ?
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
    def delte_status(self, id):
        """
        Deletes a task status.

        Args:
            id (int): Task status id.
        """
        query = "DELTE FROM task_status WHERE id = ?"

        self._execute_query(query, (id,))
