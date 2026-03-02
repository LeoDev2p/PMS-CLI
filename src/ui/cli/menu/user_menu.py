from rich.console import Console

console = Console()

class UserMenus:
    """
    Class to manage user menus.
    """

    @staticmethod
    def menu():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── USER PANEL ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] My tasks")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Update task status")
        console.print(f"{margin} [bold sky_blue3][3][/bold sky_blue3] My profile")
        console.print(f"{margin} [bold grey50][4] Logout[/bold grey50]")
        console.print("\n")

    @staticmethod
    def menu_edit_profile():
        console.print("\n") 
        margin = " " * 10
        console.print(f"{margin}[bold sky_blue3]──── EDIT PROFILE ────[/bold sky_blue3]")
        console.print(f"{margin} [bold sky_blue3][1][/bold sky_blue3] Edit username")
        console.print(f"{margin} [bold sky_blue3][2][/bold sky_blue3] Edit password")
        console.print(f"{margin} [bold grey50][3] Logout[/bold grey50]")
        console.print("\n")
