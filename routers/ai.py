from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List
import httpx
from config import MINIMAX_API_KEY

router = APIRouter(prefix="/ai", tags=["AI"])

class GenerateInstructionsRequest(BaseModel):
    currentPrompt: str
    systemPrompt: str

class GenerateInstructionsResponse(BaseModel):
    instructions: str

MINIMAX_API_URL = "https://api.minimax.io/anthropic/v1/messages"
MODEL = "MiniMax-M2"
MAX_TOKENS = 2048

@router.post("/generate-instructions", response_model=GenerateInstructionsResponse)
async def generate_instructions(
    request: GenerateInstructionsRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID")
):
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            minimax_response = await client.post(
                MINIMAX_API_URL,
                headers={
                    "Authorization": f"Bearer {MINIMAX_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "system": request.systemPrompt,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Based on the following job description or topic, generate a compelling Upwork proposal introduction:\n\n{request.currentPrompt}"
                                }
                            ]
                        }
                    ]
                }
            )
        
        if minimax_response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"MiniMax API error: {minimax_response.text}"
            )
        
        response_data = minimax_response.json()
        content = response_data.get("content", [])
        
        instructions_text = ""
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    instructions_text = item.get("text", "")
                    break
        
        return GenerateInstructionsResponse(instructions=instructions_text)
    
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to MiniMax API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate instructions: {str(e)}"
        )
