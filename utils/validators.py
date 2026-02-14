import re
from functools import wraps

from src.core.exceptions import EmailError, PasswordError


def validation_email(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        email = args[0] if args else kwargs.get("email")
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not email or not re.match(patron, str(email)):
            raise EmailError(f"Email invalido: {email}")

        return func(*args, **kwargs)
    return wrapper

def validation_password(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        password = args[0] if args else kwargs.get("password")
        patron = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

        if not password or not re.match(patron, str(password)):
            raise PasswordError(f"Password invalido: {password}")

        return func(*args, **kwargs)
    return wrapper
