import json
from google import genai
from google.genai import types
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.models.ai import ToolExecutionResult, StructuredAIResponse, AISection
from app.services.ai_tools import TOOLS_REGISTRY

# Combine all declarations into a single Tool list for Gemini
gemini_tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_foods",
                description="Search the database for specific foods, their calories, macros, or suitable options based on dietary preferences. Also returns valid food_id values.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "search": types.Schema(type=types.Type.STRING, description="Food name or query"),
                        "category": types.Schema(type=types.Type.STRING, description="Food category (e.g., Grains, Dairy, Legumes)"),
                        "diet": types.Schema(type=types.Type.STRING, description="Dietary preference (e.g., vegetarian, vegan, non_vegetarian)")
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
                description="Find an alternative food for a specific food ID that respects the user's diet.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "food_id": types.Schema(type=types.Type.STRING, description="The ID of the food to replace")
                    },
                    required=["food_id"]
                )
            ),
            types.FunctionDeclaration(
                name="search_exercises",
                description="Search the database for exercises.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "search": types.Schema(type=types.Type.STRING, description="Exercise name"),
                        "muscle": types.Schema(type=types.Type.STRING, description="Target muscle group"),
                        "equipment": types.Schema(type=types.Type.STRING, description="Required equipment")
                    }
                )
            ),
            types.FunctionDeclaration(
                name="get_exercise_details",
                description="Get full instructions and details for a specific exercise ID.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "exercise_id": types.Schema(type=types.Type.STRING, description="The ID of the exercise")
                    },
                    required=["exercise_id"]
                )
            ),
            types.FunctionDeclaration(
                name="find_alternative_exercise",
                description="Find an alternative exercise targeting the same muscles.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "exercise_id": types.Schema(type=types.Type.STRING, description="The ID of the exercise to replace")
                    },
                    required=["exercise_id"]
                )
            ),
            types.FunctionDeclaration(
                name="get_current_plan",
                description="Get the user's current logged meals or plan.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={}
                )
            ),
            types.FunctionDeclaration(
                name="swap_meal_food",
                description="Swap a food in the user's tracked meals. Alias for replace_food_in_plan.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "meal_id": types.Schema(type=types.Type.STRING, description="The ID of the meal to update"),
                        "new_food_id": types.Schema(type=types.Type.STRING, description="The ID of the new food to swap in")
                    },
                    required=["meal_id", "new_food_id"]
                )
            )
        ]
    )
]

async def call_llm(user_message: str, system_prompt: str, chat_history: List[Dict[str, Any]], user_id: str, db, user_context: Dict[str, Any]) -> Dict[str, Any]:
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here" or settings.GEMINI_API_KEY == "replace_with_new_rotated_key":
        return {
            "message": "Gemini configuration is missing. Please configure a valid GEMINI_API_KEY in the backend .env file.",
            "tool_events": []
        }
        
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    contents = []
    for msg in chat_history:
        contents.append(
            types.Content(role=msg["role"], parts=[types.Part.from_text(text=msg["content"])])
        )
        
    contents.append(
        types.Content(role="user", parts=[types.Part.from_text(text=user_message)])
    )
    
    try:
        tool_events = []
        final_text = ""
        structured_data = None
        
        MAX_ITERATIONS = 5
        for iter_count in range(MAX_ITERATIONS):
            # We ONLY enforce JSON schema on the final generation step when no tool calls are expected, 
            # OR we can enforce it initially and the model can choose to call a tool or output JSON.
            # Using google-genai, we can pass response_schema to the config.
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=gemini_tools,
                temperature=0.7,
                response_mime_type="application/json",
                response_schema=StructuredAIResponse
            )

            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=contents,
                config=config
            )
            
            if not response.function_calls:
                final_text = response.text
                if final_text:
                    try:
                        # Parse the JSON response
                        parsed = json.loads(final_text)
                        structured_data = parsed
                    except Exception as e:
                        print("Failed to parse JSON response:", e, final_text)
                        structured_data = {
                            "answer": final_text,
                            "sections": [],
                            "response_type": "general",
                            "citations_or_sources": []
                        }
                break
                
            # CRITICAL: Preserve the exact model response content including thought_signatures
            if response.candidates and len(response.candidates) > 0 and response.candidates[0].content:
                contents.append(response.candidates[0].content)
            else:
                break
                
            tool_response_parts = []
            
            for fc in response.function_calls:
                tool_name = fc.name
                args = fc.args
                
                tool_result = {"success": False, "error_message": "Unknown tool"}
                
                if tool_name in TOOLS_REGISTRY:
                    tool_fn = TOOLS_REGISTRY[tool_name]
                    try:
                        # Convert protobuf args to dict if necessary, genai usually returns dict-like
                        args_dict = dict(args) if args else {}
                        
                        if tool_name in ["swap_meal_food", "replace_food_in_plan", "replace_exercise_in_plan"]:
                            result_data = await tool_fn(db, args_dict, user_id)
                        else:
                            result_data = await tool_fn(db, args_dict, user_context)
                            
                        tool_result = {
                            "success": "error" not in result_data,
                            "data": result_data,
                            "error_message": result_data.get("error")
                        }
                    except Exception as e:
                        tool_result = {
                            "success": False,
                            "error_message": f"Tool execution failed: {str(e)}"
                        }
                
                tool_events.append({
                    "tool_name": tool_name,
                    "success": tool_result["success"],
                    "data": tool_result.get("data"),
                    "error_message": tool_result.get("error_message")
                })
                
                tool_response_parts.append(
                    types.Part.from_function_response(
                        name=tool_name,
                        response=tool_result
                    )
                )
                
            # Append all tool responses as a single user turn
            contents.append(types.Content(role="user", parts=tool_response_parts))
            
        else:
            # Reached max iterations
            final_text = '{"answer": "I need a moment to think. Please try asking again.", "sections": [], "response_type": "general", "citations_or_sources": []}'
            structured_data = json.loads(final_text)
            
        return {
            "message": final_text,
            "structured_data": structured_data,
            "tool_events": tool_events
        }
    except Exception as e:
        error_str = str(e)
        if "404" in error_str or "NOT_FOUND" in error_str:
            fallback = {"answer": "The configured AI model is currently unavailable or not found. Please contact support to check the model configuration.", "sections": [], "response_type": "safety", "citations_or_sources": []}
        elif "429" in error_str or "quota" in error_str.lower():
            fallback = {"answer": "The AI Coach is currently receiving too many requests or has exceeded its quota limit. Please wait a moment before trying again.", "sections": [], "response_type": "safety", "citations_or_sources": []}
        elif "API_KEY_INVALID" in error_str or "API key" in error_str or "400" in error_str:
            fallback = {"answer": f"The AI provider rejected the request. Details: {error_str}", "sections": [], "response_type": "safety", "citations_or_sources": []}
        else:
            fallback = {"answer": f"The service is temporarily unavailable. Details: {error_str}", "sections": [], "response_type": "safety", "citations_or_sources": []}
            
        return {
            "message": json.dumps(fallback),
            "structured_data": fallback,
            "tool_events": []
        }
