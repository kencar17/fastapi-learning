"""
User Schema.
This module will contain the schema for a user schema and enums for the validation
Authors: Kenneth Carmichael (kencar17)
Date: October 11th 2024
Version: 1.0
"""
import datetime
import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    """User Base Model - Shared Properties"""

    username: EmailStr = Field(unique=True, index=True, max_length=255)
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """
    Create user schema validation model
    """
    password: str = Field(min_length=8, max_length=40)


class ReadUser(UserBase):
    """
    Read user schema validation model
    """
    id: uuid.UUID
    registration_date: datetime.datetime
    last_login: datetime.datetime | None
    email: EmailStr


class UpdateUser(UserBase):
    """
    Update user schema validation model
    """

    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore


class UserRegister(SQLModel):
    """
    User register schema validation model
    """
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    """
    User register schema validation model
    """
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)
