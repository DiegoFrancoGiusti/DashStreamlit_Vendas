import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Importando a base de dados
@st.cache_data
def carregar_dados():
  df = pd.read_excel(r'Vendas Equipe.xlsx')
  # Separando a coluna "Vendedor" em "Vendedor" e "ID vendedor".
  df[['Vendedor','ID vendedor']] = df['Vendedor'].str.split(' - ', expand=True)
  # Criando a coluna "num mes" que vai conter o número do mês. É usada para ordenar a base de dados
  df['num mes'] = df['Data'].dt.month
  df = df.sort_values(by='num mes', ascending=True)
  df['Faturamento'] = df['Quantidade Vendida'] * df['Valor Unitario']

  return df

st.set_page_config(layout='wide')
vendas_df = carregar_dados()

# Layout da página
header= st.container()
col1,col2,col3,col4 = st.columns(4)
div1, div2 = st.columns([1,4])

st.sidebar.title('Filtros do Dashboard')
#st.dataframe(vendas_df)
vendedores = ['Todos']
meses = ['Geral']

# Substituindo os links das imagens dos vendedores
file_id = '1uf92M4d3Op0zS2eMazfGRK9oe7znTatr'
vendas_df.loc[ vendas_df['Vendedor'] == 'Diego Amorim','Imagem Vendedor'] = f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"

file_id = '1TbTvEJNJIMDbJX8ZiBJOLthcpEMmxDof'
vendas_df.loc[ vendas_df['Vendedor'] == 'Alon Pinheiro','Imagem Vendedor'] = f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"

file_id = '1_GVY_AQsTQrFc_kmc0PHSz_R1J9DCFJ4'
vendas_df.loc[ vendas_df['Vendedor'] == 'João Lira','Imagem Vendedor'] = f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"

file_id = '1L4jaM4wJ77GLP8hPK1I2CB2773ph_e5I'
vendas_df.loc[ vendas_df['Vendedor'] == 'João Martins','Imagem Vendedor'] = f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"

# Filtra a base de acordo com o filtro selecionado. Retorna a base filtrada
def filtrar_base(vendedor,periodo):
  df = vendas_df.copy()

  if vendedor != 'Todos' and periodo != 'Geral':
    df_filtrado = df[(df['Vendedor'] == vendedor) & (df['Data'].dt.month_name() == periodo)]
    return df_filtrado 
  elif vendedor == 'Todos' and periodo != 'Geral':
    df_filtrado = df[(df['Data'].dt.month_name() == periodo)]
    return df_filtrado 
  elif periodo == 'Geral' and vendedor != 'Todos':
    df_filtrado = df[(df['Vendedor'] == vendedor)]
    return df_filtrado 
  else:
    df_filtrado = df
    return df_filtrado 

# Calcular o total de faturamento
def calcular_faturamento(vendedor,periodo):
  df_filtrado = filtrar_base(vendedor,periodo)
  faturamento = sum(df_filtrado['Faturamento'])
  return f'{faturamento:,.0f}'.replace(',','.')
  
# Calcular o total de lucro
def calcular_lucro(vendedor,periodo):
  df_filtrado = filtrar_base(vendedor,periodo)
  lucro = sum(df_filtrado['Lucro'])
  return f'{lucro:,.0f}'.replace(',','.')

# Calcular o total de produtos vendidos
def calcular_total_produtos_vendidos(vendedor,periodo):
  df_filtrado = filtrar_base(vendedor,periodo)
  qtd_vendida = sum(df_filtrado['Quantidade Vendida'])
  return f'{qtd_vendida:,.0f}'.replace(',','.')

# Rankeando os produtos pela quantidade vendida. Retorna o que teve a maior quantidade vendida
def top1_produtos(df):
  ranking = df[['Produto','Quantidade Vendida']].groupby('Produto',as_index=False).sum()
  ranking = ranking.sort_values(by='Quantidade Vendida',ascending=False).reset_index(drop=True)
  return ranking.iloc[0].values

# Retorna o produto mais vendido por filtro aplicado. Utiliza o retorno da função "top1_produtos()".
def produto_mais_vendeu(vendedor,periodo):
  df_filtrado = filtrar_base(vendedor,periodo)
  produto, qtd = top1_produtos(df_filtrado)
  return f'{produto} - {qtd}'

# Calcula o faturamento total por mês. Usado no gráfico "Faturamento e Quantidade Vendida por Mês"
def faturamento_meses(vendedor,periodo):
  df_filtrado = filtrar_base(vendedor,periodo)
  faturamento_mes = df_filtrado.groupby(df_filtrado['Data'].dt.to_period('M'))['Faturamento'].sum().reset_index()
  return faturamento_mes['Faturamento']
  
