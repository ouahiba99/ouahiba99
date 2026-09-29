#!/usr/bin/env python3
"""
Builds the dark "card" SVGs that sit under each section header of the README.

GitHub strips CSS / bgcolor from README HTML, so the only way to give a block of
text a background is to draw the text inside an SVG. Colours live in P below;
change them to match your section-header SVGs, then run:

    python generate_cards.py

Output: assets/cards/*.svg
"""
import os
import re
from xml.sax.saxutils import escape

OUT_DIR = os.path.join("assets", "cards")
W = 900   # SVG units; the README displays each card at width="100%"
PAD = 28

P = {
    "bg_top": "#0a1330",
    "bg_bottom": "#050b1f",
    "border": "#1b2f66",
    "panel": "#0d1a3d",
    "panel_border": "#1f3a7a",
    "accent": "#4d9dff",
    "accent_light": "#7db8ff",
    "text": "#dbe9ff",
    "muted": "#8fa6cc",
    "green": "#3ddc84",
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'SF Mono','Fira Code',Consolas,'Liberation Mono','Courier New',monospace"

# Conservative average glyph widths (em) used only for line wrapping.
SANS_K, BOLD_K, MONO_K = 0.58, 0.62, 0.62


# --------------------------------------------------------------------------- text helpers
def tokenize(s):
    """Split 'a **bold** b' into words; each word is a list of (text, is_bold)."""
    words, cur = [], []
    for i, part in enumerate(s.split("**")):
        bold = i % 2 == 1
        for m in re.finditer(r"\s+|\S+", part):
            t = m.group()
            if t.isspace():
                if cur:
                    words.append(cur)
                    cur = []
            else:
                cur.append((t, bold))
    if cur:
        words.append(cur)
    return words


def width_of(word, size):
    return sum(len(t) * size * (BOLD_K if b else SANS_K) for t, b in word)


def wrap(s, size, max_w):
    lines, line, line_w = [], [], 0.0
    space = size * 0.30
    for word in tokenize(s):
        w = width_of(word, size)
        add = w if not line else space + w
        if line and line_w + add > max_w:
            lines.append(line)
            line, line_w = [word], w
        else:
            line.append(word)
            line_w += add
    if line:
        lines.append(line)
    return lines


def wrap_balanced(s, size, max_w):
    """Same line count as wrap(), but with evenly filled lines (no one-word orphans)."""
    n = len(wrap(s, size, max_w))
    if n < 2:
        return wrap(s, size, max_w)
    lo, hi = 0.0, float(max_w)
    for _ in range(24):
        mid = (lo + hi) / 2
        if len(wrap(s, size, mid)) <= n:
            hi = mid
        else:
            lo = mid
    return wrap(s, size, hi)


def runs_to_svg(line):
    out = []
    for i, word in enumerate(line):
        if i:
            out.append(" ")
        for t, b in word:
            out.append(f'<tspan class="b">{escape(t)}</tspan>' if b else escape(t))
    return "".join(out)


def text_block(x, y, s, size, max_w, lh, cls="t", balance=False):
    """Returns (svg, baseline_of_last_line)."""
    lines = (wrap_balanced if balance else wrap)(s, size, max_w)
    out = [
        f'<text x="{x}" y="{y + i * lh}" class="{cls}" font-size="{size}" '
        f'xml:space="preserve">{runs_to_svg(ln)}</text>'
        for i, ln in enumerate(lines)
    ]
    return "\n".join(out), y + (len(lines) - 1) * lh


def bullet_list(x, y, items, size, max_w, gap=8):
    """Returns (svg, baseline_of_last_line)."""
    lh = round(size * 1.4)
    out, cy, last = [], y, y
    for item in items:
        lines = wrap(item, size, max_w - 16)
        out.append(
            f'<circle cx="{x + 3}" cy="{cy - size * 0.32:.1f}" r="2.6" fill="{P["accent"]}"/>'
        )
        for i, ln in enumerate(lines):
            out.append(
                f'<text x="{x + 16}" y="{cy + i * lh}" class="t" font-size="{size}" '
                f'xml:space="preserve">{runs_to_svg(ln)}</text>'
            )
        last = cy + (len(lines) - 1) * lh
        cy = last + lh + gap
    return "\n".join(out), last


def pills(x, y, tags, size=12.5, gap=8):
    out = []
    for t in tags:
        w = len(t) * size * MONO_K + 22
        out.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" '
            f'fill="{P["accent"]}" fill-opacity="0.12" stroke="{P["accent"]}" stroke-opacity="0.55"/>'
        )
        out.append(
            f'<text x="{x + w / 2:.1f}" y="{y + 16}" text-anchor="middle" class="k" '
            f'font-size="{size}">{escape(t)}</text>'
        )
        x += w + gap
    return "\n".join(out)


