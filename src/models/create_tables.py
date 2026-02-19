from .sqlite import BaseModels


class CreateTables(BaseModels):
    def _table_user(self):
        query = """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'user')),
            create_by TEXT DEFAULT (CURRENT_DATE)
            )
        """

        self._execute_query(query)

    def _table_projects_status(self):
        query = """
            CREATE TABLE IF NOT EXISTS projects_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            )
        """

        self._execute_query(query)

    def _table_projects(self):
        query = """
            CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            description TEXT,
            id_admin INTEGER NOT NULL,
            id_status INTEGER NOT NULL DEFAULT (1),
            create_at TEXT DEFAULT (CURRENT_DATE),

            FOREIGN KEY (id_admin) REFERENCES users(id),
            FOREIGN KEY (id_status) REFERENCES projects_status(id)
            )
        """

        self._execute_query(query)

    def _table_users_projects(self):
        query = """
            CREATE TABLE IF NOT EXISTS users_projects (
            id_users INTEGER NOT NULL,
            id_projects INTEGER NOT NULL,

            PRIMARY KEY (id_users, id_projects), --Llave compuesta
            FOREIGN key (id_users) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN key (id_projects) REFERENCES projects(id) ON DELETE CASCADE
            )
        """

        self._execute_query(query)

    def _table_task_status(self):
        query = """
            CREATE TABLE IF NOT EXISTS task_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            )
        """

        self._execute_query(query)

    def _table_task(self):
        query = """
            CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            id_status INTEGER NOT NULL,
            id_projects INTEGER NOT NULL,
            id_assigned_to INTEGER NOT NULL,

            FOREIGN key (id_status) REFERENCES task_status(id),
            FOREIGN KEY (id_projects) REFERENCES projects(id) ON DELETE CASCADE,
            FOREIGN KEY (id_assigned_to) REFERENCES users(id)
            )
        """

        self._execute_query(query)

    def create_all_tables(self):
        self._table_user()
        self._table_projects_status()
        self._table_projects()
        self._table_users_projects()
        self._table_task_status()
        self._table_task()
