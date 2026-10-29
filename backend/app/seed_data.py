"""
Alumnia Seed Dataset
Idempotent, culturally appropriate Tamil Nadu-origin demo dataset
Contains:
 - 1 Admin (Dean of Alumni Affairs & Career Development)
 - 50 Students (diverse departments, skills, projects, and career targets)
 - 50 Alumni (diverse companies, roles, experience levels, and mentorship topics)
"""

from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.models import (
    User, Profile, ProfileSkill, WorkExperience, Education, Project,
    Job, Event, Connection, ConnectionRequest, Conversation, Message,
    MentorshipRequest, MentorshipSession, Notification, RecommendationFeedback
)
from app.new_engineering_profiles import NEW_STUDENT_SPECS, NEW_ALUMNI_SPECS

# -------------------------------------------------------------
# 50 STUDENT PROFILES SPECIFICATIONS
# -------------------------------------------------------------
STUDENT_SPECS = [
    {
        "email": "student@alumnia.edu",
        "name": "Karthik Saravanan",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "Final-Year CS Student | Aspiring Machine Learning & Full-Stack Engineer",
        "bio": "Final-year computer science engineering undergraduate focusing on generative AI, distributed systems, and modern web architectures. Seeking experienced alumni mentorship and entry-level software engineering roles in top technology companies.",
        "skills": ["Python", "React", "TypeScript", "FastAPI", "Machine Learning", "PostgreSQL", "Docker", "Tailwind CSS"],
        "target_roles": ["Software Engineer", "Machine Learning Engineer", "Full Stack Developer"],
        "industries": ["Software & Cloud", "Artificial Intelligence", "FinTech"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Remote", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Prepare for software engineering and AI technical interview loops, learn distributed system design best practices, and receive resume guidance.",
        "projects": [
            {"title": "Alumnia Networking Platform", "desc": "Full-stack AI-powered networking portal connecting students and graduates with explainable 7-factor semantic matching.", "tech": "React, TypeScript, FastAPI, Scikit-learn, PostgreSQL"}
        ]
    },
    {
        "email": "arjun.kumar@student.alumnia.edu",
        "name": "Arjun Kumar",
        "dept": "Artificial Intelligence and Data Science",
        "degree": "B.Tech Artificial Intelligence and Data Science",
        "grad_year": 2026,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "AI & Data Science Student | Deep Learning & Computer Vision Enthusiast",
        "bio": "Undergraduate passionate about deep neural networks, image segmentation, and edge AI deployment. Seeking alumni guidance on transitioning into AI research and computer vision engineering.",
        "skills": ["Python", "PyTorch", "Computer Vision", "Deep Learning", "OpenCV", "TensorFlow", "SQL"],
        "target_roles": ["AI Engineer", "Computer Vision Engineer", "Data Scientist"],
        "industries": ["Artificial Intelligence", "Autonomous Systems", "Healthcare"],
        "locations": ["Coimbatore, Tamil Nadu", "Bengaluru, Karnataka", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Guidance on preparing for AI technical interviews and selecting computer vision research projects.",
        "projects": [
            {"title": "Autonomous Agricultural Weed Detector", "desc": "YOLOv8-based edge vision model deployed on Raspberry Pi for real-time crop weed detection.", "tech": "Python, PyTorch, OpenCV, Edge TPU"}
        ]
    },
    {
        "email": "nivetha.raj@student.alumnia.edu",
        "name": "Nivetha Raj",
        "dept": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2025,
        "location": "Chennai, Tamil Nadu",
        "headline": "IT Undergrad | Cloud Architecture & DevOps Specialist",
        "bio": "Pre-final year IT student with AWS certified cloud practitioner credentials. Building automated CI/CD pipelines, containerized microservices, and Kubernetes clusters.",
        "skills": ["AWS", "Docker", "Kubernetes", "Linux", "CI/CD", "Python", "Terraform", "Java"],
        "target_roles": ["Cloud Engineer", "DevOps Engineer", "Site Reliability Engineer"],
        "industries": ["Cloud & Enterprise Software", "FinTech", "SaaS"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Hyderabad"],
        "mentorship_goals": "Looking for guidance from cloud architects on Kubernetes multi-tenancy and production infrastructure.",
        "projects": [
            {"title": "Multi-Region Cloud Deployment Orchestrator", "desc": "Terraform and GitHub Actions pipeline deploying auto-scaling microservices on AWS EKS.", "tech": "AWS, Terraform, Kubernetes, Helm"}
        ]
    },
    {
        "email": "harini.prakash@student.alumnia.edu",
        "name": "Harini Prakash",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Madurai, Tamil Nadu",
        "headline": "CS Undergraduate | Natural Language Processing & Generative AI",
        "bio": "Enthusiastic about large language models, retrieval-augmented generation (RAG), and Tamil NLP research. Eager to connect with alumni working on applied GenAI.",
        "skills": ["Python", "Generative AI", "NLP", "LangChain", "Hugging Face", "SQL", "Prompt Engineering"],
        "target_roles": ["Generative AI Engineer", "NLP Scientist", "Machine Learning Engineer"],
        "industries": ["Artificial Intelligence", "EdTech", "Enterprise Software"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Remote"],
        "mentorship_goals": "Learn how to scale fine-tuned LLM inference and build enterprise RAG applications.",
        "projects": [
            {"title": "Tamil Document Question-Answering Bot", "desc": "Domain-adapted RAG pipeline utilizing Llama-3 and multilingual sentence embeddings for government documents.", "tech": "Python, LangChain, ChromaDB, FastAPI"}
        ]
    },
    {
        "email": "praveen.kumar.s@student.alumnia.edu",
        "name": "Praveen Kumar S",
        "dept": "Electronics and Communication Engineering",
        "degree": "B.E. Electronics and Communication Engineering",
        "grad_year": 2025,
        "location": "Salem, Tamil Nadu",
        "headline": "ECE Student | Embedded Systems & IoT Firmware Developer",
        "bio": "Working on ARM Cortex microcontrollers, RTOS, and low-power IoT wireless mesh networks. Seeking alumni in semiconductor and automotive electronics.",
        "skills": ["C++", "Embedded Systems", "IoT", "RTOS", "ARM Cortex", "PCB Design", "Python"],
        "target_roles": ["Embedded Software Engineer", "Firmware Engineer", "IoT Systems Developer"],
        "industries": ["Embedded Systems & IoT", "Automotive & EV", "Semiconductors"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Guidance on transitioning from microcontroller hobby projects into industrial automotive embedded engineering.",
        "projects": [
            {"title": "Smart Factory Vibration & Thermal Monitor", "desc": "FreeRTOS firmware for ESP32 communicating via MQTT to monitor industrial motor bearings.", "tech": "Embedded C, FreeRTOS, MQTT, KiCAD"}
        ]
    },
    {
        "email": "yazhini.devi@student.alumnia.edu",
        "name": "Yazhini Devi",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Tiruchirappalli, Tamil Nadu",
        "headline": "CS Student | Frontend Specialist & UI/UX Design System Builder",
        "bio": "Passionate about creating accessible, beautiful web applications. Experienced in React, Next.js, Figma design systems, and responsive micro-frontends.",
        "skills": ["React", "TypeScript", "JavaScript", "UI/UX Design", "Figma", "HTML/CSS", "Next.js", "Tailwind CSS"],
        "target_roles": ["Frontend Engineer", "UI/UX Developer", "Product Designer"],
        "industries": ["SaaS & Cloud", "E-Commerce", "Digital Media"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Remote"],
        "mentorship_goals": "Seeking design critique and advice on interview preparation for product engineering teams.",
        "projects": [
            {"title": "Modular Design System for Academic Portals", "desc": "Component library built with React, Radix UI, and Tailwind CSS with 100% WCAG 2.1 AA accessibility score.", "tech": "React, TypeScript, Storybook, Figma"}
        ]
    },
    {
        "email": "sanjay.kumar.r@student.alumnia.edu",
        "name": "Sanjay Kumar R",
        "dept": "Mechanical Engineering",
        "degree": "B.E. Mechanical Engineering",
        "grad_year": 2025,
        "location": "Erode, Tamil Nadu",
        "headline": "Mechanical Undergrad | Electric Vehicle Powertrain & Thermal Analysis",
        "bio": "Specializing in EV battery pack design, CFD thermal simulations, and lightweight automotive chassis optimization using ANSYS and SolidWorks.",
        "skills": ["AutoCAD", "SolidWorks", "ANSYS", "Automotive Systems", "MATLAB", "Finite Element Analysis", "Python"],
        "target_roles": ["EV Design Engineer", "Thermal Engineer", "Mechanical Analyst"],
        "industries": ["Automotive & EV", "Renewable Energy", "Manufacturing"],
        "locations": ["Chennai, Tamil Nadu", "Hosur, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Seeking insights on electric vehicle manufacturing standards, battery thermal management, and R&D roles.",
        "projects": [
            {"title": "Phase-Change Material Battery Thermal Management", "desc": "Simulated battery cooling jacket maintaining lithium-ion cell temperatures below 38°C under fast charging.", "tech": "SolidWorks, ANSYS Fluent, MATLAB"}
        ]
    },
    {
        "email": "keerthana.s@student.alumnia.edu",
        "name": "Keerthana S",
        "dept": "Biotechnology",
        "degree": "B.Tech Biotechnology",
        "grad_year": 2026,
        "location": "Tiruppur, Tamil Nadu",
        "headline": "Biotechnology Student | Computational Biology & Bio-Informatics",
        "bio": "Interdisciplinary student using Python, BioPython, and machine learning to analyze genomic variants and simulate protein-ligand docking.",
        "skills": ["Python", "Bioinformatics", "Data Analytics", "Machine Learning", "SQL", "R", "Molecular Docking"],
        "target_roles": ["Computational Biologist", "Bioinformatics Analyst", "Data Scientist"],
        "industries": ["Biotech & Healthcare", "Pharmaceuticals", "Artificial Intelligence"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Hyderabad"],
        "mentorship_goals": "Guidance on career paths in clinical bio-data science and applying machine learning to drug discovery.",
        "projects": [
            {"title": "Anti-Microbial Peptide Predictor", "desc": "Support vector machine and Random Forest model classifying therapeutic peptide activity from sequence motifs.", "tech": "Python, Scikit-learn, BioPython, Streamlit"}
        ]
    },
    {
        "email": "vignesh.raj@student.alumnia.edu",
        "name": "Vignesh Raj",
        "dept": "Electrical and Electronics Engineering",
        "degree": "B.E. Electrical and Electronics Engineering",
        "grad_year": 2025,
        "location": "Vellore, Tamil Nadu",
        "headline": "EEE Student | Power Electronics & Smart Grid Systems",
        "bio": "Passionate about inverter topology, renewable microgrids, and IoT-enabled smart energy meters. Experienced with MATLAB Simulink and PCB layout.",
        "skills": ["Power Electronics", "MATLAB", "Simulink", "PCB Design", "Embedded Systems", "Control Systems", "C++"],
        "target_roles": ["Power Electronics Engineer", "Renewable Energy Specialist", "Electrical Systems Engineer"],
        "industries": ["Renewable Energy", "Automotive & EV", "Industrial Automation"],
        "locations": ["Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Connect with alumni working on solar microinverters and high-efficiency motor drives.",
        "projects": [
            {"title": "Grid-Tied Bidirectional Solar Inverter", "desc": "Simulated and built a 1kW SiC-based dual-active bridge converter with 97.4% efficiency.", "tech": "MATLAB, Simulink, Altium Designer, C++"}
        ]
    },
    {
        "email": "dharshini.m@student.alumnia.edu",
        "name": "Dharshini M",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Thanjavur, Tamil Nadu",
        "headline": "Cybersecurity & Network Defense Aspirant | Ethical Hacker",
        "bio": "Dedicated to vulnerability assessment, penetration testing, and SOC operations. Active participant in CTF security competitions.",
        "skills": ["Cybersecurity", "Network Security", "Ethical Security Testing", "Linux", "Python", "Cloud Security", "Wireshark"],
        "target_roles": ["Cybersecurity Analyst", "Security Engineer", "Penetration Tester"],
        "industries": ["Cyber Security & Defense", "FinTech", "Cloud & Enterprise Software"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Remote"],
        "mentorship_goals": "Learn how enterprise SOC teams detect advanced persistent threats and acquire relevant industry certifications.",
        "projects": [
            {"title": "Automated Web Application Vulnerability Scanner", "desc": "Python security tool identifying OWASP Top 10 vulnerabilities including SQL injection and XSS.", "tech": "Python, Docker, OWASP ZAP, SQLite"}
        ]
    },
    # 11 - 20
    {
        "email": "anbuselvan.k@student.alumnia.edu",
        "name": "Anbuselvan K",
        "dept": "Civil Engineering",
        "degree": "B.E. Civil Engineering",
        "grad_year": 2025,
        "location": "Tirunelveli, Tamil Nadu",
        "headline": "Civil Engineering Student | Structural Analysis & BIM Modeling",
        "bio": "Undergraduate skilled in Revit, ETABS, and sustainable building materials. Interested in computational structural engineering and green smart buildings.",
        "skills": ["AutoCAD", "Revit", "ETABS", "Structural Analysis", "Project Management", "Python", "BIM"],
        "target_roles": ["Structural Engineer", "BIM Coordinator", "Civil Project Engineer"],
        "industries": ["Infrastructure & Construction", "Urban Tech", "Real Estate"],
        "locations": ["Chennai, Tamil Nadu", "Madurai, Tamil Nadu", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Guidance on modern precast concrete engineering and international BIM workflows.",
        "projects": [{"title": "Seismic Analysis of High-Rise Residential Tower", "desc": "ETABS dynamic response spectrum analysis of 20-story RC structure.", "tech": "ETABS, AutoCAD, Excel VBA"}]
    },
    {
        "email": "balamurugan.t@student.alumnia.edu",
        "name": "Balamurugan T",
        "dept": "Mechatronics Engineering",
        "degree": "B.E. Mechatronics Engineering",
        "grad_year": 2026,
        "location": "Hosur, Tamil Nadu",
        "headline": "Mechatronics Undergrad | Industrial Robotics & ROS Developer",
        "bio": "Developing autonomous mobile robots (AMR) using Robot Operating System (ROS2), SLAM algorithms, and LiDAR sensor fusion.",
        "skills": ["Robotics", "ROS", "C++", "Python", "Control Systems", "Embedded Systems", "Computer Vision"],
        "target_roles": ["Robotics Software Engineer", "Automation Engineer", "Mechatronics Specialist"],
        "industries": ["Industrial Automation & Robotics", "Automotive & EV", "Logistics Tech"],
        "locations": ["Hosur, Tamil Nadu", "Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Learn navigation stack optimization in ROS2 and connect with robotics alumni.",
        "projects": [{"title": "Warehouse AMR with Autonomous Navigation", "desc": "Differential drive robot navigating mapped warehouses with real-time obstacle avoidance.", "tech": "ROS2, C++, Python, Gazebo, LiDAR"}]
    },
    {
        "email": "chithra.devi.n@student.alumnia.edu",
        "name": "Chithra Devi N",
        "dept": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2026,
        "location": "Dindigul, Tamil Nadu",
        "headline": "IT Undergrad | Data Analytics & Business Intelligence Enthusiast",
        "bio": "Passionate about transforming messy transactional data into actionable executive dashboards. Proficient in SQL, Power BI, Python, and Tableau.",
        "skills": ["SQL", "Data Analytics", "Power BI", "Python", "Tableau", "Excel", "Data Science"],
        "target_roles": ["Data Analyst", "Business Intelligence Engineer", "Product Analyst"],
        "industries": ["FinTech", "E-Commerce", "Consulting"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Understand analytics expectations in top consumer tech companies.",
        "projects": [{"title": "E-Commerce Customer Retention & Churn Engine", "desc": "Cohort analysis and RFM customer segmentation dashboard predicting 30-day dropoff.", "tech": "Python, SQL, Power BI, Pandas"}]
    },
    {
        "email": "dinesh.karthik.p@student.alumnia.edu",
        "name": "Dinesh Karthik P",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2025,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "CS Student | Backend Microservices & Distributed Databases",
        "bio": "Focusing on distributed caching, high-throughput message queues, Go, and relational database internals.",
        "skills": ["Java", "Spring Boot", "Go", "PostgreSQL", "Kafka", "REST APIs", "Docker", "System Design"],
        "target_roles": ["Backend Engineer", "Software Engineer", "Systems Developer"],
        "industries": ["FinTech", "SaaS & Cloud", "E-Commerce"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu", "Hyderabad"],
        "mentorship_goals": "Advice on cracking backend system design interviews and scaling event-driven architectures.",
        "projects": [{"title": "High-Throughput Order Matching Engine", "desc": "In-memory order book handling 50k transactions/sec with zero loss.", "tech": "Go, Redis, PostgreSQL, Docker"}]
    },
    {
        "email": "elango.s@student.alumnia.edu",
        "name": "Elango S",
        "dept": "Chemical Engineering",
        "degree": "B.Tech Chemical Engineering",
        "grad_year": 2025,
        "location": "Erode, Tamil Nadu",
        "headline": "Chemical Engineering Student | Process Simulation & Sustainable Refining",
        "bio": "Focused on ASPEN Plus simulation, green hydrogen production, and effluent treatment optimization.",
        "skills": ["Process Simulation", "Aspen Plus", "MATLAB", "Chemical Engineering", "Data Analytics", "Python"],
        "target_roles": ["Process Engineer", "Chemical Analyst", "Sustainability Engineer"],
        "industries": ["Petrochemicals & Energy", "Renewable Energy", "Pharmaceuticals"],
        "locations": ["Chennai, Tamil Nadu", "Tuticorin, Tamil Nadu", "Erode, Tamil Nadu"],
        "mentorship_goals": "Seeking guidance on process optimization jobs in energy and green manufacturing.",
        "projects": [{"title": "Bio-Ethanol Distillation Column Optimization", "desc": "ASPEN Plus simulation achieving 18% thermal energy reduction using heat integration.", "tech": "Aspen Plus, Excel, MATLAB"}]
    },
    {
        "email": "gayathri.v@student.alumnia.edu",
        "name": "Gayathri V",
        "dept": "Artificial Intelligence and Data Science",
        "degree": "B.Tech Artificial Intelligence and Data Science",
        "grad_year": 2026,
        "location": "Salem, Tamil Nadu",
        "headline": "AI & DS Student | Predictive Modeling & Time Series Forecasting",
        "bio": "Hands-on experience in financial market forecasting, anomaly detection, and automated feature engineering using Scikit-Learn and LightGBM.",
        "skills": ["Python", "Machine Learning", "Data Science", "SQL", "Deep Learning", "Pandas", "Scikit-learn"],
        "target_roles": ["Data Scientist", "Machine Learning Engineer", "Quantitative Analyst"],
        "industries": ["FinTech", "Artificial Intelligence", "Retail Tech"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Remote"],
        "mentorship_goals": "Learn how financial data science teams build robust production backtesting pipelines.",
        "projects": [{"title": "Cryptocurrency Volatility Forecasting", "desc": "LSTM and GARCH hybrid model predicting intra-day volatility spikes.", "tech": "Python, PyTorch, Pandas, Scikit-learn"}]
    },
    {
        "email": "hemalatha.r@student.alumnia.edu",
        "name": "Hemalatha R",
        "dept": "Electronics and Communication Engineering",
        "degree": "B.E. Electronics and Communication Engineering",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "ECE Student | VLSI Design & Digital Circuit Architecture",
        "bio": "Interested in ASIC/FPGA digital design, SystemVerilog verification, and CMOS semiconductor design.",
        "skills": ["VLSI", "Verilog", "FPGA", "SystemVerilog", "Digital Electronics", "C++", "Linux"],
        "target_roles": ["VLSI Design Engineer", "ASIC Verification Engineer", "FPGA Developer"],
        "industries": ["Semiconductors", "Hardware Tech", "Telecommunications"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu", "Hyderabad"],
        "mentorship_goals": "Preparation for core semiconductor company interviews (Qualcomm, Intel, TI).",
        "projects": [{"title": "RISC-V 32-bit Pipelined Processor Core", "desc": "5-stage pipelined RV32I core designed in Verilog and synthesized on Xilinx Artix-7.", "tech": "Verilog, Vivado, ModelSim, C"}]
    },
    {
        "email": "ilango.m@student.alumnia.edu",
        "name": "Ilango M",
        "dept": "Food Technology",
        "degree": "B.Tech Food Technology",
        "grad_year": 2025,
        "location": "Madurai, Tamil Nadu",
        "headline": "Food Tech Student | Quality Assurance & Novel Food Formulations",
        "bio": "Undergraduate studying food preservation, HACCP safety compliance, and sustainable packaging materials.",
        "skills": ["Food Technology", "Quality Assurance", "HACCP", "Microbiology", "Product Development", "Data Analytics"],
        "target_roles": ["Food Quality Manager", "R&D Food Technologist", "Process Quality Specialist"],
        "industries": ["FMCG & Food Processing", "Agriculture & Food", "Biotech"],
        "locations": ["Chennai, Tamil Nadu", "Madurai, Tamil Nadu", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Connect with alumni in multinational FMCG quality and supply chain divisions.",
        "projects": [{"title": "Edible Chitosan Coating for Shelf-Life Extension", "desc": "Formulated natural anti-microbial bio-film extending tropical fruit shelf life by 14 days.", "tech": "Food Chemistry, Lab Analysis, Statistical Design"}]
    },
    {
        "email": "janani.priya.k@student.alumnia.edu",
        "name": "Janani Priya K",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Vellore, Tamil Nadu",
        "headline": "CS Student | Full-Stack Web & Mobile App Developer",
        "bio": "Building cross-platform apps with React Native, Node.js, and MongoDB. Enthusiastic about progressive web apps and seamless user journeys.",
        "skills": ["JavaScript", "React", "React Native", "Node.js", "MongoDB", "Express", "REST APIs", "Tailwind CSS"],
        "target_roles": ["Full Stack Developer", "Mobile App Engineer", "Software Engineer"],
        "industries": ["Consumer Tech", "EdTech", "FinTech"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Remote"],
        "mentorship_goals": "Guidance on architecting offline-first mobile applications.",
        "projects": [{"title": "Campus Peer Tutoring Marketplace", "desc": "React Native and Node.js mobile portal for booking peer study sessions.", "tech": "React Native, Node.js, MongoDB, Socket.io"}]
    },
    {
        "email": "kabilan.v@student.alumnia.edu",
        "name": "Kabilan V",
        "dept": "Biomedical Engineering",
        "degree": "B.E. Biomedical Engineering",
        "grad_year": 2025,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Biomedical Student | Medical Device Prototyping & Biosensors",
        "bio": "Developing affordable non-invasive physiological monitoring devices. Proficient in biosignal processing with MATLAB and microcontroller interfacing.",
        "skills": ["Biomedical Engineering", "Signal Processing", "MATLAB", "Embedded Systems", "PCB Design", "Python"],
        "target_roles": ["Biomedical Engineer", "Medical Device Developer", "Clinical Systems Specialist"],
        "industries": ["Healthcare & MedTech", "Medical Devices", "Biotech"],
        "locations": ["Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Seeking advice on regulatory compliance (ISO 13485) and healthcare startup pathways.",
        "projects": [{"title": "Wearable Continuous ECG Arrythmia Detector", "desc": "Analog front-end and BLE transmission module classifying cardiac arrhythmias with 96% accuracy.", "tech": "Embedded C, MATLAB, KiCAD, Python"}]
    },
    # 21 - 30
    {
        "email": "lavanya.s@student.alumnia.edu",
        "name": "Lavanya S",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "CS Student | Machine Learning & Statistical NLP",
        "bio": "Deeply interested in semantic search, sentiment classification, and transformer model optimization.",
        "skills": ["Python", "Machine Learning", "NLP", "PyTorch", "SQL", "Docker", "FastAPI"],
        "target_roles": ["Machine Learning Engineer", "Data Scientist", "Software Engineer"],
        "industries": ["Artificial Intelligence", "SaaS & Cloud", "E-Commerce"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Resume review and tips for FAANG and high-growth AI startup interviews.",
        "projects": [{"title": "Semantic Code Search Engine", "desc": "Vector-indexed source code search matching natural language queries with Python functions.", "tech": "Python, Sentence-Transformers, Qdrant, FastAPI"}]
    },
    {
        "email": "manikandan.p@student.alumnia.edu",
        "name": "Manikandan P",
        "dept": "Mechanical Engineering",
        "degree": "B.E. Mechanical Engineering",
        "grad_year": 2025,
        "location": "Tiruppur, Tamil Nadu",
        "headline": "Mechanical Student | Smart Manufacturing & Industry 4.0",
        "bio": "Focusing on CNC programming, computer-integrated manufacturing, and predictive maintenance sensor networks.",
        "skills": ["AutoCAD", "SolidWorks", "CNC Programming", "Industrial Automation", "Manufacturing", "Python"],
        "target_roles": ["Manufacturing Engineer", "Production Specialist", "Automation Engineer"],
        "industries": ["Industrial Automation & Robotics", "Automotive & EV", "Textile Tech"],
        "locations": ["Coimbatore, Tamil Nadu", "Tiruppur, Tamil Nadu", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Learn how modern smart factories deploy digital twin and industrial IoT.",
        "projects": [{"title": "Digital Twin for CNC Lathe Vibration Tracking", "desc": "IoT accelerometer tracking spindle wear to preempt cutting tool breakage.", "tech": "SolidWorks, Python, MQTT, Node-RED"}]
    },
    {
        "email": "nandhini.r@student.alumnia.edu",
        "name": "Nandhini R",
        "dept": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2026,
        "location": "Salem, Tamil Nadu",
        "headline": "IT Student | Cloud Security & Zero Trust Architecture",
        "bio": "Studying cloud identity federation, IAM policy automation, and DevSecOps automated vulnerability scanning.",
        "skills": ["AWS", "Cloud Security", "Cybersecurity", "Python", "Linux", "Docker", "Terraform"],
        "target_roles": ["Cloud Security Engineer", "DevSecOps Specialist", "Security Analyst"],
        "industries": ["Cloud & Enterprise Software", "FinTech", "Cyber Security & Defense"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Preparing for AWS Certified Security Specialty and understanding enterprise IAM roles.",
        "projects": [{"title": "Automated AWS IAM Least-Privilege Auditor", "desc": "Serverless Lambda function analyzing CloudTrail logs to recommend reduced IAM permission policies.", "tech": "Python, AWS Lambda, Boto3, Terraform"}]
    },
    {
        "email": "omprakash.m@student.alumnia.edu",
        "name": "Omprakash M",
        "dept": "Electrical and Electronics Engineering",
        "degree": "B.E. Electrical and Electronics Engineering",
        "grad_year": 2025,
        "location": "Madurai, Tamil Nadu",
        "headline": "EEE Student | Industrial Drives & PLC Automation",
        "bio": "Specializing in Siemens and Allen-Bradley PLC ladder programming, SCADA development, and variable frequency drives.",
        "skills": ["PLC Programming", "SCADA", "Industrial Automation", "Control Systems", "Electrical Engineering", "MATLAB"],
        "target_roles": ["Automation Engineer", "SCADA Specialist", "Electrical Systems Engineer"],
        "industries": ["Industrial Automation & Robotics", "Manufacturing", "Energy"],
        "locations": ["Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Hosur, Tamil Nadu"],
        "mentorship_goals": "Guidance on transitioning into large-scale plant automation commissioning roles.",
        "projects": [{"title": "Automated Liquid Bottling & Capping Line", "desc": "Siemens S7-1200 PLC program with WinCC SCADA monitoring 60 bottles/min throughput.", "tech": "TIA Portal, Siemens PLC, SCADA"}]
    },
    {
        "email": "pavithra.k@student.alumnia.edu",
        "name": "Pavithra K",
        "dept": "Artificial Intelligence and Data Science",
        "degree": "B.Tech Artificial Intelligence and Data Science",
        "grad_year": 2026,
        "location": "Tiruchirappalli, Tamil Nadu",
        "headline": "AI & DS Student | Responsible AI & Algorithmic Fairness",
        "bio": "Researching bias mitigation in machine learning decision systems, explainable AI (SHAP, LIME), and AI governance.",
        "skills": ["Python", "Machine Learning", "Data Science", "SQL", "Explainable AI", "Data Analytics"],
        "target_roles": ["AI Ethics Specialist", "Data Scientist", "Machine Learning Engineer"],
        "industries": ["Artificial Intelligence", "FinTech", "Policy Tech"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Remote"],
        "mentorship_goals": "Seeking advice on research careers in fair AI and graduate admissions.",
        "projects": [{"title": "Credit Underwriting Fairness Auditor", "desc": "Benchmarked demographic parity and equalized odds metrics across credit risk models.", "tech": "Python, Fairlearn, Scikit-learn, Streamlit"}]
    },
    {
        "email": "ragul.s@student.alumnia.edu",
        "name": "Ragul S",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2025,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "CS Student | Competitive Programmer & Algorithms Specialist",
        "bio": "Codeforces Candidate Master. Strong foundation in graph theory, dynamic programming, and low-level C++ systems.",
        "skills": ["C++", "Algorithms", "Data Structures", "Python", "System Design", "SQL"],
        "target_roles": ["Software Engineer", "Systems Engineer", "Quantitative Developer"],
        "industries": ["FinTech", "High-Performance Computing", "Enterprise Tech"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu", "Hyderabad"],
        "mentorship_goals": "Interview prep for top tier algorithmic software engineering and HFT firms.",
        "projects": [{"title": "Lock-Free Concurrent Memory Allocator", "desc": "Custom memory manager minimizing thread contention using atomic compare-and-swap primitives.", "tech": "C++20, Linux pthreads, Benchmarking"}]
    },
    {
        "email": "saranya.m@student.alumnia.edu",
        "name": "Saranya M",
        "dept": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2026,
        "location": "Erode, Tamil Nadu",
        "headline": "IT Student | Product Management & User Research Aspirant",
        "bio": "Bridging technical engineering with customer problem discovery. Skilled in wireframing, feature prioritization, and agile roadmaps.",
        "skills": ["Product Management", "UI/UX Design", "Agile", "SQL", "Figma", "Data Analytics", "Communication"],
        "target_roles": ["Associate Product Manager", "Product Analyst", "Business Analyst"],
        "industries": ["Consumer Tech", "EdTech", "FinTech"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu"],
        "mentorship_goals": "APM interview preparation and product case study frameworks.",
        "projects": [{"title": "Student Ride-Sharing Feature Proposal", "desc": "Full PRD with market sizing, user interviews, and Figma wireframes for campus micro-transit.", "tech": "Figma, Notion, Product Analytics"}]
    },
    {
        "email": "thangavel.p@student.alumnia.edu",
        "name": "Thangavel P",
        "dept": "Civil Engineering",
        "degree": "B.E. Civil Engineering",
        "grad_year": 2025,
        "location": "Thanjavur, Tamil Nadu",
        "headline": "Civil Student | Geotechnical Engineering & Foundation Design",
        "bio": "Undergraduate studying soil mechanics, slope stability, and pile foundation load testing.",
        "skills": ["Civil Engineering", "Geotechnical Engineering", "AutoCAD", "MATLAB", "Project Management"],
        "target_roles": ["Geotechnical Engineer", "Site Engineer", "Civil Consultant"],
        "industries": ["Infrastructure & Construction", "Consulting", "Urban Tech"],
        "locations": ["Chennai, Tamil Nadu", "Thanjavur, Tamil Nadu"],
        "mentorship_goals": "Connect with structural and soil testing consultancy alumni.",
        "projects": [{"title": "Soil Stabilization Using Fly Ash and Coir Geotextiles", "desc": "Experimental CBR strength improvement for rural road subgrades.", "tech": "Lab Testing, Statistical Analysis"}]
    },
    {
        "email": "uma.maheshwari.s@student.alumnia.edu",
        "name": "Uma Maheshwari S",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Tirunelveli, Tamil Nadu",
        "headline": "CS Student | Cloud-Native Backend Development",
        "bio": "Building resilient REST and gRPC services using Node.js, TypeScript, and Docker container orchestration.",
        "skills": ["Node.js", "TypeScript", "Docker", "REST APIs", "PostgreSQL", "React", "Linux"],
        "target_roles": ["Backend Developer", "Software Engineer", "Full Stack Developer"],
        "industries": ["SaaS & Cloud", "E-Commerce", "Logistics Tech"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Best practices for writing maintainable microservices and passing system architecture interviews.",
        "projects": [{"title": "Serverless Notification Dispatcher", "desc": "Distributed queuing service delivering web push, SMS, and email notifications at scale.", "tech": "TypeScript, Node.js, Redis, AWS SQS"}]
    },
    {
        "email": "vasanth.kumar.r@student.alumnia.edu",
        "name": "Vasanth Kumar R",
        "dept": "Mechatronics Engineering",
        "degree": "B.E. Mechatronics Engineering",
        "grad_year": 2026,
        "location": "Dindigul, Tamil Nadu",
        "headline": "Mechatronics Undergrad | Drone Flight Controllers & Autonomy",
        "bio": "Building autonomous multi-rotor drones using PX4 flight stack, telemetry, and OpenCV aerial tracking.",
        "skills": ["Robotics", "Embedded Systems", "C++", "Python", "Computer Vision", "Control Systems"],
        "target_roles": ["UAV Systems Engineer", "Robotics Engineer", "Firmware Developer"],
        "industries": ["Aerospace & Defense", "Autonomous Systems", "Agriculture"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Insights on drone industry regulations (DGCA) and flight control systems engineering.",
        "projects": [{"title": "Vision-Guided Precision Agriculture Drone", "desc": "Quadcopter executing autonomous waypoints and multispectral plant canopy health analysis.", "tech": "PX4, C++, OpenCV, Python"}]
    },
    # 31 - 40
    {
        "email": "yuvaraj.k@student.alumnia.edu",
        "name": "Yuvaraj K",
        "dept": "Electronics and Communication Engineering",
        "degree": "B.E. Electronics and Communication Engineering",
        "grad_year": 2025,
        "location": "Vellore, Tamil Nadu",
        "headline": "ECE Student | Wireless Communications & 5G Signal Processing",
        "bio": "Studying MIMO antenna beamforming, OFDM modulations, and SDR (Software Defined Radio) communication links.",
        "skills": ["Wireless Communications", "Signal Processing", "MATLAB", "Python", "C++", "Embedded Systems"],
        "target_roles": ["RF Engineer", "Telecommunications Engineer", "Firmware Engineer"],
        "industries": ["Telecommunications", "Semiconductors", "Aerospace & Defense"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Hyderabad"],
        "mentorship_goals": "Connect with alumni in 5G Open-RAN and telecom equipment engineering.",
        "projects": [{"title": "GNU Radio SDR Spectrum Analyzer", "desc": "Built a 2.4 GHz real-time spectral waterfall display using HackRF SDR.", "tech": "GNU Radio, Python, C++, DSP"}]
    },
    {
        "email": "abinaya.s@student.alumnia.edu",
        "name": "Abinaya S",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "CS Student | Generative AI & Retrieval-Augmented Generation",
        "bio": "Hands-on experience with vector databases, agentic workflows, and semantic embedding pipelines.",
        "skills": ["Python", "Generative AI", "RAG", "LangChain", "SQL", "FastAPI", "React"],
        "target_roles": ["Generative AI Engineer", "AI Application Developer", "Software Engineer"],
        "industries": ["Artificial Intelligence", "EdTech", "FinTech"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Remote"],
        "mentorship_goals": "Learn how to evaluate RAG answer faithfulness and reduce hallucination in production.",
        "projects": [{"title": "Legal Case Precedent Search Assistant", "desc": "Retrieval system indexing Indian Supreme Court judgments with semantic metadata filters.", "tech": "Python, Pinecone, LlamaIndex, Streamlit"}]
    },
    {
        "email": "bharathidasan.m@student.alumnia.edu",
        "name": "Bharathidasan M",
        "dept": "Mechanical Engineering",
        "degree": "B.E. Mechanical Engineering",
        "grad_year": 2025,
        "location": "Salem, Tamil Nadu",
        "headline": "Mechanical Undergrad | Additive Manufacturing & 3D Prototyping",
        "bio": "Exploring industrial 3D printing slicing algorithms, metal additive metallurgy, and topology optimization.",
        "skills": ["SolidWorks", "Additive Manufacturing", "AutoCAD", "Materials Science", "Product Design"],
        "target_roles": ["Additive Manufacturing Engineer", "Mechanical Designer", "R&D Prototype Engineer"],
        "industries": ["Manufacturing", "Aerospace", "Medical Devices"],
        "locations": ["Coimbatore, Tamil Nadu", "Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Seeking advice on industrial additive manufacturing career avenues.",
        "projects": [{"title": "Topology-Optimized Aerospace Drone Arm", "desc": "Reduced component weight by 38% while maintaining safety factor under structural load.", "tech": "SolidWorks, ANSYS, FDM Slicing"}]
    },
    {
        "email": "deepalakshmi.k@student.alumnia.edu",
        "name": "Deepalakshmi K",
        "dept": "Biotechnology",
        "degree": "B.Tech Biotechnology",
        "grad_year": 2026,
        "location": "Madurai, Tamil Nadu",
        "headline": "Biotech Student | Bioprocess Engineering & Fermentation",
        "bio": "Specializing in microbial bioreactor scale-up, enzymatic hydrolysis, and biopharmaceutical downstream processing.",
        "skills": ["Bioprocess Engineering", "Microbiology", "Biotechnology", "Data Analytics", "Quality Control"],
        "target_roles": ["Bioprocess Engineer", "Biotech Quality Analyst", "Production Specialist"],
        "industries": ["Biotech & Healthcare", "Pharmaceuticals", "Agriculture"],
        "locations": ["Chennai, Tamil Nadu", "Hyderabad", "Bengaluru, Karnataka"],
        "mentorship_goals": "Preparing for vaccine and biologics manufacturing industrial roles.",
        "projects": [{"title": "Bacterial Cellulose Production from Agricultural Waste", "desc": "Optimized fermentation medium yielding high-tensile biomaterials from sugarcane bagasse.", "tech": "Bioreactor Operation, HPLC, UV-Vis"}]
    },
    {
        "email": "ezhilarasan.r@student.alumnia.edu",
        "name": "Ezhilarasan R",
        "dept": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2025,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "IT Undergrad | Kubernetes Cluster Administration & CI/CD",
        "bio": "Certified Kubernetes Application Developer (CKAD) aspirant. Passionate about GitOps, ArgoCD, and zero-downtime canary rollouts.",
        "skills": ["Kubernetes", "Docker", "Linux", "CI/CD", "AWS", "Python", "Go"],
        "target_roles": ["DevOps Engineer", "Site Reliability Engineer", "Cloud Infrastructure Engineer"],
        "industries": ["Cloud & Enterprise Software", "FinTech", "SaaS"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu", "Remote"],
        "mentorship_goals": "Learn how top tech firms handle Kubernetes multi-cluster failover and disaster recovery.",
        "projects": [{"title": "GitOps Automated Cluster Delivery Pipeline", "desc": "ArgoCD and Helm based configuration repository deploying microservices to local Kind clusters.", "tech": "Kubernetes, Helm, ArgoCD, GitHub Actions"}]
    },
    {
        "email": "gokulnath.s@student.alumnia.edu",
        "name": "Gokulnath S",
        "dept": "Artificial Intelligence and Data Science",
        "degree": "B.Tech Artificial Intelligence and Data Science",
        "grad_year": 2026,
        "location": "Erode, Tamil Nadu",
        "headline": "AI & DS Student | Automated Machine Learning & MLOps",
        "bio": "Building continuous model training and monitoring pipelines with MLflow, Docker, and FastAPI.",
        "skills": ["Python", "Machine Learning", "Docker", "FastAPI", "SQL", "Data Science", "Git"],
        "target_roles": ["MLOps Engineer", "Machine Learning Engineer", "Data Platform Engineer"],
        "industries": ["Artificial Intelligence", "SaaS & Cloud", "FinTech"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Understanding model drift detection and scalable real-time model serving in production.",
        "projects": [{"title": "Automated Drift Monitoring Pipeline", "desc": "Evidently AI and MLflow pipeline retraining classification models upon detecting feature distribution shift.", "tech": "Python, MLflow, Docker, FastAPI"}]
    },
    {
        "email": "hema.malini.p@student.alumnia.edu",
        "name": "Hema Malini P",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Tiruchirappalli, Tamil Nadu",
        "headline": "CS Student | React & Modern Web State Architecture",
        "bio": "Passionate about modern component composition, React query caching, and performant client-side data visualization.",
        "skills": ["React", "TypeScript", "JavaScript", "HTML/CSS", "Tailwind CSS", "REST APIs", "Node.js"],
        "target_roles": ["Frontend Developer", "Web Application Engineer", "Software Engineer"],
        "industries": ["SaaS & Cloud", "Consumer Tech", "EdTech"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Remote"],
        "mentorship_goals": "Seeking code reviews and advice on frontend performance profiling.",
        "projects": [{"title": "Interactive Analytics Kanban Dashboard", "desc": "Virtual list rendering with drag-and-drop task workflows handling 10,000+ data nodes smoothly.", "tech": "React, TypeScript, Tailwind CSS, Zustand"}]
    },
    {
        "email": "inian.v@student.alumnia.edu",
        "name": "Inian V",
        "dept": "Electrical and Electronics Engineering",
        "degree": "B.E. Electrical and Electronics Engineering",
        "grad_year": 2025,
        "location": "Thanjavur, Tamil Nadu",
        "headline": "EEE Student | Battery Management Systems (BMS) for EVs",
        "bio": "Focused on state-of-charge (SoC) estimation algorithms, cell balancing circuits, and CAN bus vehicle telemetry.",
        "skills": ["Embedded Systems", "Power Electronics", "MATLAB", "Simulink", "C++", "Automotive Systems"],
        "target_roles": ["BMS Firmware Engineer", "EV Powertrain Engineer", "Electrical Hardware Engineer"],
        "industries": ["Automotive & EV", "Renewable Energy", "Electronics"],
        "locations": ["Hosur, Tamil Nadu", "Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Learn industrial BMS safety standards (ISO 26262) from automotive alumni.",
        "projects": [{"title": "Extended Kalman Filter SoC Estimator", "desc": "Simulink model accurately predicting lithium battery state of charge under dynamic driving cycles.", "tech": "MATLAB, Simulink, Embedded C"}]
    },
    {
        "email": "jeevitha.m@student.alumnia.edu",
        "name": "Jeevitha M",
        "dept": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "IT Student | Cloud Database Administration & SQL Tuning",
        "bio": "Experienced with indexing strategies, query execution plans, PostgreSQL partitioning, and transactional consistency.",
        "skills": ["SQL", "PostgreSQL", "Database Administration", "Python", "AWS", "Linux"],
        "target_roles": ["Database Administrator", "Data Engineer", "Cloud Systems Engineer"],
        "industries": ["FinTech", "Enterprise Software", "E-Commerce"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Guidance on career paths in enterprise database reliability and migration to cloud RDS.",
        "projects": [{"title": "Automated Database Slow-Query Profiler", "desc": "Python utility capturing pg_stat_statements and alerting developers to unindexed table scans.", "tech": "PostgreSQL, Python, Docker"}]
    },
    {
        "email": "kirubakaran.s@student.alumnia.edu",
        "name": "Kirubakaran S",
        "dept": "Electronics and Communication Engineering",
        "degree": "B.E. Electronics and Communication Engineering",
        "grad_year": 2025,
        "location": "Tirunelveli, Tamil Nadu",
        "headline": "ECE Student | Edge AI & Embedded Machine Learning",
        "bio": "Deploying quantized neural networks onto ARM Cortex-M microcontrollers using TensorFlow Lite for Microcontrollers.",
        "skills": ["TinyML", "Embedded Systems", "Python", "C++", "Machine Learning", "IoT"],
        "target_roles": ["TinyML Engineer", "Embedded AI Specialist", "Firmware Engineer"],
        "industries": ["Semiconductors", "Healthcare & MedTech", "Industrial Automation"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Learn how to optimize neural network weights for ultra-low power microcontrollers.",
        "projects": [{"title": "Low-Power Acoustic Glass Breakage Detector", "desc": "8-bit quantized convolutional model running on STM32 with less than 20mW active power draw.", "tech": "TensorFlow Lite, Embedded C, STM32CubeIDE"}]
    },
    # 41 - 50
    {
        "email": "logeshwaran.r@student.alumnia.edu",
        "name": "Logeshwaran R",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Salem, Tamil Nadu",
        "headline": "CS Student | Distributed Systems & High-Concurrency APIs",
        "bio": "Passionate about event sourcing, database sharding, and fault-tolerant distributed consensus.",
        "skills": ["Java", "Spring Boot", "Go", "Docker", "PostgreSQL", "System Design", "REST APIs"],
        "target_roles": ["Software Engineer", "Backend Developer", "Systems Architect"],
        "industries": ["FinTech", "Cloud & Enterprise Software", "E-Commerce"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Learn how to design scalable multi-tier architectures for high-traffic platforms.",
        "projects": [{"title": "Distributed Flash-Sale Booking Gateway", "desc": "Redis rate-limited booking engine with optimistic locking preventing seat over-allocation.", "tech": "Java, Spring Boot, Redis, PostgreSQL"}]
    },
    {
        "email": "madhumitha.k@student.alumnia.edu",
        "name": "Madhumitha K",
        "dept": "Civil Engineering",
        "degree": "B.E. Civil Engineering",
        "grad_year": 2025,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Civil Student | Environmental Engineering & Water Treatment",
        "bio": "Focused on industrial effluent purification, membrane bioreactors, and smart municipal stormwater management.",
        "skills": ["Civil Engineering", "Environmental Engineering", "AutoCAD", "Water Treatment", "GIS", "Python"],
        "target_roles": ["Environmental Engineer", "Water Resources Specialist", "Civil Consultant"],
        "industries": ["Infrastructure & Construction", "Sustainability & CleanTech", "Government Tech"],
        "locations": ["Coimbatore, Tamil Nadu", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Connect with environmental engineering consultants working on smart city water infrastructure.",
        "projects": [{"title": "IoT Smart Urban Stormwater Sump Network", "desc": "Real-time flood telemetry network warning municipal control rooms of drainage choke points.", "tech": "AutoCAD, GIS, IoT Sensors, Python"}]
    },
    {
        "email": "naveen.prashanth.s@student.alumnia.edu",
        "name": "Naveen Prashanth S",
        "dept": "Mechanical Engineering",
        "degree": "B.E. Mechanical Engineering",
        "grad_year": 2025,
        "location": "Madurai, Tamil Nadu",
        "headline": "Mechanical Undergrad | Robotics Kinematics & Mechanical Gripper Design",
        "bio": "Designing custom end-effectors for industrial pick-and-place robots using CAD simulation and 3D printing.",
        "skills": ["SolidWorks", "Robotics", "AutoCAD", "Mechanical Design", "Python", "3D Printing"],
        "target_roles": ["Robotics Mechanical Engineer", "Product Design Engineer", "Automation Specialist"],
        "industries": ["Industrial Automation & Robotics", "Manufacturing", "Automotive"],
        "locations": ["Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Learn how industrial robot manufacturers design compliant soft-robotic grippers.",
        "projects": [{"title": "Underactuated Compliant Robotic Hand", "desc": "Tendon-driven mechanical gripper self-adapting to arbitrary fragile object geometries.", "tech": "SolidWorks, 3D Printing, Tensile Testing"}]
    },
    {
        "email": "poornima.r@student.alumnia.edu",
        "name": "Poornima R",
        "dept": "Artificial Intelligence and Data Science",
        "degree": "B.Tech Artificial Intelligence and Data Science",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "AI & DS Student | Medical Image Analysis & Healthcare AI",
        "bio": "Training convolutional and vision transformer models to detect pulmonary pathologies from chest X-rays.",
        "skills": ["Python", "Deep Learning", "Computer Vision", "PyTorch", "Healthcare AI", "Data Science"],
        "target_roles": ["Healthcare AI Engineer", "Computer Vision Scientist", "Data Scientist"],
        "industries": ["Healthcare & MedTech", "Artificial Intelligence", "Biotech"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Guidance on clinical AI validation, patient privacy standards (HIPAA/DISHA), and research publications.",
        "projects": [{"title": "Chest Radiograph Pneumonia Detection Pipeline", "desc": "DenseNet121 model achieving 94.2% ROC-AUC on NIH ChestX-ray14 benchmark dataset.", "tech": "PyTorch, Torchvision, Scikit-learn, Streamlit"}]
    },
    {
        "email": "rajesh.kannan.v@student.alumnia.edu",
        "name": "Rajesh Kannan V",
        "dept": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2026,
        "location": "Tiruppur, Tamil Nadu",
        "headline": "IT Student | Full-Stack JavaScript & GraphQL Architectures",
        "bio": "Building scalable web services with Next.js, Apollo GraphQL, and PostgreSQL. Advocate of clean architecture.",
        "skills": ["JavaScript", "TypeScript", "React", "Node.js", "GraphQL", "PostgreSQL", "REST APIs"],
        "target_roles": ["Full Stack Engineer", "Software Engineer", "Web Developer"],
        "industries": ["SaaS & Cloud", "E-Commerce", "FinTech"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu", "Remote"],
        "mentorship_goals": "Learn how fast-growing startups architect GraphQL schema federations.",
        "projects": [{"title": "Collaborative Real-Time Whiteboard", "desc": "WebSockets and Canvas API whiteboard allowing simultaneous drawing for remote teams.", "tech": "React, Node.js, Socket.io, Canvas API"}]
    },
    {
        "email": "shalini.m@student.alumnia.edu",
        "name": "Shalini M",
        "dept": "Electronics and Communication Engineering",
        "degree": "B.E. Electronics and Communication Engineering",
        "grad_year": 2025,
        "location": "Erode, Tamil Nadu",
        "headline": "ECE Student | Automotive CAN Bus & Embedded Microcontrollers",
        "bio": "Implementing automotive diagnostic protocols (UDS, OBD-II) on STM32 microcontrollers.",
        "skills": ["Embedded Systems", "C++", "Automotive Systems", "CAN Bus", "RTOS", "Linux"],
        "target_roles": ["Automotive Software Engineer", "Embedded Systems Developer", "Firmware Engineer"],
        "industries": ["Automotive & EV", "Embedded Systems & IoT", "Semiconductors"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Interview preparation for automotive Tier-1 suppliers (Bosch, Continental, Visteon).",
        "projects": [{"title": "Vehicle Telemetry Gateway with GPS and 4G", "desc": "STM32 microcontroller logging CAN speed and battery metrics to remote cloud server.", "tech": "Embedded C, CAN, GSM Module, AWS IoT"}]
    },
    {
        "email": "tamilselvan.k@student.alumnia.edu",
        "name": "Tamilselvan K",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Vellore, Tamil Nadu",
        "headline": "CS Student | Cloud Security & Container Hardening",
        "bio": "Focusing on Linux kernel namespaces, Docker security benchmarking, and automated static security analysis.",
        "skills": ["Cybersecurity", "Docker", "Linux", "Python", "Cloud Security", "CI/CD", "Bash"],
        "target_roles": ["Security Engineer", "DevSecOps Specialist", "Cloud Security Analyst"],
        "industries": ["Cyber Security & Defense", "Cloud & Enterprise Software", "FinTech"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Learn how security teams implement automated vulnerability remediation across cloud fleets.",
        "projects": [{"title": "Container Image Vulnerability Gatekeeper", "desc": "CI/CD security gate blocking images with Critical CVEs from deploying into production.", "tech": "Trivy, Docker, GitHub Actions, Python"}]
    },
    {
        "email": "udhayakumar.s@student.alumnia.edu",
        "name": "Udhayakumar S",
        "dept": "Food Technology",
        "degree": "B.Tech Food Technology",
        "grad_year": 2025,
        "location": "Dindigul, Tamil Nadu",
        "headline": "Food Tech Student | Supply Chain Cold-Chain Monitoring & Sensory Science",
        "bio": "Investigating IoT temperature-tracking tags and non-destructive quality evaluation of agricultural produce.",
        "skills": ["Food Technology", "Quality Assurance", "Data Analytics", "Supply Chain", "Python"],
        "target_roles": ["Food Quality Specialist", "Supply Chain Analyst", "Food Process Engineer"],
        "industries": ["FMCG & Food Processing", "Agriculture & Food", "Logistics Tech"],
        "locations": ["Chennai, Tamil Nadu", "Madurai, Tamil Nadu", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Advice on quality auditing and supply chain tech in large food brands.",
        "projects": [{"title": "Cold-Chain Temperature Excursion Alert System", "desc": "BLE sensor tags logging refrigerated transport container temperatures in transit.", "tech": "IoT Sensors, Python, Data Logging"}]
    },
    {
        "email": "varun.prasad.r@student.alumnia.edu",
        "name": "Varun Prasad R",
        "dept": "Artificial Intelligence and Data Science",
        "degree": "B.Tech Artificial Intelligence and Data Science",
        "grad_year": 2026,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "AI & DS Student | Reinforcement Learning & Autonomous Agents",
        "bio": "Exploring Q-learning, Proximal Policy Optimization (PPO), and multi-agent coordination in simulated environments.",
        "skills": ["Python", "Reinforcement Learning", "PyTorch", "Machine Learning", "Data Science", "C++"],
        "target_roles": ["Reinforcement Learning Scientist", "AI Engineer", "Robotics Software Developer"],
        "industries": ["Artificial Intelligence", "Autonomous Systems", "Gaming & Simulation"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu", "Remote"],
        "mentorship_goals": "Learn about practical industry deployments of reinforcement learning beyond robotics.",
        "projects": [{"title": "Autonomous Drone Obstacle Avoidance via PPO", "desc": "Trained simulated quadcopter policy navigating cluttered obstacle courses with zero collisions.", "tech": "PyTorch, Gym, Python, NumPy"}]
    },
    {
        "email": "yamini.devi.s@student.alumnia.edu",
        "name": "Yamini Devi S",
        "dept": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "CS Student | Enterprise Java & Cloud Microservices",
        "bio": "Passionate about building scalable e-commerce and banking backends with Java, Spring Boot, and PostgreSQL.",
        "skills": ["Java", "Spring Boot", "SQL", "PostgreSQL", "REST APIs", "Docker", "Git"],
        "target_roles": ["Software Engineer", "Backend Developer", "Cloud Application Engineer"],
        "industries": ["FinTech", "Banking & Financial Services", "E-Commerce"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Learn how enterprise banking platforms ensure ACID compliance across microservices.",
        "projects": [{"title": "Core Banking Transaction Ledger", "desc": "Double-entry bookkeeping accounting service with distributed transaction locking.", "tech": "Java, Spring Boot, PostgreSQL, Docker"}]
    }
]

STUDENT_SPECS.extend(NEW_STUDENT_SPECS)

# -------------------------------------------------------------
# 50 ALUMNI PROFILES SPECIFICATIONS
# -------------------------------------------------------------
ALUMNI_SPECS = [
    # Top 10 Existing Mentors (Retained and enhanced)
    {
        "email": "deepa.subramanian@alumni.edu",
        "name": "Deepa Subramanian",
        "title": "Senior Machine Learning Engineer",
        "company": "Google",
        "industry": "Artificial Intelligence",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2021,
        "years": 5,
        "location": "Bengaluru, Karnataka",
        "headline": "Senior ML Engineer at Google | Large Language Models & Deep Learning",
        "bio": "Alumna (Class of 2021). Currently building next-generation multimodal AI capabilities at Google. Enthusiastic about guiding Tamil Nadu students through machine learning interviews and research pathways.",
        "skills": ["Python", "PyTorch", "TensorFlow", "Machine Learning", "Distributed Systems", "Cloud Architecture", "Docker", "Deep Learning"],
        "mentor": True,
        "topics": ["FAANG Interview Prep", "Transition into AI/ML", "Graduate School Selection", "Deep Learning Architectures"],
        "experience": [
            {"title": "Senior ML Engineer", "company": "Google", "start": "2023-01", "is_current": True, "desc": "Scaling transformer infrastructure and high-throughput vector indexing systems."},
            {"title": "Machine Learning Engineer", "company": "Google", "start": "2021-08", "end": "2022-12", "desc": "Built deep ranking pipelines for semantic query understanding."}
        ]
    },
    {
        "email": "vignesh.balasubramanian@alumni.edu",
        "name": "Vignesh Balasubramanian",
        "title": "Staff Software Architect",
        "company": "Stripe",
        "industry": "FinTech",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2019,
        "years": 7,
        "location": "Chennai, Tamil Nadu",
        "headline": "Staff Software Architect at Stripe | Global Payments & Distributed Web",
        "bio": "Alumnus (Class of 2019). Leading front-end and resilient API architecture for financial infrastructure. Passionate about developer tooling, design systems, and startup engineering culture.",
        "skills": ["TypeScript", "React", "Node.js", "FastAPI", "PostgreSQL", "System Design", "GraphQL", "Java"],
        "mentor": True,
        "topics": ["Full-Stack Architecture", "System Design Interviews", "FinTech Trends", "Startup Engineering"],
        "experience": [
            {"title": "Staff Software Architect", "company": "Stripe", "start": "2022-03", "is_current": True, "desc": "Overseeing checkout experience handling millions of global transactions."},
            {"title": "Senior Software Engineer", "company": "Uber", "start": "2019-07", "end": "2022-02", "desc": "Built real-time dispatcher portals with React and WebSockets."}
        ]
    },
    {
        "email": "ananya.jayaram@alumni.edu",
        "name": "Ananya Jayaram",
        "title": "Senior Product Manager",
        "company": "Microsoft",
        "industry": "Cloud & Enterprise Software",
        "department": "Information Systems",
        "degree": "M.S. Information Systems",
        "grad_year": 2018,
        "years": 8,
        "location": "Bengaluru, Karnataka",
        "headline": "Senior Product Manager at Microsoft Azure | Developer Experience & Cloud SDKs",
        "bio": "Product leader with 8 years of cloud experience. Passionate about mentoring students transitioning from software development into technical product management.",
        "skills": ["Product Strategy", "Product Management", "Agile", "UI/UX Design", "Data Analytics", "Cloud Architecture", "SQL"],
        "mentor": True,
        "topics": ["Product Management Pivot", "Resume Reviews", "Cross-Functional Leadership", "Customer Discovery"],
        "experience": [
            {"title": "Senior Product Manager", "company": "Microsoft", "start": "2021-05", "is_current": True, "desc": "Directing roadmap for Azure Cloud developer telemetry and client libraries."}
        ]
    },
    {
        "email": "aravind.senthilkumar@alumni.edu",
        "name": "Aravind Senthilkumar",
        "title": "Quantitative Strategist",
        "company": "Goldman Sachs",
        "industry": "FinTech",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science & Mathematics",
        "grad_year": 2022,
        "years": 4,
        "location": "Bengaluru, Karnataka",
        "headline": "Quantitative Strategist at Goldman Sachs | Algorithmic Trading Systems",
        "bio": "Class of 2022 alumnus. Working at the intersection of high-frequency market mechanics, stochastic modeling, and low-latency C++ / Python architectures.",
        "skills": ["Python", "C++", "Quantitative Finance", "Machine Learning", "Algorithmic Trading", "SQL", "Algorithms"],
        "mentor": True,
        "topics": ["Quantitative Finance Careers", "Math & Coding Prep", "Algorithmic Systems", "Financial Markets"],
        "experience": [
            {"title": "Quantitative Strategist", "company": "Goldman Sachs", "start": "2022-07", "is_current": True, "desc": "Developing statistical arbitrage models for systematic equities trading."}
        ]
    },
    {
        "email": "selvi.shanmugam@alumni.edu",
        "name": "Selvi Shanmugam",
        "title": "Staff Cloud Security Architect",
        "company": "Amazon AWS",
        "industry": "Cyber Security & Defense",
        "department": "Electrical and Electronics Engineering",
        "degree": "B.Tech Electrical & Computer Engineering",
        "grad_year": 2017,
        "years": 9,
        "location": "Chennai, Tamil Nadu",
        "headline": "Staff Security Architect at AWS | Zero-Trust Infrastructure & Cloud Defense",
        "bio": "Alumna (Class of 2017). Defending hyperscale cloud infrastructure. Enjoys speaking to students on cloud certifications, cybersecurity defense, and building enterprise resilience.",
        "skills": ["AWS", "Kubernetes", "Cybersecurity", "Cloud Security", "Docker", "Go", "Python", "Linux"],
        "mentor": True,
        "topics": ["Cloud Certifications", "Cybersecurity Pathways", "Enterprise Architecture", "DevSecOps"],
        "experience": [
            {"title": "Staff Security Architect", "company": "Amazon AWS", "start": "2020-02", "is_current": True, "desc": "Hardening multi-tenant virtualization layers and automated threat detection."}
        ]
    },
    {
        "email": "sivakumar.natarajan@alumni.edu",
        "name": "Sivakumar Natarajan",
        "title": "Founder & CEO",
        "company": "NeuroFlow Systems",
        "industry": "Artificial Intelligence",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2016,
        "years": 10,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Founder & CEO at NeuroFlow Systems | Techstars Alum",
        "bio": "2016 graduate from Coimbatore. Built an enterprise AI automation company from college campus to Series B. Dedicated to helping ambitious student founders launch real ventures.",
        "skills": ["Entrepreneurship", "PyTorch", "Python", "Machine Learning", "System Design", "Product Strategy", "Leadership"],
        "mentor": True,
        "topics": ["Student Startups", "Fundraising & Pitching", "Product-Market Fit", "Tech Leadership"],
        "experience": [
            {"title": "Founder & CEO", "company": "NeuroFlow Systems", "start": "2018-09", "is_current": True, "desc": "Leading a 45-person generative AI engineering team."}
        ]
    },
    {
        "email": "soundarya.muralidharan@alumni.edu",
        "name": "Soundarya Muralidharan",
        "title": "Senior Data Scientist",
        "company": "Netflix",
        "industry": "Artificial Intelligence",
        "department": "Artificial Intelligence and Data Science",
        "degree": "B.Tech AI & Data Science",
        "grad_year": 2020,
        "years": 6,
        "location": "Bengaluru, Karnataka",
        "headline": "Senior Data Scientist at Netflix | Personalization Algorithms & A/B Testing",
        "bio": "Class of 2020. Developing core recommendation and personal preference models for global streaming members.",
        "skills": ["Python", "SQL", "Machine Learning", "Data Science", "A/B Testing", "FastAPI", "Pandas"],
        "mentor": True,
        "topics": ["Recommendation Engine Design", "Portfolio Building", "Data Science Interviews", "A/B Testing"],
        "experience": [
            {"title": "Senior Data Scientist", "company": "Netflix", "start": "2022-08", "is_current": True, "desc": "Designing personalized ranking pipelines and offline experimentation suites."}
        ]
    },
    {
        "email": "senthil.nathan@alumni.edu",
        "name": "Senthil Nathan",
        "title": "Site Reliability Engineering Manager",
        "company": "Datadog",
        "industry": "Cloud & Enterprise Software",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Engineering",
        "grad_year": 2015,
        "years": 11,
        "location": "Chennai, Tamil Nadu",
        "headline": "SRE Manager at Datadog | Observability, High Availability, Kubernetes",
        "bio": "Experienced reliability engineering manager. Focusing on cloud observability, multi-region incident management, and automated chaos engineering.",
        "skills": ["Kubernetes", "Docker", "Linux", "Terraform", "CI/CD", "Go", "Python", "AWS"],
        "mentor": False,
        "topics": ["DevOps Culture", "Incident Response", "Site Reliability"],
        "experience": [
            {"title": "SRE Manager", "company": "Datadog", "start": "2020-01", "is_current": True, "desc": "Managing team responsible for 99.995% uptime of global ingestion clusters."}
        ]
    },
    {
        "email": "nithya.rajasekaran@alumni.edu",
        "name": "Nithya Rajasekaran",
        "title": "Bioinformatics AI Specialist",
        "company": "Genentech",
        "industry": "Healthcare & MedTech",
        "department": "Biotechnology",
        "degree": "B.Tech Biotechnology & CS",
        "grad_year": 2020,
        "years": 6,
        "location": "Chennai, Tamil Nadu",
        "headline": "AI Computational Biologist at Genentech | Protein Modeling & Deep Learning",
        "bio": "Class of 2020. Applying graph neural networks and generative chemistry models to oncology drug discovery.",
        "skills": ["Python", "PyTorch", "Machine Learning", "Bioinformatics", "Data Science", "Docker"],
        "mentor": True,
        "topics": ["Biotech AI Careers", "Interdisciplinary Research", "Computational Biology"],
        "experience": [
            {"title": "AI Computational Biologist", "company": "Genentech", "start": "2021-01", "is_current": True, "desc": "Training geometric deep learning models for molecular affinity prediction."}
        ]
    },
    {
        "email": "kavin.vijayakumar@alumni.edu",
        "name": "Kavin Vijayakumar",
        "title": "VP of Autonomous Engineering",
        "company": "NextGen Mobility",
        "industry": "Automotive & EV",
        "department": "Mechatronics Engineering",
        "degree": "B.E. Mechatronics Engineering",
        "grad_year": 2014,
        "years": 12,
        "location": "Hosur, Tamil Nadu",
        "headline": "VP of Autonomous Engineering at NextGen | Robotics, Sensor Fusion & SLAM",
        "bio": "2014 alumnus. Leading hardware and perception software development for autonomous industrial transport robots.",
        "skills": ["C++", "Python", "Robotics", "Embedded Systems", "Computer Vision", "ROS", "Control Systems"],
        "mentor": True,
        "topics": ["Robotics Careers", "Executive Leadership", "Patents and Hardware", "Autonomous Vehicles"],
        "experience": [
            {"title": "VP of Autonomous Engineering", "company": "NextGen Mobility", "start": "2019-06", "is_current": True, "desc": "Directing perception and motion planning divisions."}
        ]
    },
    # 11 - 20
    {
        "email": "arun.prakash@alumni.alumnia.edu",
        "name": "Arun Prakash",
        "title": "Principal Architect",
        "company": "Zoho Corporation",
        "industry": "Cloud & Enterprise Software",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2013,
        "years": 13,
        "location": "Chennai, Tamil Nadu",
        "headline": "Principal Architect at Zoho | SaaS Infrastructure & Distributed Databases",
        "bio": "Alumnus (Class of 2013). Leading scalable cloud storage and database partitioning engines for millions of enterprise users worldwide. Eager to mentor students on systems engineering.",
        "skills": ["Java", "C++", "PostgreSQL", "System Design", "Linux", "Distributed Systems", "Cloud Architecture"],
        "mentor": True,
        "topics": ["Distributed Systems", "Core Engineering Careers", "SaaS Architecture"],
        "experience": [{"title": "Principal Architect", "company": "Zoho Corporation", "start": "2018-04", "is_current": True, "desc": "Designing high-scale database query routing layers."}]
    },
    {
        "email": "priya.balaji@alumni.alumnia.edu",
        "name": "Priya Balaji",
        "title": "Director of Product Management",
        "company": "Freshworks",
        "industry": "Cloud & Enterprise Software",
        "department": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2015,
        "years": 11,
        "location": "Chennai, Tamil Nadu",
        "headline": "Director of Product at Freshworks | Customer Experience SaaS",
        "bio": "Passionate about building intuitive enterprise software. Mentored over 50 female engineers in Tamil Nadu into product and design leadership roles.",
        "skills": ["Product Management", "UI/UX Design", "Agile", "Business Analysis", "Leadership", "Data Analytics"],
        "mentor": True,
        "topics": ["Women in Tech", "Product Roadmaps", "Transition to Product"],
        "experience": [{"title": "Director of Product", "company": "Freshworks", "start": "2020-08", "is_current": True, "desc": "Leading product roadmap for customer engagement suites."}]
    },
    {
        "email": "suresh.kumar.n@alumni.alumnia.edu",
        "name": "Suresh Kumar N",
        "title": "Senior Embedded Firmware Lead",
        "company": "Bosch India",
        "industry": "Automotive & EV",
        "department": "Electronics and Communication Engineering",
        "degree": "B.E. Electronics and Communication Engineering",
        "grad_year": 2016,
        "years": 10,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Firmware Lead at Bosch | Automotive ECU & Functional Safety",
        "bio": "Class of 2016 alumnus. Developing ISO 26262 compliant powertrain software for electric and hybrid vehicles.",
        "skills": ["Embedded Systems", "C++", "RTOS", "Automotive Systems", "CAN Bus", "IoT"],
        "mentor": True,
        "topics": ["Automotive Embedded Careers", "CAN Protocol", "Functional Safety"],
        "experience": [{"title": "Firmware Lead", "company": "Bosch India", "start": "2019-11", "is_current": True, "desc": "Designing battery control modules for electric two-wheelers."}]
    },
    {
        "email": "divya.raman@alumni.alumnia.edu",
        "name": "Divya Raman",
        "title": "Lead Generative AI Engineer",
        "company": "Cognizant AI Labs",
        "industry": "Artificial Intelligence",
        "department": "Artificial Intelligence and Data Science",
        "degree": "B.Tech AI and Data Science",
        "grad_year": 2021,
        "years": 5,
        "location": "Chennai, Tamil Nadu",
        "headline": "Lead GenAI Engineer at Cognizant | Enterprise LLMs & Agentic RAG",
        "bio": "Class of 2021 graduate. Building production agentic workflows and fine-tuned open-source models for enterprise automation.",
        "skills": ["Generative AI", "Python", "RAG", "LangChain", "Prompt Engineering", "PyTorch", "Machine Learning"],
        "mentor": True,
        "topics": ["Generative AI Careers", "Building Enterprise Agents", "Fine-Tuning Models"],
        "experience": [{"title": "Lead GenAI Engineer", "company": "Cognizant AI Labs", "start": "2023-02", "is_current": True, "desc": "Deploying RAG pipelines for Fortune 500 financial clients."}]
    },
    {
        "email": "ashwin.raj.s@alumni.alumnia.edu",
        "name": "Ashwin Raj S",
        "title": "Senior DevOps Engineer",
        "company": "Swiggy",
        "industry": "Cloud & Enterprise Software",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2018,
        "years": 8,
        "location": "Bengaluru, Karnataka",
        "headline": "Senior DevOps Engineer at Swiggy | High-Scale Kubernetes & Cloud Ops",
        "bio": "Managing Kubernetes clusters orchestrating thousands of microservices handling millions of hungry customer deliveries every weekend.",
        "skills": ["Kubernetes", "AWS", "Docker", "CI/CD", "Linux", "Terraform", "Python", "Go"],
        "mentor": True,
        "topics": ["DevOps Culture", "Scale Engineering", "Cloud Resiliency"],
        "experience": [{"title": "Senior DevOps Engineer", "company": "Swiggy", "start": "2021-03", "is_current": True, "desc": "Reduced deployment failure rate by 65% using canary rollouts."}]
    },
    {
        "email": "naveen.kumar.r@alumni.alumnia.edu",
        "name": "Naveen Kumar R",
        "title": "Lead Cybersecurity Consultant",
        "company": "TCS Cyber Defense",
        "industry": "Cyber Security & Defense",
        "department": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2017,
        "years": 9,
        "location": "Chennai, Tamil Nadu",
        "headline": "Lead Security Consultant at TCS | Threat Hunting & Incident Response",
        "bio": "Alumnus (Class of 2017). Defending enterprise networks across APAC and Europe. Passionate about ethical hacking and guiding students into defensive cyber operations.",
        "skills": ["Cybersecurity", "Network Security", "Ethical Security Testing", "Cloud Security", "Linux", "Python"],
        "mentor": True,
        "topics": ["Cybersecurity Roadmap", "Defensive Operations", "Security Certifications"],
        "experience": [{"title": "Lead Security Consultant", "company": "TCS", "start": "2020-04", "is_current": True, "desc": "Heading 24/7 Threat Hunting cell for global banking clients."}]
    },
    {
        "email": "ramya.krishnan@alumni.alumnia.edu",
        "name": "Ramya Krishnan",
        "title": "Senior Frontend Architect",
        "company": "Flipkart",
        "industry": "Cloud & Enterprise Software",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2019,
        "years": 7,
        "location": "Bengaluru, Karnataka",
        "headline": "Senior Frontend Architect at Flipkart | Web Performance & React",
        "bio": "Optimizing web vitals, progressive web apps, and ultra-fast client rendering for Big Billion Days.",
        "skills": ["React", "TypeScript", "JavaScript", "HTML/CSS", "Next.js", "Tailwind CSS", "UI/UX Design"],
        "mentor": True,
        "topics": ["Frontend Interviews", "Web Performance Optimization", "Design Systems"],
        "experience": [{"title": "Senior Frontend Architect", "company": "Flipkart", "start": "2021-06", "is_current": True, "desc": "Reduced mobile web First Contentful Paint by 400ms."}]
    },
    {
        "email": "balaji.shankar@alumni.alumnia.edu",
        "name": "Balaji Shankar",
        "title": "Principal Hardware Engineer",
        "company": "Qualcomm India",
        "industry": "Semiconductors",
        "department": "Electronics and Communication Engineering",
        "degree": "B.E. Electronics and Communication Engineering",
        "grad_year": 2015,
        "years": 11,
        "location": "Chennai, Tamil Nadu",
        "headline": "Principal Hardware Engineer at Qualcomm | 5G Modems & VLSI Architecture",
        "bio": "Alumnus (Class of 2015). Designing energy-efficient digital signal processors for Snapdragon mobile platforms.",
        "skills": ["VLSI", "Verilog", "FPGA", "Embedded Systems", "C++", "Digital Electronics"],
        "mentor": True,
        "topics": ["VLSI Careers", "Semiconductor Industry Realities", "Core Hardware Interviews"],
        "experience": [{"title": "Principal Hardware Engineer", "company": "Qualcomm", "start": "2019-01", "is_current": True, "desc": "Leading digital verification for sub-6GHz 5G baseband cores."}]
    },
    {
        "email": "swetha.lakshmi.m@alumni.alumnia.edu",
        "name": "Swetha Lakshmi M",
        "title": "Senior Full-Stack Engineer",
        "company": "PayPal India",
        "industry": "FinTech",
        "department": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2020,
        "years": 6,
        "location": "Chennai, Tamil Nadu",
        "headline": "Senior Full-Stack Engineer at PayPal | Node.js, React, Distributed Payments",
        "bio": "Building reliable cross-border checkout experiences and anti-fraud verification workflows.",
        "skills": ["Node.js", "React", "TypeScript", "SQL", "PostgreSQL", "REST APIs", "Docker", "Java"],
        "mentor": True,
        "topics": ["FinTech Engineering", "Full-Stack Interview Prep", "Clean Code"],
        "experience": [{"title": "Senior Software Engineer", "company": "PayPal", "start": "2022-09", "is_current": True, "desc": "Developing real-time payment authentication microservices."}]
    },
    {
        "email": "karthikeyan.murugesan@alumni.alumnia.edu",
        "name": "Karthikeyan Murugesan",
        "title": "Battery Systems Chief Engineer",
        "company": "Ather Energy",
        "industry": "Automotive & EV",
        "department": "Mechanical Engineering",
        "degree": "B.E. Mechanical Engineering",
        "grad_year": 2015,
        "years": 11,
        "location": "Hosur, Tamil Nadu",
        "headline": "Chief Battery Engineer at Ather | EV Pack Design & Thermal Safety",
        "bio": "Class of 2015. Leading mechanical architecture and thermal cooling jackets for smart electric scooters.",
        "skills": ["Automotive Systems", "SolidWorks", "ANSYS", "Finite Element Analysis", "Manufacturing", "Thermal Analysis"],
        "mentor": True,
        "topics": ["EV Industry Career Growth", "Mechanical Design for Electric Vehicles", "Patenting"],
        "experience": [{"title": "Chief Battery Engineer", "company": "Ather Energy", "start": "2019-05", "is_current": True, "desc": "Designed IP67 rated lithium battery enclosure withstand testing."}]
    },
    # 21 - 30
    {
        "email": "revathi.govindaraj@alumni.alumnia.edu",
        "name": "Revathi Govindaraj",
        "title": "Principal Data Architect",
        "company": "Amazon",
        "industry": "Cloud & Enterprise Software",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2014,
        "years": 12,
        "location": "Chennai, Tamil Nadu",
        "headline": "Principal Data Architect at Amazon | Exabyte-Scale Data Lakes",
        "bio": "Architecting big data pipelines, streaming Kafka ingestions, and real-time analytical warehouses for global retail operations.",
        "skills": ["AWS", "SQL", "Python", "Data Science", "PostgreSQL", "Distributed Systems", "Cloud Architecture"],
        "mentor": True,
        "topics": ["Data Engineering at Scale", "Big Data Architecture", "Amazon Leadership Principles"],
        "experience": [{"title": "Principal Data Architect", "company": "Amazon", "start": "2018-09", "is_current": True, "desc": "Directing AWS data ingestion pipelines processing 40TB daily."}]
    },
    {
        "email": "saravanan.palanisamy@alumni.alumnia.edu",
        "name": "Saravanan Palanisamy",
        "title": "VP of Engineering",
        "company": "Vakilsearch (Zolvit)",
        "industry": "Cloud & Enterprise Software",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2012,
        "years": 14,
        "location": "Chennai, Tamil Nadu",
        "headline": "VP of Engineering at Zolvit | LegalTech Scaling & Cloud Native",
        "bio": "Alumnus (Class of 2012). Leading engineering teams building legal and compliance platforms for 500,000+ Indian businesses.",
        "skills": ["Leadership", "System Design", "Node.js", "React", "Cloud Architecture", "Python", "Entrepreneurship"],
        "mentor": True,
        "topics": ["Engineering Leadership", "Scaling Startups in India", "Full-Stack Strategy"],
        "experience": [{"title": "VP of Engineering", "company": "Zolvit", "start": "2019-03", "is_current": True, "desc": "Scaling engineering organization from 20 to 120 engineers."}]
    },
    {
        "email": "kavitha.sundaram@alumni.alumnia.edu",
        "name": "Kavitha Sundaram",
        "title": "Lead Clinical Data Analyst",
        "company": "Apollo Hospitals Group",
        "industry": "Healthcare & MedTech",
        "department": "Biomedical Engineering",
        "degree": "B.E. Biomedical Engineering",
        "grad_year": 2017,
        "years": 9,
        "location": "Chennai, Tamil Nadu",
        "headline": "Lead Clinical Data Analyst at Apollo | Healthcare Analytics & Patient Outcomes",
        "bio": "Class of 2017 alumna. Bridging biomedical sensor data with hospital analytics to improve post-operative patient survival rates.",
        "skills": ["Biomedical Engineering", "Data Analytics", "SQL", "Python", "Healthcare AI", "Power BI"],
        "mentor": True,
        "topics": ["Health Informatics", "Biomedical Engineering Careers", "Clinical Data Analysis"],
        "experience": [{"title": "Lead Clinical Analyst", "company": "Apollo Hospitals", "start": "2020-07", "is_current": True, "desc": "Implemented predictive ICU sepsis deterioration alerts."}]
    },
    {
        "email": "venkatesh.raghavan@alumni.alumnia.edu",
        "name": "Venkatesh Raghavan",
        "title": "Senior Solutions Architect",
        "company": "Google Cloud",
        "industry": "Cloud & Enterprise Software",
        "department": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2016,
        "years": 10,
        "location": "Bengaluru, Karnataka",
        "headline": "Senior Solutions Architect at Google Cloud | Hybrid Cloud & AI Infrastructure",
        "bio": "Helping enterprise enterprises modernize monolithic architectures into containerized, autoscaling cloud native systems on GCP.",
        "skills": ["Google Cloud", "Kubernetes", "Cloud Architecture", "System Design", "Docker", "Terraform", "Python"],
        "mentor": True,
        "topics": ["Cloud Architecture Certifications", "GCP Career Pathways", "Enterprise Cloud Strategy"],
        "experience": [{"title": "Senior Solutions Architect", "company": "Google Cloud", "start": "2021-02", "is_current": True, "desc": "Architected cloud migrations for prominent APAC banking institutions."}]
    },
    {
        "email": "sandhya.srinivasan@alumni.alumnia.edu",
        "name": "Sandhya Srinivasan",
        "title": "Senior Robotics Perception Engineer",
        "company": "GreyOrange",
        "industry": "Industrial Automation & Robotics",
        "department": "Mechatronics Engineering",
        "degree": "B.E. Mechatronics Engineering",
        "grad_year": 2019,
        "years": 7,
        "location": "Chennai, Tamil Nadu",
        "headline": "Perception Engineer at GreyOrange | 3D Vision & Mobile Robotics",
        "bio": "Developing obstacle perception and real-time visual SLAM algorithms for automated warehouse picking robots.",
        "skills": ["Robotics", "ROS", "Computer Vision", "C++", "Python", "Deep Learning", "Embedded Systems"],
        "mentor": True,
        "topics": ["Robotics Perception", "Computer Vision for Automation", "ROS2 Engineering"],
        "experience": [{"title": "Senior Perception Engineer", "company": "GreyOrange", "start": "2022-01", "is_current": True, "desc": "Implemented 3D depth camera obstacle classification on warehouse AMRs."}]
    },
    {
        "email": "prakash.natarajan@alumni.alumnia.edu",
        "name": "Prakash Natarajan",
        "title": "Chief Structural Consultant",
        "company": "L&T Construction",
        "industry": "Infrastructure & Construction",
        "department": "Civil Engineering",
        "degree": "B.E. Civil Engineering",
        "grad_year": 2013,
        "years": 13,
        "location": "Chennai, Tamil Nadu",
        "headline": "Chief Structural Consultant at L&T | Metro Rail & Bridge Infrastructure",
        "bio": "Alumnus (Class of 2013). Supervised prestressed concrete elevated viaduct designs for metro rail projects in Tamil Nadu and Karnataka.",
        "skills": ["Civil Engineering", "Structural Analysis", "AutoCAD", "ETABS", "Project Management", "BIM"],
        "mentor": True,
        "topics": ["Structural Engineering Career Growth", "Mega Infrastructure Projects", "Site Management"],
        "experience": [{"title": "Chief Structural Consultant", "company": "L&T Construction", "start": "2017-06", "is_current": True, "desc": "Senior design lead for 14km elevated metro viaduct stretch."}]
    },
    {
        "email": "gayathri.subramanian@alumni.alumnia.edu",
        "name": "Gayathri Subramanian",
        "title": "Staff Quantitative Researcher",
        "company": "Morgan Stanley",
        "industry": "FinTech",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2017,
        "years": 9,
        "location": "Bengaluru, Karnataka",
        "headline": "Staff Quantitative Researcher at Morgan Stanley | Risk Modeling & Derivatives",
        "bio": "Developing Monte Carlo valuation and multi-factor equity risk models. Class of 2017 graduate.",
        "skills": ["Quantitative Finance", "Python", "C++", "SQL", "Machine Learning", "Data Analytics"],
        "mentor": True,
        "topics": ["Quantitative Modeling", "Investment Banking Tech", "Risk Management"],
        "experience": [{"title": "Staff Quantitative Researcher", "company": "Morgan Stanley", "start": "2020-03", "is_current": True, "desc": "Modeled portfolio value-at-risk for global fixed-income portfolios."}]
    },
    {
        "email": "muthukumar.s@alumni.alumnia.edu",
        "name": "Muthukumar S",
        "title": "Plant Automation General Manager",
        "company": "Tata Steel",
        "industry": "Industrial Automation & Robotics",
        "department": "Electrical and Electronics Engineering",
        "degree": "B.E. Electrical and Electronics Engineering",
        "grad_year": 2012,
        "years": 14,
        "location": "Salem, Tamil Nadu",
        "headline": "Automation General Manager at Tata Steel | Blast Furnace SCADA Systems",
        "bio": "2012 alumnus. Directing digital transformation and industrial automation for high-temperature blast furnaces and rolling mills.",
        "skills": ["PLC Programming", "SCADA", "Industrial Automation", "Control Systems", "Electrical Engineering", "Leadership"],
        "mentor": True,
        "topics": ["Core Industry Automation", "Heavy Engineering", "Leadership in Manufacturing"],
        "experience": [{"title": "General Manager Automation", "company": "Tata Steel", "start": "2018-01", "is_current": True, "desc": "Implemented centralized SCADA control for continuous casting shop."}]
    },
    {
        "email": "preethi.venkataraman@alumni.alumnia.edu",
        "name": "Preethi Venkataraman",
        "title": "Staff AI Ethics Researcher",
        "company": "IBM Research",
        "industry": "Artificial Intelligence",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2018,
        "years": 8,
        "location": "Bengaluru, Karnataka",
        "headline": "Staff AI Ethics Researcher at IBM | Model Transparency & Bias Auditing",
        "bio": "Published researcher focusing on explainable AI tools (AI Explainability 360), algorithmic accountability, and regulatory compliance.",
        "skills": ["Explainable AI", "Python", "Machine Learning", "Data Science", "Research", "NLP"],
        "mentor": True,
        "topics": ["AI Governance", "Research Publications", "Ethical AI Development"],
        "experience": [{"title": "Staff Researcher", "company": "IBM Research", "start": "2021-08", "is_current": True, "desc": "Co-authored patents on automated model fairness verification."}]
    },
    {
        "email": "sridhar.ramasamy@alumni.alumnia.edu",
        "name": "Sridhar Ramasamy",
        "title": "Chief Information Security Officer",
        "company": "Kallol FinTech",
        "industry": "Cyber Security & Defense",
        "department": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2013,
        "years": 13,
        "location": "Chennai, Tamil Nadu",
        "headline": "CISO at Kallol FinTech | Financial Threat Defense & ISO 27001",
        "bio": "Alumnus (Class of 2013). Directing corporate cybersecurity, threat governance, and RBI regulatory data compliance.",
        "skills": ["Cybersecurity", "Cloud Security", "Leadership", "Network Security", "Ethical Security Testing"],
        "mentor": True,
        "topics": ["Cybersecurity Leadership", "Financial Regulations", "CISO Career Path"],
        "experience": [{"title": "CISO", "company": "Kallol FinTech", "start": "2020-01", "is_current": True, "desc": "Achieved zero security breach incidents across 5 million account holders."}]
    },
    # 31 - 40
    {
        "email": "vidhya.chandrasekaran@alumni.alumnia.edu",
        "name": "Vidhya Chandrasekaran",
        "title": "Senior Staff Bioprocess Specialist",
        "company": "Biocon",
        "industry": "Healthcare & MedTech",
        "department": "Biotechnology",
        "degree": "B.Tech Biotechnology",
        "grad_year": 2016,
        "years": 10,
        "location": "Bengaluru, Karnataka",
        "headline": "Bioprocess Specialist at Biocon | Biosimilars & Fermentation Scale-Up",
        "bio": "Leading downstream chromatography purification and microbial expression scale-up for affordable insulin production.",
        "skills": ["Biotechnology", "Bioprocess Engineering", "Quality Control", "Data Analytics", "Microbiology"],
        "mentor": True,
        "topics": ["Biotech Industry Transition", "Pharmaceutical Manufacturing", "Biosimilars"],
        "experience": [{"title": "Bioprocess Specialist", "company": "Biocon", "start": "2019-04", "is_current": True, "desc": "Improved recombinant protein yield by 22% in 5000L bioreactors."}]
    },
    {
        "email": "vijay.anand.k@alumni.alumnia.edu",
        "name": "Vijay Anand K",
        "title": "Senior Automotive Telematics Architect",
        "company": "TVS Motor Company",
        "industry": "Automotive & EV",
        "department": "Electronics and Communication Engineering",
        "degree": "B.E. Electronics and Communication Engineering",
        "grad_year": 2015,
        "years": 11,
        "location": "Hosur, Tamil Nadu",
        "headline": "Telematics Architect at TVS Motor | Smart Connected Vehicles & Cloud IoT",
        "bio": "Alumnus (Class of 2015). Architecting connected vehicle telemetry, Bluetooth smartphone pairing, and OTA firmware updates.",
        "skills": ["Embedded Systems", "IoT", "Automotive Systems", "C++", "Python", "CAN Bus", "Cloud Architecture"],
        "mentor": True,
        "topics": ["Connected Vehicles", "Automotive IoT", "Two-Wheeler EV Innovation"],
        "experience": [{"title": "Telematics Architect", "company": "TVS Motor", "start": "2019-08", "is_current": True, "desc": "Designed SmartXonnect connected instrument cluster platform."}]
    },
    {
        "email": "shanthi.mohan@alumni.alumnia.edu",
        "name": "Shanthi Mohan",
        "title": "Principal UX Research Lead",
        "company": "Thoughtworks",
        "industry": "Cloud & Enterprise Software",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2015,
        "years": 11,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Principal UX Lead at Thoughtworks | Inclusive Design & Design Thinking",
        "bio": "Advocating for accessible, human-centered software architectures. Eager to mentor students in qualitative user research and Figma systems.",
        "skills": ["UI/UX Design", "Figma", "Product Management", "User Research", "Agile", "Design Systems"],
        "mentor": True,
        "topics": ["Design Portfolios", "User Research Methodologies", "Inclusive Design"],
        "experience": [{"title": "Principal UX Lead", "company": "Thoughtworks", "start": "2019-02", "is_current": True, "desc": "Headed enterprise digital transformation for European logistics client."}]
    },
    {
        "email": "rajasekaran.d@alumni.alumnia.edu",
        "name": "Rajasekaran D",
        "title": "Chief Process Optimization Engineer",
        "company": "Reliance Industries",
        "industry": "Petrochemicals & Energy",
        "department": "Chemical Engineering",
        "degree": "B.Tech Chemical Engineering",
        "grad_year": 2014,
        "years": 12,
        "location": "Chennai, Tamil Nadu",
        "headline": "Chief Process Engineer at Reliance | Petrochemical Refining & Energy Saving",
        "bio": "Expert in plant simulation, debottlenecking, and green hydrogen synthesis integration. Alumnus of Class of 2014.",
        "skills": ["Chemical Engineering", "Process Simulation", "Aspen Plus", "MATLAB", "Energy Optimization"],
        "mentor": True,
        "topics": ["Chemical Refining Careers", "Green Hydrogen Transition", "Plant Safety"],
        "experience": [{"title": "Chief Process Engineer", "company": "Reliance", "start": "2018-05", "is_current": True, "desc": "Saved 14 MW equivalent energy via distillation column heat integration."}]
    },
    {
        "email": "bhuvana.krishnan@alumni.alumnia.edu",
        "name": "Bhuvana Krishnan",
        "title": "Senior AI Research Scientist",
        "company": "Microsoft Research India",
        "industry": "Artificial Intelligence",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2019,
        "years": 7,
        "location": "Bengaluru, Karnataka",
        "headline": "Research Scientist at Microsoft Research | Multilingual NLP & LLM Pre-Training",
        "bio": "Working on low-resource language translation, Indic LLMs, and efficient self-attention mechanisms.",
        "skills": ["Python", "PyTorch", "NLP", "Machine Learning", "Deep Learning", "Generative AI", "Research"],
        "mentor": True,
        "topics": ["Research Careers in AI", "Paper Publications (ACL, EMNLP)", "Indic NLP"],
        "experience": [{"title": "Research Scientist", "company": "Microsoft Research", "start": "2021-10", "is_current": True, "desc": "Lead author on multilingual Indic benchmark evaluation datasets."}]
    },
    {
        "email": "anandha.kumar.p@alumni.alumnia.edu",
        "name": "Anandha Kumar P",
        "title": "Director of Cloud Infrastructure",
        "company": "Jio Platforms",
        "industry": "Telecommunications",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2013,
        "years": 13,
        "location": "Chennai, Tamil Nadu",
        "headline": "Director of Cloud Infrastructure at Jio | 5G Cloud Core & OpenStack",
        "bio": "Managing multi-datacenter private cloud orchestration supporting 400+ million subscribers.",
        "skills": ["Cloud Architecture", "Linux", "Kubernetes", "Docker", "Network Security", "System Design", "Leadership"],
        "mentor": False,
        "topics": ["Telco Cloud", "Carrier Grade Networks", "Executive Mentoring"],
        "experience": [{"title": "Director of Cloud", "company": "Jio Platforms", "start": "2019-07", "is_current": True, "desc": "Orchestrated nationwide 5G Core cloud rollout."}]
    },
    {
        "email": "menaka.devi.s@alumni.alumnia.edu",
        "name": "Menaka Devi S",
        "title": "Lead Quality Assurance Manager",
        "company": "ITC Foods Division",
        "industry": "FMCG & Food Processing",
        "department": "Food Technology",
        "degree": "B.Tech Food Technology",
        "grad_year": 2016,
        "years": 10,
        "location": "Madurai, Tamil Nadu",
        "headline": "QA Manager at ITC Foods | Food Safety Compliance & Sensory Audits",
        "bio": "Alumna (Class of 2016). Directing food safety audits, HACCP guidelines, and quality assurance testing across biscuit and confectionery facilities.",
        "skills": ["Food Technology", "Quality Assurance", "HACCP", "Supply Chain", "Leadership"],
        "mentor": True,
        "topics": ["FMCG Industry Opportunities", "Food Quality Compliance", "Auditing Skills"],
        "experience": [{"title": "QA Manager", "company": "ITC Foods", "start": "2020-03", "is_current": True, "desc": "Reduced production quality deviation by 42% across regional plants."}]
    },
    {
        "email": "senthilvelan.r@alumni.alumnia.edu",
        "name": "Senthilvelan R",
        "title": "Principal FPGA Verification Specialist",
        "company": "Texas Instruments",
        "industry": "Semiconductors",
        "department": "Electronics and Communication Engineering",
        "degree": "B.E. Electronics and Communication Engineering",
        "grad_year": 2014,
        "years": 12,
        "location": "Bengaluru, Karnataka",
        "headline": "Principal Verification Specialist at TI | UVM & SystemVerilog",
        "bio": "Class of 2014. Architecting universal verification methodology (UVM) testbenches for precision analog and mixed-signal microcontrollers.",
        "skills": ["VLSI", "SystemVerilog", "Verilog", "FPGA", "C++", "Digital Electronics"],
        "mentor": True,
        "topics": ["Semiconductor Verification", "UVM Frameworks", "ASIC Design Loops"],
        "experience": [{"title": "Principal Verification Lead", "company": "Texas Instruments", "start": "2018-06", "is_current": True, "desc": "Achieved first-pass silicon success for high-performance automotive DSP."}]
    },
    {
        "email": "geetha.ranganathan@alumni.alumnia.edu",
        "name": "Geetha Ranganathan",
        "title": "Head of People and Talent",
        "company": "Kuku FM",
        "industry": "Consumer Tech",
        "department": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2015,
        "years": 11,
        "location": "Chennai, Tamil Nadu",
        "headline": "Head of Talent at Kuku FM | Tech Recruitment & Campus Hiring",
        "bio": "Alumna (Class of 2015). Passionate about campus placement strategy, technical resume structuring, and mock behavioral interviews.",
        "skills": ["Human Resources", "Recruitment", "Communication", "Leadership", "Talent Management"],
        "mentor": True,
        "topics": ["Resume Makeover", "HR Behavioral Interviews", "Salary Negotiation for Freshers"],
        "experience": [{"title": "Head of Talent", "company": "Kuku FM", "start": "2021-04", "is_current": True, "desc": "Scaled engineering headcount from 35 to 180 engineers."}]
    },
    {
        "email": "guru.prasad.m@alumni.alumnia.edu",
        "name": "Guru Prasad M",
        "title": "Senior Site Reliability Architect",
        "company": "Paytm",
        "industry": "FinTech",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2017,
        "years": 9,
        "location": "Chennai, Tamil Nadu",
        "headline": "Senior SRE Architect at Paytm | Zero-Downtime Payment Gateways",
        "bio": "Focusing on low-latency microservices, disaster recovery, Redis clusters, and financial grade SLA maintenance.",
        "skills": ["Linux", "Kubernetes", "AWS", "Python", "Go", "Docker", "System Design"],
        "mentor": True,
        "topics": ["High Availability Systems", "SRE Interview Questions", "FinTech Reliability"],
        "experience": [{"title": "Senior SRE Architect", "company": "Paytm", "start": "2020-10", "is_current": True, "desc": "Maintained 99.999% gateway uptime during festival transaction peaks."}]
    },
    # 41 - 50
    {
        "email": "sujatha.thiagarajan@alumni.alumnia.edu",
        "name": "Sujatha Thiagarajan",
        "title": "Principal Environmental Impact Consultant",
        "company": "WSP India",
        "industry": "Infrastructure & Construction",
        "department": "Civil Engineering",
        "degree": "B.E. Civil Engineering",
        "grad_year": 2014,
        "years": 12,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Principal Environmental Consultant at WSP | Green Ratings & Smart Cities",
        "bio": "Class of 2014. Advising government and commercial builders on LEED green building certification, water conservation, and carbon neutrality.",
        "skills": ["Civil Engineering", "Environmental Engineering", "Project Management", "GIS", "Sustainability"],
        "mentor": True,
        "topics": ["Green Building Certifications", "Environmental Consulting", "Smart Infrastructure"],
        "experience": [{"title": "Principal Consultant", "company": "WSP", "start": "2018-11", "is_current": True, "desc": "Consultant on 4 Platinum LEED certified commercial tech parks."}]
    },
    {
        "email": "manikandan.chelliah@alumni.alumnia.edu",
        "name": "Manikandan Chelliah",
        "title": "Senior Medical Imaging Specialist",
        "company": "GE Healthcare",
        "industry": "Healthcare & MedTech",
        "department": "Biomedical Engineering",
        "degree": "B.E. Biomedical Engineering",
        "grad_year": 2016,
        "years": 10,
        "location": "Bengaluru, Karnataka",
        "headline": "Imaging Specialist at GE Healthcare | MRI Signal Processing & Reconstruction",
        "bio": "Alumnus (Class of 2016). Developing deep learning image reconstruction algorithms for high-field magnetic resonance scanners.",
        "skills": ["Biomedical Engineering", "Signal Processing", "Deep Learning", "Python", "C++", "Computer Vision"],
        "mentor": True,
        "topics": ["Medical Imaging Careers", "Healthcare Engineering", "MRI & CT Algorithms"],
        "experience": [{"title": "Senior Imaging Specialist", "company": "GE Healthcare", "start": "2019-09", "is_current": True, "desc": "Reduced MRI patient scan times by 35% using AI compressed sensing."}]
    },
    {
        "email": "padmavathi.r@alumni.alumnia.edu",
        "name": "Padmavathi R",
        "title": "Director of Engineering",
        "company": "Oracle India",
        "industry": "Cloud & Enterprise Software",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2012,
        "years": 14,
        "location": "Bengaluru, Karnataka",
        "headline": "Director of Engineering at Oracle | Cloud Database Autonomous Services",
        "bio": "Leading enterprise database core engineering. Passionate about women in leadership and high-concurrency systems design.",
        "skills": ["Java", "SQL", "Database Administration", "System Design", "Cloud Architecture", "Leadership"],
        "mentor": True,
        "topics": ["Database Internals", "Career Acceleration for Engineers", "Executive Strategy"],
        "experience": [{"title": "Director of Engineering", "company": "Oracle", "start": "2018-03", "is_current": True, "desc": "Overseeing 85-person database autonomous patching and telemetry team."}]
    },
    {
        "email": "thilak.raj.v@alumni.alumnia.edu",
        "name": "Thilak Raj V",
        "title": "Chief Robotics Autonomy Architect",
        "company": "Addverb Technologies",
        "industry": "Industrial Automation & Robotics",
        "department": "Mechatronics Engineering",
        "degree": "B.E. Mechatronics Engineering",
        "grad_year": 2016,
        "years": 10,
        "location": "Chennai, Tamil Nadu",
        "headline": "Robotics Architect at Addverb | Autonomous Mobile Fleet Coordination",
        "bio": "Class of 2016 alumnus. Designing centralized traffic managers and collision-free path planning for 500+ warehouse robots.",
        "skills": ["Robotics", "ROS", "C++", "Python", "Algorithms", "Control Systems"],
        "mentor": True,
        "topics": ["Fleet Robotics Systems", "Robotics Startups in India", "Motion Planning"],
        "experience": [{"title": "Autonomy Architect", "company": "Addverb", "start": "2020-04", "is_current": True, "desc": "Implemented multi-agent decentralized collision avoidance protocol."}]
    },
    {
        "email": "mahalakshmi.s@alumni.alumnia.edu",
        "name": "Mahalakshmi S",
        "title": "Senior Cyber Threat Intelligence Lead",
        "company": "CrowdStrike",
        "industry": "Cyber Security & Defense",
        "department": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2018,
        "years": 8,
        "location": "Chennai, Tamil Nadu",
        "headline": "Threat Intelligence Lead at CrowdStrike | Malware Analysis & Reverse Engineering",
        "bio": "Uncovering nation-state threat actors, reverse engineering ransomware binaries, and authoring YARA detection signatures.",
        "skills": ["Cybersecurity", "Ethical Security Testing", "Linux", "Python", "C++", "Network Security"],
        "mentor": True,
        "topics": ["Malware Analysis", "Threat Intelligence Careers", "Reverse Engineering Tips"],
        "experience": [{"title": "Threat Intel Lead", "company": "CrowdStrike", "start": "2021-07", "is_current": True, "desc": "Published detection signatures blocking prominent ransomware strains."}]
    },
    {
        "email": "jayanthi.sekar@alumni.alumnia.edu",
        "name": "Jayanthi Sekar",
        "title": "Head of Data Science",
        "company": "PolicyBazaar",
        "industry": "FinTech",
        "department": "Artificial Intelligence and Data Science",
        "degree": "B.Tech AI and Data Science",
        "grad_year": 2017,
        "years": 9,
        "location": "Bengaluru, Karnataka",
        "headline": "Head of Data Science at PolicyBazaar | InsurTech ML & Fraud Analytics",
        "bio": "Alumna (Class of 2017). Directing machine learning teams building insurance premium pricing algorithms and claims fraud detection.",
        "skills": ["Machine Learning", "Data Science", "Python", "SQL", "A/B Testing", "Leadership", "Explainable AI"],
        "mentor": True,
        "topics": ["Data Science in Insurance", "Transitioning to Management", "Fraud Analytics"],
        "experience": [{"title": "Head of Data Science", "company": "PolicyBazaar", "start": "2021-01", "is_current": True, "desc": "Reduced claims fraud by 28% using graph neural network anomaly detectors."}]
    },
    {
        "email": "raghuram.vasudevan@alumni.alumnia.edu",
        "name": "Raghuram Vasudevan",
        "title": "Staff Solar Inverter Systems Engineer",
        "company": "Schneider Electric",
        "industry": "Renewable Energy",
        "department": "Electrical and Electronics Engineering",
        "degree": "B.E. Electrical and Electronics Engineering",
        "grad_year": 2015,
        "years": 11,
        "location": "Chennai, Tamil Nadu",
        "headline": "Staff Inverter Engineer at Schneider Electric | Grid-Tie Power Electronics",
        "bio": "Designing megawatt-scale solar utility central inverters and grid-forming power electronic controls.",
        "skills": ["Power Electronics", "MATLAB", "Simulink", "PCB Design", "Electrical Engineering", "Control Systems"],
        "mentor": True,
        "topics": ["Renewable Energy Careers", "Power Electronics Design", "Grid Codes & Standards"],
        "experience": [{"title": "Staff Engineer", "company": "Schneider Electric", "start": "2019-06", "is_current": True, "desc": "Lead engineer on 1500V DC string inverter topology with 99% peak efficiency."}]
    },
    {
        "email": "archana.kannan@alumni.alumnia.edu",
        "name": "Archana Kannan",
        "title": "Senior Product Manager",
        "company": "Amazon India",
        "industry": "E-Commerce",
        "department": "Information Technology",
        "degree": "B.Tech Information Technology",
        "grad_year": 2017,
        "years": 9,
        "location": "Bengaluru, Karnataka",
        "headline": "Senior PM at Amazon | Consumer Delivery & Seller Experience",
        "bio": "Class of 2017 alumna. Championing customer experience initiatives, rural seller onboarding, and delivery optimization across South India.",
        "skills": ["Product Management", "Data Analytics", "Agile", "SQL", "Leadership", "Communication"],
        "mentor": True,
        "topics": ["Amazon PM Interviews", "Customer Backwards Strategy", "Data-Driven Decisions"],
        "experience": [{"title": "Senior Product Manager", "company": "Amazon India", "start": "2020-09", "is_current": True, "desc": "Launched automated seller inventory replenishment recommendations."}]
    },
    {
        "email": "vigneshwaran.s@alumni.alumnia.edu",
        "name": "Vigneshwaran S",
        "title": "Senior Cloud Infrastructure Lead",
        "company": "Cisco Systems",
        "industry": "Telecommunications",
        "department": "Computer Science and Engineering",
        "degree": "B.Tech Computer Science and Engineering",
        "grad_year": 2016,
        "years": 10,
        "location": "Chennai, Tamil Nadu",
        "headline": "Cloud Infrastructure Lead at Cisco | Software-Defined Networking & Edge",
        "bio": "Alumnus (Class of 2016). Specializing in SDN controllers, enterprise network telemetry, and multi-tenant edge compute nodes.",
        "skills": ["Network Security", "Linux", "Python", "Kubernetes", "AWS", "Docker", "System Design"],
        "mentor": True,
        "topics": ["Enterprise Networking", "Cisco Engineering Roles", "SDN Architecture"],
        "experience": [{"title": "Cloud Lead", "company": "Cisco Systems", "start": "2019-12", "is_current": True, "desc": "Architected zero-touch provisioning for edge SD-WAN routers."}]
    },
    {
        "email": "dr.meenakshi.sundaram@alumni.alumnia.edu",
        "name": "Dr. Meenakshi Sundaram V",
        "title": "Chief Scientific Officer",
        "company": "Tamil Nadu AI Research Consortium",
        "industry": "Artificial Intelligence",
        "department": "Computer Science and Engineering",
        "degree": "Ph.D. Computer Science & AI",
        "grad_year": 2010,
        "years": 16,
        "location": "Chennai, Tamil Nadu",
        "headline": "CSO at TN AI Research Consortium | Deep Learning & State Innovation",
        "bio": "Distinguished alumnus (Class of 2010). Mentoring academic engineering faculty and student innovators across Tamil Nadu higher education institutions.",
        "skills": ["Machine Learning", "Artificial Intelligence", "Deep Learning", "Leadership", "Research", "Python"],
        "mentor": True,
        "topics": ["Higher Education & Research", "Academic-Industry Grants", "Statewide Innovation"],
        "experience": [{"title": "Chief Scientific Officer", "company": "TN AI Research Consortium", "start": "2017-01", "is_current": True, "desc": "Facilitated over 40 applied AI student-faculty industry research grants."}]
    }
]

ALUMNI_SPECS.extend(NEW_ALUMNI_SPECS)

# -------------------------------------------------------------
# SEED DATABASE FUNCTION (IDEMPOTENT)
# -------------------------------------------------------------
def seed_database(db: Session, force: bool = False):
    """
    Idempotently seeds up to 50 students and 50 alumni with diverse
    Tamil Nadu origin names, departments, skills, and industries.
    Does not duplicate existing users when run repeatedly.
    """
    print("[Seed] Checking Alumnia database seeding status...")

    if force:
        print("[Seed] Force flag active: clearing existing demo records...")
        db.query(Notification).delete()
        db.query(RecommendationFeedback).delete()
        db.query(MentorshipSession).delete()
        db.query(MentorshipRequest).delete()
        db.query(Message).delete()
        db.query(Conversation).delete()
        db.query(ConnectionRequest).delete()
        db.query(Connection).delete()
        db.query(Job).delete()
        db.query(Event).delete()
        db.query(Project).delete()
        db.query(Education).delete()
        db.query(WorkExperience).delete()
        db.query(ProfileSkill).delete()
        db.query(Profile).delete()
        db.query(User).delete()
        db.commit()

    now = datetime.now(timezone.utc)
    hashed_pwd = get_password_hash("Password123!")

    # 1. Admin User
    admin = db.query(User).filter(User.email == "admin@alumnia.edu").first()
    if not admin:
        admin = User(
            email="admin@alumnia.edu",
            hashed_password=hashed_pwd,
            role="admin",
            is_active=True,
            is_verified=True
        )
        db.add(admin)
        db.flush()

        admin_profile = Profile(
            user_id=admin.id,
            full_name="Dr. R. Meenakshi Sundaram",
            role="admin",
            department="Alumni Relations & Career Services",
            headline="Dean of Career Development & Alumni Affairs",
            bio="Leading university initiatives to empower graduating students, build global Tamil Nadu alumni networks, and foster industry collaborations.",
            location="Chennai, Tamil Nadu",
            years_of_experience=20,
            profile_completion_percentage=100,
            is_profile_complete=True
        )
        db.add(admin_profile)
        db.commit()
        print("[Seed] Created admin account: admin@alumnia.edu")

    # 2. Seed 50 Students (Idempotent)
    student_count_created = 0
    for spec in STUDENT_SPECS:
        existing_user = db.query(User).filter(User.email == spec["email"]).first()
        if existing_user:
            continue

        u = User(
            email=spec["email"],
            hashed_password=hashed_pwd,
            role="student",
            is_active=True,
            is_verified=True
        )
        db.add(u)
        db.flush()

        p = Profile(
            user_id=u.id,
            full_name=spec["name"],
            role="student",
            department=spec["dept"],
            degree=spec["degree"],
            graduation_year=spec["grad_year"],
            headline=spec["headline"],
            bio=spec["bio"],
            college_email=spec["email"],
            location=spec["location"],
            mentorship_goals=spec.get("mentorship_goals"),
            profile_completion_percentage=95,
            is_profile_complete=True,
            hide_contact_info=False
        )
        p.target_roles = spec.get("target_roles", ["Software Engineer"])
        p.preferred_industries = spec.get("industries", ["Software & Cloud"])
        p.preferred_locations = spec.get("locations", [spec["location"]])
        db.add(p)
        db.flush()

        # Skills
        for sk in spec.get("skills", []):
            db.add(ProfileSkill(profile_id=p.id, skill_name=sk, category="Technical", endorsement_count=3))

        # Education
        db.add(Education(
            profile_id=p.id,
            institution="Bannari Amman Institute of Technology",
            degree=spec["degree"],
            field_of_study=spec["dept"],
            start_year=spec["grad_year"] - 4,
            end_year=spec["grad_year"],
            grade="8.75 / 10.0 CGPA"
        ))

        # Projects
        for proj in spec.get("projects", []):
            db.add(Project(
                profile_id=p.id,
                title=proj["title"],
                description=proj["desc"],
                technologies=proj.get("tech", "Python, React"),
                project_url="https://github.com/alumnia-students/" + proj["title"].lower().replace(" ", "-")
            ))

        student_count_created += 1

    db.commit()
    print(f"[Seed] Successfully ensured {len(STUDENT_SPECS)} student profiles (Created {student_count_created} new).")

    # 3. Seed 50 Alumni (Idempotent)
    alumni_count_created = 0
    alumni_users = []
    for spec in ALUMNI_SPECS:
        existing_user = db.query(User).filter(User.email == spec["email"]).first()
        if existing_user:
            alumni_users.append(existing_user)
            continue

        u = User(
            email=spec["email"],
            hashed_password=hashed_pwd,
            role="alumni",
            is_active=True,
            is_verified=True
        )
        db.add(u)
        db.flush()
        alumni_users.append(u)

        p = Profile(
            user_id=u.id,
            full_name=spec["name"],
            role="alumni",
            department=spec["department"],
            degree=spec["degree"],
            graduation_year=spec["grad_year"],
            current_job_title=spec["title"],
            current_company=spec["company"],
            industry=spec["industry"],
            years_of_experience=spec["years"],
            headline=spec["headline"],
            bio=spec["bio"],
            location=spec["location"],
            mentorship_available=spec.get("mentor", True),
            mentorship_capacity=3,
            profile_completion_percentage=100,
            is_profile_complete=True,
            hide_contact_info=False
        )
        p.mentorship_topics = spec.get("topics", ["Career Guidance", "Technical Interviews"])
        db.add(p)
        db.flush()

        # Skills
        for sk in spec.get("skills", []):
            db.add(ProfileSkill(profile_id=p.id, skill_name=sk, category="Technical", endorsement_count=8))

        # Education
        db.add(Education(
            profile_id=p.id,
            institution="Bannari Amman Institute of Technology",
            degree=spec["degree"],
            field_of_study=spec["department"],
            start_year=spec["grad_year"] - 4,
            end_year=spec["grad_year"],
            grade="8.90 / 10.0 CGPA"
        ))

        # Experiences
        for exp in spec.get("experience", []):
            db.add(WorkExperience(
                profile_id=p.id,
                title=exp["title"],
                company=exp["company"],
                location=spec["location"],
                start_date=exp.get("start", "2020-01"),
                end_date=exp.get("end"),
                is_current=exp.get("is_current", True),
                description=exp.get("desc", "Leading technical design and delivery.")
            ))

        alumni_count_created += 1

    db.commit()
    print(f"[Seed] Successfully ensured {len(ALUMNI_SPECS)} alumni profiles (Created {alumni_count_created} new).")

    # 4. Seed sample connections and mentorship requests for student@alumnia.edu if needed
    primary_student = db.query(User).filter(User.email == "student@alumnia.edu").first()
    deepa = db.query(User).filter(User.email == "deepa.subramanian@alumni.edu").first()
    vignesh = db.query(User).filter(User.email == "vignesh.balasubramanian@alumni.edu").first()

    if primary_student and deepa:
        # Check connection
        existing_conn = db.query(Connection).filter(
            ((Connection.user1_id == primary_student.id) & (Connection.user2_id == deepa.id)) |
            ((Connection.user1_id == deepa.id) & (Connection.user2_id == primary_student.id))
        ).first()
        if not existing_conn:
            db.add(Connection(user1_id=primary_student.id, user2_id=deepa.id))
            db.commit()

        # Check mentorship request
        existing_mr = db.query(MentorshipRequest).filter(
            MentorshipRequest.student_id == primary_student.id,
            MentorshipRequest.mentor_id == deepa.id
        ).first()
        if not existing_mr:
            mr = MentorshipRequest(
                student_id=primary_student.id,
                mentor_id=deepa.id,
                goals_description="Looking for 1-on-1 guidance on scaling transformer architectures and preparing for Google ML interview loops.",
                preferred_frequency="Bi-weekly",
                status="accepted",
                response_note="Happy to guide you Karthik! Let's schedule a bi-weekly sync to review your projects and system design."
            )
            db.add(mr)
            db.commit()

            # Schedule session
            db.add(MentorshipSession(
                mentorship_request_id=mr.id,
                student_id=primary_student.id,
                mentor_id=deepa.id,
                title="System Design & LLM Fine-Tuning Discussion",
                scheduled_at=now,
                duration_minutes=45,
                meeting_link="https://meet.google.com/alm-gdsc-blr",
                status="scheduled",
                notes="Review Alumnia recommendation engine mathematics and vector indexing optimizations."
            ))
            db.commit()

    print("[Seed] Seed data verification complete. Total Users: ", db.query(User).count())

if __name__ == "__main__":
    import sys
    force_seed = "--force" in sys.argv
    db = SessionLocal()
    try:
        seed_database(db, force=force_seed)
    finally:
        db.close()