# Calcula a quantidade de produtos vendidos por mês. Usado no gráfico "Faturamento e Quantidade Vendida por Mês"
def produtos_vendidos_porMes(vendedor,periodo):
  df_filtrado = filtrar_base(vendedor,periodo)
  qtd_vendido_mes = df_filtrado.groupby(df_filtrado['Data'].dt.to_period('M'))['Quantidade Vendida'].sum().reset_index()
  return qtd_vendido_mes['Quantidade Vendida']
  
  
# Calcula o faturamento por vendedor. Usado no gráfico "Faturamento por Vendedor"
def faturamento_vendedor(vendedor,periodo):
  df_filtrado = filtrar_base(vendedor,periodo)
  faturamento_vendedor = df_filtrado.groupby(df_filtrado['Vendedor'])['Faturamento'].sum().reset_index()
  faturamento_vendedor = faturamento_vendedor.sort_values(by='Faturamento', ascending=False).reset_index(drop=True)
  
  return faturamento_vendedor
  
# Calcula a quantidade de produtos vendidos por tipo de pagamento
def qtdVendida_tipoPagamento(vendedor,periodo):
  df_filtrado = filtrar_base(vendedor,periodo)
  qtd_tipoPagamento = df_filtrado.groupby(df_filtrado['Forma de Pagamento'])['Quantidade Vendida'].sum().reset_index()
  
  return qtd_tipoPagamento
  
for vendedor in vendas_df['Vendedor'].unique():
  vendedores.append(vendedor)

for mes in vendas_df['Data'].dt.month_name().unique():
  meses.append(mes)

# Adiciona os meses e os vendedores nos seus selectbox. Filtram os dashboard
periodo = st.sidebar.selectbox(label="Período:", options=meses)
vendedor = st.sidebar.selectbox(label="Vendedor:", options= vendedores )

# VISÃO GERAL

# Exibindo as medidas (Faturamento, Lucro, Quantidade Vendida, Produto mais Vendido)

with header:
  st.title('Dashboard de Vendas')
  st.subheader('Visão Geral',anchor=False)

with col1:
  st.metric(label="Faturamento", value=f"R$ {calcular_faturamento(vendedor,periodo)}", border=True)
with col2:
  st.metric(label="Lucro", value=f"R$ {calcular_lucro(vendedor,periodo)}", border=True)
with col3:
  st.metric(label="Quantidade Vendida", value=f'{calcular_total_produtos_vendidos(vendedor,periodo)}', border=True)
with col4:
  st.metric(label="Produto mais Vendido", value=f'{produto_mais_vendeu(vendedor,periodo)}', border=True)

# Exibindo o vendedor top 1
with div1:
  df_top1 = faturamento_vendedor(vendedor,periodo)
  top1_vendedor = df_top1['Vendedor'][0]
  faturamentos = df_top1['Faturamento'][0]
  indice = vendas_df[vendas_df['Vendedor'] == top1_vendedor].index[0]
  url_img = vendas_df.loc[indice,'Imagem Vendedor']
  
  st.subheader('Top 1 Vendedor',text_alignment='center',anchor=False)
  st.image(url_img, use_container_width=True)
  st.text(f'{top1_vendedor} ', width='stretch',text_alignment='center')
  st.text(f'R$ {faturamentos:,.0f}'.replace(',','.'), width='stretch',text_alignment='center')

# GRÁFICOS
with div2:
  # Gráfico de Faturamento e Quantidade Vendida por Mês (colunas e linha)
  meses_periodo = meses[1:] if periodo == 'Geral' else [periodo]

  fig = make_subplots(specs=[[{"secondary_y": True}]])
  fig.add_trace(
    go.Bar(x=meses_periodo,y=faturamento_meses(vendedor,periodo), name='Faturamento'),
    secondary_y=False,
  )

  fig.add_trace(
    go.Scatter(x=meses_periodo, y=produtos_vendidos_porMes(vendedor,periodo), name='Quantidade Vendida'),
    secondary_y=True,
  )

  fig.update_xaxes(showgrid=False)
  fig.update_yaxes(showgrid=False)
  fig.update_layout(title_text="Faturamento e Quantidade Vendida por Mês")
  st.plotly_chart(fig, use_container_width=True)

  col1,col2 = st.columns(2)

  with col1:
    # Gráfico de Faturamento por Vendedor (ranking) (Barra)
    df = faturamento_vendedor(vendedor,periodo)
    fig_rank = go.Figure()
    fig_rank.add_bar(x=df['Faturamento'],y=df['Vendedor'],orientation='h')
    fig_rank.update_layout(
      title_text="Faturamento por Vendedor",
      yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig_rank)

  with col2:
    # Gráfico de Quantidade Vendida por Tipo de Pagamento (Pizza)
    df = qtdVendida_tipoPagamento(vendedor,periodo)
    pagamentos_fig = go.Figure(
      data=[go.Pie(
        labels= df['Forma de Pagamento'],
        values= df['Quantidade Vendida']
        )]
    )

    pagamentos_fig.update_layout(
      title_text= "Quantidade Vendida por Tipo de Pagamento",
    )
    st.plotly_chart(pagamentos_fig)
