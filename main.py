"""
Fast Api App.
This module will the main learning fastapi main app.
Authors: Kenneth Carmichael (kencar17)
Date: October 10th 2024
Version: 1.0
"""

from fastapi import FastAPI

from app.api.tasks.routers import task_router
from app.api.users.routers import user_router
from app.db.database import create_db_and_tables

main_app = FastAPI(
    title="Learning Fastapi",
    openapi_url="/openapi.json"
)

@main_app.on_event("startup")
def on_startup():
    create_db_and_tables()


main_app.include_router(task_router.router)
main_app.include_router(user_router.router)
