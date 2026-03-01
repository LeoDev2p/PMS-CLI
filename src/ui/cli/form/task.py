
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
    def status_fields(edit=False, delete=False):
        if edit:
            try:
                id = int(input("[Id]: "))
                status = input("[New status]: ")
                return id, status
            except ValueError as e:
                print(str(e))

        elif delete:
            try:
                id = int(input("[Id]: "))
                return id
            except ValueError as e:
                print(str(e))

        status = input("[New status]: ")
        return status

    @staticmethod
    def system_key_status():
        try:
            key = int(input("[Id type]: "))
            return key
        except ValueError as e:
            print(str(e))

    @staticmethod
    def search_task_forms():
        try:
            title = input("[Task title]: ")
            return title
        except ValueError as e:
            print(str(e))

    @staticmethod
    def id_forms():
        try:
            id = int(input("[Selecy id]: "))
            return id
        except ValueError as e:
            print(str(e))