# CONTEXT.md — Estado do Projeto

> **Para o assistente de IA:** este arquivo é o ponto de retomada da conversa. Leia primeiro antes de qualquer modificação. Atualize ao final de cada sessão de trabalho.

---

## 📋 Resumo do projeto

**Nome:** Central de Performance
**Cliente:** MDLZ Interior P.E. (Mondelez — distribuidor regional Bahia/PE)
**Objetivo:** dashboard Streamlit que recebe planilha `.xlsx` de parciais de vendas (atualizada de hora em hora) e gera visualizações executivas para mandar nos grupos do WhatsApp dos vendedores e gerência.

**Usuário principal:** o próprio dono da conversa, que atua na operação comercial e precisa publicar parciais visuais a cada hora.

---

## 🗂️ Arquitetura atual

Refatorado em 27/04/2026 de monolito (`dashboard_vendas.py`, ~800 linhas) para estrutura modular:

```
app.py                          → entry point (60 linhas)
assets/styles.css               → todo o CSS dark mode
src/config.py                   → cores, paleta, layout Plotly base
src/helpers.py                  → fmt_brl, badge, avatar, scroll, axis_style
src/data.py                     → load_data + aggregate_by_supervisor
src/charts.py                   → 6 funções de gráfico Plotly
src/components.py               → kpi_card, supervisor_card, page_header,
                                  ranking_row, section_header, divider, fora_rota_banner
src/sidebar.py                  → render_sidebar
src/page_gerencia.py            → render_gerencia (sub-abas Mês/Dia)
src/page_supervisor.py          → render_supervisor (sub-abas Mês/Dia)
```

---

## ✅ Funcionalidades implementadas

- [x] Upload de planilha `.xlsx` na sidebar
- [x] Cache via `st.session_state["df_cache"]` — não perde dados ao trocar de aba
- [x] Página **Gerência** com sub-abas Mês/Dia
- [x] Página **por Supervisor** (uma para cada supervisão única) com sub-abas Mês/Dia
- [x] Dark mode completo (paleta GitHub Dark)
- [x] Fora de Rota: detecção (`real_dia == 0`), banner, tabelas, ranking, gráficos cinza
- [x] Avatares circulares com iniciais (cor determinística por hash do nome)
- [x] Ranking com medalhas 🥇🥈🥉
- [x] Gauges de atingimento Mês/Dia/Positivação
- [x] Bar charts coloridos por % atingimento (verde/amarelo/vermelho)
- [x] Tabelas executivas separadas por dia/mês
- [x] Sidebar de navegação com botões de seção (scroll suave via JS injection)
- [x] Cards KPI com altura uniforme (`height: 120px`)

---

## 🐛 Bugs conhecidos / Histórico recente

1. **[FIXED 27/04]** `textposition="outside"` aplicado em `go.Scatter` causava `ValueError`. Solução: textposition agora é setado por trace, não via `update_traces`.
2. **[FIXED 27/04]** `DARK_LAYOUT` continha `xaxis`/`yaxis` que conflitavam com overrides per-chart. Solução: removidos do dict base; criada função `axis_style()` em helpers.
3. **[FIXED 27/04]** `</div>` aparecendo como texto nos cards de supervisão. Causa: HTML com tags desbalanceadas dentro de f-string. Solução: classe CSS `sup-card` separada + concatenação string-segura.
4. **[FIXED 27/04]** Sidebar sumindo após colapso. Causa: `header { display:none }` escondia o botão hamburguer. Solução: header continua visível com `background: #0D1117`.
5. **[FIXED 27/04]** Min/max-width fixo na sidebar travava o collapse. Removidos.

---

## 📐 Convenções e decisões técnicas

- **Colunas internas** (snake_case): mapeamento em `src/data.py::COLUMN_MAP`
- **Cores**: tudo em `src/config.py` — proibido hardcode em arquivos de view
- **Linguagem**: UI em **PT-BR**, comentários de código em **inglês**
- **Persistência**: nenhuma — dados ficam apenas em `st.session_state`
- **Cache**: `@st.cache_data` em `load_data` (invalida quando o usuário sobe nova planilha)
- **Navegação**: state machine simples via `st.session_state["page"]` = `"gerencia"` ou nome do supervisor

---

## 🔮 TODO / Possíveis melhorias futuras

- [ ] Auto-refresh com `st.rerun()` programado (pra reler planilha a cada X minutos)
- [ ] Botão "Exportar parcial pro WhatsApp" (gera imagem PNG da aba)
- [ ] Histórico de parciais (banco SQLite local)
- [ ] Comparativo dia atual vs dia anterior
- [ ] Mapa de calor por hora (quem vendeu quando)
- [ ] Notificação Telegram/WhatsApp quando supervisor atinge meta
- [ ] Modo "TV mode" (tela cheia rotativa entre supervisões para projetor)

---

## 🧠 Preferências do usuário (observadas na conversa)

- Pediu **dark mode moderno**, "como sistema de verdade"
- Pediu **separação de CSS** em arquivo próprio
- Quer **navegação lateral** com botões clicáveis para scroll
- Pediu **cards uniformes** (mesmo tamanho)
- Detesta **linha de meta confusa** em gráficos — preferiu cores nas barras
- Gosta de **avatares circulares** no ranking
- Pediu identificação clara de **Fora de Rota** para vendedores zerados
- Estilo de feedback: direto, técnico, sem rodeios

---

## 📝 Como retomar a conversa

Em uma nova sessão, o assistente deve:

1. **Ler este arquivo** completo
2. **Ler `README.md`** para entender o que cada arquivo faz
3. **Antes de modificar**, verificar a tabela "Onde modificar o quê" no README
4. **Após modificações**, atualizar este `CONTEXT.md`:
   - Adicionar entrada em **Bugs conhecidos** com a tag `[FIXED <data>]`
   - Atualizar lista de **Funcionalidades implementadas**
   - Mover items concluídos do TODO

---

## 🗓️ Log de sessões

### 27/04/2026 — Sessão inicial
- Criação do dashboard inicial (monolito)
- Adição de dark mode
- Bug fixes em Plotly (scatter textposition, DARK_LAYOUT axis conflicts)
- Adição de sub-abas Mês/Dia, avatares no ranking
- Identificação de fora de rota
- Sidebar com navegação e scroll JS
- **Refatoração final**: monolito → estrutura modular `app.py` + `src/` + `assets/`
