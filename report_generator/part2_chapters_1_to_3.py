# -*- coding: utf-8 -*-
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_generator.helpers import (
    add_heading_1, add_heading_2, add_heading_3, add_p, add_bullet, add_numbered, create_table, add_code_block
)

def build_chapters_1_to_3(doc):
    # =========================================================================
    # CHAPTER 1: PROBLEM DEFINITION & INTRODUCTION
    # =========================================================================
    add_heading_1(doc, "Chapter 1: Problem Definition & Introduction")

    add_heading_2(doc, "1.1 Digital Health & Fitness Industry Overview")
    add_p(doc, "In the modern era, lifestyle-related non-communicable diseases—such as Type 2 diabetes, hypertension, cardiovascular ailments, obesity, and polycystic ovarian syndrome (PCOS)—have reached epidemic proportions globally. Rapid urbanization, sedentary office desk environments, highly processed dietary habits, and chronic sleep deprivation have created an unprecedented public health crisis. In response, millions of individuals turn to digital health technologies and mobile fitness applications seeking guidance for body recomposition, weight management, and physical conditioning.")

    add_p(doc, "The global digital fitness and nutrition market has experienced exponential expansion, projected to exceed tens of billions of dollars over the coming decade. However, despite the proliferation of hundreds of thousands of health applications across major app stores, global health metrics continue to deteriorate, and user churn rates remain extraordinarily high. Over 80% of individuals who download commercial fitness applications abandon them within thirty days. A profound dissonance exists between the marketing promises of modern digital wellness platforms and the real-world biological results delivered to end users.")

    add_heading_2(doc, "1.2 Critical Deficiencies in Contemporary Fitness Solutions")
    add_p(doc, "A comprehensive investigative analysis of existing commercial health platforms reveals four systemic, architectural flaws that severely undermine their long-term efficacy and safety:")

    add_heading_3(doc, "1.2.1 Generic Static Calorie & Macro Templates")
    add_p(doc, "Most commercial fitness applications rely on primitive, static heuristics. Users are forced into arbitrary caloric targets (such as universal 1,200 kcal diets for women or 2,000 kcal diets for men) without accounting for their exact Basal Metabolic Rate (BMR), biological sex, lean mass ratio, non-exercise activity thermogenesis (NEAT), or endocrine adaptations. These one-size-fits-all regimens frequently trigger metabolic slowdown, lean muscle loss, hormonal dysregulation, and psychological binge-restrict cycles.")

    add_heading_3(doc, "1.2.2 The Phenomenon and Clinical Hazards of LLM Hallucinations in Health")
    add_p(doc, "With the explosive rise of Large Language Models (LLMs) such as OpenAI's ChatGPT, Anthropic's Claude, and Google's Gemini, fitness startups have rushed to deploy conversational chatbots as automated nutritionists. However, LLMs are fundamentally non-deterministic probabilistic text prediction engines. They lack intrinsic arithmetic reasoning.")
    add_p(doc, "When asked to formulate daily meal plans, commercial LLM chatbots regularly exhibit dangerous hallucinations. They invent fictitious calorie amounts, output macronutrient combinations that violate the laws of physics (e.g., claiming a meal contains 50g of protein, 20g of carbohydrates, and 10g of fat yet totals 800 kilocalories instead of the mathematically true 370 kilocalories), or recommend dangerous starvation diets. In medical and clinical fitness contexts, arithmetic hallucinations pose severe physical risks to users.")

    add_heading_3(doc, "1.2.3 Cultural Bias and Inadequacy in Global Nutrition Databases")
    add_p(doc, "The world's leading diet tracking platforms—such as MyFitnessPal, LoseIt, and Cronometer—were developed with Western culinary traditions as their primary reference point. Their underlying nutritional databases are heavily saturated with western staples (e.g., chicken breasts, oatmeal, Greek yogurt, canned tuna, and commercial packaged snack foods).")
    add_p(doc, "These platforms fail catastrophically when applied to Indian, South Asian, and regional dietary traditions. Indian cuisine is characterized by complex composite cooking methods involving varied pulses (moong, toor, urad, chana), fermented batters (idli, dosa), paneer, varied cooking oils and ghee, and multi-grain flatbreads (roti, paratha, bajra). Existing platforms either lack verified Indian items entirely or depend on unmoderated crowdsourced entries riddled with extreme errors (e.g., one user logging a single roti as 50 calories and another logging it as 400 calories). Consequently, Indian users find tracking impossible without abandoning their cultural diet.")

    add_heading_3(doc, "1.2.4 Fragmentation of Diet, Workout, and Consultation Platforms")
    add_p(doc, "Currently, a fitness enthusiast must maintain a fragmented ecosystem: one application for tracking calories and food intake, a second spreadsheet or mobile app for logging weightlifting sets and progressive overload, a third for tracking body measurements, and external messaging channels to consult human trainers. This administrative friction causes cognitive overload and rapidly leads to user abandonment.")

    add_heading_2(doc, "1.3 Introduction to the AuraFIT Architecture")
    add_p(doc, "To resolve these systemic flaws, this major project conceptualizes, designs, and implements AuraFIT—an enterprise-grade, culturally aware, AI-powered fitness and nutrition platform. AuraFIT is architected upon a foundational engineering philosophy:")

    add_p(doc, "“Strict Separation of Concerns: Deterministic Clinical Arithmetic for Metabolic Calculations, Paired with Guardrailed Generative AI for Contextual Synthesis and Conversational Coaching.”", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc, "In AuraFIT, all metabolic calculations—including Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), and granular macronutrient splits (grams of protein, carbohydrates, and fats)—are strictly executed by deterministic, mathematically proven Python backend routines based on the Mifflin-St Jeor formula. The Large Language Model (Google Gemini API) is explicitly barred from generating or altering baseline nutritional arithmetic.")
    add_p(doc, "Instead, Google Gemini operates as an intelligent orchestrator via server-side Function Calling (Tools). When a user requests a meal substitution, an exercise adaptation, or general fitness advice, the backend injects the user's verified biometric context and binds Gemini to authoritative database search tools. Gemini selects verified database items, and the backend verifies macro parity before updating the user's plan. This hybrid architecture completely eliminates nutritional hallucinations while preserving the fluid, empathetic nature of conversational AI.")

    add_heading_2(doc, "1.4 Need for the AuraFIT Platform")
    add_p(doc, "The development of AuraFIT addresses several critical societal and engineering needs:")
    add_bullet(doc, "Deterministic Mathematical Rigor", "Guarantees 100% mathematical accuracy across all caloric and macronutrient recommendations, ensuring user safety and metabolic sustainability.")
    add_bullet(doc, "Comprehensive Indian & Global Food Database", "Provides a rich, verified library of regional Indian dishes alongside international staples, enabling diverse populations to achieve fitness goals eating foods they love.")
    add_bullet(doc, "Smart Macro-Equivalent Ingredient Swapping", "Allows users to seamlessly swap ingredients or whole meals when dining out or facing pantry shortages, with the system maintaining identical macronutrient balances.")
    add_bullet(doc, "Progressive Overload Workout Tracking", "Bridges the gap between nutrition and strength training by providing an integrated resistance exercise tracker that records volume, sets, reps, and muscle stimulation.")
    add_bullet(doc, "Zero-Knowledge API Privacy Architecture", "Protects user data and corporate API secrets by routing all Gemini AI queries through secure backend micro-services, never exposing proprietary keys to client browsers.")
    add_bullet(doc, "Democratization of Elite Coaching", "Offers round-the-clock, personalized, empathetic fitness guidance at virtually zero marginal cost, making evidence-based coaching accessible to all.")

    add_heading_2(doc, "1.5 Purpose and Architectural Scope")
    add_p(doc, "The purpose of this project is to build an end-to-end, full-stack, production-grade web platform utilizing modern decoupled software architecture. The scope of AuraFIT encompasses:")
    add_numbered(doc, "1.", "Presentation Layer", "A modern, highly responsive Single Page Application (SPA) built with React 18, TypeScript, Tailwind CSS, TanStack Query, and Lucide Icons, adhering to an elegant 'Editorial Fitness' design system.")
    add_numbered(doc, "2.", "API & Business Logic Layer", "A high-performance asynchronous RESTful API built with Python 3.10+ and FastAPI, leveraging Pydantic v2 schemas for rigid runtime data validation.")
    add_numbered(doc, "3.", "Persistence Layer", "A scalable cloud NoSQL document database powered by MongoDB Atlas, utilizing the async Motor driver for non-blocking I/O operations.")
    add_numbered(doc, "4.", "Intelligent Orchestration Layer", "A secure backend integration with Google Gemini 2.5/Flash, implementing structured function calling and prompt engineering guardrails.")
    add_numbered(doc, "5.", "Analytical Dashboard", "Interactive visual progress charts powered by Recharts, graphing weight trends, daily caloric compliance, and muscle volume progression.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: PROJECT OBJECTIVES & REQUIREMENTS SPECIFICATION
    # =========================================================================
    add_heading_1(doc, "Chapter 2: Project Objectives & Requirements Specification")

    add_heading_2(doc, "2.1 Core Project Objectives")
    add_p(doc, "The core engineering and clinical objectives of the AuraFIT project are categorized into four distinct domains:")
    add_bullet(doc, "User Experience Objectives", "Design a distraction-free, aesthetically refined interface that eliminates the cognitive friction of manual calorie counting and workout logging.")
    add_bullet(doc, "Algorithmic Precision Objectives", "Implement clinically validated formulas (Mifflin-St Jeor, Physical Activity Level multipliers, and 4-bucket greedy meal balancing) with zero mathematical error.")
    add_bullet(doc, "AI Safety & Reliability Objectives", "Constrain generative AI capabilities strictly to conversational synthesis and tool orchestration, establishing programmatic guardrails against hallucinations.")
    add_bullet(doc, "Architectural Scalability Objectives", "Develop a decoupled client-server architecture capable of supporting hundreds of concurrent requests with sub-150 millisecond database latencies.")

    add_heading_2(doc, "2.2 Target Demographics & User Personas")
    add_p(doc, "To ensure that AuraFIT satisfies diverse real-world user requirements, three representative user personas were modeled during the requirements analysis phase:")

    add_bullet(doc, "Persona A: The Vegetarian Fitness Beginner (Aarav, 21)", "College student who wants to lose body fat while retaining muscle. Follows a lacto-vegetarian diet. Struggles to hit protein targets without eating meat or expensive supplements. Needs verified Indian vegetarian food options and simple home workout routines.")
    add_bullet(doc, "Persona B: The Busy Corporate Professional (Priya, 32)", "Software engineer working 10-hour desk shifts. Experiences high stress and irregular meal timings. Needs quick, automated meal suggestions, rapid food logging, and home-friendly workout routines targeting posture and fat loss.")
    add_bullet(doc, "Persona C: The Advanced Gym Athlete (Vikram, 26)", "Competitive weightlifter focusing on progressive overload and hypertrophy. Needs precise tracking of workout volume (sets × reps × weight), customized macro splits (high carb, high protein), and instant macro-matched food alternatives when dining out.")

    add_heading_2(doc, "2.3 Functional Requirements Specification (FRS)")
    add_p(doc, "The functional requirements define the explicit system capabilities, workflows, and operations implemented within AuraFIT. Table 2.1 details the functional requirements matrix:")

    fr_headers = ["Req ID", "Module", "Functional Requirement Description", "Priority"]
    fr_data = [
        ["FR-01", "Auth", "User registration with email and password, utilizing Argon2 password hashing.", "High"],
        ["FR-02", "Auth", "Stateless JWT authentication issuing 15-minute access tokens and 7-day refresh tokens.", "High"],
        ["FR-03", "Profile", "Biometric onboarding capturing age, sex, height (cm/ft), weight (kg/lbs), activity, goal.", "High"],
        ["FR-04", "Profile", "Deterministic BMR computation via Mifflin-St Jeor equation and TDEE calculation.", "High"],
        ["FR-05", "Profile", "Goal-based caloric delta allocation (+300 kcal muscle gain, -500 kcal fat loss).", "High"],
        ["FR-06", "Nutrition", "Macronutrient partitioning allocating protein (2.0g/kg), fat (0.8g/kg), and carbs.", "High"],
        ["FR-07", "Nutrition", "Multi-criteria search across verified food catalog with Indian cuisine and diet tags.", "High"],
        ["FR-08", "Nutrition", "User creation and logging of custom meals, recipes, and portion adjustments.", "High"],
        ["FR-09", "Nutrition", "Algorithmic 4-bucket meal plan distribution (Breakfast, Lunch, Dinner, Snack).", "Medium"],
        ["FR-10", "AI Engine", "AI-powered ingredient substitution maintaining caloric and macronutrient parity.", "High"],
        ["FR-11", "AI Engine", "Conversational AI coach executing function calling tools for verified DB operations.", "High"],
        ["FR-12", "Fitness", "Exercise catalog categorized by target muscle group, equipment, and difficulty.", "High"],
        ["FR-13", "Fitness", "Interactive workout logger tracking sets, reps, resistance weight, and RPE notes.", "High"],
        ["FR-14", "Analytics", "Longitudinal progress dashboard charting weight, waist, and daily macro compliance.", "Medium"]
    ]
    create_table(doc, fr_headers, fr_data, [Inches(1.0), Inches(1.2), Inches(3.5), Inches(0.8)])

    add_heading_2(doc, "2.4 Non-Functional Requirements Specification (NFRS)")
    add_p(doc, "Non-functional requirements dictate the operational qualities, performance benchmarks, and security constraints governing AuraFIT. Table 2.2 outlines the non-functional standards:")

    nfr_headers = ["Req ID", "Category", "Quality Standard & Metric Constraint", "Verification Method"]
    nfr_data = [
        ["NFR-01", "Performance", "API response latency under 150ms for DB queries; sub-1.5s initial page load.", "Load testing & Lighthouse"],
        ["NFR-02", "Security", "Argon2id password hashing; JWT HMAC-SHA256 tokens; HTTPS data encryption.", "Security audit & OWASP"],
        ["NFR-03", "AI Safety", "Zero arithmetic hallucination; 100% of metabolic math executed deterministically.", "Pytest math suite"],
        ["NFR-04", "Rate Limiting", "Gemini AI endpoint rate-limited to 10 requests/minute/user to prevent abuse.", "SlowAPI integration test"],
        ["NFR-05", "Usability", "100% responsive design across mobile (375px+), tablet, and desktop (1920px).", "Cross-browser testing"],
        ["NFR-06", "Availability", "99.9% uptime architecture utilizing stateless containers and MongoDB Atlas.", "Cloud uptime monitoring"],
        ["NFR-07", "Maintainability", "Full typing with TypeScript and Pydantic v2; Controller-Service-Repo pattern.", "Static type checkers (mypy/tsc)"]
    ]
    create_table(doc, nfr_headers, nfr_data, [Inches(1.0), Inches(1.3), Inches(3.0), Inches(1.2)])

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: SYSTEM STUDY & FEASIBILITY ANALYSIS
    # =========================================================================
    add_heading_1(doc, "Chapter 3: System Study & Feasibility Analysis")

    add_heading_2(doc, "3.1 Multi-Dimensional Feasibility Study")
    add_p(doc, "A rigorous feasibility analysis was conducted to establish that AuraFIT is technically achievable, economically viable, operationally practical, and deliverable within academic deadlines.")

    add_heading_3(doc, "3.1.1 Economic Feasibility")
    add_p(doc, "AuraFIT was engineered from inception to minimize capital expenditure by leveraging open-source frameworks and modern free-tier cloud architectures. The core software stack—React, Vite, Tailwind CSS, Python, FastAPI, Motor, and MongoDB—incurs zero commercial licensing fees. Furthermore, MongoDB Atlas provides an M0 free-tier cluster offering 512 MB of cloud storage, sufficient for thousands of user profiles, food catalogs, and workout sessions during the academic and prototype lifecycle.")
    add_p(doc, "Google Gemini API provides a generous free tier for developers, supporting 15 requests per minute (RPM) and up to 1 million tokens per minute without cost. By isolating Gemini solely to contextual conversation and utilizing deterministic Python math for daily logging, token overhead is reduced by over 80% compared to brute-force LLM fitness apps.")

    add_heading_3(doc, "3.1.2 Technical Feasibility")
    add_p(doc, "The technical feasibility of AuraFIT is anchored in industry-standard, production-proven technologies:")
    add_bullet(doc, "Asynchronous Backend", "FastAPI operates on Python's `asyncio` event loop and Starlette, delivering performance comparable to NodeJS and Go while retaining Python's rich data science ecosystem.")
    add_bullet(doc, "Reactive Frontend", "React 18 with Vite provides instant Hot Module Replacement (HMR), optimized tree-shaking, and efficient client-side rendering via the virtual DOM.")
    add_bullet(doc, "Server-State Caching", "TanStack Query manages asynchronous data caching, stale-time invalidation, and optimistic UI updates, drastically reducing network payloads.")
    add_bullet(doc, "NoSQL Flexibility", "MongoDB's BSON document structure accommodates dynamic nested structures (e.g., custom meals with varied ingredients, exercise sets with varied weights) without complex SQL joins.")

    add_heading_3(doc, "3.1.3 Operational Feasibility")
    add_p(doc, "Operational feasibility evaluates the ease with which users of varying technical and fitness literacy can navigate the application. AuraFIT abstracts all metabolic complexities into clean visual metaphors: radial progress rings indicate remaining calories and macro grams, color-coded badges categorize exercises by difficulty, and an interactive chat drawer provides immediate answers. Users require zero training to begin logging meals and workouts.")

    add_heading_3(doc, "3.1.4 Motivational Feasibility")
    add_p(doc, "Adherence is the single greatest determinant of fitness success. AuraFIT incorporates motivational design patterns: daily logging streaks, milestone achievement badges, real-time macro balance confirmations, and empathetic coaching messages that celebrate consistency rather than demanding perfection.")

    add_heading_3(doc, "3.1.5 Schedule Feasibility")
    add_p(doc, "The project scope was carefully aligned with a 15-week academic development lifecycle. Divided into 7 distinct two-week Agile sprints, milestones were achieved systematically, from initial schema definitions to final UAT testing.")

    add_heading_2(doc, "3.2 Cost-Benefit Analysis Matrix")
    add_p(doc, "Table 3.1 provides a detailed cost-benefit analysis evaluating development, infrastructure, and ongoing operational parameters against quantitative health and software benefits:")

    cb_headers = ["Category", "Financial / Resource Cost", "Qualitative & Technical Benefit Realized"]
    cb_data = [
        ["Software Tooling", "Rs. 0 (Open source: React, FastAPI, Tailwind)", "Zero proprietary software licensing expenses; open architecture."],
        ["Database Hosting", "Rs. 0 (MongoDB Atlas Cloud M0 Sandbox)", "Automated backups, global cloud availability, zero maintenance overhead."],
        ["Client Hosting", "Rs. 0 (Vercel / Netlify Static Cloud Edge)", "Global Content Delivery Network (CDN), SSL encryption, sub-second latency."],
        ["AI LLM Service", "Rs. 0 (Google Gemini Free Tier / Developer Key)", "Access to state-of-the-art multimodal reasoning with zero fixed overhead."],
        ["Nutritional Accuracy", "Negligible CPU overhead (<5ms calculation time)", "100% deterministic accuracy; elimination of health and starvation risks."],
        ["Development Effort", "Approx. 940 person-hours across academic team", "Creation of a production-ready, portfolio-grade enterprise platform."]
    ]
    create_table(doc, cb_headers, cb_data, [Inches(1.5), Inches(2.2), Inches(2.8)])

    add_heading_2(doc, "3.3 Fact-Finding & Competitive Benchmarking")
    add_p(doc, "During the comprehensive system study, existing industry leaders were evaluated to identify functional gaps and technical opportunities. Table 3.2 illustrates the competitive benchmarking analysis:")

    bench_headers = ["Evaluation Metric", "MyFitnessPal", "HealthifyMe", "ChatGPT Plus", "AuraFIT Platform"]
    bench_data = [
        ["Deterministic Metabolic Math", "Partial", "Yes", "No (Hallucinates)", "Yes (100% Guaranteed)"],
        ["Indian Food Database Accuracy", "Poor (Crowdsourced)", "Good", "Generic / Guessed", "Excellent (Curated)"],
        ["Smart Macro-Matched Swaps", "No", "No", "Unverified Math", "Yes (Function Calling)"],
        ["Integrated Workout Logger", "Basic", "Basic", "Text only", "Comprehensive"],
        ["Free Tier Usability", "Heavily Paywalled", "Restricted", "Subscription ($20/mo)", "Complete Core Access"],
        ["Data Privacy / No-Ad Model", "Ad-supported", "Heavy Upselling", "Subject to Training", "Private & Ad-Free"],
        ["Real-Time AI Coach Support", "No", "Paid Humans Only", "Unconstrained Chat", "Grounded AI Tools"]
    ]
    create_table(doc, bench_headers, bench_data, [Inches(1.5), Inches(1.2), Inches(1.2), Inches(1.3), Inches(1.3)])

    add_heading_2(doc, "3.4 System Overview & Decoupled 3-Tier Architecture")
    add_p(doc, "AuraFIT is structured around a decoupled, service-oriented 3-tier architecture. Figure 3.1 illustrates the structural relationship between system tiers:")

    add_code_block(doc,
"""
========================================================================================
[PRESENTATION LAYER] - React 18 Single Page Application (SPA)
 - Components: Layout (AppShell), Features (Auth, Nutrition, Workouts, AI Coach, Analytics)
 - State Management: TanStack Query (Server State), Zustand (UI State), Axios Interceptors
 - Styling & Assets: Tailwind CSS Custom Tokens, Recharts Visualizations, Lucide Icons
                                       |
                     HTTPS / REST API  |  JSON Web Tokens (Bearer)
                                       v
========================================================================================
[APPLICATION & DOMAIN LAYER] - Python 3.10+ / FastAPI Server
 - Middleware: CORS Policy Enforcer, SlowAPI Rate Limiter, Exception Interceptor
 - Routers: /auth, /profile, /nutrition, /foods, /exercises, /workouts, /ai, /analytics
 - Security Service: Argon2id Password Hasher, PyJWT Token Signer & Verifier
 - Deterministic Engine: Mifflin-St Jeor Algorithm, TDEE Multipliers, 4-Bucket Meal Balancer
 - AI Orchestrator: Google Gemini Client, Function Calling Tool Registry, Pydantic Parser
                                       |
                    Asynchronous I/O   |   Motor Async Driver (BSON)
                                       v
========================================================================================
[PERSISTENCE & EXTERNAL SERVICE LAYER]
 - MongoDB Atlas Cloud Cluster: Collections for users, profiles, foods, exercises, logs
 - Google Gemini API: Remote LLM Engine for Function Execution and Natural Language Synthesis
========================================================================================
"""
    )

    add_heading_2(doc, "3.5 User Roles, Privileges & RBAC Matrix")
    add_p(doc, "To enforce strict data segregation and operational security, AuraFIT implements Role-Based Access Control (RBAC). Table 3.3 defines the access permissions matrix:")

    rbac_headers = ["System Module / Resource", "Public Guest", "Authenticated User", "Certified Coach", "Administrator"]
    rbac_data = [
        ["Landing Page & Onboarding", "Read Only", "Full Access", "Full Access", "Full Access"],
        ["User Registration & Login", "Create / Auth", "Read Profile", "Read Profile", "Full Access"],
        ["Personal Nutrition & Macros", "No Access", "Full CRUD", "Read / Advise", "Full CRUD"],
        ["Master Food Catalog", "No Access", "Read / Search", "Read / Search", "Full CRUD / Audit"],
        ["Workout & Exercise Logging", "No Access", "Full CRUD", "Read / Prescribe", "Full CRUD"],
        ["Conversational AI Coach", "No Access", "Full Access", "Full Access", "Full Access / Logs"],
        ["User Management & System DB", "No Access", "No Access", "No Access", "Full System Admin"]
    ]
    create_table(doc, rbac_headers, rbac_data, [Inches(1.8), Inches(1.0), Inches(1.3), Inches(1.2), Inches(1.2)])

    doc.add_page_break()
