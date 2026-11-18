# -*- coding: utf-8 -*-
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_generator.helpers import (
    add_heading_1, add_heading_2, add_heading_3, add_p, create_table
)

def build_front_matter(doc, page_map=None):
    if page_map is None:
        page_map = {}

    def get_p(key, default):
        return str(page_map.get(key, default))

    # ==========================================
    # 1. COVER PAGE
    # ==========================================
    p1 = add_p(doc, "A", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p1.runs[0].font.size = Pt(14)
    
    p2 = add_p(doc, "Major Project", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p2.runs[0].font.size = Pt(16)
    
    p3 = add_p(doc, "On", bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    p3.runs[0].font.size = Pt(13)
    
    p4 = add_p(doc, "“AuraFIT”", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    p4.runs[0].font.size = Pt(22)
    
    p5 = add_p(doc, "In Partial Fulfillment for the award of the Degree Of", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p5.runs[0].font.size = Pt(13)
    
    p6 = add_p(doc, "Bachelor Of Computer Application (BCA)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=22)
    p6.runs[0].font.size = Pt(15)

    p_univ = add_p(doc, "JECRC UNIVERSITY", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p_univ.runs[0].font.size = Pt(22)
    
    p_tag = add_p(doc, "BUILD YOUR WORLD", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)
    p_tag.runs[0].font.size = Pt(12)

    # 2-column table for Guide & Student
    tbl_meta = doc.add_table(rows=1, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = tbl_meta.cell(0, 0)
    c_right = tbl_meta.cell(0, 1)
    c_left.width = Inches(3.25)
    c_right.width = Inches(3.25)
    
    p_gl = c_left.paragraphs[0]
    p_gl.paragraph_format.line_spacing = 1.3
    p_gl.paragraph_format.space_after = Pt(2)
    r1 = p_gl.add_run("Under The Guidance Of:\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r2 = p_gl.add_run("Ms. Rashi Jain\n(Assistant Professor)\nDepartment of Computer Application")
    r2.bold = False
    r2.font.size = Pt(11)
    
    p_gr = c_right.paragraphs[0]
    p_gr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_gr.paragraph_format.line_spacing = 1.3
    p_gr.paragraph_format.space_after = Pt(2)
    r3 = p_gr.add_run("Submitted By:\n")
    r3.bold = True
    r3.font.size = Pt(11)
    r4 = p_gr.add_run("Ved Gupta\n24BCAN0252\nBCA 5th Semester\nDepartment of Computer Application")
    r4.bold = False
    r4.font.size = Pt(11)

    p_bot1 = add_p(doc, "Department of Computer Application", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p_bot1.paragraph_format.space_before = Pt(50)
    p_bot1.runs[0].font.size = Pt(12)
    p_bot2 = add_p(doc, "JECRC UNIVERSITY, JAIPUR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p_bot2.runs[0].font.size = Pt(13)
    p_bot3 = add_p(doc, "2024–2027", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    p_bot3.runs[0].font.size = Pt(12)

    doc.add_page_break()

    # ==========================================
    # 2. CANDIDATE DECLARATION
    # ==========================================
    add_heading_1(doc, "CANDIDATE DECLARATION", align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc, "I hereby declare that the project work titled “AuraFIT: AI-POWERED PERSONALIZED FITNESS & NUTRITION PLATFORM”, submitted as part of my academic requirement, is a record of my own work carried out under the guidance of Ms. Rashi Jain. This project has been completed in partial fulfillment of the requirements for Bachelor of Computer Application (BCA) at JECRC University.")

    add_p(doc, "I further declare that this project has not been submitted to any other university or institution for the award of any degree, diploma, or certificate. All sources of information and data used in this project have been acknowledged appropriately.")

    add_p(doc, "I understand that any breach of this declaration will result in the rejection of this project and disciplinary action.")

    add_p(doc, "Name of the Student:", bold=True, space_after=1)
    add_p(doc, "Ved Gupta", space_after=6)

    add_p(doc, "Roll Number:", bold=True, space_after=1)
    add_p(doc, "24BCAN0252", space_after=6)

    add_p(doc, "Course and Semester:", bold=True, space_after=1)
    add_p(doc, "Bachelor of Computer Application (BCA), 5th Semester", space_after=6)

    add_p(doc, "Name(s) of Supervisor(s)/Guide(s):", bold=True, space_after=1)
    add_p(doc, "Ms. Rashi Jain (Assistant Professor)", space_after=6)

    add_p(doc, "Submission Date:", bold=True, space_after=1)
    add_p(doc, "January, 2027", space_after=28)

    add_p(doc, "Signature: __________________________", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=0)

    doc.add_page_break()

    # ==========================================
    # 3. MAJOR PROJECT COMPLETION CERTIFICATE
    # ==========================================
    add_heading_1(doc, "JECRC UNIVERSITY", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Department of Computer Application", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_heading_2(doc, "Major Project Completion Certificate", align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc, "This is to certify that Mr. Ved Gupta, Registration No: 24BCAN0252, has successfully completed the Major Project as a Part of the requirement for the Bachelor of Computer Application (BCA) Program at JECRC UNIVERSITY, Jaipur, India.")

    add_p(doc, "Project Title: AuraFIT: AI-Powered Personalized Fitness & Nutrition Platform", bold=True)
    add_p(doc, "Technology Used: React 18, TypeScript, Tailwind CSS, Python 3.10+, FastAPI, Motor (Async MongoDB), MongoDB Atlas, Google Gemini API.", bold=True)
    add_p(doc, "Project Supervisor: Ms. Rashi Jain", bold=True)

    add_p(doc, "This project demonstrates student’s ability to apply theoretical knowledge gained during his academic tenure to practical real-world engineering scenarios. His dedication, hard work, architectural ingenuity, and proficiency in full-stack software development and artificial intelligence integration is commendable.")

    tbl_cert = doc.add_table(rows=1, cols=2)
    tbl_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_hod = tbl_cert.cell(0, 0)
    c_sup = tbl_cert.cell(0, 1)
    c_hod.width = Inches(3.25)
    c_sup.width = Inches(3.25)
    
    p_hod = c_hod.paragraphs[0]
    p_hod.paragraph_format.space_before = Pt(65)
    p_hod.paragraph_format.line_spacing = 1.2
    r_h1 = p_hod.add_run("_________________________\n")
    r_h2 = p_hod.add_run("Mr. Shekhar Chander\nHoD, Department of Computer Application\nJECRC University, Jaipur")
    r_h2.bold = True
    r_h2.font.size = Pt(11)

    p_sup = c_sup.paragraphs[0]
    p_sup.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sup.paragraph_format.space_before = Pt(65)
    p_sup.paragraph_format.line_spacing = 1.2
    r_s1 = p_sup.add_run("_________________________\n")
    r_s2 = p_sup.add_run("Project Supervisor\nMs. Rashi Jain\nDepartment of Computer Application")
    r_s2.bold = True
    r_s2.font.size = Pt(11)

    doc.add_page_break()

    # ==========================================
    # 4. ACKNOWLEDGEMENT
    # ==========================================
    add_heading_1(doc, "ACKNOWLEDGEMENT", align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc, 'I am sincerely grateful to everyone who contributed to the successful conceptualization, engineering, and completion of my project, "AuraFIT: AI-Powered Personalized Fitness & Nutrition Platform".')

    add_p(doc, "First and foremost, I would like to express my heartfelt gratitude to my project guide, Ms. Rashi Jain, for her invaluable guidance, constant encouragement, and critical feedback throughout this project. Her profound academic expertise and practical advice helped me rigorously define the boundaries between deterministic calculations and generative AI, ensuring the platform remained scientifically authoritative.")

    add_p(doc, "I would also like to thank Mr. Shekhar Chander, Head of the Department of Computer Application, and all respected faculty members of JECRC University for providing the computational infrastructure, academic resources, and nurturing environment that enabled me to undertake this ambitious project.")

    add_p(doc, "Additionally, I am deeply thankful to my classmates and peers for their active participation in user acceptance testing, UI evaluation, and constructive feedback, which substantially enhanced the usability, design aesthetics, and resilience of the AuraFIT platform.")

    add_p(doc, "Finally, I would like to extend my deepest appreciation to my family for their unwavering moral support, patience, and encouragement during countless hours of development and academic research.")

    add_p(doc, "Ved Gupta", bold=True, space_after=1)
    add_p(doc, "Roll No: 24BCAN0252", space_after=1)
    add_p(doc, "Bachelor of Computer Application (BCA), 5th Semester\nDepartment of Computer Application, JECRC University, Jaipur", italic=True)

    doc.add_page_break()

    # ==========================================
    # 5. TABLE OF CONTENTS
    # ==========================================
    add_heading_1(doc, "TABLE OF CONTENTS", align=WD_ALIGN_PARAGRAPH.CENTER)

    toc_headers = ["Chapter", "Title / Section", "Page No."]
    toc_data = [
        ["", "Cover Page", get_p("Cover Page", "1")],
        ["", "Candidate Declaration", get_p("Candidate Declaration", "2")],
        ["", "Major Project Completion Certificate", get_p("Major Project Completion Certificate", "3")],
        ["", "Acknowledgement", get_p("Acknowledgement", "4")],
        ["", "List of Tables", get_p("List of Tables", "7")],
        ["", "List of Figures", get_p("List of Figures", "8")],
        ["Chapter 1", "Problem Definition & Introduction", get_p("Chapter 1", "9")],
        ["", "1.1 Digital Health & Fitness Industry Overview", get_p("1.1", "9")],
        ["", "1.2 Critical Deficiencies in Contemporary Fitness Solutions", get_p("1.2", "10")],
        ["", "1.3 Introduction to the AuraFIT Architecture", get_p("1.3", "11")],
        ["", "1.4 Need for the AuraFIT Platform", get_p("1.4", "12")],
        ["", "1.5 Purpose and Architectural Scope", get_p("1.5", "13")],
        ["Chapter 2", "Project Objectives & Requirements Specification", get_p("Chapter 2", "14")],
        ["", "2.1 Core Project Objectives", get_p("2.1", "14")],
        ["", "2.2 Target Demographics & User Personas", get_p("2.2", "15")],
        ["", "2.3 Functional Requirements Specification (FRS)", get_p("2.3", "16")],
        ["", "2.4 Non-Functional Requirements Specification (NFRS)", get_p("2.4", "17")],
        ["Chapter 3", "System Study & Feasibility Analysis", get_p("Chapter 3", "18")],
        ["", "3.1 Multi-Dimensional Feasibility Study", get_p("3.1", "18")],
        ["", "3.2 Cost-Benefit Analysis Matrix", get_p("3.2", "19")],
        ["", "3.3 Fact-Finding & Competitive Benchmarking", get_p("3.3", "20")],
        ["", "3.4 System Overview & Decoupled 3-Tier Architecture", get_p("3.4", "21")],
        ["", "3.5 User Roles, Privileges & RBAC Matrix", get_p("3.5", "22")],
        ["Chapter 4", "Mathematical Models & Algorithmic Foundations", get_p("Chapter 4", "23")],
        ["", "4.1 Deterministic Metabolic Rate Computations (BMR & TDEE)", get_p("4.1", "23")],
        ["", "4.2 Caloric Delta & Macronutrient Partitioning Model", get_p("4.2", "24")],
        ["", "4.3 Algorithmic 4-Bucket Meal Plan Generation Engine", get_p("4.3", "25")],
        ["", "4.4 Food Ranking Heuristic & Nutrient Density Index", get_p("4.4", "26")],
        ["", "4.5 Resistance Training Volume & Progressive Overload Tracking", get_p("4.5", "27")],
        ["Chapter 5", "AI Engine & Google Gemini Tool Orchestration", get_p("Chapter 5", "28")],
        ["", "5.1 Architectural Segregation: Determinism vs. LLM Generation", get_p("5.1", "28")],
        ["", "5.2 Server-Side AI Orchestration Pipeline", get_p("5.2", "29")],
        ["", "5.3 Gemini Tool Declarations & JSON Schema Definitions", get_p("5.3", "30")],
        ["", "5.4 Anti-Hallucination Guardrails & Mathematical Verification", get_p("5.4", "31")],
        ["Chapter 6", "Data Flow Diagrams & System Workflows", get_p("Chapter 6", "32")],
        ["", "6.1 Level 0: Context-Level DFD", get_p("6.1", "32")],
        ["", "6.2 Level 1: Subsystem Decomposition DFD", get_p("6.2", "33")],
        ["", "6.3 Level 2: Detailed Process Flows (Nutrition, Workouts, AI)", get_p("6.3", "34")],
        ["", "6.4 Sequence Diagrams for Critical User Transactions", get_p("6.4", "35")],
        ["Chapter 7", "Database Architecture & Data Dictionary", get_p("Chapter 7", "36")],
        ["", "7.1 Cloud NoSQL Document Architecture (MongoDB Atlas)", get_p("7.1", "36")],
        ["", "7.2 Comprehensive Data Dictionaries (10 Collections)", get_p("7.2", "37")],
        ["", "7.3 Database Indexing & Query Optimization Strategy", get_p("7.3", "42")],
        ["Chapter 8", "RESTful API Specifications & Endpoint Contracts", get_p("Chapter 8", "43")],
        ["", "8.1 API Architectural Design & OpenAPI Standards", get_p("8.1", "43")],
        ["", "8.2 Authentication & User Endpoints", get_p("8.2", "44")],
        ["", "8.3 Biometric Profile & Target Endpoints", get_p("8.3", "45")],
        ["", "8.4 Master Foods & Nutrition Plan Endpoints", get_p("8.4", "46")],
        ["", "8.5 Exercises & Workout Logging Endpoints", get_p("8.5", "47")],
        ["", "8.6 Conversational AI Coach Endpoint", get_p("8.6", "48")],
        ["Chapter 9", "System Development Life Cycle (SDLC) & Management", get_p("Chapter 9", "49")],
        ["", "9.1 Agile Scrum Methodology & Sprint Cadence", get_p("9.1", "49")],
        ["", "9.2 Work Breakdown Structure (WBS) & Milestones", get_p("9.2", "50")],
        ["", "9.3 Project Scheduling & Phase Breakdown Timeline", get_p("9.3", "51")],
        ["", "9.4 Effort Estimation & Person-Hour Allocations", get_p("9.4", "52")],
        ["Chapter 10", "Exhaustive Testing & Quality Assurance", get_p("Chapter 10", "53")],
        ["", "10.1 8-Tier Testing Strategy", get_p("10.1", "53")],
        ["", "10.2 Unit Testing of Deterministic Mathematical Models", get_p("10.2", "54")],
        ["", "10.3 Integration & API Verification", get_p("10.3", "55")],
        ["", "10.4 Functional Test Cases Matrix (20 Test Scenarios)", get_p("10.4", "56")],
        ["", "10.5 Security, OWASP Top 10 & Vulnerability Audits", get_p("10.5", "58")],
        ["", "10.6 Performance Benchmarks & User Acceptance Testing", get_p("10.6", "59")],
        ["Chapter 11", "Production Source Code Implementation", get_p("Chapter 11", "60")],
        ["", "11.1 Backend Core Entrypoint (`main.py`)", get_p("11.1", "60")],
        ["", "11.2 Cryptographic Security & JWT (`security.py`)", get_p("11.2", "61")],
        ["", "11.3 AI Orchestrator & Gemini Tools (`ai_service.py`)", get_p("11.3", "62")],
        ["Chapter 12", "Visual Interfaces, Screenshots & User Manual", get_p("Chapter 12", "64")],
        ["", "12.1 Visual Interface Catalog (Figures 12.1 to 12.10)", get_p("12.1", "64")],
        ["", "12.2 Operational User Manual & Step-by-Step Walkthrough", get_p("12.2", "66")],
        ["Chapter 13", "Limitations, Future Enhancements & Conclusion", get_p("Chapter 13", "68")],
        ["", "13.1 Technical and Operational Limitations", get_p("13.1", "68")],
        ["", "13.2 Strategic Future Enhancements Roadmap", get_p("13.2", "69")],
        ["", "13.3 Project Summary & Academic Conclusion", get_p("13.3", "70")],
        ["", "References & Bibliography", get_p("References", "71")]
    ]
    create_table(doc, toc_headers, toc_data, [Inches(1.2), Inches(4.3), Inches(1.0)])

    doc.add_page_break()

    # ==========================================
    # 6. LIST OF TABLES
    # ==========================================
    add_heading_1(doc, "LIST OF TABLES", align=WD_ALIGN_PARAGRAPH.CENTER)
    lot_headers = ["Table No.", "Table Caption", "Page No."]
    lot_data = [
        ["Table 2.1", "Functional Requirements Specification Matrix", get_p("Table 2.1", "16")],
        ["Table 2.2", "Non-Functional Requirements Standards Matrix", get_p("Table 2.2", "17")],
        ["Table 3.1", "Economic Feasibility & Cost-Benefit Analysis Matrix", get_p("Table 3.1", "19")],
        ["Table 3.2", "Competitive Benchmarking: AuraFIT vs. Existing Platforms", get_p("Table 3.2", "20")],
        ["Table 3.3", "Role-Based Access Control (RBAC) Permissions Matrix", get_p("Table 3.3", "22")],
        ["Table 4.1", "Physical Activity Level (PAL) Multipliers and Descriptions", get_p("Table 4.1", "24")],
        ["Table 4.2", "Goal-Based Caloric Delta and Macro Split Allocation", get_p("Table 4.2", "25")],
        ["Table 4.3", "4-Bucket Meal Plan Daily Calorie & Macro Target Split", get_p("Table 4.3", "26")],
        ["Table 5.1", "Google Gemini Tool Declarations & Input/Output Schemas", get_p("Table 5.1", "30")],
        ["Table 7.1", "Data Dictionary: Users Collection Schema", get_p("Table 7.1", "37")],
        ["Table 7.2", "Data Dictionary: Profiles Collection Schema", get_p("Table 7.2", "37")],
        ["Table 7.3", "Data Dictionary: Foods Master Catalog Collection Schema", get_p("Table 7.3", "38")],
        ["Table 7.4", "Data Dictionary: Exercises Master Catalog Collection Schema", get_p("Table 7.4", "39")],
        ["Table 7.5", "Data Dictionary: Meal Plans Collection Schema", get_p("Table 7.5", "39")],
        ["Table 7.6", "Data Dictionary: Saved Meals Collection Schema", get_p("Table 7.6", "40")],
        ["Table 7.7", "Data Dictionary: Workout Plans Collection Schema", get_p("Table 7.7", "40")],
        ["Table 7.8", "Data Dictionary: Daily Logs Tracking Collection Schema", get_p("Table 7.8", "41")],
        ["Table 7.9", "Data Dictionary: Body Measurements Collection Schema", get_p("Table 7.9", "41")],
        ["Table 7.10", "Data Dictionary: User Achievements Collection Schema", get_p("Table 7.10", "42")],
        ["Table 8.1", "Authentication & Session Management Endpoints", get_p("Table 8.1", "44")],
        ["Table 8.2", "Biometric Profile & Target Management Endpoints", get_p("Table 8.2", "45")],
        ["Table 8.3", "Food Catalog & Meal Management Endpoints", get_p("Table 8.3", "46")],
        ["Table 8.4", "Exercise Catalog & Workout Logging Endpoints", get_p("Table 8.4", "47")],
        ["Table 8.5", "Conversational AI Coach API Endpoints", get_p("Table 8.5", "48")],
        ["Table 9.1", "AuraFIT 15-Week Agile Sprint Cadence & Deliverables", get_p("Table 9.1", "50")],
        ["Table 9.2", "Project Phase Breakdown, Timeline & Milestones", get_p("Table 9.2", "51")],
        ["Table 9.3", "Effort Estimations by Phase in Person-Hours", get_p("Table 9.3", "52")],
        ["Table 10.1", "Deterministic Mathematical Engine Unit Test Cases", get_p("Table 10.1", "54")],
        ["Table 10.2", "Comprehensive Functional Test Scenarios (TC-01 to TC-20)", get_p("Table 10.2", "56")]
    ]
    create_table(doc, lot_headers, lot_data, [Inches(1.2), Inches(4.3), Inches(1.0)])

    doc.add_page_break()

    # ==========================================
    # 7. LIST OF FIGURES
    # ==========================================
    add_heading_1(doc, "LIST OF FIGURES", align=WD_ALIGN_PARAGRAPH.CENTER)
    lof_headers = ["Figure No.", "Figure Caption", "Page No."]
    lof_data = [
        ["Figure 3.1", "AuraFIT Decoupled 3-Tier Enterprise Architecture", get_p("Figure 3.1", "21")],
        ["Figure 5.1", "Server-Side Google Gemini AI Orchestration Flow", get_p("Figure 5.1", "29")],
        ["Figure 6.1", "Context-Level Data Flow Diagram (DFD Level 0)", get_p("Figure 6.1", "32")],
        ["Figure 6.2", "Subsystem Decomposition Data Flow Diagram (DFD Level 1)", get_p("Figure 6.2", "33")],
        ["Figure 6.3", "Nutrition Logging & AI Meal Swap Process Flow (DFD Level 2)", get_p("Figure 6.3", "34")],
        ["Figure 6.4", "Sequence Diagram: User Authentication & JWT Exchange", get_p("Figure 6.4", "35")],
        ["Figure 12.1", "AuraFIT Landing Page Portal & Editorial Aesthetics", get_p("Figure 12.1", "64")],
        ["Figure 12.2", "Comprehensive Biometric Onboarding & Goal Selection", get_p("Figure 12.2", "64")],
        ["Figure 12.3", "Daily Overview Dashboard & Radial Macro Progress Rings", get_p("Figure 12.3", "65")],
        ["Figure 12.4", "Master Food Catalog & Multi-Criteria Filter Interface", get_p("Figure 12.4", "65")],
        ["Figure 12.5", "Algorithmic 4-Bucket Meal Planner & Daily Schedule", get_p("Figure 12.5", "65")],
        ["Figure 12.6", "AI Ingredient Swap Modal with Mathematical Parity", get_p("Figure 12.6", "66")],
        ["Figure 12.7", "Exercise Library with Anatomical Muscle Categorization", get_p("Figure 12.7", "66")],
        ["Figure 12.8", "Active Workout Logger & Progressive Overload Tracking", get_p("Figure 12.8", "67")],
        ["Figure 12.9", "Conversational AI Fitness Coach (AICoachChat)", get_p("Figure 12.9", "67")],
        ["Figure 12.10", "Longitudinal Biometric Trends & Body Weight Analytics", get_p("Figure 12.10", "67")]
    ]
    create_table(doc, lof_headers, lof_data, [Inches(1.2), Inches(4.3), Inches(1.0)])

    doc.add_page_break()
