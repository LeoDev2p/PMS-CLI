from src.models.sqlite import BaseModels


class ProjectModels(BaseModels):
    def select_by_projects(self, title):
        query = "SELECT id FROM projects WHERE title = ?"

        return self._execute_query(query, (title,), select=True, fetch=1)
