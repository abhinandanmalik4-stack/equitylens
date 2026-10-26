"""Render the saved roadmap overview. Requires Pillow; no network access."""

from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "assets" / "equitylens-eight-week-roadmap.png"
W, H = 1800, 2010
BG, INK, MUTED = "#F3F5F2", "#142A27", "#4D625C"
GREEN, PALE = "#205D4B", "#E0EAE3"
FONT_DIR = Path("C:/Windows/Fonts")


def font(size, bold=False):
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    if (FONT_DIR / name).exists():
        return ImageFont.truetype(str(FONT_DIR / name), size)
    return ImageFont.truetype("DejaVuSans.ttf", size)


weeks = [
    ("01", "Foundation", "Python environments, Git, modules, Streamlit widgets and session state.",
     "Set up the project; build company selection and an interactive chart using labelled sample data.",
     "App runs locally; selection updates the chart; sample prices are unmistakably labelled."),
    ("02", "Historical data", "APIs, pandas, OHLCV, adjusted prices, date handling and caching.",
     "Select a provider; fetch and validate daily history for 10-20 Indian stocks; record provenance.",
     "Real data has a source and as-of date; errors and stale data are handled explicitly."),
    ("03", "Dashboard", "Plotly charts, returns, date alignment, SQLite and persistent watchlists.",
     "Add chart ranges, volume, daily change, comparisons and saved watchlist; review the layout.",
     "Metrics match data; watchlist survives restart; chart ranges and comparisons work."),
    ("04", "Baseline", "Forecast targets, chronological splits, leakage prevention, MAE and RMSE.",
     "Define target/horizon; build a persistence baseline; run reproducible walk-forward evaluation.",
     "Past-only predictions, recorded split dates and repeatable per-stock baseline results."),
    ("05", "ML + uncertainty", "Lagged features, model selection, training-only preprocessing and interval coverage.",
     "Train one model; compare with baseline on untouched test data; assess prediction intervals.",
     "Honest model comparison and measured uncertainty; no promised accuracy or returns."),
    ("06", "Company evidence", "Reliable documents, text extraction, metadata, chunking and retrieval evaluation.",
     "Start with 2-3 companies; index official documents; retrieve relevant passages with locators.",
     "Evidence traces to a company, document date, URL and page/section; retrieval is checked."),
    ("07", "Research chatbot", "Grounded answers, LLM access, citations, tool use and answer evaluation.",
     "Add chat; answer from retrieved evidence; get prices from data functions; test missing evidence.",
     "Supported answers cite sources; numeric results are traceable; unknowns are acknowledged."),
    ("08", "Test + present", "Integration checks, errors, deployment, reproducibility and architecture explanation.",
     "Test flows; prepare a verified demo if hosting is ready; finish report, README and walkthrough.",
     "Reproducible setup/evaluation, clear limitations and an explainable project demonstration."),
]

im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
d.rectangle((0, 0, W, 285), fill=INK)
d.text((64, 34), "EQUITYLENS / BUILD & LEARN", font=font(23, True), fill="#B2D1C0")
d.text((60, 81), "Your eight-week project roadmap", font=font(56, True), fill="#FFFFFF")
d.text((64, 160), "Python + Streamlit  /  Plotly  /  pandas + NumPy  /  SQLite  /  scikit-learn", font=font(25), fill="#E1EBE4")
d.text((64, 211), "Indian stocks first. US support later. No handwritten HTML, CSS or JavaScript required.", font=font(24), fill="#E1EBE4")
d.text((64, 316), "PLAN ASSUMPTION", font=font(20, True), fill=GREEN)
d.text((64, 351), "1-2 hours/day, 5-6 days/week. Weeks start when development begins; dates are not fixed.", font=font(25), fill=INK)
d.text((64, 389), "Current status: planning + repository setup only. All application milestones below are planned.", font=font(23), fill=MUTED)
xs = [64, 365, 800, 1320]
d.rectangle((48, 447, W - 48, 499), fill=GREEN)
for x, label in zip(xs, ["WEEK / FOCUS", "LEARN", "BUILD", "DONE WHEN"]):
    d.text((x, 460), label, font=font(21, True), fill="#FFFFFF")


def paragraph(text, x, y, width, size=23):
    f = font(size)
    words = text.split()
    lines, line = [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if d.textlength(candidate, font=f) > width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    for n, line in enumerate(lines):
        d.text((x, y + n * 33), line, font=f, fill=INK)
    assert len(lines) * 33 <= 142, (text, lines)


for i, (number, title, learn, build, done) in enumerate(weeks):
    y = 500 + i * 163
    d.rectangle((48, y, W - 48, y + 162), fill="#FFFFFF" if i % 2 == 0 else "#EAF0E9")
    d.text((64, y + 20), "WEEK " + number, font=font(21, True), fill=GREEN)
    paragraph(title, 64, y + 60, 270, size=27)
    paragraph(learn, 365, y + 20, 395)
    paragraph(build, 800, y + 20, 480)
    paragraph(done, 1320, y + 20, 405)

d.text((64, 1838), "WEEKLY RHYTHM", font=font(20, True), fill=GREEN)
d.text((64, 1874), "Learn -> build -> verify -> explain -> document. Day 6: review/demo. Day 7: buffer/rest.", font=font(24), fill=INK)
d.text((64, 1920), "Advance after milestone checks pass. Make meaningful commits; never invent results or filler activity.", font=font(23), fill=MUTED)
d.text((64, 1962), "Detailed daily tasks: docs/WEEKLY_ROADMAP.md   |   Updated 26 October 2026 (IST)", font=font(20), fill=MUTED)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
im.save(OUTPUT, optimize=True)
print(OUTPUT)
