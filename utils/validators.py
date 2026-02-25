import re
from functools import wraps
from typing import Any

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
        patron = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        )
        if not password:
            log.warning("Password is required")
            raise PasswordError("Password is required")

        if not re.match(patron, password):
            log.warning("Invalid password")
            raise PasswordError(f"invalid password: {password}")

        return func(*args, **kwargs)

    return wrapper


def validation_data_empty(data: Any) -> bool:
    """Validate if the data is empty.

    Args:
        data (any): Data to validate.

    Returns:
        bool: True if the data is not empty, False otherwise.
    """
    if data is None:
        return False

    if isinstance(data, (int, float)):
        return True

    if isinstance(data, str):
        return bool(data.strip())

    if isinstance(data, (list, tuple, set)):
        if not data:
            return False

        return all(validation_data_empty(item) for item in data)

    return bool(data)


def textvalidator(data: str) -> bool:
    """Validate if the data is a valid email.

    Args:
        data (str): Data to validate.

    Returns:
        bool: True if the data is a valid email, False otherwise.
    """
    return True if re.search(r"@[a-zA-Z0-9]+\.[a-zA-Z]+|@{1}", data) else False


# funcion invalida eliminar
def validation_match_status(
    result: list[tuple], data: tuple | list | list[tuple]
) -> list:
    """Validate if the data matches the result.

    Args:
        result (list[tuple]): Result to validate.
        data (tuple | list | list[tuple]): Data to validate.

    Returns:
        list: List of data that matches the result.
    """
    new_result = [r[1] for r in result]
    if isinstance(data, tuple):
        return list(filter(lambda x: x in new_result, data))

    else:
        try:
            new_data = [d[0] for d in data]
            return [i for i in new_data if i in new_result]
        except IndexError:
            return [i for i in data if i in new_result]
