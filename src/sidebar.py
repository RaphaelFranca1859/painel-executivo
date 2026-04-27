"""
Sidebar — apenas logo e file uploader.
"""
import streamlit as st

def _logo_block():
    st.markdown(
        '<div style="padding:18px 16px 12px 16px;border-bottom:1px solid #21262D;">'
        '<div style="display:flex;align-items:center;gap:10px;">'
        '<div style="width:32px;height:32px;border-radius:8px;'
        'background:linear-gradient(135deg,#1F6FEB,#8B5CF6);'
        'display:flex;align-items:center;justify-content:center;font-size:16px;">⚡</div>'
        '<div>'
        '<div style="font-size:14px;font-weight:900;color:#E6EDF3;">Performance</div>'
        '<div style="font-size:10px;color:#6E7681;">MDLZ Interior P.E.</div>'
        '</div></div></div>',
        unsafe_allow_html=True,
    )

def _upload_status(df):
    if df is None:
        return
    n_fora = int(df["fora_rota"].sum())
    html = ('<div style="padding:4px 16px 8px 16px;">'
            '<div style="font-size:10px;color:#3FB950;font-weight:600;">✓ Planilha carregada</div>')
    if n_fora > 0:
        html += (f'<div style="margin-top:4px;font-size:10px;color:#F85149;font-weight:600;">'
                 f'⛔ {n_fora} fora de rota</div>')
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_sidebar(df):
    """Renderiza a sidebar simplificada e retorna o arquivo de upload."""
    with st.sidebar:
        _logo_block()
        
        st.markdown(
            '<div style="padding:10px 16px 4px 16px;">'
            '<div style="font-size:10px;font-weight:700;color:#6E7681;'
            'text-transform:uppercase;letter-spacing:0.8px;margin-bottom:6px;">📂 Planilha</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        
        uploaded = st.file_uploader("up", type=["xlsx"],
                                     label_visibility="collapsed",
                                     key="sidebar_upload")
        _upload_status(df)
        
    return uploaded