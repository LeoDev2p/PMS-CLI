from src.models.sqlite import BaseModels


class TaskModels(BaseModels):
    # admin
    def select_all(self):
        query = """
        SELECT * FROM task
        """

        return self._execute_query(query)
    
    # user
    def select_task_by_project_task(self, params):
        query = """
            SELECT t.title, t.description, ts.name, p.title FROM task t
            JOIN task_status ts ON t.id_status = ts.id
            JOIN projects p ON t.id_projects = p.id
            WHERE p.title = ? AND t.title = ?
        """

        return self._execute_query(query, params, select=True, single=True)

    def select_all_tasks_of_user(self, id):
        query = """
            SELECT t.title, t.description, ts.name, p.title FROM task t
            JOIN task_status ts ON t.id_status = ts.id
            JOIN projects p ON t.id_projects = p.id
            WHERE t.id_assigned_to = ?
        """

        return self._execute_query(query, (id,), select=True)

    def select_by_task_status(self, name):
        query = "SELECT id FROM task_status WHERE name = ?"

        return self._execute_query(query, (name,), select=True, single=True)
    
    def update_by_status_task(self, params):
        query = """
            UPDATE task
            SET id_status = ?
            WHERE title = ? AND id_projects = ?
        """

        return self._execute_query(query, params)

