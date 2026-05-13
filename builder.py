from pathlib import Path
from datetime import datetime
from fpdf import FPDF
from config import config

FONT_URLS = {
    "DejaVuSans.ttf": "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf",
    "DejaVuSans-Bold.ttf": "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans-Bold.ttf",
}
FONT_DIR = Path(__file__).parent

def _ensure_fonts():
    import urllib.request
    for name, url in FONT_URLS.items():
        p = FONT_DIR / name
        if not p.exists():
            print(f"  Downloading {name}...")
            urllib.request.urlretrieve(url, p)

class PromptPackPDF(FPDF):
    def __init__(self):
        super().__init__()
        _ensure_fonts()
        self.add_font("DejaVu", "", str(FONT_DIR / "DejaVuSans.ttf"), uni=True)
        self.add_font("DejaVu", "B", str(FONT_DIR / "DejaVuSans-Bold.ttf"), uni=True)

    def header(self):
        self.set_font("DejaVu", "B", 10)
        self.cell(0, 8, "DeepSeek Prompt Pack", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
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

    pdf.set_font("DejaVu", "B", 18)
    pdf.multi_cell(0, 10, data["title"], align="C")
    pdf.ln(4)

    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(0, 6, data["description"])
    pdf.ln(4)

    for category in data["prompts"]:
        if pdf.get_y() > 240:
            pdf.add_page()
        pdf.set_font("DejaVu", "B", 13)
        pdf.set_text_color(0, 70, 74)
        pdf.cell(0, 8, category["category"], new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("DejaVu", "", 10)

        for i, prompt in enumerate(category["prompts"], 1):
            if pdf.get_y() > 250:
                pdf.add_page()
            pdf.multi_cell(0, 5, f"{i}. {prompt}")
            pdf.ln(2)

    pdf.ln(10)
    pdf.set_font("DejaVu", "", 9)
    pdf.cell(0, 6, f"Generated with DeepSeek V4 Flash | {datetime.now().strftime('%Y-%m-%d')}",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Get more at: gumroad.com/your-store",
             align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(filepath))
    return filepath
