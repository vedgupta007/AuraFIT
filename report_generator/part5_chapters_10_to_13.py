# -*- coding: utf-8 -*-
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_generator.helpers import (
    add_heading_1, add_heading_2, add_heading_3, add_p, add_bullet, add_numbered, create_table, add_code_block, add_figure_box
)

def build_chapters_10_to_13(doc):
    # =========================================================================
    # CHAPTER 10: EXHAUSTIVE TESTING & QUALITY ASSURANCE
    # =========================================================================
    add_heading_1(doc, "Chapter 10: Exhaustive Testing & Quality Assurance")

    add_heading_2(doc, "10.1 8-Tier Testing Strategy")
    add_p(doc, "Software reliability in health and fitness platforms is paramount; an undetected error in mathematical calculation can lead to chronic metabolic damage. AuraFIT was subjected to an exhaustive 8-tier quality assurance framework spanning the entire software testing pyramid:")
    add_bullet(doc, "1. Unit Testing", "Isolating mathematical algorithms, cryptographic hashing, and validation models.")
    add_bullet(doc, "2. Integration Testing", "Validating communication between FastAPI, MongoDB Atlas, and remote Gemini APIs.")
    add_bullet(doc, "3. Functional Testing", "Verifying end-to-end user workflows against functional requirement specifications.")
    add_bullet(doc, "4. Usability Testing", "Assessing UI aesthetics, touch targets, and readability across viewports.")
    add_bullet(doc, "5. Security Testing", "Auditing authentication, token expiry, CORS policies, and injection vulnerabilities.")
    add_bullet(doc, "6. Regression Testing", "Automating pytest suites to ensure feature enhancements preserve existing functionality.")
    add_bullet(doc, "7. Performance Testing", "Benchmarking response times, concurrency limits, and database query throughput.")
    add_bullet(doc, "8. User Acceptance Testing (UAT)", "Deploying the platform to peer cohorts and gathering empirical qualitative feedback.")

    add_heading_2(doc, "10.2 Unit Testing of Deterministic Mathematical Models")
    add_p(doc, "Table 10.1 details the unit test cases developed in `pytest` to guarantee the clinical accuracy of the Mifflin-St Jeor engine and macronutrient allocator:")

    ut_headers = ["Test ID", "Target Function", "Test Input Vector", "Expected Output", "Observed Result", "Status"]
    ut_data = [
        ["UT-01", "calculate_bmr_male", "Weight: 80kg, Height: 180cm, Age: 25", "1805.00 kcal", "1805.00 kcal", "PASSED"],
        ["UT-02", "calculate_bmr_female", "Weight: 60kg, Height: 165cm, Age: 30", "1320.25 kcal", "1320.25 kcal", "PASSED"],
        ["UT-03", "calculate_tdee_sedentary", "BMR: 1805.00, Activity: 'sedentary'", "2166.00 kcal", "2166.00 kcal", "PASSED"],
        ["UT-04", "calculate_tdee_active", "BMR: 1805.00, Activity: 'active'", "3113.62 kcal", "3113.62 kcal", "PASSED"],
        ["UT-05", "macro_split_protein", "Weight: 80kg, Factor: 2.0g/kg", "160.00 grams (640 kcal)", "160.00 grams", "PASSED"],
        ["UT-06", "macro_split_fat", "Weight: 80kg, Factor: 0.8g/kg", "64.00 grams (576 kcal)", "64.00 grams", "PASSED"],
        ["UT-07", "macro_split_carbs", "Target: 2000 kcal, P: 160g, F: 64g", "196.00 grams (784 kcal)", "196.00 grams", "PASSED"],
        ["UT-08", "safety_calorie_floor", "Target calculation resulting in 950 kcal", "1200.00 kcal (Floor enforced)", "1200.00 kcal", "PASSED"]
    ]
    create_table(doc, ut_headers, ut_data, [Inches(0.9), Inches(1.5), Inches(1.6), Inches(1.2), Inches(0.8), Inches(0.5)])

    add_heading_2(doc, "10.3 Functional Test Cases Matrix (20 Test Scenarios)")
    add_p(doc, "Table 10.2 details the comprehensive functional test scenarios validating user journeys:")

    tc_headers = ["Scenario ID", "Module", "Test Description & Steps", "Expected Result", "Status"]
    tc_data = [
        ["TC-01", "Auth", "Register with valid new email and strong password.", "HTTP 201 Created; JWT tokens returned.", "PASSED"],
        ["TC-02", "Auth", "Register with already existing email address.", "HTTP 400 Bad Request: 'Email already registered'.", "PASSED"],
        ["TC-03", "Auth", "Login with incorrect password.", "HTTP 401 Unauthorized: 'Invalid credentials'.", "PASSED"],
        ["TC-04", "Auth", "Access protected `/profile/me` without Bearer token.", "HTTP 401 Unauthorized: 'Not authenticated'.", "PASSED"],
        ["TC-05", "Profile", "Submit biometric onboarding with imperial units.", "Units converted to metric; targets computed.", "PASSED"],
        ["TC-06", "Profile", "Update body weight from 80kg to 78kg.", "BMR/TDEE recalculated; targets updated.", "PASSED"],
        ["TC-07", "Nutrition", "Search food catalog for 'Paneer'.", "Returns verified Paneer with exact 100g macros.", "PASSED"],
        ["TC-08", "Nutrition", "Filter foods with tag 'vegetarian' and 'high_protein'.", "Returns strictly vegetarian items with NDS > 0.3.", "PASSED"],
        ["TC-09", "Nutrition", "Create and save custom composite meal.", "Meal persisted in MongoDB; appears in saved list.", "PASSED"],
        ["TC-10", "Nutrition", "Delete saved custom meal.", "HTTP 204 No Content; removed from DB.", "PASSED"],
        ["TC-11", "Nutrition", "Trigger 4-bucket meal plan generation.", "Generates 4 meals matching target macros ±5%.", "PASSED"],
        ["TC-12", "AI Engine", "Request AI food swap for 100g Paneer.", "Suggests 115g Tofu; calories match within 5%.", "PASSED"],
        ["TC-13", "AI Engine", "Ask AI for medical diagnosis or prescription.", "AI politely declines, advising physician consult.", "PASSED"],
        ["TC-14", "AI Engine", "Ask AI to invent unverified calorie amount.", "Guardrail triggered; AI queries database tool.", "PASSED"],
        ["TC-15", "Fitness", "Filter exercise library by muscle 'Chest'.", "Returns Bench Press, Pushups, Incline DB Press.", "PASSED"],
        ["TC-16", "Fitness", "Log workout session: 3 sets Bench Press 80kg x 8.", "Aggregates volume = 1920 kg; saves to DB.", "PASSED"],
        ["TC-17", "Tracking", "Log daily morning weigh-in of 77.5kg.", "Entry appended to measurements; chart updates.", "PASSED"],
        ["TC-18", "Security", "Submit XSS payload `<script>` in user notes.", "Pydantic sanitizes input; payload rendered inert.", "PASSED"],
        ["TC-19", "Security", "Exceed 10 requests/min on `/api/v1/ai/chat`.", "HTTP 429 Too Many Requests enforced.", "PASSED"],
        ["TC-20", "UI/UX", "Toggle dark/light theme and resize to mobile 375px.", "Layout reflows; no horizontal scroll or overlap.", "PASSED"]
    ]
    create_table(doc, tc_headers, tc_data, [Inches(1.0), Inches(1.0), Inches(2.3), Inches(1.7), Inches(0.5)])

    add_heading_2(doc, "10.4 Security & Vulnerability Audits (OWASP Top 10)")
    add_p(doc, "AuraFIT was evaluated against the OWASP Top 10 web application security risks:")
    add_bullet(doc, "A01: Broken Access Control", "Enforced via FastAPI dependency injection (`get_current_user`), verifying cryptographic signatures on every request and checking user ownership on resource mutation.")
    add_bullet(doc, "A02: Cryptographic Failures", "Passwords are hashed using Argon2id with 64MB memory cost, 3 iterations, and 4 parallelism lanes. Tokens use HMAC-SHA256 with 256-bit entropy keys.")
    add_bullet(doc, "A03: Injection Attacks", "Pydantic models sanitize all incoming JSON payloads. MongoDB Motor driver parameterizes all queries, preventing NoSQL query injection.")
    add_bullet(doc, "A05: Security Misconfiguration", "CORS is strictly locked to trusted origins. Debug mode is disabled in production. Verbose tracebacks are caught by a global exception middleware.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 11: PRODUCTION SOURCE CODE IMPLEMENTATION
    # =========================================================================
    add_heading_1(doc, "Chapter 11: Production Source Code Implementation")
    add_p(doc, "This chapter presents the production source code implementations of the core modules powering AuraFIT, extracted directly from the verified project repository.")

    add_heading_2(doc, "11.1 Backend Core Entrypoint: `backend/app/main.py`")
    add_code_block(doc,
"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.api.routes import (
    auth, profile, nutrition, foods, exercises, 
    ai, workouts, goals, measurements, analytics, plans
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB Atlas Pool
    logger.info("Initializing connection to MongoDB Atlas...")
    await connect_to_mongo()
    yield
    # Shutdown: Cleanly close connection pool
    logger.info("Closing MongoDB connection pool...")
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Authoritative Backend REST API for AuraFIT Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration for React SPA
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Modular Domain Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["profile"])
app.include_router(nutrition.router, prefix="/api/v1/nutrition", tags=["nutrition"])
app.include_router(foods.router, prefix="/api/v1/foods", tags=["foods"])
app.include_router(exercises.router, prefix="/api/v1/exercises", tags=["exercises"])
app.include_router(workouts.router, prefix="/api/v1/workouts", tags=["workouts"])
app.include_router(goals.router, prefix="/api/v1/goals", tags=["goals"])
app.include_router(measurements.router, prefix="/api/v1/measurements", tags=["measurements"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(plans.router, prefix="/api/v1/plans", tags=["plans"])

@app.get("/ping")
async def ping():
    return {"status": "ok", "app": "AuraFIT Core Engine"}
"""
    )

    add_heading_2(doc, "11.2 Cryptographic Security Service: `backend/app/core/security.py`")
    add_code_block(doc,
"""from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from app.core.config import settings

# Argon2 Cryptographic Context for state-of-the-art password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, token_type: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != token_type:
            return None
        return payload
    except jwt.PyJWTError:
        return None
"""
    )

    add_heading_2(doc, "11.3 AI Orchestration & Tool Declarations: `backend/app/services/ai_service.py`")
    add_code_block(doc,
"""import json
from google import genai
from google.genai import types
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.models.ai import StructuredAIResponse, AISection
from app.services.ai_tools import TOOLS_REGISTRY

# Combine explicit declarations into a single Tool list for Google Gemini
gemini_tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_foods",
                description="Search the database for foods, calories, macros based on dietary preferences.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "search": types.Schema(type=types.Type.STRING, description="Food name query"),
                        "category": types.Schema(type=types.Type.STRING, description="Food category (Grains, Dairy, Legumes)"),
                        "diet": types.Schema(type=types.Type.STRING, description="Dietary preference (vegetarian, vegan)")
                    }
                )
            ),
            types.FunctionDeclaration(
                name="get_food_details",
                description="Get exact nutritional breakdown and macros for a specific food ID.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "food_id": types.Schema(type=types.Type.STRING, description="The ID of the food")
                    },
                    required=["food_id"]
                )
            ),
            types.FunctionDeclaration(
                name="find_alternative_food",
                description="Find an alternative food for a food ID respecting calorie and macro parity.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "food_id": types.Schema(type=types.Type.STRING, description="The ID of food to replace")
                    },
                    required=["food_id"]
                )
            ),
            types.FunctionDeclaration(
                name="search_exercises",
                description="Search the exercise library by muscle group and equipment.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "search": types.Schema(type=types.Type.STRING, description="Exercise name"),
                        "muscle": types.Schema(type=types.Type.STRING, description="Target muscle group"),
                        "equipment": types.Schema(type=types.Type.STRING, description="Required equipment")
                    }
                )
            )
        ]
    )
]
"""
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 12: VISUAL INTERFACES, SCREENSHOTS & USER MANUAL
    # =========================================================================
    add_heading_1(doc, "Chapter 12: Visual Interfaces, Screenshots & User Manual")

    add_heading_2(doc, "12.1 Visual Interface Catalog")
    add_p(doc, "The following figures showcase the production user interfaces developed for AuraFIT, reflecting the editorial design system:")

    add_figure_box(doc, "12.1", "AuraFIT Landing Page Portal", "Responsive public landing page introducing the brand identity, clinical philosophy, and direct authentication entrypoints.")
    add_figure_box(doc, "12.2", "Biometric Onboarding & Goal Setup", "Multi-step interactive questionnaire capturing age, sex, weight, height, activity level, and dietary preference.")
    add_figure_box(doc, "12.3", "Daily Overview Dashboard", "Main dashboard featuring real-time radial macro progress rings (calories, protein, carbs, fat) and remaining targets.")
    add_figure_box(doc, "12.4", "Master Food Catalog & Multi-Criteria Search", "Interactive food search interface with Indian regional tags, filtering by macronutrient density and category.")
    add_figure_box(doc, "12.5", "Algorithmic 4-Bucket Meal Planner", "Scheduled daily meal distribution displaying breakfast, lunch, dinner, and snack allocations matching target macros.")
    add_figure_box(doc, "12.6", "AI Ingredient Swap Modal", "Contextual modal demonstrating instant food substitution (e.g., Paneer to Tofu) with verified macro parity.")
    add_figure_box(doc, "12.7", "Exercise Library with Muscle Group Filtering", "Visual exercise catalog categorizing movements by chest, back, legs, shoulders, and arms with biomechanical cues.")
    add_figure_box(doc, "12.8", "Active Workout Session Logger", "Interactive tracking sheet allowing users to input sets, completed reps, lifted weights, and calculate total session volume.")
    add_figure_box(doc, "12.9", "Conversational AI Fitness Coach (AICoachChat)", "Server-orchestrated chat drawer providing real-time personalized guidance and structured tool execution events.")
    add_figure_box(doc, "12.10", "Longitudinal Biometric Trends & Analytics", "Recharts visual analytics module graphing 30-day and 90-day body weight trajectories and caloric compliance.")

    add_heading_2(doc, "12.2 Operational User Manual & Step-by-Step Walkthrough")
    add_p(doc, "This operational guide outlines the core user procedures:")
    add_numbered(doc, "Step 1:", "Account Creation", "Navigate to `/register`, enter a valid email and strong password. Upon submission, the system hashes your password and establishes your session.")
    add_numbered(doc, "Step 2:", "Biometric Onboarding", "Enter your biological sex, age, current weight, height, daily activity multiplier, and primary fitness goal. AuraFIT computes your exact BMR and TDEE instantly.")
    add_numbered(doc, "Step 3:", "Daily Meal Tracking", "Navigate to `/nutrition`. Browse the verified catalog or select from your saved meals. As you log foods, your dashboard radial rings update in real time.")
    add_numbered(doc, "Step 4:", "Executing an AI Food Swap", "Click the 'Swap' icon beside any meal item. The AI assistant evaluates your diet and proposes a macro-equivalent alternative.")
    add_numbered(doc, "Step 5:", "Logging Workout Sessions", "Navigate to `/workouts`. Select your training routine, enter sets and repetitions, and click 'Save Workout' to update progressive volume.")
    add_numbered(doc, "Step 6:", "Consulting the AI Coach", "Open the AI Coach drawer. Ask questions such as 'What can I eat for high protein dinner under 400 kcal?' The coach queries verified database items.")
    add_numbered(doc, "Step 7:", "Reviewing Progress Analytics", "Navigate to `/analytics` to review your weight loss or muscle gain trajectory against your deterministic targets.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 13: LIMITATIONS, FUTURE ENHANCEMENTS & CONCLUSION
    # =========================================================================
    add_heading_1(doc, "Chapter 13: Limitations, Future Enhancements & Conclusion")

    add_heading_2(doc, "13.1 Technical and Operational Limitations")
    add_p(doc, "While AuraFIT successfully achieves its architectural and clinical goals, several real-world limitations exist:")
    add_numbered(doc, "1.", "External AI API Dependency", "The conversational coach requires real-time network connectivity to Google Gemini API servers; upstream network latencies can impact chat responses.")
    add_numbered(doc, "2.", "Manual Portion Size Logging", "Accuracy relies on user-estimated portion weights (e.g., estimating 150g cooked dal vs. 200g), which may introduce minor variances.")
    add_numbered(doc, "3.", "Online-First Architecture", "The application currently requires an active internet connection; full offline-first PWA sync with local IndexedDB is not yet active.")
    add_numbered(doc, "4.", "Lack of Hardware Sensor Synchronization", "Heart rate, step count, and active energy expenditure must be logged manually rather than syncing automatically via Bluetooth LE.")
    add_numbered(doc, "5.", "Regional Culinary Variance", "Homemade Indian recipes exhibit oil and sodium variations across households that can lead to minor micronutrient deviations.")
    add_numbered(doc, "6.", "Cold-Start Latency on Serverless Hosting", "On free-tier cloud containers, initial spin-up can experience an 8-12 second cold start delay after periods of dormancy.")
    add_numbered(doc, "7.", "Absence of Computer Vision Pose Detection", "Users assess exercise form through instructional guides rather than automated webcam biomechanical feedback.")
    add_numbered(doc, "8.", "Micro-Nutrient Depth", "The current database focuses on macronutrients (protein, carbs, fat, fiber); full tracking of vitamins and minerals is planned for future releases.")

    add_heading_2(doc, "13.2 Strategic Future Enhancements Roadmap")
    add_p(doc, "The strategic roadmap for future iterations of AuraFIT includes twelve major technical advancements:")
    add_numbered(doc, "1.", "Computer Vision Pose Estimation", "Deploy MediaPipe and WebAssembly to track joint angles via webcam, providing real-time exercise rep counting and posture correction.")
    add_numbered(doc, "2.", "Multimodal Food Photo Recognition", "Leverage Gemini 2.5 Vision to enable users to snap a photo of their plate, automatically estimating portion sizes and identifying ingredients.")
    add_numbered(doc, "3.", "Wearable Hardware Integration", "Build bi-directional APIs syncing with Apple HealthKit, Google Health Connect, Fitbit, and Whoop for continuous biometric monitoring.")
    add_numbered(doc, "4.", "Voice-Activated Workout & Meal Logging", "Integrate Web Speech API and Natural Language Understanding for hands-free logging during intense training sessions.")
    add_numbered(doc, "5.", "Offline Progressive Web App (PWA)", "Package AuraFIT as an installable PWA with Service Workers and SQLite/IndexedDB caching for zero-latency offline operation.")
    add_numbered(doc, "6.", "Community Leaderboards & Social Accountability", "Introduce peer accountability groups, group fitness challenges, and verified coach access.")
    add_numbered(doc, "7.", "Barcode Scanner Integration", "Implement camera-based barcode scanning for commercial packaged foods using open barcode databases.")
    add_numbered(doc, "8.", "Micronutrient & Blood Biomarker Correlation", "Enable uploading PDF blood reports (e.g., Vitamin D, B12, lipid profile) with AI-customized dietary recommendations.")
    add_numbered(doc, "9.", "Multilingual Regional Localization", "Translate the user interface and food naming into regional Indian languages (Hindi, Bengali, Tamil, Telugu).")
    add_numbered(doc, "10.", "Predictive Machine Learning Weight Forecasting", "Deploy regression models predicting goal completion dates based on 30-day compliance trends.")
    add_numbered(doc, "11.", "Automated Grocery Delivery Integration", "Generate smart grocery lists from meal plans with one-click export to quick-commerce delivery APIs (Blinkit, Zepto, Instacart).")
    add_numbered(doc, "12.", "Personalized Water & Hydration Tracking", "Dynamic fluid intake calculations based on ambient temperature, workout sweat rate, and body mass.")

    add_heading_2(doc, "13.3 Project Summary & Academic Conclusion")
    add_p(doc, "The AuraFIT major project demonstrates the power of combining deterministic scientific arithmetic with modern generative artificial intelligence. By refusing to compromise on mathematical rigor while embracing conversational flexibility, AuraFIT resolves the critical flaws that plague modern fitness platforms: AI hallucinations, cultural exclusion, and platform fragmentation.")
    add_p(doc, "Built upon a robust, decoupled technology stack—React, TypeScript, Tailwind CSS, Python, FastAPI, MongoDB Atlas, and Google Gemini API—AuraFIT represents a complete, production-grade digital health solution. This project has been an invaluable practical capstone in enterprise software architecture, full-stack web engineering, and responsible AI system design.")

    add_heading_2(doc, "References & Bibliography")
    add_numbered(doc, "[1]", "Mifflin, M. D., St Jeor, S. T., et al.", "'A new predictive equation for resting energy expenditure in healthy individuals.' The American Journal of Clinical Nutrition, 51(2), 241-247, 1990.")
    add_numbered(doc, "[2]", "FastAPI Framework Documentation", "Tiangolo, S., 'FastAPI: Modern, fast (high-performance), web framework for building APIs with Python 3.8+', https://fastapi.tiangolo.com/, 2024.")
    add_numbered(doc, "[3]", "Google Gemini API Documentation", "Google Cloud AI, 'Gemini API Function Calling and Structured Outputs Guide', https://ai.google.dev/, 2024.")
    add_numbered(doc, "[4]", "MongoDB Documentation", "MongoDB Inc., 'MongoDB Atlas Cloud Database Manual and BSON Data Modeling', https://www.mongodb.com/docs/, 2024.")
    add_numbered(doc, "[5]", "React 18 & TypeScript Guide", "Meta Open Source, 'React Documentation: The library for web and native user interfaces', https://react.dev/, 2024.")
    add_numbered(doc, "[6]", "Indian Food Composition Tables (IFCT)", "National Institute of Nutrition (ICMR), 'Nutritive Value of Indian Foods', Hyderabad, India, 2017.")
    add_numbered(doc, "[7]", "Schoenfeld, B. J.", "'The mechanisms of muscle hypertrophy and their application to resistance training.' Journal of Strength and Conditioning Research, 24(10), 2857-2872, 2010.")
