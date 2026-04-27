import plotly.graph_objects as go
from .config import (DARK_LAYOUT, BLUE, GREEN, RED, YELLOW, GRAY, BG2, BG4, T1, T2, T3, BORDER)
from .helpers import fmt_brl, axis_style, pct_of

def bar_achievement(df_s, x_col, y_col, pct_col, title, fmt_fn=None, height=280):
    def bar_color(value, pct):
        if value == 0: return GRAY
        return GREEN if pct >= 100 else YELLOW if pct >= 70 else RED

    colors = [bar_color(v, p) for v, p in zip(df_s[y_col], df_s[pct_col])]
    texts = [f"<b>{fmt_fn(v)}</b><br>{p:.0f}%" if fmt_fn else f"<b>{v:.0f}</b><br>{p:.0f}%" for v, p in zip(df_s[y_col], df_s[pct_col])]

    fig = go.Figure(go.Bar(
        x=df_s[x_col], y=df_s[y_col], marker_color=colors, text=texts, textposition="outside",
        textfont=dict(color=T1, size=11), cliponaxis=False,
    ))
    fig.update_layout(**DARK_LAYOUT, height=height, title=dict(text=f"<b>{title}</b>", font=dict(color=T1, size=14)))
    return fig

def speedometer_gauge(value, max_val, label, height=260):
    """Velocímetro executivo para a Gerência."""
    color = GREEN if value >= max_val*0.75 else YELLOW if value >= max_val*0.5 else RED
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        number={"valueformat": ".1f", "font": {"size": 28, "family": "Inter", "color": T1}},
        title={"text": label, "font": {"size": 14, "family": "Inter", "color": T2}},
        gauge={
            "axis": {"range": [0, max_val], "tickwidth": 1, "tickcolor": BORDER, "tickfont": {"color": T3, "size": 11}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": BG2, "borderwidth": 0,
            "steps": [{"range": [0, max_val*0.5], "color": "#1a0f0d"}, {"range": [max_val*0.5, max_val*0.75], "color": "#1f1a08"}, {"range": [max_val*0.75, max_val], "color": "#0d1f12"}],
        },
    ))
    fig.update_layout(height=height, paper_bgcolor=BG2, font_family="Inter", margin=dict(t=40, b=8, l=24, r=24))
    return fig

def vendor_real_vs_meta(df_s, real_col, meta_col, title, is_currency=True, height=500):
    """Gráficos Real x Meta para Vendedores (Supervisor Page)."""
    df_s = df_s.copy()
    df_s["temp_pct"] = (df_s[real_col] / df_s[meta_col].replace(0, 1)) * 100
    real_colors = [GREEN if p >= 100 else YELLOW if p >= 70 else RED for p in df_s["temp_pct"]]
    texts = [fmt_brl(v) if is_currency else f"{v:.0f}" for v in df_s[real_col]]
    meta_texts = [fmt_brl(v) if is_currency else f"{v:.0f}" for v in df_s[meta_col]]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_s["vendedor"], y=df_s[meta_col], name="Meta", marker_color="#1F6FEB", text=meta_texts, textposition="outside", textfont=dict(color="#8B949E", size=13)))
    fig.add_trace(go.Bar(x=df_s["vendedor"], y=df_s[real_col], name="Realizado", marker_color=real_colors, text=texts, textposition="outside", textfont=dict(color="#E6EDF3", size=14)))
    fig.update_layout(**DARK_LAYOUT, height=height, barmode="group", title=dict(text=f"<b>{title}</b>", font=dict(color=T1, size=16)))
    return fig

def grouped_real_vs_meta(sup_g, height=450):
    """Gráficos Real x Meta para a Gerência (Visão por Supervisor). A FUNÇÃO QUE FALTAVA!"""
    sup_g = sup_g.copy()
    sup_g["temp_pct"] = (sup_g["real_mes"] / sup_g["meta_mes"].replace(0, 1)) * 100
    real_colors = [GREEN if p >= 100 else YELLOW if p >= 70 else RED for p in sup_g["temp_pct"]]
    texts = [fmt_brl(v) for v in sup_g["real_mes"]]
    meta_texts = [fmt_brl(v) for v in sup_g["meta_mes"]]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=sup_g["sup_short"], y=sup_g["meta_mes"], name="Meta", marker_color="#1F6FEB", text=meta_texts, textposition="outside", textfont=dict(color="#8B949E", size=13)))
    fig.add_trace(go.Bar(x=sup_g["sup_short"], y=sup_g["real_mes"], name="Realizado", marker_color=real_colors, text=texts, textposition="outside", textfont=dict(color="#E6EDF3", size=14)))
    fig.update_layout(**DARK_LAYOUT, height=height, barmode="group", title=dict(text="<b>Real vs Meta — Mês (Supervisores)</b>", font=dict(color=T1, size=16)))
    return fig

def hbar_pct(df_s, y_col, x_col, title, height=280):
    df_s = df_s.sort_values(x_col, ascending=True).copy()
    colors = [GRAY if v == 0 else RED if v < 70 else YELLOW if v < 100 else GREEN for v in df_s[x_col]]
    fig = go.Figure(go.Bar(x=df_s[x_col], y=df_s[y_col], orientation="h", marker_color=colors, text=[f"{v:.0f}%" for v in df_s[x_col]], textposition="outside", textfont=dict(color=T2, size=10)))
    fig.update_layout(**DARK_LAYOUT, height=height, title=dict(text=f"<b>{title}</b>", font=dict(color=T1, size=14)))
    return fig

def gauge(value, target, label, height=210):
    pct = min(pct_of(value, target), 130)
    color = GREEN if pct >= 100 else YELLOW if pct >= 70 else RED
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=pct,
        delta={"reference": 100, "valueformat": ".1f", "suffix": "%", "font": {"size": 12, "color": T2}},
        number={"suffix": "%", "font": {"size": 26, "family": "Inter", "color": T1}},
        title={"text": label, "font": {"size": 11, "family": "Inter", "color": T2}},
        gauge={"axis": {"range": [0, 120], "tickwidth": 1, "tickcolor": BORDER, "tickfont": {"color": T3, "size": 9}}, "bar": {"color": color, "thickness": 0.28}, "bgcolor": BG2, "borderwidth": 0, "steps": [{"range": [0, 70], "color": "#1a0f0d"}, {"range": [70, 100], "color": "#1f1a08"}, {"range": [100, 120], "color": "#0d1f12"}], "threshold": {"line": {"color": BLUE, "width": 2}, "thickness": 0.85, "value": 100}},
    ))
    fig.update_layout(height=height, paper_bgcolor=BG2, font_family="Inter", margin=dict(t=40, b=8, l=24, r=24))
    return fig