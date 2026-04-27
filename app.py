"""
Central de Performance — Main entry point.
Run with: streamlit run app.py
"""
from pathlib import Path
import streamlit as st

from src.data import load_data
from src.sidebar import render_sidebar
from src.page_gerencia import render_gerencia
from src.page_supervisor import render_supervisor

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Central de Performance | MDLZ",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ──────────────────────────────────────────────────────────
def load_css():
    css_path = Path(__file__).parent / "assets" / "styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Welcome screen ────────────────────────────────────────────────────
def welcome_screen():
    st.markdown(
        '<div style="display:flex;flex-direction:column;align-items:center;'
        'justify-content:center;height:80vh;gap:16px;text-align:center;">'
        '<div style="width:72px;height:72px;border-radius:18px;'
        'background:linear-gradient(135deg,#1F6FEB,#8B5CF6);'
        'display:flex;align-items:center;justify-content:center;font-size:34px;">⚡</div>'
        '<div><div style="font-size:26px;font-weight:900;color:#E6EDF3;letter-spacing:-0.5px;">'
        'Central de Performance</div>'
        '<div style="font-size:14px;color:#6E7681;margin-top:6px;">'
        'Carregue a planilha de parciais no painel lateral para começar</div></div>'
        '<div style="background:#161B22;border:1px dashed #30363D;border-radius:12px;'
        'padding:20px 32px;margin-top:8px;">'
        '<div style="font-size:12px;color:#8B949E;">📂 Use o campo '
        '<strong style="color:#1F6FEB">Planilha</strong> na barra lateral esquerda</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

# ── Main ──────────────────────────────────────────────────────────────
def main():
    load_css()

    df = st.session_state.get("df_cache")
    supervisors = sorted(df["supervisor"].unique().tolist()) if df is not None else []

    # Renderiza apenas o upload na lateral esquerda
    uploaded = render_sidebar(df)

    if uploaded is not None:
        with st.spinner("Processando planilha…"):
            df = load_data(uploaded)
        st.session_state["df_cache"] = df
        supervisors = sorted(df["supervisor"].unique().tolist())

    if df is None:
        welcome_screen()
        return

    # ── Criação das Abas Principais no Topo ──
    # Gera a lista com "Gerência" seguida dos nomes curtos dos supervisores
    tab_titles = ["🏢 Gerência"] + [f"👤 {sup.split('-')[-1].strip()}" for sup in supervisors]
    
    # Cria as abas no Streamlit
    main_tabs = st.tabs(tab_titles)

    # Injeta o conteúdo dentro de cada aba
    with main_tabs[0]:
        render_gerencia(df)
        
    for i, sup in enumerate(supervisors):
        with main_tabs[i + 1]:
            # Passa o dataframe filtrado apenas daquele supervisor
            render_supervisor(df[df["supervisor"] == sup].copy(), sup)

if __name__ == "__main__":
    main()