"""
User Schema.
This module will contain the schema for a user schema and enums for the validation
Authors: Kenneth Carmichael (kencar17)
Date: October 11th 2024
Version: 1.0
"""
from pydantic import BaseModel


class UpdateUser(BaseModel):
    """
    Update user schema validation model
    """

    display_name: str
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_superuser: bool
    is_active: bool
