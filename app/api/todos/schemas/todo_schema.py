"""
Todo Item Schema.
This module will contain the schema for a "to do" item schema and enums for the validation
Authors: Kenneth Carmichael (kencar17)
Date: October 10th 2024
Version: 1.0
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Status(str, Enum):
    """ Status Enum """

    not_started = 'Not Started'
    prioritized = 'Prioritized'
    in_process = 'In Progress'
    testing_qa = 'Testing/QA'
    completed = 'Completed'


class Priority(str, Enum):
    """ Priority Enum """

    extra = 'Extra'
    low = 'Low'
    medium = 'Medium'
    high = 'High'
    extreme = 'Extreme'


class TodoBase(BaseModel):
    """
    TodoBase Schema validation model
    """

    status: Status
    priority: Priority
    description: str


class CreateTodo(TodoBase):
    """
    Create TodoSchema validation model
    """

    pass


class GetTodo(TodoBase):
    """
    Get TodoSchema validation model
    """

    id: UUID
    creation_date: datetime
    completed_date: datetime | None


class UpdateTodo(TodoBase):
    """
    Update TodoSchema validation model
    """

    completed_date: datetime | None
