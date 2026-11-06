from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted, Image, KeepTogether
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SCREENSHOTS = ROOT / "evidence" / "screenshots" / "kali"
OUTPUT_DIR = ROOT / "reports"
OUTPUT_PDF = OUTPUT_DIR / "NetworkWalks-B084N-Kali-Lab-Technical-Report.pdf"

SOURCE_DOCS = [
    "01-objectives.md",
    "02-prerequisites.md",
    "03-virtualbox-setup.md",
    "04-kali-configuration.md",
    "05-network-configuration.md",
    "06-verification.md",
    "07-troubleshooting.md",
]

CAPTIONS = {
    "K01-virtualbox-version.jpeg": (
        "K01 — Oracle VirtualBox version",
        "Host hypervisor version recorded for the lab environment."
    ),
    "K02-nat-network.png": (
        "K02 — NAT Network configuration",
        "NetworkWalks-NAT network configuration, including subnet and DHCP setting."
    ),
    "K03a-kali-motherboard.jpeg": (
        "K03a — Virtual machine base hardware",
        "Kali virtual machine motherboard and base configuration."
    ),
    "K03b-kali-processor.png": (
        "K03b — Virtual processor allocation",
        "Two virtual CPUs assigned to the Kali guest."
    ),
    "K03c-kali-display.png": (
        "K03c — Virtual display configuration",
        "Video memory and display acceleration configuration."
    ),
    "K04-kali-network-adapter.png": (
        "K04 — Virtual network adapter",
        "Adapter model and NAT Network attachment used by the Kali guest."
    ),
    "K05-clipboard-dragdrop.jpeg": (
        "K05 — Integration settings",
        "Bidirectional shared clipboard and drag-and-drop settings. These settings were configured; a separate functional transfer test was not recorded."
    ),
    "K06-shared-folder-configuration.png": (
        "K06 — Shared folder configuration",
        "Shared-Files host share and guest mount configuration."
    ),
    "K07-static-ip-configuration.png": (
        "K07 — Static IPv4 configuration",
        "NetworkManager configuration for the Kali guest's static IPv4 settings."
    ),
    "K08-ip-route-device-status.png": (
        "K08 — Interface and routing verification",
        "Recorded interface address and routing table."
    ),
    "K09-K10-connectivity-tests.png": (
        "K09–K10 — Connectivity tests",
        "Gateway and external IP connectivity test results."
    ),
    "K11-dns-resolution.png": (
        "K11 — DNS resolution",
        "Successful DNS lookup using the configured DNS resolver."
    ),
    "K12-shared-folder-access.png": (
        "K12 — Shared folder access test",
        "Successful read of the shared-folder test file from Kali."
    ),
    "K13-kali-base-snapshot.png": (
        "K13 — Baseline snapshot",
        "VirtualBox snapshot created after the base Kali lab configuration."
    ),
}

NAVY = colors.HexColor("#101827")
BURGUNDY = colors.HexColor("#7D2438")
INK = colors.HexColor("#202633")
MUTED = colors.HexColor("#667085")
PALE = colors.HexColor("#F2F4F7")
LINE = colors.HexColor("#D8DDE5")
WHITE = colors.white


