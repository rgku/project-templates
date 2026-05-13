from pathlib import Path
from datetime import datetime
from fpdf import FPDF
from config import config

class PromptPackPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 8, "DeepSeek Prompt Pack", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

def build(data: dict) -> Path:
    config.data_dir.mkdir(parents=True, exist_ok=True)
    safe_title = data["title"].replace(" ", "_").replace("/", "-")[:60]
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{date_str}_{safe_title}.pdf"
    filepath = config.data_dir / filename

    pdf = PromptPackPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 10, data["title"], align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, data["description"])
    pdf.ln(4)

    for category in data["prompts"]:
        if pdf.get_y() > 240:
            pdf.add_page()
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(0, 70, 74)
        pdf.cell(0, 8, category["category"], new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)

        for i, prompt in enumerate(category["prompts"], 1):
            if pdf.get_y() > 250:
                pdf.add_page()
            pdf.multi_cell(0, 5, f"{i}. {prompt}")
            pdf.ln(2)

    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, f"Generated with DeepSeek V4 Flash | {datetime.now().strftime('%Y-%m-%d')}",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Get more at: gumroad.com/your-store",
             align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(filepath))
    return filepath
