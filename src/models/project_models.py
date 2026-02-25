from src.models.sqlite import BaseModels


class ProjectModels(BaseModels):
    """
    Class to manage project models.
    """

    # select
    def select_all_project(self) -> list[tuple]:
        """
        Selects all projects.

        Returns:
            list[tuple]: List of tuples of projects.
        """
        query = """
            SELECT p.id, p.title, ps.name FROM projects p
            JOIN projects_status ps ON p.id_status = ps.id
        """

        return self._execute_query(query, select=True)

    def select_by_project(self, title: str) -> tuple:
        """
        Selects a project by title.

        Args:
            title (str): Project title.

        Returns:
            tuple: Tuple of the project.
        """
        query = "SELECT id, title FROM projects WHERE title = ?"

        return self._execute_query(query, (title,), select=True, single=True)

    def select_all_status(self) -> list[tuple]:
        """
        Selects all project statuses.

        Returns:
            list[tuple]: List of tuples of project statuses.
        """
        query = "SELECT * FROM projects_status"

        return self._execute_query(query, select=True)

    def select_by_system_key(self, system_key: str) -> tuple:
        """
        Selects a project status by system key.

        Args:
            system_key (str): Project status system key.

        Returns:
            tuple: Tuple of the project status.
        """
        query = "SELECT id FROM projects_status WHERE system_key = ?"

        return self._execute_query(query, (system_key,), select=True, single=True)

    def default_min_id_status(self) -> tuple:
        """
        Returns the default minimum id of project status.

        Returns:
            tuple: Default minimum id of project status.
        """
        query = "SELECT MIN(id) FROM projects_status WHERE system_key = 'active'"

        return self._execute_query(query, select=True, single=True)

    def select_projects_new(self) -> list[tuple]:
        """
        Selects all new projects.

        Returns:
            list[tuple]: List of tuples of new projects.
        """
        query = """
            SELECT p.id, p.title, ps.system_key FROM projects p
            JOIN projects_status ps ON  p.id_status = ps.id
            WHERE ps.system_key = 'NEW'
        """

        return self._execute_query(query, select=True)

    def select_projects_by_title(self, title: str) -> list[tuple]:
        """
        Selects all projects by title.

        Args:
            title (str): Project title.

        Returns:
            list[tuple]: List of tuples of projects.
        """
        query = """
            SELECT id, title, description
            FROM projects
            WHERE title LIKE ?
            ORDER BY title ASC LIMIT 10;
        """

        return self._execute_query(query, (f"%{title}%",), select=True)

    def count_projects_by_title(self, title: str) -> int:
        """
        Counts the number of projects by title.

        Args:
            title (str): Project title.

        Returns:
            int: Number of projects.
        """
        query = """
            SELECT COUNT(*)
            FROM projects
            WHERE title LIKE ?;
        """

        return self._execute_query(query, (f"%{title}%",), select=True, single=True)

    # insert
    def insert_projects_status(self, params: tuple | list[tuple], is_many=False):
        """
        Inserts a new project status.

        Args:
            params (tuple | list[tuple]): Tuple or list of tuples of project statuses.
            is_many (bool): Whether to insert multiple project statuses.
        """
        query = """
            INSERT INTO projects_status (name, system_key, is_active)
            VALUES (?, ?, ?)
        """

        self._execute_query(query, params, is_many=is_many)

    def insert_project(self, params: tuple):
        """
        Inserts a new project.

        Args:
            params (tuple): Tuple of project parameters.
        """
        query = """
            INSERT INTO projects (title, description, id_admin, id_status)
            VALUES (?, ?, ?, ?)
        """

        self._execute_query(query, params)

    def insert_project_user(self, params):
        """
        Inserts a new project user.

        Args:
            params (tuple): Tuple of project user parameters.
        """
        query = """
            INSERT INTO project_user (id_project, id_user)
            VALUES (?, ?)
        """

        self._execute_query(query, params, is_many=True)

    # update
    def update_project(self, params):
        """
        Updates a project.

        Args:
            params (tuple): Tuple of project parameters.
        """
        query = """
            UPDATE projects
            SET title = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    def update_project_status_by_project(self, params):
        """
        Updates a project status by project.

        Args:
            params (tuple): Tuple of project status parameters.
        """
        query = """
            UPDATE projects
            SET id_status = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    def update_project_status(self, params):
        """
        Updates a project status.

        Args:
            params (tuple): Tuple of project status parameters.
        """
        query = """
            UPDATE projects_status
            SET name = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    # delete
    def delete_project(self, id):
        """
        Deletes a project.

        Args:
            id (int): Project id.
        """
        query = """
            DELETE FROM projects
            WHERE id = ?
        """

        self._execute_query(query, (id,))

    def delete_project_status(self, id):
        """
        Deletes a project status.

        Args:
            id (int): Project status id.
        """
        query = """
            DELETE FROM projects_status
            WHERE id = ?
        """

        self._execute_query(query, (id,))
