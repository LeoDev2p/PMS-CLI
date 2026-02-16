-- 1. Tabla maestra
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('Admin', 'User')),
     create_by TEXT DEFAULT (CURRENT_DATE)
);

CREATE TABLE IF NOT EXISTS projects_status (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL
	-- 'Activo', 'Pausado', 'Finalizado'
);

-- 2. Proyectos
CREATE TABLE IF NOT EXISTS projects (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL UNIQUE,
	description TEXT,
	id_admin INTEGER NOT NULL,
	id_status INTEGER NOT NULL,
	create_at TEXT DEFAULT (CURRENT_DATE),
	
	FOREIGN KEY (id_admin) REFERENCES users(id),
	FOREIGN KEY (id_status) REFERENCES projects_status(id)
);

-- 3. Tabla intermedia (proyectos - usuarios)
CREATE TABLE IF NOT EXISTS users_projects (
	id_users INTEGER NOT NULL,
	id_projects INTEGER NOT NULL,
	
	PRIMARY KEY (id_users, id_projects), --Llave compuesta
	FOREIGN key (id_users) REFERENCES users(id) ON DELETE CASCADE,
	FOREIGN key (id_projects) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS task_status (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL
	-- Culimnado, En proceso, Pausado
);

-- 4. Tareas
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
);
