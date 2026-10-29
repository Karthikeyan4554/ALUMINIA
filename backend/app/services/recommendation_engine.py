import re
import json
from typing import List, Dict, Any, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.models import Profile, RecommendationFeedback

class RecommendationEngine:
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        # Default weights as requested:
        # Skill similarity: 35%
        # Career-interest / semantic match: 20%
        # Industry match: 15%
        # Desired-role match: 15%
        # Department / academic relevance: 10%
        # Mentorship availability: 5%
        self.default_weights = {
            "skills": 0.35,
            "career_interest": 0.20,
            "industry": 0.15,
            "desired_role": 0.15,
            "academic": 0.10,
            "mentorship": 0.05
        }
        self.weights = weights or self.default_weights.copy()

    def update_weights(self, new_weights: Dict[str, float]):
        total = sum(new_weights.values())
        if total > 0:
            self.weights = {k: v / total for k, v in new_weights.items()}

    def _normalize_string(self, text: Optional[str]) -> str:
        if not text:
            return ""
        return re.sub(r'[^a-zA-Z0-9\s]', '', text.lower()).strip()

    def compute_role_alignment(self, student_targets: List[str], alumni_title: Optional[str], alumni_experiences: List[Any]) -> Tuple[float, List[str]]:
        if not student_targets:
            return 0.5, [] # Neutral baseline if student hasn't specified yet
        
        matches = []
        alumni_titles = [self._normalize_string(alumni_title)]
        for exp in alumni_experiences:
            if hasattr(exp, 'title') and exp.title:
                alumni_titles.append(self._normalize_string(exp.title))

        score = 0.0
        for target in student_targets:
            norm_target = self._normalize_string(target)
            if not norm_target:
                continue
            for a_title in alumni_titles:
                if not a_title:
                    continue
                if norm_target in a_title or a_title in norm_target:
                    score = 1.0
                    matches.append(target)
                    break
                # Partial token overlap
                target_tokens = set(norm_target.split())
                title_tokens = set(a_title.split())
                overlap = target_tokens.intersection(title_tokens)
                if overlap:
                    partial = len(overlap) / max(len(target_tokens), 1)
                    if partial > score:
                        score = partial
                        matches.append(f"{target} ({', '.join(overlap)})")

        return min(score, 1.0), list(set(matches))

    # Backward compatibility alias
    compute_career_alignment = compute_role_alignment

    def compute_skill_similarity(self, student_skills: List[str], alumni_skills: List[str]) -> Tuple[float, List[str]]:
        if not student_skills or not alumni_skills:
            return 0.0, []

        s_set = {self._normalize_string(s) for s in student_skills if s}
        a_set = {self._normalize_string(a) for a in alumni_skills if a}
        
        common = s_set.intersection(a_set)
        # Find original casing for presentation
        shared_skills_original = []
        for s in student_skills:
            if self._normalize_string(s) in common and s not in shared_skills_original:
                shared_skills_original.append(s)

        # Realistic skill overlap: sharing 3+ core tech skills indicates high alignment
        overlap_ratio = len(common) / max(len(s_set), 1)
        scaled_score = min(1.0, (len(common) / 3.0) * 0.7 + overlap_ratio * 0.3)
        return min(scaled_score, 1.0), shared_skills_original

    def compute_industry_alignment(self, student_industries: List[str], alumni_industry: Optional[str]) -> Tuple[float, Optional[str]]:
        if not student_industries:
            return 0.5, None # Neutral
        if not alumni_industry:
            return 0.2, None
            
        norm_a_ind = self._normalize_string(alumni_industry)
        for ind in student_industries:
            norm_s_ind = self._normalize_string(ind)
            if norm_s_ind == norm_a_ind or norm_s_ind in norm_a_ind or norm_a_ind in norm_s_ind:
                return 1.0, alumni_industry
            # Token match
            s_tokens = set(norm_s_ind.split())
            a_tokens = set(norm_a_ind.split())
            if s_tokens.intersection(a_tokens):
                return 0.75, alumni_industry

        return 0.1, None

    def compute_academic_alignment(self, s_dept: Optional[str], s_degree: Optional[str], a_dept: Optional[str], a_degree: Optional[str]) -> Tuple[float, List[str]]:
        score = 0.0
        matches = []
        if s_dept and a_dept:
            ns_dept = self._normalize_string(s_dept)
            na_dept = self._normalize_string(a_dept)
            if ns_dept == na_dept or ns_dept in na_dept or na_dept in ns_dept:
                score += 0.7
                matches.append(f"Department of {a_dept}")
            elif set(ns_dept.split()).intersection(set(na_dept.split())):
                score += 0.4
                matches.append(f"Related field ({a_dept})")
        if s_degree and a_degree:
            ns_deg = self._normalize_string(s_degree)
            na_deg = self._normalize_string(a_degree)
            if ns_deg == na_deg or ns_deg in na_deg:
                score += 0.3
                matches.append(f"Degree ({a_degree})")
        return min(score, 1.0), matches

    def compute_location_match(self, s_locations: List[str], a_location: Optional[str]) -> Tuple[float, Optional[str]]:
        if not s_locations:
            return 0.5, None
        if not a_location:
            return 0.2, None
        na_loc = self._normalize_string(a_location)
        for loc in s_locations:
            ns_loc = self._normalize_string(loc)
            if ns_loc in na_loc or na_loc in ns_loc:
                return 1.0, a_location
        return 0.2, None

    def compute_semantic_similarity(self, student_corpus: str, alumni_corpus_list: List[str]) -> List[float]:
        all_docs = [student_corpus] + alumni_corpus_list
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
            tfidf_matrix = vectorizer.fit_transform(all_docs)
            student_vector = tfidf_matrix[0:1]
            alumni_vectors = tfidf_matrix[1:]
            sims = cosine_similarity(student_vector, alumni_vectors)[0]
            # Scale raw TF-IDF cosine (which rarely exceeds 0.5 across disparate texts) to [0, 1] range
            return [float(max(0.2, min(1.0, s * 1.8))) for s in sims]
        except Exception:
            return [0.5 for _ in alumni_corpus_list]

    def generate_explanation(
        self,
        alumnus: Profile,
        role_matches: Optional[List[str]] = None,
        shared_skills: Optional[List[str]] = None,
        industry_match: Optional[str] = None,
        academic_matches: Optional[List[str]] = None,
        location_match: Optional[str] = None,
        mentorship_active: bool = False,
        career_matches: Optional[List[str]] = None
    ) -> str:
        role_matches = role_matches or career_matches or []
        shared_skills = shared_skills or []
        academic_matches = academic_matches or []
        points = []
        if role_matches:
            points.append(f"their current role relates directly to your target role in {role_matches[0]}")
        if shared_skills:
            points.append(f"you share technical proficiency in {', '.join(shared_skills[:3])}")
        if industry_match:
            points.append(f"they have active experience within the {industry_match} sector")
        if academic_matches:
            points.append(f"shared academic roots in the {academic_matches[0]}")
        if mentorship_active:
            points.append("they are an active mentor open to guiding students")
        if location_match:
            points.append(f"based in your preferred location ({location_match})")

        if not points:
            points.append(f"graduated from your university and has built {alumnus.years_of_experience} years of industry experience at {alumnus.current_company or 'leading organizations'}")

        explanation = f"Recommended because {', '.join(points[:-1]) + (' and ' + points[-1] if len(points) > 1 else points[0])}."
        return explanation

    def generate_conversation_starter(
        self,
        alumnus: Profile,
        role_matches: List[str],
        shared_skills: List[str],
        industry_match: Optional[str]
    ) -> str:
        first_name = alumnus.full_name.split()[0] if alumnus.full_name else "there"
        
        if role_matches and alumnus.current_company:
            return (
                f"Hi {first_name}, I am an undergraduate exploring career paths in {role_matches[0]}. "
                f"I noticed your role as {alumnus.current_job_title or 'an engineer'} at {alumnus.current_company} "
                f"and would love to connect to learn more about your career journey!"
            )
        elif shared_skills:
            return (
                f"Hi {first_name}, I came across your profile and noticed our shared background in {', '.join(shared_skills[:2])}. "
                f"I would be grateful to hear your advice on transitioning from college to working at {alumnus.current_company or 'industry leading firms'}."
            )
        elif industry_match:
            return (
                f"Hi {first_name}, I'm aspiring to enter the {industry_match} sector after graduation. "
                f"Given your inspiring path at {alumnus.current_company or 'your organization'}, could I connect to follow your professional updates?"
            )
        else:
            return (
                f"Hi {first_name}, as a fellow student from the university, I would love to connect and follow your journey at {alumnus.current_company or 'in the industry'}!"
            )

    def rank_alumni(
        self,
        student: Profile,
        alumni_list: List[Profile],
        feedback_dict: Optional[Dict[str, bool]] = None
    ) -> List[Dict[str, Any]]:
        if not alumni_list:
            return []

        # Prepare rich corpus for TF-IDF incorporating student projects
        project_text = " ".join([f"{p.title} {p.description or ''} {p.technologies or ''}" for p in student.projects])
        student_corpus = f"{student.headline or ''} {student.bio or ''} {' '.join(student.skills_list)} {' '.join(student.target_roles)} {student.mentorship_goals or ''} {project_text}"
        
        alumni_corpora = []
        for a in alumni_list:
            exp_text = " ".join([f"{e.title} {e.company} {e.description or ''}" for e in a.work_experiences])
            corpus = f"{a.current_job_title or ''} {a.current_company or ''} {a.industry or ''} {a.headline or ''} {a.bio or ''} {' '.join(a.skills_list)} {' '.join(a.mentorship_topics)} {exp_text}"
            alumni_corpora.append(corpus)

        semantic_scores = self.compute_semantic_similarity(student_corpus, alumni_corpora)

        results = []
        feedback_dict = feedback_dict or {}

        # Resolve weights dynamically
        w_skills = self.weights.get("skills", 0.35)
        w_career = self.weights.get("career_interest", self.weights.get("career", 0.20))
        w_industry = self.weights.get("industry", 0.15)
        w_role = self.weights.get("desired_role", 0.15)
        w_academic = self.weights.get("academic", 0.10)
        w_mentor = self.weights.get("mentorship", 0.05)

        for idx, a in enumerate(alumni_list):
            role_score, role_matches = self.compute_role_alignment(
                student.target_roles, a.current_job_title, a.work_experiences
            )
            skill_score, shared_skills = self.compute_skill_similarity(
                student.skills_list, a.skills_list
            )
            industry_score, industry_match = self.compute_industry_alignment(
                student.preferred_industries, a.industry
            )
            academic_score, academic_matches = self.compute_academic_alignment(
                student.department, student.degree, a.department, a.degree
            )
            location_score, location_match = self.compute_location_match(
                student.preferred_locations, a.location
            )
            semantic_score = semantic_scores[idx]
            
            mentorship_score = 1.0 if a.mentorship_available else 0.2

            # Weighted sum according to configured academic priorities
            weighted_sum = (
                w_skills * skill_score +
                w_career * semantic_score +
                w_industry * industry_score +
                w_role * role_score +
                w_academic * academic_score +
                w_mentor * mentorship_score
            )

            # Incorporate feedback loop if available (+5% for confirmed relevant, -15% if flagged)
            if a.user_id in feedback_dict:
                if feedback_dict[a.user_id] is True:
                    weighted_sum = min(1.0, weighted_sum + 0.05)
                elif feedback_dict[a.user_id] is False:
                    weighted_sum = max(0.1, weighted_sum - 0.15)

            final_score = round(weighted_sum * 100, 1)
            final_percentage = int(round(final_score))

            explanation = self.generate_explanation(
                a, role_matches, shared_skills, industry_match, academic_matches, location_match, a.mentorship_available
            )
            starter = self.generate_conversation_starter(
                a, role_matches, shared_skills, industry_match
            )

            mutual_attributes = []
            if shared_skills:
                mutual_attributes.append(f"{len(shared_skills)} Shared Skills")
            if role_matches:
                mutual_attributes.append("Target Role Match")
            if industry_match:
                mutual_attributes.append(f"Industry: {industry_match}")
            if academic_matches:
                mutual_attributes.append("Alma Mater Department")
            if a.mentorship_available:
                mutual_attributes.append("Active Mentor")

            breakdown = {
                "skill_similarity": round(skill_score * 100, 1),
                "career_alignment": round(role_score * 100, 1),
                "desired_role": round(role_score * 100, 1),
                "industry_alignment": round(industry_score * 100, 1),
                "semantic_similarity": round(semantic_score * 100, 1),
                "academic_alignment": round(academic_score * 100, 1),
                "location_match": round(location_score * 100, 1),
                "mentorship_bonus": round(mentorship_score * 100, 1)
            }

            results.append({
                "profile": a,
                "score": final_score,
                "match_percentage": final_percentage,
                "breakdown": breakdown,
                "explanation": explanation,
                "conversation_starter": starter,
                "shared_skills": shared_skills,
                "mutual_attributes": mutual_attributes
            })

        # Sort by final score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

recommendation_engine = RecommendationEngine()
