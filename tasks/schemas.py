import datetime
from ninja import Schema, ModelSchema, Field, FilterSchema
from pydantic import model_validator
from django.contrib.auth.models import User
from tasks.enums import TaskStatus
from .models import Task

class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "username"]

class TaskSchemaIn(ModelSchema):
    title: str = Field(..., example="Enhanced Satellite Data Analisis")
    description: str = Field(
        ..., example="Develop a comprehensive analytical model to process"
    )

    class Config:
        description = "Schema for creating a new task"
        model = Task
        model_fields = ["title", "description"]
        model_fields_optional = ["status"]


class TaskSchemaOut(ModelSchema):
    # owner: UserSchema | None = Field(None)
    class Config:
        model = Task
        model_fields = ["title", "description"]

class TaskFilterSchema(FilterSchema):
    title: str | None
    status: TaskStatus | None

class CreateSchemaOut(Schema):
    id: int = Field(..., example=1)


class PathDate(Schema):
    year: int = Field(..., ge=1)            # Year must be greater than or equal to 1.
    month: int = Field(..., ge=1, le=12)    # Month must be between 1 and 12.
    day: int = Field(..., ge=1, le=31)      # Day must be between 1 and 31.

    @model_validator(mode="after")
    def validate_date(self) -> "PathDate":
        try:
            return datetime.date(self.year, self.month, self.day)
        except ValueError:
            raise ValueError(
                f"The date {self.year}-{self.month}-{self.day} is not valid."
            )

    def value(self):
        return datetime.date(self.year, self.month, self.day)
