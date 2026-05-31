"""
Tasks API routes.

Endpoints for creating, reading, updating, and deleting tasks.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from bson import ObjectId

from app.database import get_db
from app.models.task import TaskCreate, TaskUpdate, TaskResponse, PriorityLevel

router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    """
    Create a new task.
    
    Args:
        task: Task creation data
        
    Returns:
        Created task with ID
    """
    db = await get_db()
    
    task_data = task.dict()
    task_data["createdAt"] = datetime.utcnow()
    task_data["updatedAt"] = datetime.utcnow()
    
    result = await db.tasks.insert_one(task_data)
    
    created_task = await db.tasks.find_one({"_id": result.inserted_id})
    return TaskResponse(**created_task)


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    priority: PriorityLevel | None = Query(None),
    category: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    List all tasks with optional filtering.
    
    Args:
        priority: Filter by priority level
        category: Filter by category
        skip: Number of tasks to skip
        limit: Maximum number of tasks to return
        
    Returns:
        List of tasks
    """
    db = await get_db()
    
    query = {}
    if priority:
        query["priority"] = priority
    if category:
        query["category"] = category
    
    tasks = await db.tasks.find(query).skip(skip).limit(limit).to_list(length=limit)
    return [TaskResponse(**task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """
    Get a specific task by ID.
    
    Args:
        task_id: Task ID
        
    Returns:
        Task details
    """
    db = await get_db()
    
    try:
        task = await db.tasks.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse(**task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate):
    """
    Update a task.
    
    Args:
        task_id: Task ID
        task_update: Updated task data
        
    Returns:
        Updated task
    """
    db = await get_db()
    
    try:
        update_data = task_update.dict(exclude_unset=True)
        update_data["updatedAt"] = datetime.utcnow()
        
        await db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
        
        updated_task = await db.tasks.find_one({"_id": ObjectId(task_id)})
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return TaskResponse(**updated_task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """
    Delete a task.
    
    Args:
        task_id: Task ID
    """
    db = await get_db()
    
    try:
        result = await db.tasks.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
