# Excepcion base del proyecto
class ProjectsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Excepccion superior de manejo de errores de base de datos
class ModelsError(ProjectsError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# IntegrityError
class UniqueError(ModelsError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotnullError(ModelsError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ForeingKeyError(ModelsError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CheckError(ModelsError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# OperationalError
class DatabaseLockedError(ModelsError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def handle_sqlite_error(e, log_error, sqlite3):
    msg = str(e).lower()

    # --- ERRORES DE INTEGRIDAD (El usuario puede corregirlos) ---
    # -- insert
    if isinstance(e, sqlite3.IntegrityError):
        if "unique" in msg:
            raise UniqueError("This record already exists.")
        if "not null" in msg:
            raise NotnullError("There are required fields that are empty.")
        if "foreign key" in msg:
            raise ForeingKeyError("The related resource does not exist.")
        if "check" in msg:
            raise CheckError("The data does not comply with the validation rules.")

        raise ModelsError(f"integrity error: {msg}")

    # --- ERRORES OPERATIVOS Y DE PROGRAMACIÓN (Bugs del desarrollador) ---
    # -- select, delete, update
    if isinstance(
        e, (sqlite3.OperationalError, sqlite3.ProgrammingError, sqlite3.DatabaseError)
    ):
        log_error.critical(f"Database Technical Error: {msg}")

        if "database is locked" in msg:
            raise DatabaseLockedError("The file is busy, try again in a moment.")

        # Para todo lo demás (tablas, columnas, sintaxis, bindings)
        raise ModelsError("Technical error in the data server. Contact support.")

    # --- ERROR DESCONOCIDO ---
    log_error.error(f"Unknown DB Error: {msg}")
    raise ProjectsError("An unexpected error has occurred.")


# Excepcion superior de manejo de errores de logica de negocio
# -- conotrollers, views, services
class BussinesError(ProjectsError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# excepcion de autenticacion
class AuthenticactionError(BussinesError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EmailError(AuthenticactionError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PasswordError(AuthenticactionError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# excepcion de seguridad
class HashCreatingError(AuthenticactionError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class HashInvalidError(AuthenticactionError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# excepcion de tareas
class NotFoundTaskError(BussinesError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NotFoundTaskStatusError(BussinesError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NotFoundProjectError(BussinesError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
