from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# USER SCHEMAS
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    role: str
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# PROFILE SCHEMAS
class ProfileBase(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=12, le=120)
    sex: str = Field(..., pattern="^(M|F|Other)$")
    height_cm: float = Field(..., gt=0, lt=300)
    weight_kg: float = Field(..., gt=0)
    
    goal: str = Field(..., pattern="^(lose_weight|maintain_weight|gain_muscle|improve_fitness)$")
    activity_level: str = Field(..., pattern="^(sedentary|light|moderate|active|very_active)$")
    training_experience: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    preferred_workout_frequency: int = Field(..., ge=1, le=7)
    
    dietary_preference: str = Field(..., pattern="^(vegetarian|vegan|eggetarian|non_vegetarian|other)$")
    allergies: List[str] = []
    disliked_foods: List[str] = []

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    age: Optional[int] = Field(None, ge=12, le=120)
    sex: Optional[str] = Field(None, pattern="^(M|F|Other)$")
    height_cm: Optional[float] = Field(None, gt=0, lt=300)
    weight_kg: Optional[float] = Field(None, gt=0)
    
    goal: Optional[str] = Field(None, pattern="^(lose_weight|maintain_weight|gain_muscle|improve_fitness)$")
    activity_level: Optional[str] = Field(None, pattern="^(sedentary|light|moderate|active|very_active)$")
    training_experience: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    preferred_workout_frequency: Optional[int] = Field(None, ge=1, le=7)
    
    dietary_preference: Optional[str] = Field(None, pattern="^(vegetarian|vegan|eggetarian|non_vegetarian|other)$")
    allergies: Optional[List[str]] = None
    disliked_foods: Optional[List[str]] = None

class ProfileResponse(ProfileBase):
    user_id: str


# NUTRITION SCHEMAS
class SavedMealBase(BaseModel):
    meal_name: str = Field(..., min_length=1, max_length=100)
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner|snack)$")
    serving_size: str = Field(..., min_length=1, max_length=50)
    calories: int = Field(..., ge=0)
    protein_grams: float = Field(..., ge=0)
    carbohydrates_grams: float = Field(..., ge=0)
    fat_grams: float = Field(..., ge=0)
    fiber_grams: float = Field(..., ge=0)
    ingredients: List[str] = []
    notes: Optional[str] = Field(None, max_length=500)

class SavedMealCreate(SavedMealBase):
    pass

class SavedMealResponse(SavedMealBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
class MealBase(BaseModel):
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner|snack)$")
    meal_name: str = Field(..., min_length=1, max_length=100)
    consumed_at: datetime
    serving_size: str = Field(..., min_length=1, max_length=50)
    calories: int = Field(..., ge=0)
    protein_grams: float = Field(..., ge=0)
    carbohydrates_grams: float = Field(..., ge=0)
    fat_grams: float = Field(..., ge=0)
    fiber_grams: float = Field(..., ge=0)
    notes: Optional[str] = Field(None, max_length=500)

class MealCreate(MealBase):
    pass

class MealUpdate(BaseModel):
    meal_type: Optional[str] = Field(None, pattern="^(breakfast|lunch|dinner|snack)$")
    meal_name: Optional[str] = Field(None, min_length=1, max_length=100)
    consumed_at: Optional[datetime] = None
    serving_size: Optional[str] = Field(None, min_length=1, max_length=50)
    calories: Optional[int] = Field(None, ge=0)
    protein_grams: Optional[float] = Field(None, ge=0)
    carbohydrates_grams: Optional[float] = Field(None, ge=0)
    fat_grams: Optional[float] = Field(None, ge=0)
    fiber_grams: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=500)

