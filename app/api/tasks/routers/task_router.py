"""
Task Router.
This module will contain the router for a "user" endpoint.
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

from app.api.tasks.models.task import Task
from app.api.tasks.schemas.task_schema import Status, Priority, UpdateTask
from app.db.database import SessionDep

router = APIRouter(
    prefix="/tasks",
    tags=["task"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def get_tasks(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100, username: UUID4 = None, status: Status = None, priority: Priority = None) -> list[Task]:
    """
    Retrieve a list of all task for a specific user. This endpoint takes as input a user identifier, queries
    the database for all tasks associated with this user and returns them in a structured format. Each task
    contains details such as the task description, its status (completed or in progress), the creation date and
    the completed date.
    """
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()

    return tasks


@router.post("")
async def create_task(task_data: Task, session: SessionDep) -> Task:
    """
    Create a new task for a specific user. This endpoint takes as input a user identifier, a task description,
    and an optional due date. It creates a new task in the database with these details, setting the status
    of the task to 'not started' by default and automatically recording the creation date. A dictionary representing
    the created task. The dictionary contains fields like 'task_id', 'description', 'status', 'creation_date',
    'due_date'.
    """
    task_data.id = uuid.uuid4()
    task_data.creation_date = datetime.datetime.now(tz=pytz.utc)

    session.add(task_data)
    session.commit()
    session.refresh(task_data)
    return task_data


@router.get("/{task_id}")
async def get_task(task_id: UUID4, session: SessionDep) -> Task:
    """
    Retrieve a specific task for a particular user. This endpoint accepts a user identifier and a task
    identifier as input. It queries the database for the specified task associated with the given user
    and returns it in a structured format. The returned task includes details such as the task description,
    its status (completed or not started), the creation date, and the due date.
    """
    record = session.get(Task, task_id)

    if not record:
        raise HTTPException(status_code=404, detail="Task not found")

    return record


@router.put("/{task_id}")
async def update_task(task_id: UUID4, task_data: UpdateTask, session: SessionDep) -> Task:
    """
    Update the details of a specific task for a certain user. This endpoint accepts a user identifier, a
    task identifier, and optionally a new task description, a status, and a due date. It locates the specified
    task in the database and updates its details according to the provided parameters. The returned task
    item includes the updated task, with fields like 'task_id', 'description', 'status', 'creation_date',
    'due_date'.
    """
    record = session.get(Task, task_id)

    if not record:
        raise HTTPException(status_code=404, detail="Task not found")

    task_clean_data = task_data.model_dump(exclude_unset=True)
    record.sqlmodel_update(task_clean_data)
    session.add(record)
    session.commit()
    session.refresh(record)

    return record


@router.delete("/{task_id}")
async def delete_task(task_id: UUID4, session: SessionDep) -> dict:
    """
    Delete a specific task for a particular user. This endpoint accepts a user identifier and a task
    identifier as input. It locates and deletes the specified to-do item from the database. If the deletion is
    successful, it returns a confirmation message indicating that the task has been successfully deleted.
    """
    record = session.get(Task, task_id)

    if not record:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(record)
    session.commit()

    return {"status": "success", "message": f"{task_id} has been deleted."}
