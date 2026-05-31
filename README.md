# RoutAIne: AI-Powered Adaptive Planner & Scheduler

An intelligent scheduling system that combines task planning, time blocking, habit tracking, and AI optimization to create adaptive daily routines.

## Features

- **Task Management**: Create and manage tasks with duration, priority, and deadlines
- **AI-Powered Routine Generation**: OpenAI/GitHub Copilot integration to generate optimal daily schedules
- **Time Blocking**: Visual calendar interface with time-blocked routines
- **Habit Tracking**: Monitor daily habit completion
- **SMS Notifications**: Twilio integration for schedule reminders
- **Real-time Updates**: Live dashboard with upcoming tasks and routines

## Tech Stack

- **Frontend**: Next.js 14+, TypeScript, React, Tailwind CSS
- **Backend**: FastAPI (Python 3.11+), Pydantic, SQLAlchemy
- **Database**: MongoDB
- **Notifications**: Twilio SMS
- **AI Integration**: OpenAI API / GitHub Copilot
- **Containerization**: Docker & Docker Compose

## Project Structure

```
RoutAIne/
├── frontend/                    # Next.js application
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── styles/
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── .env.local.example
├── backend/                     # FastAPI application
│   ├── app/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── main.py
├── docker-compose.yml
├── .gitignore
└── ARCHITECTURE.md
```

## Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Docker & Docker Compose
- OpenAI API key
- Twilio account credentials (optional, for SMS)
- MongoDB Atlas URI or local MongoDB

### Setup Instructions

#### 1. Clone and Install
```bash
# Clone repository
git clone https://github.com/barunkc/RoutAIne.git
cd RoutAIne

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
```

#### 2. Environment Configuration
```bash
# Frontend
cd frontend
cp .env.local.example .env.local
# Edit .env.local with your API endpoints

# Backend
cd ../backend
cp .env.example .env
# Edit .env with your credentials:
# - MONGODB_URL
# - OPENAI_API_KEY
# - TWILIO_ACCOUNT_SID
# - TWILIO_AUTH_TOKEN
# - TWILIO_PHONE_NUMBER
```

#### 3. Run with Docker Compose
```bash
docker-compose up -d
```

#### 4. Manual Setup (without Docker)
```bash
# Terminal 1: Frontend
cd frontend
npm run dev
# Runs on http://localhost:3000

# Terminal 2: Backend
cd backend
uvicorn app.main:app --reload
# Runs on http://localhost:8000

# Terminal 3: MongoDB
mongod  # or use MongoDB Atlas
```

## API Endpoints

### Tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Routines
- `POST /api/routines/generate` - AI generates daily routine from tasks
- `GET /api/routines` - List routines
- `GET /api/routines/{id}` - Get routine details

### Schedules
- `GET /api/schedules/today` - Get today's schedule
- `GET /api/schedules/{date}` - Get schedule for specific date

### Habits
- `GET /api/habits` - Get all habits
- `POST /api/habits` - Create habit
- `POST /api/habits/{id}/complete` - Mark habit as complete

### Notifications
- `POST /api/notifications/send-sms` - Send SMS reminder
- `GET /api/notifications` - Get notification history

## Development Workflow

### Frontend Development
```bash
cd frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run type-check   # Check TypeScript
```

### Backend Development
```bash
cd backend
uvicorn app.main:app --reload  # Start dev server
pytest                          # Run tests
black .                         # Format code
pylint app                      # Lint code
```

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed system design, data models, and integration patterns.

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for better productivity and time management**
