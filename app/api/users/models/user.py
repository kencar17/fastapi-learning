"""
Task Database Table
This module will contain the database model for a task item
Authors: Kenneth Carmichael (kencar17)
Date: October 10th 2024
Version: 1.0
"""
import datetime
import uuid

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User Model"""

    id: uuid.UUID | None = Field(default=None, primary_key=True)
    registration_date: datetime.datetime
    last_login: datetime.datetime | None = None
    username: str
    display_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None
