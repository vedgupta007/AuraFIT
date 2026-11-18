import asyncio
import os
import sys
from datetime import datetime, timezone
from pymongo import ASCENDING, UpdateOne

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_database
from bson import ObjectId

# Expanded Foods Seed
FOODS_SEED = [
    {"name": "Cooked Basmati Rice", "category": "Grains", "serving_size": 100, "serving_unit": "g", "calories": 130, "protein": 2.7, "carbohydrates": 28, "fat": 0.3, "fiber": 0.4, "diet_types": ["vegetarian", "vegan"], "allergens": [], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Whole Wheat Roti (Chapati)", "category": "Grains", "serving_size": 1, "serving_unit": "piece", "calories": 120, "protein": 4.0, "carbohydrates": 24.0, "fat": 0.5, "fiber": 4.0, "diet_types": ["vegetarian", "vegan"], "allergens": ["Gluten"], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Dal Tadka (Cooked)", "category": "Legumes", "serving_size": 100, "serving_unit": "g", "calories": 116, "protein": 6.5, "carbohydrates": 16.0, "fat": 3.0, "fiber": 5.0, "diet_types": ["vegetarian", "vegan"], "allergens": [], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Paneer (Raw)", "category": "Dairy", "serving_size": 100, "serving_unit": "g", "calories": 296, "protein": 18.0, "carbohydrates": 3.5, "fat": 23.0, "fiber": 0.0, "diet_types": ["vegetarian"], "allergens": ["Dairy"], "is_vegetarian": True, "is_vegan": False, "is_eggetarian": True},
    {"name": "Chicken Breast (Cooked)", "category": "Meat", "serving_size": 100, "serving_unit": "g", "calories": 165, "protein": 31.0, "carbohydrates": 0.0, "fat": 3.6, "fiber": 0.0, "diet_types": ["non_vegetarian"], "allergens": [], "is_vegetarian": False, "is_vegan": False, "is_eggetarian": False},
    {"name": "Boiled Egg", "category": "Eggs", "serving_size": 1, "serving_unit": "large", "calories": 78, "protein": 6.3, "carbohydrates": 0.6, "fat": 5.3, "fiber": 0.0, "diet_types": ["eggetarian", "non_vegetarian"], "allergens": ["Egg"], "is_vegetarian": False, "is_vegan": False, "is_eggetarian": True},
    {"name": "Apple", "category": "Fruits", "serving_size": 1, "serving_unit": "medium", "calories": 95, "protein": 0.5, "carbohydrates": 25.0, "fat": 0.3, "fiber": 4.4, "diet_types": ["vegetarian", "vegan"], "allergens": [], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Almonds", "category": "Nuts and Seeds", "serving_size": 28, "serving_unit": "g", "calories": 164, "protein": 6.0, "carbohydrates": 6.0, "fat": 14.0, "fiber": 3.5, "diet_types": ["vegetarian", "vegan"], "allergens": ["Tree Nuts"], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Soy Chunks (Cooked)", "category": "Legumes", "serving_size": 100, "serving_unit": "g", "calories": 345, "protein": 52.0, "carbohydrates": 33.0, "fat": 0.5, "fiber": 13.0, "diet_types": ["vegetarian", "vegan"], "allergens": ["Soy"], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Masala Oats", "category": "Grains", "serving_size": 40, "serving_unit": "g", "calories": 150, "protein": 5.0, "carbohydrates": 25.0, "fat": 3.0, "fiber": 4.0, "diet_types": ["vegetarian", "vegan"], "allergens": ["Gluten"], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Greek Yogurt (Plain, Low Fat)", "category": "Dairy", "serving_size": 150, "serving_unit": "g", "calories": 95, "protein": 15.0, "carbohydrates": 6.0, "fat": 2.0, "fiber": 0.0, "diet_types": ["vegetarian"], "allergens": ["Dairy"], "is_vegetarian": True, "is_vegan": False, "is_eggetarian": True},
    {"name": "Salmon (Grilled)", "category": "Fish", "serving_size": 100, "serving_unit": "g", "calories": 206, "protein": 22.0, "carbohydrates": 0.0, "fat": 12.0, "fiber": 0.0, "diet_types": ["non_vegetarian"], "allergens": ["Fish"], "is_vegetarian": False, "is_vegan": False, "is_eggetarian": False},
    {"name": "Chickpeas (Boiled)", "category": "Legumes", "serving_size": 100, "serving_unit": "g", "calories": 164, "protein": 8.9, "carbohydrates": 27.4, "fat": 2.6, "fiber": 7.6, "diet_types": ["vegetarian", "vegan"], "allergens": [], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Spinach (Raw)", "category": "Vegetables", "serving_size": 100, "serving_unit": "g", "calories": 23, "protein": 2.9, "carbohydrates": 3.6, "fat": 0.4, "fiber": 2.2, "diet_types": ["vegetarian", "vegan"], "allergens": [], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Avocado", "category": "Healthy Fats", "serving_size": 100, "serving_unit": "g", "calories": 160, "protein": 2.0, "carbohydrates": 8.5, "fat": 14.7, "fiber": 6.7, "diet_types": ["vegetarian", "vegan"], "allergens": [], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Peanut Butter (Unsweetened)", "category": "Nuts and Seeds", "serving_size": 32, "serving_unit": "g", "calories": 188, "protein": 8.0, "carbohydrates": 6.0, "fat": 16.0, "fiber": 2.0, "diet_types": ["vegetarian", "vegan"], "allergens": ["Peanuts"], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Moong Dal Chilla", "category": "Legumes", "serving_size": 1, "serving_unit": "piece", "calories": 125, "protein": 7.0, "carbohydrates": 15.0, "fat": 3.5, "fiber": 2.5, "diet_types": ["vegetarian", "vegan"], "allergens": [], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Brown Rice (Cooked)", "category": "Grains", "serving_size": 100, "serving_unit": "g", "calories": 112, "protein": 2.6, "carbohydrates": 23.5, "fat": 0.9, "fiber": 1.8, "diet_types": ["vegetarian", "vegan"], "allergens": [], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Chicken Curry (Home-style)", "category": "Meat", "serving_size": 200, "serving_unit": "g", "calories": 250, "protein": 20.0, "carbohydrates": 8.0, "fat": 15.0, "fiber": 2.0, "diet_types": ["non_vegetarian"], "allergens": [], "is_vegetarian": False, "is_vegan": False, "is_eggetarian": False},
    {"name": "Mutton Curry", "category": "Meat", "serving_size": 200, "serving_unit": "g", "calories": 320, "protein": 25.0, "carbohydrates": 5.0, "fat": 22.0, "fiber": 1.0, "diet_types": ["non_vegetarian"], "allergens": [], "is_vegetarian": False, "is_vegan": False, "is_eggetarian": False},
    {"name": "Fish Tikka", "category": "Fish", "serving_size": 150, "serving_unit": "g", "calories": 180, "protein": 25.0, "carbohydrates": 4.0, "fat": 6.0, "fiber": 1.0, "diet_types": ["non_vegetarian"], "allergens": ["Fish", "Dairy"], "is_vegetarian": False, "is_vegan": False, "is_eggetarian": False},
    {"name": "Tofu (Firm)", "category": "Legumes", "serving_size": 100, "serving_unit": "g", "calories": 144, "protein": 15.8, "carbohydrates": 2.8, "fat": 8.7, "fiber": 2.3, "diet_types": ["vegetarian", "vegan"], "allergens": ["Soy"], "is_vegetarian": True, "is_vegan": True, "is_eggetarian": True},
    {"name": "Protein Powder (Whey Isolate)", "category": "Supplements", "serving_size": 30, "serving_unit": "g", "calories": 110, "protein": 25.0, "carbohydrates": 1.0, "fat": 0.5, "fiber": 0.0, "diet_types": ["vegetarian"], "allergens": ["Dairy"], "is_vegetarian": True, "is_vegan": False, "is_eggetarian": True}
]

# Expanded Exercises Seed
EXERCISES_SEED = [
    {
        "name": "Push-ups", "normalized_name": "push-ups", "description": "A classic bodyweight exercise for the chest, shoulders, and triceps.",
        "category": "Strength", "primary_muscle": "Chest", "secondary_muscles": ["Triceps", "Shoulders", "Core"],
        "equipment": "Bodyweight", "difficulty": "Beginner",
        "instructions": ["Start in a plank position.", "Lower your body until your chest nearly touches the floor.", "Push yourself back up."],
        "sets_recommendation": "3", "reps_recommendation": "10-15", "duration_seconds": None,
        "safety_notes": "Keep your core engaged and your back straight."
    },
    {
        "name": "Squats", "normalized_name": "squats", "description": "A fundamental lower body exercise.",
        "category": "Strength", "primary_muscle": "Quadriceps", "secondary_muscles": ["Glutes", "Hamstrings", "Core"],
        "equipment": "Bodyweight", "difficulty": "Beginner",
        "instructions": ["Stand with feet shoulder-width apart.", "Lower your hips as if sitting in a chair.", "Push back up to the starting position."],
        "sets_recommendation": "3", "reps_recommendation": "15-20", "duration_seconds": None,
        "safety_notes": "Keep your chest up and don't let your knees cave inward."
    },
    {
        "name": "Dumbbell Bicep Curls", "normalized_name": "dumbbell_bicep_curls", "description": "Isolation exercise for the biceps.",
        "category": "Strength", "primary_muscle": "Biceps", "secondary_muscles": ["Forearms"],
        "equipment": "Dumbbells", "difficulty": "Beginner",
        "instructions": ["Hold a dumbbell in each hand.", "Curl the weights toward your shoulders.", "Lower them slowly."],
        "sets_recommendation": "3", "reps_recommendation": "10-12", "duration_seconds": None,
        "safety_notes": "Avoid using momentum to swing the weights."
    },
    {
        "name": "Plank", "normalized_name": "plank", "description": "An isometric core exercise.",
        "category": "Core", "primary_muscle": "Core", "secondary_muscles": ["Shoulders"],
        "equipment": "Bodyweight", "difficulty": "Beginner",
        "instructions": ["Rest on your forearms and toes.", "Keep your body in a straight line.", "Hold the position."],
        "sets_recommendation": "3", "reps_recommendation": "N/A", "duration_seconds": 60,
        "safety_notes": "Don't let your lower back sag."
    },
    {
        "name": "Pull-ups", "normalized_name": "pull-ups", "description": "A challenging upper body compound exercise.",
        "category": "Strength", "primary_muscle": "Back", "secondary_muscles": ["Biceps", "Forearms"],
        "equipment": "Pull-up Bar", "difficulty": "Intermediate",
        "instructions": ["Grab the bar with an overhand grip.", "Pull yourself up until your chin is over the bar.", "Lower yourself slowly."],
        "sets_recommendation": "3", "reps_recommendation": "5-10", "duration_seconds": None,
        "safety_notes": "Avoid swinging or using excessive momentum."
    },
    {
        "name": "Barbell Bench Press", "normalized_name": "barbell_bench_press", "description": "A compound movement for chest size and strength.",
        "category": "Strength", "primary_muscle": "Chest", "secondary_muscles": ["Triceps", "Shoulders"],
        "equipment": "Barbell", "difficulty": "Intermediate",
        "instructions": ["Lie flat on the bench.", "Grip the bar slightly wider than shoulder-width.", "Lower the bar to your chest and press it back up."],
        "sets_recommendation": "3", "reps_recommendation": "8-12", "duration_seconds": None,
        "safety_notes": "Use a spotter if lifting heavy weights."
    },
    {
        "name": "Jumping Jacks", "normalized_name": "jumping_jacks", "description": "A full-body cardio and warm-up exercise.",
        "category": "Cardio", "primary_muscle": "Full Body", "secondary_muscles": ["Calves", "Shoulders"],
        "equipment": "Bodyweight", "difficulty": "Beginner",
        "instructions": ["Start standing with legs together.", "Jump while spreading legs and raising arms.", "Return to the starting position."],
        "sets_recommendation": "N/A", "reps_recommendation": "N/A", "duration_seconds": 60,
        "safety_notes": "Land softly to protect your joints."
    },
    {
        "name": "Walking Lunges", "normalized_name": "walking_lunges", "description": "Unilateral lower body movement.",
        "category": "Strength", "primary_muscle": "Quadriceps", "secondary_muscles": ["Glutes", "Hamstrings"],
        "equipment": "Bodyweight", "difficulty": "Beginner",
        "instructions": ["Step forward with one leg and lower your hips.", "Push off the back foot to bring it forward into the next lunge.", "Alternate legs."],
        "sets_recommendation": "3", "reps_recommendation": "10-12 per leg", "duration_seconds": None,
        "safety_notes": "Keep your front knee aligned with your toes."
    },
    {
        "name": "Yoga: Cat-Cow", "normalized_name": "yoga_cat_cow", "description": "Mobility exercise for the spine.",
        "category": "Mobility", "primary_muscle": "Lower Back", "secondary_muscles": ["Core", "Neck"],
        "equipment": "None", "difficulty": "Beginner",
        "instructions": ["Start on all fours.", "Arch your back up (Cat), then drop your belly and lift your head (Cow).", "Move slowly between the two positions."],
        "sets_recommendation": "2", "reps_recommendation": "10", "duration_seconds": None,
        "safety_notes": "Move within a comfortable range of motion."
    }
]

def normalize_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace(",", "")

async def seed():
    await connect_to_mongo()
    db = get_database()
    
    now = datetime.now(timezone.utc)
    
    # 1. Ensure indexes
    print("Creating indexes...")
    await db.foods.create_index([("normalized_name", ASCENDING)], unique=True)
    await db.foods.create_index([("category", ASCENDING)])
    await db.foods.create_index([("is_active", ASCENDING)])
    
    await db.exercises.create_index([("normalized_name", ASCENDING)], unique=True)
    await db.exercises.create_index([("category", ASCENDING)])
    await db.exercises.create_index([("primary_muscle", ASCENDING)])
    await db.exercises.create_index([("equipment", ASCENDING)])
    await db.exercises.create_index([("is_active", ASCENDING)])

    # 2. Seed Foods
    foods_operations = []
    for food in FOODS_SEED:
        food["normalized_name"] = normalize_name(food["name"] + "_" + str(food["serving_size"]) + food["serving_unit"])
        food["updated_at"] = now
        food["is_active"] = True
        
        operations = {
            "$set": food,
            "$setOnInsert": {"created_at": now}
        }
        foods_operations.append(UpdateOne({"normalized_name": food["normalized_name"]}, operations, upsert=True))
            
    if foods_operations:
        result = await db.foods.bulk_write(foods_operations)
        print(f"Foods -> Upserted: {result.upserted_count}, Modified: {result.modified_count}")
    
    # 3. Seed Exercises
    exercises_operations = []
    for ex in EXERCISES_SEED:
        if "normalized_name" not in ex:
            ex["normalized_name"] = normalize_name(ex["name"])
        ex["updated_at"] = now
        ex["is_active"] = True
        
        operations = {
            "$set": ex,
            "$setOnInsert": {"created_at": now}
        }
        exercises_operations.append(UpdateOne({"normalized_name": ex["normalized_name"]}, operations, upsert=True))
            
    if exercises_operations:
        result = await db.exercises.bulk_write(exercises_operations)
        print(f"Exercises -> Upserted: {result.upserted_count}, Modified: {result.modified_count}")
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(seed())
