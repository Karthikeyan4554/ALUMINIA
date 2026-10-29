from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.core.database import get_db
from app.models.models import User, Profile, Connection, ConnectionRequest, Notification
from app.schemas.schemas import ConnectionRequestCreate, ConnectionRequestOut, ProfileOut
from app.api.deps import get_current_user
from app.api.profiles import format_profile_out

router = APIRouter(prefix="/connections", tags=["Connections"])

@router.post("/request", response_model=ConnectionRequestOut)
def send_connection_request(
    data: ConnectionRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id == data.receiver_id:
        raise HTTPException(status_code=400, detail="You cannot send a connection request to yourself")

    receiver = db.query(User).filter(User.id == data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver user not found")

    # Check existing connection
    u1, u2 = sorted([current_user.id, data.receiver_id])
    existing_conn = db.query(Connection).filter(
        Connection.user1_id == u1,
        Connection.user2_id == u2
    ).first()
    if existing_conn:
        raise HTTPException(status_code=400, detail="You are already connected with this user")

    # Check pending request
    existing_req = db.query(ConnectionRequest).filter(
        or_(
            and_(ConnectionRequest.sender_id == current_user.id, ConnectionRequest.receiver_id == data.receiver_id),
            and_(ConnectionRequest.sender_id == data.receiver_id, ConnectionRequest.receiver_id == current_user.id)
        ),
        ConnectionRequest.status == "pending"
    ).first()

    if existing_req:
        raise HTTPException(status_code=400, detail="A pending connection request already exists between you")

    req = ConnectionRequest(
        sender_id=current_user.id,
        receiver_id=data.receiver_id,
        message=data.message,
        status="pending"
    )
    db.add(req)

    # Create notification for receiver
    sender_name = current_user.profile.full_name if current_user.profile else "A university member"
    notif = Notification(
        user_id=data.receiver_id,
        type="connection_request",
        title="New Connection Request",
        message=f"{sender_name} sent you a connection request.",
        link="/connections"
    )
    db.add(notif)
    db.commit()
    db.refresh(req)

    return {
        "id": req.id,
        "sender_id": req.sender_id,
        "receiver_id": req.receiver_id,
        "message": req.message,
        "status": req.status,
        "created_at": req.created_at,
        "sender_profile": format_profile_out(current_user.profile, current_user.id, db) if current_user.profile else None,
        "receiver_profile": format_profile_out(receiver.profile, current_user.id, db) if receiver.profile else None
    }

@router.get("/requests")
def get_connection_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    incoming = db.query(ConnectionRequest).filter(
        ConnectionRequest.receiver_id == current_user.id,
        ConnectionRequest.status == "pending"
    ).all()

    outgoing = db.query(ConnectionRequest).filter(
        ConnectionRequest.sender_id == current_user.id,
        ConnectionRequest.status == "pending"
    ).all()

    def format_req(r: ConnectionRequest):
        sender = db.query(User).filter(User.id == r.sender_id).first()
        receiver = db.query(User).filter(User.id == r.receiver_id).first()
        return {
            "id": r.id,
            "sender_id": r.sender_id,
            "receiver_id": r.receiver_id,
            "message": r.message,
            "status": r.status,
            "created_at": r.created_at,
            "sender_profile": format_profile_out(sender.profile, current_user.id, db) if sender and sender.profile else None,
            "receiver_profile": format_profile_out(receiver.profile, current_user.id, db) if receiver and receiver.profile else None
        }

    return {
        "incoming": [format_req(r) for r in incoming],
        "outgoing": [format_req(r) for r in outgoing]
    }

@router.post("/requests/{request_id}/accept")
def accept_request(
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    req = db.query(ConnectionRequest).filter(
        ConnectionRequest.id == request_id,
        ConnectionRequest.receiver_id == current_user.id,
        ConnectionRequest.status == "pending"
    ).first()

    if not req:
        raise HTTPException(status_code=404, detail="Pending request not found")

    req.status = "accepted"

    # Establish connection
    u1, u2 = sorted([req.sender_id, req.receiver_id])
    conn = Connection(user1_id=u1, user2_id=u2)
    db.add(conn)

    # Notify sender
    user_name = current_user.profile.full_name if current_user.profile else "A peer"
    notif = Notification(
        user_id=req.sender_id,
        type="connection_accepted",
        title="Connection Accepted",
        message=f"{user_name} accepted your connection request.",
        link=f"/profile/{current_user.id}"
    )
    db.add(notif)
    db.commit()

    return {"message": "Connection request accepted successfully"}

@router.post("/requests/{request_id}/reject")
def reject_request(
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    req = db.query(ConnectionRequest).filter(
        ConnectionRequest.id == request_id,
        ConnectionRequest.receiver_id == current_user.id,
        ConnectionRequest.status == "pending"
    ).first()

    if not req:
        raise HTTPException(status_code=404, detail="Pending request not found")

    req.status = "rejected"
    db.commit()
    return {"message": "Connection request rejected"}

@router.post("/requests/{request_id}/cancel")
def cancel_request(
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    req = db.query(ConnectionRequest).filter(
        ConnectionRequest.id == request_id,
        ConnectionRequest.sender_id == current_user.id,
        ConnectionRequest.status == "pending"
    ).first()

    if not req:
        raise HTTPException(status_code=404, detail="Pending request not found")

    req.status = "cancelled"
    db.commit()
    return {"message": "Connection request cancelled"}

@router.get("", response_model=List[ProfileOut])
def list_connections(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conns = db.query(Connection).filter(
        or_(Connection.user1_id == current_user.id, Connection.user2_id == current_user.id)
    ).all()

    other_ids = [c.user2_id if c.user1_id == current_user.id else c.user1_id for c in conns]
    profiles = db.query(Profile).filter(Profile.user_id.in_(other_ids)).all()

    return [format_profile_out(p, current_user.id, db) for p in profiles]

@router.delete("/{target_user_id}")
def remove_connection(
    target_user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    u1, u2 = sorted([current_user.id, target_user_id])
    conn = db.query(Connection).filter(
        Connection.user1_id == u1,
        Connection.user2_id == u2
    ).first()

    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")

    db.delete(conn)
    db.commit()
    return {"message": "Connection successfully removed"}