# --------------------------------------------------------------------------- card shell
def shell(h, body, desc):
    d = escape(desc, {'"': "&quot;"})
    css = "\n".join(
        [
            f".t{{font-family:{SANS};fill:{P['text']}}}",
            f".b{{font-weight:700;fill:{P['accent_light']}}}",
            f".ti{{font-family:{SANS};font-weight:700;fill:#ffffff}}",
            f".h{{font-family:{MONO};font-weight:700;letter-spacing:1.6px;fill:{P['accent']}}}",
            f".k{{font-family:{MONO};fill:{P['accent_light']}}}",
            f".d{{font-family:{MONO};fill:{P['muted']}}}",
        ]
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="{d}">
<title>{escape(desc)}</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P['bg_top']}"/><stop offset="1" stop-color="{P['bg_bottom']}"/></linearGradient>
<radialGradient id="glow" cx="0.92" cy="0" r="0.75"><stop offset="0" stop-color="{P['accent']}" stop-opacity="0.16"/><stop offset="1" stop-color="{P['accent']}" stop-opacity="0"/></radialGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P['accent']}" stop-opacity="0"/><stop offset="0.5" stop-color="{P['accent_light']}"/><stop offset="1" stop-color="{P['accent']}" stop-opacity="0"/></linearGradient>
<clipPath id="clip"><rect width="{W}" height="{h}" rx="14"/></clipPath>
</defs>
<style>
{css}
</style>
<g clip-path="url(#clip)">
<rect width="{W}" height="{h}" fill="url(#bg)"/>
<rect width="{W}" height="{h}" fill="url(#glow)"/>
<rect x="60" y="0" width="{W - 120}" height="2" fill="url(#edge)"/>
{body}
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="14" fill="none" stroke="{P['border']}"/>
</svg>
"""


def panel_rect(x, y, w, h):
    return (
        f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="10" '
        f'fill="{P["panel"]}" fill-opacity="0.6" stroke="{P["panel_border"]}" stroke-opacity="0.75"/>'
    )


def panel_grid(panels, ncols, size, y0, gap=20):
    """Rows of equal-height panels. Returns (svg, bottom_y)."""
    pw = (W - 2 * PAD - gap * (ncols - 1)) / ncols
    out, y = [], y0
    for r in range(0, len(panels), ncols):
        laid = []
        for c, (head, items) in enumerate(panels[r:r + ncols]):
            x = PAD + c * (pw + gap)
            svg, last = bullet_list(x + 20, y + 66, items, size, pw - 44)
            laid.append((x, head, svg, last))
        ph = max(item[3] for item in laid) - y + 24
        for x, head, svg, _ in laid:
            out.append(panel_rect(x, y, pw, ph))
            out.append(f'<rect x="{x + 20:.1f}" y="{y + 20}" width="3" height="18" rx="1.5" fill="{P["accent"]}"/>')
            out.append(f'<text x="{x + 34:.1f}" y="{y + 34}" class="h" font-size="13">{escape(head)}</text>')
            out.append(svg)
        y += ph + gap
    return "\n".join(out), y - gap


# --------------------------------------------------------------------------- cards
def card_overview():
    x, mw = PAD + 22, W - 2 * PAD - 44
    p1 = ("I'm a **Telecom & ICT State Engineer** and **DataOps & Cloud Consultant** focused on "
          "building reliable systems at the intersection of **data engineering**, "
          "**cloud infrastructure**, **MLOps**, and **telecom operations**.")
    p2 = ("I enjoy turning complex technical requirements into "
          "**automated, observable, and production-ready solutions**.")
    a, last_a = text_block(x, 62, p1, 17, mw, 28)
    b, last_b = text_block(x, last_a + 44, p2, 17, mw, 28)
    h = last_b + 34
    bar = f'<rect x="{PAD}" y="36" width="3" height="{h - 72}" rx="1.5" fill="{P["accent"]}"/>'
    desc = "Telecom & ICT State Engineer and DataOps & Cloud Consultant building reliable systems across data engineering, cloud infrastructure, MLOps and telecom operations."
    return shell(h, "\n".join([bar, a, b]), desc)


CAPS = [
    ("DATA ENGINEERING", ["ETL / ELT orchestration", "Python, SQL, Spark",
                          "PostgreSQL, MongoDB, Redis", "Airflow, Prefect"]),
    ("CLOUD INFRASTRUCTURE", ["GCP, Azure", "Docker, Kubernetes", "Linux, Nginx",
                              "Production-ready deployment"]),
    ("MLOPS & AUTOMATION", ["MLflow, DVC", "FastAPI services", "CI/CD automation",
                            "Operational reliability"]),
    ("OBSERVABILITY & TELECOM", ["Prometheus, Grafana", "Kibana & log analysis",
                                 "OSS / BSS operations", "Network monitoring and support"]),
]


def card_capabilities():
    body, bottom = panel_grid(CAPS, 2, 15.5, PAD)
    return shell(bottom + PAD, body,
                 "Core capabilities: data engineering, cloud infrastructure, MLOps and automation, observability and telecom.")


def card_project(title, subtitle, tags, items, desc, hint=None):
    body = [
        f'<circle cx="{PAD + 8}" cy="46" r="10" fill="{P["green"]}" fill-opacity="0.16"/>',
        f'<circle cx="{PAD + 8}" cy="46" r="4.5" fill="{P["green"]}"/>',
        f'<text x="{PAD + 28}" y="53" class="ti" font-size="21">{escape(title)}</text>',
    ]
    sub, last = text_block(PAD + 2, 90, f"**{subtitle}**", 15.5, W - 2 * PAD - 4, 22, balance=True)
    body.append(sub)
    py = last + 18
    body.append(pills(PAD + 2, py, tags))
    if hint:
        body.append(
            f'<text x="{W - PAD}" y="{py + 16.5}" text-anchor="end" class="d" font-size="12">{escape(hint)}</text>'
        )
    lst, last_b = bullet_list(PAD + 2, py + 24 + 34, items, 15.5, W - 2 * PAD - 4)
    body.append(lst)
    return shell(last_b + 30, "\n".join(body), desc)


EXPERIENCE = [
    ("DATA / ANALYTICS OPERATIONS", [
        "Built and maintained production data processing and ETL workflows",
        "Worked with Python, SQL, Spark, NoSQL, and workflow orchestration",
        "Supported monitoring, troubleshooting, and incident investigation",
        "Collaborated with international B2B technical teams",
    ]),
    ("TELECOM NETWORK OPERATIONS", [
        "Network monitoring and performance analysis across OSS platforms",
        "Incident investigation and troubleshooting",
        "Exposure to Nagios, Zabbix, NetAct, ENM, U2020, Jira, and Power BI",
        "Support for multinational telecom operators and teams",
    ]),
]


def card_experience():
    body, bottom = panel_grid(EXPERIENCE, 2, 14.5, PAD)
    return shell(bottom + PAD, body,
                 "Work experience: data and analytics operations, and telecom network operations.")


def card_academy():
    x = PAD + 22
    body = [
        f'<text x="{x}" y="60" class="ti" font-size="24">ITAAR Academy</text>',
        f'<text x="{x}" y="86" class="h" font-size="13">FOUNDER · TECHNOLOGY &amp; PRACTICAL LEARNING</text>',
    ]
    d, last = text_block(
        x, 122,
        "ITAAR Academy is a practical learning initiative focused on helping people "
        "learn, practice, and share useful skills.",
        15.5, W - 2 * PAD - 44, 23, balance=True)
    body.append(d)
    py = last + 22
    body.append(pills(x, py, ["learn", "practice", "grow"]))
    h = py + 24 + 30
    body.insert(0, f'<rect x="{PAD}" y="36" width="3" height="{h - 72}" rx="1.5" fill="{P["accent"]}"/>')
    return shell(h, "\n".join(body),
                 "ITAAR Academy, founded by Ouahiba: a practical learning initiative to learn, practice and share useful skills.")


# --------------------------------------------------------------------------- main
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cards = {
        "01-overview.svg": card_overview(),
        "02-capabilities.svg": card_capabilities(),
        "03-project-mlops.svg": card_project(
            "End-to-End MLOps Platform",
            "Production-oriented ML platform for predicting late e-commerce deliveries.",
            ["Python", "PostgreSQL", "MLflow", "DVC", "FastAPI"],
            ["End-to-end ML lifecycle from training to deployment",
             "Model registry and champion model workflow",
             "Artifact tracking with DVC and data validation",
             "Monitoring, Docker, CI/CD, and cloud integration"],
            "End-to-End MLOps Platform: production-oriented ML platform for predicting late e-commerce deliveries.",
            hint="↗ github.com/ouahiba99/MLOPS_training"),
        "03-project-telecom.svg": card_project(
            "Telecom Network Operations Platform",
            "Engineering platform for simulating, ingesting, processing, and monitoring telecom network data.",
            ["Python", "Kafka", "PostgreSQL", "FastAPI", "Grafana"],
            ["Network KPI and alarm simulation",
             "Kafka event streaming and operational stores",
             "Real-time observability dashboards",
             "Containerized architecture for performant processing"],
            "Telecom Network Operations Platform: simulating, ingesting, processing and monitoring telecom network data."),
        "04-experience.svg": card_experience(),
        "05-academy.svg": card_academy(),
    }
    for name, svg in cards.items():
        with open(os.path.join(OUT_DIR, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {OUT_DIR}/{name}  ({len(svg) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