class MealResponse(MealBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class DailySummaryResponse(BaseModel):
    date: str
    total_calories: int
    total_protein: float
    total_carbohydrates: float
    total_fat: float
    total_fiber: float
    meal_count: int

class NutritionGoalsResponse(BaseModel):
    bmr: int
    tdee: int
    daily_calories: int
    daily_protein: float
    daily_carbohydrates: float
    daily_fat: float
    daily_fiber: float

# FOOD SCHEMAS
class FoodBase(BaseModel):
    name: str = Field(..., min_length=1)
    category: str
    serving_size: float = Field(..., gt=0)
    serving_unit: str
    calories: float = Field(..., ge=0)
    protein: float = Field(..., ge=0)
    carbohydrates: float = Field(..., ge=0)
    fat: float = Field(..., ge=0)
    fiber: float = Field(..., ge=0)
    diet_types: List[str] = []
    allergens: List[str] = []
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_eggetarian: bool = False
    is_active: bool = True

class FoodResponse(FoodBase):
    id: str
    created_at: datetime
    updated_at: datetime

class PaginatedFoodResponse(BaseModel):
    items: List[FoodResponse]
    total: int
    page: int
    size: int
    pages: int

# EXERCISE SCHEMAS
class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: str
    category: str
    primary_muscle: str
    secondary_muscles: List[str] = []
    equipment: str
    difficulty: str = Field(..., pattern="^(Beginner|Intermediate|Advanced)$")
    instructions: List[str]
    sets_recommendation: Optional[str] = None
    reps_recommendation: Optional[str] = None
    duration_seconds: Optional[int] = None
    safety_notes: Optional[str] = None
    is_active: bool = True

class ExerciseResponse(ExerciseBase):
    id: str
    created_at: datetime
    updated_at: datetime

class PaginatedExerciseResponse(BaseModel):
    items: List[ExerciseResponse]
    total: int
    page: int
    size: int
    pages: int

# --- WORKOUT MODELS ---

class ExerciseLogBase(BaseModel):
    exercise_name: str
    exercise_id: Optional[str] = None
    sets: int = Field(..., ge=0)
    reps: int = Field(..., ge=0)
    weight_kg: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[float] = Field(None, ge=0)
    distance_km: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None

class WorkoutBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    started_at: datetime
    ended_at: Optional[datetime] = None
    notes: Optional[str] = None
    exercises: List[ExerciseLogBase] = []

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    notes: Optional[str] = None
    exercises: Optional[List[ExerciseLogBase]] = None

class WorkoutResponse(WorkoutBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

# --- GOALS MODELS ---

class GoalBase(BaseModel):
    goal_type: str = Field(..., description="E.g., lose_weight, gain_muscle, improve_strength")
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    start_date: datetime
    target_date: Optional[datetime] = None
    status: str = Field(default="active", pattern="^(active|completed|paused|archived)$")

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    goal_type: Optional[str] = None
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    start_date: Optional[datetime] = None
    target_date: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(active|completed|paused|archived)$")

class GoalResponse(GoalBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


# --- MEASUREMENTS MODELS ---

class MeasurementBase(BaseModel):
    date: datetime
    weight_kg: Optional[float] = Field(None, ge=0)
    body_fat_percent: Optional[float] = Field(None, ge=0, le=100)
    waist_cm: Optional[float] = Field(None, ge=0)
    chest_cm: Optional[float] = Field(None, ge=0)
    arms_cm: Optional[float] = Field(None, ge=0)
    thighs_cm: Optional[float] = Field(None, ge=0)
    hips_cm: Optional[float] = Field(None, ge=0)
    neck_cm: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None

class MeasurementCreate(MeasurementBase):
    pass

class MeasurementUpdate(MeasurementBase):
    date: Optional[datetime] = None

class MeasurementResponse(MeasurementBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

# --- ACHIEVEMENTS MODELS ---
class AchievementBase(BaseModel):
    title: str
    description: str
    key: str
    earned_at: datetime

class AchievementResponse(AchievementBase):
    id: str
    user_id: str

# --- SETTINGS MODELS ---
class SettingsBase(BaseModel):
    workout_reminders: bool = False
    meal_reminders: bool = False
    weekly_summary: bool = True
    preferred_units: str = Field(default="metric", pattern="^(metric|imperial)$")

class SettingsResponse(SettingsBase):
    id: str
    user_id: str
    updated_at: datetime
    
class SettingsUpdate(BaseModel):
    workout_reminders: Optional[bool] = None
    meal_reminders: Optional[bool] = None
    weekly_summary: Optional[bool] = None
    preferred_units: Optional[str] = Field(None, pattern="^(metric|imperial)$")

# --- PLAN MODELS ---

class MealPlanBase(BaseModel):
    date: str
    meals: List[dict] # {meal_type, meal_name, calories, protein, carbs, fats, ingredients: [], status: 'generated' | 'accepted' | 'completed' | 'rejected'}
    status: str = Field(default="generated", pattern="^(generated|accepted|completed|rejected)$")
    total_calories: int = 0
    total_protein: float = 0

class MealPlanCreate(MealPlanBase):
    pass

class MealPlanUpdate(BaseModel):
    meals: Optional[List[dict]] = None
    status: Optional[str] = None
    total_calories: Optional[int] = None
    total_protein: Optional[float] = None

class MealPlanResponse(MealPlanBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class WorkoutPlanBase(BaseModel):
    date: str
    workout_title: str
    focus: str
    exercises: List[dict] # {exercise_name, sets, reps, weight_kg, duration, rest, completed}
    status: str = Field(default="generated", pattern="^(generated|accepted|completed|rejected)$")
    estimated_duration_minutes: int = 0

class WorkoutPlanCreate(WorkoutPlanBase):
    pass

class WorkoutPlanUpdate(BaseModel):
    workout_title: Optional[str] = None
    focus: Optional[str] = None
    exercises: Optional[List[dict]] = None
    status: Optional[str] = None
    estimated_duration_minutes: Optional[int] = None

class WorkoutPlanResponse(WorkoutPlanBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class FitnessPlanStrategyBase(BaseModel):
    strategy_text: str
    nutrition_protocol: str
    training_protocol: str
    status: str = Field(default="generated", pattern="^(generated|accepted|rejected)$")

class FitnessPlanStrategyCreate(FitnessPlanStrategyBase):
    pass

class FitnessPlanStrategyUpdate(BaseModel):
    strategy_text: Optional[str] = None
    nutrition_protocol: Optional[str] = None
    training_protocol: Optional[str] = None
    status: Optional[str] = None

class FitnessPlanStrategyResponse(FitnessPlanStrategyBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

