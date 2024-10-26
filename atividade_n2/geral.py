import streamlit as st
from datetime import datetime
from data_processing import load_and_process_data
from visualization import create_charts
import altair as alt

# Configuração da página
st.set_page_config(layout='wide')

# Carregar e processar os dados
df_merged = load_and_process_data()

# Barra lateral para navegação e filtros
st.sidebar.title("Navegação")

# Remover o radio
# pagina = st.sidebar.radio("Ir para", ["Visão Geral", "Detalhes"])

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

# Remover títulos duplicados
df_filtrado = df_filtrado.drop_duplicates(subset='title')

# Exibir o número total de títulos
total_titulos = df_filtrado['title'].nunique()
st.sidebar.metric("Total de Títulos", total_titulos)

# Exibir a seção "Visão Geral"
st.title("Página de Visão Geral")

# Criar gráficos
charts = create_charts(df_filtrado)

# Criar duas colunas para a primeira linha
col1, col2 = st.columns(2)
col1.altair_chart(charts['release_year'], use_container_width=True)
col2.altair_chart(charts['country'], use_container_width=True)

# Criar três colunas para a segunda linha
col3, col4, col5 = st.columns(3)
col3.altair_chart(charts['type'], use_container_width=True)
col4.altair_chart(charts['year_line'], use_container_width=True)
col5.altair_chart(charts['available_countries'], use_container_width=True)

# Adicionar elementos de top 3 melhores e piores notas
st.title("Top 3 Melhores e Piores Notas")

# Criar duas colunas para separar melhores e piores notas
col_melhores, col_piores = st.columns(2)

# Top 3 melhores notas
top_3_melhores = df_filtrado.nlargest(3, 'imdbAverageRating')
top_3_melhores['rank'] = range(1, len(top_3_melhores) + 1)
for i, row in top_3_melhores.iterrows():
    with col_melhores:
        if row['rank'] == 1:
            st.subheader("Melhor Filme")
        else:
            st.subheader(f"{int(row['rank'])}° Melhor")
        st.write(f"**Título:** {row['title']}")
        st.write(f"**Nota Média no IMDB:** {row['imdbAverageRating']}")

# Top 3 piores notas
top_3_piores = df_filtrado.nsmallest(3, 'imdbAverageRating')
top_3_piores['rank'] = range(1, len(top_3_piores) + 1)
for i, row in top_3_piores.iterrows():
    with col_piores:
        if row['rank'] == 1:
            st.subheader("Pior Filme")
        else:
            st.subheader(f"{int(row['rank'])}° Pior")
        st.write(f"**Título:** {row['title']}")
        st.write(f"**Nota Média no IMDB:** {row['imdbAverageRating']}")