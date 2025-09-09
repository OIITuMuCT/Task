import datetime
from ninja import Schema, ModelSchema, Field

# from django.contrib.auth.models import User

from .models import Task

class TaskSchemaIn(ModelSchema):
    title: str = Field(..., example="Enhanced Satellite Data Analisis")
    description: str = Field(..., example="Develop a comprehensive analytical model to process")

    class Config:
        description = "Schema for creating a new task"
        model = Task
        model_fields = ["title", "description"]
        model_fields_optional = ["status"]

class TaskSchemaOut(ModelSchema):
    # owner: UserSchema | None = Field(None)
    class Config:
        model = Task
        model_fields = ['title', 'description']

class CreateSchemaOut(Schema):
    id: int = Field(..., example=1)

class PathDate(Schema):
    year: int
    month: int
    day: int

    def value(self):
        return datetime.date(self.year, self.month, self.day)

