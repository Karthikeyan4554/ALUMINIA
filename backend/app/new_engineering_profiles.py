"""
New Engineering Departments and Industries Dataset for Alumnia.
Adds 20 students and 20 alumni profiles across cutting-edge engineering disciplines:
- Aerospace & Aeronautical Engineering (Aerospace & Defense)
- Robotics & Automation Engineering (Robotics & Industrial Automation)
- Biomedical & Medical Electronics Engineering (Medical Devices & MedTech)
- Civil & Structural Engineering (Infrastructure & Smart Cities)
- Electronics & VLSI Engineering (VLSI & Semiconductor Tech)
- Chemical & Process Engineering (Process Engineering & Petrochemicals)
- Agriculture & Food Engineering (Agritech & Food Processing)
- Automotive & Electric Vehicle Engineering (Automotive & Clean Mobility)
- Cybersecurity & Digital Forensics Engineering (Cybersecurity & Critical Infrastructure)
- Renewable Energy & Power Engineering (Clean Energy & Power Systems)
- Textile & Fashion Technology (Smart Textiles & Apparel Manufacturing)
- Environmental Engineering & Sustainability (Environmental Tech & Sustainability)
- Marine & Ocean Engineering (Marine & Ocean Technology)
- Materials Science & Metallurgical Engineering (Advanced Materials & Metallurgy)
- Mechatronics & Precision Engineering (Robotics & Industrial Automation)
- Electronics & Embedded IoT (Consumer Tech)
- Biotechnology & Bioprocess Engineering (Biotech & Healthcare)
- Industrial Engineering & Operations Research (E-Commerce)
- Autonomous Aerial Systems (Aerospace & Defense)
- Smart Grid & Electric Mobility (Clean Energy & Power Systems)
"""

