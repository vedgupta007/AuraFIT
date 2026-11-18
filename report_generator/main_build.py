# -*- coding: utf-8 -*-
import os
import sys
import math
import docx

sys.path.insert(0, os.path.abspath("."))

from report_generator.helpers import init_doc
from report_generator.part1_front_matter import build_front_matter
from report_generator.part2_chapters_1_to_3 import build_chapters_1_to_3
from report_generator.part3_chapters_4_to_6 import build_chapters_4_to_6
from report_generator.part4_chapters_7_to_9 import build_chapters_7_to_9
from report_generator.part5_chapters_10_to_13 import build_chapters_10_to_13

def build_full_doc(page_map=None):
    doc = init_doc()
    build_front_matter(doc, page_map=page_map)
    build_chapters_1_to_3(doc)
    build_chapters_4_to_6(doc)
    build_chapters_7_to_9(doc)
    build_chapters_10_to_13(doc)
    return doc

def simulate_page_numbers(doc):
    body = doc.element.body
    MAX_HEIGHT = 648.0  # (11 - 2) * 72 pt usable height
    current_page = 1
    current_height = 0.0

    page_map = {
        "Cover Page": 1,
        "Candidate Declaration": 2,
        "Major Project Completion Certificate": 3,
        "Acknowledgement": 4,
        "Table of Contents": 5,
    }

    for child in body:
        tag = child.tag.split('}')[-1]

        if tag == 'p':
            has_page_break = False
            for r in child.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}br'):
                if r.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type') == 'page':
                    has_page_break = True
                    break

            p_obj = docx.text.paragraph.Paragraph(child, doc)
            text = p_obj.text.strip()
            char_count = len(text)
            lines = 1 if char_count == 0 else max(1, math.ceil(char_count / 72.0))

            is_h1 = False
            is_h2 = False
            for run in p_obj.runs:
                if run.font.size and run.font.size.pt >= 15:
                    is_h1 = True
                elif run.font.size and run.font.size.pt >= 13.5:
                    is_h2 = True

            if is_h1:
                p_height = lines * 22.0 + 14.0 + 6.0
            elif is_h2:
                p_height = lines * 19.0 + 12.0 + 4.0
            else:
                p_height = lines * 18.0 + 6.0

            if current_height + p_height > MAX_HEIGHT and current_height > 0:
                current_page += 1
                current_height = 0.0

            # Match headings and figures
            if text.startswith("Chapter 1:"):
                page_map["Chapter 1"] = current_page
            elif text.startswith("Chapter 2:"):
                page_map["Chapter 2"] = current_page
            elif text.startswith("Chapter 3:"):
                page_map["Chapter 3"] = current_page
            elif text.startswith("Chapter 4:"):
                page_map["Chapter 4"] = current_page
            elif text.startswith("Chapter 5:"):
                page_map["Chapter 5"] = current_page
            elif text.startswith("Chapter 6:"):
                page_map["Chapter 6"] = current_page
            elif text.startswith("Chapter 7:"):
                page_map["Chapter 7"] = current_page
            elif text.startswith("Chapter 8:"):
                page_map["Chapter 8"] = current_page
            elif text.startswith("Chapter 9:"):
                page_map["Chapter 9"] = current_page
            elif text.startswith("Chapter 10:"):
                page_map["Chapter 10"] = current_page
            elif text.startswith("Chapter 11:"):
                page_map["Chapter 11"] = current_page
            elif text.startswith("Chapter 12:"):
                page_map["Chapter 12"] = current_page
            elif text.startswith("Chapter 13:"):
                page_map["Chapter 13"] = current_page
            elif text == "LIST OF TABLES":
                page_map["List of Tables"] = current_page
            elif text == "LIST OF FIGURES":
                page_map["List of Figures"] = current_page
            elif text == "References & Bibliography":
                page_map["References"] = current_page
            elif text.startswith("Figure "):
                fig_key = text.split(":")[0].strip()
                page_map[fig_key] = current_page
            else:
                # Subsections: e.g., 1.1, 1.2, 2.1, etc.
                parts = text.split(" ")
                if len(parts) >= 2 and len(parts[0]) >= 3 and parts[0][0].isdigit() and "." in parts[0]:
                    sec_key = parts[0]
                    page_map[sec_key] = current_page

            current_height += p_height

            if has_page_break:
                current_page += 1
                current_height = 0.0

        elif tag == 'tbl':
            tbl_obj = docx.table.Table(child, doc)
            num_rows = len(tbl_obj.rows)
            tbl_height = 28.0 + (num_rows - 1) * 24.0

            if tbl_height < MAX_HEIGHT and (current_height + tbl_height > MAX_HEIGHT):
                current_page += 1
                current_height = 0.0

            # Match Table titles if preceding paragraph had Table caption
            while tbl_height > 0:
                available = MAX_HEIGHT - current_height
                if tbl_height <= available:
                    current_height += tbl_height
                    tbl_height = 0
                else:
                    tbl_height -= available
                    current_page += 1
                    current_height = 0.0

    return page_map, current_page

def main():
    print("Executing Pass 1 (Simulating exact layout & page breaks)...")
    doc_draft = build_full_doc(page_map=None)
    page_map, total_pages = simulate_page_numbers(doc_draft)

    print(f"Simulation completed. Total Pages: {total_pages}")
    print("Sample mapped chapter pages:")
    for ch in ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5", "Chapter 6", "Chapter 7", "Chapter 8", "Chapter 9", "Chapter 10", "Chapter 11", "Chapter 12", "Chapter 13"]:
        print(f"  {ch}: Page {page_map.get(ch)}")

    print("\nExecuting Pass 2 (Generating document with exact page numbers)...")
    final_doc = build_full_doc(page_map=page_map)
    output_path = os.path.abspath("AuraFIT_Major_Project_Report.docx")
    final_doc.save(output_path)
    print(f"Report successfully generated and saved to: {output_path}")

if __name__ == '__main__':
    main()
