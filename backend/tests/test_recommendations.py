import pytest
from app.services.recommendation_engine import RecommendationEngine
from app.models.models import Profile, ProfileSkill, WorkExperience

@pytest.fixture
def engine():
    return RecommendationEngine()

def test_skill_similarity(engine):
    student_skills = ["Python", "React", "TypeScript", "Machine Learning"]
    alumni_skills = ["Python", "Machine Learning", "PyTorch", "Docker"]
    
    score, shared = engine.compute_skill_similarity(student_skills, alumni_skills)
    assert score > 0.5 # 2 out of 4 student skills (scaled for realistic overlap)
    assert "Python" in shared
    assert "Machine Learning" in shared
    assert "Docker" not in shared

def test_career_alignment(engine):
    student_targets = ["Machine Learning Engineer", "AI Researcher"]
    alumni_title = "Senior Machine Learning Engineer"
    experiences = []
    
    score, matches = engine.compute_career_alignment(student_targets, alumni_title, experiences)
    assert score == 1.0
    assert "Machine Learning Engineer" in matches

def test_industry_alignment(engine):
    student_industries = ["Artificial Intelligence", "FinTech"]
    
    score_ai, match_ai = engine.compute_industry_alignment(student_industries, "Artificial Intelligence")
    assert score_ai == 1.0
    assert match_ai == "Artificial Intelligence"

    score_other, match_other = engine.compute_industry_alignment(student_industries, "Agriculture")
    assert score_other == 0.1

def test_academic_alignment(engine):
    score, matches = engine.compute_academic_alignment(
        "Computer Science", "B.Tech",
        "Computer Science", "B.Tech"
    )
    assert score == 1.0
    assert len(matches) == 2

def test_explanation_factual_grounding(engine):
    p = Profile(
        full_name="Elena Rostova",
        current_job_title="Senior Product Manager",
        current_company="Microsoft",
        years_of_experience=8,
        mentorship_available=True
    )
    explanation = engine.generate_explanation(
        alumnus=p,
        career_matches=["Product Manager"],
        shared_skills=["Agile"],
        industry_match="Software & Cloud",
        academic_matches=["Department of Information Systems"],
        location_match="Seattle, WA",
        mentorship_active=True
    )
    assert "Microsoft" not in explanation or "Product Manager" in explanation
    assert "Agile" in explanation
    assert "Software & Cloud" in explanation
    assert "mentor" in explanation
