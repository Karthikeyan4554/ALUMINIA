import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.models import User, Profile, Connection, ConnectionRequest, Message, JobApplication, MentorshipRequest

client = TestClient(app)

def test_full_student_and_alumni_journey():
    # 1. Register a new student
    student_email = "new_student_e2e@alumnia.edu"
    password = "TestPassword123!"

    # Clean up if existed from previous run
    db = SessionLocal()
    existing = db.query(User).filter(User.email == student_email).first()
    if existing:
        db.query(ConnectionRequest).filter((ConnectionRequest.sender_id == existing.id) | (ConnectionRequest.receiver_id == existing.id)).delete()
        db.query(Connection).filter((Connection.user1_id == existing.id) | (Connection.user2_id == existing.id)).delete()
        db.query(Message).filter(Message.sender_id == existing.id).delete()
        db.query(JobApplication).filter(JobApplication.user_id == existing.id).delete()
        db.query(MentorshipRequest).filter((MentorshipRequest.student_id == existing.id) | (MentorshipRequest.mentor_id == existing.id)).delete()
        db.delete(existing)
        db.commit()
    db.close()

    reg_resp = client.post("/api/auth/register", json={
        "email": student_email,
        "password": password,
        "role": "student",
        "full_name": "Marcus Aurelius Vance",
        "department": "Computer Science & Engineering",
        "graduation_year": 2026,
        "location": "Boston, MA",
        "skills": ["Python", "FastAPI", "React", "PostgreSQL"],
        "target_roles": ["Software Engineer", "Backend Developer"],
        "preferred_industries": ["Software & Cloud", "FinTech"]
    })
    assert reg_resp.status_code in [200, 201], reg_resp.text
    student_token = reg_resp.json()["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}

    # 2. Update Student Profile with Work Experience, Education & Projects
    update_resp = client.put("/api/profiles/me", headers=student_headers, json={
        "headline": "CS Junior & Systems Enthusiast",
        "bio": "Passionate about building scalable distributed systems, databases, and AI tooling. Seeking high-impact software internships.",
        "skills": ["Python", "FastAPI", "React", "Docker", "PostgreSQL", "Go"],
        "target_roles": ["Software Engineer", "Systems Engineer"],
        "work_experiences": [
            {
                "title": "Backend Engineering Intern",
                "company": "Acme Cloud Corp",
                "location": "Boston, MA",
                "start_date": "2024-05",
                "end_date": "2024-08",
                "is_current": False,
                "description": "Architected microservices handling 2M requests/day using FastAPI and Redis."
            }
        ],
        "educations": [
            {
                "institution": "Alumnia Institute of Technology",
                "degree": "B.Tech",
                "field_of_study": "Computer Science",
                "start_year": 2022,
                "end_year": 2026,
                "grade": "3.92 / 4.0 GPA"
            }
        ],
        "projects": [
            {
                "title": "Distributed KV Engine",
                "description": "Raft-consensus replicated key-value storage engine in Go.",
                "technologies": "Go, Raft, gRPC",
                "project_url": "https://github.com/marcus/raft-kv"
            }
        ]
    })
    assert update_resp.status_code == 200
    updated_profile = update_resp.json()
    assert updated_profile["profile_completion_percentage"] >= 80
    assert len(updated_profile["work_experiences"]) == 1
    assert len(updated_profile["educations"]) == 1
    assert len(updated_profile["projects"]) == 1

    # 3. Verify Dashboard Stats
    stats_resp = client.get("/api/profiles/dashboard/stats", headers=student_headers)
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert stats["connections_count"] == 0
    assert "weekly_activity" in stats
    assert len(stats["weekly_activity"]) == 7

    # 4. Fetch AI recommendations and check compatibility scores & factual explanations
    recs_resp = client.get("/api/recommendations?limit=5", headers=student_headers)
    assert recs_resp.status_code == 200
    recs = recs_resp.json()
    assert len(recs) > 0
    top_alumnus = recs[0]["profile"]
    assert top_alumnus["user_id"] != updated_profile["user_id"]
    assert recs[0]["score"] > 0
    assert len(recs[0]["explanation"]) > 10

    # 5. Submit feedback on top recommendation
    fb_resp = client.post("/api/recommendations/feedback", headers=student_headers, json={
        "alumni_id": top_alumnus["user_id"],
        "is_relevant": True
    })
    assert fb_resp.status_code == 200
    assert fb_resp.json()["status"] == "success"

    # 6. Send connection request from student to the top alumnus
    req_resp = client.post("/api/connections/request", headers=student_headers, json={
        "receiver_id": top_alumnus["user_id"],
        "message": "Hi, I admire your work at your company and would love to connect!"
    })
    assert req_resp.status_code in [200, 201], req_resp.text
    conn_req_id = req_resp.json()["id"]

    # 7. Log in as an alumnus (David Chen or Priya Patel) and accept the request
    # Let's check top alumnus email from db
    db = SessionLocal()
    alumni_user = db.query(User).filter(User.id == top_alumnus["user_id"]).first()
    alumni_email = alumni_user.email
    db.close()

    alumni_login = client.post("/api/auth/login", json={
        "email": alumni_email,
        "password": "Password123!"
    })
    assert alumni_login.status_code == 200
    alumni_token = alumni_login.json()["access_token"]
    alumni_headers = {"Authorization": f"Bearer {alumni_token}"}

    # Verify incoming request on alumni's side
    in_resp = client.get("/api/connections/requests", headers=alumni_headers)
    assert in_resp.status_code == 200
    incoming_list = in_resp.json()["incoming"]
    assert any(r["id"] == conn_req_id for r in incoming_list)

    # Accept request
    accept_resp = client.post(f"/api/connections/requests/{conn_req_id}/accept", headers=alumni_headers)
    assert accept_resp.status_code == 200

    # 8. Verify they are now in each other's connections list
    conns_resp = client.get("/api/connections", headers=student_headers)
    assert conns_resp.status_code == 200
    assert len(conns_resp.json()) >= 1
    assert any(c["user_id"] == top_alumnus["user_id"] for c in conns_resp.json())

    # 9. Send a direct message in the conversation
    start_resp = client.post(f"/api/messages/start/{top_alumnus['user_id']}", headers=student_headers)
    assert start_resp.status_code == 200
    conv_id = start_resp.json()["conversation_id"]

    msg_resp = client.post(f"/api/messages/conversations/{conv_id}/messages", headers=student_headers, json={
        "content": "Thank you for accepting my connection request! Looking forward to learning from you."
    })
    assert msg_resp.status_code in [200, 201], msg_resp.text
    msg_data = msg_resp.json()
    assert msg_data["content"].startswith("Thank you")

    # 10. Student requests mentorship
    if top_alumnus.get("mentorship_available"):
        mentor_resp = client.post("/api/mentorship/request", headers=student_headers, json={
            "mentor_id": top_alumnus["user_id"],
            "goals_description": "Seeking monthly 1-on-1 guidance on systems engineering and preparing for technical interviews.",
            "preferred_frequency": "Monthly"
        })
        assert mentor_resp.status_code in [200, 201], mentor_resp.text

    # 11. Student applies to an open job opportunity
    jobs_resp = client.get("/api/jobs", headers=student_headers)
    jobs = jobs_resp.json()
    assert len(jobs) > 0
    first_job = jobs[0]

    apply_resp = client.post(f"/api/jobs/{first_job['id']}/apply", headers=student_headers, json={
        "cover_note": "I have extensive experience with FastAPI and React."
    })
    assert apply_resp.status_code in [201, 200]

    # 12. Admin checks telemetry & moderation
    admin_login = client.post("/api/auth/login", json={
        "email": "admin@alumnia.edu",
        "password": "Password123!"
    })
    assert admin_login.status_code == 200
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

    metrics_resp = client.get("/api/admin/metrics", headers=admin_headers)
    assert metrics_resp.status_code == 200
    metrics = metrics_resp.json()
    assert metrics["total_users"] > 0
    assert metrics["total_connections"] > 0
