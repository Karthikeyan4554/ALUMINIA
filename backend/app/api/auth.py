from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.models import User, Profile
from app.schemas.schemas import UserRegister, UserLogin, Token, ProfileOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists"
        )
    
    hashed = get_password_hash(data.password)
    user = User(
        email=data.email.lower(),
        hashed_password=hashed,
        role=data.role,
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.flush()

    # Create associated profile
    avatar = f"https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&auto=format&fit=crop&q=80" if data.role == "alumni" else "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=200&auto=format&fit=crop&q=80"
    profile = Profile(
        user_id=user.id,
        full_name=data.full_name,
        role=data.role,
        department=data.department,
        graduation_year=data.graduation_year,
        avatar_url=avatar,
        headline=f"{'Alumnus' if data.role == 'alumni' else 'Student'} | {data.department or 'Engineering'}",
        profile_completion_percentage=45,
        is_profile_complete=False
    )
    db.add(profile)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.id, role=user.role)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "full_name": profile.full_name,
            "avatar_url": profile.avatar_url
        }
    }

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Contact platform administrator."
        )

    profile = user.profile
    token = create_access_token(subject=user.id, role=user.role)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "full_name": profile.full_name if profile else user.email,
            "avatar_url": profile.avatar_url if profile else None
        }
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    profile = current_user.profile
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "profile": profile
    }

@router.post("/forgot-password")
def forgot_password(data: dict):
    # Simulated secure token issuance for educational project demonstration
    email = data.get("email")
    return {"message": f"If an account exists with {email}, password reset instructions have been dispatched."}

@router.post("/reset-password")
def reset_password(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    new_password = data.get("new_password")
    if not email or not new_password:
        raise HTTPException(status_code=400, detail="Email and new password required")
    user = db.query(User).filter(User.email == email.lower()).first()
    if user:
        user.hashed_password = get_password_hash(new_password)
        db.commit()
    return {"message": "Password successfully updated."}
