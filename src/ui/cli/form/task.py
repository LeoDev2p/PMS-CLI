
class FormsTask:
    """
    Class to manage forms tasks.
    """

    @staticmethod
    def edit_taskstatus_forms():
        try:
            project_title = input("[project title]: ")
            task_title = input("[task title]: ")
            state_name = input("[New task status name]: ")
            return state_name, task_title, project_title
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def asigne_task():
        title = input("[New task]: ")
        description = input("[Description]: ")
        return title, description

    @staticmethod
    def edit_status():
        try:
            id = int(input("[Id]: "))
            status = input("[New status]: ")
            return id, status
        except ValueError as e:
            print(str(e))


    @staticmethod
    def system_key_status():
        try:
            key = int(input("[Id type]: "))
            return key
        except ValueError as e:
            print(str(e))

