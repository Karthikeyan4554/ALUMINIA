from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from app.core.database import get_db
from app.models.models import User, Profile, Conversation, Message, Notification
from app.schemas.schemas import ConversationOut, MessageOut, MessageCreate
from app.api.deps import get_current_user
from app.api.profiles import format_profile_out

router = APIRouter(prefix="/messages", tags=["Messaging"])

@router.get("/conversations")
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    convs = db.query(Conversation).filter(
        or_(Conversation.user1_id == current_user.id, Conversation.user2_id == current_user.id)
    ).order_by(desc(Conversation.updated_at)).all()

    result = []
    for c in convs:
        other_id = c.user2_id if c.user1_id == current_user.id else c.user1_id
        other_user = db.query(User).filter(User.id == other_id).first()
        if not other_user or not other_user.profile:
            continue

        last_msg = db.query(Message).filter(Message.conversation_id == c.id).order_by(desc(Message.created_at)).first()
        unread = db.query(Message).filter(
            Message.conversation_id == c.id,
            Message.sender_id != current_user.id,
            Message.is_read == False
        ).count()

        result.append({
            "id": c.id,
            "other_user": format_profile_out(other_user.profile, current_user.id, db),
            "last_message": {
                "id": last_msg.id,
                "conversation_id": last_msg.conversation_id,
                "sender_id": last_msg.sender_id,
                "content": last_msg.content,
                "is_read": last_msg.is_read,
                "created_at": last_msg.created_at
            } if last_msg else None,
            "unread_count": unread,
            "updated_at": c.updated_at
        })

    return result

@router.post("/start/{target_user_id}")
def start_or_get_conversation(
    target_user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id == target_user_id:
        raise HTTPException(status_code=400, detail="Cannot message yourself")

    u1, u2 = sorted([current_user.id, target_user_id])
    conv = db.query(Conversation).filter(
        Conversation.user1_id == u1,
        Conversation.user2_id == u2
    ).first()

    if not conv:
        conv = Conversation(user1_id=u1, user2_id=u2)
        db.add(conv)
        db.commit()
        db.refresh(conv)

    return {"conversation_id": conv.id}

@router.get("/conversations/{conversation_id}/messages")
def get_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv or (conv.user1_id != current_user.id and conv.user2_id != current_user.id):
        raise HTTPException(status_code=404, detail="Conversation not found or unauthorized")

    # Mark incoming messages as read
    db.query(Message).filter(
        Message.conversation_id == conversation_id,
        Message.sender_id != current_user.id,
        Message.is_read == False
    ).update({"is_read": True})
    db.commit()

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()

    return [
        {
            "id": m.id,
            "conversation_id": m.conversation_id,
            "sender_id": m.sender_id,
            "content": m.content,
            "is_read": m.is_read,
            "created_at": m.created_at
        } for m in messages
    ]

@router.post("/conversations/{conversation_id}/messages", response_model=MessageOut)
def send_message(
    conversation_id: str,
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not data.content.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv or (conv.user1_id != current_user.id and conv.user2_id != current_user.id):
        raise HTTPException(status_code=404, detail="Conversation not found or unauthorized")

    msg = Message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=data.content.strip()
    )
    db.add(msg)
    conv.updated_at = datetime.now(timezone.utc)

    # Notify recipient
    recipient_id = conv.user2_id if conv.user1_id == current_user.id else conv.user1_id
    sender_name = current_user.profile.full_name if current_user.profile else "A peer"
    notif = Notification(
        user_id=recipient_id,
        type="message",
        title="New Message",
        message=f"{sender_name}: {data.content[:50]}...",
        link=f"/messages?conversation_id={conv.id}"
    )
    db.add(notif)
    db.commit()
    db.refresh(msg)

    return {
        "id": msg.id,
        "conversation_id": msg.conversation_id,
        "sender_id": msg.sender_id,
        "content": msg.content,
        "is_read": msg.is_read,
        "created_at": msg.created_at
    }
