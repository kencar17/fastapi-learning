"""
Todo Item Schema.
This module will contain the schema for a "to do" item schema and enums for the validation
Authors: Kenneth Carmichael (kencar17)
Date: October 10th 2024
Version: 1.0
"""
import datetime
import uuid

from fastapi import APIRouter
from pydantic import UUID4

from app.api.todos.schemas.todo_schema import Status, Priority, GetTodo, UpdateTodo, CreateTodo

router = APIRouter(
    prefix="/todos",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def get_todos(username: UUID4 = None, status: Status = None, priority: Priority = None) -> list[GetTodo]:
    """
    Retrieve a list of all to-do items for a specific user. This endpoint takes as input a user identifier, queries
    the database for all to-do items associated with this user and returns them in a structured format. Each to-do
    item contains details such as the task description, its status (completed or in progress), the creation date and
    the completed date.
    """
    return [
        GetTodo(id=uuid.UUID("bb673bb6-ee2e-4664-81af-56d49f17b8bb"), creation_date=datetime.datetime.now(), status=Status.completed, priority=Priority.extreme, description="Am a Todo one", completed_date=None),
        GetTodo(id=uuid.UUID("89f29588-02df-4a25-a426-80c310cc1532"), creation_date=datetime.datetime.now(), status=Status.testing_qa, priority=Priority.high, description="Am a Todo two", completed_date=None),
        GetTodo(id=uuid.UUID("f7774da0-5520-4d7d-9726-969ce27106c2"), creation_date=datetime.datetime.now(), status=Status.in_process, priority=Priority.medium, description="Am a Todo three", completed_date=None),
        GetTodo(id=uuid.UUID("96cbb9f8-d02d-4d5a-9a48-2ab2c0b8f6f1"), creation_date=datetime.datetime.now(), status=Status.prioritized, priority=Priority.low, description="Am a Todo four", completed_date=None),
    ]


@router.post("")
async def create_todo(todo_data: CreateTodo) -> GetTodo:
    """
    Create a new to-do item for a specific user. This endpoint takes as input a user identifier, a task description,
    and an optional due date. It creates a new to-do item in the database with these details, setting the status
    of the task to 'not started' by default and automatically recording the creation date. A dictionary representing
    the created to-do item. The dictionary contains fields like 'todo_id', 'description', 'status',
    'creation_date', 'due_date'.
    """
    return GetTodo(id=uuid.uuid4(), creation_date=datetime.datetime.now(), status=Status.not_started, priority=Priority.low, description="New One", completed_date=None)


@router.get("/{todo_id}")
async def get_todo(todo_id: UUID4) -> GetTodo:
    """
    Retrieve a specific to-do item for a particular user. This endpoint accepts a user identifier and a task
    identifier as input. It queries the database for the specified to-do item associated with the given user
    and returns it in a structured format. The returned to-do item includes details such as the task description,
    its status (completed or not started), the creation date, and the due date.
    """
    return GetTodo(id=uuid.uuid4(), creation_date=datetime.datetime.now(), status=Status.not_started, priority=Priority.low, description="New One", completed_date=None)


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
async def delete_todo(todo_id: UUID4) -> dict:
    """
    Delete a specific to-do item for a particular user. This endpoint accepts a user identifier and a task
    identifier as input. It locates and deletes the specified to-do item from the database. If the deletion is
    successful, it returns a confirmation message indicating that the to-do item has been successfully deleted.
    """
    return {"status": "success", "message": f"{todo_id} has been deleted."}
