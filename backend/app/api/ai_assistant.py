from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, Profile
from app.schemas.schemas import AIAssistantRequest, AIAssistantResponse
from app.services.ai_service import ai_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Networking Assistant"])

@router.post("/assistant", response_model=AIAssistantResponse)
def chat_with_assistant(
    data: AIAssistantRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = current_user.profile
    if not profile:
        raise HTTPException(status_code=400, detail="Profile required to interact with AI Networking Assistant")

    target_alumni = None
    if data.target_user_id:
        target_alumni = db.query(Profile).filter(Profile.user_id == data.target_user_id).first()

    result = ai_service.generate_response(
        db=db,
        current_user=current_user,
        user_message=data.message,
        task=data.task or "general",
        target_alumni=target_alumni,
        history=data.history
    )

    return AIAssistantResponse(
        response=result["response"],
        suggested_actions=result.get("suggested_actions", []),
        recommended_alumni=result.get("recommended_alumni", []),
        is_llm_generated=result.get("is_llm_generated", False)
    )
