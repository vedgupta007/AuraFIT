# AuraFIT: Complete Implementation Specification

This document provides the exhaustive, final technical specification for AuraFIT. It dictates all architectural, database, API, algorithmic, and design decisions required for implementation. 

**Rule:** No application code is written here. This is the blueprint for development.

---

# A. FINAL ARCHITECTURE

## 1. Complete Project Folder Structure
A monorepo structure separating frontend (React/Vite) and backend (FastAPI).

```text
AuraFIT/
├── frontend/
│   ├── public/
│   │   └── fonts/                 # Local font files (Playfair Display, Inter)
│   ├── src/
│   │   ├── assets/                # Static images, SVG icons
│   │   ├── components/
│   │   │   ├── ui/                # Base design system (Button, Input, Typography)
│   │   │   ├── layout/            # Sidebar, Navbar, PageLayout, Grid
│   │   │   └── shared/            # Reusable complex components (MacroBar, FoodCard)
│   │   ├── features/              # Feature-based domains
│   │   │   ├── auth/              # api.ts, components/, hooks/, types.ts
│   │   │   ├── profile/
│   │   │   ├── nutrition/         # Meal plans, food search
│   │   │   ├── fitness/           # Workouts, exercise swap
│   │   │   ├── tracking/          # Daily logs, progress
│   │   │   └── ai-coach/          # Chat interface, message parsing
│   │   ├── hooks/                 # Global hooks (useMediaQuery, useDebounce)
│   │   ├── lib/
│   │   │   ├── axios.ts           # Axios instance with interceptors
│   │   │   └── queryClient.ts     # TanStack Query configuration
│   │   ├── routes/                # React Router definitions
│   │   ├── store/                 # Zustand store (UI state only: sidebar open, etc.)
│   │   ├── styles/
│   │   │   └── index.css          # Tailwind base imports, global overrides
│   │   ├── types/                 # Shared TypeScript interfaces
│   │   ├── utils/                 # Formatting (date, numbers)
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   ├── api/                   # FastAPI Routers
│   │   │   ├── dependencies.py    # Auth, DB injection
│   │   │   └── routes/            # auth.py, profile.py, nutrition.py, ai.py
│   │   ├── core/
│   │   │   ├── config.py          # Pydantic BaseSettings (Env vars)
│   │   │   └── security.py        # Hashing, JWT encoding/decoding
│   │   ├── db/
│   │   │   └── mongodb.py         # Motor async client connection
│   │   ├── models/
│   │   │   ├── domain.py          # DB Models (Pydantic representations)
│   │   │   └── schemas.py         # API Request/Response Models
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── nutrition_engine.py # DETERMINISTIC MATH ONLY
│   │   │   ├── plan_generator.py   # Algorithmic plan creation
│   │   │   └── ai_orchestrator.py  # Gemini API interaction
│   │   └── main.py                # App entry point
│   ├── tests/
│   │   ├── unit/                  # Math, validation testing
│   │   └── integration/           # API endpoint testing
│   ├── requirements.txt
│   └── pytest.ini
└── .gitignore
```

## 2. Authentication & Authorization System
- **Mechanism**: JWT (JSON Web Tokens).
- **Hashing**: Argon2 (via `passlib`).
- **Registration**: Accepts email/password, hashes password, creates user document, immediately returns tokens.
- **Login**: Validates credentials.
- **Token Strategy**:
  - **Access Token**: Short-lived (15 minutes). Returned in JSON response body. Stored in memory (React context/closure) by the frontend.
  - **Refresh Token**: Long-lived (7 days). Set as an `HttpOnly`, `Secure`, `SameSite=Strict` cookie by the backend.
- **Protected Routes**: Backend `get_current_user` dependency verifies Access Token.
- **Logout**: Clears the `HttpOnly` refresh cookie on the backend. Frontend drops the Access Token from memory.
- **Admin**: `role` field on User document (`user` or `admin`). Admin routes check this role in the dependency injection.

## 3. Backend Services Responsibility
- **AuthService**: Hashing, JWT generation, user verification.
- **NutritionEngine**: Pure, deterministic math for BMR, TDEE, Macros. No DB calls.
- **ProfileService**: CRUD for user metrics, triggers NutritionEngine on updates.
- **Food/ExerciseService**: CRUD and complex querying/filtering of domain data.
- **PlanGenerator**: Deterministic algorithms to select foods/exercises based on constraints.
- **TrackingService**: Appending daily logs, calculating daily aggregates.
- **AIOrchestrator**: Assembles system prompts, invokes Gemini API, parses tool calls, coordinates with other services to execute DB changes requested by AI.

