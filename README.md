# ALUMNIA — Connect Beyond Graduation
### Generative AI Based Alumni Networking Platform with Personalized Connection Recommendations
> **Department of Artificial Intelligence and Data Science**  
> **Bannari Amman Institute of Technology, Sathyamangalam, Tamil Nadu**  
> **Final-Year Project by Karthikeyan V (7376242AD200) & Kavineayan R (7376242AD201)**  
> **Project Guide & HOD: Dr. Gomathi R**

---

## 1. Executive Summary

**Alumnia** is a modern, production-grade web platform engineered to bridge the gap between higher education students and graduates. Engineered specifically for academic and institutional deployment at **Bannari Amman Institute of Technology**, Alumnia leverages a transparent 6-factor academic recommendation model, TF-IDF vector space cosine similarity with project grounding, and a dual-mode AI Networking Assistant.

Alumnia matches students with relevant alumni based on target career paths, overlapping competencies, industry verticals, academic departments, and active mentorship availability. Every match provides:
1. **Explainable Compatibility Score Breakdown** (Skill 35%, Career Interest 20%, Industry 15%, Desired Role 15%, Academic 10%, Mentorship 5%).
2. **Context-Grounded Natural Language Justification** referencing mutual skills and project topics.
3. **Personalized Icebreaker Conversation Starter** ready for 1-click outreach.

---

## 2. System Architecture

```
                                  +---------------------------------------+
                                  |         Client: React 18 + TS         |
                                  | Vite • Tailwind CSS • Recharts • Zod  |
                                  +---------------------------------------+
                                                      |
                                                      |  REST API + JWT Bearer
                                                      v
                                  +---------------------------------------+
                                  |         Backend: Python FastAPI       |
                                  +---------------------------------------+
                                  |  - Authentication & RBAC Guards       |
                                  |  - 6-Factor Academic Rec Engine       |
                                  |  - Grounded AI Networking Assistant   |
                                  |  - Mentorship, Jobs, Events, Chat     |
                                  +---------------------------------------+
                                          |                         |
                +-------------------------+                         +--------------------------+
                |                                                                              |
                v                                                                              v
+-------------------------------+                                              +-------------------------------+
|     Data Persistence Layer    |                                              |     Applied AI Components     |
+-------------------------------+                                              +-------------------------------+
| - SQLite Local Zero-Config    |                                              | - TF-IDF Vector Space Model   |
| - PostgreSQL / Supabase Ready |                                              | - Cosine Vector Similarity    |
| - 103 Pre-seeded TN Profiles  |                                              | - Project & Experience Corpus |
| - Normalized Relational DDL   |                                              | - Grounded Explanation Engine |
+-------------------------------+                                              +-------------------------------+
```

---

## 3. The 6-Factor Academic Recommendation Algorithm

Alumnia implements a mathematically rigorous, transparent academic recommendation formula. For a student $S$ and an alumnus candidate $A$, the compatibility score $C(S, A) \in [0, 100]$ is computed as:

$$C(S, A) = 100 \times \sum_{i=1}^{6} w_i \cdot s_i(S, A)$$

### Configurable Weights & Evaluation Criteria:
| Factor | Weight ($w_i$) | Academic Matching Methodology |
|---|---|---|
| **Skill Overlap Similarity** | **35%** | Scaled Jaccard overlap on verified technical skills ($\min(1.0, \frac{|Skills_S \cap Skills_A|}{3} \times 0.7 + J \times 0.3)$) |
| **Career Interest & Project Cosine** | **20%** | TF-IDF vector space model over student projects, career goals, and alumnus background |
| **Industry Alignment** | **15%** | Exact or sub-token sector match across student preferred industries |
| **Desired Role Alignment** | **15%** | Token similarity between student target roles and alumnus current title/experience |
| **Academic Department & Degree** | **10%** | Departmental alignment (BIT AI & DS, CSE, IT, ECE, EEE, Mech, Biotech, Civil) |
| **Mentorship Bonus** | **5%** | Full bonus awarded if the alumnus is an active mentor open to guiding students |

> **Interactive Multi-Filter**: The recommendations page allows real-time multi-attribute filtering by **Industry**, **Skill**, **Job Role**, **Location**, **Graduation Year**, and **Mentorship Only**.

---

## 4. Grounded AI Networking Assistant

The platform features an intelligent conversational assistant tailored for higher education networking:

### Dual Operation Modes:
1. **Student Mode**:
   - Discovers alumni by technical domain (*"Find alumni working in artificial intelligence"*).
   - Generates skill roadmaps and gap analyses (*"Which skills should I learn to become a data scientist?"*).
   - Recommends mentors for capstone projects (*"Recommend three alumni for my Generative AI project"*).
   - Drafts polite, personalized outreach notes referencing mutual skills and college background.
2. **Alumni Mode**:
   - Searches for mentees (*"Show students interested in web development who need mentorship"*).
   - Analyzes student skill trends and project areas.

### Domain Synonyms & Semantic Expansion:
Supports deep keyword mapping across AI, Machine Learning, Generative AI, Cloud Architecture, DevOps, Cybersecurity, Embedded Systems, Robotics, VLSI, Full Stack, Data Science, Automotive/EV, Biotechnology, and Civil Engineering.

---

## 5. Verified Demonstration Accounts

The platform contains **142 pre-seeded profiles** (70 Students, 71 Alumni, 1 Administrator) with culturally authentic Tamil Nadu names across 20+ engineering disciplines and industries:

| Persona | Email | Password | Role | Background Details |
|---|---|---|---|---|
| **Student (Demo Lead)** | `student@alumnia.edu` | `Password123!` | Student | Karthik Saravanan (AI & DS '26, Aspiring ML/Full-Stack) |
| **Alumni (Lead Mentor)** | `deepa.subramanian@alumni.edu` | `Password123!` | Alumni | Deepa Subramanian (Principal Architect, Cloud & AI) |
| **Alumni (Software Mentor)** | `vignesh.balasubramanian@alumni.edu` | `Password123!` | Alumni | Vignesh Balasubramanian (Staff Engineer, FinTech) |
| **Alumni (AI Engineer)** | `arun.prakash@alumni.edu` | `Password123!` | Alumni | Arun Prakash (Senior AI Engineer, Computer Vision) |
| **Alumni (Data Scientist)** | `priya.balaji@alumni.edu` | `Password123!` | Alumni | Priya Balaji (Lead Data Scientist, Deep Learning) |
| **Alumni (Aerospace Lead)** | `rajendran.periasamy@alumni.edu` | `Password123!` | Alumni | Dr. Rajendran Periasamy (Principal Aerospace Scientist, ISRO) |
| **Alumni (Robotics Architect)** | `karthikeyan.munusamy@alumni.edu` | `Password123!` | Alumni | Karthikeyan Munusamy (Lead Robotics Architect, Addverb) |
| **Alumni (Silicon Verification)**| `venkatesh.radhakrishnan@alumni.edu` | `Password123!` | Alumni | Venkatesh Radhakrishnan (Principal Silicon Architect, Qualcomm) |
| **HOD / Administrator** | `admin@alumnia.edu` | `Password123!` | Admin | Dr. R. Meenakshi Sundaram (HOD, AI & DS) |

*All 142 seeded accounts (70 Students, 71 Alumni, 1 Admin) use the default demonstration password: `Password123!`*

---

## 6. How to Run and Test the Application

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### Step 1: Run the Automated Verification Test Suite
```bash
cd backend
python -m pytest tests/test_recommendations.py tests/test_enhancements.py -v
```
*Expected result: 8 passed in ~3 seconds.*

### Step 2: Start the Backend Server
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
- API Base URL: `http://localhost:8000`
- Swagger Interactive Documentation: `http://localhost:8000/docs`

### Step 3: Start the Frontend Application
```bash
cd frontend
npm.cmd run dev
```
- Web Application: `http://localhost:5173`

---

## 7. Sample Queries to Test in the AI Assistant

Sign in with `student@alumnia.edu` (Password: `Password123!`) and navigate to **AI Assistant**:
1. *"Find alumni working in artificial intelligence"*
2. *"Which skills should I learn to become a data scientist?"*
3. *"Help me write a message requesting mentorship to Deepa"*
4. *"Find alumni in Chennai who work in cloud computing"*
5. *"Recommend three alumni for my Generative AI project"*

Sign in with `deepa.subramanian@alumni.edu` (Password: `Password123!`) to test Alumni Mode:
1. *"Show students interested in web development who need mentorship"*
2. *"Find students interested in Artificial Intelligence"*

---

## 8. College Project Verification Summary

- **Database Integrity**: 51 Students + 51 Alumni + 1 Admin = 103 total users with idempotent seed script.
- **Academic Grounding**: Formatted specifically for Bannari Amman Institute of Technology (BIT), Sathyamangalam.
- **Codebase Tests**: 8 unit & integration tests passing (`tests/test_recommendations.py`, `tests/test_enhancements.py`).
- **Frontend Build**: Zero TypeScript errors (`tsc && vite build` clean exit 0).
