# RoutAIne System Architecture

## Overview

RoutAIne is an AI-powered adaptive planner that intelligently schedules tasks into daily routines. The system uses machine learning to optimize time allocation and provides real-time notifications via SMS.

## System Components

### Frontend (Next.js 14+)
- **Dashboard**: Real-time overview of today's routine and upcoming tasks
- **Task Manager**: CRUD operations for tasks with duration and priority
- **Calendar View**: Visual time-blocking interface
- **Habit Tracker**: Daily habit completion tracking
- **Routine Generator UI**: Trigger AI-powered routine generation

### Backend (FastAPI)
- **Task Service**: Manages task storage and retrieval
- **AI Service**: OpenAI integration for routine optimization
- **Scheduler Service**: Creates optimal time blocks
- **Notification Service**: Twilio SMS integration
- **Habit Service**: Tracks habit completion and statistics

### Database (MongoDB)
- Document-based storage for flexible schema
- Collections: tasks, routines, schedules, habits, notifications

## Data Models

### Task
```typescript
{
  _id: ObjectId
  title: string
  description: string
  duration: number (minutes)
  priority: "low" | "medium" | "high"
  deadline: Date
  category: string
  createdAt: Date
  updatedAt: Date
}
```

### Routine
```typescript
{
  _id: ObjectId
  date: Date
  timeBlocks: [
    {
      startTime: string (HH:MM)
      endTime: string (HH:MM)
      taskId: ObjectId
      type: "task" | "break" | "habit"
    }
  ]
  generatedBy: "ai" | "manual"
  aiScore: number (0-100)
  createdAt: Date
}
```

### Habit
```typescript
{
  _id: ObjectId
  name: string
  frequency: "daily" | "weekly" | "custom"
  targetDays: number[]
  completionHistory: [
    {
      date: Date
      completed: boolean
    }
  ]
  streak: number
  createdAt: Date
}
```

### Notification
```typescript
{
  _id: ObjectId
  recipientPhone: string
  message: string
  taskId: ObjectId
  sentAt: Date
  status: "pending" | "sent" | "failed"
  retryCount: number
}
```

## API Architecture

### RESTful Endpoints
- `/api/tasks/*` - Task management
- `/api/routines/*` - Routine management and generation
- `/api/schedules/*` - Schedule queries
- `/api/habits/*` - Habit tracking
- `/api/notifications/*` - Notification management

### AI Integration Flow
1. User submits tasks for the day
2. AI Service receives task list
3. OpenAI API generates optimal routine
4. Scheduler Service creates time blocks
5. Frontend displays generated routine
6. User can accept or modify routine

## Background Services

### Notification Worker
- Monitors upcoming tasks and habits
- Sends SMS reminders via Twilio
- Retries failed notifications
- Runs independently of web server

### Routine Generator
- Scheduled daily routine optimization
- AI learns from user preferences
- Adjusts recommendations based on completion rates

## Deployment Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP/REST
       ↓
┌─────────────────┐
│   Next.js App   │
│   (Port 3000)   │
└────────┬────────┘
         │ HTTP
         ↓
┌─────────────────┐
│   FastAPI       │
│   (Port 8000)   │
└────────┬────────┘
         │ Query/Store
         ↓
┌─────────────────┐
│   MongoDB       │
└─────────────────┘
```

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=RoutAIne
```

### Backend (.env)
```
MONGODB_URL=mongodb://localhost:27017/routaine
OPENAI_API_KEY=sk-...
TWILIO_ACCOUNT_SID=ACxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxx
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
DEBUG=False
```

## Security Considerations

- API endpoints require authentication (JWT tokens)
- Environment variables for sensitive credentials
- MongoDB connection with IP whitelisting
- Rate limiting on public endpoints
- Input validation on all API endpoints
- CORS configuration for frontend origin

## Future Enhancements

- Machine learning model for routine optimization
- Mobile app (React Native)
- Calendar integrations (Google Calendar, Outlook)
- Advanced analytics dashboard
- Team/shared routines
- Integration with productivity tools (Slack, Teams)
- Voice commands and smart speaker integration

---

For implementation details, see individual service documentation in `backend/app/`.
