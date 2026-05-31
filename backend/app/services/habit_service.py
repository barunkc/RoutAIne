from datetime import date

from app.models import Habit, HabitProgress


class HabitService:
    """Provides read/update helpers for habit tracking."""

    async def list_habits(self) -> list[Habit]:
        return [
            Habit(
                name="Morning planning",
                frequency="daily",
                progress=[HabitProgress(day=date.today(), completed=True)],
            ),
            Habit(
                name="Workout",
                frequency="daily",
                progress=[HabitProgress(day=date.today(), completed=False)],
            ),
        ]
