"""
Todo Database Table
This module will contain the database model for a todo item
Authors: Kenneth Carmichael (kencar17)
Date: October 10th 2024
Version: 1.0
"""
import datetime
import uuid
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Todo(SQLModel, table=True):
    """Todo Item"""

    id: uuid.UUID | None = Field(default=None, primary_key=True)
    creation_date: datetime.datetime
    description: str = Field(index=True)
    status: str
    priority: str
    completed_date: datetime.datetime | None = None