## 4. Frontend State & Server State
- **Server State**: Managed strictly by TanStack Query. Handles all data fetching, caching, invalidation, and loading/error states.
- **Client State**: Minimal. Zustand used ONLY for non-persisted UI state (e.g., `isSidebarOpen`, `activeChatDrawer`).
- **Form State**: React Hook Form for performance and validation.

## 5. Caching & Database Optimization
- **Database**:
  - Compound Indexes: `{ "tags": 1, "protein_per_100g": -1 }` on foods for fast macro sorting.
  - Index on `{ "user_id": 1, "date": -1 }` on daily_logs.
- **Frontend Caching**: TanStack Query `staleTime` set to 5 minutes for profile/targets, and 24 hours for immutable food/exercise catalogs.

## 6. Security Architecture
- **API Keys**: Gemini keys strictly in backend `.env`.
- **CORS**: Restricted strictly to the Vercel frontend URL.
- **Rate Limiting**: `slowapi` limits `/api/ai/chat` to 10 requests/minute to prevent billing spikes.
- **Validation**: Pydantic strictly strips unknown fields from payloads to prevent NoSQL injection.

## 7. Error Handling
- **Backend**: Global exception handler transforms errors into standard RFC 7807 problem details: `{"type": "...", "title": "...", "status": 400, "detail": "..."}`.
- **Frontend**: Axios interceptor catches 401s to trigger refresh token flow. 400/500s are caught by TanStack Query `onError` and displayed via a unified Toast notification system. React Error Boundaries prevent full app crashes.

## 8. Logging and Monitoring
- Backend uses Python's standard `logging` module.
- `INFO` for state changes (user registered, plan generated).
- `ERROR` with stack traces for 500s.
- `WARNING` for Gemini timeouts or malformed LLM responses.

## 9. Automated Testing
- **Unit**: Pytest for `NutritionEngine` (ensuring math is exactly correct).
- **API**: Pytest + `httpx` async client to test endpoints with a mocked database.
- **Frontend**: Vitest for utility functions (e.g., date formatting).
- **AI Validation**: Pytest suite that sends mock inputs to the `AIOrchestrator` to ensure it correctly triggers Pydantic schema validation on mock LLM outputs.

---

# B. FINAL DATABASE DESIGN

MongoDB Atlas, native async driver (Motor).

### 1. `users`
- `_id`: ObjectId
- `email`: String (Unique, Indexed)
- `password_hash`: String
- `role`: String (Enum: "user", "admin")
- `created_at`: Datetime
- *Example*: `{"email": "user@test.com", "role": "user"}`

### 2. `profiles`
- `_id`: ObjectId
- `user_id`: ObjectId (Ref `users`, Indexed, Unique)
- `age`: Int (Required)
- `sex`: String (Enum: "M", "F")
- `height_cm`: Float (Required)
- `weight_kg`: Float (Required)
- `activity_level`: String (Enum: "sedentary", "light", "moderate", "active", "very_active")
- `goal`: String (Enum: "fat_loss", "maintenance", "muscle_gain")
- `dietary_preference`: String (Enum: "vegetarian", "eggetarian", "vegan", "non_vegetarian")
- `allergies`: Array of Strings (Optional)
- `calculated_targets`: Object (Required)
  - `bmr`: Float
  - `tdee`: Float
  - `daily_calories`: Float
  - `macros`: Object (`protein_g`, `carbs_g`, `fat_g`)
- *Example*: `{"user_id": "...", "age": 25, "sex": "M", "goal": "fat_loss", "calculated_targets": {"bmr": 1800, "daily_calories": 2000, "macros": {"protein_g": 150...}}}`

### 3. `foods`
- `_id`: ObjectId
- `name`: String (Indexed)
- `brand`: String (Optional)
- `calories_per_100g`: Float (Required)
- `protein_per_100g`: Float
- `carbs_per_100g`: Float
- `fat_per_100g`: Float
- `tags`: Array of Strings (Indexed. e.g., ["vegetarian", "high_protein", "indian"])
- `allergens`: Array of Strings (e.g., ["dairy", "nuts"])
- *Example*: `{"name": "Paneer", "calories_per_100g": 265, "protein_per_100g": 18.3, "tags": ["vegetarian", "indian"], "allergens": ["dairy"]}`

