"""
Task Database Table
This module will contain the database model for a task item
Authors: Kenneth Carmichael (kencar17)
Date: October 10th 2024
Version: 1.0
"""
import datetime
import uuid

from pydantic import EmailStr
from sqlmodel import Field

from app.api.users.schemas.user_schema import UserBase


class User(UserBase, table=True):
    """User Model"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    registration_date: datetime.datetime
    last_login: datetime.datetime | None = None
    email: EmailStr = Field(max_length=255)
