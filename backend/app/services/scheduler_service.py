from datetime import date, datetime, timedelta

from app.models import RoutineSlot, Schedule, Task


class SchedulerService:
    """Builds a daily schedule from tasks and generated routine data."""

    async def create_schedule(self, tasks: list[Task]) -> Schedule:
        cursor = datetime.utcnow().replace(second=0, microsecond=0)
        blocks: list[RoutineSlot] = []

        for task in tasks:
            end = cursor + timedelta(minutes=task.duration)
            blocks.append(RoutineSlot(task_title=task.title, start_time=cursor, end_time=end))
            cursor = end

        return Schedule(day=date.today(), blocks=blocks)
