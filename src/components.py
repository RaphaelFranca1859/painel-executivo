import streamlit as st
from .helpers import badge, avatar_html, fmt_brl, row_bg
from .config import RED, GREEN

try:
    from src.config import DANGER_COLOR
except ImportError:
    DANGER_COLOR = "#DA3633"

def _team_badge(equipe):
    """Retorna uma tag HTML baseada no nome da equipe."""
    if not equipe: return ""
    color = "#1F6FEB" if "express" in equipe.lower() else "#8B5CF6"
    return f'<span style="background:{color}33; color:{color}; border: 1px solid {color}55; padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; font-weight: 800; text-transform: uppercase; margin-left: 8px;">{equipe}</span>'

def kpi_card(label, value, sub, badge_pct=None, color="blue", value_color=None):
    vc  = f'style="color:{value_color};"' if value_color else ""
    bdg = badge(badge_pct) if badge_pct is not None else ""
    st.markdown(f'<div class="kpi-card {color}"><div class="kpi-label">{label}</div><div class="kpi-value" {vc}>{value}</div><div class="kpi-sub">{sub}</div><div style="margin-top:7px;">{bdg}</div></div>', unsafe_allow_html=True)

def supervisor_card(row, mode="mes"):
    """Card de resumo para a visão de gerência."""
    from .helpers import card_class
    if mode == "mes":
        pct = row["pct_mes"]; big_value = fmt_brl(row["real_mes"]); gap = row["gap_mes"]
        meta_label = f"Meta {fmt_brl(row['meta_mes'])}"
        sub_line   = f'Dia: {fmt_brl(row["real_dia"])} {badge(row["pct_dia"])}'
    else:
        pct = row["pct_dia"]; big_value = fmt_brl(row["real_dia"]); gap = row["gap_dia"]
        meta_label = f"Meta {fmt_brl(row['meta_dia'])}"; sub_line = ""

    gc = card_class(pct); gap_clr = RED if gap > 0 else GREEN
    fora_blk = (f'<div class="kpi-sub" style="color:#F85149;margin-top:4px;">⛔ {int(row["n_fora"])} fora de rota</div>' if row["n_fora"] > 0 else "")

    html = (
        f'<div class="sup-card {gc}">'
        f'<div class="kpi-label">{row["sup_short"]}</div>'
        f'<div class="kpi-value" style="font-size:16px;">{big_value}</div>'
        f'<div style="margin:4px 0;">{badge(pct)}</div>'
        f'<div class="kpi-sub">{int(row["n_vend"])} vendedores</div>'
        f'<div class="kpi-sub">{meta_label}</div>'
    )
    if sub_line: html += f'<div class="kpi-sub">{sub_line}</div>'
    html += f'<div class="kpi-sub">Gap: <span style="color:{gap_clr}">{fmt_brl(gap)}</span></div>{fora_blk}</div>'
    st.markdown(html, unsafe_allow_html=True)

def page_header(icon, title, subtitle, is_supervisor=False, sup_name=None):
    icon_html = avatar_html(sup_name, size=64, is_executive_header=True) if is_supervisor and sup_name else f'<div class="brand-icon">{icon}</div>'
    st.markdown(f'<div class="main-header"><div class="brand-area" style="gap:16px;">{icon_html}<div><div class="brand-title" style="font-size:24px;">{title}</div><div class="brand-sub" style="font-size:13px;">{subtitle}</div></div></div></div>', unsafe_allow_html=True)

def section_header(label):
    st.markdown(f"<div class='sec-hdr'>{label}</div>", unsafe_allow_html=True)

def divider():
    st.markdown('<div class="divhr"></div>', unsafe_allow_html=True)

def fora_rota_banner(df_sup):
    n_fora = int(df_sup["fora_rota"].sum())
    if n_fora == 0: return
    fnames = ", ".join(df_sup[df_sup["fora_rota"]]["vendedor"].tolist())
    plural = "es" if n_fora > 1 else ""
    st.markdown(
        '<div style="background:#1a0f0d;border:1px solid #3d0f0d;border-radius:8px;'
        'padding:10px 14px;margin:10px 0;display:flex;align-items:center;gap:10px;">'
        '<span style="font-size:18px;">⛔</span>'
        f'<div><div style="font-size:12px;font-weight:700;color:#F85149;">'
        f'{n_fora} vendedor{plural} fora de rota hoje</div>'
        f'<div style="font-size:11px;color:#6E7681;margin-top:2px;">{fnames}</div></div></div>',
        unsafe_allow_html=True
    )

