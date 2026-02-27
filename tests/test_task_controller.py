from unittest.mock import MagicMock

import pytest

from src.controllers.task_controller import TaskController, TaskStatusController
from src.core.exceptions import DataEmptyError


# ═══════════════════════════════════════════════════════════
#  TaskController
# ═══════════════════════════════════════════════════════════
class TestTaskController:
    """Tests for TaskController class."""

    @pytest.fixture
    def controller(self):
        service = MagicMock()
        return TaskController(service)

    # ── get_by_user ─────────────────────────────────────────
    def test_get_by_user_delegates_to_service(self, controller):
        controller.service.fetch_by_user.return_value = [{"title": "t1"}]

        result = controller.get_by_user(1)

        controller.service.fetch_by_user.assert_called_once_with(1)
        assert result == [{"title": "t1"}]

    # ── get_by_project_and_title ────────────────────────────
    def test_get_by_project_and_title_validates_not_empty(self, controller):
        with pytest.raises(DataEmptyError):
            controller.get_by_project_and_title(("", ""))

    def test_get_by_project_and_title_delegates(self, controller):
        controller.service.fetch_by_project_and_title.return_value = {"title": "t1"}

        result = controller.get_by_project_and_title(("proj", "task"))

        assert result["title"] == "t1"

    # ── get_details_by_project ──────────────────────────────
    def test_get_details_by_project_validates_not_empty(self, controller):
        with pytest.raises(DataEmptyError):
            controller.get_details_by_project(None)

    def test_get_details_by_project_delegates(self, controller):
        controller.service.fetch_details_by_project.return_value = [{"id": 1}]

        result = controller.get_details_by_project(1)

        assert result == [{"id": 1}]

    # ── add ─────────────────────────────────────────────────
    def test_add_validates_required_fields(self, controller):
        with pytest.raises(DataEmptyError):
            controller.add(("", None, None, None))

    def test_add_delegates_to_service(self, controller):
        controller.add(("Title", "desc", 1, 2))

        controller.service.create.assert_called_once()

    # ── edit_status ─────────────────────────────────────────
    def test_edit_status_validates_not_empty(self, controller):
        with pytest.raises(DataEmptyError):
            controller.edit_status(None, None, None)

    def test_edit_status_delegates(self, controller):
        controller.edit_status(2, 1, 10)

        controller.service.modify_status.assert_called_once_with(2, 1, 10)

    # ── edit_assigned_user ──────────────────────────────────
    def test_edit_assigned_user_validates_not_empty(self, controller):
        with pytest.raises(DataEmptyError):
            controller.edit_assigned_user(("", "", ""))

    def test_edit_assigned_user_delegates(self, controller):
        controller.edit_assigned_user((1, 5, 10))

        controller.service.modify_assigned_user.assert_called_once_with((1, 5, 10))


# ═══════════════════════════════════════════════════════════
#  TaskStatusController
# ═══════════════════════════════════════════════════════════
class TestTaskStatusController:
    """Tests for TaskStatusController class."""

    @pytest.fixture
    def controller(self):
        service = MagicMock()
        return TaskStatusController(service)

    def test_get_all_delegates(self, controller):
        controller.service.fetch_all.return_value = [{"id": 1, "name": "pending"}]

        result = controller.get_all()

        assert result == [{"id": 1, "name": "pending"}]

    def test_add_validates_not_empty(self, controller):
        with pytest.raises(DataEmptyError):
            controller.add([])

    def test_add_delegates(self, controller):
        controller.add([("status", 1)])

        controller.service.create.assert_called_once()

    def test_add_default_delegates(self, controller):
        controller.add_default()

        controller.service.create_default.assert_called_once()

    def test_edit_validates_not_empty(self, controller):
        with pytest.raises(DataEmptyError):
            controller.edit((1, ""))

    def test_edit_delegates(self, controller):
        controller.edit((1, "new name"))

        controller.service.modify.assert_called_once_with("new name", 1)

    def test_delete_validates_not_empty(self, controller):
        with pytest.raises(DataEmptyError):
            controller.delete(None)

    def test_delete_delegates(self, controller):
        controller.delete(1)

        controller.service.remove.assert_called_once_with(1)
