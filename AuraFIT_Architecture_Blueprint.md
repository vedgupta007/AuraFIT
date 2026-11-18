# AuraFIT: Technical Architecture Blueprint & Implementation Roadmap

As the lead software architect, I have deeply analyzed the requirements for AuraFIT. To meet the goal of a premium, culturally-aware, AI-powered fitness and nutrition platform—while strictly maintaining the boundaries between deterministic calculations and LLM generation—this blueprint defines a robust, scalable, and maintainable architecture.

---

## 1. Complete System Architecture

AuraFIT follows a decoupled Client-Server architecture.
- **Client (Frontend)**: A Single Page Application (SPA) built with React and Vite. It handles the premium, editorial-style UI, client-side routing, and data caching.
- **Server (Backend)**: A RESTful API built with Python and FastAPI. It acts as the authoritative source of truth, performing deterministic health calculations and managing database interactions.
- **Database**: MongoDB Atlas. A NoSQL document database chosen for its flexibility with varied data structures (like complex nested meal plans or exercise logs).
- **AI Service**: Google Gemini API, accessed **exclusively** through the backend. The backend acts as an orchestrator, securely passing user context to Gemini and enforcing structured JSON responses.

**WHY**: This separation of concerns ensures that the frontend remains lightweight and secure (no API keys exposed), the backend maintains authority over critical calculations (preventing AI hallucinations of BMR/Macros), and the database scales flexibly.

---

## 2. Recommended Folder Structure

A monorepo structure separating the frontend and backend ensures easy context sharing while keeping dependencies isolated.

```text
AuraFIT/
├── frontend/                 # React/Vite Application
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── assets/           # Images, typography files
│   │   ├── components/       # Reusable UI building blocks (buttons, inputs)
│   │   │   ├── common/       # Generic components (styled for AuraFIT)
│   │   │   └── layout/       # Navigation, sidebars, page wrappers
│   │   ├── features/         # Domain-driven feature modules
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── nutrition/
│   │   │   ├── workouts/
│   │   │   └── ai-assistant/
│   │   ├── hooks/            # Custom React hooks
│   │   ├── lib/              # Third-party library configs (Axios, TanStack)
│   │   ├── store/            # Global state (e.g., Zustand) if needed
│   │   ├── types/            # TypeScript interfaces (if using TS)
│   │   └── utils/            # Helper functions (formatting, validation)
│   ├── index.html
│   └── package.json
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/              # API Route definitions (Controllers)
│   │   ├── core/             # App config, security, JWT settings
│   │   ├── db/               # MongoDB connection and setup
│   │   ├── models/           # Pydantic schemas (data validation)
│   │   ├── services/         # Business logic & AI orchestration
│   │   └── utils/            # Deterministic calculation functions (BMR, etc.)
│   ├── tests/                # Pytest directory
│   ├── requirements.txt
│   └── main.py               # FastAPI entry point
└── README.md
```

**WHY**: The `features/` folder pattern in the frontend prevents the "file soup" problem as the app grows. In the backend, the Controller-Service-Repository pattern (api -> services -> db) ensures business logic is testable independently of HTTP routes.

---

## 3. Frontend Architecture

- **Core**: React + Vite (for rapid HMR and optimized builds).
- **Styling**: Tailwind CSS with a strict, custom design system configuration. We will deliberately avoid UI component libraries (like MUI or generic Bootstrap) to fulfill the "editorial, premium, non-generic" UI requirement.
- **State & Data Fetching**: TanStack Query (React Query).
- **Routing**: React Router DOM.
- **Visuals/Charts**: Recharts (for lightweight, customizable progress tracking).

**WHY**: TanStack Query eliminates the need for complex Redux setups by intelligently caching API responses, handling loading/error states, and minimizing unnecessary network requests. Custom Tailwind ensures the UI feels "designed, not generated" with strong typography and intentional whitespace.

---

## 4. Backend Architecture

- **Framework**: FastAPI (Python).
- **Data Validation**: Pydantic.
- **Async I/O**: The entire backend will utilize Python's `asyncio` to prevent blocking during network requests to the Gemini API or MongoDB.
- **Layered Design**:
  - *Routers*: Handle HTTP requests/responses.
  - *Services*: Contain business logic (e.g., `NutritionService.calculate_macros()`).
  - *AI Orchestration*: Dedicated services that construct prompts, bind tools, and parse structured outputs from Gemini.

**WHY**: FastAPI is built on Pydantic, meaning the data schemas we use to validate incoming API requests are the exact same schemas we use to enforce structured outputs from the Gemini API. This guarantees type safety across the entire application.

---

## 5. MongoDB Collections and Schema Design

