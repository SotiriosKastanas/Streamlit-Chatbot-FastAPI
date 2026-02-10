from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
from backend.qa import get_response

app = FastAPI(title="Chat Backend")

class ChatRequest(BaseModel):
    messages: List[Dict[str, Any]]
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    conversation_id: str
    metadata: Dict[str, Any]

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    try:
        conversation_id = req.conversation_id or str(uuid.uuid4())
        answer = get_response(req.messages)
        return {
            "answer": answer,
            "conversation_id": conversation_id,
            "metadata": {
                "user_id": req.user_id,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
