class AdminMenus:
    """
    Class to manage admin menus.
    """
    @staticmethod
    def menu():
        print("""
                      ADMIN PANEL\n
        [1] User management
        [2] Project management
        [3] Statistics panel
        [4] Logout
        """)

    @staticmethod
    def menu_project():
        print("""
                      ADMIN MANAGEMENT\n
        [1] projects
        [2] system setting
        [3] Gestion operativa
        [4] Back
        """)

    #ManagementProjectViews

    @staticmethod
    def menu_management_project():
        print("""
                      PROJECTS MANAGEMENT\n
        [1] nuevo proyecto
        [2] listar proyecto
        [3] editar proyecto
        [4] eliminar proyecto
        [5] Back
        """)
    
    @staticmethod
    def menu_edit_project():
        print("""
                      EDIT PROJECT\n
        [1] Editing title
        [2] Editing status
        [3] Back
        """)

    #SettingsViews

    @staticmethod
    def menu_system_setting():
        print("""
                      SYSTEM SETTING\n
        [1] gestionar estados de proyectos
        [2] gestionar estados de tareas
        [3] Back
        """)

    @staticmethod
    def menu_status_projects():
        print("""
                      STATUS PROJECTS
        [1] crear estado
        [2] listar estados
        [3] editar estado
        [4] eliminar estado
        [5] Back
        """)

    @staticmethod
    def menu_status_tasks():
        print("""
                      STATUS TASKS
        [1] crear estado
        [2] listar estados
        [3] editar estado
        [4] eliminar estado
        [5] Back
        """)

    #OperationalViews
    
    @staticmethod
    def menu_operational():
        print("""
                      OPERATIONAL
        [1] new assignment / create task
        [2] team control / monitoring
        [3] personnel maintenance
        [4] Back
        """)