1. **`users`**: Authentication credentials, roles (admin/user).
2. **`profiles`**: Linked to `users`. Stores age, sex, height, weight, activity level, goals, dietary preferences, allergies, and the *system-calculated* BMR/TDEE/Macros.
3. **`foods`**: Authoritative database of foods (heavily featuring Indian/North Indian cuisine). Fields: `name`, `calories_per_100g`, `protein_g`, `carbs_g`, `fat_g`, `tags` (vegan, gluten-free, high-protein).
4. **`exercises`**: Authoritative database. Fields: `name`, `muscle_group`, `equipment_needed`, `difficulty`, `instructions`.
5. **`meal_plans`**: Pre-generated or AI-customized daily plans linking to `foods` with specific portion sizes.
6. **`workout_plans`**: Daily routines linking to `exercises` with sets/reps.
7. **`daily_logs`**: Tracks user compliance. Fields: `date`, `user_id`, `consumed_foods` (array), `completed_exercises` (array), `current_weight`.

**WHY**: MongoDB's document model perfectly handles dynamic arrays (like a list of ingredients in a meal or sets in an exercise) without requiring complex SQL joins.

---

## 6. API Endpoint Specification

**Auth**:
- `POST /api/auth/register`
- `POST /api/auth/login` (Returns JWT)

**User Profile**:
- `GET /api/profile/me`
- `PUT /api/profile/me` (Triggers background recalculation of macros)

**Nutrition (Deterministic)**:
- `GET /api/nutrition/targets` (Returns calculated macros/calories)
- `GET /api/foods/search?q={query}&diet={diet}`

**Plans (Hybrid DB/AI)**:
- `POST /api/plans/meals/generate` (Generates meal plan based on profile constraints)
- `POST /api/plans/workouts/generate`

**Tracking**:
- `POST /api/tracking/log-meal`
- `POST /api/tracking/log-weight`

**AI Assistant**:
- `POST /api/ai/chat` (Receives user message, returns AI response + updated structured data)
- `POST /api/ai/replace-food` (Specific endpoint for targeted AI mutations)

**WHY**: RESTful principles keep the API predictable. Dedicated endpoints for specific AI actions (like replacing a food) prevent the need for a massive, monolithic chat endpoint to handle every single app state change.

---

## 7. Authentication Architecture

- **Mechanism**: JSON Web Tokens (JWT).
- **Flow**: User logs in -> Backend validates password -> Backend issues an Access Token (short-lived, e.g., 15 mins) and a Refresh Token (long-lived, e.g., 7 days) stored in an HTTP-only, secure cookie.
- **Frontend Handling**: Frontend attaches the Access Token to the `Authorization: Bearer <token>` header using an Axios interceptor. If it expires, the interceptor automatically calls the refresh endpoint using the cookie to get a new token.

**WHY**: HTTP-only cookies for refresh tokens prevent Cross-Site Scripting (XSS) attacks from stealing long-term access. JWTs are stateless, reducing database lookups for every request.

---

## 8. Nutrition Calculation Architecture

- **Core Rule**: AI is NEVER allowed to guess these numbers.
- **Logic**: 
  1. Backend receives user metrics.
  2. Uses the **Mifflin-St Jeor equation** to calculate Basal Metabolic Rate (BMR) (most accurate for modern populations).
  3. Applies an activity multiplier (e.g., 1.2 for sedentary, 1.55 for moderate) to get TDEE (Total Daily Energy Expenditure).
  4. Applies goal offset (+500 for muscle gain, -500 for fat loss).
  5. Calculates Macro splits deterministically based on goal (e.g., Fat Loss: 40% Protein, 30% Carbs, 30% Fat).
- **Storage**: These values are saved to the user's `profile` document.

**WHY**: Calculations must be deterministic, mathematically sound, and legally safe. Medical/Health algorithms must be hardcoded and rigorously tested, not left to LLM probability.

---

## 9. Food Recommendation Architecture

- **Filtering Engine**: When recommending foods, the backend first runs a deterministic MongoDB query: `db.foods.find({ tags: { $in: [user.dietary_preference] }, allergens: { $nin: user.allergies } })`.
- **Cultural Context**: The database will be seeded with rich Indian metadata (e.g., Paneer, Dal Moong, Roti, Chicken Tikka).
- **Ranking**: Results can be ranked by how well they fill the user's remaining daily macro targets.

**WHY**: Relying on the DB for recommendations guarantees that we only suggest foods we actually have nutritional data for, preventing the AI from suggesting imaginary dishes with fabricated calorie counts.

---

## 10. Meal-Plan Generation Architecture

1. **Fetch Constraints**: Backend retrieves user's target macros and dietary restrictions.
2. **Candidate Selection**: Backend queries the DB for a pool of valid breakfast, lunch, dinner, and snack options.
3. **Constraint Solving**: A backend algorithm (or a carefully prompted Gemini call using *only* the provided DB options) pieces together combinations that total within +/- 5% of the macro targets.
4. **AI Personalization (Optional)**: Gemini can be used to generate a human-friendly description of the day ("A hearty North Indian vegetarian day focusing on high protein...").

