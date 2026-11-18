# -*- coding: utf-8 -*-
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_generator.helpers import (
    add_heading_1, add_heading_2, add_heading_3, add_p, add_bullet, add_numbered, create_table, add_code_block
)

def build_chapters_4_to_6(doc):
    # =========================================================================
    # CHAPTER 4: MATHEMATICAL MODELS & ALGORITHMIC FOUNDATIONS
    # =========================================================================
    add_heading_1(doc, "Chapter 4: Mathematical Models & Algorithmic Foundations")

    add_heading_2(doc, "4.1 Deterministic Metabolic Rate Computations (BMR & TDEE)")
    add_p(doc, "The cornerstone of the AuraFIT nutritional intelligence engine is absolute mathematical determinism. The platform rejects arbitrary heuristic estimations in favor of the clinically validated Mifflin-St Jeor formula, widely recognized in clinical dietetics as the most accurate predictor of human Basal Metabolic Rate (BMR) across diverse body compositions.")

    add_p(doc, "Basal Metabolic Rate represents the minimum caloric expenditure required to sustain vital physiological functions—such as cellular respiration, cardiovascular circulation, neural activity, and thermoregulation—at complete physical and digestive rest. The Mifflin-St Jeor equation computes BMR utilizing biological sex, current weight in kilograms, height in centimeters, and chronological age in years:")

    add_code_block(doc,
"""
Male BMR Formulation:
  BMR (kcal/day) = (10 * Weight_kg) + (6.25 * Height_cm) - (5.0 * Age_years) + 5

Female BMR Formulation:
  BMR (kcal/day) = (10 * Weight_kg) + (6.25 * Height_cm) - (5.0 * Age_years) - 161
"""
    )

    add_p(doc, "To translate BMR into Total Daily Energy Expenditure (TDEE)—the total energy burned over a 24-hour cycle including physical movement and the Thermic Effect of Food (TEF)—AuraFIT multiplies the calculated BMR by standardized Physical Activity Level (PAL) coefficients. Table 4.1 delineates the physical activity categories and multiplier constants implemented within the backend engine:")

    pal_headers = ["Activity Classification", "PAL Multiplier", "Clinical Description & Lifestyle Criteria", "Typical Energy Expenditure"]
    pal_data = [
        ["Sedentary", "1.200", "Desk-bound employment; minimal intentional physical exercise or walking.", "Base metabolic maintenance + minimal NEAT."],
        ["Lightly Active", "1.375", "Light daily movement; structured exercise or sports 1 to 3 days per week.", "+200 to 400 kcal above basal rate."],
        ["Moderately Active", "1.550", "Moderate physical exertion; resistance training or cardio 3 to 5 days per week.", "+400 to 650 kcal above basal rate."],
        ["Very Active", "1.725", "Heavy physical training; strenuous athletic sessions 6 to 7 days per week.", "+650 to 900 kcal above basal rate."],
        ["Extremely Active", "1.900", "Professional athletics, intense physical labor, or double training sessions.", "+900 to 1200+ kcal above basal rate."]
    ]
    create_table(doc, pal_headers, pal_data, [Inches(1.5), Inches(1.1), Inches(2.6), Inches(1.3)])

    add_heading_2(doc, "4.2 Caloric Delta & Macronutrient Partitioning Model")
    add_p(doc, "Once TDEE is established, the user's primary fitness objective dictates a scientifically safe caloric adjustment. AuraFIT strictly bounds caloric deficits to preserve lean muscle tissue and hormonal health:")
    add_bullet(doc, "Fat Loss Deficit", "TDEE - 500 kcal/day (targeting ~0.45 kg of adipose tissue loss per week). A strict safety floor of 1,200 kcal is programmatically enforced to prevent nutritional starvation.")
    add_bullet(doc, "Maintenance Target", "Identical to TDEE (caloric equilibrium).")
    add_bullet(doc, "Hypertrophy / Muscle Gain", "TDEE + 300 kcal/day (lean caloric surplus supporting myofibrillar protein synthesis with minimal fat accumulation).")

    add_p(doc, "Following caloric target determination, the macronutrient partitioning algorithm computes exact daily targets for protein, fat, and carbohydrates using the standard Atwater conversion factors: Protein = 4 kcal/g, Carbohydrate = 4 kcal/g, Dietary Fat = 9 kcal/g. Table 4.2 presents the mathematical partitioning framework:")

    macro_headers = ["Macronutrient", "Clinical Partitioning Formula", "Metabolic Rationale in AuraFIT", "Caloric Contribution"]
    macro_data = [
        ["Protein", "2.0 g per kg of bodyweight", "Maximizes muscle protein synthesis (MPS) and minimizes sarcopenia.", "Protein_g * 4 kcal"],
        ["Dietary Fat", "0.8 g per kg of bodyweight", "Ensures essential fatty acid uptake and optimal endocrine/hormone synthesis.", "Fat_g * 9 kcal"],
        ["Carbohydrates", "(Target_Calories - Protein_kcal - Fat_kcal) / 4", "Provides primary glycogen substrate for high-intensity training performance.", "Remaining Calories / 4"]
    ]
    create_table(doc, macro_headers, macro_data, [Inches(1.4), Inches(1.8), Inches(2.1), Inches(1.2)])

    add_heading_2(doc, "4.3 Algorithmic 4-Bucket Meal Plan Generation Engine")
    add_p(doc, "To translate daily macronutrient targets into actionable meals, AuraFIT employs a deterministic 4-bucket greedy optimization algorithm. The user's total daily caloric allowance is partitioned into four distinct meal allocations: Breakfast (25%), Lunch (35%), Dinner (30%), and Mid-Day Snack (10%). Table 4.3 outlines the 4-bucket distribution:")

    bucket_headers = ["Meal Window", "Caloric Split (%)", "Target Macro Focus", "Sample Curated Indian Composition"]
    bucket_data = [
        ["Breakfast", "25%", "High Protein, Moderate Complex Carbs", "Sprouted Moong Cheela / Besan Chilla with Paneer Filling"],
        ["Lunch", "35%", "Balanced High Energy, Fiber & Protein", "Brown Rice / Whole Wheat Roti, Dal Tadka, Grilled Soya / Chicken, Curd"],
        ["Dinner", "30%", "High Protein, Moderate Healthy Fats", "Paneer Bhurji / Tofu Stir-Fry, Mixed Vegetable Sabzi, Multigrain Roti"],
        ["Snack", "10%", "Fast Digesting Protein / Satiety", "Roasted Chana, Greek Yogurt, Whey Protein Isolate Shake, or Almonds"]
    ]
    create_table(doc, bucket_headers, bucket_data, [Inches(1.2), Inches(1.2), Inches(2.1), Inches(2.0)])

    add_p(doc, "The backend greedy algorithm executes constraint satisfaction: it queries MongoDB for foods matching the user's dietary preferences (e.g., vegetarian, vegan, non-vegetarian) and allergen restrictions. It iteratively populates each meal bucket until the aggregated calories and macronutrients fall within a tight ±5% tolerance band of the target values.")

    add_heading_2(doc, "4.4 Food Ranking Heuristic & Nutrient Density Index")
    add_p(doc, "To identify optimal food items for muscle building and fat loss, AuraFIT calculates a proprietary Nutrient Density Ratio:")
    add_code_block(doc,
"""
Nutrient Density Score (NDS) = (Protein_grams_per_100g * 4) / Total_Calories_per_100g
"""
    )
    add_p(doc, "Foods exhibiting higher NDS values (e.g., Soya Chunks, Chicken Breast, Egg Whites, Paneer, Sprouted Moong) are prioritized by the recommendation engine during meal formulation, maximizing satiety per calorie.")

    add_heading_2(doc, "4.5 Resistance Training Volume & Progressive Overload Tracking")
    add_p(doc, "For resistance training, AuraFIT models workout volume quantitatively to support the physiological principle of progressive overload. Total training volume is formulated as:")
    add_code_block(doc,
"""
Total Training Volume (kg) = SUM (Sets * Repetitions * Resistance_Weight_kg)
"""
    )
    add_p(doc, "The system automatically aggregates total volume per muscle group across training sessions, enabling athletes to visualize whether volume is progressively increasing over consecutive weeks.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: AI ENGINE & GOOGLE GEMINI TOOL ORCHESTRATION
    # =========================================================================
    add_heading_1(doc, "Chapter 5: AI Engine & Google Gemini Tool Orchestration")

    add_heading_2(doc, "5.1 Architectural Segregation: Determinism vs. LLM Generation")
    add_p(doc, "A critical innovation in AuraFIT is the rigorous architectural firewall established between deterministic backend calculations and generative artificial intelligence. Large Language Models operate via next-token prediction across multi-dimensional vector spaces. While LLMs excel at linguistic synthesis, style adaptation, and conversational empathy, their probabilistic nature makes them fundamentally unreliable for numerical arithmetic.")
    add_p(doc, "If an LLM is directly asked: 'What should my daily macros be to lose weight?', it may invent arbitrary numbers without consulting clinical formulas. AuraFIT eliminates this failure mode entirely: the backend computes exact targets deterministically and supplies them to Google Gemini as immutable, read-only system context.")

    add_heading_2(doc, "5.2 Server-Side AI Orchestration Pipeline")
    add_p(doc, "Figure 5.1 illustrates the server-side AI orchestration pipeline deployed in the FastAPI backend:")

    add_code_block(doc,
"""
+---------------------------------------------------------------------------------------+
| 1. Client Chat Message -> Transmitted to FastAPI /api/v1/ai/chat                      |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| 2. Context Injection Pipeline:                                                        |
|    - Query MongoDB for user profile (Age, Weight, Goal, Allergies, Diet)              |
|    - Query MongoDB for today's consumed calories and remaining macro budget           |
|    - Prepend system prompt with strict negative constraints                           |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| 3. Remote Google Gemini Invocation (with Bound Tool Declarations):                    |
|    - System Prompt: 'You are AuraFIT AI. You CANNOT invent nutrition values...'       |
|    - Tools Provided: search_foods, get_food_details, find_alternative_food, etc.      |
+---------------------------------------------------------------------------------------+
                                           |
                 Does Gemini request a Tool Call?
                               /                    \\
                             YES                     NO (Direct Text Explanation)
                             /                         \\
                            v                           v
+------------------------------------+    +------------------------------------+
| 4. Backend Tool Execution:         |    | 5. Return Formatted JSON Response  |
|    - Execute Python DB query       |    |    to Client React Component       |
|    - Return verified data to Gemini|    +------------------------------------+
|    - Gemini formats final response |
+------------------------------------+
"""
    )

    add_heading_2(doc, "5.3 Gemini Tool Declarations & JSON Schema Definitions")
    add_p(doc, "AuraFIT exposes five high-level tools to Google Gemini via OpenAPI-compliant JSON schemas. Table 5.1 details the functional contracts of these tools:")

    tool_headers = ["Tool Name", "Purpose & Responsibility", "Input Parameters", "Output Return Schema"]
    tool_data = [
        ["search_foods", "Searches verified database for food items matching queries and dietary tags.", "search: str, category: str, diet: str", "List of Food BSON objects with IDs, calories, macros"],
        ["get_food_details", "Retrieves complete nutritional and allergen profile for a given food ID.", "food_id: str (Required)", "Exact calories, protein, carbs, fat, fiber, allergens"],
        ["find_alternative_food", "Discovers macro-equivalent food alternatives matching dietary constraints.", "food_id: str (Required)", "Array of matched replacement food items with portions"],
        ["search_exercises", "Queries exercise library by anatomical target muscle and equipment.", "search: str, muscle: str, equipment: str", "List of exercise definitions with instruction steps"],
        ["get_exercise_details", "Extracts biomechanical steps and video links for an exercise ID.", "exercise_id: str (Required)", "Full exercise instructions and safety tips"]
    ]
    create_table(doc, tool_headers, tool_data, [Inches(1.4), Inches(2.0), Inches(1.6), Inches(1.5)])

    add_heading_2(doc, "5.4 Anti-Hallucination Guardrails & Mathematical Verification")
    add_p(doc, "To prevent hallucinated data from contaminating the database, all tool execution results returned by Gemini pass through secondary backend validation. If Gemini suggests replacing 100g of paneer with tofu, the backend verifies that the calculated calories of the suggested tofu portion match the paneer within an acceptable variance (±10%). If variance is exceeded, the server automatically recalibrates the portion size before presenting it to the user.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: DATA FLOW DIAGRAMS & SYSTEM WORKFLOWS
    # =========================================================================
    add_heading_1(doc, "Chapter 6: Data Flow Diagrams & System Workflows")

    add_heading_2(doc, "6.1 Level 0: Context-Level DFD")
    add_p(doc, "The Context-Level Data Flow Diagram (DFD Level 0) defines the operational boundary of AuraFIT. It models the core application as a single process interacting with three external entities: the User, MongoDB Atlas Cloud Database, and the Google Gemini AI Service. Figure 6.1 illustrates the Level 0 DFD:")

    add_code_block(doc,
"""
                               +-----------------------------------+
                               |               USER                |
                               +-----------------------------------+
                                     |                       ^
                 Registration Data,  |                       | Calculated Macros,
                 Biometrics, Meals,  |                       | Verified Meal Plans,
                 Workouts, Chat      |                       | AI Coaching Text
                                     v                       |
                        +=================================================+
                        |                     [ 0.0 ]                     |
                        |             AuraFIT Application Engine          |
                        +=================================================+
                                  /       ^              \\        ^
                Async BSON Write /        | BSON Docs     \\ Prompt | Structured
                Updates & Queries        |                \\ Tools | JSON Tool Resp
                                v        |                 v      |
                 +-------------------------------+   +-----------------------------+
                 |       MONGODB ATLAS DB        |   |      GOOGLE GEMINI API      |
                 +-------------------------------+   +-----------------------------+
"""
    )

    add_heading_2(doc, "6.2 Level 1: Subsystem Decomposition DFD")
    add_p(doc, "Level 1 decomposes the AuraFIT system into its 6 primary operational processes. Figure 6.2 illustrates the subsystem decomposition:")

    add_code_block(doc,
"""
                           +------------------------+
                           |          USER          |
                           +------------------------+
                             /     |         |     \\
            Credentials     /      | Bio     | Food \\ Workout
                           v       v Data    v Logs  v Sessions
            +----------------+   +-------+  +----+   +--------+
            | 1.0 Auth & JWT |   |2.0 BMR|  |3.0 |   | 4.0    |
            |     Manager    |   | Engine|  |Meal|   | Workout|
            +----------------+   +-------+  | Log|   | Planner|
                   |                 |      +----+   +--------+
                   v                 v        |          |
             [Users Table]    [Profiles Tab]  |          |
                                              v          v
                                         [Foods Coll] [Exercises]
                                              |
               Context & Tool Invocations     v
                   +----------------------------------+
                   | 5.0 AI Coach & Tool Orchestrator | <---> [Gemini API]
                   +----------------------------------+
                                              |
                                              v
                   +----------------------------------+
                   | 6.0 Analytics & Progress Engine  | ----> [Measurements]
                   +----------------------------------+
"""
    )

    add_heading_2(doc, "6.3 Level 2: Detailed Process Flows (Nutrition & AI Swapping)")
    add_p(doc, "Figure 6.3 details the process flow when an authenticated user requests an AI-powered meal ingredient substitution:")

    add_code_block(doc,
"""
[User] -> Selects Food to Swap (e.g., Paneer 100g)
   |
   v
[Process 3.1: Validation & Macro Extraction]
   - Extracts current calories (265 kcal), protein (18.3g), fat (20.8g)
   |
   v
[Process 3.2: Context Assembly & Tool Invocation]
   - Packages user dietary preference (Vegetarian) & allergen exclusions
   - Invokes Gemini API with find_alternative_food(food_id)
   |
   v
[Process 3.3: Database Tool Query Execution]
   - Server searches Foods Collection for items with similar protein/calorie ratio
   - Discovers Tofu (Firm): 140 kcal, 16g protein per 100g
   |
   v
[Process 3.4: Mathematical Parity Recalibration]
   - Calculates exact portion required for macro parity: 115g Tofu
   |
   v
[Process 3.5: Client UI Notification & MongoDB Log Mutation]
   - Returns verified substitution to user with side-by-side comparison
"""
    )

    add_heading_2(doc, "6.4 Sequence Diagrams for Critical User Transactions")
    add_p(doc, "Figure 6.4 depicts the UML sequence diagram for User Registration and JWT Exchange:")

    add_code_block(doc,
"""
User Client SPA             FastAPI Gateway          MongoDB Atlas
      |                            |                       |
      |-- POST /auth/register ---->|                       |
      |   {email, password}        |                       |
      |                            |-- Query User By Email>|
      |                            |<-- None Found --------|
      |                            |                       |
      |                            |-- Hash Password       |
      |                            |   via Argon2id        |
      |                            |                       |
      |                            |-- Insert User Doc --->|
      |                            |<-- Insert Success ----|
      |                            |                       |
      |                            |-- Generate JWT Access |
      |                            |   & Refresh Tokens    |
      |                            |                       |
      |<-- 201 Created ------------|                       |
      |   {access_token, user_id}  |                       |
"""
    )

    doc.add_page_break()
