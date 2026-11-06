import reflex as rx

from crud_agenda_app.db.schemas.task import TaskDTO
from crud_agenda_app.states.task_state import TaskState

PRIORITY_COLOR = {"low": "gray", "medium": "amber", "high": "red"}


def task_row(task: TaskDTO) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.checkbox(
                checked=task.done,
                on_change=lambda v: TaskState.toggle(task.id, v),
            ),
            rx.vstack(
                rx.text(
                    task.title,
                    weight="bold",
                    text_decoration=rx.cond(task.done, "line-through", "none"),
                ),
                rx.cond(task.description != "", rx.text(task.description, size="2", color_scheme="gray")),
                rx.hstack(
                    rx.badge(
                        task.priority,
                        color_scheme=rx.match(
                            task.priority,
                            ("high", "red"),
                            ("medium", "amber"),
                            "gray",
                        ),
                    ),
                    rx.cond(task.due_date != "", rx.badge(task.due_date, variant="outline")),
                    spacing="2",
                ),
                spacing="1",
                align="start",
                flex="1",
            ),
            rx.icon_button(
                rx.icon("pencil"),
                variant="ghost",
                on_click=TaskState.open_edit(task.id),
            ),
            rx.icon_button(
                rx.icon("trash-2"),
                variant="ghost",
                color_scheme="red",
                on_click=TaskState.delete(task.id),
            ),
            align="center",
            spacing="3",
            width="100%",
        ),
        width="100%",
    )


def task_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(rx.cond(TaskState.editing_id > 0, "Edit task", "New task")),
            rx.form(
                rx.vstack(
                    rx.input(
                        name="title",
                        placeholder="Title",
                        default_value=TaskState.form_title,
                        width="100%",
                    ),
                    rx.text_area(
                        name="description",
                        placeholder="Description",
                        default_value=TaskState.form_description,
                        width="100%",
                    ),
                    rx.select(
                        ["low", "medium", "high"],
                        name="priority",
                        default_value=TaskState.form_priority,
                        width="100%",
                    ),
                    rx.input(
                        name="due_date",
                        type="date",
                        default_value=TaskState.form_due_date,
                        width="100%",
                    ),
                    rx.cond(
                        TaskState.error != "",
                        rx.callout(TaskState.error, color_scheme="red", icon="triangle-alert"),
                    ),
                    rx.hstack(
                        rx.dialog.close(rx.button("Cancel", variant="soft", color_scheme="gray", type="button")),
                        rx.button("Save", type="submit"),
                        justify="end",
                        width="100%",
                    ),
                    spacing="3",
                ),
                on_submit=TaskState.save,
                reset_on_submit=False,
            ),
        ),
        open=TaskState.dialog_open,
        on_open_change=TaskState.set_dialog_open,
    )


def index_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("Agenda", size="7"),
                rx.spacer(),
                rx.button(rx.icon("plus"), "New task", on_click=TaskState.open_new),
                width="100%",
                align="center",
            ),
            rx.cond(
                TaskState.tasks.length() > 0,
                rx.vstack(rx.foreach(TaskState.tasks, task_row), spacing="2", width="100%"),
                rx.text("No tasks yet.", color_scheme="gray"),
            ),
            task_dialog(),
            spacing="4",
            width="100%",
        ),
        size="2",
        padding_y="2em",
    )