**WHY**: This guarantees mathematical accuracy while utilizing AI for the "flavor" and presentation of the plan.

---

## 11. Workout Recommendation Architecture

- **Templates**: The database holds workout templates (e.g., "Push/Pull/Legs", "Full Body Home Workout").
- **Constraint Filtering**: The backend filters templates based on the user's `activity_level` and `available_equipment`.
- **AI Modification**: If a user says "I don't have a bench for bench press", the system uses the Gemini tool `get_alternative_exercise(current_exercise, available_equipment)` which queries the DB for exercises hitting the same `muscle_group`.

**WHY**: Safe exercise programming requires proven templates. AI is best used for modular replacements rather than generating routines from scratch, preventing unsafe volume or exercise pairings.

---

## 12. AI Service Architecture

- **Integration Point**: The frontend sends a chat message to `POST /api/ai/chat`.
- **Context Injection**: The backend intercepts this, fetches the user's profile, current macros, and today's meal plan, and constructs a System Prompt: *"You are AuraFIT. User target is 2000 kcal. They are currently at 1500 kcal. Do not invent nutrition values."*
- **Execution**: The backend calls the Gemini API.
- **Response**: The backend parses the response, applies any requested database changes (if a tool was called), and returns the text response + updated state to the frontend.

**WHY**: Injecting context securely on the backend means the AI always knows the user's current state without the frontend having to manage complex prompt engineering.

---

## 13. AI Tool/Function-Calling Architecture

Gemini will be configured with specific tools (functions) it can invoke.
- `search_food_database(query, max_results)`
- `replace_meal_item(meal_id, old_food_id, new_food_id)`
- `replace_exercise(routine_id, old_exercise_id, available_equipment)`
- `log_water_intake(amount_ml)`

**Workflow**:
1. User: "Swap my chicken with paneer."
2. Gemini decides to call `search_food_database("paneer")`.
3. Backend intercepts tool call, queries MongoDB, returns paneer ID and macros to Gemini.
4. Gemini calls `replace_meal_item(123, "chicken_id", "paneer_id")`.
5. Backend executes the DB update and returns success to Gemini.
6. Gemini generates text: "I've swapped that for Paneer. Your protein dropped slightly by 5g."

**WHY**: Function calling grounds the AI in reality. It forces the AI to interact with your deterministic systems rather than hallucinating changes.

---

## 14. Structured JSON Schemas for AI Responses

When we need Gemini to generate structured data (e.g., summarizing a complex nutritional analysis), we use Pydantic models to define the expected schema.

```python
class MealAnalysisSchema(BaseModel):
    is_compliant: bool
    reasoning: str
    suggested_modifications: list[str]
```
We pass this schema to Gemini's `response_schema` parameter.

**WHY**: Guaranteed JSON structure means the frontend can reliably map the AI's response to React components (like alert banners or lists) without parsing errors.

---

## 15. Error-Handling Strategy

- **Backend**: Global exception handlers in FastAPI. Custom exceptions like `FoodNotFoundError` or `AIHallucinationError` mapped to specific HTTP status codes (e.g., 404, 422). All errors return a standard JSON format: `{"error": {"code": "...", "message": "..."}}`.
- **Frontend**: Axios response interceptors catch errors. TanStack Query uses `onError` callbacks to trigger toast notifications. React Error Boundaries wrap major layout sections so a crash in the AI chat doesn't crash the whole dashboard.

**WHY**: Prevents the application from silently failing or showing raw stack traces to the user.

---

## 16. Security Strategy

- **No Secrets in Frontend**: Gemini API keys live *only* in backend environment variables.
- **CORS**: Strictly configured in FastAPI to only allow the Vercel frontend domain.
- **Rate Limiting**: Implemented on the `/api/ai/*` endpoints to prevent abuse of the expensive Gemini API.
- **Data Sanitization**: All user inputs (especially chat messages) are sanitized before being processed to prevent prompt injection.

**WHY**: AI endpoints are prime targets for abuse. Rate limiting and backend-only API keys protect the project's billing and integrity.

---

## 17. Performance Strategy

- **DB Indexing**: Indexes on `users.email`, `foods.name`, `foods.tags`, and `daily_logs.user_id` + `date`.
- **Frontend Caching**: TanStack Query caches static data (like the food database search results) for a set time (staleTime), preventing redundant API calls.
- **Pagination**: Food searches and log history will use offset/limit pagination.
- **Image Optimization**: Any food/fitness imagery will be served via modern formats (WebP) using Vite's asset optimization.

**WHY**: Ensures the app feels instantaneous, fulfilling the "premium" requirement, and reduces load on the database.

