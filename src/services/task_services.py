from src.core.exceptions import (
    NotFoundProjectError,
    NotFoundTaskError,
    NotFoundTaskStatusError,
)


class TaskServices:
    def __init__(self, task_model, project_model):
        self.task_model = task_model
        self.project_model = project_model

    def fetch_tasks_of_user(self, id) -> list[tuple]:
        result = self.task_model.select_all_tasks_of_user(id)
        if not result:
            raise NotFoundTaskError("No tasks found for this user.")

        return result

    def modify_id_taskstatus(self, tasK_name, task_title, project_title):
        print (f"[DEBUG] task service {tasK_name}")
        id_taskstatus = self.task_model.select_by_task_status(tasK_name)
        print(f"[DEBUG] task service {id_taskstatus}")
        if not id_taskstatus:
            raise NotFoundTaskStatusError("The task status could not be found.")

        id_projects = self.project_model.select_by_projects(project_title)
        if not id_projects:
            raise NotFoundProjectError("Project not found.")

        params = (id_taskstatus[0], task_title, id_projects[0])
        result = self.task_model.update_by_status_task(params)
        if not result:
            raise NotFoundTaskError("Task not found.")

        return result
