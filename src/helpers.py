"""
Helpers — formatting, badges, avatars, scroll injection.
(Restaurado com todas as funções matemáticas + Suporte a Fotos)
"""
import hashlib
import base64
from pathlib import Path
import streamlit as st
from .config import GREEN, YELLOW, RED, AVATAR_PALETTE, GRID, BORDER, T2, T3

# ── Number formatters ────────────────────────────────────────────────
def fmt_brl(v):
    try:
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "–"

def pct_of(real, meta):
    return (real / meta * 100) if meta and meta > 0 else 0.0

# ── Achievement-based UI helpers ─────────────────────────────────────
def badge(pct):
    if pct >= 100: return f'<span class="badge-ok">✓ {pct:.0f}%</span>'
    if pct >= 70:  return f'<span class="badge-warn">⚡ {pct:.0f}%</span>'
    return f'<span class="badge-bad">✗ {pct:.0f}%</span>'

def card_class(pct):
    if pct >= 100: return "green"
    if pct >= 70:  return "yellow"
    return "red"

def row_bg(pct):
    if pct >= 100: return "#0d1f12", GREEN
    if pct >= 70:  return "#1f1a08", YELLOW
    return "#1a0f0d", RED

# ── Plotly axis helper ────────────────────────────────────────────────
def axis_style(tick_color=None, tick_size=10, rng=None):
    d = dict(
        gridcolor=GRID, linecolor=BORDER,
        tickfont=dict(color=tick_color or T2, size=tick_size, family="Inter"),
        title_font=dict(color=T3),
    )
    if rng:
        d["range"] = rng
    return d

# ── Avatar generator (AGORA COM SUPORTE A FOTOS) ──────────────────────
def avatar_html(name, size=36, is_executive_header=False):
    """Return colored circle <div> with initials OR load photo from assets/photos/."""
    base_dir = Path(__file__).parent.parent
    photo_dirs = [
        base_dir / "assets" / "photos" / f"{name}.png",
        base_dir / "assets" / "photos" / f"{name}.jpg",
        base_dir / "assets" / "photos" / f"{name}.jpeg",
        base_dir / "assets" / "photos" / f"{name.lower()}.png",
    ]
    
    found_photo = next((p for p in photo_dirs if p.exists()), None)
    
    if found_photo:
        try:
            with open(found_photo, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            mime_type = "image/png" if found_photo.suffix == ".png" else "image/jpeg"
            
            # Se for o cabeçalho executivo, coloca uma borda mais bonita
            extra_style = "border: 3px solid #161B22; box-shadow: 0 4px 12px rgba(0,0,0,0.5);" if is_executive_header else ""
            
            return f'<img src="data:{mime_type};base64,{encoded_string}" style="width:{size}px;height:{size}px;border-radius:50%;object-fit:cover;flex-shrink:0;{extra_style}" />'
        except Exception:
            pass # Se der erro na leitura, cai pro fallback de iniciais

    # Fallback: Iniciais coloridas
    parts = str(name).strip().split()
    initials = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper() if parts else "??"
    color = AVATAR_PALETTE[abs(hash(name)) % len(AVATAR_PALETTE)]
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{color};'
        f'display:flex;align-items:center;justify-content:center;font-weight:800;'
        f'font-size:{int(size*0.37)}px;color:#fff;flex-shrink:0;">{initials}</div>'
    )

# ── Scroll/anchor utilities ────────────────────────────────────────────
def anchor(anchor_id):
    st.markdown(f'<div id="{anchor_id}" class="scroll-anchor"></div>', unsafe_allow_html=True)

def scroll_to(anchor_id):
    st.markdown(
        f'<script>(function(){{var e=window.parent.document.getElementById("{anchor_id}");'
        f'if(e)e.scrollIntoView({{behavior:"smooth",block:"start"}});}})();</script>',
        unsafe_allow_html=True,
    )