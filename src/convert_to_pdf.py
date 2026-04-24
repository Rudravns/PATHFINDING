import os
import img2pdf
from docx2pdf import convert as word_to_pdf
from aspose.cells import Workbook, SaveFormat
from fpdf import FPDF


def convert_to_pdf(input_folder, output_folder):
    """
    Recursively converts supported files in input_folder to PDF and saves them in output_folder,
    preserving the directory structure. Supported formats include:
    - Word documents (.docx)
    - Excel spreadsheets (.xlsx, .xls)
    - Images (.jpg, .png, .jpeg)
    - Text files (.txt, .py, .md, .gitignore, .license, .toml)
        Unsupported files are skipped. Existing PDFs are not reprocessed.
        Errors during conversion are logged to the console.

    This function was created with the help of ChatGPT. It helped find the libraries and code snipets for library commands
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Skip PDFs
            if filename.lower().endswith(".pdf"):
                continue

            # Preserve folder structure
            relative_path = os.path.relpath(root, input_folder)
            output_dir = os.path.join(output_folder, relative_path)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_path = os.path.join(
                output_dir,
                f"{os.path.splitext(filename)[0]}.pdf"
            )

            try:
                # Word
                if filename.lower().endswith(".docx"):
                    word_to_pdf(file_path, output_path)

                # Excel
                elif filename.lower().endswith((".xlsx", ".xls")):
                    workbook = Workbook(file_path)
                    workbook.save(output_path, SaveFormat.PDF)

                # Images
                elif filename.lower().endswith((".jpg", ".png", ".jpeg")):
                    with open(output_path, "wb") as f:
                        f.write(img2pdf.convert(file_path))

                # Text-like files
                elif filename.lower().endswith((
                    ".txt", ".py", ".md", ".gitignore", ".license", ".toml"
                )):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Courier", size=10)

                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            pdf.multi_cell(0, 5, txt=line)

                    pdf.output(output_path)

                else:
                    continue  # skip unsupported files

                print(f" Converted: {file_path}")

            except Exception as e:
                print(f"Failed: {file_path} -> {e}")


# --- RUN SCRIPT SAFELY ---
if __name__ == "__main__":
    # Get location of THIS script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Go to project root (one level up from src/)
    project_root = os.path.abspath(os.path.join(base_dir, ".."))

    # Output folder at project root
    output_folder = os.path.join(project_root, "pdf")

    convert_to_pdf(project_root, output_folder)