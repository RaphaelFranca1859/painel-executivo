"""
Data loading and transformation.
"""
import pandas as pd
import streamlit as st
from .helpers import pct_of

COLUMN_MAP = {
    "CÓD. SUP":      "cod_sup",
    "SUP":           "supervisor",
    "COD RCA":       "cod_rca",
    "RCA":           "rca_full",
    "TELEFONE":      "telefone",
    "RCA NOME":      "vendedor",
    "Meta mês":      "meta_mes",
    "Meta dia":      "meta_dia",
    "Real dia":      "real_dia",
    "Real MÊS":      "real_mes",
    "Gap Mês":       "gap_mes",
    "Meta Pos. mês": "meta_pos_mes",
    "Real Pos. mês": "real_pos_mes",
    "GAP Pos mês":   "gap_pos_mes",
    "Meta pos. dia": "meta_pos_dia",
    "Real Pos. dia": "real_pos_dia",
    "SKU/PDV":       "sku_pdv",
    "Ticket médio":  "ticket_medio",
}

NUMERIC_COLS = [
    "meta_mes", "meta_dia", "real_dia", "real_mes", "gap_mes",
    "meta_pos_mes", "real_pos_mes", "gap_pos_mes",
    "meta_pos_dia", "real_pos_dia", "sku_pdv", "ticket_medio",
]

@st.cache_data(show_spinner=False)
def load_data(file_bytes):
    df = pd.read_excel(file_bytes, engine="openpyxl")
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns})

    df["supervisor"] = df["supervisor"].astype(str).str.strip()
    df["vendedor"]   = df["vendedor"].astype(str).str.strip()

    for c in NUMERIC_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # ── MAPEAMENTO DE EQUIPES POR CÓDIGO SUP ──
    if "cod_sup" in df.columns:
        # Pega apenas o número (evita decimais do Pandas)
        df["cod_sup_str"] = df["cod_sup"].astype(str).str.split('.').str[0]
        
        # EDITE AQUI OS SEUS CÓDIGOS REAIS!
        TEAM_MAP = {
            "19": "Pronta Entrega",
            "126": "Express",
            # Exemplo para o Eduardo (substitua pelos códigos corretos dele):
            "21": "Pronta Entrega", 
            "127": "Express"
        }
        df["equipe"] = df["cod_sup_str"].map(TEAM_MAP).fillna("")
    else:
        df["equipe"] = ""

    df["pct_mes"]   = df.apply(lambda r: pct_of(r["real_mes"], r["meta_mes"]), axis=1)
    df["pct_dia"]   = df.apply(lambda r: pct_of(r["real_dia"], r["meta_dia"]), axis=1)
    df["pct_pos_m"] = df.apply(lambda r: pct_of(r["real_pos_mes"], r["meta_pos_mes"]), axis=1)
    df["fora_rota"] = df["real_dia"] == 0

    return df

def aggregate_by_supervisor(df):
    sup_g = df.groupby("supervisor").agg(
        real_mes     = ("real_mes",     "sum"),
        meta_mes     = ("meta_mes",     "sum"),
        real_dia     = ("real_dia",     "sum"),
        meta_dia     = ("meta_dia",     "sum"),
        real_pos_mes = ("real_pos_mes", "sum"),
        meta_pos_mes = ("meta_pos_mes", "sum"),
        sku_pdv      = ("sku_pdv",      "mean"),
        ticket_medio = ("ticket_medio", "mean"),
        n_vend       = ("vendedor",     "count"),
        n_fora       = ("fora_rota",    "sum"),
    ).reset_index()

    sup_g["pct_mes"]   = sup_g.apply(lambda r: pct_of(r["real_mes"], r["meta_mes"]), axis=1)
    sup_g["pct_dia"]   = sup_g.apply(lambda r: pct_of(r["real_dia"], r["meta_dia"]), axis=1)
    sup_g["gap_mes"]   = sup_g["meta_mes"] - sup_g["real_mes"]
    sup_g["gap_dia"]   = sup_g["meta_dia"] - sup_g["real_dia"]
    sup_g["sup_short"] = sup_g["supervisor"].str.extract(r"- (.+)$").fillna(sup_g["supervisor"])

    return sup_g