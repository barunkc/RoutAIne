# routAIne

routAIne is an AI-powered adaptive planner and scheduler with task planning, routine generation, habit tracking, and SMS notifications.

## Tech stack

- Frontend: Next.js + React + TypeScript
- Backend: FastAPI (Python 3.11+)
- Database: MongoDB
- Notifications: Twilio SMS
- AI: OpenAI/GitHub Copilot compatible service layer

## Project structure

```text
frontend/   # Next.js app router UI
backend/    # FastAPI API and services
```

## Prerequisites

- Node.js 20+
- npm 10+
- Python 3.11+
- Docker + Docker Compose

## 1) Start MongoDB locally

```bash
docker compose up -d mongodb
```

## 2) Run backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Backend API is available at `http://localhost:8000`.

## 3) Run frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Frontend is available at `http://localhost:3000`.

## Core API endpoints

- `POST /api/tasks`
- `GET /api/tasks`
- `POST /api/routines/generate`
- `GET /api/schedules`
- `GET /api/habits`
- `POST /api/notifications/send-sms`

## Notes on background workers

The backend starts placeholder workers for:

- SMS notification processing
- Scheduled routine generation
- Habit tracking

For always-on notifications, deploy the backend on an always-running host (cloud VM/container) so workers continue when your laptop sleeps.
