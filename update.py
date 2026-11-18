import re

fp = 'backend/app/api/routes/plans.py'
content = open(fp, 'r', encoding='utf-8').read()

pattern = re.compile(r'@router\.post\(\"/meals/\{plan_id\}/log\"\).*?return serialize_meal_plan\(updated_plan\)', re.DOTALL)

code = '''@router.post(\"/meals/{plan_id}/log\")
async def log_meal_plan_to_diary(plan_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    plan = await db.meal_plans.find_one({\"_id\": ObjectId(plan_id), \"user_id\": str(current_user[\"_id\"])})
    if not plan:
        raise HTTPException(status_code=404, detail=\"Plan not found\")
    
    await db.meal_plans.update_one({\"_id\": ObjectId(plan_id)}, {\"\": {\"status\": \"completed\", \"updated_at\": datetime.utcnow()}})
    
    dt = datetime.fromisoformat(plan[\"date\"]) if \"T\" not in plan[\"date\"] else datetime.fromisoformat(plan[\"date\"].split(\"T\")[0])
    
    # Clean up previous logs for this plan to prevent duplicates
    await db.meals.delete_many({
        \"user_id\": str(current_user[\"_id\"]),
        \"consumed_at\": dt,
        \"notes\": \"From Meal Plan\"
    })
    
    docs = []
    for m in plan.get(\"meals\", []):
        if m.get(\"status\") != \"rejected\":
            docs.append({
                \"user_id\": str(current_user[\"_id\"]),
                \"meal_type\": m.get(\"meal_type\", \"snack\").lower(),
                \"meal_name\": m.get(\"meal_name\", \"Planned Meal\"),
                \"consumed_at\": dt,
                \"serving_size\": m.get(\"serving_size\", \"1 serving\"),
                \"calories\": m.get(\"calories\", 0),
                \"protein_grams\": m.get(\"protein\", 0),
                \"carbohydrates_grams\": m.get(\"carbs\", 0),
                \"fat_grams\": m.get(\"fats\", 0),
                \"fiber_grams\": m.get(\"fiber\", 0),
                \"notes\": \"From Meal Plan\",
                \"created_at\": datetime.utcnow(),
                \"updated_at\": datetime.utcnow()
            })
            
    if docs:
        await db.meals.insert_many(docs)
        
    updated_plan = await db.meal_plans.find_one({\"_id\": ObjectId(plan_id)})
    return serialize_meal_plan(updated_plan)'''

content = re.sub(pattern, code, content)
open(fp, 'w', encoding='utf-8').write(content)