def ranking_row(row, rank_idx, mode="dia", show_supervisor=False, off_route=False):
    medals = ["🥇", "🥈", "🥉"] + [f"{i+1}°" for i in range(3, 50)]
    equipe_html = _team_badge(row.get("equipe", ""))

    if off_route:
        st.markdown(
            '<div class="rank-row" style="opacity:0.45;border-style:dashed;">'
            f'{avatar_html(row["vendedor"], 36)}'
            '<div style="min-width:22px;font-size:14px;text-align:center;">–</div>'
            f'<div style="flex:1;"><div style="font-weight:700;color:#6E7681;font-size:13px;">{row["vendedor"]}{equipe_html}</div>'
            '<div style="font-size:10px;color:#F85149;font-weight:700;">⛔ FORA DE ROTA</div></div>'
            '<div style="text-align:right;"><div style="font-weight:700;color:#6E7681;font-size:14px;">0%</div>'
            '<div style="font-size:11px;color:#6E7681;">R$ 0,00</div></div></div>',
            unsafe_allow_html=True
        )
        return
        
    pct = row["pct_dia"] if mode == "dia" else row["pct_mes"]
    val = row["real_dia"] if mode == "dia" else row["real_mes"]
    bg, clr = row_bg(pct); medal = medals[rank_idx] if rank_idx < len(medals) else ""
    sub_txt = row["supervisor"].split("-")[-1].strip() if show_supervisor else (f"Pos: {int(row['real_pos_dia'])}/{int(row['meta_pos_dia'])}" if mode == "dia" else "")

    st.markdown(
        f'<div class="rank-row" style="background:{bg};border-color:{clr}33;">'
        f'{avatar_html(row["vendedor"], 36)}'
        f'<span style="font-size:16px;min-width:24px;text-align:center;">{medal}</span>'
        f'<div style="flex:1;"><div style="font-weight:800;color:#E6EDF3;font-size:13px;">{row["vendedor"]}{equipe_html}</div>'
        f'<div style="font-size:10px;color:#6E7681;">{sub_txt}</div></div>'
        f'<div style="text-align:right;"><div style="font-weight:900;color:{clr};font-size:16px;">{pct:.0f}%</div>'
        f'<div style="font-size:11px;color:#6E7681;">{fmt_brl(val)}</div></div></div>',
        unsafe_allow_html=True
    )

def render_podium(df_top3):
    """Pódio com valor em verde destaque e porcentagem em cinza."""
    if len(df_top3) == 0: return
    cols = st.columns(min(len(df_top3), 3))
    medals = [("🥇", "#D29922"), ("🥈", "#C9D1D9"), ("🥉", "#b08d57")]
    
    for i in range(len(cols)):
        row = df_top3.iloc[i]
        medal_emoji, medal_color = medals[i]
        pct = row["pct_dia"]
        equipe_html = _team_badge(row.get("equipe", ""))
        
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px 10px; background: #161B22; border: 1px solid #30363D; border-radius: 12px; border-top: 5px solid {medal_color}; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                <div style="font-size: 28px; margin-bottom: 10px; margin-top: -10px;">{medal_emoji}</div>
                <div style="display: flex; justify-content: center; margin-bottom: 15px;">
                    {avatar_html(row["vendedor"], size=80)}
                </div>
                <div style="font-weight: 900; color: #E6EDF3; font-size: 15px; margin-bottom: 5px;">{row["vendedor"]}</div>
                <div style="margin-bottom: 12px;">{equipe_html}</div>
                <div style="font-size: 24px; font-weight: 900; color: #3FB950;">{fmt_brl(row["real_dia"])}</div>
                <div style="font-size: 14px; color: #8B949E; font-weight: 600;">{pct:.1f}% atingido</div>
            </div>
            """, unsafe_allow_html=True)