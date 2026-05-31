"""
Schedules API routes.

Endpoints for retrieving daily schedules.
"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, date
from bson import ObjectId

from app.database import get_db
from app.models.schedule import ScheduleResponse, DayScheduleResponse

router = APIRouter()


@router.get("/today", response_model=DayScheduleResponse)
async def get_today_schedule():
    """
    Get today's schedule with all time blocks.
    
    Returns:
        Today's schedule with routine details
    """
    db = await get_db()
    
    today = date.today()
    start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
    end_of_day = datetime(today.year, today.month, today.day, 23, 59, 59)
    
    routine = await db.routines.find_one({
        "date": {"$gte": start_of_day, "$lte": end_of_day}
    })
    
    if not routine:
        return DayScheduleResponse(
            date=start_of_day,
            timeBlocks=[],
            summary={
                "totalTasks": 0,
                "totalDuration": 0,
                "completedTasks": 0,
                "upcomingTasks": []
            }
        )
    
    return DayScheduleResponse(
        date=routine["date"],
        timeBlocks=routine.get("timeBlocks", []),
        summary={
            "totalTasks": len([tb for tb in routine.get("timeBlocks", []) if tb.get("type") == "task"]),
            "totalDuration": sum([calculate_duration(tb) for tb in routine.get("timeBlocks", [])]),
            "completedTasks": 0,
            "upcomingTasks": routine.get("timeBlocks", [])
        }
    )


@router.get("/{date_str}", response_model=DayScheduleResponse)
async def get_schedule_by_date(date_str: str):
    """
    Get schedule for a specific date.
    
    Args:
        date_str: Date in YYYY-MM-DD format
        
    Returns:
        Schedule for the specified date
    """
    db = await get_db()
    
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        start_of_day = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0)
        end_of_day = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59)
        
        routine = await db.routines.find_one({
            "date": {"$gte": start_of_day, "$lte": end_of_day}
        })
        
        if not routine:
            return DayScheduleResponse(
                date=start_of_day,
                timeBlocks=[],
                summary={
                    "totalTasks": 0,
                    "totalDuration": 0,
                    "completedTasks": 0,
                    "upcomingTasks": []
                }
            )
        
        return DayScheduleResponse(
            date=routine["date"],
            timeBlocks=routine.get("timeBlocks", []),
            summary={
                "totalTasks": len([tb for tb in routine.get("timeBlocks", []) if tb.get("type") == "task"]),
                "totalDuration": sum([calculate_duration(tb) for tb in routine.get("timeBlocks", [])]),
                "completedTasks": 0,
                "upcomingTasks": routine.get("timeBlocks", [])
            }
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")


def calculate_duration(time_block: dict) -> int:
    """
    Calculate duration of a time block in minutes.
    
    Args:
        time_block: Time block dictionary with startTime and endTime
        
    Returns:
        Duration in minutes
    """
    try:
        start = datetime.strptime(time_block.get("startTime", "00:00"), "%H:%M")
        end = datetime.strptime(time_block.get("endTime", "00:00"), "%H:%M")
        return int((end - start).total_seconds() / 60)
    except:
        return 0
