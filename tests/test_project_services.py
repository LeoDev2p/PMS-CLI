from unittest.mock import MagicMock, patch

import pytest

from src.core.exceptions import (
    NotFoundProjectError,
    NotFoundStatusProjectError,
    ProjectsExistsError,
)
from src.services.project_services import (
    ProjectServices,
    ProjectStatusServices,
    UserProjectServices,
)


# ═══════════════════════════════════════════════════════════
#  ProjectServices
# ═══════════════════════════════════════════════════════════
class TestProjectServices:
    """Tests for ProjectServices class."""

    @pytest.fixture
    def service(self):
        project_model = MagicMock()
        status_model = MagicMock()
        return ProjectServices(project_model, status_model)

    # ── fetch_all ───────────────────────────────────────────
    def test_fetch_all_returns_list_of_dicts(self, service):
        service.model.get_all.return_value = [
            (1, "Project A", "new"),
            (2, "Project B", "active"),
        ]

        result = service.fetch_all()

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == {"id": 1, "title": "Project A", "status": "new"}
        assert result[1] == {"id": 2, "title": "Project B", "status": "active"}

    def test_fetch_all_raises_when_no_projects(self, service):
        service.model.get_all.return_value = []

        with pytest.raises(NotFoundProjectError):
            service.fetch_all()

    # ── fetch_by_title ──────────────────────────────────────
    def test_fetch_by_title_returns_list_of_dicts(self, service):
        service.model.get_by_title.return_value = [(1, "test project")]

        result = service.fetch_by_title("test")

        assert result == [{"id": 1, "title": "test project"}]

    def test_fetch_by_title_raises_when_not_found(self, service):
        service.model.get_by_title.return_value = []

        with pytest.raises(NotFoundProjectError):
            service.fetch_by_title("nonexistent")

    # ── fetch_search_by_title ───────────────────────────────
    def test_fetch_search_by_title_returns_dicts_with_description(self, service):
        service.model.search_by_title.return_value = [
            (1, "Project A", "Description A"),
        ]

        result = service.fetch_search_by_title("project")

        assert result[0]["description"] == "Description A"

    # ── fetch_count_by_title ────────────────────────────────
    def test_fetch_count_by_title_returns_integer(self, service):
        service.model.count_by_title.return_value = (5,)

        result = service.fetch_count_by_title("test")

        assert result == 5

    def test_fetch_count_by_title_returns_zero_when_none(self, service):
        service.model.count_by_title.return_value = None

        result = service.fetch_count_by_title("nonexistent")

        assert result == 0

    # ── fetch_new ───────────────────────────────────────────
    def test_fetch_new_returns_list_of_dicts(self, service):
        service.model.get_new.return_value = [
            (1, "New Project", "NEW"),
        ]

        result = service.fetch_new()

        assert result == [{"id": 1, "title": "New Project", "system_key": "NEW"}]

    # ── fetch_new_active ────────────────────────────────────
    def test_fetch_new_active_returns_list_of_dicts(self, service):
        service.model.get_new_active.return_value = [
            (1, "Project A"),
            (2, "Project B"),
        ]

        result = service.fetch_new_active()

        assert len(result) == 2
        assert result[0] == {"id": 1, "title": "Project A"}

    # ── create ──────────────────────────────────────────────
    @patch("src.services.project_services.Session")
    def test_create_project_success(self, mock_session, service):
        mock_session.get_id.return_value = 1
        service.model.get_by_title.return_value = []
        service.status_model.get_all.return_value = [(1, "new", "NEW", 1)]
        service.status_model.get_default_id.return_value = (1,)

        service.create(("New Project", "A description"))

        service.model.create.assert_called_once()

    @patch("src.services.project_services.Session")
    def test_create_project_raises_when_exists(self, mock_session, service):
        mock_session.get_id.return_value = 1
        service.model.get_by_title.return_value = [(1, "existing")]

        with pytest.raises(ProjectsExistsError):
            service.create(("existing", "desc"))

    @patch("src.services.project_services.Session")
    def test_create_project_creates_default_status_if_none(self, mock_session, service):
        mock_session.get_id.return_value = 1
        service.model.get_by_title.return_value = []
        service.status_model.get_all.return_value = []
        service.status_model.get_default_id.return_value = (1,)

        service.create(("Project", "desc"))

        # Should create defaults first, then create the project
        service.status_model.create.assert_called_once()
        service.model.create.assert_called_once()

    # ── modify_title ────────────────────────────────────────
    @patch("src.services.project_services.Session")
    def test_modify_title_normalizes_and_updates(self, mock_session, service):
        mock_session.get_id.return_value = 1

        service.modify_title(("NEW TITLE", 1))

        service.model.update_title.assert_called_once_with(("new title", 1))

    # ── modify_status ───────────────────────────────────────
    def test_modify_status_calls_model(self, service):
        service.modify_status((2, 1))

        service.model.update_status.assert_called_once_with((2, 1))

    # ── remove ──────────────────────────────────────────────
    @patch("src.services.project_services.Session")
    def test_remove_deletes_project(self, mock_session, service):
        mock_session.get_id.return_value = 1

        service.remove(1)

        service.model.delete.assert_called_once_with(1)


# ═══════════════════════════════════════════════════════════
#  ProjectStatusServices
# ═══════════════════════════════════════════════════════════
class TestProjectStatusServices:
    """Tests for ProjectStatusServices class."""

    @pytest.fixture
    def service(self):
        status_model = MagicMock()
        return ProjectStatusServices(status_model)

    def test_fetch_all_returns_list_of_dicts(self, service):
        service.model.get_all.return_value = [
            (1, "new", "NEW", 1),
            (2, "active", "ACTIVE", 1),
        ]

        result = service.fetch_all()

        assert len(result) == 2
        assert result[0] == {
            "id": 1,
            "name": "new",
            "system_key": "NEW",
            "is_active": 1,
        }

    def test_fetch_all_raises_when_empty(self, service):
        service.model.get_all.return_value = []

        with pytest.raises(NotFoundStatusProjectError):
            service.fetch_all()

    def test_create_default_inserts_5_statuses(self, service):
        service.create_default()

        service.model.create.assert_called_once()
        args = service.model.create.call_args
        assert len(args[0][0]) == 5

    def test_remove_deletes_status(self, service):
        service.remove(1)

        service.model.delete.assert_called_once_with(1)


# ═══════════════════════════════════════════════════════════
#  UserProjectServices
# ═══════════════════════════════════════════════════════════
class TestUserProjectServices:
    """Tests for UserProjectServices class."""

    @pytest.fixture
    def service(self):
        up_model = MagicMock()
        return UserProjectServices(up_model)

    def test_create_adds_membership(self, service):
        service.create((1, 10))

        service.model.create_many.assert_called_once_with([(1, 10)])
