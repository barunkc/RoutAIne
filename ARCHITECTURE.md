# routAIne Architecture

## Overview

routAIne uses a split architecture:

- **Next.js frontend** for dashboard, tasks, calendar, and habits UX.
- **FastAPI backend** exposing API endpoints and background workers.
- **MongoDB** for task/routine/schedule/habit/notification persistence.
- **Twilio** for outbound SMS reminders.
- **AI service layer** for routine recommendation generation.

## Backend layers

1. **API routers (`backend/app/api`)**: request validation and endpoint wiring.
2. **Services (`backend/app/services`)**: AI, scheduling, notification, and habits logic.
3. **Models (`backend/app/models`)**: Pydantic schemas for domain objects.
4. **Database (`backend/app/database.py`)**: MongoDB client and DB access helper.

## Data model summary

- **Task**: title, description, duration, priority, deadline
- **Routine**: generated time slots + AI recommendations
- **Schedule**: day + routine time blocks
- **Habit**: name, frequency, completion history
- **Notification**: SMS content, recipient, sent time, delivery status

## Runtime flow

1. User creates tasks from the frontend.
2. Backend stores tasks in MongoDB.
3. Routine generation endpoint uses AI service + scheduler support.
4. Daily schedule and habits endpoints provide planner context.
5. Notification endpoint uses Twilio to send SMS reminders.
6. Startup workers periodically process notification/routine/habit jobs.