def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "CoverTitle": ParagraphStyle(
            "CoverTitle", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=27, leading=33, textColor=WHITE, alignment=TA_LEFT,
            spaceAfter=12
        ),
        "CoverSub": ParagraphStyle(
            "CoverSub", parent=base["Normal"], fontName="Helvetica",
            fontSize=12, leading=18, textColor=colors.HexColor("#E7EAF0"),
            alignment=TA_LEFT
        ),
        "CoverMeta": ParagraphStyle(
            "CoverMeta", parent=base["Normal"], fontName="Helvetica",
            fontSize=9, leading=14, textColor=colors.HexColor("#D4D9E2")
        ),
        "FrontHeading": ParagraphStyle(
            "FrontHeading", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=19, leading=24, textColor=NAVY, spaceBefore=4, spaceAfter=12
        ),
        "Heading1": ParagraphStyle(
            "Heading1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=16, leading=20, textColor=NAVY, spaceBefore=14, spaceAfter=8,
            keepWithNext=True
        ),
        "Heading2": ParagraphStyle(
            "Heading2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=12, leading=16, textColor=BURGUNDY, spaceBefore=10,
            spaceAfter=5, keepWithNext=True
        ),
        "Heading3": ParagraphStyle(
            "Heading3", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=10, leading=13, textColor=INK, spaceBefore=7,
            spaceAfter=4, keepWithNext=True
        ),
        "Body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Helvetica",
            fontSize=9, leading=13.2, textColor=INK, spaceAfter=6,
            alignment=TA_LEFT
        ),
        "Bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"], fontName="Helvetica",
            fontSize=9, leading=12.5, textColor=INK, leftIndent=13,
            firstLineIndent=-8, spaceAfter=3
        ),
        "Small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName="Helvetica",
            fontSize=8, leading=11, textColor=MUTED, spaceAfter=4
        ),
        "Code": ParagraphStyle(
            "Code", fontName="Courier", fontSize=7.2, leading=9.2,
            textColor=INK, backColor=PALE, borderColor=LINE,
            borderWidth=0.4, borderPadding=6, leftIndent=4, rightIndent=4,
            spaceBefore=4, spaceAfter=8
        ),
        "Table": ParagraphStyle(
            "Table", parent=base["BodyText"], fontName="Helvetica",
            fontSize=7.6, leading=10, textColor=INK
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=7.6, leading=10, textColor=WHITE
        ),
        "Caption": ParagraphStyle(
            "Caption", parent=base["BodyText"], fontName="Helvetica",
            fontSize=8, leading=11, textColor=MUTED, alignment=TA_CENTER,
            spaceBefore=5, spaceAfter=4
        ),
        "ImageTitle": ParagraphStyle(
            "ImageTitle", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=10, leading=13, textColor=NAVY, alignment=TA_CENTER,
            spaceBefore=3, spaceAfter=4
        ),
    }
    return styles


def inline_markup(text: str) -> str:
    text = escape(text.strip())
    # Links first, then emphasis/code.
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<link href="\2" color="#7D2438">\1</link>', text
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    return text


def split_table_row(line: str):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def parse_markdown(path: Path, styles):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    story = []
    paragraph_lines = []
    i = 0

    def flush_paragraph():
        nonlocal paragraph_lines
        if paragraph_lines:
            text = " ".join(part.strip() for part in paragraph_lines if part.strip())
            if text:
                story.append(Paragraph(inline_markup(text), styles["Body"]))
            paragraph_lines = []

    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            flush_paragraph()
            i += 1
            continue

        if line.lstrip().startswith("```"):
            flush_paragraph()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].lstrip().startswith("```"):
                code_lines.append(lines[i].rstrip())
                i += 1
            if i < len(lines):
                i += 1
            code_text = "\n".join(code_lines).replace("\t", "    ")
            story.append(Preformatted(code_text, styles["Code"], maxLineLength=100))
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            style = styles[f"Heading{level}"]
            story.append(Paragraph(inline_markup(heading.group(2)), style))
            i += 1
            continue

        if line.strip() in ("---", "***", "___"):
            flush_paragraph()
            story.append(Spacer(1, 4))
            i += 1
            continue

        # Markdown table: header row followed by separator row.
        if "|" in line and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            flush_paragraph()
            raw_rows = [split_table_row(line)]
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                raw_rows.append(split_table_row(lines[i]))
                i += 1
            col_count = max(len(row) for row in raw_rows)
            table_data = []
            for row_index, row in enumerate(raw_rows):
                row = row + [""] * (col_count - len(row))
                style = styles["TableHeader"] if row_index == 0 else styles["Table"]
                table_data.append([Paragraph(inline_markup(cell), style) for cell in row])
            available_width = A4[0] - 36 * mm
            col_widths = [available_width / col_count] * col_count
            tbl = Table(table_data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
            ]))
            story.extend([Spacer(1, 4), tbl, Spacer(1, 8)])
            continue

        bullet = re.match(r"^\s*[-*+]\s+(.+)$", line)
        numbered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if bullet or numbered:
            flush_paragraph()
            content = bullet.group(1) if bullet else numbered.group(1)
            marker = "•" if bullet else "–"
            story.append(Paragraph(
                f"{marker} {inline_markup(content)}",
                styles["Bullet"]
            ))
            i += 1
            continue

        if line.lstrip().startswith(">"):
            flush_paragraph()
            quote = line.lstrip()[1:].strip()
            story.append(Paragraph(
                f'<font color="#7D2438"><b>Note:</b></font> {inline_markup(quote)}',
                styles["Body"]
            ))
            i += 1
            continue

        paragraph_lines.append(line)
        i += 1

    flush_paragraph()
    return story


class ReportDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            18 * mm, 17 * mm, A4[0] - 36 * mm, A4[1] - 34 * mm,
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
            id="normal"
        )
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=self.draw_page)])

    def draw_page(self, canvas, doc):
        canvas.saveState()
        if doc.page == 1:
            canvas.setFillColor(NAVY)
            canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
            canvas.setFillColor(BURGUNDY)
            canvas.rect(0, 0, 9 * mm, A4[1], fill=1, stroke=0)
        else:
            canvas.setStrokeColor(LINE)
            canvas.setLineWidth(0.5)
            canvas.line(18 * mm, A4[1] - 13 * mm, A4[0] - 18 * mm, A4[1] - 13 * mm)
            canvas.setFont("Helvetica-Bold", 7.5)
            canvas.setFillColor(NAVY)
            canvas.drawString(18 * mm, A4[1] - 10 * mm, "NETWORKWALKS  /  B084N")
            canvas.setFont("Helvetica", 7.5)
            canvas.setFillColor(MUTED)
            canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {doc.page}")
            canvas.line(18 * mm, 14 * mm, A4[0] - 18 * mm, 14 * mm)
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style_name = flowable.style.name
            if style_name in ("Heading1", "Heading2"):
                level = 0 if style_name == "Heading1" else 1
                text = flowable.getPlainText()
                key = f"h{level}-{self.seq.nextf('heading')}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level, closed=False)
                self.notify("TOCEntry", (level, text, self.page, key))


def add_evidence_gallery(story, styles):
    story.append(PageBreak())
    story.append(Paragraph("Evidence Gallery", styles["Heading1"]))
    story.append(Paragraph(
        "The following images are the project evidence supplied in "
        "evidence/screenshots/kali/. Captions describe what each image records; "
        "they do not imply additional tests beyond those documented.",
        styles["Body"]
    ))

    if not SCREENSHOTS.exists():
        story.append(Paragraph(
            "Screenshot directory not found. The evidence gallery could not be generated.",
            styles["Body"]
        ))
        return

    files = sorted(
        p for p in SCREENSHOTS.iterdir()
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )
    if not files:
        story.append(Paragraph("No screenshot files were found.", styles["Body"]))
        return

    for index, path in enumerate(files):
        title, caption = CAPTIONS.get(
            path.name, (path.stem, "Project evidence screenshot.")
        )
        story.append(PageBreak() if index > 0 else Spacer(1, 6))
        story.append(Paragraph(escape(title), styles["ImageTitle"]))

        try:
            with PILImage.open(path) as im:
                width_px, height_px = im.size
            max_w = A4[0] - 42 * mm
            max_h = A4[1] - 82 * mm
            scale = min(max_w / width_px, max_h / height_px)
            img = Image(str(path), width=width_px * scale, height=height_px * scale)
            img.hAlign = "CENTER"
            story.append(Spacer(1, 5))
            story.append(img)
            story.append(Paragraph(escape(caption), styles["Caption"]))
            story.append(Paragraph(
                f"<font name='Courier'>{escape(path.name)}</font>  ·  "
                f"{width_px} × {height_px} px",
                styles["Small"]
            ))
        except Exception as exc:
            story.append(Paragraph(
                f"Could not render {escape(path.name)}: {escape(str(exc))}",
                styles["Body"]
            ))


