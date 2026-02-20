from src.models.sqlite import BaseModels


class ProjectModels(BaseModels):
    # select
    def select_all_project(self) -> list[tuple]:
        query = """
            SELECT p.title, ps.name FROM projects p
            JOIN projects_status ps ON p.id_status = ps.id
        """

        return self._execute_query(query, select=True)

    def select_by_project(self, title: str) -> tuple:
        query = "SELECT id, title FROM projects WHERE title = ?"

        return self._execute_query(query, (title,), select=True, single=True)

    def select_all_status(self) -> list[tuple]:
        query = "SELECT * FROM projects_status"

        return self._execute_query(query, select=True)

    # insert
    def insert_projects_status(self, params: list[tuple]):
        query = """
            INSERT INTO projects_status (name)
            VALUES (?)
        """

        self._execute_query(query, params, is_many=True)

    def insert_project(self, params: tuple):
        query = """
            INSERT INTO projects (title, description, id_admin)
            VALUES (?, ?, ?)
        """

        self._execute_query(query, params)

    def insert_project_user(self, params):
        query = """
            INSERT INTO project_user (id_project, id_user)
            VALUES (?, ?)
        """

        self._execute_query(query, params, is_many=True)

    # update
    def update_project(self, params): # observar aqui
        query = """
            UPDATE projects
            SET title = ?, id_status = ?
            WHERE id = ?
        """

        self._execute_query(query, params)

    # delete
    def delete_project(self, id):
        query = """
            DELETE FROM projects
            WHERE id = ?
        """

        self._execute_query(query, (id,))