---

## 18. Testing Strategy

- **Backend**: `pytest` for unit testing the deterministic math functions (BMR, Macros) rigorously. We must assert that given X inputs, Y is exactly calculated. Integration tests for API endpoints mocking the DB.
- **Frontend**: `vitest` for utility functions. React Testing Library for verifying that critical components render correctly (e.g., "Does the macro progress bar show 50% when given 100g/200g?").

**WHY**: If the health math is wrong, the app fails its primary purpose. Automated tests guarantee these core functions never break during updates.

---

## 19. Deployment Architecture

- **Frontend**: Deployed on Vercel. Automatic CI/CD from the `main` branch.
- **Backend**: Deployed on a suitable production Python hosting provider (e.g., Render, Railway, or Heroku). Configured with environment variables for DB URIs and API keys.
- **Database**: MongoDB Atlas Serverless or Free Tier cluster.

**WHY**: These platforms provide easy CI/CD, SSL out of the box, and scale down to zero/cheaply for a student project, while still being production-ready architectures.

---

## 20. Development Phases

**Phase 1: Foundation (Week 1)**
- Repo setup, CI/CD pipelines.
- DB schema creation in Atlas.
- FastAPI backend setup, user auth, and deterministic math modules.

**Phase 2: Core Platform (Week 2)**
- React setup, routing, Tailwind design system config.
- User onboarding flow (metric collection).
- Connecting frontend auth to backend.

**Phase 3: Domain Data & UI (Week 3)**
- Seeding the DB with Indian/Global foods and exercises.
- Building the Dashboard, Progress tracking UI, and Food Search UI.

**Phase 4: AI & Orchestration (Week 4)**
- Integrating Gemini API in the backend.
- Building the AI Chat interface.
- Implementing AI function calling (Tool integration).

**Phase 5: Polish & Deployment (Week 5)**
- Error handling refinement, loading states.
- Responsive design audit (Mobile first).
- Final user testing and presentation prep.

**WHY**: You cannot build the AI features until the deterministic data and API exist for the AI to interact with.

---

## 21. Major Technical Risks & Mitigation

1. **Risk**: AI Hallucinates Calories or Macros.
   - *Mitigation*: Strictly enforce the rule that AI cannot output raw numbers for nutrition. It must call a tool to retrieve them from MongoDB, and the backend formats the final output.
2. **Risk**: Prompt Injection / Chat Abuse.
   - *Mitigation*: Hardcode system prompts on the backend. Do not allow the frontend to pass "instructions" to the AI, only raw user messages.
3. **Risk**: Slow Gemini Response Times blocking the UI.
   - *Mitigation*: Use streaming responses for the chat interface, and decouple heavy generation tasks (like full meal plan generation) using loading states or async background tasks.

---

# Implementation Roadmap

Follow this strictly to ensure you do not break previously built systems.

### Step 1: Project Initialization
- Initialize Git repository.
- Setup `frontend` (Vite/React/Tailwind).
- Setup `backend` (FastAPI/Virtual Env).
- Define custom Tailwind typography and colors (Editorial style).

### Step 2: Database & Auth
- Provision MongoDB Atlas.
- Create Pydantic models for User and Profile.
- Implement JWT login/register routes in FastAPI.
- Build React login/register pages and Auth Context.

### Step 3: Core Nutrition Engine (Backend Only)
- Write pure Python functions for Mifflin-St Jeor, TDEE, and Macro splitting.
- Write Pytest unit tests to verify these calculations are 100% accurate.
- Create `/api/profile/me` endpoint to accept user metrics and save calculated macros.

### Step 4: User Onboarding (Frontend)
- Build the multi-step profile creation form in React.
- Submit data to backend, fetch, and display calculated targets in a premium Dashboard layout.

### Step 5: Data Seeding
- Create a script to populate MongoDB with a base set of foods (focusing on Indian cuisine) and exercises.

### Step 6: Tracking Interfaces
- Build backend endpoints for searching foods and logging meals.
- Build frontend Food Search UI (using TanStack Query for fast searching).
- Build the Daily Log UI (progress bars for macros).

### Step 7: AI Integration Foundation
- Get Gemini API Key.
- Setup Gemini client in FastAPI backend.
- Write the foundational System Prompt injecting user profile data.

### Step 8: AI Chat Interface
- Build the chat UI in React.
- Connect to a basic `/api/ai/chat` endpoint to establish communication.

### Step 9: AI Function Calling (The Brains)
- Implement `search_food` and `replace_food` tools in the Gemini backend configuration.
- Test the AI's ability to swap a food in the database via natural language.

### Step 10: Final Polish
- Add loading skeletons, empty states, and error toasts.
- Audit mobile responsiveness.
- Ensure the UI looks designed and premium (no generic dashboards).
