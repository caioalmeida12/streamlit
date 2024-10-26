import streamlit as st
import altair as alt
from data_processing import load_and_process_data

def show_detalhes():
    st.title("Página de Detalhes")

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

    # Exibir os dados filtrados como uma tabela
    st.dataframe(df_filtrado)

    # Criar duas colunas para a primeira linha
    col1, col2 = st.columns(2)

    # Agrupar por 'director' e calcular a média de 'imdbAverageRating'
    df_avaliacao_diretor = df_filtrado.groupby('director')['imdbAverageRating'].mean().reset_index()

    # Exibir os dados como um gráfico Altair usando `st.altair_chart`.
    grafico = (
        alt.Chart(df_avaliacao_diretor)
        .mark_bar()
        .encode(
            x=alt.X("director:N", title="Diretor"),
            y=alt.Y("imdbAverageRating:Q", title="Nota Média no IMDB"),
        )
        .properties(height=320, title="Nota Média no IMDB por Diretor")
    )
    col1.altair_chart(grafico, use_container_width=True)

    # Agrupar por 'cast' e calcular a média de 'imdbAverageRating'
    df_avaliacao_elenco = df_filtrado.groupby('cast')['imdbAverageRating'].mean().reset_index()

    # Exibir os dados como um gráfico Altair usando `st.altair_chart`.
    grafico = (
        alt.Chart(df_avaliacao_elenco)
        .mark_bar()
        .encode(
            x=alt.X("cast:N", title="Elenco"),
            y=alt.Y("imdbAverageRating:Q", title="Nota Média no IMDB"),
        )
        .properties(height=320, title="Nota Média no IMDB por Elenco")
    )
    col2.altair_chart(grafico, use_container_width=True)

show_detalhes()
