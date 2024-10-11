"""
Todo Item Schema.
This module will contain the schema for a "to do" item schema and enums for the validation
Authors: Kenneth Carmichael (kencar17)
Date: October 10th 2024
Version: 1.0
"""
import datetime
import uuid
from typing import Annotated

import pytz
from fastapi import APIRouter, Query, HTTPException
from pydantic import UUID4
from sqlmodel import select

from app.api.todos.models.todo import Todo
from app.api.todos.schemas.todo_schema import Status, Priority, GetTodo, UpdateTodo
from app.db.database import SessionDep

router = APIRouter(
    prefix="/todos",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def get_todos(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100, username: UUID4 = None, status: Status = None, priority: Priority = None) -> list[Todo]:
    """
    Retrieve a list of all to-do items for a specific user. This endpoint takes as input a user identifier, queries
    the database for all to-do items associated with this user and returns them in a structured format. Each to-do
    item contains details such as the task description, its status (completed or in progress), the creation date and
    the completed date.
    """
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()

    return todos


@router.post("")
async def create_todo(todo_data: Todo, session: SessionDep) -> Todo:
    """
    Create a new to-do item for a specific user. This endpoint takes as input a user identifier, a task description,
    and an optional due date. It creates a new to-do item in the database with these details, setting the status
    of the task to 'not started' by default and automatically recording the creation date. A dictionary representing
    the created to-do item. The dictionary contains fields like 'todo_id', 'description', 'status',
    'creation_date', 'due_date'.
    """
    todo_data.id = uuid.uuid4()
    todo_data.creation_date = datetime.datetime.now(tz=pytz.utc)

    session.add(todo_data)
    session.commit()
    session.refresh(todo_data)
    return todo_data


@router.get("/{todo_id}")
async def get_todo(todo_id: UUID4, session: SessionDep) -> Todo:
    """
    Retrieve a specific to-do item for a particular user. This endpoint accepts a user identifier and a task
    identifier as input. It queries the database for the specified to-do item associated with the given user
    and returns it in a structured format. The returned to-do item includes details such as the task description,
    its status (completed or not started), the creation date, and the due date.
    """
    record = session.get(Todo, todo_id)
    if not record:
        raise HTTPException(status_code=404, detail="Todo not found")

    return record


@router.put("/{todo_id}")
async def update_todo(todo_id: UUID4, todo_data: UpdateTodo) -> GetTodo:
    """
    Update the details of a specific to-do item for a certain user. This endpoint accepts a user identifier, a
    task identifier, and optionally a new task description, a status, and a due date. It locates the specified
    to-do item in the database and updates its details according to the provided parameters. The returned to-do
    item includes the updated to-do item, with fields like 'todo_id', 'description', 'status', 'creation_date',
    'due_date'.
    """
    return GetTodo(id=uuid.uuid4(), creation_date=datetime.datetime.now(), status=Status.not_started, priority=Priority.low, description="New One", completed_date=None)


@router.delete("/{todo_id}")
async def delete_todo(todo_id: UUID4, session: SessionDep) -> dict:
    """
    Delete a specific to-do item for a particular user. This endpoint accepts a user identifier and a task
    identifier as input. It locates and deletes the specified to-do item from the database. If the deletion is
    successful, it returns a confirmation message indicating that the to-do item has been successfully deleted.
    """
    record = session.get(Todo, todo_id)

    if not record:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(record)
    session.commit()

    return {"status": "success", "message": f"{todo_id} has been deleted."}
