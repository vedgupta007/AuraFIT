import pytest
from unittest.mock import patch, MagicMock
from google.genai import types

@pytest.fixture
def auth_token(client):
    client.post("/api/v1/auth/register", json={
        "email": "ai2@example.com",
        "password": "strongpassword123"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "ai2@example.com",
        "password": "strongpassword123"
    })
    return login.json()["access_token"]

@patch("app.services.ai_service.settings.GEMINI_API_KEY", "dummy_key")
@patch("app.services.ai_service.genai.Client")
def test_ai_chat_mock_simple(mock_genai, client, auth_token):
    mock_client_instance = MagicMock()
    mock_genai.return_value = mock_client_instance
    
    mock_response = MagicMock()
    mock_response.text = "This is a mocked response."
    mock_response.function_calls = None
    mock_client_instance.models.generate_content.return_value = mock_response
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post("/api/v1/ai/chat", json={"message": "Hello"}, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["message"] == "This is a mocked response."

@patch("app.services.ai_service.settings.GEMINI_API_KEY", "dummy_key")
@patch("app.services.ai_service.genai.Client")
def test_ai_chat_mock_tool_call(mock_genai, client, auth_token):
    mock_client_instance = MagicMock()
    mock_genai.return_value = mock_client_instance
    
    # First response: function call
    mock_fc_response = MagicMock()
    mock_fc_response.function_calls = [
        MagicMock(name="search_foods", args={"search": "apple"})
    ]
    mock_fc_response.function_calls[0].name = "search_foods"
    mock_fc_response.function_calls[0].args = {"search": "apple"}
    
    mock_content = MagicMock()
    mock_fc_response.candidates = [MagicMock(content=mock_content)]
    
    # Second response: text
    mock_text_response = MagicMock()
    mock_text_response.text = "Here is your food."
    mock_text_response.function_calls = None
    
    mock_client_instance.models.generate_content.side_effect = [mock_fc_response, mock_text_response]
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post("/api/v1/ai/chat", json={"message": "Find apple"}, headers=headers)
    
    assert res.status_code == 200
    data = res.json()
    assert data["message"] == "Here is your food."
    assert len(data["tool_events"]) == 1
    assert data["tool_events"][0]["tool_name"] == "search_foods"
