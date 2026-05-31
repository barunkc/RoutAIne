"""
Habits API routes.

Endpoints for habit management and tracking.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from bson import ObjectId

from app.database import get_db
from app.models.habit import HabitCreate, HabitUpdate, HabitResponse, HabitCompleteRequest

router = APIRouter()


@router.post("", response_model=HabitResponse, status_code=201)
async def create_habit(habit: HabitCreate):
    """
    Create a new habit.
    
    Args:
        habit: Habit creation data
        
    Returns:
        Created habit
    """
    db = await get_db()
    
    habit_data = habit.dict()
    habit_data["completionHistory"] = []
    habit_data["streak"] = 0
    habit_data["bestStreak"] = 0
    habit_data["totalCompleted"] = 0
    habit_data["createdAt"] = datetime.utcnow()
    habit_data["updatedAt"] = datetime.utcnow()
    
    result = await db.habits.insert_one(habit_data)
    
    created_habit = await db.habits.find_one({"_id": result.inserted_id})
    return HabitResponse(**created_habit)


@router.get("", response_model=List[HabitResponse])
async def list_habits(
    category: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    List all habits with optional filtering.
    
    Args:
        category: Filter by category
        skip: Number of habits to skip
        limit: Maximum number of habits to return
        
    Returns:
        List of habits
    """
    db = await get_db()
    
    query = {}
    if category:
        query["category"] = category
    
    habits = await db.habits.find(query).skip(skip).limit(limit).to_list(length=limit)
    return [HabitResponse(**habit) for habit in habits]


@router.get("/{habit_id}", response_model=HabitResponse)
async def get_habit(habit_id: str):
    """
    Get a specific habit by ID.
    
    Args:
        habit_id: Habit ID
        
    Returns:
        Habit details
    """
    db = await get_db()
    
    try:
        habit = await db.habits.find_one({"_id": ObjectId(habit_id)})
        if not habit:
            raise HTTPException(status_code=404, detail="Habit not found")
        return HabitResponse(**habit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{habit_id}", response_model=HabitResponse)
async def update_habit(habit_id: str, habit_update: HabitUpdate):
    """
    Update a habit.
    
    Args:
        habit_id: Habit ID
        habit_update: Updated habit data
        
    Returns:
        Updated habit
    """
    db = await get_db()
    
    try:
        update_data = habit_update.dict(exclude_unset=True)
        update_data["updatedAt"] = datetime.utcnow()
        
        await db.habits.update_one(
            {"_id": ObjectId(habit_id)},
            {"$set": update_data}
        )
        
        updated_habit = await db.habits.find_one({"_id": ObjectId(habit_id)})
        if not updated_habit:
            raise HTTPException(status_code=404, detail="Habit not found")
        
        return HabitResponse(**updated_habit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{habit_id}/complete", response_model=HabitResponse)
async def complete_habit(habit_id: str, request: HabitCompleteRequest):
    """
    Mark a habit as completed for a specific date.
    
    Args:
        habit_id: Habit ID
        request: Completion request with date and optional notes
        
    Returns:
        Updated habit
    """
    db = await get_db()
    
    try:
        completion_record = {
            "date": request.date,
            "completed": True,
            "notes": request.notes
        }
        
        await db.habits.update_one(
            {"_id": ObjectId(habit_id)},
            {
                "$push": {"completionHistory": completion_record},
                "$inc": {"totalCompleted": 1},
                "$set": {"updatedAt": datetime.utcnow()}
            }
        )
        
        updated_habit = await db.habits.find_one({"_id": ObjectId(habit_id)})
        if not updated_habit:
            raise HTTPException(status_code=404, detail="Habit not found")
        
        return HabitResponse(**updated_habit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{habit_id}", status_code=204)
async def delete_habit(habit_id: str):
    """
    Delete a habit.
    
    Args:
        habit_id: Habit ID
    """
    db = await get_db()
    
    try:
        result = await db.habits.delete_one({"_id": ObjectId(habit_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Habit not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