def build_report():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    story = []

    # Cover
    story.extend([
        Spacer(1, 46 * mm),
        Paragraph("NETWORKWALKS", styles["CoverMeta"]),
        Spacer(1, 8 * mm),
        Paragraph("Cybersecurity Lab<br/>Environment Setup", styles["CoverTitle"]),
        Paragraph("Kali Linux virtual lab — technical project report", styles["CoverSub"]),
        Spacer(1, 18 * mm),
        Paragraph("<b>Prepared by</b>  Madhurja Bhattacharjee", styles["CoverMeta"]),
        Paragraph("<b>Batch ID</b>  B084N", styles["CoverMeta"]),
        Paragraph("<b>Project</b>  Week 1 · Project Module 1", styles["CoverMeta"]),
        Paragraph("<b>Host</b>  Windows 11", styles["CoverMeta"]),
        Paragraph("<b>Hypervisor</b>  Oracle VirtualBox 7.2.8", styles["CoverMeta"]),
        Paragraph("<b>Guest</b>  Kali Linux 2026.3", styles["CoverMeta"]),
        Spacer(1, 35 * mm),
        Paragraph(
            f"Prepared from the project's Markdown documentation and recorded evidence · {date.today():%d %B %Y}",
            styles["CoverMeta"]
        ),
        PageBreak(),
    ])

    # Contents
    story.append(Paragraph("Contents", styles["FrontHeading"]))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            "TOCLevel0", fontName="Helvetica-Bold", fontSize=9.5,
            leading=14, leftIndent=0, firstLineIndent=0, textColor=NAVY,
            spaceBefore=4
        ),
        ParagraphStyle(
            "TOCLevel1", fontName="Helvetica", fontSize=8.5,
            leading=12, leftIndent=14, firstLineIndent=0, textColor=INK
        ),
    ]
    story.append(toc)
    story.append(PageBreak())

    # Executive summary and factual configuration overview
    story.append(Paragraph("Executive Summary", styles["Heading1"]))
    story.append(Paragraph(
        "This report documents the setup and verification of a Kali Linux "
        "cybersecurity lab running as a virtual machine on a Windows 11 host. "
        "The work establishes a repeatable base environment, configures a "
        "dedicated VirtualBox NAT Network, assigns a static guest IPv4 address, "
        "checks routing, external connectivity and DNS resolution, validates "
        "shared-folder access, and records a baseline snapshot.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "The documented results support the conclusion that the Kali guest "
        "had working connectivity to its configured gateway and an external "
        "IP address, successfully resolved a domain name, and read a test file "
        "from the configured shared folder. Clipboard and drag-and-drop were "
        "enabled in VirtualBox settings, but a separate functional transfer "
        "test was not recorded.",
        styles["Body"]
    ))

    story.append(Paragraph("Environment at a Glance", styles["Heading2"]))
    overview = [
        [Paragraph("Item", styles["TableHeader"]), Paragraph("Recorded configuration", styles["TableHeader"])],
        ["Host operating system", "Windows 11"],
        ["Hypervisor", "Oracle VirtualBox 7.2.8r173730"],
        ["Guest operating system", "Kali Linux 2026.3"],
        ["VM resources", "2 GB RAM · 2 virtual CPUs · 128 MB video memory"],
        ["Network mode", "NAT Network — NetworkWalks-NAT"],
        ["Network range", "10.0.0.0/24 · DHCP disabled"],
        ["Guest IPv4 / gateway", "10.0.0.2/24 · 10.0.0.1"],
        ["DNS resolver", "8.8.8.8"],
        ["Shared folder", "Shared-Files → /downloads"],
        ["Baseline snapshot", "NetworkWalks-Kali-Base-Setup"],
    ]
    overview = [
        [cell if isinstance(cell, Paragraph) else Paragraph(escape(cell), styles["Table"])
         for cell in row]
        for row in overview
    ]
    overview_table = Table(overview, colWidths=[48 * mm, 120 * mm], repeatRows=1)
    overview_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.extend([overview_table, Spacer(1, 10)])

    story.append(Paragraph("Implementation Status", styles["Heading2"]))
    status_rows = [
        [Paragraph("Status", styles["TableHeader"]), Paragraph("Items", styles["TableHeader"])],
        ["Configured and verified", "Static IPv4, routing table, gateway ping, external IP ping, DNS lookup, shared-folder file read, baseline snapshot."],
        ["Configured; functional test not recorded", "Bidirectional shared clipboard and drag-and-drop."],
        ["Planned / not completed in this phase", "Android-x86 VM, Windows 10 VM, inter-VM connectivity testing, Wireshark browser-based labs."],
    ]
    status_rows = [
        [cell if isinstance(cell, Paragraph) else Paragraph(escape(cell), styles["Table"])
         for cell in row]
        for row in status_rows
    ]
    status_table = Table(status_rows, colWidths=[53 * mm, 115 * mm], repeatRows=1)
    status_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([status_table, Spacer(1, 8)])

    story.append(Paragraph("Important Configuration Notes", styles["Heading2"]))
    notes = [
        "The VirtualBox VM display name contains an older image label (2026.1), while the installed guest operating system reports Kali Linux 2026.3. The report distinguishes the VM label from the guest OS version.",
        "The host shared-folder directory is intentionally redacted in the configuration record; the share name and guest mount point are documented.",
        "A NAT Network provides address translation and connectivity; it should not be treated as a complete security-isolation boundary. Host firewall policy and guest configuration remain relevant.",
        "The interface state string UNKNOWN, as displayed by ip -br addr, is not by itself proof of failed connectivity. The recorded gateway and external connectivity tests succeeded.",
        "The verification text file is a curated record of previously observed results, not a fresh command execution log.",
    ]
    for note in notes:
        story.append(Paragraph(f"• {escape(note)}", styles["Bullet"]))

    # Main documentation, sourced directly from the repository Markdown.
    for filename in SOURCE_DOCS:
        path = DOCS / filename
        story.append(PageBreak())
        if path.exists():
            story.extend(parse_markdown(path, styles))
        else:
            story.append(Paragraph(
                f"Source document missing: {escape(filename)}",
                styles["Body"]
            ))

    # Screenshot evidence
    add_evidence_gallery(story, styles)

    # Appendix: source inventory and evidence interpretation
    story.append(PageBreak())
    story.append(Paragraph("Appendix A — Source and Evidence Inventory", styles["Heading1"]))
    story.append(Paragraph(
        "This report is generated from the following repository materials. "
        "The Markdown files remain the authoritative editable documentation; "
        "this PDF is a formatted report derived from them and the recorded screenshots.",
        styles["Body"]
    ))
    for filename in SOURCE_DOCS:
        story.append(Paragraph(f"• docs/{escape(filename)}", styles["Bullet"]))
    story.append(Paragraph("Evidence directory", styles["Heading2"]))
    story.append(Paragraph(
        "evidence/screenshots/kali/ — screenshot files K01 through K13 "
        "(14 image files; K03 is split into three images and K09/K10 share one image).",
        styles["Body"]
    ))

    story.append(Paragraph("Appendix B — Scope and Safe Use", styles["Heading1"]))
    story.append(Paragraph(
        "This environment is intended for authorized cybersecurity education, "
        "controlled lab exercises, and defensive learning. Testing against "
        "systems or networks without explicit permission is outside the scope "
        "of this project. Keep intentionally vulnerable targets isolated and "
        "use only lab assets for practical exercises.",
        styles["Body"]
    ))

    doc = ReportDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        title="NetworkWalks B084N — Kali Linux Cybersecurity Lab Technical Report",
        author="Madhurja Bhattacharjee",
        subject="VirtualBox and Kali Linux lab setup, configuration, and verification",
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )
    doc.multiBuild(story)

    print(f"PDF created: {OUTPUT_PDF}")
    print(f"Size: {OUTPUT_PDF.stat().st_size:,} bytes")
    print(f"Screenshot files found: {len(list(SCREENSHOTS.glob('*')))}")


if __name__ == "__main__":
    build_report()
