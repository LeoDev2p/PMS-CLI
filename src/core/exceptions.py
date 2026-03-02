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


class DataIntegrityError(ModelsError):
    """Errores causados por datos enviados (el usuario puede corregirlos)"""

    pass


class DatabaseSystemError(ModelsError):
    """Errores técnicos (tablas, bloqueos, sintaxis SQL)"""

    pass


# IntegrityError
class UniqueError(DataIntegrityError):
    """
    Clase para errores de unicidad.
    """

    pass


class NotnullError(DataIntegrityError):
    """
    Clase para errores de no nulidad.
    """

    pass


class ForeingKeyError(DataIntegrityError):
    """
    Clase para errores de clave foránea.
    """

    pass


class CheckError(DataIntegrityError):
    """
    Clase para errores de verificación.
    """

    pass


# OperationalError
class DatabaseLockedError(DatabaseSystemError):
    """
    Clase para errores de bloqueo de base de datos.
    """

    pass


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
class DataNotFoundError(BussinesError):
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


# * excepcion de datos existentes
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


class StatusExistsError(DataExistsError):
    """
    Clase para error de stados existentes
    """

    pass


# excepcion de datos vacios vista -> controller
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
