# Excepcion base del proyecto
class ProjectsError(Exception):
    """
    Clase base para todas las excepciones del proyecto.
    """
    pass


# Excepccion superior de manejo de errores de base de datos
class ModelsError(ProjectsError):
    """
    Clase base para todas las excepciones relacionadas con la base de datos.
    """
    pass


# IntegrityError
class UniqueError(ModelsError):
    """
    Clase para errores de unicidad.
    """
    pass


class NotnullError(ModelsError):
    """
    Clase para errores de no nulidad.
    """
    pass


class ForeingKeyError(ModelsError):
    """
    Clase para errores de clave foránea.
    """
    pass


class CheckError(ModelsError):
    """
    Clase para errores de verificación.
    """
    pass


# OperationalError
class DatabaseLockedError(ModelsError):
    """
    Clase para errores de bloqueo de base de datos.
    """
    pass


def handle_sqlite_error(e, sqlite3):
    msg = str(e).lower()

    # --- ERRORES DE INTEGRIDAD (El usuario puede corregirlos) ---
    # -- insert, update
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
    # -- insert select, delete, update
    if isinstance(
        e, (sqlite3.OperationalError, sqlite3.ProgrammingError, sqlite3.DatabaseError)
    ):

        if "database is locked" in msg:
            raise DatabaseLockedError("The file is busy, try again in a moment.")

        # Para todo lo demás (tablas, columnas, sintaxis, bindings)
        raise ModelsError("Technical error in the data server. Contact support.")

    # --- ERROR DESCONOCIDO ---
    raise ProjectsError("An unexpected error has occurred.")


# Excepcion superior de manejo de errores de logica de negocio
# -- conotrollers, views, services
class BussinesError(ProjectsError):
    """
    Clase base para todas las excepciones relacionadas con la lógica de negocio.
    """
    pass

# excepcion de autenticacion
class AuthenticactionError(BussinesError):
    """
    Clase base para todas las excepciones relacionadas con la autenticación.
    """
    pass


class EmailError(AuthenticactionError):
    """
    Clase para errores de correo electrónico.
    """
    pass


class PasswordError(AuthenticactionError):
    """
    Clase para errores de contraseña.
    """
    pass    

class PasswordMatchError(AuthenticactionError):
    """
    Clase para errores de coincidencia de contraseña.
    """
    pass

# excepcion de seguridad
class HashCreatingError(AuthenticactionError):
    """
    Clase para errores de creación de hash.
    """
    pass

class HashInvalidError(AuthenticactionError):
    """
    Clase para errores de hash inválido.
    """
    pass

# excepcion de datos no encontradas
class DataNotFoundError (BussinesError):
    """
    Clase base para todas las excepciones relacionadas con datos no encontrados.
    """
    pass    

class NotFoundTaskError(DataNotFoundError):
    """
    Clase para errores de tareas no encontradas.
    """
    pass

class NotFoundTaskStatusError(DataNotFoundError):
    """
    Clase para errores de estados de tareas no encontrados.
    """
    pass

class NotFoundProjectError(DataNotFoundError):
    """
    Clase para errores de proyectos no encontrados.
    """
    pass

class NotFoundStatusProjectError(DataNotFoundError):
    """
    Clase para errores de estados de proyectos no encontrados.
    """
    pass

class NotFoundUserError(DataNotFoundError):
    """
    Clase para errores de usuarios no encontrados.
    """
    pass

#* excepcion de datos existentes
class DataExistsError(BussinesError):
    """
    Clase base para todas las excepciones relacionadas con datos existentes.
    """
    pass

class ProjectsExistsError(DataExistsError):
    """
    Clase para errores de proyectos existentes.
    """
    pass

# excepcion de datos vacios
class DataEmptyError(BussinesError):
    """
    Clase base para todas las excepciones relacionadas con datos vacíos.
    """
    pass

class EmptyFieldsError(DataEmptyError):
    """
    Clase para errores de campos vacíos.
    """
    pass
