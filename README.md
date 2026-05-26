# 📊 Dashboard de Vendas — Streamlit

Dashboard interativo para análise de desempenho de vendas por vendedor e período, desenvolvido com Python e Streamlit.

---

## 💡 Inspiração

Projeto inspirado em um exercício do curso de Power BI da 
[Hashtag Treinamentos](https://www.hashtagtreinamentos.com/), 
reimplementado com Python e Streamlit.

Base de dados disponibilizada pela Hashtag Treinamentos para fins educacionais.

---
## 🖥️ Demonstração | [Ir para o Dashboard](https://dashappvendas-z8lua9fznmmx4j5zugh7x6.streamlit.app/)

<img src="https://github.com/DiegoFrancoGiusti/DiegoFrancoGiusti/blob/main/BannerLikedin2.png">

---

## 🚀 Funcionalidades

- Filtros dinâmicos por **vendedor** e **período**
- Indicadores de **faturamento**, **lucro**, **quantidade vendida** e **produto mais vendido**
- Destaque visual do **Top 1 Vendedor** com foto
- Gráfico de **faturamento e quantidade vendida por mês** (barras + linha com eixo duplo)
- Gráfico de **faturamento por vendedor** (ranking horizontal)
- Gráfico de **quantidade vendida por forma de pagamento** (pizza)

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| Pandas | Manipulação e análise de dados |
| Streamlit | Interface web interativa |
| Plotly | Visualizações gráficas |
| OpenPyXL | Leitura de arquivos Excel |

---

## ⚙️ Como executar localmente

**Pré-requisitos:** Python 3.8+

1. Clone o repositório
```bash
git clone https://github.com/DiegoFrancoGiusti/DashStreamlit_Vendas.git
cd dashboard-vendas
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Adicione o arquivo `Vendas Equipe.xlsx` na raiz do projeto

4. Execute o dashboard
```bash
streamlit run app.py
```

---

## 📚 Aprendizados

- Uso de `@st.cache_data` para otimizar a leitura de dados e evitar reprocessamentos desnecessários
- Aplicação do princípio **DRY** com uma função de filtragem centralizada (`filtrar_base`)
- Construção de gráficos combinados com eixo duplo no Plotly
- Estruturação de layouts responsivos com colunas no Streamlit

---

## 👤 Autor

**Diego** — [LinkedIn](https://www.linkedin.com/in/diego-franco-giusti-modesto-da-silva-b2a98a409/) · [GitHub](https://github.com/DiegoFrancoGiusti/)
