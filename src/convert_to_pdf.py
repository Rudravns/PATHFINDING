import os
import re
import tempfile
import img2pdf

from docx2pdf import convert as word_to_pdf
from aspose.cells import Workbook, SaveFormat

from fpdf import FPDF

from PyPDF2 import PdfMerger

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# =========================================================
# CONFIG
# =========================================================

CENSORED_NAME = "Rudransh Kumar"


# =========================================================
# UTILITIES
# =========================================================

def normalize_text(text):
    """
    Lowercases and removes whitespace for comparisons.
    """
    return re.sub(r"\s+", "", text.lower())


def censor_text(text):
    """
    Replaces occurrences of the censored name,
    ignoring case and whitespace differences.
    """

    target = normalize_text(CENSORED_NAME)

    result = []
    buffer = ""

    for char in text:

        if not char.isspace():
            buffer += char

        else:
            buffer += char

        normalized_buffer = normalize_text(buffer)

        if target in normalized_buffer:
            return "[CENSORED]"

    return text


# =========================================================
# TITLE PAGE
# =========================================================

def create_title_page(title, output_path):
    """
    Creates a section divider page.
    """

    c = canvas.Canvas(output_path, pagesize=letter)

    width, height = letter

    if not title.endswith("/"):
        title += "/"

    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height / 2, title)

    c.save()


# =========================================================
# TEXT PDF CREATION
# =========================================================

def create_text_pdf(input_file, output_pdf, display_name):
    """
    Converts a text/code file into a styled PDF.
    """

    pdf = FPDF()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    # -------------------------
    # File title
    # -------------------------
    pdf.set_font("Helvetica", style="B", size=16)

    pdf.cell(
        0,
        10,
        display_name,
        ln=True,
        align="C"
    )
    pdf.ln(4)

    # Divider line
    page_width = pdf.w - 20
    y = pdf.get_y()

    pdf.line(10, y, page_width, y)

    pdf.ln(8)

    # -------------------------
    # Code/text body
    # -------------------------
    pdf.set_font("Courier", size=10)

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:

        for line in f:

            # Censor name
            if normalize_text(CENSORED_NAME) in normalize_text(line):
                line = "[CENSORED]\n"

            pdf.multi_cell(0, 5, txt=line)

    pdf.output(output_pdf)


# =========================================================
# MAIN CONVERSION
# =========================================================

def convert_and_merge_project(project_root, final_output_pdf):
    """
    Converts the entire project into ONE merged PDF.

    Structure:
    - Folder title pages
    - File content directly after
    """

    merger = PdfMerger()

    temp_dir = tempfile.mkdtemp()

    for root, _, files in os.walk(project_root):

        # Skip generated files/folders
        if "venv" in root.lower():
            continue

        if "__pycache__" in root.lower():
            continue

        relative_folder = os.path.relpath(root, project_root)

        if relative_folder == ".":
            relative_folder = "root"

        supported_files = []

        for filename in sorted(files):

            lower = filename.lower()

            if lower.endswith(".pdf"):
                continue

            if lower == os.path.basename(final_output_pdf).lower():
                continue

            if lower.endswith((
                ".txt",
                ".py",
                ".md",
                ".gitignore",
                ".license",
                ".toml",
                ".docx",
                ".xlsx",
                ".xls",
                ".jpg",
                ".jpeg",
                ".png"
            )):
                supported_files.append(filename)

        if not supported_files:
            continue

        # =================================================
        # Folder divider page
        # =================================================

        folder_title_pdf = os.path.join(
            temp_dir,
            f"{relative_folder.replace(os.sep, '_')}_folder.pdf"
        )

        create_title_page(relative_folder, folder_title_pdf)

        merger.append(folder_title_pdf)

        print(f"\n=== {relative_folder}/ ===")

        # =================================================
        # Files
        # =================================================

        for filename in supported_files:

            file_path = os.path.join(root, filename)

            name_without_ext = os.path.splitext(filename)[0]
            display_name = filename
            temp_pdf = os.path.join(
                temp_dir,
                f"{name_without_ext}.pdf"
            )

            try:

                # -----------------------------------------
                # TEXT-LIKE FILES
                # -----------------------------------------
                if filename.lower().endswith((
                    ".txt",
                    ".py",
                    ".md",
                    ".gitignore",
                    ".license",
                    ".toml"
                )):

                    create_text_pdf(
                        file_path,
                        temp_pdf,
                        display_name
                    )

                # -----------------------------------------
                # WORD
                # -----------------------------------------
                elif filename.lower().endswith(".docx"):

                    word_to_pdf(file_path, temp_pdf)

                # -----------------------------------------
                # EXCEL
                # -----------------------------------------
                elif filename.lower().endswith((".xlsx", ".xls")):

                    workbook = Workbook(file_path)
                    workbook.save(temp_pdf, SaveFormat.PDF)

                # -----------------------------------------
                # IMAGES
                # -----------------------------------------
                elif filename.lower().endswith((
                    ".jpg",
                    ".jpeg",
                    ".png"
                )):

                    with open(temp_pdf, "wb") as f:
                        f.write(img2pdf.convert(file_path))

                else:
                    continue

                merger.append(temp_pdf)

                print(f"Added: {file_path}")

            except Exception as e:
                print(f"Failed: {file_path} -> {e}")

    # =====================================================
    # FINAL OUTPUT
    # =====================================================

    merger.write(final_output_pdf)

    merger.close()

    print("\n===================================")
    print("Combined PDF created:")
    print(final_output_pdf)
    print("===================================")


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    # Current file location
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Project root
    project_root = os.path.abspath(
        os.path.join(base_dir, "..")
    )

    # Final singular PDF
    final_output = os.path.join(
        project_root,
        "COMPLETE_PROJECT.pdf"
    )

    convert_and_merge_project(
        project_root,
        final_output
    )

