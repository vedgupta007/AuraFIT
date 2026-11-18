# -*- coding: utf-8 -*-
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_generator.helpers import (
    add_heading_1, add_heading_2, add_heading_3, add_p, add_bullet, add_numbered, create_table, add_code_block
)

def build_chapters_7_to_9(doc):
    # =========================================================================
    # CHAPTER 7: DATABASE ARCHITECTURE & DATA DICTIONARY
    # =========================================================================
    add_heading_1(doc, "Chapter 7: Database Architecture & Data Dictionary")

    add_heading_2(doc, "7.1 Cloud NoSQL Document Architecture (MongoDB Atlas)")
    add_p(doc, "AuraFIT utilizes MongoDB Atlas—a fully managed, distributed NoSQL document database. Traditional relational database management systems (RDBMS) impose rigid tabular schemas that struggle with highly polymorphic, hierarchical health data (such as custom meal recipes with dynamic ingredient arrays, or resistance workouts with varying set, repetition, and weight parameters). In contrast, MongoDB represents entities as rich BSON (Binary JSON) documents, mapping naturally to TypeScript interfaces on the client and Pydantic models on the backend.")

    add_heading_2(doc, "7.2 Comprehensive Data Dictionaries (10 Collections)")
    add_p(doc, "The following tables define the formal data dictionaries for all ten collections within the AuraFIT database cluster:")

    add_heading_3(doc, "Table 7.1: Users Collection Schema (`users`)")
    add_p(doc, "Stores core authentication credentials, role assignments, and account lifecycle metadata.")
    u_headers = ["Field Name", "Data Type", "Constraints & Validation", "Description & Rationale"]
    u_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique 12-byte BSON identifier for the user account."],
        ["email", "String", "Unique, Indexed, Valid Email Format", "User login identifier and communication address."],
        ["password_hash", "String", "Not Null, Argon2id Hash String", "Cryptographically secure password digest (Argon2)."],
        ["role", "String", "Enum: 'user', 'admin', 'coach'", "Authorization role governing RBAC access levels."],
        ["is_active", "Boolean", "Default: True", "Flag indicating whether account has active login privileges."],
        ["created_at", "DateTime", "Default: Current UTC Timestamp", "Timestamp of initial registration."],
        ["updated_at", "DateTime", "Default: Current UTC Timestamp", "Timestamp of most recent account modification."]
    ]
    create_table(doc, u_headers, u_data, [Inches(1.5), Inches(1.1), Inches(1.8), Inches(2.1)])

    add_heading_3(doc, "Table 7.2: Profiles Collection Schema (`profiles`)")
    add_p(doc, "Encapsulates physical biometrics, dietary preferences, and system-calculated metabolic targets.")
    p_headers = ["Field Name", "Data Type", "Constraints & Validation", "Description & Rationale"]
    p_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for the biometric profile."],
        ["user_id", "ObjectId", "Foreign Key (users._id), Unique, Indexed", "Reference to the parent user account."],
        ["age", "Integer", "Min: 13, Max: 100, Required", "Chronological age in years (used in BMR formula)."],
        ["sex", "String", "Enum: 'M', 'F', Required", "Biological sex required for Mifflin-St Jeor constant."],
        ["height_cm", "Float", "Min: 100.0, Max: 250.0, Required", "Height in centimeters."],
        ["weight_kg", "Float", "Min: 30.0, Max: 300.0, Required", "Current body weight in kilograms."],
        ["activity_level", "String", "Enum: sedentary, light, moderate, active", "Physical activity multiplier applied to BMR."],
        ["goal", "String", "Enum: fat_loss, maintenance, muscle_gain", "Primary fitness goal dictating caloric delta."],
        ["dietary_pref", "String", "Enum: vegetarian, vegan, non_veg", "Dietary boundary for food recommendations."],
        ["allergens", "Array[String]", "Optional", "List of excluded allergen tags (e.g., dairy, peanuts)."],
        ["bmr", "Float", "Deterministic Calculated", "Basal Metabolic Rate in kcal/day."],
        ["tdee", "Float", "Deterministic Calculated", "Total Daily Energy Expenditure in kcal/day."],
        ["daily_calories", "Float", "Deterministic Calculated", "Final daily calorie target based on goal delta."],
        ["protein_g", "Float", "Deterministic Calculated (2.0g/kg)", "Daily target protein intake in grams."],
        ["carbs_g", "Float", "Deterministic Calculated", "Daily target carbohydrate intake in grams."],
        ["fat_g", "Float", "Deterministic Calculated (0.8g/kg)", "Daily target dietary fat intake in grams."]
    ]
    create_table(doc, p_headers, p_data, [Inches(1.5), Inches(1.1), Inches(1.8), Inches(2.1)])

    add_heading_3(doc, "Table 7.3: Master Foods Catalog Schema (`foods`)")
    add_p(doc, "The authoritative master database of raw and cooked ingredients with validated nutritional facts.")
    f_headers = ["Field Name", "Data Type", "Constraints & Validation", "Description & Rationale"]
    f_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for the food item."],
        ["name", "String", "Not Null, Text Indexed", "Food name (e.g., 'Paneer', 'Moong Dal Tadka')."],
        ["category", "String", "Enum: Grains, Dairy, Legumes, Meats", "Nutritional categorization for search grouping."],
        ["serving_size_g", "Float", "Default: 100.0g, Required", "Standard reference portion in grams."],
        ["calories", "Float", "Min: 0.0, Required", "Energy content per 100g serving."],
        ["protein_g", "Float", "Min: 0.0, Required", "Protein content per 100g serving."],
        ["carbs_g", "Float", "Min: 0.0, Required", "Carbohydrate content per 100g serving."],
        ["fat_g", "Float", "Min: 0.0, Required", "Fat content per 100g serving."],
        ["fiber_g", "Float", "Min: 0.0, Optional", "Dietary fiber content per 100g serving."],
        ["tags", "Array[String]", "Indexed (e.g., 'indian', 'high_protein')", "Searchable classification tags."],
        ["allergens", "Array[String]", "e.g., ['dairy', 'nuts', 'gluten']", "Allergenic components for safety filtering."],
        ["is_indian", "Boolean", "Default: True", "Flag identifying regional South Asian cuisine items."]
    ]
    create_table(doc, f_headers, f_data, [Inches(1.5), Inches(1.1), Inches(1.8), Inches(2.1)])

    add_heading_3(doc, "Table 7.4: Master Exercises Catalog Schema (`exercises`)")
    add_p(doc, "Curated catalog of multi-joint compound and isolation exercises with biomechanical execution details.")
    e_headers = ["Field Name", "Data Type", "Constraints & Validation", "Description & Rationale"]
    e_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for the exercise."],
        ["name", "String", "Unique, Not Null, Text Indexed", "Name of exercise (e.g., 'Barbell Deadlift')."],
        ["muscle_group", "String", "Enum: Chest, Back, Legs, Shoulders, Core", "Primary anatomical target."],
        ["secondary_muscles", "Array[String]", "Optional", "Auxiliary stabilizing muscle groups."],
        ["equipment", "String", "Enum: barbell, dumbbell, machine, bodyweight", "Equipment required for execution."],
        ["difficulty", "String", "Enum: beginner, intermediate, advanced", "Technical complexity rating."],
        ["instructions", "Array[String]", "Not Null", "Step-by-step biomechanical movement cues."],
        ["video_url", "String", "Optional, Valid URL", "Demonstration video reference."]
    ]
    create_table(doc, e_headers, e_data, [Inches(1.5), Inches(1.1), Inches(1.8), Inches(2.1)])

    add_heading_3(doc, "Table 7.5: Meal Plans Collection Schema (`meal_plans`)")
    add_p(doc, "Structured daily schedules generated by the 4-bucket greedy algorithm or customized by users.")
    mp_headers = ["Field Name", "Data Type", "Constraints & Validation", "Description & Rationale"]
    mp_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for the meal plan document."],
        ["user_id", "ObjectId", "Foreign Key (users._id), Indexed", "User to whom the plan is assigned."],
        ["date", "Date", "Required, Indexed", "Calendar date for plan execution."],
        ["meals", "Array[Object]", "Required (Breakfast, Lunch, Dinner, Snack)", "Array of meal bucket objects containing food items."],
        ["total_calories", "Float", "Aggregated", "Sum of calories across all four meal buckets."],
        ["total_protein_g", "Float", "Aggregated", "Sum of protein grams across meals."],
        ["total_carbs_g", "Float", "Aggregated", "Sum of carbohydrate grams across meals."],
        ["total_fat_g", "Float", "Aggregated", "Sum of fat grams across meals."]
    ]
    create_table(doc, mp_headers, mp_data, [Inches(1.5), Inches(1.1), Inches(1.8), Inches(2.1)])

    add_heading_3(doc, "Table 7.6: Saved Meals Collection Schema (`saved_meals`)")
    add_p(doc, "Stores user-defined custom recipes, composite dishes, and quick-log favorites.")
    sm_headers = ["Field Name", "Data Type", "Constraints & Validation", "Description & Rationale"]
    sm_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for saved meal."],
        ["user_id", "ObjectId", "Foreign Key (users._id), Indexed", "Owner user account."],
        ["meal_name", "String", "Not Null, Max: 100 chars", "User label (e.g., 'Post-Workout High Protein Shake')."],
        ["meal_type", "String", "Enum: breakfast, lunch, dinner, snack", "Categorical meal timing."],
        ["calories", "Float", "Min: 0.0, Required", "Total caloric content."],
        ["protein_grams", "Float", "Min: 0.0, Required", "Total protein grams."],
        ["carbs_grams", "Float", "Min: 0.0, Required", "Total carbohydrate grams."],
        ["fat_grams", "Float", "Min: 0.0, Required", "Total fat grams."],
        ["ingredients", "Array[Object]", "Not Null", "Embedded list of ingredient IDs and amounts."]
    ]
    create_table(doc, sm_headers, sm_data, [Inches(1.5), Inches(1.1), Inches(1.8), Inches(2.1)])

    add_heading_3(doc, "Table 7.7: Workout Plans Collection Schema (`workout_plans`)")
    add_p(doc, "Prescribed resistance routines specifying target exercises, split allocations, and sets/reps.")
    wp_headers = ["Field Name", "Data Type", "Constraints & Validation", "Description & Rationale"]
    wp_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for the workout plan."],
        ["user_id", "ObjectId", "Foreign Key (users._id), Indexed", "Assigned user account."],
        ["routine_name", "String", "Not Null (e.g., 'Push Day Hypertrophy')", "Descriptive split title."],
        ["day_of_week", "Integer", "Range: 1 (Monday) to 7 (Sunday)", "Scheduled execution day."],
        ["exercises", "Array[Object]", "Required", "List of exercise IDs, target sets, and rep ranges."]
    ]
    create_table(doc, wp_headers, wp_data, [Inches(1.5), Inches(1.1), Inches(1.8), Inches(2.1)])

    add_heading_3(doc, "Table 7.8: Daily Tracking Logs Schema (`daily_logs`)")
    add_p(doc, "Continuous timestamped log recording real-world nutritional compliance and workout completion.")
    dl_headers = ["Field Name", "Data Type", "Constraints & Validation", "Description & Rationale"]
    dl_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for daily log record."],
        ["user_id", "ObjectId", "Foreign Key (users._id), Compound Indexed", "User identifier."],
        ["date", "Date", "Compound Indexed with user_id", "Calendar date of tracking."],
        ["consumed_items", "Array[Object]", "Default: []", "Array of logged food items with portion amounts."],
        ["total_calories", "Float", "Default: 0.0", "Accumulated calories consumed."],
        ["workout_done", "Boolean", "Default: False", "Flag indicating workout session completion."],
        ["water_intake_ml", "Integer", "Default: 0", "Daily fluid consumption in milliliters."]
    ]
    create_table(doc, dl_headers, dl_data, [Inches(1.5), Inches(1.1), Inches(1.8), Inches(2.1)])

    add_heading_3(doc, "Table 7.9: Body Measurements Schema (`measurements`)")
    add_p(doc, "Stores longitudinal physical transformation metrics for graphical trend analysis.")
    bm_headers = ["Field Name", "Data Type", "Constraints & Validation", "Description & Rationale"]
    bm_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for measurement entry."],
        ["user_id", "ObjectId", "Foreign Key (users._id), Indexed", "Associated user account."],
        ["date", "Date", "Required, Indexed", "Date of physical weigh-in."],
        ["weight_kg", "Float", "Required, > 0", "Morning fasted body weight in kg."],
        ["waist_cm", "Float", "Optional", "Waist circumference at navel in cm."],
        ["body_fat_pct", "Float", "Optional, Range: 3.0 to 60.0%", "Estimated body fat percentage."]
    ]
    create_table(doc, bm_headers, bm_data, [Inches(1.5), Inches(1.1), Inches(1.8), Inches(2.1)])

    add_heading_3(doc, "Table 7.10: Gamification Achievements Schema (`achievements`)")
    add_p(doc, "Tracks motivational milestones, consistency streaks, and unlocked badges.")
    ac_headers = ["Field Name", "Data Type", "Constraints & Validation", "Description & Rationale"]
    ac_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for achievement record."],
        ["user_id", "ObjectId", "Foreign Key (users._id), Indexed", "User awarded the achievement."],
        ["badge_code", "String", "e.g., 'STREAK_7_DAYS', 'MACRO_MASTER'", "Unique badge code identifier."],
        ["title", "String", "Not Null", "Human-readable badge name."],
        ["unlocked_at", "DateTime", "Default: Current UTC Timestamp", "Date and time of achievement unlock."]
    ]
    create_table(doc, ac_headers, ac_data, [Inches(1.5), Inches(1.1), Inches(1.8), Inches(2.1)])

    add_heading_2(doc, "7.3 Database Indexing & Query Optimization Strategy")
    add_p(doc, "To maintain sub-50ms query response times under high concurrency, AuraFIT implements targeted compound indexes in MongoDB Atlas:")
    add_bullet(doc, "Daily Log Query Index", "`{ user_id: 1, date: -1 }` ensures instantaneous retrieval of today's tracking data and historical timeline scans.")
    add_bullet(doc, "Food Search Compound Index", "`{ tags: 1, protein_g: -1 }` enables instantaneous filtering of high-protein Indian foods matching user dietary preferences.")
    add_bullet(doc, "Text Search Index", "`{ name: 'text', brand: 'text' }` on the `foods` collection powers full-text fuzzy search across thousands of food items.")

    add_heading_2(doc, "7.4 Data Normalization vs. Embedding Decisions in NoSQL")
    add_p(doc, "AuraFIT balances normalization and embedding based on query access patterns:")
    add_bullet(doc, "Embedded Sub-documents", "Ingredients inside `saved_meals` and individual sets inside `workout_logs` are embedded directly, ensuring single-document atomic reads without costly joins.")
    add_bullet(doc, "Referenced Documents", "User IDs are normalized as foreign references across `profiles`, `daily_logs`, and `saved_meals`, preventing data duplication and maintaining referential consistency.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: RESTFUL API SPECIFICATIONS & ENDPOINTS
    # =========================================================================
    add_heading_1(doc, "Chapter 8: RESTful API Specifications & Endpoint Contracts")

    add_heading_2(doc, "8.1 API Architectural Design & OpenAPI Standards")
    add_p(doc, "The AuraFIT backend exposes an asynchronous RESTful API fully conforming to OpenAPI 3.1 and JSON:API standards. All API endpoints reside under the `/api/v1` namespace. Requests transmitting payload bodies use `application/json`, and errors follow the RFC 7807 Problem Details specification:")
    add_code_block(doc,
"""
RFC 7807 Error Response Schema:
{
  "type": "https://aurafit.com/errors/invalid-credentials",
  "title": "Authentication Failed",
  "status": 401,
  "detail": "The password supplied does not match our records.",
  "instance": "/api/v1/auth/login"
}
"""
    )

    add_heading_2(doc, "8.2 Authentication & User Endpoints")
    add_p(doc, "Table 8.1 documents the authentication and session management endpoints:")
    a_headers = ["HTTP Method & Route", "Auth Required", "Request Body Payload", "Response Status & Schema"]
    a_data = [
        ["POST /api/v1/auth/register", "None", "{ email: str, password: str }", "201 Created -> { id, email, access_token }"],
        ["POST /api/v1/auth/login", "None", "{ email: str, password: str }", "200 OK -> { access_token, token_type: 'bearer' }"],
        ["POST /api/v1/auth/refresh", "Refresh Cookie", "None (HttpOnly Cookie)", "200 OK -> { access_token }"],
        ["POST /api/v1/auth/logout", "Bearer JWT", "None", "200 OK -> { message: 'Logged out successfully' }"]
    ]
    create_table(doc, a_headers, a_data, [Inches(2.2), Inches(1.1), Inches(1.8), Inches(1.4)])

    add_heading_2(doc, "8.3 Biometric Profile & Target Endpoints")
    add_p(doc, "Table 8.2 documents the profile onboarding and deterministic target calculation endpoints:")
    pr_headers = ["HTTP Method & Route", "Auth Required", "Request Body Payload", "Response Status & Schema"]
    pr_data = [
        ["GET /api/v1/profile/me", "Bearer JWT", "None", "200 OK -> Full ProfileSchema with BMR & Macros"],
        ["POST /api/v1/profile", "Bearer JWT", "ProfileCreate (age, sex, height, weight...)", "201 Created -> ProfileResponse with calculated targets"],
        ["PUT /api/v1/profile/me", "Bearer JWT", "ProfileUpdate (partial fields)", "200 OK -> Triggers recalculation & returns Profile"],
        ["GET /api/v1/nutrition/targets", "Bearer JWT", "None", "200 OK -> { calories, protein_g, carbs_g, fat_g }"]
    ]
    create_table(doc, pr_headers, pr_data, [Inches(2.2), Inches(1.1), Inches(1.8), Inches(1.4)])

    add_heading_2(doc, "8.4 Master Foods & Nutrition Plan Endpoints")
    add_p(doc, "Table 8.3 documents the food catalog querying and meal logging endpoints:")
    fd_headers = ["HTTP Method & Route", "Auth Required", "Query Parameters / Body", "Response Status & Schema"]
    fd_data = [
        ["GET /api/v1/foods", "Bearer JWT", "?q=str&diet=str&category=str", "200 OK -> List[FoodSchema]"],
        ["POST /api/v1/nutrition/saved-meals", "Bearer JWT", "SavedMealCreate { meal_name, ingredients... }", "201 Created -> SavedMealResponse"],
        ["GET /api/v1/nutrition/saved-meals", "Bearer JWT", "None", "200 OK -> List[SavedMealResponse]"],
        ["DELETE /api/v1/nutrition/saved-meals/{id}", "Bearer JWT", "Path: meal_id", "204 No Content -> Deletion confirmed"],
        ["POST /api/v1/plans/meals/generate", "Bearer JWT", "{ date: 'YYYY-MM-DD' }", "200 OK -> 4-Bucket Algorithmic MealPlanSchema"]
    ]
    create_table(doc, fd_headers, fd_data, [Inches(2.2), Inches(1.1), Inches(1.8), Inches(1.4)])

    add_heading_2(doc, "8.5 Exercises & Workout Logging Endpoints")
    add_p(doc, "Table 8.4 documents the exercise catalog and resistance workout logging endpoints:")
    ex_headers = ["HTTP Method & Route", "Auth Required", "Query Parameters / Body", "Response Status & Schema"]
    ex_data = [
        ["GET /api/v1/exercises", "Bearer JWT", "?muscle=str&equipment=str", "200 OK -> List[ExerciseSchema]"],
        ["POST /api/v1/workouts", "Bearer JWT", "WorkoutCreate { name, exercises... }", "201 Created -> WorkoutResponse"],
        ["GET /api/v1/workouts", "Bearer JWT", "?limit=20&skip=0", "200 OK -> List[WorkoutResponse]"],
        ["POST /api/v1/workouts/log", "Bearer JWT", "{ exercise_id, sets: [{ reps, weight }] }", "201 Created -> Aggregated Volume Log"]
    ]
    create_table(doc, ex_headers, ex_data, [Inches(2.2), Inches(1.1), Inches(1.8), Inches(1.4)])

    add_heading_2(doc, "8.6 Conversational AI Coach Endpoint")
    add_p(doc, "Table 8.5 documents the Google Gemini AI coaching endpoints:")
    ai_headers = ["HTTP Method & Route", "Auth Required", "Request Body Payload", "Response Status & Schema"]
    ai_data = [
        ["POST /api/v1/ai/chat", "Bearer JWT", "{ message: str, conversation_id: str }", "200 OK -> { answer, structured_data, tool_events }"],
        ["GET /api/v1/ai/conversations", "Bearer JWT", "None", "200 OK -> List[ConversationSummary]"],
        ["DELETE /api/v1/ai/conversations/{id}", "Bearer JWT", "Path: conversation_id", "204 No Content -> Conversation deleted"]
    ]
    create_table(doc, ai_headers, ai_data, [Inches(2.2), Inches(1.1), Inches(1.8), Inches(1.4)])

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 9: SYSTEM DEVELOPMENT LIFE CYCLE & PROJECT MANAGEMENT
    # =========================================================================
    add_heading_1(doc, "Chapter 9: System Development Life Cycle (SDLC) & Project Management")

    add_heading_2(doc, "9.1 Agile Scrum Methodology & Sprint Cadence")
    add_p(doc, "AuraFIT was developed following the Agile Scrum methodology, employing two-week iterative sprint cycles. Scrum was selected over traditional Waterfall models because modern full-stack development—especially involving external generative AI APIs—requires continuous empirical feedback, rapid prototyping, and architectural pivots.")

    add_heading_2(doc, "9.2 Work Breakdown Structure (WBS) & Milestones")
    add_p(doc, "The project was decomposed into five major milestones:")
    add_bullet(doc, "Milestone 1: Architectural Blueprint & Schema Definitions (Week 3)", "Delivery of formal SRS, MongoDB schemas, and OpenAPI contracts.")
    add_bullet(doc, "Milestone 2: Deterministic Core & Auth API (Week 6)", "FastAPI backend operational with Mifflin-St Jeor math and Argon2 authentication.")
    add_bullet(doc, "Milestone 3: React SPA & UI Design System (Week 9)", "Frontend operational with Tailwind design tokens, TanStack Query, and onboarding.")
    add_bullet(doc, "Milestone 4: AI Gemini Orchestrator & Tool Binding (Week 12)", "Function calling integration complete with macro-equivalent ingredient swapping.")
    add_bullet(doc, "Milestone 5: Multi-Stage Testing & Production Deployment (Week 15)", "Full testing, documentation, and cloud deployment complete.")

    add_heading_2(doc, "9.3 Project Scheduling & Phase Breakdown Timeline")
    add_p(doc, "Table 9.2 details the project scheduling across the academic semester:")
    sch_headers = ["Phase", "Start Date", "End Date", "Duration", "Key Deliverable"]
    sch_data = [
        ["1. Requirements Gathering", "01/09/2026", "07/09/2026", "1 week", "SRS Document & Clinical Nutrition Specs"],
        ["2. Architecture & DB Design", "08/09/2026", "21/09/2026", "2 weeks", "MongoDB Atlas Schemas & DFD Diagrams"],
        ["3. Frontend SPA Development", "22/09/2026", "12/10/2026", "3 weeks", "React / Vite / Tailwind AppShell & Pages"],
        ["4. Backend API & Math Engine", "13/10/2026", "02/11/2026", "3 weeks", "FastAPI Routes, Argon2 Auth, BMR Logic"],
        ["5. AI Engine & Tool Calling", "03/11/2026", "16/11/2026", "2 weeks", "Google Gemini Integration & Tool Schemas"],
        ["6. Multi-Stage QA & Testing", "17/11/2026", "30/11/2026", "2 weeks", "Pytest Suite, Vitest, Security Audit"],
        ["7. UAT & Final Deployment", "01/12/2026", "15/12/2026", "2 weeks", "Live Deployment & Academic Documentation"]
    ]
    create_table(doc, sch_headers, sch_data, [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.5)])

    add_heading_2(doc, "9.4 Effort Estimation & Person-Hour Allocations")
    add_p(doc, "Table 9.3 outlines the person-hour effort distribution across development phases, totaling 940 dedicated hours:")
    eff_headers = ["Phase", "Frontend Effort", "Backend Effort", "AI & QA Effort", "Total Hours"]
    eff_data = [
        ["Phase 1: Requirements Gathering", "10 hours", "20 hours", "10 hours", "40 hours"],
        ["Phase 2: Architecture & DB Design", "30 hours", "60 hours", "30 hours", "120 hours"],
        ["Phase 3: Frontend SPA Development", "160 hours", "20 hours", "20 hours", "200 hours"],
        ["Phase 4: Backend REST API & Math", "20 hours", "160 hours", "40 hours", "220 hours"],
        ["Phase 5: AI Engine & Tool Calling", "30 hours", "50 hours", "60 hours", "140 hours"],
        ["Phase 6: Multi-Stage Testing", "30 hours", "40 hours", "50 hours", "120 hours"],
        ["Phase 7: UAT & Documentation", "20 hours", "30 hours", "30 hours", "80 hours"],
        ["Aggregate Project Total", "300 hours", "380 hours", "240 hours", "940 hours"]
    ]
    create_table(doc, eff_headers, eff_data, [Inches(2.2), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.0)])

    doc.add_page_break()
