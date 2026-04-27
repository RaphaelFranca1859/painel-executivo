import streamlit as st

from .helpers import fmt_brl, pct_of, badge, card_class, anchor
from .components import (
    kpi_card, page_header, section_header, divider,
    ranking_row, fora_rota_banner, render_podium
)
from .charts import bar_achievement, gauge, hbar_pct, vendor_real_vs_meta
from .config import RED, GREEN

def _tab_mes(df_sup, sid):
    anchor(f"mes_kpi_{sid}")
    section_header("📊 KPIs do Mês")

    real_mes = df_sup["real_mes"].sum(); meta_mes = df_sup["meta_mes"].sum()
    pos_mes  = df_sup["real_pos_mes"].sum(); mpos_mes = df_sup["meta_pos_mes"].sum()
    gap_mes  = meta_mes - real_mes
    pct_mes  = pct_of(real_mes, meta_mes)
    pct_pos  = pct_of(pos_mes, mpos_mes)

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Realizado Mês", fmt_brl(real_mes), f"Meta {fmt_brl(meta_mes)}", pct_mes, card_class(pct_mes))
    with c2: kpi_card("Gap Mês", fmt_brl(gap_mes), f"{pct_mes:.1f}% atingido", color="red" if gap_mes > 0 else "green", value_color=RED if gap_mes > 0 else GREEN)
    with c3: kpi_card("Positivação Mês", f"{int(pos_mes)}/{int(mpos_mes)}", "PDVs positivados", pct_pos, "purple")
    with c4: kpi_card("SKU / PDV · Ticket", f"{df_sup['sku_pdv'].mean():.1f} SKUs", f"Ticket {fmt_brl(df_sup['ticket_medio'].mean())}", color="blue")

    divider()
    anchor(f"mes_charts_{sid}")
    section_header("📈 Gráficos do Mês — Realizado vs Meta")

    df_m = df_sup.copy()
    
    # ✨ Gráficos agora ficam um embaixo do outro usando 100% da largura ✨
    st.plotly_chart(
        vendor_real_vs_meta(df_m.sort_values("real_mes", ascending=False), "real_mes", "meta_mes", "Faturamento Mês vs Meta", is_currency=True, height=500),
        use_container_width=True, config={"displayModeBar": False}
    )
    
    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
    
    st.plotly_chart(
        vendor_real_vs_meta(df_m.sort_values("real_pos_mes", ascending=False), "real_pos_mes", "meta_pos_mes", "Positivação Mês vs Meta", is_currency=False, height=500),
        use_container_width=True, config={"displayModeBar": False}
    )

