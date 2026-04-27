import streamlit as st
from .data import aggregate_by_supervisor
from .helpers import fmt_brl, pct_of, card_class
from .components import (kpi_card, supervisor_card, page_header, section_header, divider, ranking_row)
from .charts import gauge, hbar_pct, grouped_real_vs_meta, speedometer_gauge
from .config import RED, GREEN

def _tab_mes_consolidado(df, sup_g):
    section_header("📊 KPIs do Mês — Consolidado")
    real_mes = df["real_mes"].sum(); meta_mes = df["meta_mes"].sum()
    pct_mes = pct_of(real_mes, meta_mes)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi_card("Realizado Mês", fmt_brl(real_mes), f"Meta {fmt_brl(meta_mes)}", pct_mes, card_class(pct_mes))
    with c2: kpi_card("Gap Mês", fmt_brl(meta_mes - real_mes), f"{pct_mes:.1f}% atingido", color="red" if meta_mes > real_mes else "green", value_color=RED if meta_mes > real_mes else GREEN)
    with c3: kpi_card("Positivação Mês", f"{int(df['real_pos_mes'].sum())}/{int(df['meta_pos_mes'].sum())}", "PDVs positivados", pct_of(df['real_pos_mes'].sum(), df['meta_pos_mes'].sum()), "purple")
    with c4: kpi_card("SKU / PDV Médio", f"{df['sku_pdv'].mean():.1f}", f"Ticket {fmt_brl(df['ticket_medio'].mean())}", color="blue")
    with c5: kpi_card("Fora de Rota", str(int(df["fora_rota"].sum())), "vendedores hoje", color="red" if df["fora_rota"].sum() > 0 else "green", value_color=RED if df["fora_rota"].sum() > 0 else GREEN)

    divider()
    g1, g2, g3 = st.columns(3)
    with g1: st.plotly_chart(gauge(real_mes, meta_mes, "Atingimento Mês"), use_container_width=True, config={"displayModeBar": False})
    with g2: st.plotly_chart(gauge(df["real_dia"].sum(), df["meta_dia"].sum(), "Desempenho Dia"), use_container_width=True, config={"displayModeBar": False})
    with g3: st.plotly_chart(gauge(df['real_pos_mes'].sum(), df['meta_pos_mes'].sum(), "Positivação Mês"), use_container_width=True, config={"displayModeBar": False})

    divider()
    section_header("📍 Resultado por Supervisão — Mês")
    cols = st.columns(len(sup_g))
    for i, (_, row) in enumerate(sup_g.iterrows()):
        with cols[i]: supervisor_card(row, mode="mes")

    divider()
    section_header("📈 Gráficos do Mês — Realizado vs Meta (Supervisões)")
    st.plotly_chart(grouped_real_vs_meta(sup_g), use_container_width=True, config={"displayModeBar": False})

    divider()
    section_header("📋 Tabela Consolidada por Supervisão")
    tbl = sup_g[["sup_short", "n_vend", "n_fora", "real_mes", "meta_mes", "pct_mes", "sku_pdv", "ticket_medio", "gap_mes"]].sort_values("pct_mes", ascending=False).copy().reset_index(drop=True)
    tbl.index += 1
    tbl.columns = ["Supervisor", "Vendedores", "F.Rota", "Real Mês", "Meta Mês", "% Mês", "SKU/PDV", "Ticket Médio", "Gap Mês"]
    for c in ["Real Mês", "Meta Mês", "Ticket Médio", "Gap Mês"]: tbl[c] = tbl[c].apply(fmt_brl)
    tbl["% Mês"] = tbl["% Mês"].apply(lambda v: f"{v:.1f}%")
    tbl["SKU/PDV"] = tbl["SKU/PDV"].apply(lambda v: f"{v:.1f}")
    st.dataframe(tbl, use_container_width=True)

def _tab_dia_consolidado(df, sup_g):
    section_header("☀️ KPIs do Dia — Consolidado")
    real_dia = df["real_dia"].sum(); meta_dia = df["meta_dia"].sum()
    pct_dia = pct_of(real_dia, meta_dia)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi_card("Desempenho Dia", fmt_brl(real_dia), f"Meta {fmt_brl(meta_dia)}", pct_dia, card_class(pct_dia))
    with c2: kpi_card("Gap do Dia", fmt_brl(meta_dia - real_dia), f"{pct_dia:.1f}% atingido", color="red" if meta_dia > real_dia else "green", value_color=RED if meta_dia > real_dia else GREEN)
    with c3: kpi_card("Positivação Dia", f"{int(df['real_pos_dia'].sum())}/{int(df['meta_pos_dia'].sum())}", "PDVs visitados", pct_of(df['real_pos_dia'].sum(), df['meta_pos_dia'].sum()), "purple")
    with c4: kpi_card("Em Rota", str(len(df) - int(df["fora_rota"].sum())), "vendedores ativos", color="green")
    with c5: kpi_card("Fora de Rota", str(int(df["fora_rota"].sum())), "sem faturamento", color="red" if df["fora_rota"].sum() > 0 else "green", value_color=RED if df["fora_rota"].sum() > 0 else GREEN)

    divider()
    section_header("🏆 Top Vendedores e Velocidade")
    t1, t2 = st.columns([2, 1])
    with t1:
        top5 = df[~df["fora_rota"]].sort_values("pct_dia", ascending=False).head(5)
        for i, row in top5.reset_index(drop=True).iterrows(): ranking_row(row, i, mode="dia", show_supervisor=True)
    with t2:
        st.plotly_chart(speedometer_gauge(df["sku_pdv"].mean(), max_val=15.0, label="Velocidade: SKU / PDV Médio"), use_container_width=True, config={"displayModeBar": False})

def render_gerencia(df):
    page_header("🏢", "Visão Gerencial", "Consolidado")
    sup_g = aggregate_by_supervisor(df)
    tab_m, tab_d = st.tabs(["Desempenho Mês", "Desempenho Dia"])
    with tab_m: _tab_mes_consolidado(df, sup_g)
    with tab_d: _tab_dia_consolidado(df, sup_g)