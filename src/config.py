"""
Constants — colors, plotly base layout, palette.
Edit this file when you want to change the visual identity globally.
"""

# ── Background tones ──
BG1 = "#0D1117"   # page background
BG2 = "#161B22"   # card/panel background
BG3 = "#1C2128"   # hover/secondary
BG4 = "#21262D"   # borders/separators

# ── Brand colors ──
BLUE   = "#1F6FEB"
CYAN   = "#39D3F2"
GREEN  = "#3FB950"
RED    = "#F85149"
YELLOW = "#D29922"
PURPLE = "#8B5CF6"
GRAY   = "#484F58"

# ── Typography ──
T1 = "#E6EDF3"   # primary text
T2 = "#8B949E"   # secondary
T3 = "#6E7681"   # tertiary/muted

# ── Borders ──
GRID   = "#21262D"
BORDER = "#30363D"

# ── Avatar palette (deterministic by hash) ──
AVATAR_PALETTE = [
    "#1F6FEB", "#8B5CF6", "#3FB950", "#D29922", "#F85149",
    "#39D3F2", "#F78166", "#58A6FF", "#BC8CFF", "#56D364",
]

# ── Plotly base dark layout (no axes, no height — set per chart) ──
DARK_LAYOUT = dict(
    paper_bgcolor=BG2,
    plot_bgcolor=BG2,
    font=dict(family="Inter", color=T2, size=11),
    margin=dict(t=44, b=16, l=16, r=16),
    title_font=dict(color=T1, size=13, family="Inter"),
    hoverlabel=dict(bgcolor=BG3, bordercolor=BORDER, font=dict(color=T1)),
)

# ── Threshold rules (used across charts and badges) ──
THRESHOLDS = {
    "achievement_great": 100,
    "achievement_ok":    70,
    "sku_great": 12,
    "sku_ok":    8,
}
