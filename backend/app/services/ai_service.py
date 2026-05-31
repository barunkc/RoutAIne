from datetime import datetime, timedelta

from app.models import Routine, RoutineSlot, Task


class AIService:
    """Handles AI-assisted routine generation using available task data."""

    async def generate_routine(self, tasks: list[Task]) -> Routine:
        now = datetime.utcnow().replace(second=0, microsecond=0)
        slots: list[RoutineSlot] = []
        cursor = now

        for task in sorted(tasks, key=lambda item: item.priority):
            end_time = cursor + timedelta(minutes=task.duration)
            slots.append(
                RoutineSlot(task_title=task.title, start_time=cursor, end_time=end_time)
            )
            cursor = end_time

        recommendations = [
            "Start with high-priority tasks first.",
            "Leave 10-minute buffer breaks between focus blocks.",
            "Review progress at the end of the day.",
        ]

        return Routine(slots=slots, recommendations=recommendations)
