"""
Routines API routes.

Endpoints for managing routines and generating AI-powered schedules.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from bson import ObjectId

from app.database import get_db
from app.models.routine import RoutineCreate, RoutineUpdate, RoutineResponse, RoutineGenerateRequest
from app.services.scheduler_service import SchedulerService

router = APIRouter()
scheduler_service = SchedulerService()


@router.post("/generate", response_model=RoutineResponse, status_code=201)
async def generate_routine(request: RoutineGenerateRequest):
    """
    Generate an AI-powered routine from tasks.
    
    Args:
        request: Routine generation request with task IDs
        
    Returns:
        Generated routine with optimized time blocks
    """
    db = await get_db()
    
    # Fetch tasks from database
    tasks = await db.tasks.find(
        {"_id": {"$in": [ObjectId(tid) for tid in request.taskIds]}}
    ).to_list(length=len(request.taskIds))
    
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    
    # Generate routine using scheduler service
    time_blocks = await scheduler_service.generate_optimal_schedule(
        tasks=tasks,
        date=request.date,
        start_time=request.preferredStartTime,
        end_time=request.preferredEndTime,
        break_duration=request.breakDurationMinutes
    )
    
    # Save routine to database
    routine_data = {
        "date": request.date,
        "timeBlocks": [block.dict() for block in time_blocks],
        "generatedBy": "ai",
        "aiScore": 0.85,  # Placeholder AI score
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    
    result = await db.routines.insert_one(routine_data)
    
    created_routine = await db.routines.find_one({"_id": result.inserted_id})
    return RoutineResponse(**created_routine)


@router.post("", response_model=RoutineResponse, status_code=201)
async def create_routine(routine: RoutineCreate):
    """
    Create a routine manually.
    
    Args:
        routine: Routine creation data
        
    Returns:
        Created routine
    """
    db = await get_db()
    
    routine_data = routine.dict()
    routine_data["createdAt"] = datetime.utcnow()
    routine_data["updatedAt"] = datetime.utcnow()
    
    result = await db.routines.insert_one(routine_data)
    
    created_routine = await db.routines.find_one({"_id": result.inserted_id})
    return RoutineResponse(**created_routine)


@router.get("", response_model=List[RoutineResponse])
async def list_routines(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    List all routines.
    
    Args:
        skip: Number of routines to skip
        limit: Maximum number of routines to return
        
    Returns:
        List of routines
    """
    db = await get_db()
    
    routines = await db.routines.find().skip(skip).limit(limit).to_list(length=limit)
    return [RoutineResponse(**routine) for routine in routines]


@router.get("/{routine_id}", response_model=RoutineResponse)
async def get_routine(routine_id: str):
    """
    Get a specific routine by ID.
    
    Args:
        routine_id: Routine ID
        
    Returns:
        Routine details
    """
    db = await get_db()
    
    try:
        routine = await db.routines.find_one({"_id": ObjectId(routine_id)})
        if not routine:
            raise HTTPException(status_code=404, detail="Routine not found")
        return RoutineResponse(**routine)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{routine_id}", response_model=RoutineResponse)
async def update_routine(routine_id: str, routine_update: RoutineUpdate):
    """
    Update a routine.
    
    Args:
        routine_id: Routine ID
        routine_update: Updated routine data
        
    Returns:
        Updated routine
    """
    db = await get_db()
    
    try:
        update_data = routine_update.dict(exclude_unset=True)
        update_data["updatedAt"] = datetime.utcnow()
        
        await db.routines.update_one(
            {"_id": ObjectId(routine_id)},
            {"$set": update_data}
        )
        
        updated_routine = await db.routines.find_one({"_id": ObjectId(routine_id)})
        if not updated_routine:
            raise HTTPException(status_code=404, detail="Routine not found")
        
        return RoutineResponse(**updated_routine)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{routine_id}", status_code=204)
async def delete_routine(routine_id: str):
    """
    Delete a routine.
    
    Args:
        routine_id: Routine ID
    """
    db = await get_db()
    
    try:
        result = await db.routines.delete_one({"_id": ObjectId(routine_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Routine not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