NEW_STUDENT_SPECS = [
    {
        "email": "siddharth.natarajan@student.alumnia.edu",
        "name": "Siddharth Natarajan",
        "dept": "Aerospace & Aeronautical Engineering",
        "degree": "B.Tech Aerospace Engineering",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "Aerospace Student | Flight Dynamics, CFD & Avionics Systems",
        "bio": "Aerospace engineering undergraduate focused on computational fluid dynamics (CFD), UAV trajectory planning, and supersonic aerodynamics. Seeking mentorship from aerospace research scientists and avionics specialists.",
        "skills": ["Aerodynamics", "MATLAB", "ANSYS Fluent", "Avionics", "Flight Controls", "C++", "Python"],
        "target_roles": ["Avionics Systems Engineer", "Aerodynamics Engineer", "Flight Dynamics Specialist"],
        "industries": ["Aerospace & Defense", "Autonomous Systems"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Understand avionics integration standards and learn how to prepare for propulsion/aerodynamics entry-level roles at aerospace organizations.",
        "projects": [
            {
                "title": "Subsonic UAV Wing Profile Optimization",
                "desc": "Parametric aerodynamic modeling and boundary layer simulation of high-lift wings using ANSYS Fluent and OpenFOAM.",
                "tech": "ANSYS Fluent, OpenFOAM, MATLAB, SolidWorks"
            }
        ]
    },
    {
        "email": "anbuchezhian.p@student.alumnia.edu",
        "name": "Anbuchezhian P",
        "dept": "Robotics & Automation Engineering",
        "degree": "B.Tech Robotics and Automation",
        "grad_year": 2026,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Robotics Student | ROS2, Mobile Robotics & Autonomous Navigation",
        "bio": "Pre-final year robotics engineer specializing in robotic operating systems (ROS/ROS2), 3D SLAM mapping, and industrial robotic arm motion kinematics.",
        "skills": ["ROS", "ROS2", "Python", "C++", "Inverse Kinematics", "SLAM", "Gazebo", "OpenCV"],
        "target_roles": ["Robotics Engineer", "Autonomous Navigation Developer", "Automation Systems Engineer"],
        "industries": ["Robotics & Industrial Automation", "Automotive & Clean Mobility"],
        "locations": ["Coimbatore, Tamil Nadu", "Bengaluru, Karnataka", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Gain industry insights into deploying autonomous mobile robots (AMRs) in manufacturing and warehouse facilities.",
        "projects": [
            {
                "title": "Autonomous Warehouse AMR with LiDAR SLAM",
                "desc": "Built and tested a differential drive mobile robot operating in ROS2 with 2D LiDAR cartographer navigation and obstacle avoidance.",
                "tech": "ROS2, C++, Python, LiDAR, Nav2, Gazebo"
            }
        ]
    },
    {
        "email": "soundarya.murugan@student.alumnia.edu",
        "name": "Soundarya Murugan",
        "dept": "Biomedical & Medical Electronics Engineering",
        "degree": "B.Tech Biomedical Engineering",
        "grad_year": 2025,
        "location": "Madurai, Tamil Nadu",
        "headline": "Biomedical Engineering Senior | MedTech Sensors & Physiological Signal Processing",
        "bio": "Final-year biomedical engineer dedicated to physiological signal monitoring, biosensor instrumentation, and microcontroller-based medical device prototyping.",
        "skills": ["Biomedical Signal Processing", "MATLAB", "LabVIEW", "Medical Device Standards", "Microcontrollers", "Python", "Embedded C"],
        "target_roles": ["Biomedical Systems Engineer", "MedTech Firmware Specialist", "Clinical Applications Specialist"],
        "industries": ["Medical Devices & MedTech", "Healthcare & MedTech"],
        "locations": ["Madurai, Tamil Nadu", "Bengaluru, Karnataka", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Learn regulatory compliance paths (ISO 13485, FDA/CE) for medical electronic hardware and wearable patient monitors.",
        "projects": [
            {
                "title": "Low-Cost Arrhythmia Detector with ECG Wavelet Analysis",
                "desc": "Wearable 3-lead ECG front-end amplifier with real-time Pan-Tompkins QRS wave classification on an ARM Cortex processor.",
                "tech": "MATLAB, Embedded C, Bio-Sensors, Bluetooth Low Energy"
            }
        ]
    },
    {
        "email": "tharun.balasubramaniam@student.alumnia.edu",
        "name": "Tharun Balasubramaniam",
        "dept": "Civil & Structural Engineering",
        "degree": "B.Tech Civil Engineering",
        "grad_year": 2026,
        "location": "Erode, Tamil Nadu",
        "headline": "Civil Engineering Student | Structural Analysis, Seismic Design & BIM Modeling",
        "bio": "Third-year civil engineering undergraduate focusing on tall structure stability, earthquake-resistant design, and Revit 4D building information modeling (BIM).",
        "skills": ["AutoCAD", "ETABS", "STAAD Pro", "Revit BIM", "Concrete Technology", "Structural Dynamics", "Surveying"],
        "target_roles": ["Structural Design Engineer", "BIM Coordinator", "Civil Project Engineer"],
        "industries": ["Infrastructure & Smart Cities", "Infrastructure & Construction"],
        "locations": ["Erode, Tamil Nadu", "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu"],
        "mentorship_goals": "Connect with structural engineering consultants to understand high-rise shear wall design and smart infrastructure tenders.",
        "projects": [
            {
                "title": "Multi-Story Earthquake Resistant Building Analysis",
                "desc": "Seismic response spectrum and dynamic wind load modeling for a G+14 residential concrete building according to Indian Standards (IS 1893).",
                "tech": "ETABS, AutoCAD, Revit, Excel Structural Sheets"
            }
        ]
    },
    {
        "email": "mythili.chandrasekar@student.alumnia.edu",
        "name": "Mythili Chandrasekar",
        "dept": "Electronics & VLSI Engineering",
        "degree": "B.Tech Electronics and Communication Engineering",
        "grad_year": 2025,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "ECE Senior | Digital VLSI Design, Verilog, FPGA & UVM Verification",
        "bio": "Aspiring silicon design engineer with solid experience in RTL design, static timing analysis (STA), SystemVerilog testbenches, and FPGA synthesis.",
        "skills": ["Verilog", "SystemVerilog", "UVM", "FPGA", "Synopsys Design Compiler", "Digital Electronics", "Xilinx Vivado"],
        "target_roles": ["VLSI Design Engineer", "Silicon Verification Engineer", "ASIC Design Specialist"],
        "industries": ["VLSI & Semiconductor Tech", "Semiconductors"],
        "locations": ["Coimbatore, Tamil Nadu", "Bengaluru, Karnataka", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Guidance on semiconductor industry interview rounds covering clock domain crossing (CDC) and SystemVerilog UVM architecture.",
        "projects": [
            {
                "title": "32-bit RISC-V Pipelined Microprocessor Core",
                "desc": "Designed a 5-stage pipelined RV32I integer core with hazard detection, branch prediction, and verified on a Xilinx Artix-7 FPGA.",
                "tech": "SystemVerilog, ModelSim, Xilinx Vivado, FPGA"
            }
        ]
    },
    {
        "email": "iniyan.selvaraj@student.alumnia.edu",
        "name": "Iniyan Selvaraj",
        "dept": "Chemical & Process Engineering",
        "degree": "B.Tech Chemical Engineering",
        "grad_year": 2026,
        "location": "Tiruchirappalli, Tamil Nadu",
        "headline": "Chemical Engineering Student | Process Simulation, Aspen Plus & Reaction Engineering",
        "bio": "Undergraduate enthusiastic about chemical plant optimization, heat exchanger networks, carbon capture reactors, and thermodynamic simulation.",
        "skills": ["Aspen Plus", "Process Simulation", "Heat Transfer", "Fluid Mechanics", "Python", "Mass Transfer", "Process Safety"],
        "target_roles": ["Process Design Engineer", "Chemical Plant Engineer", "Process Safety Specialist"],
        "industries": ["Process Engineering & Petrochemicals", "Petrochemicals & Energy"],
        "locations": ["Tiruchirappalli, Tamil Nadu", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Learn how refinery and fertilizer chemical engineers apply energy pinch analysis and process safety management (HAZOP).",
        "projects": [
            {
                "title": "Bio-Ethanol Distillation Column Simulation",
                "desc": "Steady-state thermodynamic modeling of extractive distillation for fuel-grade ethanol dehydration using Aspen Plus.",
                "tech": "Aspen Plus, MATLAB, Process Control"
            }
        ]
    },
    {
        "email": "kabilan.senthil@student.alumnia.edu",
        "name": "Kabilan Senthil",
        "dept": "Agriculture & Food Engineering",
        "degree": "B.Tech Food Technology",
        "grad_year": 2026,
        "location": "Thanjavur, Tamil Nadu",
        "headline": "Food Technology Student | Sustainable Food Processing, Quality Control & HACCP",
        "bio": "Passionate about novel food processing preservation technologies, dairy engineering, cold-chain logistics, and food safety regulatory standards.",
        "skills": ["Food Preservation", "HACCP", "Thermal Processing", "Food Chemistry", "Dairy Engineering", "Quality Control"],
        "target_roles": ["Food Process Engineer", "Quality Assurance Lead", "Product Development Scientist"],
        "industries": ["Agritech & Food Processing", "FMCG & Food Processing"],
        "locations": ["Thanjavur, Tamil Nadu", "Coimbatore, Tamil Nadu", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Connect with food production managers in FMCG organizations regarding high-throughput aseptic packaging lines.",
        "projects": [
            {
                "title": "Solar-Assisted Heat Pump Food Dehydration Unit",
                "desc": "Fabrication and thermodynamic characterization of an energy-efficient solar hybrid convective dryer for agricultural produce.",
                "tech": "Food Chemistry, Thermal Systems, Quality Testing"
            }
        ]
    },
    {
        "email": "vaishnavi.sundaram@student.alumnia.edu",
        "name": "Vaishnavi Sundaram",
        "dept": "Automotive & Electric Vehicle Engineering",
        "degree": "B.Tech Mechanical Engineering",
        "grad_year": 2025,
        "location": "Hosur, Tamil Nadu",
        "headline": "EV Specialist | Battery Management Systems, Thermal Modeling & Motor Drives",
        "bio": "Final-year mechanical engineering student specializing in lithium-ion battery pack packaging, cell cooling CFD, and electric vehicle powertrain simulation.",
        "skills": ["Battery Management Systems", "MATLAB/Simulink", "CAN Protocol", "Electric Powertrains", "SolidWorks", "ANSYS Fluent"],
        "target_roles": ["EV Powertrain Engineer", "BMS Firmware Engineer", "Battery Thermal Analyst"],
        "industries": ["Automotive & Clean Mobility", "Automotive & EV"],
        "locations": ["Hosur, Tamil Nadu", "Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Learn how EV OEMs configure battery management algorithms (SOC/SOH estimation) for hot climatic conditions.",
        "projects": [
            {
                "title": "Air-Cooled EV Battery Pack with Phase Change Material",
                "desc": "Thermal and fluid dynamics transient simulation of a 48V cylindrical battery pack under aggressive fast-charge discharge cycles.",
                "tech": "MATLAB Simulink, ANSYS Fluent, SolidWorks, CANape"
            }
        ]
    },
    {
        "email": "vigneshwaran.r@student.alumnia.edu",
        "name": "Vigneshwaran R",
        "dept": "Cybersecurity & Digital Forensics Engineering",
        "degree": "B.Tech Information Technology",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "Cybersecurity Enthusiast | Threat Intelligence, SIEM, & Cloud Security",
        "bio": "Third-year IT undergraduate specializing in security operations center (SOC) monitoring, network threat detection, penetration testing, and digital forensics.",
        "skills": ["Network Security", "SIEM", "Wireshark", "Ethical Hacking", "Linux Hardening", "Python", "Cryptography"],
        "target_roles": ["Security Operations Analyst", "Penetration Tester", "Cloud Security Engineer"],
        "industries": ["Cybersecurity & Critical Infrastructure", "Cyber Security & Defense"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Prepare for industry offensive security certifications (OSCP, CEH) and understand enterprise zero-trust infrastructure.",
        "projects": [
            {
                "title": "Automated Network Intrusion Detection with Snort and ELK",
                "desc": "Configured deep packet inspection pipelines streaming IDS alerts into Elasticsearch and Kibana dashboards for anomaly triage.",
                "tech": "Snort, Elasticsearch, Kibana, Python, Linux"
            }
        ]
    },
    {
        "email": "elango.palanisamy@student.alumnia.edu",
        "name": "Elango Palanisamy",
        "dept": "Renewable Energy & Power Engineering",
        "degree": "B.Tech Electrical and Electronics Engineering",
        "grad_year": 2025,
        "location": "Salem, Tamil Nadu",
        "headline": "EEE Senior | Solar PV Farm Engineering, Grid Interconnection & Power Electronics",
        "bio": "Senior electrical engineering student focusing on utility-scale solar PV farm design, maximum power point tracking (MPPT), and smart inverter grid stability.",
        "skills": ["PVsyst", "Solar PV Design", "Power World", "MATLAB Simulink", "High Voltage Engineering", "AutoCAD Electrical"],
        "target_roles": ["Solar PV Design Engineer", "Grid Interconnection Engineer", "Power Systems Analyst"],
        "industries": ["Clean Energy & Power Systems", "Renewable Energy"],
        "locations": ["Salem, Tamil Nadu", "Coimbatore, Tamil Nadu", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Understand grid code compliance requirements for utility-scale solar and wind hybridization projects.",
        "projects": [
            {
                "title": "1 MW Rooftop Solar Microgrid Simulation with Battery Storage",
                "desc": "Techno-economic feasibility analysis and energy yield modeling using PVsyst with power quality assessment under fluctuating loads.",
                "tech": "PVsyst, MATLAB Simulink, AutoCAD Electrical"
            }
        ]
    },
    {
        "email": "archana.veeramani@student.alumnia.edu",
        "name": "Archana Veeramani",
        "dept": "Textile & Fashion Technology",
        "degree": "B.Tech Textile Technology",
        "grad_year": 2026,
        "location": "Tiruppur, Tamil Nadu",
        "headline": "Textile Engineering Student | Smart Textiles, Functional Fabrics & Sustainable Dyeing",
        "bio": "Passionate about smart functional technical textiles, antimicrobial nano-finishing, electronic textile integration, and eco-friendly garment processing.",
        "skills": ["Technical Textiles", "Polymer Chemistry", "Quality Control", "Textile Testing", "Nano-coatings", "Garment Manufacturing"],
        "target_roles": ["Technical Textiles R&D Engineer", "Textile Quality Manager", "Sustainable Apparel Specialist"],
        "industries": ["Smart Textiles & Apparel Manufacturing"],
        "locations": ["Tiruppur, Tamil Nadu", "Coimbatore, Tamil Nadu", "Erode, Tamil Nadu"],
        "mentorship_goals": "Learn how leading export textile mills implement zero liquid discharge (ZLD) and develop conductive yarn wearable sensors.",
        "projects": [
            {
                "title": "Graphene-Coated Conductive Cotton Fabric for Wearable Antennas",
                "desc": "Synthesized graphene-oxide dip-coated functional fabric samples and characterized electrical conductivity and wash durability.",
                "tech": "Textile Testing, Polymer Chemistry, Material Characterization"
            }
        ]
    },
    {
        "email": "gokulnath.s@student.alumnia.edu",
        "name": "Gokulnath S",
        "dept": "Environmental Engineering & Sustainability",
        "degree": "B.Tech Civil Engineering",
        "grad_year": 2026,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Environmental Engineering Focus | Water Treatment, Circular Economy & Carbon Footprinting",
        "bio": "Third-year engineering student dedicated to industrial effluent treatment plant (ETP) design, membrane bioreactors, and municipal circular waste recycling.",
        "skills": ["GIS Mapping", "Air Quality Modeling", "Water Treatment Design", "Circular Economy", "LCA", "Environmental Regulations"],
        "target_roles": ["Environmental Impact Analyst", "Water Treatment Process Engineer", "Sustainability Consultant"],
        "industries": ["Environmental Tech & Sustainability", "Infrastructure & Construction"],
        "locations": ["Coimbatore, Tamil Nadu", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Learn how consulting firms perform environmental impact assessments (EIA) for industrial corridors and river rejuvenation.",
        "projects": [
            {
                "title": "Decentralized Greywater Treatment with Bio-Sand Filtration",
                "desc": "Engineered a low-cost gravity-fed wastewater filtration unit demonstrating 85% turbidity and biological oxygen demand (BOD) reduction.",
                "tech": "Water Quality Analysis, Environmental Modeling, GIS"
            }
        ]
    },
    {
        "email": "poonguzhali.k@student.alumnia.edu",
        "name": "Poonguzhali K",
        "dept": "Marine & Ocean Engineering",
        "degree": "B.Tech Mechanical Engineering",
        "grad_year": 2025,
        "location": "Thoothukudi, Tamil Nadu",
        "headline": "Mechanical Senior | Naval Architecture, Offshore Moorings & Wave Energy",
        "bio": "Senior mechanical engineering student specializing in marine vessel hydrodynamics, offshore wind platform mooring analysis, and corrosion prevention.",
        "skills": ["Hydrodynamics", "Ship Stability", "AutoCAD Marine", "ANSYS Aqwa", "Python", "Finite Element Analysis"],
        "target_roles": ["Naval Architect", "Offshore Marine Engineer", "Subsea Systems Engineer"],
        "industries": ["Marine & Ocean Technology"],
        "locations": ["Thoothukudi, Tamil Nadu", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Connect with shipyard naval architects to understand vessel classification society rules (IRS, DNV) and sea-keeping trials.",
        "projects": [
            {
                "title": "Floating Offshore Wind Turbine Platform Motion Analysis",
                "desc": "Hydrodynamic wave diffraction analysis and 6-DOF motion response simulation for semi-submersible offshore wind foundations.",
                "tech": "ANSYS Aqwa, SolidWorks, MATLAB"
            }
        ]
    },
    {
        "email": "saravanan.thangavel@student.alumnia.edu",
        "name": "Saravanan Thangavel",
        "dept": "Materials Science & Metallurgical Engineering",
        "degree": "B.Tech Mechanical Engineering",
        "grad_year": 2026,
        "location": "Salem, Tamil Nadu",
        "headline": "Materials Science Focus | Alloy Characterization, Heat Treatment & High-Entropy Alloys",
        "bio": "Undergraduate fascinated by physical metallurgy, aerospace titanium alloys, microstructure grain boundary engineering, and additive manufacturing powders.",
        "skills": ["Material Characterization", "XRD", "SEM Analysis", "Phase Diagrams", "Heat Treatment", "Metallography"],
        "target_roles": ["Metallurgical Engineer", "Materials Characterization Specialist", "Failure Analysis Engineer"],
        "industries": ["Advanced Materials & Metallurgy", "Automotive & EV"],
        "locations": ["Salem, Tamil Nadu", "Chennai, Tamil Nadu", "Tiruchirappalli, Tamil Nadu"],
        "mentorship_goals": "Receive guidance from metallurgical quality leads at heavy engineering and steel forging manufacturing plants.",
        "projects": [
            {
                "title": "Cryogenic Heat Treatment Effect on Tool Steel Wear Resistance",
                "desc": "Conducted cryogenic tempering cycles on D2 tool steel specimens, measuring microhardness improvement and retained austenite reduction.",
                "tech": "SEM Analysis, Micro-Hardness Tester, XRD Analysis"
            }
        ]
    },
    {
        "email": "madhumitha.rajasekaran@student.alumnia.edu",
        "name": "Madhumitha Rajasekaran",
        "dept": "Mechatronics & Precision Engineering",
        "degree": "B.Tech Mechatronics Engineering",
        "grad_year": 2026,
        "location": "Erode, Tamil Nadu",
        "headline": "Mechatronics Student | PLC Automation, SCADA & Precision Motion Control",
        "bio": "Mechatronics engineer focused on industrial programmable logic controllers (Siemens/Allen-Bradley), servo motion tuning, and smart factory sensors.",
        "skills": ["Siemens PLC", "SCADA", "Industrial Automation", "SolidWorks", "Microcontrollers", "Pneumatics", "Modbus"],
        "target_roles": ["Industrial Automation Engineer", "PLC Programmer", "Mechatronics Systems Integrator"],
        "industries": ["Robotics & Industrial Automation"],
        "locations": ["Erode, Tamil Nadu", "Coimbatore, Tamil Nadu", "Hosur, Tamil Nadu"],
        "mentorship_goals": "Understand how smart industrial assembly lines integrate machine vision cameras with PLC ladder logic for quality sorting.",
        "projects": [
            {
                "title": "Smart Conveyor Sorting Cell with Vision-Guided Pick and Place",
                "desc": "Engineered a pneumatic pick-and-place gantry controlled via Siemens S7-1200 PLC with Modbus TCP communication and color sensor feedback.",
                "tech": "TIA Portal, Siemens PLC, SolidWorks, Industrial Sensors"
            }
        ]
    },
    {
        "email": "naveen.prasath@student.alumnia.edu",
        "name": "Naveen Prasath",
        "dept": "Electronics & Embedded IoT",
        "degree": "B.Tech Electronics and Communication Engineering",
        "grad_year": 2026,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Embedded Systems Student | Bare-Metal C, RTOS & Low-Power IoT Hardware",
        "bio": "Passionate about low-power embedded software, custom PCB schematic design, ARM Cortex-M firmware architecture, and BLE sensor nodes.",
        "skills": ["C", "C++", "ARM Cortex", "FreeRTOS", "TinyML", "BLE", "KiCad", "I2C/SPI"],
        "target_roles": ["Embedded Firmware Engineer", "IoT Hardware Designer", "Edge Device Developer"],
        "industries": ["Consumer Tech", "Semiconductors"],
        "locations": ["Coimbatore, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Learn how consumer hardware companies bring smart connected wearables from breadboard prototype to mass-manufactured PCB.",
        "projects": [
            {
                "title": "Ultra-Low-Power Environmental Sensor Node with Bluetooth Mesh",
                "desc": "Designed a custom coin-cell powered 4-layer PCB running FreeRTOS with sub-10uA sleep current for smart building telemetry.",
                "tech": "KiCad, C, FreeRTOS, Nordic nRF52840, BLE"
            }
        ]
    },
    {
        "email": "divya.bharathi@student.alumnia.edu",
        "name": "Divya Bharathi",
        "dept": "Biotechnology & Bioprocess Engineering",
        "degree": "B.Tech Biotechnology",
        "grad_year": 2025,
        "location": "Tiruchirappalli, Tamil Nadu",
        "headline": "Biotech Senior | Bioreactor Scale-Up, Upstream Fermentation & Chromatography",
        "bio": "Senior biotechnology student dedicated to recombinant protein expression, microbial fermentation kinetics, and downstream protein purification.",
        "skills": ["Bioreactor Scaling", "Downstream Processing", "Fermentation", "Chromatography", "Python", "Microbiology", "ELISA"],
        "target_roles": ["Bioprocess Development Scientist", "Upstream Fermentation Engineer", "Biotech QA Analyst"],
        "industries": ["Biotech & Healthcare"],
        "locations": ["Tiruchirappalli, Tamil Nadu", "Bengaluru, Karnataka", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Learn how biopharmaceutical manufacturing facilities validate clean-in-place (CIP) and tangential flow filtration (TFF) equipment.",
        "projects": [
            {
                "title": "Optimization of Recombinant Enzyme Yield in Fed-Batch Bioreactor",
                "desc": "Kinetic modeling of glucose feeding strategies in 5-liter stirred tank fermenters resulting in 35% higher biomass density.",
                "tech": "Bioreactor Control, Chromatography, HPLC, Statistical Design of Experiments"
            }
        ]
    },
    {
        "email": "kishore.vasanth@student.alumnia.edu",
        "name": "Kishore Vasanth",
        "dept": "Industrial Engineering & Operations Research",
        "degree": "B.Tech Mechanical Engineering",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "Industrial Engineering Focus | Supply Chain Simulation, Linear Programming & Lean 4.0",
        "bio": "Third-year engineering undergraduate dedicated to mathematical optimization of factory throughput, warehouse bottlenecks, and discrete event simulation.",
        "skills": ["Operations Research", "Linear Programming", "Six Sigma", "SimPy", "Python", "SQL", "Lean Manufacturing"],
        "target_roles": ["Supply Chain Optimization Engineer", "Industrial Operations Analyst", "Lean Manufacturing Specialist"],
        "industries": ["E-Commerce", "Consumer Tech"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Connect with logistics directors to learn how e-commerce fulfillment hubs run dynamic route planning algorithms.",
        "projects": [
            {
                "title": "Discrete-Event Simulation for Automotive Assembly Line Balancing",
                "desc": "Simulated multi-station assembly bottlenecks in SimPy to optimize cycle times, yielding a 14% line balance efficiency improvement.",
                "tech": "Python, SimPy, Operations Research, Tableau"
            }
        ]
    },
    {
        "email": "bhavani.shankar@student.alumnia.edu",
        "name": "Bhavani Shankar",
        "dept": "Autonomous Aerial Systems",
        "degree": "B.Tech Aerospace Engineering",
        "grad_year": 2026,
        "location": "Bengaluru, Karnataka",
        "headline": "Aero Engineering Student | Quadcopter Autonomy, Drone Avionics & PX4 Flight Stacks",
        "bio": "Undergraduate focused on unmanned aerial vehicle (UAV) software, onboard companion computers, vision-based landing, and PX4 flight stack configuration.",
        "skills": ["PX4 Autopilot", "ArduPilot", "Drone Dynamics", "Computer Vision", "C++", "ROS", "MAVLink"],
        "target_roles": ["UAV Flight Software Engineer", "Drone Autonomy Specialist", "Avionics Integrator"],
        "industries": ["Aerospace & Defense", "Robotics & Industrial Automation"],
        "locations": ["Bengaluru, Karnataka", "Chennai, Tamil Nadu"],
        "mentorship_goals": "Understand DGCA drone type certification processes and fail-safe return-to-launch (RTL) telemetry systems.",
        "projects": [
            {
                "title": "GPS-Denied Autonomous Drone Navigation with Optical Flow",
                "desc": "Implemented visual-inertial odometry on an onboard Raspberry Pi companion computer communicating via MAVLink with a Pixhawk flight controller.",
                "tech": "PX4 Autopilot, ROS, C++, MAVLink, OpenCV"
            }
        ]
    },
    {
        "email": "subhashree.anand@student.alumnia.edu",
        "name": "Subhashree Anand",
        "dept": "Smart Grid & Electric Mobility",
        "degree": "B.Tech Electrical and Electronics Engineering",
        "grad_year": 2026,
        "location": "Chennai, Tamil Nadu",
        "headline": "EEE Student | Smart Grid Protection, EV Charging Protocols & Distribution Automation",
        "bio": "Electrical engineering undergraduate passionate about modernizing power grids with EV fast-charging integration, OpenDSS feeder simulation, and SCADA relays.",
        "skills": ["OpenDSS", "Smart Inverters", "SCADA", "EV Charging Protocols", "Python", "Power Systems", "MATLAB"],
        "target_roles": ["Smart Grid Automation Engineer", "EV Charging Infrastructure Lead", "Distribution Systems Analyst"],
        "industries": ["Clean Energy & Power Systems", "Automotive & Clean Mobility"],
        "locations": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka"],
        "mentorship_goals": "Learn how power distribution utilities handle voltage sags and harmonic distortion from high-power fast-charging corridors.",
        "projects": [
            {
                "title": "Impact Analysis of Fast-Charging EV Stations on Distribution Feeders",
                "desc": "Modeled a 33kV urban distribution sub-station in OpenDSS to evaluate transformer loading and propose smart solar inverter VAR support.",
                "tech": "OpenDSS, Python, MATLAB, Power Systems Analysis"
            }
        ]
    }
]

NEW_ALUMNI_SPECS = [
    {
        "email": "rajendran.periasamy@alumni.edu",
        "name": "Dr. Rajendran Periasamy",
        "title": "Principal Aerospace Systems Scientist",
        "company": "ISRO Propulsion Complex",
        "industry": "Aerospace & Defense",
        "department": "Aerospace & Aeronautical Engineering",
        "degree": "Ph.D. Aerospace Propulsion",
        "grad_year": 2012,
        "years": 14,
        "location": "Tirunelveli, Tamil Nadu",
        "headline": "Principal Aerospace Scientist at ISRO | Cryogenic Rocket Propulsion & Launch Vehicle Aerodynamics",
        "bio": "Distinguished alumnus with 14 years of leadership in satellite launch vehicle propulsion, cryogenic fluid management, and aerodynamic thermal protection. Passionate about mentoring aspiring Tamil Nadu aerospace engineers.",
        "skills": ["Aerodynamics", "Aerospace Propulsion", "ANSYS Fluent", "Flight Controls", "MATLAB", "Cryogenics"],
        "mentor": True,
        "topics": ["Space Technology Careers", "Cryogenic Propulsion Design", "ISRO & Defense Research"],
        "experience": [
            {
                "title": "Principal Aerospace Systems Scientist",
                "company": "ISRO Propulsion Complex",
                "start": "2015-06",
                "is_current": True,
                "desc": "Supervised testing and validation of cryogenic upper-stage rocket engines for heavy satellite launch vehicles."
            }
        ]
    },
    {
        "email": "karthikeyan.munusamy@alumni.edu",
        "name": "Karthikeyan Munusamy",
        "title": "Lead Robotics Automation Architect",
        "company": "Addverb Technologies",
        "industry": "Robotics & Industrial Automation",
        "department": "Robotics & Automation Engineering",
        "degree": "M.Tech Robotics & Autonomous Systems",
        "grad_year": 2016,
        "years": 10,
        "location": "Bengaluru, Karnataka",
        "headline": "Lead Robotics Architect at Addverb | Autonomous Mobile Robots & Industrial Warehouse Robotics",
        "bio": "10 years designing multi-agent mobile robotic fleets (AMRs/AGVs) deployed in Fortune 500 manufacturing plants across Asia and Europe. Open for 1:1 student mentorship in ROS2 and robot fleet dispatching.",
        "skills": ["ROS", "ROS2", "Python", "C++", "SLAM", "Industrial Automation", "Autonomous Navigation"],
        "mentor": True,
        "topics": ["Industrial Robotics Careers", "Autonomous Navigation (SLAM)", "Robotics System Architecture"],
        "experience": [
            {
                "title": "Lead Robotics Automation Architect",
                "company": "Addverb Technologies",
                "start": "2019-01",
                "is_current": True,
                "desc": "Architected fleet management software controlling 300+ autonomous warehouse mobile robots with zero deadlocks."
            }
        ]
    },
    {
        "email": "lavanya.jayachandran@alumni.edu",
        "name": "Dr. Lavanya Jayachandran",
        "title": "Director of Medical Device Innovation",
        "company": "Siemens Healthineers",
        "industry": "Medical Devices & MedTech",
        "department": "Biomedical & Medical Electronics Engineering",
        "degree": "Ph.D. Biomedical Instrumentation",
        "grad_year": 2013,
        "years": 13,
        "location": "Bengaluru, Karnataka",
        "headline": "Director of MedTech Innovation at Siemens Healthineers | Patient Monitoring & Biosignal Systems",
        "bio": "Experienced leader in clinical medical electronics, non-invasive cardiac telemetry, and FDA-certified wearable medical instruments. Dedicated to helping biomedical students bridge the gap between classroom theory and clinical products.",
        "skills": ["Biomedical Signal Processing", "Medical Device Standards", "Embedded C", "LabVIEW", "Bio-Sensors", "Healthcare Tech"],
        "mentor": True,
        "topics": ["Medical Device Regulatory Approvals", "Biomedical Product Design", "Clinical Healthcare Engineering"],
        "experience": [
            {
                "title": "Director of Medical Device Innovation",
                "company": "Siemens Healthineers",
                "start": "2018-04",
                "is_current": True,
                "desc": "Led an international cross-functional engineering team delivering next-generation ICU bedside cardiac monitors."
            }
        ]
    },
    {
        "email": "sundararajan.natarajan@alumni.edu",
        "name": "Sundararajan Natarajan",
        "title": "Chief Structural Engineer",
        "company": "L&T Construction",
        "industry": "Infrastructure & Smart Cities",
        "department": "Civil & Structural Engineering",
        "degree": "M.Tech Structural Engineering",
        "grad_year": 2012,
        "years": 14,
        "location": "Chennai, Tamil Nadu",
        "headline": "Chief Structural Engineer at L&T Construction | Metro Rail Infrastructure & Mega Structures",
        "bio": "Structural engineer with 14 years overseeing major metro viaducts, coastal bridge spans, and seismic-isolated airport terminal structures across India. Active mentor for civil engineering students.",
        "skills": ["STAAD Pro", "ETABS", "Revit BIM", "Structural Dynamics", "AutoCAD", "Concrete Technology"],
        "mentor": True,
        "topics": ["Large Infrastructure Mega-Projects", "Seismic Structural Analysis", "Civil Engineering Career Growth"],
        "experience": [
            {
                "title": "Chief Structural Engineer",
                "company": "L&T Construction",
                "start": "2016-08",
                "is_current": True,
                "desc": "Technical lead for elevated viaduct prestressed concrete girder design across Chennai Metro Rail Phase II."
            }
        ]
    },
    {
        "email": "venkatesh.radhakrishnan@alumni.edu",
        "name": "Venkatesh Radhakrishnan",
        "title": "Principal Silicon Verification Architect",
        "company": "Qualcomm",
        "industry": "VLSI & Semiconductor Tech",
        "department": "Electronics & VLSI Engineering",
        "degree": "M.Tech VLSI Design",
        "grad_year": 2014,
        "years": 12,
        "location": "Chennai, Tamil Nadu",
        "headline": "Principal Silicon Verification Architect at Qualcomm | 4nm Mobile SoC & UVM Environments",
        "bio": "12 years in semiconductor tape-outs, high-speed interface protocols (PCIe, LPDDR5), and complex SystemVerilog UVM verification suites. Passionate about empowering students to enter top semiconductor silicon design teams.",
        "skills": ["SystemVerilog", "UVM", "Verilog", "FPGA", "Digital Electronics", "ASIC Design"],
        "mentor": True,
        "topics": ["Semiconductor Tape-Out Roadmap", "SystemVerilog / UVM Mastery", "Hardware Verification Careers"],
        "experience": [
            {
                "title": "Principal Silicon Verification Architect",
                "company": "Qualcomm",
                "start": "2017-03",
                "is_current": True,
                "desc": "Directed pre-silicon verification for multi-core neural processing units (NPU) in flagship mobile Snapdragon platforms."
            }
        ]
    },
    {
        "email": "muthukumar.shanmugam@alumni.edu",
        "name": "Muthukumar Shanmugam",
        "title": "Head of Petrochemical Process Engineering",
        "company": "Tamil Nadu Petroproducts",
        "industry": "Process Engineering & Petrochemicals",
        "department": "Chemical & Process Engineering",
        "degree": "B.Tech Chemical Engineering",
        "grad_year": 2013,
        "years": 13,
        "location": "Chennai, Tamil Nadu",
        "headline": "Head of Petrochemical Process Engineering | Refinery Energy Optimization & Plant Safety",
        "bio": "Chemical engineering professional with 13 years managing large-scale linear alkylbenzene chemical plants, energy conservation audits, and safety integrity level (SIL) HAZOP protocols.",
        "skills": ["Aspen Plus", "Process Simulation", "Process Safety", "Heat Transfer", "Mass Transfer", "Fluid Mechanics"],
        "mentor": True,
        "topics": ["Refinery & Petrochemical Operations", "Process Safety Management", "Energy Pinch Optimization"],
        "experience": [
            {
                "title": "Head of Petrochemical Process Engineering",
                "company": "Tamil Nadu Petroproducts",
                "start": "2018-05",
                "is_current": True,
                "desc": "Engineered multi-column distillation modifications saving 18% thermal steam consumption across plant operations."
            }
        ]
    },
    {
        "email": "sangeetha.thirunavukkarasu@alumni.edu",
        "name": "Sangeetha Thirunavukkarasu",
        "title": "VP of Food Process Engineering",
        "company": "ITC Foods Division",
        "industry": "Agritech & Food Processing",
        "department": "Agriculture & Food Engineering",
        "degree": "M.Tech Food Process Engineering",
        "grad_year": 2014,
        "years": 12,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "VP of Food Process Engineering at ITC Foods | High-Speed Aseptic Processing & FSSAI Standards",
        "bio": "12 years leading industrial food processing lines, extrusion technology, smart food shelf-life packaging, and national regulatory quality assurance. Mentoring food technology innovators.",
        "skills": ["Food Preservation", "HACCP", "Quality Control", "Thermal Processing", "Food Chemistry"],
        "mentor": True,
        "topics": ["FMCG Food Manufacturing", "HACCP & International Food Audits", "Novel Food Technology Trends"],
        "experience": [
            {
                "title": "VP of Food Process Engineering",
                "company": "ITC Foods Division",
                "start": "2017-09",
                "is_current": True,
                "desc": "Commissioned 5 automated bakery and dairy aseptic packaging production lines across South India manufacturing hubs."
            }
        ]
    },
    {
        "email": "hariharan.balakrishnan@alumni.edu",
        "name": "Hariharan Balakrishnan",
        "title": "Principal Battery Systems Architect",
        "company": "Ather Energy",
        "industry": "Automotive & Clean Mobility",
        "department": "Automotive & Electric Vehicle Engineering",
        "degree": "M.Tech Automotive Engineering",
        "grad_year": 2015,
        "years": 11,
        "location": "Hosur, Tamil Nadu",
        "headline": "Principal Battery Systems Architect at Ather Energy | EV Battery Packs, Safety & Thermal Architecture",
        "bio": "Leading electric mobility hardware engineering for over a decade. Specialized in lithium battery thermal management, structural crash safety, and CAN bus vehicle diagnostics. Passionate about empowering EV student engineers.",
        "skills": ["Battery Management Systems", "Electric Powertrains", "MATLAB/Simulink", "CAN Protocol", "SolidWorks", "ANSYS Fluent"],
        "mentor": True,
        "topics": ["Electric Vehicle Powertrain Engineering", "BMS Algorithms & Battery Safety", "Clean Mobility Career Guidance"],
        "experience": [
            {
                "title": "Principal Battery Systems Architect",
                "company": "Ather Energy",
                "start": "2018-02",
                "is_current": True,
                "desc": "Architected the aluminum-diecast IP67 battery pack assembly for high-performance electric two-wheelers."
            }
        ]
    },
    {
        "email": "sendhilvelan.gurusamy@alumni.edu",
        "name": "Sendhilvelan Gurusamy",
        "title": "Chief Information Security Officer",
        "company": "Tamilnad Mercantile Tech Security",
        "industry": "Cybersecurity & Critical Infrastructure",
        "department": "Cybersecurity & Digital Forensics Engineering",
        "degree": "M.S. Information Security",
        "grad_year": 2013,
        "years": 13,
        "location": "Chennai, Tamil Nadu",
        "headline": "CISO at TMB Tech | Critical Banking Cyber Defense, Threat Forensics & SOC Operations",
        "bio": "Cybersecurity veteran with 13 years safeguarding critical financial infrastructure against advanced persistent threats (APTs), zero-day exploits, and ransomware attacks. Dedicated student mentor.",
        "skills": ["Network Security", "SIEM", "Ethical Hacking", "Cryptography", "Linux Hardening", "Wireshark"],
        "mentor": True,
        "topics": ["Banking & Defense Cybersecurity", "SOC Analyst Career Roadmaps", "Hands-on Penetration Testing"],
        "experience": [
            {
                "title": "Chief Information Security Officer",
                "company": "Tamilnad Mercantile Tech Security",
                "start": "2017-06",
                "is_current": True,
                "desc": "Built and managed a 24/7 Security Operations Center monitoring over 15 million daily financial transactions."
            }
        ]
    },
    {
        "email": "akilandeshwari.subramanian@alumni.edu",
        "name": "Akilandeshwari Subramanian",
        "title": "Senior Technical Director of Clean Energy",
        "company": "Tata Power Solar",
        "industry": "Clean Energy & Power Systems",
        "department": "Renewable Energy & Power Engineering",
        "degree": "M.Tech Power Systems Engineering",
        "grad_year": 2014,
        "years": 12,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Senior Technical Director at Tata Power Solar | 500MW Utility Solar Parks & Microgrid Architecture",
        "bio": "12 years engineering mega-watt scale solar photovoltaic installations, high-voltage substations, and battery energy storage systems (BESS). Mentoring young electrical engineers.",
        "skills": ["Solar PV Design", "PVsyst", "High Voltage Engineering", "Power World", "MATLAB Simulink", "AutoCAD Electrical"],
        "mentor": True,
        "topics": ["Utility-Scale Renewable Energy", "Grid Integration of Renewables", "Power Sector Careers"],
        "experience": [
            {
                "title": "Senior Technical Director of Clean Energy",
                "company": "Tata Power Solar",
                "start": "2018-01",
                "is_current": True,
                "desc": "Supervised engineering design and grid commissioning for 750 MW of solar PV parks across Tamil Nadu and Karnataka."
            }
        ]
    },
    {
        "email": "rangasamy.chinnasamy@alumni.edu",
        "name": "Rangasamy Chinnasamy",
        "title": "Executive Director of Technical Textiles R&D",
        "company": "Loyal Textile Mills",
        "industry": "Smart Textiles & Apparel Manufacturing",
        "department": "Textile & Fashion Technology",
        "degree": "M.Tech Textile Technology",
        "grad_year": 2011,
        "years": 15,
        "location": "Erode, Tamil Nadu",
        "headline": "Executive Director of R&D at Loyal Textile Mills | Protective Textiles & Smart Functional Fabrics",
        "bio": "Distinguished textile alumnus with 15 years developing flame-retardant military fabrics, medical PPE textiles, and sensor-integrated smart garments. Proud to support students from Tamil Nadu textile hubs.",
        "skills": ["Technical Textiles", "Polymer Chemistry", "Textile Testing", "Quality Control", "Nano-coatings"],
        "mentor": True,
        "topics": ["Technical & Defense Textiles", "Sustainable Textile Chemistry", "Apparel Export Strategy"],
        "experience": [
            {
                "title": "Executive Director of Technical Textiles R&D",
                "company": "Loyal Textile Mills",
                "start": "2015-04",
                "is_current": True,
                "desc": "Patented viral-barrier nano-composite finished woven fabrics exported across 24 countries worldwide."
            }
        ]
    },
    {
        "email": "hemalatha.sivaraman@alumni.edu",
        "name": "Hemalatha Sivaraman",
        "title": "Principal Sustainability & Carbon Consultant",
        "company": "ERM India",
        "industry": "Environmental Tech & Sustainability",
        "department": "Environmental Engineering & Sustainability",
        "degree": "M.Tech Environmental Engineering",
        "grad_year": 2015,
        "years": 11,
        "location": "Chennai, Tamil Nadu",
        "headline": "Principal Consultant at ERM India | ESG Strategies, Industrial Decarbonization & Water Neutrality",
        "bio": "Consultant specializing in industrial carbon auditing, life cycle assessments (LCA), zero liquid discharge plant design, and corporate sustainability frameworks.",
        "skills": ["LCA", "Circular Economy", "Water Treatment Design", "GIS Mapping", "Environmental Regulations"],
        "mentor": True,
        "topics": ["Corporate Decarbonization & ESG", "Environmental Engineering Roles", "Industrial Water Recycling"],
        "experience": [
            {
                "title": "Principal Sustainability Consultant",
                "company": "ERM India",
                "start": "2018-09",
                "is_current": True,
                "desc": "Advised over 30 manufacturing plants across South India on attaining zero-liquid discharge and Scope 1 & 2 carbon reductions."
            }
        ]
    },
    {
        "email": "balasubramaniam.chelladurai@alumni.edu",
        "name": "Balasubramaniam Chelladurai",
        "title": "Chief Marine Systems Engineer",
        "company": "Cochin Shipyard Ltd",
        "industry": "Marine & Ocean Technology",
        "department": "Marine & Ocean Engineering",
        "degree": "B.Tech Mechanical & Marine Engineering",
        "grad_year": 2013,
        "years": 13,
        "location": "Thoothukudi, Tamil Nadu",
        "headline": "Chief Marine Systems Engineer at Cochin Shipyard | Commercial Ships & Offshore Patrol Vessels",
        "bio": "Over 13 years managing commercial ship construction, hull hydrodynamics, propulsion shafting alignment, and international maritime safety regulations (SOLAS).",
        "skills": ["Hydrodynamics", "Ship Stability", "AutoCAD Marine", "ANSYS Aqwa", "Finite Element Analysis"],
        "mentor": True,
        "topics": ["Shipbuilding & Marine Engineering", "Offshore Platform Design", "Maritime Engineering Careers"],
        "experience": [
            {
                "title": "Chief Marine Systems Engineer",
                "company": "Cochin Shipyard Ltd",
                "start": "2016-11",
                "is_current": True,
                "desc": "Lead machinery outfitting and sea-trial commissioning manager for multi-purpose commercial freight carriers."
            }
        ]
    },
    {
        "email": "ganesan.muthiah@alumni.edu",
        "name": "Ganesan Muthiah",
        "title": "Senior Materials & Metallurgy Specialist",
        "company": "BHEL Tiruchirappalli",
        "industry": "Advanced Materials & Metallurgy",
        "department": "Materials Science & Metallurgical Engineering",
        "degree": "M.Tech Metallurgical Engineering",
        "grad_year": 2014,
        "years": 12,
        "location": "Tiruchirappalli, Tamil Nadu",
        "headline": "Senior Materials Specialist at BHEL | Supercritical Boiler Alloys & High-Temperature Metallurgy",
        "bio": "12 years conducting failure analysis, creep fatigue assessment, advanced welding metallurgy, and non-destructive testing for ultra-supercritical power plant components.",
        "skills": ["Material Characterization", "Heat Treatment", "SEM Analysis", "XRD", "Phase Diagrams"],
        "mentor": True,
        "topics": ["Physical Metallurgy Careers", "Failure Analysis Methodology", "Heavy Manufacturing Materials"],
        "experience": [
            {
                "title": "Senior Materials & Metallurgy Specialist",
                "company": "BHEL Tiruchirappalli",
                "start": "2016-01",
                "is_current": True,
                "desc": "Conducted creep-life prediction and microscopic grain boundary evaluations for high-nickel turbine alloys."
            }
        ]
    },
    {
        "email": "dhanalakshmi.narayanan@alumni.edu",
        "name": "Dhanalakshmi Narayanan",
        "title": "Senior Director of Precision Automation",
        "company": "Titan Precision Engineering",
        "industry": "Robotics & Industrial Automation",
        "department": "Mechatronics & Precision Engineering",
        "degree": "B.Tech Mechatronics Engineering",
        "grad_year": 2015,
        "years": 11,
        "location": "Hosur, Tamil Nadu",
        "headline": "Senior Director at Titan Precision Engineering | High-Speed Micro-Assembly & Automated Inspection",
        "bio": "11 years developing precision automated assembly fixtures, multi-axis servo controllers, and sub-micron vision inspection machinery. Open to mentoring students in automation.",
        "skills": ["Siemens PLC", "SCADA", "Industrial Automation", "SolidWorks", "Pneumatics", "Microcontrollers"],
        "mentor": True,
        "topics": ["Precision Automation Engineering", "PLC & Vision System Integration", "Smart Factory Manufacturing"],
        "experience": [
            {
                "title": "Senior Director of Precision Automation",
                "company": "Titan Precision Engineering",
                "start": "2019-03",
                "is_current": True,
                "desc": "Designed fully automated watch-component and precision sensor assembly cells with 99.8% first-pass yields."
            }
        ]
    },
    {
        "email": "prasanna.venkatesh@alumni.edu",
        "name": "Prasanna Venkatesh",
        "title": "Staff Embedded Architect",
        "company": "Bosch India",
        "industry": "Consumer Tech",
        "department": "Electronics & Embedded IoT",
        "degree": "M.Tech Embedded Systems",
        "grad_year": 2016,
        "years": 10,
        "location": "Coimbatore, Tamil Nadu",
        "headline": "Staff Embedded Architect at Bosch | Automotive Body Electronics & Microcontroller Firmware",
        "bio": "10 years in bare-metal C, AUTOSAR architecture, automotive bus communication (CAN/LIN), and secure bootloaders for smart automotive sensors.",
        "skills": ["C", "C++", "ARM Cortex", "FreeRTOS", "BLE", "TinyML", "I2C/SPI"],
        "mentor": True,
        "topics": ["Automotive Embedded Systems", "AUTOSAR & RTOS Deep Dive", "Embedded Engineering Interviews"],
        "experience": [
            {
                "title": "Staff Embedded Architect",
                "company": "Bosch India",
                "start": "2018-07",
                "is_current": True,
                "desc": "Architected low-power microcontroller body control modules operating in over 2 million passenger vehicles."
            }
        ]
    },
    {
        "email": "anbarasu.marimuthu@alumni.edu",
        "name": "Anbarasu Marimuthu",
        "title": "Head of Biologics Upstream Manufacturing",
        "company": "Biocon",
        "industry": "Biotech & Healthcare",
        "department": "Biotechnology & Bioprocess Engineering",
        "degree": "M.Tech Bioprocess Technology",
        "grad_year": 2014,
        "years": 12,
        "location": "Bengaluru, Karnataka",
        "headline": "Head of Biologics Manufacturing at Biocon | Monoclonal Antibodies & Commercial Bioreactor Scale-Up",
        "bio": "12 years in biopharmaceutical manufacturing, recombinant antibody production in 10,000-liter stainless steel bioreactors, and cGMP compliance.",
        "skills": ["Bioreactor Scaling", "Fermentation", "Downstream Processing", "Chromatography", "Microbiology"],
        "mentor": True,
        "topics": ["Biopharmaceutical Manufacturing Careers", "Upstream Bioprocess Scale-Up", "cGMP Quality Guidelines"],
        "experience": [
            {
                "title": "Head of Biologics Upstream Manufacturing",
                "company": "Biocon",
                "start": "2017-04",
                "is_current": True,
                "desc": "Supervised commercial-scale recombinant insulin and oncology biosimilar fermentation campaigns."
            }
        ]
    },
    {
        "email": "vijayalakshmi.sethuraman@alumni.edu",
        "name": "Vijayalakshmi Sethuraman",
        "title": "Director of Supply Chain Operations Research",
        "company": "Amazon Logistics",
        "industry": "E-Commerce",
        "department": "Industrial Engineering & Operations Research",
        "degree": "M.S. Operations Research & Industrial Eng.",
        "grad_year": 2015,
        "years": 11,
        "location": "Chennai, Tamil Nadu",
        "headline": "Director at Amazon Logistics | Operations Research, Last-Mile Routing & Warehouse Optimization",
        "bio": "11 years developing mixed-integer linear programming algorithms, network flow optimizations, and automated robotic fulfillment center scheduling.",
        "skills": ["Operations Research", "Linear Programming", "Python", "SQL", "SimPy", "Six Sigma"],
        "mentor": True,
        "topics": ["Operations Research in Tech", "Supply Chain Analytics Careers", "Large-Scale Mathematical Optimization"],
        "experience": [
            {
                "title": "Director of Supply Chain Operations Research",
                "company": "Amazon Logistics",
                "start": "2019-02",
                "is_current": True,
                "desc": "Engineered last-mile dispatch routing algorithms cutting average package fulfillment times by 12% across South India."
            }
        ]
    },
    {
        "email": "kalyanaraman.srinivasan@alumni.edu",
        "name": "Kalyanaraman Srinivasan",
        "title": "Head of Flight Software",
        "company": "AgniKul Cosmos",
        "industry": "Aerospace & Defense",
        "department": "Autonomous Aerial Systems",
        "degree": "B.Tech Aerospace Engineering",
        "grad_year": 2017,
        "years": 9,
        "location": "Chennai, Tamil Nadu",
        "headline": "Head of Flight Software at AgniKul Cosmos | Rocket Guidance, Navigation & Real-Time Flight Computers",
        "bio": "Alumnus leading mission-critical launch vehicle software for customizable space rockets manufactured with 3D printed engines at IIT Madras Research Park.",
        "skills": ["Flight Controls", "C++", "Avionics", "PX4 Autopilot", "Aerodynamics", "ROS"],
        "mentor": True,
        "topics": ["NewSpace Startups in India", "Real-Time Embedded Flight Code", "Aerospace Systems Engineering"],
        "experience": [
            {
                "title": "Head of Flight Software",
                "company": "AgniKul Cosmos",
                "start": "2019-10",
                "is_current": True,
                "desc": "Built hard-real-time flight guidance and autopilot software for orbital and sub-orbital launch vehicles."
            }
        ]
    },
    {
        "email": "revathi.senthilvel@alumni.edu",
        "name": "Revathi Senthilvel",
        "title": "Principal Microgrid Solutions Architect",
        "company": "Schneider Electric",
        "industry": "Clean Energy & Power Systems",
        "department": "Smart Grid & Electric Mobility",
        "degree": "M.Tech Power Electronics & Drives",
        "grad_year": 2016,
        "years": 10,
        "location": "Chennai, Tamil Nadu",
        "headline": "Principal Architect at Schneider Electric | Smart Microgrids, Renewable Inverters & EV Integration",
        "bio": "10 years designing autonomous industrial microgrids, battery storage power conversion systems, and smart factory energy management platforms.",
        "skills": ["Smart Inverters", "SCADA", "Power Systems", "EV Charging Protocols", "OpenDSS", "MATLAB"],
        "mentor": True,
        "topics": ["Smart Grid & Microgrid Trends", "Industrial Power Electronics", "Energy Transition Careers"],
        "experience": [
            {
                "title": "Principal Microgrid Solutions Architect",
                "company": "Schneider Electric",
                "start": "2019-05",
                "is_current": True,
                "desc": "Deployed over 40 islanded microgrid control systems across industrial manufacturing campuses in India."
            }
        ]
    }
]