### 4. `exercises`
- `_id`: ObjectId
- `name`: String (Indexed)
- `muscle_group`: String (Required. e.g., "Chest", "Legs")
- `equipment`: String (Enum: "none", "dumbbells", "barbell", "machine", "bands")
- `difficulty`: String (Enum: "beginner", "intermediate", "advanced")
- *Example*: `{"name": "Dumbbell Bench Press", "muscle_group": "Chest", "equipment": "dumbbells"}`

### 5. `meal_plans`
- `_id`: ObjectId
- `user_id`: ObjectId (Ref `users`, Indexed)
- `date`: Date
- `meals`: Array of Objects
  - `meal_type`: String (Enum: "breakfast", "lunch", "dinner", "snack")
  - `items`: Array of Objects:
    - `food_id`: ObjectId (Ref `foods`)
    - `amount_g`: Float
- `total_calories`: Float
- *Example*: `{"date": "2026-09-11", "meals": [{"meal_type": "breakfast", "items": [{"food_id": "...", "amount_g": 150}]}]}`

### 6. `workout_plans`
- `_id`: ObjectId
- `user_id`: ObjectId (Ref `users`, Indexed)
- `date`: Date
- `exercises`: Array of Objects
  - `exercise_id`: ObjectId (Ref `exercises`)
  - `sets`: Int
  - `reps`: Int
- *Example*: `{"date": "2026-09-11", "exercises": [{"exercise_id": "...", "sets": 3, "reps": 10}]}`

### 7. `daily_logs`
- `_id`: ObjectId
- `user_id`: ObjectId (Indexed)
- `date`: Date (Indexed)
- `weight_logged_kg`: Float (Optional)
- `water_logged_ml`: Int
- `consumed_foods`: Array (Same structure as meal_plan items)
- `completed_workouts`: Boolean

---

# C. FINAL API CONTRACT

All endpoints prefixed with `/api/v1`.

### Auth
1. `POST /auth/register` | Body: `{email, password}` | Resp: `UserSchema` | Auth: None | Set HttpOnly Cookie.
2. `POST /auth/login` | Body: `{email, password}` | Resp: `{access_token}` | Auth: None | Set HttpOnly Cookie.
3. `POST /auth/refresh` | Body: None | Resp: `{access_token}` | Auth: Cookie Valid | Read cookie, issue new access token.
4. `POST /auth/logout` | Body: None | Resp: `200 OK` | Auth: Valid Token | Clear cookie.

### Profile & Nutrition
5. `GET /profile/me` | Resp: `ProfileSchema` | Auth: Required
6. `PUT /profile/me` | Body: `{age, weight, goal...}` | Resp: `ProfileSchema` | Auth: Required | *Triggers backend macro recalculation*.
7. `GET /nutrition/targets` | Resp: `{calories, protein, carbs, fat}` | Auth: Required | Fetches calculated data.

### Domain Data
8. `GET /foods` | Query: `?q=&diet=&min_protein=` | Resp: `List[FoodSchema]` | Auth: Required
9. `GET /exercises` | Query: `?muscle=&equipment=` | Resp: `List[ExerciseSchema]` | Auth: Required

### Generation & Planning
10. `POST /plans/meals/generate` | Body: `{date}` | Resp: `MealPlanSchema` | Auth: Required | Triggers algorithmic generation.
11. `PUT /plans/meals/{plan_id}/replace` | Body: `{meal_type, old_food_id, new_food_id, amount_g}` | Resp: `MealPlanSchema` | Auth: Required.

### Tracking
12. `POST /tracking/food` | Body: `{date, food_id, amount_g, meal_type}` | Resp: `DailyLogSchema` | Auth: Required
13. `POST /tracking/weight` | Body: `{date, weight_kg}` | Resp: `DailyLogSchema` | Auth: Required

### AI Coach
14. `POST /ai/chat` | Body: `{message: str, history: List[Msg]}` | Resp: `{reply: str, actions_taken: List[str]}` | Auth: Required | Main AI entry point.

---

# D. FINAL AI & DOMAIN ARCHITECTURE

