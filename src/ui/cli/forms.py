class Forms:
    @staticmethod
    def login_forms() -> tuple:
        email = input("[email]: ").strip()
        password = input("[password]: ").strip()
        return email, password

    @staticmethod
    def register_forms() -> tuple:
        username = input("[username]: ").strip()
        email = input("[email]: ").strip()
        password = input("[password]: ").strip()
        return email, password, username


    @staticmethod
    def option_forms():
        try:
            option = int(input("option: "))
            return option
        except ValueError as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def show_message(message):
        print(message)

    @staticmethod
    def show_error(message):
        print(message)

    @staticmethod
    def banner():
        print(r"""
         ██▓███   ███▄ ▄███▓  ██████  ▄████▄   ██▓     ██▓
        ▓██░  ██▒▓██▒▀█▀ ██▒▒██    ▒ ▒██▀ ▀█  ▓██▒    ▓██▒
        ▓██░ ██▓▒▓██    ▓██░░ ▓██▄   ▒▓█    ▄ ▒██░    ▒██▒
        ▒██▄█▓▒ ▒▒██    ▒██   ▒   ██▒▒▓▓▄ ▄██▒▒██░    ░██░
        ▒██▒ ░  ░▒██▒   ░██▒▒██████▒▒▒ ▓███▀ ░░██████▒░██░
        ▒▓▒░ ░  ░░ ▒░   ░  ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒░▓  ░░▓  
        ░▒ ░     ░  ░      ░░ ░▒  ░ ░  ░  ▒   ░ ░ ▒  ░ ▒ ░
        ░░       ░      ░   ░  ░  ░  ░          ░ ░    ▒ ░
                ░         ░  ░ ░          ░  ░ ░  
                             ░                  By LeoDev2p    
        """)
    
    def ask_forms(question = "Do you want to continue?"):
        try:
            ask = input(f"{question} (S/N): ").upper()
        except Exception as e:
            print(f"Error: {e}")
            return None
        return ask
