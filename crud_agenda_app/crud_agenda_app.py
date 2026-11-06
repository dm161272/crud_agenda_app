import reflex as rx

from crud_agenda_app.db.base import init_db
from crud_agenda_app.pages.index import index_page
from crud_agenda_app.states.task_state import TaskState

init_db()  # prototype only; replace with Alembic migrations later

app = rx.App(
    theme=rx.theme(appearance="light", accent_color="indigo", radius="medium"),
)

app.add_page(index_page, route="/", title="Agenda", on_load=TaskState.load)