## 1. Deterministic Nutrition Engine (Backend Math)
**Must not use AI.**
- **BMR (Mifflin-St Jeor)**:
  - Male: `(10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5`
  - Female: `(10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161`
- **TDEE**:
  - `BMR * Multiplier` (Sedentary: 1.2, Light: 1.375, Moderate: 1.55, Active: 1.725, Very Active: 1.9)
- **Goal Adjustment (Calories)**:
  - Fat Loss: `TDEE - 500` (Floor at 1200 kcal).
  - Maintenance: `TDEE`.
  - Muscle Gain: `TDEE + 300`.
- **Macro Split**:
  - Protein: `2.0 * weight_kg` (grams).
  - Fat: `0.8 * weight_kg` (grams).
  - Carbs: `(Total Calories - (Protein*4) - (Fat*9)) / 4` (grams).

## 2. Food Recommendation & Filtering Engine
- **Filter**: Strict MongoDB query excluding `allergens` array and enforcing `tags` must contain the user's `dietary_preference`.
- **Ranking**: Foods are scored by `protein_per_100g / calories_per_100g`. Higher ratio = higher ranking for fat loss/muscle gain.

## 3. Meal-Plan Generation System
- **Deterministic Baseline**: The backend divides daily calories into 4 buckets (Breakfast 25%, Lunch 35%, Dinner 30%, Snack 10%). It queries the DB for high-ranking foods matching the user's diet and fills the buckets using a greedy algorithm until macros are within +/- 5% of targets.
- **AI Role**: AI does NOT calculate amounts. AI is only used to format the output or explain *why* the deterministic plan is good.

## 4. Workout Recommendation Engine
- **Logic**: Rule-based. 
  - Beginner -> 3x/week Full Body.
  - Intermediate/Advanced -> 4x/week Upper/Lower or 6x/week PPL.
- **Filtering**: Queries DB strictly based on `equipment` available to the user.

## 5. Gemini AI Architecture
- **Isolation**: Frontend -> FastAPI -> Gemini API.
- **System Prompt**: 
  `"You are AuraFIT AI. The user's goal is {goal}, target calories are {calories}. You CANNOT invent nutrition values. To modify plans or find foods, you MUST use the provided tools. If asked for medical advice, decline politely."`
- **Context passing**: Backend fetches current `Profile` and `DailyLog` and prepends it as JSON to the user's message before sending to Gemini.
- **Tool Calling (Function Calling)**:
  Gemini is provided with JSON schema descriptions of backend functions:
  - `find_alternative_food(food_id)`: Triggers backend DB search for similar macros.
  - `replace_food_in_plan(plan_id, old_id, new_id, amount_g)`: Triggers DB update.
- **Output Schema**: Pydantic models enforce Gemini returns structured JSON when required, preventing markdown parsing errors.
- **Hallucination Prevention**: If Gemini attempts to state a calorie amount without calling the DB tool, the prompt instructs it to default to: "Let me check the database for that exact nutritional profile."

---

# E. FINAL UI/DESIGN SYSTEM

**Concept**: "Editorial Fitness" - Premium, readable, intentional, uncrowded. Avoid generic SaaS styling.

## Design Tokens
- **Typography**:
  - Headings/Logos: `Playfair Display` (Serif). Conveys editorial authority and elegance.
  - Body/UI: `Inter` (Sans-serif). Highly legible for data and metrics.
- **Color Palette**:
  - Background: `Cream` `#F9F8F6` (Not pure white, softer on eyes).
  - Surface: `Paper` `#FFFFFF` (For cards, but without heavy shadows).
  - Primary Text/Brand: `Forest Green` `#1A362D` (Grounding, natural).
  - Accent/Action: `Terracotta` `#D87D61` (Warm, energetic without being neon).
  - Secondary Text: `Stone` `#6B7280`.
  - Borders: `Light Gray` `#E5E7EB`.
- **Spacing**: Intentional whitespace. Tailwind `p-8` or `p-12` on sections. No cramped data grids.
- **Cards**: Flat design. 1px border. NO heavy drop shadows. NO glowing borders. `border-gray-200 bg-white rounded-none md:rounded-sm`.
- **Imagery**: High-contrast, desaturated photography.

