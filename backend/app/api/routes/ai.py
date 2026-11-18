from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from app.models.ai import ChatRequest, ChatResponse, AIConversation
from app.services.ai_context import build_user_context
from app.services.ai_prompts import get_system_prompt
from app.services.ai_service import call_llm
from datetime import datetime, timezone

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    user_id = str(current_user["_id"])
    
    # 1. Load context
    user_context = await build_user_context(user_id, db)
    system_prompt = get_system_prompt(user_context)
    
    # 2. Get or create conversation
    conversation_id = request.conversation_id
    chat_history = []
    
    if conversation_id:
        if not ObjectId.is_valid(conversation_id):
            raise HTTPException(status_code=400, detail="Invalid conversation ID")
        conv = await db.ai_conversations.find_one({"_id": ObjectId(conversation_id), "user_id": user_id})
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
            
        chat_history = conv.get("messages", [])[-10:] # Limit to last 10 messages for context
    else:
        # Create new conversation
        title = request.message[:40] + "..." if len(request.message) > 40 else request.message
        res = await db.ai_conversations.insert_one({
            "user_id": user_id,
            "title": title,
            "messages": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        })
        conversation_id = str(res.inserted_id)
        
    # 3. Call LLM Service
    llm_result = await call_llm(
        user_message=request.message,
        system_prompt=system_prompt,
        chat_history=chat_history,
        user_id=user_id,
        db=db,
        user_context=user_context
    )
    
    # 4. Save messages to DB
    new_user_msg = {
        "role": "user",
        "content": request.message,
        "created_at": datetime.now(timezone.utc)
    }
    
    new_model_msg = {
        "role": "model",
        "content": llm_result["message"],
        "structured_data": llm_result.get("structured_data"),
        "tool_events": [t for t in llm_result["tool_events"]],
        "created_at": datetime.now(timezone.utc)
    }
    
    await db.ai_conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$push": {"messages": {"$each": [new_user_msg, new_model_msg]}},
            "$set": {"updated_at": datetime.now(timezone.utc)}
        }
    )
    
    return {
        "conversation_id": conversation_id,
        "message": llm_result["message"],
        "structured_data": llm_result.get("structured_data"),
        "tool_events": llm_result["tool_events"]
    }

@router.get("/conversations")
async def get_conversations(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    user_id = str(current_user["_id"])
    cursor = db.ai_conversations.find({"user_id": user_id}).sort("updated_at", -1)
    convs = await cursor.to_list(length=50)
    
    result = []
    for c in convs:
        result.append({
            "id": str(c["_id"]),
            "title": c.get("title"),
            "updated_at": c.get("updated_at")
        })
    return result

@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    user_id = str(current_user["_id"])
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    conv = await db.ai_conversations.find_one({"_id": ObjectId(conversation_id), "user_id": user_id})
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
        
    # Serialize ObjectId to string for Pydantic/FastAPI JSON
    conv["id"] = str(conv["_id"])
    del conv["_id"]
    return conv

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    user_id = str(current_user["_id"])
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    result = await db.ai_conversations.delete_one({"_id": ObjectId(conversation_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
        
    return {"status": "success"}
