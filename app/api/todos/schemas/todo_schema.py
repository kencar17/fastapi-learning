"""
Todo Item Schema.
This module will contain the schema for a "to do" item schema and enums for the validation
Authors: Kenneth Carmichael (kencar17)
Date: October 10th 2024
Version: 1.0
"""

from datetime import datetime
from enum import Enum

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


class UpdateTodo(BaseModel):
    """
    Update TodoSchema validation model
    """

    description: str
    status: Status
    priority: Priority
    completed_date: datetime | None