## Major User Flows
1. **Onboarding**: Clean, one-question-per-screen flow (Typeform style) asking for age, weight, goals. Editorial typography.
2. **Dashboard (First Visit)**: Displays the deterministically calculated BMR and Macros in a clean typographic layout. No "glassmorphism" metric cards. Simple, elegant progress bars.
3. **Meal Plan View**: A structured list. Each food item shows name, amount, and macros in a minimalist row. An "AI Swap" button next to items opens a side-drawer.
4. **AI Coach Chat**: A clean chat interface (WhatsApp style but tailored to the color palette). When the AI invokes a tool (e.g., swapping a food), a small inline UI component renders in the chat showing the specific DB action taken, rather than just text.

---

# F. FINAL DEVELOPMENT ROADMAP & RISKS

## 1. Major Technical Risks & Mitigation
- **Risk**: AI Hallucination of Health Data. *Mitigation*: Strictly deterministic NutritionEngine. Gemini prompt heavily penalized for inventing numbers.
- **Risk**: MongoDB Schema rigidity. *Mitigation*: NoSQL chosen specifically. Arrays of subdocuments used for meals to allow dynamic sizing.
- **Risk**: Frontend State Desync. *Mitigation*: TanStack Query handles all server state. Mutations (like AI swapping a food) automatically invalidate the `['meal_plan']` query cache, forcing an immediate, consistent UI refresh.

## 2. Unnecessary Features (DO NOT IMPLEMENT)
- Social media sharing / feeds.
- Complex payment/Stripe integration.
- Live video workouts.
- Real-time WebSockets (polling/standard REST is fine for AI chat in a BCA project).
- Redis caching (DB indexing is sufficient).

## 3. Development Phases (Dependency Order)

**PHASE 1: Project Skeleton & Database**
- **Objective**: Setup repo, FastApi, Vite, MongoDB connection.
- **Files**: `main.py`, `mongodb.py`, `vite.config.ts`.
- **Dependencies**: None.
- **Acceptance**: Backend responds to `/ping`. Frontend renders "Hello World". DB connection successful.

**PHASE 2: Auth & Profile Engine**
- **Objective**: User registration, login, JWT handling, Profile CRUD.
- **Files**: `auth_service.py`, `auth.py`, `models/domain.py`, React Auth Context.
- **Tests**: Unit tests for JWT encoding/decoding.
- **Acceptance**: User can register, login, and secure cookie is set. Can fetch `/profile/me`.

**PHASE 3: Deterministic Nutrition Math (CRITICAL)**
- **Objective**: Implement exact BMR/TDEE/Macro logic.
- **Files**: `nutrition_engine.py`.
- **Tests**: Exhaustive Pytest unit tests asserting exact outputs for specific age/weight/height inputs.
- **Acceptance**: Backend accurately calculates and saves targets when Profile is updated.

**PHASE 4: Domain Data (Foods & Exercises)**
- **Objective**: Schema and endpoints for querying the authoritative database.
- **Files**: `foods.py`, `exercises.py`.
- **Acceptance**: Postman can query `/foods?diet=vegetarian` and get correct JSON.

**PHASE 5: Frontend Design System & Onboarding**
- **Objective**: Implement Tailwind config, typography, and the onboarding flow.
- **Files**: `tailwind.config.js`, `index.css`, `features/auth/Onboarding.tsx`.
- **Acceptance**: UI perfectly matches the "Editorial" design tokens. User can complete onboarding and see their calculated macros.

**PHASE 6: Plan Generation & Tracking**
- **Objective**: Deterministic baseline generation and daily logging.
- **Files**: `plan_generator.py`, `tracking.py`, React Dashboard UI.
- **Acceptance**: User can click "Generate Plan" and receive a mathematically valid diet. User can log weight.

**PHASE 7: AI Orchestration & Gemini Integration**
- **Objective**: Connect Gemini API, build system prompts, implement Tool Calling.
- **Files**: `ai_orchestrator.py`, `features/ai-coach/Chat.tsx`.
- **Tests**: Mock LLM responses to ensure backend parses tool calls correctly.
- **Acceptance**: User can chat. User can ask "Swap chicken for paneer", Gemini calls the tool, backend updates DB, and frontend automatically updates the UI.

**PHASE 8: Polish & E2E Testing**
- **Objective**: Error boundaries, loading states, empty states, final design tweaks.
- **Acceptance**: Application handles offline states, API errors gracefully without crashing. Mobile view is flawless.

---
*END OF SPECIFICATION. READY FOR IMPLEMENTATION.*
