from rich.console import Console

console = Console()

class AdminMenus:
    """
    Class to manage admin menus.
    """


    @staticmethod
    def menu():
        """Dibuja el menú con márgenes para que no esté pegado al borde."""

        console.print("\n") 
    
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── ADMIN PANEL ────[/bold sky_blue3]")

        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] User management")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Project management")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Statistics panel")
        console.print(f"{margin} [bold grey50][4] Logout[/bold grey50]")

        console.print("\n") 

    # User management
    @staticmethod
    def menu_users():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── USER MANAGEMENT ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Create user")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Edit user")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Delete user")
        console.print(f"{margin} [bold sky_blue3][4][/bold sky_blue3] View users")
        console.print(f"{margin} [bold grey50][5] Back[/bold grey50]")
        console.print("\n")

    @staticmethod
    def menu_edit_users():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── EDIT USER ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Edit username")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Edit email")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Reset password")
        console.print(f"{margin} [bold sky_blue3][4][/bold sky_blue3] Change role")
        console.print(f"{margin} [bold grey50][5] Back[/bold grey50]")
        console.print("\n")

    # ManagementProjectViews
    @staticmethod
    def menu_project():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── ADMIN MANAGEMENT ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Projects")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] System setting")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Operational management")
        console.print(f"{margin} [bold grey50][4] Back[/bold grey50]")
        console.print("\n")


    # Projects
    @staticmethod
    def menu_management_project():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── PROJECT MANAGEMENT ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] New project")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] List projects")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Edit project")
        console.print(f"{margin} [bold sky_blue3][4][/bold sky_blue3] Delete project")
        console.print(f"{margin} [bold grey50][5] Back[/bold grey50]")
        console.print("\n")

    @staticmethod
    def menu_edit_project():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── EDIT PROJECT ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Editing title")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Editing status")
        console.print(f"{margin} [bold grey50][3] Back[/bold grey50]")
        console.print("\n")

    # system setting
    @staticmethod
    def menu_system_setting():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── SYSTEM SETTING ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Managing project states")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Managing task states")
        console.print(f"{margin} [bold grey50][3] Back[/bold grey50]")
        console.print("\n")

    @staticmethod
    def menu_status_projects():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── STATUS PROJECTS ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Create state")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] List states")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Edit state")
        console.print(f"{margin} [bold sky_blue3][4][/bold sky_blue3] Delete state")
        console.print(f"{margin} [bold grey50][5] Back[/bold grey50]")
        console.print("\n")

    @staticmethod
    def menu_status_tasks():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── STATUS TASKS ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Create state")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] List states")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Edit state")
        console.print(f"{margin} [bold sky_blue3][4][/bold sky_blue3] Delete state")
        console.print(f"{margin} [bold grey50][5] Back[/bold grey50]")
        console.print("\n")


    # Gestion operativa
    @staticmethod
    def menu_operational():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── OPERATIONAL ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] New assignment / create task")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Team control / monitoring")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Personnel maintenance")
        console.print(f"{margin} [bold grey50][4] Back[/bold grey50]")
        console.print("\n")


    @staticmethod
    def menu_team_monitoring():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── TEAM MONITORING ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] View Team by Project")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Change Task Status")
        console.print(f"{margin} [bold grey50][3] Back[/bold grey50]")
        console.print("\n")


    @staticmethod
    def menu_personnel_maintenance():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── PERSONNEL MAINTENANCE ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Reassign User")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Remove User")
        console.print(f"{margin} [bold grey50][3] Back[/bold grey50]")
        console.print("\n")


    # Statistics panel
    @staticmethod
    def menu_statistics():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── STATISTICS ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Talent Management (users)")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Health Status (projects)")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Performance and Averages (metrics)")
        console.print(f"{margin} [bold sky_blue3][4][/bold sky_blue3] Critical Control Panel")
        console.print(f"{margin} [bold grey50][5] Back[/bold grey50]")
        console.print("\n")


    @staticmethod
    def menu_talent_management():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── TALENT MANAGEMENT ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Availability counter")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Workload per user")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Productivity ranking")
        console.print(f"{margin} [bold grey50][4] Back[/bold grey50]")
        console.print("\n")


    @staticmethod
    def menu_health_status():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── HEALTH STATUS ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Project progress")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Distribution of states")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] Users per project")
        console.print(f"{margin} [bold grey50][4] Back[/bold grey50]")
        console.print("\n")


    @staticmethod
    def menu_performance_metrics():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── PERFORMANCE METRICS ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Blocking rate")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Completion Efficiency")
        console.print(f"{margin} [bold grey50][3] Back[/bold grey50]")
        console.print("\n")
    
    @staticmethod
    def menu_critical_control_panel():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── CRITICAL CONTROL PANEL ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Orphan Task Alerts")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Critical Projects")
        console.print(f"{margin} [bold grey50][3] Back[/bold grey50]")
        console.print("\n")

