# -*- coding: utf-8 -*-
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def generate_aurafit_report():
    doc = docx.Document()

    # Page Margins: 1 inch all around as specified by the user
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Normal Style: Times New Roman, 12pt, 1.5 line spacing, 6pt after
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/>'
            f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/>'
            f'<w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_h(text, level=1, space_before=12, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        if level == 1:
            run.font.size = Pt(16)
        elif level == 2:
            run.font.size = Pt(14)
        elif level == 3:
            run.font.size = Pt(12)
        return p

    def add_p(text="", bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6, line_spacing=1.5):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.bold = bold
            run.italic = italic
            run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        run1 = p.add_run(bold_prefix + ": ")
        run1.font.name = 'Times New Roman'
        run1.font.size = Pt(12)
        run1.bold = True
        run1.font.color.rgb = RGBColor(0, 0, 0)

        run2 = p.add_run(text)
        run2.font.name = 'Times New Roman'
        run2.font.size = Pt(12)
        run2.bold = False
        run2.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_numbered(num_str, bold_prefix, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.left_indent = Inches(0.25)
        
        run_num = p.add_run(num_str + " ")
        run_num.font.name = 'Times New Roman'
        run_num.font.size = Pt(12)
        run_num.bold = True

        run_pre = p.add_run(bold_prefix + ": ")
        run_pre.font.name = 'Times New Roman'
        run_pre.font.size = Pt(12)
        run_pre.bold = True

        run_txt = p.add_run(text)
        run_txt.font.name = 'Times New Roman'
        run_txt.font.size = Pt(12)
        return p

    def add_code(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F7F9FA")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
            f'<w:left w:val="single" w:sz="18" w:space="0" w:color="0969DA"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_text.strip())
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(36, 41, 47)

    def create_table(headers, data, col_widths):
        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)

        # Header Row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].width = col_widths[i]
            set_cell_background(hdr_cells[i], "EAECEF")
            set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(header_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            run.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Data Rows
        for row_idx, row_data in enumerate(data):
            row_cells = table.rows[row_idx + 1].cells
            bg_color = "F9FAFB" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, cell_value in enumerate(row_data):
                row_cells[col_idx].width = col_widths[col_idx]
                set_cell_background(row_cells[col_idx], bg_color)
                set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)
                p = row_cells[col_idx].paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(2)
                if col_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = p.add_run(str(cell_value))
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==========================================
    # 1. COVER PAGE
    # ==========================================
    p_title_pre = add_p("A", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p_title_pre.runs[0].font.size = Pt(14)
    
    p_major = add_p("Major Project", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p_major.runs[0].font.size = Pt(16)
    
    p_on = add_p("On", bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    p_on.runs[0].font.size = Pt(13)
    
    p_proj = add_p('“AuraFIT: AI-POWERED PERSONALIZED FITNESS & NUTRITION PLATFORM”', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    p_proj.runs[0].font.size = Pt(18)
    
    p_part = add_p("In Partial Fulfillment for the award of the Degree Of", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p_part.runs[0].font.size = Pt(13)
    
    p_deg = add_p("Bachelor Of Computer Application (BCA)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=20)
    p_deg.runs[0].font.size = Pt(15)

    # University Name Header Block
    p_univ = add_p("JECRC UNIVERSITY", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p_univ.runs[0].font.size = Pt(22)
    
    p_tag = add_p("BUILD YOUR WORLD", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)
    p_tag.runs[0].font.size = Pt(12)

    # 2-column table for Guides & Student
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
    r2 = p_gl.add_run("Prof. Dr. Deepak Dembla\nMs. Rashi Jain\n(Assistant Professor)\nDepartment of Computer Application")
    r2.bold = False
    r2.font.size = Pt(11)
    
    p_gr = c_right.paragraphs[0]
    p_gr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_gr.paragraph_format.line_spacing = 1.3
    p_gr.paragraph_format.space_after = Pt(2)
    r3 = p_gr.add_run("Submitted By:\n")
    r3.bold = True
    r3.font.size = Pt(11)
    r4 = p_gr.add_run("Ved Gupta\nRoll No: 24BCAN0252\nBCA 5th Semester\nDepartment of Computer Application")
    r4.bold = False
    r4.font.size = Pt(11)

    p_bot1 = add_p("Department of Computer Application", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p_bot1.paragraph_format.space_before = Pt(40)
    p_bot1.runs[0].font.size = Pt(12)
    p_bot2 = add_p("JECRC UNIVERSITY, JAIPUR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p_bot2.runs[0].font.size = Pt(13)
    p_bot3 = add_p("2024–2027", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    p_bot3.runs[0].font.size = Pt(12)

    doc.add_page_break()

    # ==========================================
    # 2. CANDIDATE DECLARATION
    # ==========================================
    add_h("CANDIDATE DECLARATION", level=1, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14)

    add_p("I hereby declare that the project work titled “AuraFIT: AI-POWERED PERSONALIZED FITNESS & NUTRITION PLATFORM”, submitted as part of my academic requirement, is a record of my own work carried out under the guidance of Prof. Dr. Deepak Dembla and Ms. Rashi Jain (Assistant Professor). This project has been completed in partial fulfillment of the requirements for Bachelor of Computer Application (BCA) at JECRC University.")

    add_p("I further declare that this project has not been submitted to any other university or institution for the award of any degree, diploma, or certificate. All sources of information and data used in this project have been acknowledged appropriately.")

    add_p("I understand that any breach of this declaration will result in the rejection of this project and disciplinary action.")

    add_p("Name of the Student:", bold=True, space_after=1)
    add_p("Ved Gupta", space_after=6)

    add_p("Roll Number:", bold=True, space_after=1)
    add_p("24BCAN0252", space_after=6)

    add_p("Course and Semester:", bold=True, space_after=1)
    add_p("Bachelor of Computer Application (BCA), 5th Semester", space_after=6)

    add_p("Name(s) of Supervisor(s)/Guide(s):", bold=True, space_after=1)
    add_p("Prof. Dr. Deepak Dembla\nMs. Rashi Jain (Assistant Professor)", space_after=6)

    add_p("Submission Date:", bold=True, space_after=1)
    add_p("January, 2027", space_after=24)

    add_p("Signature: __________________________", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=0)

    doc.add_page_break()

    # ==========================================
    # 3. MAJOR PROJECT COMPLETION CERTIFICATE
    # ==========================================
    add_h("JECRC UNIVERSITY", level=1, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p("Department of Computer Application", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    add_h("Major Project Completion Certificate", level=2, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)

    add_p("This is to certify that Mr. Ved Gupta, Registration No: 24BCAN0252, has successfully completed the Major Project as a Part of the requirement for the Bachelor of Computer Application (BCA) Program at JECRC UNIVERSITY, Jaipur, India.")

    add_p("Project Title: AuraFIT: AI-Powered Personalized Fitness & Nutrition Platform", bold=True)
    add_p("Technology Used: React, TypeScript, Tailwind CSS, Python, FastAPI, Motor (Async MongoDB), MongoDB Atlas, Google Gemini API.", bold=True)
    add_p("Project Supervisor: Prof. Dr. Deepak Dembla and Ms. Rashi Jain (Assistant Professor)", bold=True)

    add_p("This project demonstrates student’s ability to apply theoretical knowledge gained during his/her academic to practical real-world scenarios. His/her dedication, hard work, and proficiency in the subject matter is commendable.")

    # Signatures
    tbl_cert = doc.add_table(rows=1, cols=2)
    tbl_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_hod = tbl_cert.cell(0, 0)
    c_sup = tbl_cert.cell(0, 1)
    c_hod.width = Inches(3.25)
    c_sup.width = Inches(3.25)
    
    p_hod = c_hod.paragraphs[0]
    p_hod.paragraph_format.space_before = Pt(60)
    p_hod.paragraph_format.line_spacing = 1.2
    r_h1 = p_hod.add_run("_________________________\n")
    r_h2 = p_hod.add_run("Mr. Shekhar Chander\nHoD, Department of Computer Application\nJECRC University, Jaipur")
    r_h2.bold = True
    r_h2.font.size = Pt(11)

    p_sup = c_sup.paragraphs[0]
    p_sup.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sup.paragraph_format.space_before = Pt(60)
    p_sup.paragraph_format.line_spacing = 1.2
    r_s1 = p_sup.add_run("_________________________\n")
    r_s2 = p_sup.add_run("Project Supervisor\nProf. Dr. Deepak Dembla / Ms. Rashi Jain\nDepartment of Computer Application")
    r_s2.bold = True
    r_s2.font.size = Pt(11)

    doc.add_page_break()

    # ==========================================
    # 4. ACKNOWLEDGEMENT
    # ==========================================
    add_h("ACKNOWLEDGEMENT", level=1, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14)

    add_p('I am sincerely grateful to everyone who contributed to the successful completion of my project, "AuraFIT: AI-Powered Personalized Fitness & Nutrition Platform".')

    add_p("First and foremost, I would like to express my heartfelt gratitude to my project guides, Prof. Dr. Deepak Dembla and Ms. Rashi Jain (Assistant Professor), for their invaluable guidance, encouragement, and support throughout this project. Their expertise, continuous mentoring, and constructive feedback helped me refine my architectural ideas and bring this platform to fruition.")

    add_p("I would also like to thank Mr. Shekhar Chander, Head of the Department, and all the respected faculty members of the Department of Computer Application at JECRC University for providing me with the essential knowledge, computing resources, and academic environment necessary to undertake this ambitious project.")

    add_p("Additionally, I am deeply thankful to my classmates and friends for their collaboration, insightful discussions, and peer testing, which significantly enhanced the scope, usability, and quality of my work.")

    add_p("Finally, I would like to extend my deepest appreciation to my family for their unwavering support, moral encouragement, and constant belief in my capabilities during this intensive development process.")

    add_p("This project has been an invaluable learning experience in developing full-stack decoupled enterprise systems, integrating cutting-edge generative AI models safely with deterministic mathematics, and I am truly thankful for all the guidance and support I received.")

    add_p("Ved Gupta", bold=True, space_after=1)
    add_p("24BCAN0252", space_after=1)
    add_p("BCA 5th Semester, JECRC University, Jaipur", italic=True)

    doc.add_page_break()

    # ==========================================
    # 5. TABLE OF CONTENT
    # ==========================================
    add_h("TABLE OF CONTENT", level=1, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14)

    toc_headers = ["SR. No.", "Section", "Page No."]
    toc_data = [
        ["1", "Cover Page", "1"],
        ["2", "Declaration", "2"],
        ["3", "Major Project Completion Certificate", "3"],
        ["4", "Acknowledgement", "4"],
        ["5", "Problem Definition", "6"],
        ["6", "Objective", "9"],
        ["7", "System Study", "10"],
        ["8", "System Analysis", "20"],
        ["9", "System Development Cycle (SDLC)", "28"],
        ["10", "Context Level DFD", "32"],
        ["11", "Data Dictionary", "36"],
        ["12", "Source Code", "43"],
        ["13", "Output / Visual Interfaces", "56"],
        ["14", "Limitations And Future Enhancements", "60"]
    ]
    create_table(toc_headers, toc_data, [Inches(1.0), Inches(4.3), Inches(1.2)])

    doc.add_page_break()

    # ==========================================
    # SECTION 1: PROBLEM DEFINITION
    # ==========================================
    add_h("1. Problem Definition", level=1, space_before=0, space_after=8)
    
    add_p("The modern wellness and preventive health ecosystem is undergoing a dramatic shift toward digital platforms. However, existing fitness applications suffer from severe architectural limitations, leading to high user drop-off rates and suboptimal or even hazardous health outcomes. The primary issues plaguing contemporary fitness solutions include:")

    add_bullet("Prevalence of Generic, Static Plans", "Most digital health applications rely on static templates that assign identical calorie targets and macro splits regardless of an individual's unique metabolic profile, lean body mass, dynamic activity levels, or biochemical adaptations.")

    add_bullet("Dangers of Unchecked AI Hallucinations", "With the recent advent of Large Language Models (LLMs), many fitness startups have directly plugged chatbots into user prompts. LLMs are probabilistic text engines and inherently incapable of exact mathematical arithmetic. Consequently, they regularly hallucinate dangerous calorie targets, mathematically inconsistent macronutrient totals, and medically contraindicated dietary recommendations.")

    add_bullet("Cultural Disconnect in Dietary Databases", "Leading international fitness applications (e.g., MyFitnessPal, Cronometer) feature databases heavily biased toward Western dietary staples. They fail to accurately capture the nutritional nuances of Indian and South Asian cuisines, such as regional dals, subzis, cooked rotis, paneer preparations, and plant-based protein combinations.")

    add_bullet("Platform Fragmentation", "Users are forced to juggle multiple disjointed applications: one for tracking food intake, another for logging resistance workouts, and a third for consulting nutritionists or seeking motivation.")

    add_p("This project addresses these critical problems by architecting and developing AuraFIT—an enterprise-grade, culturally aware, AI-powered fitness and nutrition platform. AuraFIT establishes a strict architectural boundary: deterministic, clinically proven formulas (Mifflin-St Jeor equation and standard exercise volume formulas) perform all metabolic calculations on the authoritative FastAPI backend, while Google's Gemini API is integrated purely as a context-aware assistant for structured meal swapping, recipe formulation, and workout modifications.")

    add_h("1.1 INTRODUCTION", level=2, space_before=10, space_after=6)
    add_p("AuraFIT is an advanced, full-stack health platform designed to democratize scientific, personalized fitness and nutrition coaching. Built on modern web technologies including React, TypeScript, Tailwind CSS, Python FastAPI, and MongoDB Atlas, AuraFIT bridges the gap between clinical nutrition science and engaging consumer software.")

    add_p("In today’s fast-paced digital era, the demand for personalized, instantaneous, and scientifically validated health coaching has surged. AuraFIT provides an intuitive single-page application (SPA) where users can seamlessly complete comprehensive onboarding (capturing age, biological sex, height, weight, activity multiplier, dietary preferences, and fitness goals). The platform instantly derives Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), and granular macronutrient targets (protein, carbohydrates, and fats in grams and calories).")

    add_p("Furthermore, AuraFIT leverages the state-of-the-art Google Gemini API through server-side function calling. This ensures that when a user requests an alternative for a high-fat item or an adjustment to their workout routine due to muscle fatigue, the AI orchestrator queries the internal database for verified food items and structured parameters rather than hallucinating arbitrary nutritional figures. AuraFIT delivers a refined, editorial-grade user interface that prioritizes clarity, usability, and speed.")

    add_h("1.2 Need", level=2, space_before=10, space_after=6)
    add_p("The necessity for this project stems from the urgent requirement for reliable, evidence-based digital health tools. The specific needs addressed by AuraFIT include:")

    add_bullet("Enhanced Mathematical Precision", "A critical need exists to separate mathematical nutrition calculations from generative text models. AuraFIT guarantees 100% mathematical accuracy for all caloric and macronutrient allocations.")

    add_bullet("Culturally-Contextualized Nutrition", "Indian dietary habits encompass rich regional cuisines with unique macronutrient balances. AuraFIT provides a rich, verified database of regional foods, making it practical for Indian and global users to hit target macros without abandoning cultural cuisines.")

    add_bullet("Smart Ingredient & Meal Swapping", "When users lack specific ingredients or dine out, AuraFIT dynamically calculates identical macro swaps using intelligent backend tool execution, ensuring diet adherence without rigidity.")

    add_bullet("Unified Fitness & Strength Tracking", "Combines nutrition tracking with progressive overload workout logging (sets, reps, weights, muscle groups), eliminating the need for fragmented third-party apps.")

    add_bullet("Data Security & Scalable Persistence", "Guarantees data confidentiality using modern Argon2 password hashing and stateless JWT bearer tokens, storing complex nested meal and workout logs in MongoDB Atlas.")

    add_bullet("Interactive AI Motivation & Guidance", "Empowers users with an empathetic, 24/7 AI fitness coach that understands their specific context (recent workouts, remaining macros, dietary allergies) without exposing API keys to the browser.")

    add_h("1.3 Purpose", level=2, space_before=10, space_after=6)
    add_p("The purpose of this project is to design and develop a comprehensive web application that reflects the highest standards of software architecture and clinical fitness principles. Key objectives include:")

    add_bullet("Deterministic Calculation Engine", "Implement automated, clinically validated formulas for BMR, TDEE, and goal-specific macronutrient partitioning.")

    add_bullet("Modern Responsive Web Interface", "Develop a high-performance React application using TypeScript, Tailwind CSS, and TanStack Query for instantaneous data caching and seamless device responsiveness.")

    add_bullet("Secure AI Integration", "Orchestrate Google Gemini API exclusively through backend micro-services using structured Pydantic schemas and strict function declarations.")

    add_bullet("Comprehensive Database Schema", "Utilize MongoDB's flexible document model to efficiently represent complex nested food logs, workout sets, user metrics, and historical progress.")

    add_bullet("Continuous Progress Analytics", "Deliver interactive data visualizations (using Recharts) for tracking body weight trajectories, daily caloric adherence, and muscle group volume.")

    # ==========================================
    # SECTION 2: OBJECTIVE
    # ==========================================
    add_h("2. Objective", level=1, space_before=14, space_after=8)
    add_p("The objective of this project is to engineer and deploy a production-ready, highly reliable web platform for AuraFIT that unites modern full-stack development with state-of-the-art AI. The detailed objectives include:")

    add_bullet("Create a Unified Digital Wellness Hub", "Develop an intuitive web platform where users manage all aspects of physical fitness, daily nutrition, body biometrics, and motivational coaching in a single ecosystem.")

    add_bullet("Deterministic Metabolic Calculations", "Implement the Mifflin-St Jeor metabolic algorithm and dynamic physical activity level (PAL) multipliers to compute exact daily caloric requirements, eliminating generative arithmetic errors.")

    add_bullet("Context-Aware Generative AI Features", "Integrate Google Gemini API to offer conversational coaching, intelligent meal modifications, and workout substitutions that strictly adhere to user-specific allergy, dietary, and caloric constraints.")

    add_bullet("Curate an Authoritative Food & Exercise Database", "Build structured database collections featuring rich Indian and continental cuisine items alongside verified multi-muscle resistance and cardiovascular exercises.")

    add_bullet("Empower User Habit Adherence", "Provide responsive daily dashboards displaying dynamic macro progress rings, remaining calories, meal completion checkboxes, and workout progression logging.")

    add_bullet("Ensure Enterprise-Grade Security", "Implement robust user authentication utilizing Argon2 password hashing, time-limited JSON Web Tokens (JWT), role-based endpoint authorization, and CORS policy enforcement.")

    add_bullet("Deliver Decoupled Architecture", "Maintain an architectural separation of concerns between client (React SPA) and server (FastAPI REST API), enabling independent scaling, testing, and deployment.")

    add_bullet("Longitudinal Visual Analytics", "Enable historical tracking of biometric data (weight, waist measurements, body fat percentage) through dynamic charts to provide actionable health insights.")

    # ==========================================
    # SECTION 3: SYSTEM STUDY
    # ==========================================
    add_h("3. System Study", level=1, space_before=14, space_after=8)
    add_p("The system study represents an in-depth investigation into existing digital fitness solutions, user requirements, technical feasibility, and architectural parameters necessary to build AuraFIT.")

    add_h("3.1 Feasibility Study", level=2, space_before=10, space_after=6)
    add_p("The feasibility study evaluates the practical viability of AuraFIT across five critical dimensions: economic, operational, technical, motivational, and schedule.")

    add_h("3.1.1 Economic Feasibility", level=3, space_before=6, space_after=4)
    add_p("Economic feasibility assesses the total development, hosting, and ongoing infrastructure expenditure against expected technological value:")
    add_bullet("Development Costs", "Built utilizing free, open-source technologies (Python, React, TypeScript, FastAPI, Tailwind CSS), eliminating software licensing fees.")
    add_bullet("Cloud Infrastructure", "Leverages MongoDB Atlas's free/M0 tier and serverless deployment platforms (e.g., Render/Vercel), minimizing hosting costs during the academic and prototype lifecycle.")
    add_bullet("AI API Cost Optimization", "By isolating Gemini calls strictly to contextual advisory and tool-calling queries—rather than relying on LLMs for static database queries or basic arithmetic—API token consumption is minimized by over 80%.")

    add_h("3.1.2 Operational Feasibility", level=3, space_before=6, space_after=4)
    add_p("Operational feasibility examines how easily end users can adopt and integrate the platform into their daily routine. AuraFIT provides an intuitive onboarding flow requiring zero prior fitness knowledge. The user interface abstracts all complex calculations into visual progress bars, allowing users to log meals and workouts with minimal clicks.")

    add_h("3.1.3 Technical Feasibility", level=3, space_before=6, space_after=4)
    add_p("Technical feasibility examines the technologies selected for the stack:")
    add_bullet("FastAPI Backend", "Provides asynchronous request processing, automatic OpenAPI documentation, and native Pydantic schema validation for blazing-fast responses.")
    add_bullet("React with Vite & TypeScript", "Ensures strict compile-time type safety, rapid Hot Module Replacement (HMR), and lightning-fast client rendering.")
    add_bullet("MongoDB Atlas", "Offers native JSON document storage, making it effortless to store dynamic arrays of ingredients, meal plans, and workout logs without complex relational join overhead.")
    add_bullet("Google Gemini API", "Delivers advanced reasoning capabilities and function calling to interact with backend services securely.")

    add_h("3.1.4 Motivational Feasibility", level=3, space_before=6, space_after=4)
    add_p("Motivational feasibility evaluates user engagement. By delivering transparent calculations, daily streaks, dynamic progress feedback, and an encouraging AI coach, users remain motivated to maintain long-term dietary and fitness habits.")

    add_h("3.1.5 Schedule Feasibility", level=3, space_before=6, space_after=4)
    add_p("The project schedule was designed around academic milestones across a 15-week sprint cycle, ensuring sufficient time for requirements gathering, architecture definition, prototyping, integration, testing, and documentation.")

    add_h("3.2 Cost and Benefit Analysis for AuraFIT", level=2, space_before=10, space_after=6)
    add_p("A rigorous cost and benefit analysis confirms that the proposed AuraFIT architecture yields substantial operational advantages while maintaining negligible operating expenses.")

    add_h("3.2.1 Cost Analysis", level=3, space_before=6, space_after=4)
    add_bullet("Infrastructure Hosting", "MongoDB Atlas (Free tier), Frontend static hosting (Vercel/Netlify free tier), Backend API hosting on cloud containers ($0 to nominal tier).")
    add_bullet("AI Service Costs", "Google Gemini API offers a generous free tier for academic development and highly competitive per-token pricing thereafter.")
    add_bullet("Maintenance & Tooling", "Modern Git-based CI/CD workflows and pytest automation eliminate ongoing testing overhead.")

    add_h("3.2.2 Benefit Analysis", level=3, space_before=6, space_after=4)
    add_bullet("Zero Hallucination Risk", "Deterministic calculations prevent dangerous nutritional guidance.")
    add_bullet("High User Retention", "Culturally specific food items ensure long-term usability for diverse demographics.")
    add_bullet("Rapid Performance", "Async FastAPI server handles multiple concurrent user requests with sub-100ms response times for database operations.")

    add_h("3.3 Fact Findings of AuraFIT", level=2, space_before=10, space_after=6)
    add_p("During the fact-finding phase, multiple commercial fitness applications were surveyed:")
    add_bullet("MyFitnessPal", "Large database but highly cluttered with duplicate user-submitted entries, paywalled barcode scanning, and zero culturally tailored Indian macro balancing.")
    add_bullet("HealthifyMe", "Provides Indian food entries but restricts personalized AI advice behind expensive premium human-coach tiers.")
    add_bullet("Generic LLM Chatbots (ChatGPT/Claude)", "Provide conversational advice but regularly fail at basic macro arithmetic (e.g., claiming 100g of chicken contains 60g protein) and lack persistent memory of user daily logs.")

    add_h("3.4 System Overview of AuraFIT", level=2, space_before=10, space_after=6)
    add_p("AuraFIT adopts a modern decoupled client-server architecture designed for high availability, modularity, and rapid responsiveness.")

    add_h("3.4.1 System Components", level=3, space_before=6, space_after=4)
    add_bullet("Frontend Single-Page Application (SPA)", "Built with React, TypeScript, Vite, and Tailwind CSS. Employs TanStack Query for client-side state caching and React Router for smooth navigation.")
    add_bullet("Backend REST API", "Powered by Python FastAPI. Acts as the authoritative source of truth, orchestrating business logic, deterministic metabolic calculations, and database access.")
    add_bullet("Database Layer", "MongoDB Atlas document database storing user credentials, profiles, foods, exercises, meal logs, and workout sessions.")
    add_bullet("AI Orchestration Service", "Server-side integration with Google Gemini API using function calling to bind database tools to generative prompts.")

    add_h("3.4.2 Key Features of the System", level=3, space_before=6, space_after=4)
    add_bullet("Deterministic Macro Engine", "Calculates BMR, TDEE, and exact protein, carb, and fat gram targets based on biological metrics.")
    add_bullet("Dynamic Food & Meal Logging", "Allows searching verified foods, creating custom meals, and tracking caloric intake against daily targets.")
    add_bullet("AI Food & Ingredient Swapping", "Enables users to swap meal ingredients on-the-fly while maintaining identical macro profiles.")
    add_bullet("Workout Planner & Log Tracker", "Provides an exercise library categorized by muscle group and difficulty, enabling users to log sets, reps, and volume.")
    add_bullet("Longitudinal Visual Analytics", "Renders interactive charts for weight tracking, caloric adherence, and body composition changes.")

    add_h("3.4.3 System Architecture", level=3, space_before=6, space_after=4)
    add_p("AuraFIT implements a decoupled 3-tier architecture:")
    add_bullet("Presentation Layer (Client)", "React/TypeScript SPA running in the user's browser, communicating with the backend exclusively via HTTPS/JSON REST APIs.")
    add_bullet("Application Logic Layer (Server)", "FastAPI backend hosting modular route controllers, dependency injection, security layers, and AI service orchestrators.")
    add_bullet("Data Persistence Layer (Database)", "MongoDB Atlas hosting collections with indexed queries and schema validation.")

    add_h("3.4.4 User Roles and Permissions", level=3, space_before=6, space_after=4)
    add_bullet("Regular User", "Access to personal profile, onboarding, daily food/workout logging, AI coach chat, and progress analytics.")
    add_bullet("Admin / Coach", "Full access to manage the master food database, add new exercise definitions, inspect platform metrics, and manage user accounts.")

    add_h("3.4.5 System Benefits", level=3, space_before=6, space_after=4)
    add_p("The AuraFIT architecture guarantees high reliability, complete mathematical transparency, robust security, and seamless user experiences across mobile and desktop devices.")

    # ==========================================
    # SECTION 4: SYSTEM ANALYSIS
    # ==========================================
    add_h("4. System Analysis", level=1, space_before=14, space_after=8)
    add_p("System analysis examines the functional, non-functional, security, and algorithmic requirements of AuraFIT to ensure robust design and execution.")

    add_h("1. Objectives of the System", level=2, space_before=10, space_after=6)
    add_bullet("User-Centric Objectives", "Deliver an intuitive, aesthetically refined interface for seamless daily logging of meals and workouts with zero learning curve.")
    add_bullet("Technical Objectives", "Maintain strict separation between deterministic calculations and LLM generation, ensuring 100% calculation accuracy.")
    add_bullet("Analytical Objectives", "Provide clear visual feedback and actionable analytics on body transformation, weight trends, and macronutrient adherence.")

    add_h("2. Functional Requirements", level=2, space_before=10, space_after=6)
    add_bullet("User Registration and Authentication", "Users can sign up with email and password, log in to receive JWT bearer tokens, and maintain secure sessions.")
    add_bullet("Profile Onboarding & Metric Setup", "Captures age, biological sex, height, weight, activity multiplier, dietary preferences, and fitness goals.")
    add_bullet("Deterministic Calculation Engine", "Computes BMR using the Mifflin-St Jeor formula, multiplies by activity level for TDEE, and applies goal-based calorie adjustments (+/- 300-500 kcal).")
    add_bullet("Food Library & Meal Logging", "Enables searching verified foods, assembling meals, logging food items, and calculating daily consumed macros.")
    add_bullet("AI-Driven Meal Swaps", "Allows users to replace individual meal ingredients with macro-equivalent alternatives via the Gemini API.")
    add_bullet("Workout Planning & Logging", "Allows scheduling workout routines, viewing exercise instructions, and recording completed sets, reps, and weights.")
    add_bullet("Conversational AI Coaching", "Provides real-time fitness advice grounded in user profile context and database tools.")

    add_h("3. Non-Functional Requirements", level=2, space_before=10, space_after=6)
    add_bullet("Performance", "API response times under 150ms for database queries; client initial page load under 1.5 seconds via Vite code splitting.")
    add_bullet("Security", "Passwords hashed using Argon2; stateless JWTs with 30-minute access token expiration and 7-day refresh tokens; strict CORS restrictions.")
    add_bullet("Usability", "Responsive layout tailored for mobile, tablet, and desktop screens; accessible color contrasts and clear typography.")
    add_bullet("Maintainability", "Domain-driven folder structure on the frontend; Controller-Service-Repository pattern on the backend; full typing with TypeScript and Pydantic.")
    add_bullet("Scalability", "Asynchronous Python I/O via Motor and FastAPI handles hundreds of concurrent user requests per second.")

    add_h("4. Data Flow Analysis", level=2, space_before=10, space_after=6)
    add_p("Data flows systematically across the presentation, logic, and persistence tiers:")
    add_bullet("Authentication Flow", "User inputs credentials -> FastAPI verifies Argon2 hash -> Issues JWT access and refresh tokens -> Client stores token in memory/secure storage.")
    add_bullet("Profile Calculation Flow", "User submits biometric parameters -> Backend executes Mifflin-St Jeor formula -> Calculates TDEE & macro splits -> Saves profile to MongoDB -> Returns calculated targets to UI.")
    add_bullet("Food Logging & AI Swap Flow", "User selects food -> Client sends request to `/api/v1/nutrition/meals` -> Backend updates daily log -> If AI swap requested, backend calls Gemini with tool declarations -> Gemini executes `find_alternative_food` -> Backend validates macro parity and returns response.")

    add_h("5. System Design Considerations", level=2, space_before=10, space_after=6)
    add_bullet("Modular Architecture", "Frontend features split into `auth`, `dashboard`, `nutrition`, `workouts`, and `ai`. Backend split into `api/routes`, `core`, `db`, `models`, and `services`.")
    add_bullet("Strict Schema Enforcement", "Pydantic models enforce data integrity on incoming HTTP payloads, MongoDB document schemas, and Gemini tool input/output formats.")

    add_h("6. Tools and Technologies", level=2, space_before=10, space_after=6)
    tech_headers = ["Layer", "Technology", "Role in AuraFIT"]
    tech_data = [
        ["Frontend UI", "React 18 + Vite", "High-performance Single Page Application with Hot Module Replacement"],
        ["Language", "TypeScript", "Static type safety across components, props, API responses, and stores"],
        ["Styling", "Tailwind CSS", "Modern, responsive, utility-first editorial styling with custom design tokens"],
        ["Client State", "TanStack Query + Zustand", "Asynchronous server-state caching, optimistic updates, and global auth state"],
        ["Backend API", "Python 3.10+ & FastAPI", "High-speed asynchronous RESTful API framework with automatic OpenAPI docs"],
        ["Data Validation", "Pydantic v2", "Data serialization, validation schemas, and LLM structured output enforcement"],
        ["Database", "MongoDB Atlas & Motor", "Fully managed cloud NoSQL database with async Python driver for non-blocking I/O"],
        ["Authentication", "Argon2 & PyJWT", "Modern cryptographic password hashing and JSON Web Token session management"],
        ["AI Service", "Google Gemini API", "LLM reasoning engine for contextual fitness coaching and function calling tools"],
        ["Testing", "pytest & Vitest", "Automated backend unit tests and frontend component verification"]
    ]
    create_table(tech_headers, tech_data, [Inches(1.5), Inches(2.0), Inches(3.0)])

    add_h("7. Risk Analysis and Mitigation", level=2, space_before=10, space_after=6)
    add_bullet("AI Hallucination Risk", "Mitigated by disallowing LLMs from computing BMR, TDEE, or macros; all math is hardcoded in deterministic Python utility functions.")
    add_bullet("API Rate Limiting", "Mitigated by caching frequent food database queries and utilizing exponential backoff on external Gemini API requests.")
    add_bullet("Data Security & Injection", "Mitigated by using Pydantic schema validation, parameterized MongoDB queries, Argon2 password hashing, and strict JWT signature checks.")

    add_h("8. Testing Methodology", level=2, space_before=10, space_after=6)
    add_p("AuraFIT was subjected to an exhaustive 8-stage testing methodology:")
    add_numbered("1.", "Unit Testing", "Tested isolated algorithms, including Mifflin-St Jeor calculation functions, height metric/imperial conversions, and password hashing helpers.")
    add_numbered("2.", "Integration Testing", "Verified communication between FastAPI routes and MongoDB Atlas via Motor, ensuring atomic document inserts and updates.")
    add_numbered("3.", "Functional Testing", "Tested complete user journeys: account registration, profile setup, meal logging, and workout plan generation.")
    add_numbered("4.", "Usability Testing", "Evaluated UI responsiveness, touch target sizes on mobile screens, and clarity of daily macro visual rings.")
    add_numbered("5.", "Security Testing", "Audited endpoints against unauthorized access, expired JWT tokens, CORS policy violations, and NoSQL injection attempts.")
    add_numbered("6.", "Regression Testing", "Executed automated pytest test suites on backend refactoring to ensure existing API contracts remained uncompromised.")
    add_numbered("7.", "Performance Testing", "Simulated concurrent user traffic to ensure FastAPI's async event loop maintained sub-200ms latency under load.")
    add_numbered("8.", "User Acceptance Testing (UAT)", "Engaged peer students and fitness enthusiasts to test daily logging and evaluate the quality of AI coach recommendations.")

    # ==========================================
    # SECTION 5: SYSTEM DEVELOPMENT CYCLE (SDLC)
    # ==========================================
    add_h("5. System Development Cycle (SDLC)", level=1, space_before=14, space_after=8)
    add_p("The development of AuraFIT adhered to the Agile System Development Life Cycle (SDLC), utilizing iterative 2-week sprints to progressively design, build, test, and refine system features.")

    add_h("4.1 Phases of SDLC in the AuraFIT Project", level=2, space_before=10, space_after=6)
    add_numbered("4.1.1", "Planning", "Defined system scope, clinical formulas, target demographic, and functional boundaries separating deterministic code from generative AI.")
    add_numbered("4.1.2", "Requirement Analysis", "Authored comprehensive Software Requirements Specifications (SRS), capturing user stories, data schemas, and API endpoint contracts.")
    add_numbered("4.1.3", "System Design", "Created database schemas, wireframes, architectural blueprints, and Gemini function-calling tool specifications.")
    add_numbered("4.1.4", "Development", "Implemented frontend React components and backend FastAPI micro-services, configuring MongoDB and integrating the Gemini API.")
    add_numbered("4.1.5", "Testing", "Executed unit, integration, security, and usability testing across all modules.")
    add_numbered("4.1.6", "Deployment", "Configured production environment variables, database indexes, and cloud hosting.")
    add_numbered("4.1.7", "Maintenance", "Monitored API latencies, optimized food search indexing, and tuned AI prompt templates.")

    add_h("Importance of SDLC in the AuraFIT Project", level=2, space_before=10, space_after=6)
    add_numbered("1.", "Meets Health Objectives", "Ensures clinical nutritional formulas strictly govern the user experience.")
    add_numbered("2.", "Minimizes Architectural Risks", "Prevents runtime AI hallucinations by enforcing rigid backend schemas.")
    add_numbered("3.", "Enhances Code Quality", "Structured iterations facilitated automated unit testing with pytest.")
    add_numbered("4.", "Ensures Scalability", "NoSQL document modeling allows adding new meal types or exercise metrics without schema migrations.")
    add_numbered("5.", "Improves Project Management", "Clear milestone definitions kept the development on schedule within academic deadlines.")
    add_numbered("6.", "Facilitates Faculty Collaboration", "Allowed iterative reviews and supervisor feedback to be incorporated into subsequent sprints.")
    add_numbered("7.", "Ensures Regulatory & Data Standards", "Protects sensitive user biometric and health data via modern encryption standards.")
    add_numbered("8.", "Promotes Cost Efficiency", "Early architecture decisions avoided expensive cloud refactoring.")
    add_numbered("9.", "Encourages Technological Innovation", "Enabled the safe, effective integration of cutting-edge LLM function calling.")

    add_h("Project Scheduling & Milestones", level=2, space_before=10, space_after=6)
    sched_headers = ["Phase", "Start Date", "End Date", "Duration"]
    sched_data = [
        ["Requirements Gathering & Analysis", "01/09/2026", "07/09/2026", "1 week"],
        ["System Architecture & DB Design", "08/09/2026", "21/09/2026", "2 weeks"],
        ["Frontend UI & State Development", "22/09/2026", "12/10/2026", "3 weeks"],
        ["Backend REST API & Deterministic Engine", "13/10/2026", "02/11/2026", "3 weeks"],
        ["AI Orchestrator & Gemini Tool Integration", "03/11/2026", "16/11/2026", "2 weeks"],
        ["System Integration & Multi-Stage Testing", "17/11/2026", "30/11/2026", "2 weeks"],
        ["UAT, Performance Tuning & Deployment", "01/12/2026", "15/12/2026", "2 weeks"]
    ]
    create_table(sched_headers, sched_data, [Inches(2.5), Inches(1.3), Inches(1.3), Inches(1.4)])

    add_h("Estimates of Efforts", level=2, space_before=10, space_after=6)
    effort_headers = ["Phase", "Estimated Duration", "Estimated Effort (Hours)", "Core Focus"]
    effort_data = [
        ["Phase 1: Requirements Analysis", "1 Week", "40 hours", "SRS documentation, formula verification"],
        ["Phase 2: System & DB Design", "2 Weeks", "120 hours", "Pydantic models, MongoDB collections, wireframes"],
        ["Phase 3: Frontend Development", "3 Weeks", "200 hours", "React, TypeScript, Tailwind, TanStack Query"],
        ["Phase 4: Backend API & Math Engine", "3 Weeks", "220 hours", "FastAPI routes, Mifflin-St Jeor, Argon2 auth"],
        ["Phase 5: AI Service Integration", "2 Weeks", "140 hours", "Gemini API client, function calling tools"],
        ["Phase 6: Integration & Testing", "2 Weeks", "120 hours", "pytest test suite, Vitest, security audit"],
        ["Phase 7: Deployment & Documentation", "2 Weeks", "80 hours", "Cloud configuration, index optimization, thesis"]
    ]
    create_table(effort_headers, effort_data, [Inches(2.2), Inches(1.3), Inches(1.5), Inches(1.5)])

    # ==========================================
    # SECTION 6: CONTEXT LEVEL DFD
    # ==========================================
    add_h("6. Context level DFD", level=1, space_before=14, space_after=8)
    add_p("Data Flow Diagrams (DFDs) illustrate the path and transformation of data across AuraFIT. Below is the structural analysis and layout of DFD Level 0, Level 1, and Level 2.")

    add_h("6.1 Level 0: Context-Level DFD", level=2, space_before=8, space_after=4)
    add_p("At Level 0, the entire AuraFIT platform is represented as a single centralized process interacting with external entities (User, MongoDB Atlas Database, and Google Gemini AI Service):")

    add_code(
"""
           +-------------------------------------------------------+
           |                      USER                             |
           |  (Inputs: Biometrics, Food Logs, Workout Logs, Chat)  |
           |  (Outputs: Macro Targets, Daily Ratios, AI Guidance)  |
           +---------------------------+---------------------------+
                                       |
                User Actions & Auth    |   HTTP Responses & Data
                                       v
                     +===================================+
                     |             [0.0]                 |
                     |            AuraFIT                |
                     |    Core Application Platform      |
                     +===================================+
                           /                       \\
     Async DB Queries &   /                         \\  Prompt Context & Tools
     Document Mutates    /                           \\ Structured JSON
                        v                             v
           +-------------------------+   +-------------------------+
           |      MONGODB ATLAS      |   |    GOOGLE GEMINI API    |
           |   (Persistent Cloud     |   |   (Contextual Reasoning |
           |    Document Store)      |   |    & Tool Execution)    |
           +-------------------------+   +-------------------------+
"""
    )

    add_h("6.2 Level 1: Subsystem Decomposition DFD", level=2, space_before=10, space_after=4)
    add_p("Level 1 decomposes the AuraFIT system into its 6 primary operational processes:")
    add_code(
"""
 [User] ---> (1.0 Authentication & JWT Manager) ------> [Users Collection]
   |
   +-------> (2.0 Biometric Profile & BMR/TDEE Engine) -> [Profiles Collection]
   |
   +-------> (3.0 Food Database & Meal Logging) -------> [Foods & Saved Meals]
   |                     ^
   |                     | (Tool Calls for Food Swaps)
   +-------> (4.0 AI Fitness Coach Orchestrator) <-----> [Google Gemini API]
   |
   +-------> (5.0 Workout Planner & Exercise Log) -----> [Exercises & Workouts]
   |
   +-------> (6.0 Progress Analytics & Reporting) -----> [Measurements Log]
"""
    )

    add_h("6.3 Level 2: Detailed Process Flow (Nutrition & AI Meal Swapping)", level=2, space_before=10, space_after=4)
    add_p("Level 2 models the detailed execution pipeline when a user requests an AI-powered meal swap:")
    add_code(
"""
 1. User selects meal item to swap -> Submits swap request to FastAPI
 2. Process validates current user JWT & extracts current food macros
 3. Server packages food constraints + user dietary tags into Gemini Tool Context
 4. Gemini executes 'find_alternative_food(food_id)' tool
 5. Server queries Foods Collection for matching caloric and macro boundaries
 6. Result returned to Gemini -> Gemini outputs structured replacement JSON
 7. Server verifies mathematical parity -> Updates UI and database log
"""
    )

    # ==========================================
    # SECTION 7: DATA DICTIONARY
    # ==========================================
    add_h("7. Data Dictionary", level=1, space_before=14, space_after=8)
    add_p("The Data Dictionary documents the schema definitions, field data types, validation constraints, and operational descriptions of all collections stored within MongoDB Atlas.")

    add_h("1. Users Collection", level=2, space_before=10, space_after=4)
    add_p("Stores core account credentials, authentication parameters, and role designations.")
    u_headers = ["Field Name", "Data Type", "Constraints", "Description"]
    u_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique system identifier for each user account."],
        ["email", "String", "Unique, Not Null, Valid Email", "User's email address used for login and notifications."],
        ["hashed_password", "String", "Not Null, Argon2 Hash", "Securely hashed password using the Argon2id algorithm."],
        ["role", "String", "Default: 'user' ('user', 'admin')", "Access control level defining authorization scope."],
        ["is_active", "Boolean", "Default: True", "Flag indicating whether account is active or suspended."],
        ["created_at", "DateTime", "Default: Current UTC Timestamp", "Timestamp of account registration."],
        ["updated_at", "DateTime", "Default: Current UTC Timestamp", "Timestamp of last account modification."]
    ]
    create_table(u_headers, u_data, [Inches(1.5), Inches(1.2), Inches(1.8), Inches(2.0)])

    add_h("2. Profiles Collection", level=2, space_before=10, space_after=4)
    add_p("Maintains biometric parameters, fitness goals, and deterministic metabolic targets.")
    p_headers = ["Field Name", "Data Type", "Constraints", "Description"]
    p_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for the profile document."],
        ["user_id", "String / ObjectId", "Foreign Key (Users), Unique", "References the owner user account."],
        ["age", "Integer", "Not Null, Min 13, Max 100", "Age of the user in years."],
        ["gender", "String", "Enum: 'male', 'female'", "Biological sex used for Mifflin-St Jeor calculations."],
        ["height_cm", "Decimal", "Not Null, Min 100, Max 250", "Height of the user in centimeters."],
        ["weight_kg", "Decimal", "Not Null, Min 30, Max 300", "Current body weight of the user in kilograms."],
        ["activity_level", "String", "Enum: sedentary, light, moderate, heavy", "Physical activity multiplier used for TDEE."],
        ["goal", "String", "Enum: fat_loss, maintain, muscle_gain", "Primary fitness goal affecting caloric adjustment."],
        ["dietary_preference", "String", "Enum: veg, vegan, non_veg, eggetarian", "Dietary boundary for food recommendations."],
        ["allergies", "Array[String]", "Optional", "List of allergens (e.g., peanuts, gluten, dairy)."],
        ["bmr", "Decimal", "Deterministic Calculated", "Basal Metabolic Rate computed via Mifflin-St Jeor."],
        ["tdee", "Decimal", "Deterministic Calculated", "Total Daily Energy Expenditure (BMR * Activity)."],
        ["target_calories", "Decimal", "Deterministic Calculated", "Final daily calorie target based on goal."],
        ["target_protein_g", "Decimal", "Deterministic Calculated", "Target daily protein intake in grams."],
        ["target_carbs_g", "Decimal", "Deterministic Calculated", "Target daily carbohydrates intake in grams."],
        ["target_fat_g", "Decimal", "Deterministic Calculated", "Target daily healthy fats intake in grams."]
    ]
    create_table(p_headers, p_data, [Inches(1.5), Inches(1.2), Inches(1.8), Inches(2.0)])

    add_h("3. Foods Collection", level=2, space_before=10, space_after=4)
    add_p("The authoritative master catalog of verified food items with rich macronutrient breakdowns.")
    f_headers = ["Field Name", "Data Type", "Constraints", "Description"]
    f_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for the food item."],
        ["name", "String", "Not Null, Indexed", "Common name of food (e.g., 'Paneer Bhurji', 'Moong Dal')."],
        ["category", "String", "Enum: Grains, Dairy, Legumes, Meats", "Nutritional grouping of the item."],
        ["serving_size_g", "Decimal", "Not Null, Default: 100g", "Standard portion size for macro reporting."],
        ["calories", "Decimal", "Not Null, >= 0", "Energy content per serving."],
        ["protein_g", "Decimal", "Not Null, >= 0", "Protein content in grams."],
        ["carbs_g", "Decimal", "Not Null, >= 0", "Carbohydrate content in grams."],
        ["fat_g", "Decimal", "Not Null, >= 0", "Total fat content in grams."],
        ["fiber_g", "Decimal", "Optional, >= 0", "Dietary fiber content in grams."],
        ["diet_tags", "Array[String]", "Values: 'vegetarian', 'vegan', etc.", "Dietary classification tags for filtering."],
        ["is_indian_cuisine", "Boolean", "Default: True", "Flag identifying regional South Asian food items."]
    ]
    create_table(f_headers, f_data, [Inches(1.5), Inches(1.2), Inches(1.8), Inches(2.0)])

    add_h("4. Exercises Collection", level=2, space_before=10, space_after=4)
    add_p("Catalog of verified resistance, calisthenics, and cardiovascular exercises.")
    e_headers = ["Field Name", "Data Type", "Constraints", "Description"]
    e_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for the exercise."],
        ["name", "String", "Not Null, Unique, Indexed", "Name of exercise (e.g., 'Barbell Back Squat')."],
        ["muscle_group", "String", "Enum: Chest, Back, Legs, Shoulders, Core", "Primary anatomical target."],
        ["secondary_muscles", "Array[String]", "Optional", "Auxiliary stabilizing muscle groups."],
        ["equipment", "String", "Enum: Barbell, Dumbbell, Machine, None", "Required gym or home equipment."],
        ["difficulty", "String", "Enum: Beginner, Intermediate, Advanced", "Technical complexity of execution."],
        ["instructions", "Text", "Not Null", "Step-by-step biomechanical execution instructions."]
    ]
    create_table(e_headers, e_data, [Inches(1.5), Inches(1.2), Inches(1.8), Inches(2.0)])

    add_h("5. Saved Meals & Daily Nutrition Logs Collection", level=2, space_before=10, space_after=4)
    add_p("Records user-created recipes, assembled meals, and timestamped daily consumption.")
    m_headers = ["Field Name", "Data Type", "Constraints", "Description"]
    m_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for the logged meal."],
        ["user_id", "String / ObjectId", "Foreign Key (Users), Indexed", "User who logged the meal."],
        ["meal_name", "String", "Not Null, Max 100 chars", "Custom label (e.g., 'Post-Workout Oats & Whey')."],
        ["meal_type", "String", "Enum: breakfast, lunch, dinner, snack", "Designation of meal timing."],
        ["calories", "Decimal", "Not Null, >= 0", "Total energy in kilocalories."],
        ["protein_grams", "Decimal", "Not Null, >= 0", "Total protein provided by meal."],
        ["carbohydrates_grams", "Decimal", "Not Null, >= 0", "Total carbohydrates in meal."],
        ["fat_grams", "Decimal", "Not Null, >= 0", "Total fats in meal."],
        ["ingredients", "Array[Object]", "Not Null", "List of embedded ingredient objects with portions."],
        ["created_at", "DateTime", "Default: Current UTC Timestamp", "Timestamp when consumption was logged."]
    ]
    create_table(m_headers, m_data, [Inches(1.5), Inches(1.2), Inches(1.8), Inches(2.0)])

    add_h("6. Workouts & Exercise Logs Collection", level=2, space_before=10, space_after=4)
    add_p("Tracks completed physical training sessions, volume, sets, and rep logs.")
    w_headers = ["Field Name", "Data Type", "Constraints", "Description"]
    w_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for the workout session."],
        ["user_id", "String / ObjectId", "Foreign Key (Users), Indexed", "User who performed the session."],
        ["workout_name", "String", "Not Null", "Name of routine (e.g., 'Push Day Hypertrophy')."],
        ["date", "DateTime", "Not Null, Indexed", "Date on which session was executed."],
        ["exercises_performed", "Array[Object]", "Not Null", "Nested objects detailing sets, reps, and weights lifted."],
        ["duration_minutes", "Integer", "Optional, > 0", "Total elapsed workout time in minutes."],
        ["notes", "Text", "Optional", "Personal notes on fatigue, RPE, or soreness."]
    ]
    create_table(w_headers, w_data, [Inches(1.5), Inches(1.2), Inches(1.8), Inches(2.0)])

    add_h("7. Measurements & Progress Logs Collection", level=2, space_before=10, space_after=4)
    add_p("Logs historical biometric progress for graphical trend analysis.")
    me_headers = ["Field Name", "Data Type", "Constraints", "Description"]
    me_data = [
        ["_id", "ObjectId", "Primary Key, Auto-generated", "Unique identifier for measurement entry."],
        ["user_id", "String / ObjectId", "Foreign Key (Users), Indexed", "References user account."],
        ["date", "DateTime", "Not Null, Indexed", "Date of measurement."],
        ["weight_kg", "Decimal", "Not Null, > 0", "Recorded morning body weight in kg."],
        ["waist_cm", "Decimal", "Optional", "Waist circumference in cm."],
        ["body_fat_percentage", "Decimal", "Optional, Between 3% and 60%", "Estimated or caliper body fat percentage."],
        ["notes", "String", "Optional", "Context notes (e.g., 'Weigh-in after refeed day')."]
    ]
    create_table(me_headers, me_data, [Inches(1.5), Inches(1.2), Inches(1.8), Inches(2.0)])

    # ==========================================
    # SECTION 8: SOURCE CODE
    # ==========================================
    add_h("8. Source Code", level=1, space_before=14, space_after=8)
    add_p("The following listings showcase core architectural modules from the AuraFIT codebase, illustrating FastAPI backend initialization, Argon2 cryptographic security, deterministic nutrition routing, and Google Gemini AI tool orchestration.")

    add_h("8.1 backend/app/main.py: FastAPI Entrypoint & Router Mounting", level=2, space_before=10, space_after=4)
    add_code(
"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.api.routes import (
    auth, profile, nutrition, foods, exercises, 
    ai, workouts, goals, measurements, analytics, plans
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB Atlas
    await connect_to_mongo()
    yield
    # Shutdown: Cleanly close connection pool
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Authoritative Backend API for AuraFIT",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration for React SPA
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Modular Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["profile"])
app.include_router(nutrition.router, prefix="/api/v1/nutrition", tags=["nutrition"])
app.include_router(foods.router, prefix="/api/v1/foods", tags=["foods"])
app.include_router(exercises.router, prefix="/api/v1/exercises", tags=["exercises"])
app.include_router(workouts.router, prefix="/api/v1/workouts", tags=["workouts"])
app.include_router(goals.router, prefix="/api/v1/goals", tags=["goals"])
app.include_router(measurements.router, prefix="/api/v1/measurements", tags=["measurements"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(plans.router, prefix="/api/v1/plans", tags=["plans"])

@app.get("/ping")
async def ping():
    return {"status": "ok", "app": "AuraFIT Core Engine"}
"""
    )

    add_h("8.2 backend/app/core/security.py: Argon2 Hashing & JWT Security", level=2, space_before=10, space_after=4)
    add_code(
"""from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from app.core.config import settings

# Argon2 Cryptographic Context for state-of-the-art password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, token_type: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != token_type:
            return None
        return payload
    except jwt.PyJWTError:
        return None
"""
    )

    add_h("8.3 backend/app/api/routes/nutrition.py: Saved Meals & Macro Calculations", level=2, space_before=10, space_after=4)
    add_code(
"""from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime, timezone
from bson import ObjectId
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from app.models.domain import SavedMealCreate, SavedMealResponse

router = APIRouter()

def serialize_saved_meal(meal: dict) -> dict:
    return {
        "id": str(meal["_id"]),
        "user_id": str(meal["user_id"]),
        "meal_name": meal["meal_name"],
        "meal_type": meal["meal_type"],
        "serving_size": meal["serving_size"],
        "calories": meal["calories"],
        "protein_grams": meal["protein_grams"],
        "carbohydrates_grams": meal["carbohydrates_grams"],
        "fat_grams": meal["fat_grams"],
        "fiber_grams": meal.get("fiber_grams", 0.0),
        "ingredients": meal.get("ingredients", []),
        "notes": meal.get("notes"),
        "created_at": meal["created_at"],
        "updated_at": meal["updated_at"]
    }

@router.post("/saved-meals", response_model=SavedMealResponse, status_code=status.HTTP_201_CREATED)
async def create_saved_meal(meal: SavedMealCreate, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    meal_dict = meal.model_dump()
    meal_dict["user_id"] = str(current_user["_id"])
    now = datetime.now(timezone.utc)
    meal_dict["created_at"] = now
    meal_dict["updated_at"] = now
    result = await db.saved_meals.insert_one(meal_dict)
    meal_dict["_id"] = result.inserted_id
    return serialize_saved_meal(meal_dict)

@router.get("/saved-meals", response_model=List[SavedMealResponse])
async def get_saved_meals(current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    cursor = db.saved_meals.find({"user_id": str(current_user["_id"])}).sort("created_at", -1)
    meals = await cursor.to_list(length=100)
    return [serialize_saved_meal(m) for m in meals]
"""
    )

    add_h("8.4 backend/app/services/ai_service.py: Google Gemini Tool Declarations", level=2, space_before=10, space_after=4)
    add_code(
"""import json
from google import genai
from google.genai import types
from app.core.config import settings

# Explicit Gemini Function Declarations for Tool Calling
gemini_tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_foods",
                description="Search database for foods, calories, macros based on dietary preferences.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "search": types.Schema(type=types.Type.STRING, description="Food name query"),
                        "category": types.Schema(type=types.Type.STRING, description="Food category"),
                        "diet": types.Schema(type=types.Type.STRING, description="Dietary preference")
                    }
                )
            ),
            types.FunctionDeclaration(
                name="find_alternative_food",
                description="Find an alternative food for a food ID respecting calorie and macro constraints.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "food_id": types.Schema(type=types.Type.STRING, description="ID of food to replace")
                    },
                    required=["food_id"]
                )
            ),
            types.FunctionDeclaration(
                name="search_exercises",
                description="Search exercises by muscle group, difficulty, and required equipment.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "search": types.Schema(type=types.Type.STRING, description="Exercise name"),
                        "muscle": types.Schema(type=types.Type.STRING, description="Target muscle group"),
                        "equipment": types.Schema(type=types.Type.STRING, description="Equipment needed")
                    }
                )
            )
        ]
    )
]
"""
    )

    # ==========================================
    # SECTION 9: OUTPUT / VISUAL INTERFACES
    # ==========================================
    add_h("9. Output / Visual Interfaces", level=1, space_before=14, space_after=8)
    add_p("The following figures illustrate key responsive user interfaces developed for AuraFIT, demonstrating the user onboarding workflow, daily macro tracking dashboard, AI coach conversational interface, workout manager, and longitudinal analytics.")

    def add_figure_placeholder(fig_num, title, description):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F0F4F8")
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="B0C4DE"/>'
            f'<w:left w:val="single" w:sz="6" w:space="0" w:color="B0C4DE"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="B0C4DE"/>'
            f'<w:right w:val="single" w:sz="6" w:space="0" w:color="B0C4DE"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        run_box = p.add_run(f"[ Screenshot Interface: {title} ]\n(Insert Application UI Screenshot Here)")
        run_box.font.name = 'Times New Roman'
        run_box.font.size = Pt(11)
        run_box.italic = True
        run_box.bold = True
        run_box.font.color.rgb = RGBColor(70, 90, 120)

        p_cap = add_p(f"Figure {fig_num}: {description}", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
        p_cap.paragraph_format.space_before = Pt(4)

    add_figure_placeholder(
        "7.1", 
        "AuraFIT Landing Page & User Onboarding Flow",
        "Illustrates the responsive landing portal and dynamic biometric onboarding questionnaire where height, weight, activity multiplier, and fitness goals are captured for deterministic BMR computation."
    )

    add_figure_placeholder(
        "7.2", 
        "Daily Overview Dashboard & Macro Allocation",
        "Displays the central dashboard featuring interactive radial progress rings for daily caloric consumption vs. deterministic target, alongside real-time protein, carbohydrate, and fat breakdown."
    )

    add_figure_placeholder(
        "7.3", 
        "AI Nutrition Coach & Contextual Meal Swapper",
        "Demonstrates the server-orchestrated Google Gemini AI chat interface, highlighting intelligent ingredient substitutions (e.g., swapping Paneer for Tofu with matched macros) using function calling."
    )

    add_figure_placeholder(
        "7.4", 
        "Exercise Library & Workout Session Logger",
        "Shows the interactive workout planning module, categorizing exercises by primary muscle groups with modal biomechanical instructions and set/rep/weight logging."
    )

    add_figure_placeholder(
        "7.5", 
        "Longitudinal Progress Tracking & Weight Analytics",
        "Depicts the analytics module powered by Recharts, showing trend lines for body weight, waist circumference, and caloric compliance over 30-day and 90-day timeframes."
    )

    # ==========================================
    # SECTION 10: LIMITATIONS AND FUTURE ENHANCEMENTS
    # ==========================================
    add_h("10. Limitations And Future Enhancements", level=1, space_before=14, space_after=8)

    add_h("Limitations", level=2, space_before=10, space_after=6)
    add_numbered("1.", "External AI API Dependency", "The intelligent assistant relies on network communication with Google Gemini API; temporary upstream latency or quota exhaustion can affect conversational response times.")
    add_numbered("2.", "Manual Portion Logging", "Nutritional accuracy depends on the fidelity of user-entered portion sizes (e.g., estimating 150g vs 200g cooked dal), as automated volumetric computer vision is not yet integrated.")
    add_numbered("3.", "Continuous Connectivity Requirement", "AuraFIT currently operates as an online web application; full offline-first synchronization using Service Workers and IndexedDB is not yet active.")
    add_numbered("4.", "Absence of Direct Hardware Sensor Sync", "Biometric data (heart rate, active calories burned) must currently be entered manually rather than syncing automatically with wearable hardware.")
    add_numbered("5.", "Regional Cooking Variance", "While Indian foods are thoroughly represented, homemade recipes exhibit oil and sodium variances that can lead to minor micronutrient deviations.")
    add_numbered("6.", "Cold-Start Latency on Serverless Tiers", "On free-tier cloud hosting platforms, inactive backend containers can experience a 10-15 second cold start upon initial invocation.")
    add_numbered("7.", "Lack of Real-Time Video Exercise Pose Detection", "Users must self-assess their exercise form using instructional guides rather than receiving automated webcam biomechanical feedback.")
    add_numbered("8.", "Nutritional Micro-Nutrient Granularity", "The current database optimizes for macronutrients (calories, protein, carbs, fat, fiber); granular tracking of micronutrients (vitamins, minerals) is planned for future releases.")

    add_h("Future Enhancements", level=2, space_before=10, space_after=6)
    add_numbered("1.", "Computer Vision Pose Estimation", "Integrate MediaPipe or OpenCV via WebAssembly to track joint angles through the user's webcam and offer real-time exercise rep counting and posture correction.")
    add_numbered("2.", "Automated Food Image Recognition", "Incorporate Gemini Multimodal Vision to allow users to snap a photo of their meal, automatically estimating food categories and serving sizes.")
    add_numbered("3.", "Wearable Device Integration", "Build bidirectional synchronization with Apple HealthKit, Google Health Connect, Fitbit, and Garmin to automatically pull daily step counts and resting heart rates.")
    add_numbered("4.", "Voice-Activated Logging", "Deploy Web Speech API and Natural Language Understanding to allow hands-free meal and workout logging during gym sessions.")
    add_numbered("5.", "Offline Progressive Web App (PWA)", "Transform AuraFIT into an installable PWA with local SQLite/IndexedDB caching, enabling complete offline logging with background sync.")
    add_numbered("6.", "Community & Peer Accountability", "Introduce community leaderboards, challenge groups, and coach sharing features to boost user consistency and engagement.")
    add_numbered("7.", "Barcode Scanning Integration", "Implement camera-based barcode scanning for packaged food items to instantly populate nutritional facts.")
    add_numbered("8.", "Micronutrient & Blood Biomarker Correlation", "Enable users to upload annual blood test reports (e.g., Vitamin D, B12, lipid panels) and receive AI-customized dietary optimization.")
    add_numbered("9.", "Multilingual Regional Localization", "Expand user interface and food database nomenclature into regional Indian languages including Hindi, Tamil, Telugu, and Bengali.")
    add_numbered("10.", "Predictive Weight Trend Modeling", "Apply predictive machine learning models to forecast goal arrival dates based on 30-day historical compliance and caloric deficits.")

    # Save to workspace root
    output_path = os.path.abspath("AuraFIT_Major_Project_Report.docx")
    doc.save(output_path)
    print(f"Report generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_aurafit_report()
