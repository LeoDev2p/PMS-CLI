-- por tareas
SELECT t.title, t.description, ts.name, p.title FROM task t
JOIN task_status ts ON t.id_status = ts.id
JOIN projects p ON t.id_projects = p.id
WHERE t.id_assigned_to = ?;

-- actualizar estado de tarea

UPDATE task
SET id_status = (SELECT id FROM task_status WHERE name = 'Cancelado')
WHERE title = 'Front-end' AND id_projects = (
	SELECT id FROM projects WHERE title = 'IQ GeoSpatial'
);

SELECT id FROM task_status WHERE name = ?
SELECT id FROM projects WHERE title = ?

UPDATE task
set id_status = ?
WHERE title = ? AND id_projects = ?

-- mi Perfil

SELECT username, email, password_hash FROM users
WHERE id = ?

UPDATE users
SET username = ?, password_hash = ?
WHERE id = ?
