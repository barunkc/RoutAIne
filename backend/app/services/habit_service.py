"""
Habit Service for tracking and analyzing habit completion.

Manages habit statistics and completion history.
"""

from datetime import datetime, timedelta
from typing import Dict, List


class HabitService:
    """Service for habit management and tracking."""
    
    async def calculate_streak(self, completion_history: List[Dict]) -> int:
        """
        Calculate current habit streak.
        
        Args:
            completion_history: List of completion records
            
        Returns:
            Current streak count
        """
        if not completion_history:
            return 0
        
        # Sort by date descending
        sorted_history = sorted(
            completion_history,
            key=lambda x: x.get("date"),
            reverse=True
        )
        
        streak = 0
        current_date = datetime.utcnow().date()
        
        for record in sorted_history:
            record_date = record.get("date")
            if isinstance(record_date, datetime):
                record_date = record_date.date()
            
            # Check if this is today or yesterday relative to current streak
            expected_date = current_date - timedelta(days=streak)
            
            if record_date == expected_date and record.get("completed"):
                streak += 1
            else:
                break
        
        return streak
    
    async def calculate_best_streak(self, completion_history: List[Dict]) -> int:
        """
        Calculate best/longest habit streak.
        
        Args:
            completion_history: List of completion records
            
        Returns:
            Best streak count
        """
        if not completion_history:
            return 0
        
        # Sort by date ascending
        sorted_history = sorted(
            completion_history,
            key=lambda x: x.get("date")
        )
        
        best_streak = 0
        current_streak = 0
        prev_date = None
        
        for record in sorted_history:
            if not record.get("completed"):
                current_streak = 0
                prev_date = None
                continue
            
            record_date = record.get("date")
            if isinstance(record_date, datetime):
                record_date = record_date.date()
            
            if prev_date is None:
                current_streak = 1
            elif (record_date - prev_date).days == 1:
                current_streak += 1
            else:
                current_streak = 1
            
            best_streak = max(best_streak, current_streak)
            prev_date = record_date
        
        return best_streak
    
    async def get_habit_statistics(self, habit: Dict) -> Dict:
        """
        Generate comprehensive habit statistics.
        
        Args:
            habit: Habit document
            
        Returns:
            Dictionary with statistics
        """
        completion_history = habit.get("completionHistory", [])
        total_records = len(completion_history)
        completed = len([r for r in completion_history if r.get("completed")])
        
        completion_rate = (completed / total_records * 100) if total_records > 0 else 0
        
        return {
            "totalDays": total_records,
            "completedDays": completed,
            "completionRate": completion_rate,
            "currentStreak": await self.calculate_streak(completion_history),
            "bestStreak": await self.calculate_best_streak(completion_history),
            "lastCompleted": self._get_last_completion(completion_history)
        }
    
    def _get_last_completion(self, completion_history: List[Dict]) -> str:
        """
        Get the date of last completion.
        
        Args:
            completion_history: List of completion records
            
        Returns:
            Last completion date or "Never"
        """
        if not completion_history:
            return "Never"
        
        completed_records = [r for r in completion_history if r.get("completed")]
        if not completed_records:
            return "Never"
        
        last = max(completed_records, key=lambda x: x.get("date", datetime.min))
        last_date = last.get("date")
        
        if isinstance(last_date, datetime):
            return last_date.strftime("%Y-%m-%d")
        return str(last_date)
