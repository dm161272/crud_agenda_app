from sqlalchemy import select

from crud_agenda_app.db.base import SessionLocal
from crud_agenda_app.db.models.task import Task
from crud_agenda_app.db.schemas.task import TaskCreateDTO, TaskDTO, TaskUpdateDTO


def _to_dto(t: Task) -> TaskDTO:
    return TaskDTO.model_validate(t)


def list_tasks() -> list[TaskDTO]:
    with SessionLocal() as s:
        rows = s.scalars(select(Task).order_by(Task.created_at.desc())).all()
        return [_to_dto(r) for r in rows]


def create_task(dto: TaskCreateDTO) -> TaskDTO:
    with SessionLocal.begin() as s:
        task = Task(**dto.model_dump())   # dates stay date objects, enum already a str
        s.add(task)
        s.flush()
        s.refresh(task)
        return _to_dto(task)


def update_task(task_id: int, dto: TaskUpdateDTO) -> TaskDTO:
    with SessionLocal.begin() as s:
        task = s.get(Task, task_id)
        if task is None:
            raise LookupError(f"Task {task_id} not found")
        for key, value in dto.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        s.flush()
        s.refresh(task)
        return _to_dto(task)


def delete_task(task_id: int) -> None:
    with SessionLocal.begin() as s:
        task = s.get(Task, task_id)
        if task is not None:
            s.delete(task)