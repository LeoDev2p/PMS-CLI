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

    # User management
    @staticmethod
    def menu_users():
        print("""
                      USER MANAGEMENT\n
        [1] Create user
        [2] Edit user
        [3] Delete user
        [4] View users
        [5] Back
        """)

    @staticmethod
    def menu_edit_users():
        print("""
                      EDIT USER\n
        [1] change username
        [2] change email
        [3] reset password
        [4] change role
        [5] Back
        """)

    # ManagementProjectViews
    @staticmethod
    def menu_project():
        print("""
                      ADMIN MANAGEMENT\n
        [1] projects
        [2] system setting
        [3] Gestion operativa
        [4] Back
        """)

    # Projects
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

    # system setting
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

    # Gestion operativa
    @staticmethod
    def menu_operational():
        print("""
                      OPERATIONAL
        [1] new assignment / create task
        [2] team control / monitoring
        [3] personnel maintenance
        [4] Back
        """)

    @staticmethod
    def menu_team_monitoring():
        print("""
                      TEAM MONITORING
        [1] View Team by Project
        [2] Change Task Status
        [3] Back
        """)

    @staticmethod
    def menu_personnel_maintenance():
        print("""
                      PERSONNEL MAINTENANCE
        [1] Reassign User
        [2] Remove User
        [3] Back
        """)

    # Statistics panel
    @staticmethod
    def menu_statistics():
        print("""
                      STATISTICS

        [1] Talent Management (users)
        [2] Health Status (projects)
        [3] Performance and Averages (metrics)
        [4] Back
        """)

    @staticmethod
    def menu_talent_management():
        print("""
                      TALENT MANAGEMENT

        [1] Availability counter
        [2] Workload per user
        [3] Productivity ranking
        [4] Back
        """)

    @staticmethod
    def menu_health_status():
        print("""
                      HEALTH STATUS

        [1] Project progress
        [2] Distribution of states
        [3] Users per project
        [4] Back
        """)

    @staticmethod
    def menu_performance_metrics():
        print("""
                      PERFORMANCE METRICS

        [1] Blocking rate
        [2] Completion Efficiency
        [3] Back
        """)
