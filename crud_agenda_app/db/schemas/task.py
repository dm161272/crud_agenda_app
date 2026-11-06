from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreateDTO(BaseModel):
    model_config = ConfigDict(use_enum_values=True)  # store "high", not Priority.high

    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    priority: Priority = Priority.medium
    due_date: date | None = None


class TaskUpdateDTO(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: Priority | None = None
    due_date: date | None = None
    done: bool | None = None


class TaskDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: str          # plain str is easier in the frontend than an Enum
    due_date: date | None
    done: bool
    created_at: datetime