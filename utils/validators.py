import re
from functools import wraps

from src.core.exceptions import EmailError, PasswordError
from src.core.logging import get_logger

log = get_logger("security", "Validators")

def validation_email(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = args[1] if len(args) > 1 else args[0]

        email = data[0]
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not email:
            log.warning("Email is required")
            raise EmailError("Email is required")

        if not re.match(patron, email):
            log.warning("Invalid email")
            raise EmailError(f"invalid email: {email}")

        return func(*args, **kwargs)
    return wrapper

def validation_password(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = args[1] if len(args) > 1 else args[0]
        password = data[1]
        patron = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if not password:
            log.warning("Password is required")
            raise PasswordError("Password is required")

        if not re.match(patron, password):
            log.warning("Invalid password")
            raise PasswordError(f"invalid password: {password}")

        return func(*args, **kwargs)
    return wrapper

def validation_data_empty(data) -> bool:
    if isinstance(data, (list, tuple)):
        return all(x != "" and not str(x).isspace() for x in data)
    return True if isinstance(data, str) and data != "" and not str(data).isspace() else False
