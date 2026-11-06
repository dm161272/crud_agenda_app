import reflex as rx
from pydantic import ValidationError

from crud_agenda_app.db.schemas.task import TaskCreateDTO, TaskDTO, TaskUpdateDTO
from crud_agenda_app.services import task_service


class TaskState(rx.State):
    tasks: list[TaskDTO] = []
    error: str = ""

    dialog_open: bool = False
    editing_id: int = 0
    form_title: str = ""
    form_description: str = ""
    form_priority: str = "medium"
    form_due_date: str = ""

    @rx.event
    def load(self):
        self.tasks = task_service.list_tasks()

    @rx.event
    def set_dialog_open(self, value: bool):
        self.dialog_open = value
        if not value:
            self.error = ""

    @rx.event
    def open_new(self):
        self.editing_id = 0
        self.form_title = ""
        self.form_description = ""
        self.form_priority = "medium"
        self.form_due_date = ""
        self.error = ""
        self.dialog_open = True

    @rx.event
    def open_edit(self, task_id: int):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task is None:
            return
        self.editing_id = task.id
        self.form_title = task.title
        self.form_description = task.description
        self.form_priority = task.priority
        self.form_due_date = task.due_date
        self.error = ""
        self.dialog_open = True

    @rx.event
    def save(self, form: dict):
        data = dict(
            title=form.get("title", "").strip(),
            description=form.get("description", "").strip(),
            priority=form.get("priority", "medium"),
            due_date=form.get("due_date") or None,
        )
        try:
            if self.editing_id:
                task_service.update_task(self.editing_id, TaskUpdateDTO(**data))
            else:
                task_service.create_task(TaskCreateDTO(**data))
        except ValidationError as e:
            self.error = e.errors()[0]["msg"]
            return
        self.error = ""
        self.dialog_open = False
        self.tasks = task_service.list_tasks()

    @rx.event
    def toggle(self, task_id: int, done: bool):
        task_service.update_task(task_id, TaskUpdateDTO(done=done))
        self.tasks = task_service.list_tasks()

    @rx.event
    def delete(self, task_id: int):
        task_service.delete_task(task_id)
        self.tasks = task_service.list_tasks()