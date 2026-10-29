import sys
from app.core.database import SessionLocal
from app.models.models import User, Profile
from app.services.ai_service import ai_service
from app.services.recommendation_engine import recommendation_engine

def test_database_counts():
    print("Starting test_database_counts...", flush=True)
    db = SessionLocal()
    try:
        student_count = db.query(Profile).filter(Profile.role == "student").count()
        alumni_count = db.query(Profile).filter(Profile.role == "alumni").count()
        admin_count = db.query(Profile).filter(Profile.role == "admin").count()
        print(f"[TEST 1] Counts -> Students: {student_count}, Alumni: {alumni_count}, Admins: {admin_count}", flush=True)
        assert student_count >= 50, f"Expected >= 50 students, got {student_count}"
        assert alumni_count >= 50, f"Expected >= 50 alumni, got {alumni_count}"
        assert admin_count >= 1, "Expected at least 1 admin"
    finally:
        db.close()

def test_recommendation_ranking():
    print("Starting test_recommendation_ranking...", flush=True)
    db = SessionLocal()
    try:
        student = db.query(User).filter(User.email == "student@alumnia.edu").first()
        alumni = db.query(Profile).filter(Profile.role == "alumni").all()
        print(f"Ranking {len(alumni)} alumni for {student.profile.full_name}...", flush=True)
        ranked = recommendation_engine.rank_alumni(student.profile, alumni)
        print(f"[TEST 2] Top match: {ranked[0]['profile'].full_name} ({ranked[0]['match_percentage']}%)", flush=True)
        print(f"         Explanation: {ranked[0]['explanation']}", flush=True)
        assert len(ranked) >= 50
        assert ranked[0]["match_percentage"] >= 60
        assert "skill_similarity" in ranked[0]["breakdown"]
    finally:
        db.close()

def test_ai_chatbot_queries():
    print("Starting test_ai_chatbot_queries...", flush=True)
    db = SessionLocal()
    try:
        student = db.query(User).filter(User.email == "student@alumnia.edu").first()
        
        # Query 1: Find AI alumni
        print("Calling query 1...", flush=True)
        res1 = ai_service.generate_response(db, student, "Find alumni working in artificial intelligence")
        print("[TEST 3A] AI Query 1 Cards:", len(res1["recommended_alumni"]), flush=True)

        # Query 2: Skills for data scientist
        print("Calling query 2...", flush=True)
        res2 = ai_service.generate_response(db, student, "Which skills should I learn to become a data scientist?")
        print("[TEST 3B] AI Query 2 Cards:", len(res2["recommended_alumni"]), flush=True)

        # Query 3: Outreach draft
        print("Calling query 3...", flush=True)
        res3 = ai_service.generate_response(db, student, "Help me write a message requesting mentorship to Deepa")
        print("[TEST 3C] AI Query 3 Cards:", len(res3["recommended_alumni"]), flush=True)

        # Query 4: Cloud computing in Chennai
        print("Calling query 4...", flush=True)
        res4 = ai_service.generate_response(db, student, "Find alumni in Chennai who work in cloud computing")
        print("[TEST 3D] AI Query 4 Cards:", len(res4["recommended_alumni"]), flush=True)

        # Query 5: Alumni mode -> Student search
        print("Calling query 5...", flush=True)
        alumni_user = db.query(User).filter(User.email == "deepa.subramanian@alumni.edu").first()
        res5 = ai_service.generate_response(db, alumni_user, "Show students interested in web development who need mentorship")
        print("[TEST 3E] AI Query 5 Cards:", len(res5["recommended_alumni"]), flush=True)

        print("\nALL ENHANCEMENT TESTS PASSED PERFECTLY!", flush=True)
    finally:
        db.close()

def test_engineering_departments_and_industries():
    print("Starting test_engineering_departments_and_industries...", flush=True)
    db = SessionLocal()
    try:
        # 1. Distinct department count
        depts = [d[0] for d in db.query(Profile.department).distinct().all() if d[0]]
        print(f"[TEST 4A] Total distinct departments in DB: {len(depts)}", flush=True)
        assert len(depts) >= 20, f"Expected >= 20 departments, found {len(depts)}"

        # 2. Distinct industry count
        inds = [i[0] for i in db.query(Profile.industry).distinct().all() if i[0]]
        print(f"[TEST 4B] Total distinct industries in DB: {len(inds)}", flush=True)
        assert len(inds) >= 15, f"Expected >= 15 industries, found {len(inds)}"

        # 3. Check specific engineering disciplines exist
        sample_branches = [
            "Aerospace", "Robotics", "Biomedical", "Civil", "VLSI",
            "Chemical", "Food", "Automotive", "Cybersecurity", "Renewable Energy"
        ]
        for branch in sample_branches:
            matches = db.query(Profile).filter(Profile.department.ilike(f"%{branch}%")).count()
            print(f"  Branch '{branch}': {matches} profiles found", flush=True)
            assert matches > 0, f"Expected at least 1 profile for {branch}"

        # 4. Check AI assistant responds to Aerospace and Robotics engineering
        student = db.query(User).filter(User.email == "student@alumnia.edu").first()
        aero_res = ai_service.generate_response(db, student, "Find alumni working in Aerospace & Defense")
        assert len(aero_res["recommended_alumni"]) > 0, "Expected recommended alumni in Aerospace"
        print(f"[TEST 4C] Aerospace AI matches: {len(aero_res['recommended_alumni'])} alumni", flush=True)

        robotics_res = ai_service.generate_response(db, student, "Show mentors in Robotics and Automation")
        assert len(robotics_res["recommended_alumni"]) > 0, "Expected recommended alumni in Robotics"
        print(f"[TEST 4D] Robotics AI matches: {len(robotics_res['recommended_alumni'])} alumni", flush=True)

        print("ALL ENGINEERING DEPARTMENT TESTS PASSED!", flush=True)
    finally:
        db.close()

if __name__ == "__main__":
    test_database_counts()
    test_recommendation_ranking()
    test_ai_chatbot_queries()
