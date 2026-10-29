import os
import re
import json
import httpx
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from app.core.config import settings
from app.models.models import Profile, ProfileSkill, WorkExperience, Project, User
from app.services.recommendation_engine import recommendation_engine

class AIService:
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.gemini_key = settings.GEMINI_API_KEY
        self.model = settings.LLM_MODEL or "gpt-4o-mini"

        # Domain synonym dictionary for robust query expansion
        self.synonyms = {
            "ai": ["Artificial Intelligence", "Machine Learning", "Deep Learning", "Generative AI"],
            "artificial intelligence": ["Artificial Intelligence", "Machine Learning", "Deep Learning", "Generative AI"],
            "ml": ["Machine Learning", "Deep Learning", "Data Science", "Python"],
            "machine learning": ["Machine Learning", "Deep Learning", "Python", "PyTorch", "TensorFlow"],
            "genai": ["Generative AI", "RAG", "LangChain", "Prompt Engineering", "NLP"],
            "generative ai": ["Generative AI", "RAG", "LangChain", "Prompt Engineering", "NLP"],
            "nlp": ["NLP", "Natural Language Processing", "LangChain", "Generative AI", "Python"],
            "cv": ["Computer Vision", "OpenCV", "Deep Learning", "PyTorch"],
            "computer vision": ["Computer Vision", "OpenCV", "Deep Learning", "PyTorch"],
            "cloud": ["Cloud Architecture", "AWS", "Google Cloud", "Kubernetes", "Docker", "Terraform", "DevOps"],
            "cloud computing": ["Cloud Architecture", "AWS", "Google Cloud", "Kubernetes", "Docker", "Terraform", "DevOps"],
            "devops": ["DevOps", "CI/CD", "Docker", "Kubernetes", "Linux", "Terraform", "AWS"],
            "sre": ["Site Reliability Engineering", "Kubernetes", "Linux", "Docker", "Cloud Architecture"],
            "cybersecurity": ["Cybersecurity", "Network Security", "Cloud Security", "Ethical Security Testing"],
            "security": ["Cybersecurity", "Network Security", "Cloud Security", "Ethical Security Testing"],
            "embedded": ["Embedded Systems", "IoT", "RTOS", "C++", "PCB Design", "ARM Cortex", "TinyML"],
            "embedded systems": ["Embedded Systems", "IoT", "RTOS", "C++", "PCB Design", "ARM Cortex"],
            "iot": ["IoT", "Embedded Systems", "C++", "Python", "MQTT"],
            "robotics": ["Robotics", "ROS", "Control Systems", "Embedded Systems", "Computer Vision", "C++"],
            "vlsi": ["VLSI", "Verilog", "SystemVerilog", "FPGA", "Digital Electronics", "Semiconductors"],
            "semiconductor": ["Semiconductors", "VLSI", "Verilog", "FPGA", "Hardware Tech"],
            "data science": ["Data Science", "Machine Learning", "Python", "SQL", "Data Analytics", "Pandas"],
            "data scientist": ["Data Science", "Machine Learning", "Python", "SQL", "Pandas", "Scikit-learn"],
            "data analytics": ["Data Analytics", "SQL", "Power BI", "Tableau", "Python"],
            "fullstack": ["Full Stack Developer", "React", "TypeScript", "Node.js", "FastAPI", "PostgreSQL"],
            "full stack": ["Full Stack Developer", "React", "TypeScript", "Node.js", "FastAPI", "PostgreSQL"],
            "web development": ["React", "TypeScript", "JavaScript", "Node.js", "HTML/CSS", "Next.js"],
            "frontend": ["React", "TypeScript", "JavaScript", "HTML/CSS", "Tailwind CSS", "UI/UX Design"],
            "backend": ["Java", "Spring Boot", "Go", "PostgreSQL", "Node.js", "FastAPI", "REST APIs", "System Design"],
            "product": ["Product Management", "UI/UX Design", "Agile", "Business Analysis", "Leadership"],
            "product management": ["Product Management", "UI/UX Design", "Agile", "Business Analysis", "Leadership"],
            "ev": ["Automotive & EV", "Automotive Systems", "SolidWorks", "Battery Management", "Embedded Systems"],
            "electric vehicle": ["Automotive & EV", "Automotive Systems", "SolidWorks", "Battery Management", "Embedded Systems"],
            "biotech": ["Biotechnology", "Bioinformatics", "Bioprocess Engineering", "Microbiology"],
            "civil": ["Civil Engineering", "Structural Analysis", "AutoCAD", "ETABS", "BIM", "Environmental Engineering"],
            "aerospace": ["Aerospace & Defense", "Aerodynamics", "Avionics", "Flight Controls", "ANSYS Fluent"],
            "aeronautical": ["Aerospace & Defense", "Aerodynamics", "Avionics", "Flight Controls"],
            "avionics": ["Avionics", "Flight Controls", "Embedded Systems", "Aerodynamics"],
            "biomedical": ["Biomedical Engineering", "Medical Devices & MedTech", "Biomedical Signal Processing", "Bio-Sensors"],
            "medtech": ["Medical Devices & MedTech", "Biomedical Signal Processing", "Healthcare & MedTech"],
            "structural": ["Civil & Structural Engineering", "Structural Dynamics", "STAAD Pro", "ETABS", "Revit BIM"],
            "chemical": ["Chemical & Process Engineering", "Process Simulation", "Aspen Plus", "Process Safety"],
            "food tech": ["Agritech & Food Processing", "Food Preservation", "HACCP", "Quality Control"],
            "food technology": ["Agritech & Food Processing", "Food Preservation", "HACCP", "Quality Control"],
            "textile": ["Smart Textiles & Apparel Manufacturing", "Technical Textiles", "Polymer Chemistry"],
            "marine": ["Marine & Ocean Technology", "Hydrodynamics", "Ship Stability", "ANSYS Aqwa"],
            "materials": ["Advanced Materials & Metallurgy", "Material Characterization", "Heat Treatment", "SEM Analysis"],
            "metallurgy": ["Advanced Materials & Metallurgy", "Material Characterization", "Heat Treatment", "Phase Diagrams"],
            "solar": ["Clean Energy & Power Systems", "Solar PV Design", "PVsyst", "Renewable Energy"],
            "clean energy": ["Clean Energy & Power Systems", "Solar PV Design", "Renewable Energy", "Smart Inverters"],
            "smart grid": ["Clean Energy & Power Systems", "Smart Inverters", "SCADA", "Power Systems"]
        }

        # Location synonym mapping
        self.locations = {
            "chennai": "Chennai",
            "coimbatore": "Coimbatore",
            "madurai": "Madurai",
            "bengaluru": "Bengaluru",
            "bangalore": "Bengaluru",
            "salem": "Salem",
            "erode": "Erode",
            "tiruppur": "Tiruppur",
            "vellore": "Vellore",
            "thanjavur": "Thanjavur",
            "tirunelveli": "Tirunelveli",
            "hosur": "Hosur",
            "dindigul": "Dindigul"
        }

    def _extract_intent_and_entities(self, message: str, user_role: str) -> Dict[str, Any]:
        msg_lower = message.lower().strip()
        entities = {
            "skills": set(),
            "location": None,
            "roles": set(),
            "target_alumnus_name": None,
            "mentorship_only": False
        }

        # Check for mentorship intent
        if "mentor" in msg_lower or "guide" in msg_lower or "guidance" in msg_lower or "advice" in msg_lower:
            entities["mentorship_only"] = True

        # Check locations
        for loc_key, loc_name in self.locations.items():
            if re.search(r'\b' + re.escape(loc_key) + r'\b', msg_lower):
                entities["location"] = loc_name
                break

        # Check synonyms / skills
        for term, expansions in self.synonyms.items():
            pattern = r'\b' + re.escape(term) + r'\b'
            if re.search(pattern, msg_lower):
                for exp in expansions:
                    entities["skills"].add(exp)

        # Check explicit single skill tokens
        for token in ["python", "java", "c++", "react", "node.js", "sql", "aws", "docker", "kubernetes", "pytorch", "tensorflow", "figma", "go", "linux"]:
            if token in msg_lower:
                entities["skills"].add(token.capitalize() if token != "sql" and token != "aws" else token.upper())

        # Check if user mentioned a specific name
        known_names = [
            "deepa", "deepa subramanian", "vignesh", "vignesh balasubramanian", "ananya", "ananya jayaram",
            "aravind", "selvi", "sivakumar", "soundarya", "senthil", "nithya", "kavin", "arun", "arun prakash",
            "priya", "priya balaji", "suresh", "divya", "ashwin", "ramya", "balaji", "swetha"
        ]
        for name in known_names:
            if name in msg_lower:
                entities["target_alumnus_name"] = name
                break

        # Classify intent
        intent = "general_search"
        if user_role == "alumni" and ("student" in msg_lower or "mentee" in msg_lower or "need mentorship" in msg_lower):
            intent = "student_search"
        elif "skill" in msg_lower and ("learn" in msg_lower or "become" in msg_lower or "prepare" in msg_lower or "gap" in msg_lower or "require" in msg_lower):
            intent = "skill_guidance"
        elif "draft" in msg_lower or "message" in msg_lower or "outreach" in msg_lower or "request" in msg_lower or "write" in msg_lower:
            intent = "outreach_draft"
        elif "interview" in msg_lower or "question" in msg_lower:
            intent = "interview_prep"
        elif "project" in msg_lower or "recommend three" in msg_lower or "recommend" in msg_lower:
            intent = "project_recommendation"
        elif "why" in msg_lower and "recommend" in msg_lower:
            intent = "why_recommended"
        elif entities["mentorship_only"]:
            intent = "mentorship_search"

        return {
            "intent": intent,
            "entities": entities
        }

    def generate_response(
        self,
        db: Session,
        current_user: User,
        user_message: str,
        task: str = "general",
        target_alumni: Optional[Profile] = None,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Database-grounded AI Networking Assistant.
        Executes verified queries across students and alumni, applying RBAC and transparent matching.
        """
        user_profile = current_user.profile
        if not user_profile:
            return {
                "response": "Please complete your profile to enable personalized alumni guidance.",
                "suggested_actions": ["Complete Profile"],
                "recommended_alumni": [],
                "is_llm_generated": False
            }

        extracted = self._extract_intent_and_entities(user_message, current_user.role)
        intent = extracted["intent"]
        entities = extracted["entities"]

        # -------------------------------------------------------------
        # INTENT 1: OUTREACH DRAFT GENERATION
        # -------------------------------------------------------------
        if intent == "outreach_draft" or task == "connection_draft":
            target = target_alumni
            if not target and entities["target_alumnus_name"]:
                target = db.query(Profile).options(joinedload(Profile.skills)).filter(
                    Profile.role == "alumni",
                    Profile.full_name.ilike(f"%{entities['target_alumnus_name']}%")
                ).first()

            if not target:
                # Pick top matching active mentor
                target = db.query(Profile).options(joinedload(Profile.skills)).filter(
                    Profile.role == "alumni",
                    Profile.mentorship_available == True
                ).first()

            target_name = target.full_name if target else "Alumnus"
            first_name = target_name.split()[0]
            target_role = target.current_job_title if target else "Engineer"
            target_company = target.current_company if target else "Leading Tech Company"

            shared = [s for s in (user_profile.skills_list or []) if target and s in (target.skills_list or [])]
            skill_mention = f" and your deep expertise in {shared[0]}" if shared else ""

            draft = (
                f"**Subject:** Connecting with a fellow student from Bannari Amman Institute of Technology\n\n"
                f"Dear {first_name},\n\n"
                f"I hope this note finds you well! I am an undergraduate in {user_profile.department or 'the Department of AI & DS'} "
                f"(Class of {user_profile.graduation_year or '2026'}).\n\n"
                f"I came across your inspiring work as {target_role} at {target_company}{skill_mention}. As someone actively preparing "
                f"for a career in {target_role}, I would be deeply grateful to connect with you on Alumnia to follow your journey.\n\n"
                f"If you ever have 15 minutes in the coming weeks for a brief chat or advice on navigating the transition from college "
                f"into industry, I would truly appreciate your insights.\n\n"
                f"Thank you for your time and continued support of our alma mater!\n\n"
                f"Warm regards,\n"
                f"{user_profile.full_name}\n"
                f"{user_profile.college_email or ''}"
            )

            rec_cards = [{
                "id": target.id,
                "user_id": target.user_id,
                "name": target.full_name,
                "title": target.current_job_title,
                "company": target.current_company,
                "department": target.department,
                "location": target.location,
                "mentorship": target.mentorship_available,
                "skills": target.skills_list[:3]
            }] if target else []

            return {
                "response": f"Here is a personalized, professional outreach draft for **{target_name}** grounded in your shared academic background:\n\n{draft}\n\n*Tip: Personalized notes referencing specific mutual skills increase alumni response rates significantly.*",
                "suggested_actions": ["Copy Outreach Message", "Request 1:1 Mentorship", "Explore Other Mentors"],
                "recommended_alumni": rec_cards,
                "is_llm_generated": False
            }

        # -------------------------------------------------------------
        # INTENT 2: SKILL GUIDANCE & CAREER GAP ANALYSIS
        # -------------------------------------------------------------
        if intent == "skill_guidance":
            # Identify target role from message or student profile
            target_role = "Data Scientist"
            for role_candidate in ["data scientist", "machine learning engineer", "cloud engineer", "devops engineer", "full stack developer", "software engineer", "cybersecurity analyst", "product manager", "embedded systems engineer"]:
                if role_candidate in user_message.lower():
                    target_role = role_candidate.title()
                    break
            else:
                if user_profile.target_roles:
                    target_role = user_profile.target_roles[0]

            # Query real alumni in database holding this or related role
            alumni_with_role = db.query(Profile).options(joinedload(Profile.skills)).filter(
                Profile.role == "alumni",
                or_(
                    Profile.current_job_title.ilike(f"%{target_role}%"),
                    Profile.headline.ilike(f"%{target_role}%")
                )
            ).all()

            if not alumni_with_role:
                alumni_with_role = db.query(Profile).options(joinedload(Profile.skills)).filter(Profile.role == "alumni").limit(8).all()

            # Aggregate actual skills held by these alumni
            skill_counts = {}
            for a in alumni_with_role:
                for sk in a.skills_list:
                    skill_counts[sk] = skill_counts.get(sk, 0) + 1

            sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
            top_industry_skills = [sk for sk, count in sorted_skills[:7]]

            student_skills = set(user_profile.skills_list)
            already_have = [sk for sk in top_industry_skills if sk in student_skills]
            to_learn = [sk for sk in top_industry_skills if sk not in student_skills]

            response_lines = [
                f"### Skill Roadmap & Gap Analysis for **{target_role}**",
                f"Based on real career profiles of **{len(alumni_with_role)} alumni** currently working in this role:\n",
                f"✅ **Skills You Already Possess:** {', '.join(already_have) if already_have else 'None explicitly listed yet'}",
                f"🎯 **High-Priority Skills to Learn Next:** {', '.join(to_learn) if to_learn else 'You already have strong coverage of the primary skills!'}\n",
                f"**Alumni Practitioners in {target_role}:**"
            ]

            cards = []
            for a in alumni_with_role[:4]:
                response_lines.append(f"- **{a.full_name}** ({a.current_job_title} at **{a.current_company}**) • Class of {a.graduation_year} • {', '.join(a.skills_list[:3])}")
                cards.append({
                    "id": a.id,
                    "user_id": a.user_id,
                    "name": a.full_name,
                    "title": a.current_job_title,
                    "company": a.current_company,
                    "department": a.department,
                    "location": a.location,
                    "mentorship": a.mentorship_available,
                    "skills": a.skills_list[:3]
                })

            response_lines.append("\n**Suggested Next Step:** Connect with these alumni to inquire about the exact project challenges they tackle daily.")

            return {
                "response": "\n".join(response_lines),
                "suggested_actions": ["Explore Mentors in this Role", "Update My Profile Skills", "Draft Outreach Note"],
                "recommended_alumni": cards,
                "is_llm_generated": False
            }

        # -------------------------------------------------------------
        # INTENT 3: ALUMNI ASSISTANCE (STUDENT SEARCH FOR MENTORING)
        # -------------------------------------------------------------
        if intent == "student_search" or current_user.role == "alumni":
            query = db.query(Profile).options(joinedload(Profile.skills)).filter(Profile.role == "student", Profile.is_public == True)

            if entities["skills"]:
                matched_students = []
                for p in query.all():
                    p_text = f"{' '.join(p.skills_list)} {' '.join(p.target_roles)} {p.bio or ''}".lower()
                    if any(s.lower() in p_text for s in entities["skills"]):
                        matched_students.append(p)
                candidates = matched_students
            else:
                candidates = query.limit(6).all()

            if not candidates:
                return {
                    "response": "No student profiles currently match those specific criteria. You can browse the complete student directory or update your mentoring availability in Settings.",
                    "suggested_actions": ["View Student Directory", "Update Mentorship Slots"],
                    "recommended_alumni": [],
                    "is_llm_generated": False
                }

            response_lines = [
                f"Found **{len(candidates)} aspiring student{'s' if len(candidates) != 1 else ''}** looking for mentorship and industry guidance:\n"
            ]
            student_cards = []
            for s in candidates[:4]:
                response_lines.append(f"- **{s.full_name}** • {s.department} (Class of {s.graduation_year}) • Target: {', '.join(s.target_roles[:2])} • Skills: {', '.join(s.skills_list[:3])}")
                student_cards.append({
                    "id": s.id,
                    "user_id": s.user_id,
                    "name": s.full_name,
                    "title": f"Student ({s.department})",
                    "company": f"Class of {s.graduation_year}",
                    "department": s.department,
                    "location": s.location,
                    "mentorship": False,
                    "skills": s.skills_list[:3]
                })

            return {
                "response": "\n".join(response_lines),
                "suggested_actions": ["Review Student Profiles", "Accept Pending Requests"],
                "recommended_alumni": student_cards,
                "is_llm_generated": False
            }

        # -------------------------------------------------------------
        # INTENT 4: PROJECT-BASED ALUMNI RECOMMENDATION
        # -------------------------------------------------------------
        if intent == "project_recommendation":
            # Query all eligible alumni
            all_alumni = db.query(Profile).options(
                joinedload(Profile.skills),
                joinedload(Profile.projects),
                joinedload(Profile.work_experiences)
            ).filter(
                Profile.role == "alumni",
                Profile.is_public == True,
                Profile.user_id != current_user.id
            ).all()

            ranked = recommendation_engine.rank_alumni(user_profile, all_alumni)
            top_matches = ranked[:3]

            response_lines = [
                f"### Top 3 Verified Alumni Matches for Your Career & Project Path:\n"
            ]
            cards = []
            for item in top_matches:
                a = item["profile"]
                pct = item["match_percentage"]
                expl = item["explanation"]
                response_lines.append(f"- **{a.full_name}** — {a.current_job_title} at **{a.current_company}** (**{pct}% Compatibility**)\n  *{expl}*")
                cards.append({
                    "id": a.id,
                    "user_id": a.user_id,
                    "name": a.full_name,
                    "title": a.current_job_title,
                    "company": a.current_company,
                    "department": a.department,
                    "location": a.location,
                    "mentorship": a.mentorship_available,
                    "skills": a.skills_list[:3]
                })

            response_lines.append("\n**Action Plan:** Review their profiles above and reach out with the auto-generated ice-breaker message!")

            return {
                "response": "\n".join(response_lines),
                "suggested_actions": ["Draft Outreach for Top Match", "Explore All Recommendations", "View 7-Factor Breakdown"],
                "recommended_alumni": cards,
                "is_llm_generated": False
            }

        # -------------------------------------------------------------
        # INTENT 5: GENERAL ALUMNI & MENTOR SEARCH
        # -------------------------------------------------------------
        query = db.query(Profile).options(
            joinedload(Profile.skills),
            joinedload(Profile.projects),
            joinedload(Profile.work_experiences)
        ).filter(
            Profile.role == "alumni",
            Profile.is_public == True,
            Profile.user_id != current_user.id
        )

        if entities["location"]:
            query = query.filter(Profile.location.ilike(f"%{entities['location']}%"))

        if entities["mentorship_only"]:
            query = query.filter(Profile.mentorship_available == True)

        candidates = query.all()

        # Filter by skills or role keywords if extracted
        if entities["skills"]:
            filtered = []
            for a in candidates:
                a_text = f"{a.current_job_title} {a.industry} {a.bio or ''} {' '.join(a.skills_list)}".lower()
                if any(s.lower() in a_text for s in entities["skills"]):
                    filtered.append(a)
            if filtered:
                candidates = filtered

        if not candidates:
            # Honest message when no direct match exists
            return {
                "response": (
                    f"I searched our alumni database, but could not find an exact match for your specific criteria "
                    f"({', '.join(entities['skills']) if entities['skills'] else 'current query'} in {entities['location'] or 'all locations'}).\n\n"
                    f"💡 **Suggested Alternatives:**\n"
                    f"1. Try searching related domains like **Artificial Intelligence**, **Cloud & DevOps**, or **FinTech**.\n"
                    f"2. Broaden your location filter across all Tamil Nadu hubs (Chennai, Coimbatore, Bengaluru).\n"
                    f"3. Visit the **Alumni Directory** tab to search by graduation year or company name."
                ),
                "suggested_actions": ["Explore All AI Alumni", "View Cloud Mentors in Chennai", "Open Alumni Directory"],
                "recommended_alumni": [],
                "is_llm_generated": False
            }

        # Format retrieved candidates
        count = len(candidates)
        desc_parts = []
        if entities["skills"]:
            desc_parts.append(f"specializing in **{', '.join(list(entities['skills'])[:3])}**")
        if entities["location"]:
            desc_parts.append(f"located in **{entities['location']}**")
        if entities["mentorship_only"]:
            desc_parts.append("open for **active 1:1 mentorship**")

        summary_desc = " " + " and ".join(desc_parts) if desc_parts else " matching your request"

        response_lines = [
            f"Here are verified alumni{summary_desc} retrieved from the database:\n"
        ]

        cards = []
        for a in candidates[:4]:
            mentor_tag = " [✨ Active Mentor]" if a.mentorship_available else ""
            response_lines.append(f"- **{a.full_name}** — {a.current_job_title} at **{a.current_company}** (Class of {a.graduation_year}){mentor_tag}\n  *Key skills: {', '.join(a.skills_list[:4])}*")
            cards.append({
                "id": a.id,
                "user_id": a.user_id,
                "name": a.full_name,
                "title": a.current_job_title,
                "company": a.current_company,
                "department": a.department,
                "location": a.location,
                "mentorship": a.mentorship_available,
                "skills": a.skills_list[:3]
            })

        response_lines.append("\n**Suggested Next Step:** Click on any profile card to view their complete background or send a personalized connection request.")

        return {
            "response": "\n".join(response_lines),
            "suggested_actions": ["Draft Outreach Message", "Request Mentorship Session", "Explore All Recommendations"],
            "recommended_alumni": cards,
            "is_llm_generated": False
        }

ai_service = AIService()
