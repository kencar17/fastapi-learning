"""
Fast Api App.
This module will the main learning fastapi main app.
Authors: Kenneth Carmichael (kencar17)
Date: October 10th 2024
Version: 1.0
"""

from fastapi import FastAPI

from app.api.todos.routers import todo_router

main_app = FastAPI(
    title="Learning Fastapi",
    openapi_url="/openapi.json"
)


main_app.include_router(todo_router.router)
