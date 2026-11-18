# AuraFIT

AuraFIT is an AI-powered personalized fitness and nutrition platform. It provides deterministic, calculated nutrition targets and integrates AI to assist with meal planning, exercise modifications, and tracking.

## Technology Stack
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, TanStack Query, React Router, Zustand.
- **Backend**: Python, FastAPI, Pydantic, Motor (async MongoDB).
- **Database**: MongoDB Atlas.
- **AI Technology**: Google Gemini API (accessed strictly via backend).

## Local Development

### Requirements
- Node.js (v18+)
- Python (3.10+)
- MongoDB Atlas (or local MongoDB instance)

### Environment Variables
You will need to create `.env` files in both the frontend and backend directories. See the respective `.env.example` files for required variables.

- Frontend needs the backend API URL.
- Backend needs MongoDB URI, JWT secret, and Gemini API Key.

### Running Frontend
```bash
cd frontend
npm install
npm run dev
```

### Running Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```
