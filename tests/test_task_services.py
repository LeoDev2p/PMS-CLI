from unittest.mock import MagicMock

import pytest

from src.core.exceptions import (
    DatabaseLockedError,
    ModelsError,
    NotFoundTaskError,
    StatusExistsError,
)
from src.services.task_services import TaskServices, TaskStatusServices


# ═══════════════════════════════════════════════════════════
#  TaskServices
# ═══════════════════════════════════════════════════════════
class TestTaskServices:
    """Tests for TaskServices class."""

    @pytest.fixture
    def service(self):
        task_model = MagicMock()
        up_model = MagicMock()
        return TaskServices(task_model, up_model)

    # ── fetch_by_user ───────────────────────────────────────
    def test_fetch_by_user_returns_list_of_dicts(self, service):
        service.model.get_all_by_user.return_value = [
            ("Task 1", "Description 1", "pendiente", "Project A"),
            ("Task 2", "Description 2", "progreso", "Project B"),
        ]

        result = service.fetch_by_user(1)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == {
            "title": "Task 1",
            "description": "Description 1",
            "status": "pendiente",
            "project": "Project A",
        }

    def test_fetch_by_user_raises_when_no_tasks(self, service):
        service.model.get_all_by_user.return_value = []

        with pytest.raises(NotFoundTaskError):
            service.fetch_by_user(999)

    # ── fetch_by_project_and_title ──────────────────────────
    def test_fetch_by_project_and_title_returns_dict(self, service):
        service.model.get_by_project_and_title.return_value = (
            "task 1",
            "desc",
            "pendiente",
            "project a",
        )

        result = service.fetch_by_project_and_title(("Project A", "Task 1"))

        assert isinstance(result, dict)
        assert result["title"] == "task 1"
        assert result["project"] == "project a"

    def test_fetch_by_project_and_title_raises_when_not_found(self, service):
        service.model.get_by_project_and_title.return_value = None

        with pytest.raises(NotFoundTaskError):
            service.fetch_by_project_and_title(("No Project", "No Task"))

    # ── fetch_details_by_project ────────────────────────────
    def test_fetch_details_by_project_returns_list_of_dicts(self, service):
        service.model.get_details_by_project.return_value = [
            (1, "Task 1", "pendiente", "Project A", "user1"),
            (2, "Task 2", "progreso", "Project A", None),
        ]

        result = service.fetch_details_by_project(1)

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["assigned_to"] == "user1"
        assert result[1]["assigned_to"] is None

    def test_fetch_details_by_project_raises_when_empty(self, service):
        service.model.get_details_by_project.return_value = []

        with pytest.raises(NotFoundTaskError):
            service.fetch_details_by_project(999)

    # ── create ──────────────────────────────────────────────
    def test_create_adds_membership_if_not_exists(self, service):
        service.up_model.exists.return_value = None

        service.create(("title", "desc", 10, 5))

        service.up_model.create.assert_called_once_with(5, 10)
        service.model.create.assert_called_once()

    def test_create_skips_membership_if_exists(self, service):
        service.up_model.exists.return_value = (5, 10)

        service.create(("title", "desc", 10, 5))

        service.up_model.create.assert_not_called()
        service.model.create.assert_called_once()

    def test_create_raises_models_error_on_db_lock(self, service):
        service.up_model.exists.return_value = (5, 10)
        service.model.create.side_effect = DatabaseLockedError("locked")

        with pytest.raises(ModelsError):
            service.create(("title", "desc", 10, 5))

    # ── modify_status ───────────────────────────────────────
    def test_modify_status_calls_model(self, service):
        service.modify_status(2, 1, 10)

        service.model.update_status.assert_called_once_with((2, 1, 10))

    def test_modify_status_raises_on_db_lock(self, service):
        service.model.update_status.side_effect = DatabaseLockedError("locked")

        with pytest.raises(ModelsError):
            service.modify_status(2, 1, 10)

    # ── modify_assigned_user ────────────────────────────────
    def test_modify_assigned_user_removes_and_unassigns(self, service):
        service.modify_assigned_user((1, 5, 10))

        service.up_model.delete.assert_called_once_with((5, 10))
        service.model.update_assigned_user.assert_called_once_with((None, 1))


# ═══════════════════════════════════════════════════════════
#  TaskStatusServices
# ═══════════════════════════════════════════════════════════
class TestTaskStatusServices:
    """Tests for TaskStatusServices class."""

    @pytest.fixture
    def service(self):
        status_model = MagicMock()
        return TaskStatusServices(status_model)

    # ── fetch_all ───────────────────────────────────────────
    def test_fetch_all_returns_list_of_dicts(self, service):
        service.model.get_all.return_value = [
            (1, "pendiente", "PENDING", 1),
            (2, "progreso", "IN_PROGRESS", 1),
        ]

        result = service.fetch_all()

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == {
            "id": 1,
            "name": "pendiente",
            "system_key": "PENDING",
            "is_active": 1,
        }

    def test_fetch_all_raises_when_empty(self, service):
        service.model.get_all.return_value = []

        from src.core.exceptions import NotFoundStatusProjectError

        with pytest.raises(NotFoundStatusProjectError):
            service.fetch_all()

    # ── create ──────────────────────────────────────────────
    def test_create_inserts_with_system_keys(self, service):
        service.model.get_all.return_value = []

        service.create([("nuevo", 1)])

        service.model.create.assert_called_once()
        args = service.model.create.call_args
        assert args[0][0][0] == ("nuevo", "PENDING", 1)

    def test_create_raises_on_duplicate(self, service):
        service.model.get_all.return_value = [
            (1, "pendiente", "PENDING", 1),
        ]

        with pytest.raises(StatusExistsError):
            service.create([("pendiente", 1)])

    # ── create_default ──────────────────────────────────────
    def test_create_default_inserts_5_statuses(self, service):
        service.create_default()

        service.model.create.assert_called_once()
        args = service.model.create.call_args
        assert len(args[0][0]) == 5
        assert args[1]["is_many"] is True

    # ── modify ──────────────────────────────────────────────
    def test_modify_normalizes_and_updates(self, service):
        service.modify("NEW NAME", 1)

        service.model.update.assert_called_once_with(("new name", 1))

    # ── remove ──────────────────────────────────────────────
    def test_remove_deletes_status(self, service):
        service.remove(1)

        service.model.delete.assert_called_once_with(1)
