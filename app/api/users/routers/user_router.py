"""
User Router.
This module will contain the router for a "user" endpoint.
Authors: Kenneth Carmichael (kencar17)
Date: October 11th 2024
Version: 1.0
"""
import datetime
import uuid
from typing import Annotated

import pytz
from fastapi import APIRouter, Query, HTTPException
from pydantic import UUID4
from sqlmodel import select

from app.api.users.models.user import User
from app.api.users.schemas.user_schema import UpdateUser
from app.db.database import SessionDep

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def get_user(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100, username: str = None, first_name: str = None, last_name: str = None, email: str = None, is_staff: bool = None, is_superuser: bool = None, is_active: bool = None) -> list[User]:
    """
    Retrieve a list of all users in the system. This endpoint accepts a user identifier as input, queries the
    database for all relevant user details, and returns them in a structured format. Each user record contains
    information such as the user’s name, email, registration date, and account status (active or inactive).
    """
    tasks = session.exec(select(User).offset(offset).limit(limit)).all()

    return tasks


@router.post("")
async def create_user(user_data: User, session: SessionDep) -> User:
    """
    Create a new user in the system. This endpoint accepts user details such as the user’s name, email, and an
    optional registration date. It creates a new user record in the database, setting the account status to ‘active’
    by default and automatically recording the registration date. A dictionary representing the created user is
    returned, containing fields like ‘user_id’, ‘name’, ‘email’, ‘status’, and ‘join_date’.
    """
    user_data.id = uuid.uuid4()
    user_data.registration_date = datetime.datetime.now(tz=pytz.utc)
    user_data.is_active = True

    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data


@router.get("/{user_id}")
async def get_user(user_id: UUID4, session: SessionDep) -> User:
    """
    Retrieve a specific user by their identifier. This endpoint accepts a user identifier as input and queries the
    database for the specified user. It returns the user details in a structured format, including information such
    as the user’s name, email, account status (active or inactive), registration date, and any additional metadata
    associated with the user.
    """
    record = session.get(User, user_id)

    if not record:
        raise HTTPException(status_code=404, detail="Task not found")

    return record


@router.put("/{user_id}")
async def update_user(user_id: UUID4, user_data: UpdateUser, session: SessionDep) -> User:
    """
    Update the details of a specific user. This endpoint accepts a user identifier and optionally new details such
    as the user’s name, email, and account status. It locates the specified user in the database and updates the
    user’s information according to the provided parameters. The returned user object includes the updated fields,
    such as ‘user_id’, ‘name’, ‘email’, ‘status’, and ‘registration_date’.
    """
    record = session.get(User, user_id)

    if not record:
        raise HTTPException(status_code=404, detail="User not found")

    user_clean_data = user_data.model_dump(exclude_unset=True)
    record.sqlmodel_update(user_clean_data)
    session.add(record)
    session.commit()
    session.refresh(record)

    return record


@router.delete("/{user_id}")
async def deactivate_user(user_id: UUID4, session: SessionDep) -> dict:
    """
    Deactivate a specific user from the system. This endpoint accepts a user identifier as input. It locates and
    deactivate the specified user record from the database. If the deletion is successful, it returns a confirmation
    message indicating that the user has been successfully removed.
    """
    record = session.get(User, user_id)

    if not record:
        raise HTTPException(status_code=404, detail="Task not found")

    record.is_active = False

    session.add(record)
    session.commit()
    session.refresh(record)

    return {"status": "success", "message": f"{user_id} has been deactivated."}
