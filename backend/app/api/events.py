from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.models.models import User, Event, EventRegistration, Notification
from app.schemas.schemas import EventCreate, EventOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/events", tags=["Alumni Events"])

def format_event_out(e: Event, current_user_id: str, db: Session) -> dict:
    reg_count = db.query(EventRegistration).filter(
        EventRegistration.event_id == e.id,
        EventRegistration.status == "registered"
    ).count()

    is_reg = db.query(EventRegistration).filter(
        EventRegistration.event_id == e.id,
        EventRegistration.user_id == current_user_id,
        EventRegistration.status == "registered"
    ).first() is not None

    return {
        "id": e.id,
        "organizer_id": e.organizer_id,
        "title": e.title,
        "event_type": e.event_type,
        "description": e.description,
        "location": e.location,
        "is_virtual": e.is_virtual,
        "virtual_meeting_link": e.virtual_meeting_link,
        "start_time": e.start_time,
        "end_time": e.end_time,
        "capacity": e.capacity,
        "banner_url": e.banner_url,
        "status": e.status,
        "registered_count": reg_count,
        "is_registered": is_reg,
        "created_at": e.created_at
    }

@router.get("", response_model=List[EventOut])
def list_events(
    event_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    q = db.query(Event).filter(Event.status != "cancelled")
    if event_type and event_type != "All":
        q = q.filter(Event.event_type == event_type)

    events = q.order_by(Event.start_time.asc()).all()
    return [format_event_out(e, current_user.id, db) for e in events]

@router.post("", response_model=EventOut)
def create_event(
    data: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["alumni", "admin"]:
        raise HTTPException(status_code=403, detail="Only alumni and administrators can host platform events")

    event = Event(
        organizer_id=current_user.id,
        title=data.title,
        event_type=data.event_type,
        description=data.description,
        location=data.location,
        is_virtual=data.is_virtual,
        virtual_meeting_link=data.virtual_meeting_link or ("https://meet.google.com/alm-evt-2026" if data.is_virtual else None),
        start_time=data.start_time,
        end_time=data.end_time,
        capacity=data.capacity,
        banner_url=data.banner_url or "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&auto=format&fit=crop&q=80",
        status="upcoming"
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    return format_event_out(event, current_user.id, db)

@router.post("/{event_id}/register")
def register_for_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    existing = db.query(EventRegistration).filter(
        EventRegistration.event_id == event_id,
        EventRegistration.user_id == current_user.id
    ).first()

    if existing and existing.status == "registered":
        raise HTTPException(status_code=400, detail="You are already registered for this event")

    reg_count = db.query(EventRegistration).filter(
        EventRegistration.event_id == event_id,
        EventRegistration.status == "registered"
    ).count()

    if reg_count >= event.capacity:
        raise HTTPException(status_code=400, detail="This event has reached full capacity")

    if existing:
        existing.status = "registered"
        existing.registered_at = datetime.now(timezone.utc)
    else:
        reg = EventRegistration(
            event_id=event_id,
            user_id=current_user.id,
            status="registered"
        )
        db.add(reg)

    notif = Notification(
        user_id=current_user.id,
        type="event_reminder",
        title="Event Registration Confirmed",
        message=f"You're registered for '{event.title}'.",
        link="/events"
    )
    db.add(notif)
    db.commit()

    return {"message": "Successfully registered for event"}

@router.post("/{event_id}/cancel")
def cancel_registration(
    event_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reg = db.query(EventRegistration).filter(
        EventRegistration.event_id == event_id,
        EventRegistration.user_id == current_user.id,
        EventRegistration.status == "registered"
    ).first()

    if not reg:
        raise HTTPException(status_code=400, detail="Registration not found")

    reg.status = "cancelled"
    db.commit()
    return {"message": "Event registration cancelled"}