def _tab_dia(df_sup, sid):
    df_rota = df_sup[~df_sup["fora_rota"]]
    anchor(f"dia_kpi_{sid}")
    section_header("☀️ KPIs do Dia")

    real_dia = df_sup["real_dia"].sum(); meta_dia = df_sup["meta_dia"].sum()
    pos_dia  = df_sup["real_pos_dia"].sum(); mpos_dia = df_sup["meta_pos_dia"].sum()
    gap_dia  = meta_dia - real_dia
    pct_dia  = pct_of(real_dia, meta_dia)
    best     = df_rota.loc[df_rota["real_dia"].idxmax()] if len(df_rota) > 0 else None

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Desempenho Dia", fmt_brl(real_dia), f"Meta {fmt_brl(meta_dia)}", pct_dia, card_class(pct_dia))
    with c2: kpi_card("Gap do Dia", fmt_brl(gap_dia), f"{pct_dia:.1f}% atingido", color="red" if gap_dia > 0 else "green", value_color=RED if gap_dia > 0 else GREEN)
    with c3: kpi_card("Positivação Dia", f"{int(pos_dia)}/{int(mpos_dia)}", "PDVs visitados", pct_of(pos_dia, mpos_dia), "purple")
    with c4:
        if best is not None: kpi_card("Destaque", best["vendedor"], fmt_brl(best["real_dia"]), pct_of(best["real_dia"], best["meta_dia"]), "blue")
        else: kpi_card("Destaque", "–", "Nenhum em rota", color="gray")

    fora_rota_banner(df_sup)

    divider()
    anchor(f"dia_charts_{sid}")
    
    rank_em   = df_sup[~df_sup["fora_rota"]].sort_values("pct_dia", ascending=False).reset_index(drop=True)
    rank_fora = df_sup[df_sup["fora_rota"]].copy()

    section_header("🏆 Pódio do Dia")
    if len(rank_em) > 0:
        render_podium(rank_em.head(3))

    divider()
    section_header("📈 Ranking Gráfico")

    rk1, rk2 = st.columns([3, 2])
    df_d = df_sup.copy()
    df_d["pct_d"] = df_d.apply(lambda r: pct_of(r["real_dia"], r["meta_dia"]), axis=1)

    with rk1:
        for i, row in rank_em.iterrows():
            ranking_row(row, i, mode="dia")
        for _, row in rank_fora.iterrows():
            ranking_row(row, 0, mode="dia", off_route=True)
    with rk2:
        st.plotly_chart(
            hbar_pct(df_d, "vendedor", "pct_d", "% Desempenho do Dia", height=max(len(df_sup) * 46 + 60, 300)),
            use_container_width=True, config={"displayModeBar": False},
        )

    # ✨ TABELA RESTAURADA AQUI ✨
    divider()
    section_header("📋 Tabela — Desempenho do Dia")

    df_d_tbl = df_sup.copy()
    df_d_tbl["pct_pos_d"] = df_d_tbl.apply(lambda r: pct_of(r["real_pos_dia"], r["meta_pos_dia"]), axis=1)
    
    tbl_d = df_d_tbl[["vendedor", "fora_rota", "meta_dia", "real_dia", "pct_dia", "meta_pos_dia", "real_pos_dia", "pct_pos_d", "ticket_medio"]].sort_values(["fora_rota", "pct_dia"], ascending=[True, False]).copy().reset_index(drop=True)
    tbl_d.index += 1
    tbl_d["Status"] = tbl_d["fora_rota"].apply(lambda v: "⛔ F.Rota" if v else "✓ Em Rota")
    tbl_d = tbl_d.drop(columns=["fora_rota"])
    tbl_d.columns = ["Vendedor", "Meta Dia", "Real Dia", "% Dia", "Meta Pos.", "Real Pos.", "% Pos.", "Ticket Médio", "Status"]
    
    for c in ["Meta Dia", "Real Dia", "Ticket Médio"]: tbl_d[c] = tbl_d[c].apply(fmt_brl)
    for c in ["% Dia", "% Pos."]: tbl_d[c] = tbl_d[c].apply(lambda v: f"{v:.1f}%")
    tbl_d = tbl_d[["Status", "Vendedor", "Meta Dia", "Real Dia", "% Dia", "Meta Pos.", "Real Pos.", "% Pos.", "Ticket Médio"]]
    
    st.dataframe(tbl_d, use_container_width=True, height=min(56 + len(tbl_d) * 38, 600))


def render_supervisor(df_sup, sup_name):
    short    = sup_name.split("-")[-1].strip() if "-" in sup_name else sup_name
    n_fora   = int(df_sup["fora_rota"].sum())
    n_em     = len(df_sup) - n_fora
    fora_part = (f' · <span style="color:#F85149;font-weight:700;">{n_fora} fora de rota</span>' if n_fora else "")
    
    page_header("👤", short, f"{sup_name} · {n_em} em rota{fora_part}", is_supervisor=True, sup_name=sup_name)

    # ✨ Abas renomeadas ✨
    tab_m, tab_d = st.tabs(["Desempenho Mês", "Desempenho Dia"])
    with tab_m: _tab_mes(df_sup, sid="")
    with tab_d: _tab_dia(df_sup, sid="")