import streamlit as st
from datetime import datetime
from data_processing import load_and_process_data
import altair as alt

# Configuração da página
st.set_page_config(layout='wide')

# Carregar e processar os dados
df_merged = load_and_process_data()

# Barra lateral para filtros
st.sidebar.title("Filtros")

# Caixa de seleção para gêneros na barra lateral
generos = sorted(df_merged['generos'].dropna().unique())
genero_selecionado = st.sidebar.selectbox('Selecione um gênero', generos)

# Filtro de intervalo de datas na barra lateral
data_inicio = st.sidebar.date_input('Data de início', df_merged['releaseYear'].min().date())
data_fim = st.sidebar.date_input('Data de fim', df_merged['releaseYear'].max().date())

# Filtrar dados com base no gênero selecionado e intervalo de datas
df_filtrado = df_merged[(df_merged['generos'] == genero_selecionado) & 
                        (df_merged['releaseYear'].dt.date >= data_inicio) & 
                        (df_merged['releaseYear'].dt.date <= data_fim)]

# Exibir o número total de títulos
total_titulos = df_filtrado['title'].nunique()
st.sidebar.metric("Total de Títulos", total_titulos)

# Instrução para o usuário
st.title("Bem-vindo ao Dashboard")
st.write("Use a barra lateral para aplicar filtros. Navegue para as páginas 'Visão Geral' e 'Detalhes' para visualizar os dados.")