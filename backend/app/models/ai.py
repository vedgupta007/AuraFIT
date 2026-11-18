from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime, timezone

class AIChatMessage(BaseModel):
    role: str # "user", "model", "system"
    content: str
    structured_data: Optional[Dict[str, Any]] = None
    tool_calls: Optional[List[dict]] = None
    tool_events: Optional[List[dict]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AIConversationBase(BaseModel):
    user_id: str
    title: str = "New Conversation"
    messages: List[AIChatMessage] = []

class AIConversation(AIConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context_item_id: Optional[str] = None
    context_type: Optional[str] = None

class ToolExecutionResult(BaseModel):
    tool_name: str
    success: bool
    data: Optional[Any] = None
    error_message: Optional[str] = None

# Structured Response Schemas
class AISection(BaseModel):
    title: Optional[str] = None
    items: List[str] = []

class StructuredAIResponse(BaseModel):
    answer: str = Field(description="The main answer in two or three clear sentences.")
    sections: List[AISection] = Field(default=[], description="Structured sections with titles and items (bullets or numbers) for steps/guidance.")
    response_type: str = Field(description="Type of response: 'general', 'food', 'workout', 'plan', or 'safety'.")
    citations_or_sources: List[str] = Field(default=[], description="Any references or citations.")

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    structured_data: Optional[StructuredAIResponse] = None
    tool_events: List[ToolExecutionResult] = []
