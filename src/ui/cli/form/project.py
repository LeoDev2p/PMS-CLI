class FormsProjects:
    """
    Class to manage forms projects.
    """

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
    def edit_project_forms():
        try:
            id = int(input("[Id]: "))
            title = input("[New title]: ")
            return title, id
        except ValueError as e:
            print(str(e))

    @staticmethod
    def edit_project_status_forms():
        # eliminar
        try:
            id_project = int(input("[Id project]: "))
            id_status = int(input("[Id status]: "))
            return id_status, id_project
        except ValueError as e:
            print(str(e))

    @staticmethod
    def project_forms():
        title = input("[New project]: ")
        description = input("[Description]: ")
        return title, description

    @staticmethod
    def search_project_forms():
        try:
            title = input("[Search by title]: ")
            return title
        except ValueError as e:
            print(str(e))
