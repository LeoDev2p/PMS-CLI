class ControllerBundle:
    """Container for all controller instances."""

    def __init__(
        self, user, auth, project, project_status, task, task_status, user_project
    ):
        self.user = user
        self.auth = auth
        self.project = project
        self.project_status = project_status
        self.task = task
        self.task_status = task_status
        self.user_project = user_project
