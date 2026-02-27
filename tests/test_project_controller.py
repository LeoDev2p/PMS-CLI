from unittest.mock import MagicMock

import pytest

from src.controllers.project_controller import (
    ProjectController,
    ProjectStatusController,
    UserProjectController,
)
from src.core.exceptions import DataEmptyError


# ═══════════════════════════════════════════════════════════
#  ProjectController
# ═══════════════════════════════════════════════════════════
class TestProjectController:
    """Tests for ProjectController class."""

    @pytest.fixture
    def controller(self):
        service = MagicMock()
        return ProjectController(service)

    # ── get_all ─────────────────────────────────────────────
    def test_get_all_delegates(self, controller):
        controller.service.fetch_all.return_value = [{"id": 1, "title": "p1"}]

        result = controller.get_all()

        assert result == [{"id": 1, "title": "p1"}]

    # ── get_by_title ────────────────────────────────────────
    def test_get_by_title_validates_not_empty(self, controller):
        with pytest.raises(DataEmptyError):
            controller.get_by_title("")

    def test_get_by_title_delegates(self, controller):
        controller.service.fetch_by_title.return_value = [{"id": 1, "title": "p1"}]

        result = controller.get_by_title("p1")

        assert result[0]["title"] == "p1"

    # ── get_search_by_title ─────────────────────────────────
    def test_get_search_by_title_validates(self, controller):
        with pytest.raises(DataEmptyError):
            controller.get_search_by_title("")

    # ── count_by_title ──────────────────────────────────────
    def test_count_by_title_validates(self, controller):
        with pytest.raises(DataEmptyError):
            controller.count_by_title("")

    def test_count_by_title_delegates(self, controller):
        controller.service.fetch_count_by_title.return_value = 3

        result = controller.count_by_title("test")

        assert result == 3

    # ── get_new ─────────────────────────────────────────────
    def test_get_new_delegates(self, controller):
        controller.service.fetch_new.return_value = [{"id": 1}]

        result = controller.get_new()

        assert result == [{"id": 1}]

    # ── get_new_active ──────────────────────────────────────
    def test_get_new_active_delegates(self, controller):
        controller.service.fetch_new_active.return_value = [{"id": 1}]

        result = controller.get_new_active()

        assert result == [{"id": 1}]

    # ── add ─────────────────────────────────────────────────
    def test_add_validates_title_not_empty(self, controller):
        with pytest.raises(DataEmptyError):
            controller.add(("", "desc"))

    def test_add_delegates(self, controller):
        controller.add(("Title", "desc"))

        controller.service.create.assert_called_once_with(("Title", "desc"))

    # ── edit_title ──────────────────────────────────────────
    def test_edit_title_validates(self, controller):
        with pytest.raises(DataEmptyError):
            controller.edit_title(("", 1))

    def test_edit_title_delegates(self, controller):
        controller.edit_title(("New Title", 1))

        controller.service.modify_title.assert_called_once_with(("New Title", 1))

    # ── edit_status ─────────────────────────────────────────
    def test_edit_status_validates(self, controller):
        with pytest.raises(DataEmptyError):
            controller.edit_status(("", ""))

    def test_edit_status_delegates(self, controller):
        controller.edit_status((2, 1))

        controller.service.modify_status.assert_called_once_with((2, 1))

    # ── delete ──────────────────────────────────────────────
    def test_delete_validates(self, controller):
        with pytest.raises(DataEmptyError):
            controller.delete(None)

    def test_delete_delegates(self, controller):
        controller.delete(1)

        controller.service.remove.assert_called_once_with(1)


# ═══════════════════════════════════════════════════════════
#  ProjectStatusController
# ═══════════════════════════════════════════════════════════
class TestProjectStatusController:
    """Tests for ProjectStatusController class."""

    @pytest.fixture
    def controller(self):
        service = MagicMock()
        return ProjectStatusController(service)

    def test_get_all_delegates(self, controller):
        controller.service.fetch_all.return_value = [{"id": 1}]

        result = controller.get_all()

        assert result == [{"id": 1}]

    def test_add_validates(self, controller):
        with pytest.raises(DataEmptyError):
            controller.add([])

    def test_add_delegates(self, controller):
        controller.add([("status", 1)])

        controller.service.create.assert_called_once()

    def test_add_default_delegates(self, controller):
        controller.add_default()

        controller.service.create_default.assert_called_once()

    def test_edit_validates(self, controller):
        with pytest.raises(DataEmptyError):
            controller.edit((1, ""))

    def test_edit_delegates(self, controller):
        controller.edit((1, "new name"))

        controller.service.modify.assert_called_once_with(("new name", 1))

    def test_delete_validates(self, controller):
        with pytest.raises(DataEmptyError):
            controller.delete(None)

    def test_delete_delegates(self, controller):
        controller.delete(1)

        controller.service.remove.assert_called_once_with(1)


# ═══════════════════════════════════════════════════════════
#  UserProjectController
# ═══════════════════════════════════════════════════════════
class TestUserProjectController:
    """Tests for UserProjectController class."""

    @pytest.fixture
    def controller(self):
        service = MagicMock()
        return UserProjectController(service)

    def test_add_validates(self, controller):
        with pytest.raises(DataEmptyError):
            controller.add(("", ""))

    def test_add_delegates(self, controller):
        controller.add((1, 10))

        controller.service.create.assert_called_once_with((1, 10))
