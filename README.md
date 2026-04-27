Dashboard executivo em Streamlit para monitoramento em tempo real das parciais de vendas por supervisão e gerência.

## 🚀 Como Rodar

1.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Execute a aplicação**:
    ```bash
    streamlit run app.py
    ```

## 📁 Estrutura de Pastas

- `app.py`: Orquestrador principal e navegação por abas.
- `assets/`: Arquivos estáticos (CSS e Fotos).
    - `photos/`: **IMPORTANTE** Coloque aqui as fotos dos supervisores e vendedores (nome do arquivo = nome na planilha).
- `src/`: Módulos de lógica, dados e visualização.
- `.gitignore`: Configurado para proteger sua privacidade (não sobe fotos nem planilhas).

## 🛠️ Onde modificar o quê

| Objetivo | Arquivo |
| :--- | :--- |
| Mudar cores globais | `src/config.py` |
| Ajustar regras de equipes | `src/data.py` (dicionário `TEAM_MAP`) |
| Alterar visual do pódio | `src/components.py` |
| Mudar fontes/estilos CSS | `assets/styles.css` |
| Criar novos gráficos | `src/charts.py` |

## 💡 Dicas de Uso

- **Identidade**: Para que as fotos apareçam, salve-as em `assets/photos/` com o nome exato do vendedor.
- **Navegação**: Use as abas no topo para trocar de supervisor e as abas internas para ver o Mês ou o Dia.
- **Fora de Rota**: Vendedores com Real Dia igual a 0 são automaticamente sinalizados e movidos para o final dos rankings.