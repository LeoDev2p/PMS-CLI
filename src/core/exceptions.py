# Excepcion base del proyecto
class ProjectsError (Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# Excepccion de manejo de errores de base de datos
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
    if isinstance(e, sqlite3.IntegrityError):
        if "unique" in msg:
            raise UniqueError("Este registro ya existe.")
        if "not null" in msg:
            raise NotnullError("Hay campos obligatorios vacíos.")
        if "foreign key" in msg:
            raise ForeingKeyError("El recurso relacionado no existe.")
        if "check" in msg:
            raise CheckError("Los datos no cumplen con las reglas de validación.")

        raise ModelsError(f"Error de integridad: {msg}")

    # --- ERRORES OPERATIVOS Y DE PROGRAMACIÓN (Bugs del desarrollador) ---
    if isinstance(e, (sqlite3.OperationalError, sqlite3.ProgrammingError, sqlite3.DatabaseError)):
        log_error.critical(f"Database Technical Error: {msg}")

        if "database is locked" in msg:
            raise DatabaseLockedError("El archivo está ocupado, reintenta en un momento.")

        # Para todo lo demás (tablas, columnas, sintaxis, bindings)
        raise ModelsError("Error técnico en el servidor de datos. Contacte a soporte.")

    # --- ERROR DESCONOCIDO ---
    log_error.error(f"Unknown DB Error: {msg}")
    raise ProjectsError("Ha ocurrido un error inesperado.")


# Excepcion de manejo de errores de logica de negocio
class BussinesError(ProjectsError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class AuthError(BussinesError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class EmailError(AuthError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PasswordError(AuthError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)