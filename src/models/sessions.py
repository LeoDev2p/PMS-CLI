class Session:
    _data = {
        "id": None,
        "role": None,
        "state": False,
        "email": None,
    }

    @classmethod
    def start(cls, id, role, email):
        cls._data["id"] = id
        cls._data["role"] = role
        cls._data["state"] = True
        cls._data["email"] = email

    @classmethod
    def stop(cls):
        cls._data["id"] = None
        cls._data["role"] = None
        cls._data["state"] = False
        cls._data["email"] = None

    @classmethod
    def get_id(cls):
        return cls._data["id"]

    @classmethod
    def get_role(cls):
        return cls._data["role"]

    @classmethod
    def get_state(cls):
        return cls._data["state"]

    @classmethod
    def get_email(cls):
        return cls._data["email"]

