"""
Scheduler Service for creating optimized time blocks.

Manages time allocation and schedule optimization logic.
"""

from datetime import datetime, timedelta
from typing import List, Dict
from app.models.routine import TimeBlock, TimeBlockType


class SchedulerService:
    """Service for scheduling and time block optimization."""
    
    async def generate_optimal_schedule(
        self,
        tasks: List[Dict],
        date: datetime,
        start_time: str,
        end_time: str,
        break_duration: int = 15
    ) -> List[TimeBlock]:
        """
        Generate optimal time blocks for tasks.
        
        Args:
            tasks: List of tasks to schedule
            date: Date for the schedule
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            break_duration: Minutes for breaks between tasks
            
        Returns:
            List of TimeBlock objects
        """
        # Parse times
        start_dt = datetime.strptime(start_time, "%H:%M")
        end_dt = datetime.strptime(end_time, "%H:%M")
        
        # Sort tasks by priority (high -> medium -> low)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(
            tasks,
            key=lambda t: priority_order.get(t.get("priority", "medium"), 1)
        )
        
        time_blocks: List[TimeBlock] = []
        current_time = start_dt
        
        for task in sorted_tasks:
            task_duration = task.get("duration", 60)
            
            # Check if task fits in remaining time
            if current_time + timedelta(minutes=task_duration) > end_dt:
                continue  # Skip if doesn't fit
            
            # Create time block
            end_time_obj = current_time + timedelta(minutes=task_duration)
            
            time_block = TimeBlock(
                startTime=current_time.strftime("%H:%M"),
                endTime=end_time_obj.strftime("%H:%M"),
                taskId=str(task.get("_id", "")),
                title=task.get("title", "Untitled Task"),
                type=TimeBlockType.TASK,
                description=task.get("description")
            )
            time_blocks.append(time_block)
            
            # Add break after task (except for last task)
            current_time = end_time_obj
            if current_time + timedelta(minutes=break_duration) < end_dt:
                break_block = TimeBlock(
                    startTime=current_time.strftime("%H:%M"),
                    endTime=(current_time + timedelta(minutes=break_duration)).strftime("%H:%M"),
                    title="Break",
                    type=TimeBlockType.BREAK
                )
                time_blocks.append(break_block)
                current_time += timedelta(minutes=break_duration)
        
        return time_blocks
    
    async def calculate_schedule_efficiency(self, time_blocks: List[TimeBlock]) -> float:
        """
        Calculate efficiency score of a schedule.
        
        Args:
            time_blocks: List of time blocks
            
        Returns:
            Efficiency score 0-100
        """
        if not time_blocks:
            return 0.0
        
        total_minutes = 0
        task_minutes = 0
        
        for block in time_blocks:
            try:
                start = datetime.strptime(block.startTime, "%H:%M")
                end = datetime.strptime(block.endTime, "%H:%M")
                duration = (end - start).total_seconds() / 60
                total_minutes += duration
                
                if block.type == TimeBlockType.TASK:
                    task_minutes += duration
            except:
                continue
        
        if total_minutes == 0:
            return 0.0
        
        efficiency = (task_minutes / total_minutes) * 100
        return min(efficiency, 100.0)
