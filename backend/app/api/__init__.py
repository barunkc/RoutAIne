from fastapi import APIRouter

from app.api.habits import router as habits_router
from app.api.notifications import router as notifications_router
from app.api.routines import router as routines_router
from app.api.schedules import router as schedules_router
from app.api.tasks import router as tasks_router

api_router = APIRouter(prefix="/api")
api_router.include_router(tasks_router)
api_router.include_router(routines_router)
api_router.include_router(schedules_router)
api_router.include_router(habits_router)
api_router.include_router(notifications_router)
