# Central de Performance — MDLZ Interior P.E.

Dashboard executivo em Streamlit para acompanhamento das parciais de vendas (de hora em hora) por supervisão e gerência.

---

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

A aplicação abre em `http://localhost:8501`.

Use o painel lateral esquerdo:
1. **📂 Planilha** — anexar `.xlsx` (formato MDLZ Interior P.E.)
2. **Navegação** — alternar entre Gerência e cada Supervisor
3. **Sub-botões** — clicar para rolar até a seção dentro da página

---

## Estrutura do projeto

```
projeto/
├── app.py                      # Entry point — apenas orquestra
├── requirements.txt
├── README.md
├── CONTEXT.md                  # Estado do projeto para retomada de conversa
├── assets/
│   └── styles.css              # Todo o CSS (dark mode)
└── src/
    ├── __init__.py
    ├── config.py               # Cores, layout Plotly, paleta
    ├── helpers.py              # fmt_brl, badge, avatar, scroll, axis_style
    ├── data.py                 # load_data, aggregate_by_supervisor
    ├── charts.py               # Fábricas de gráficos Plotly
    ├── components.py           # KPI cards, headers, ranking rows
    ├── sidebar.py              # Sidebar com nav e upload
    ├── page_gerencia.py        # Página de gerência (sub-abas Mês/Dia)
    └── page_supervisor.py      # Página por supervisor (sub-abas Mês/Dia)
```

---

## Onde modificar o quê

| Quero mudar...                          | Edite em                  |
|----------------------------------------|---------------------------|
| Cores / esquema visual                 | `src/config.py`           |
| Estilo CSS (cards, tabelas, fontes…)   | `assets/styles.css`       |
| Como a planilha é lida (colunas etc.)  | `src/data.py`             |
| Formatação de moeda, badges, avatares  | `src/helpers.py`          |
| Aparência ou tipo de um gráfico        | `src/charts.py`           |
| KPI card / header / ranking row        | `src/components.py`       |
| Botões da barra lateral / navegação    | `src/sidebar.py`          |
| Layout da aba **Gerência**             | `src/page_gerencia.py`    |
| Layout da aba **por Supervisor**       | `src/page_supervisor.py`  |
| Adicionar nova rota / página           | `app.py` + novo módulo    |

---

## Identificação de "Fora de Rota"

Vendedor com `Real dia == 0` é classificado como **Fora de Rota**:
- Aparece em cinza nos gráficos
- É exibido no final do ranking com card tracejado
- Tem badge `⛔ F.Rota` nas tabelas
- Banner vermelho aparece no topo da aba Dia
- Contador na barra lateral

---

## Convenções

- **Coluna interna** (snake_case): definida em `src/data.py` → `COLUMN_MAP`
- **Cores fixas**: SEMPRE referenciar de `config.py`, nunca hardcoded
- **Strings de UI**: em português (público é time comercial brasileiro)
- **Comentários no código**: em inglês (padrão técnico)
