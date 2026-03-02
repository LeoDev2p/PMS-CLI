
import time

from src.core.exceptions import (
    DataEmptyError,
    ModelsError,
    NotFoundProjectError,
    NotFoundStatusProjectError,
    ProjectsExistsError,
)
from src.ui.cli.base import BaseForms, BaseTables, BaseUI
from src.ui.cli.form.project import FormsProjects
from src.ui.cli.menu.admin_menu import AdminMenus
from utils.helpers import ViewHelper


class ManagementProjectViews:
    """Class to manage project views."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        """Runs the project management views."""
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_management_project()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")
            match option:
                case 1:
                    data = FormsProjects.project_forms()
                    try:
                        self.controller.project_status.get_all()

                        try:
                            self.controller.project.add(data)
                            BaseUI.show_message("\nProject successfully added")
                        except (DataEmptyError, ProjectsExistsError, ModelsError) as e:
                            BaseUI.show_error(str(e))
                            if BaseForms.ask_forms("Try again?") == "Y":
                                continue

                    except NotFoundStatusProjectError:
                        BaseUI.show_message("First you need to create the states in 'system setting' or")
                        if BaseForms.ask_forms("Create by default") == "Y":
                            try:
                                self.controller.project.add(data)
                                BaseUI.show_message("Project successfully added")
                            except (DataEmptyError, ProjectsExistsError, ModelsError) as e:
                                BaseUI.show_error(str(e))
                                if BaseForms.ask_forms("Try again?") == "Y":
                                    continue
                        else:
                            BaseUI.show_message("Set status in 'SYSTEM SETTING")

                    except (DataEmptyError, ModelsError) as e:
                        BaseUI.show_error(str(e))
                        if BaseForms.ask_forms("Try again?") == "Y":
                            continue

                    time.sleep(3.2)

                case 2:
                    try:
                        result = self.controller.project.get_all()
                        BaseTables.show_table(result, title="Projects")
                    except (NotFoundProjectError, ModelsError) as e:
                        BaseUI.show_error(str(e))

                    if BaseForms.ask_forms() == "Y":
                        continue

                case 3:
                    self.edit_project()

                case 4:
                    data = FormsProjects.search_project_forms()
                    # hacerlo global esa funcion
                    try:
                        result = self.controller.project.get_by_title(data)
                        BaseTables.show_table(result, title="Projects")
                        id_project = BaseForms.id_forms()

                        if BaseForms.ask_forms(question="Do you want delete?") == "Y":
                            try:
                                self.controller.project.delete(id_project)
                                BaseUI.show_message("\nProject successfully deleted")
                            except (DataEmptyError, ModelsError) as e:
                                BaseUI.show_error(str(e))
                                if BaseForms.ask_forms() == "Y":
                                    continue
                        else:
                            BaseUI.show_message("\nAction canceled")
                    except (DataEmptyError, NotFoundProjectError, ModelsError) as e:
                        BaseUI.show_error(str(e))
                        if BaseForms.ask_forms() == "Y":
                            continue
                    
                    time.sleep(3.2)

                case 5:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")

    def edit_project(self):
        """Edits a project."""
        while True:
            ViewHelper.clear_screen()
            BaseUI.banner()
            AdminMenus.menu_edit_project()

            option = BaseForms.option_forms()
            BaseUI.show_message("\n")

            match option:
                case 1:
                    try:
                        search = BaseForms.search_forms("Search project")
                        result = self.controller.project.get_all(search)
                        BaseTables.show_table(result, title="Projects")

                        try:
                            data = FormsProjects.edit_project_forms()

                            if BaseForms.ask_forms(question="Do you want edit?") == "Y":
                                self.controller.project.edit_title(data)
                                BaseUI.show_message("\nProject title successfully updated")
                            else:
                                BaseUI.show_message("\nAction canceled")
                        except (DataEmptyError, ModelsError) as e:
                            BaseUI.show_error(str(e))
                            if BaseForms.ask_forms() == "Y":
                                continue

                    except (DataEmptyError, NotFoundProjectError, ModelsError) as e:
                        BaseUI.show_error(str(e))
                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 2:
                    try:
                        search = BaseForms.search_forms("Search project")
                        result = self.controller.project.get_all(search)
                        BaseTables.show_table(result, title="Projects")
                        id_project = BaseForms.id_forms()

                        try:
                            result = self.controller.project_status.get_all()
                            BaseTables.show_table(result, title="Projects")
                            id_status = BaseForms.id_forms()

                            try:
                                data = (id_status, id_project)
                                if BaseForms.ask_forms(question="Do you want edit?") == "Y":
                                    self.controller.project.edit_status(data)
                                    BaseUI.show_message("Project status successfully updated")
                                else:
                                    BaseUI.show_message("\nAction canceled")
                            except (DataEmptyError, ModelsError) as e:
                                BaseUI.show_error(str(e))
                                if BaseForms.ask_forms() == "Y":
                                    continue

                        except (DataEmptyError, NotFoundStatusProjectError, ModelsError) as e:
                            BaseUI.show_error(str(e))
                            if BaseForms.ask_forms() == "Y":
                                continue

                    except (DataEmptyError, NotFoundProjectError, ModelsError) as e:
                        BaseUI.show_error(str(e))
                        if BaseForms.ask_forms() == "Y":
                            continue

                    time.sleep(3.2)

                case 3:
                    break
                case _:
                    BaseUI.show_message("\nInvalid option")
