from rich.console import Console

console = Console()


class AuthMenus:
    """
    Class to manage auth menus.
    """

    @staticmethod
    def menu():
        console.print("""
            [bold sky_blue3]────────────── AUTHENTICATION ──────────────[/bold sky_blue3]

            [bold sky_blue3][1][/bold sky_blue3] Login      [bold sky_blue3][2][/bold sky_blue3] Register      [bold grey50][3] Back[/bold grey50]
        """)
