import altair as alt

def create_charts(df_filtrado):
    charts = {}

    # Gráfico de Nota Média no IMDB por Ano de Lançamento
    charts['release_year'] = (
        alt.Chart(df_filtrado)
        .mark_bar()
        .encode(
            x=alt.X("releaseYear:T", title="Ano de Lançamento"),
            y=alt.Y("imdbAverageRating:Q", title="Nota Média no IMDB"),
            color='tipo:N'
        )
        .properties(height=320, title="Nota Média no IMDB por Ano de Lançamento")
    )

    # Gráfico de Nota Média no IMDB por País
    df_avaliacao_pais = df_filtrado.groupby('country')['imdbAverageRating'].mean().reset_index()
    charts['country'] = (
        alt.Chart(df_avaliacao_pais)
        .mark_bar()
        .encode(
            x=alt.X("country:N", title="País"),
            y=alt.Y("imdbAverageRating:Q", title="Nota Média no IMDB"),
        )
        .properties(height=320, title="Nota Média no IMDB por País")
    )

    # Gráfico de Nota Média no IMDB por Tipo
    df_avaliacao_tipo = df_filtrado.groupby('tipo')['imdbAverageRating'].mean().reset_index()
    charts['type'] = (
        alt.Chart(df_avaliacao_tipo)
        .mark_bar()
        .encode(
            x=alt.X("tipo:N", title="Tipo"),
            y=alt.Y("imdbAverageRating:Q", title="Nota Média no IMDB"),
        )
        .properties(height=320, title="Nota Média no IMDB por Tipo")
    )

    # Gráfico de Nota Média no IMDB por Ano de Lançamento (Linha)
    df_avaliacao_ano = df_filtrado.groupby(df_filtrado['releaseYear'].dt.year)['imdbAverageRating'].mean().reset_index()
    charts['year_line'] = (
        alt.Chart(df_avaliacao_ano)
        .mark_line(point=True)
        .encode(
            x=alt.X("releaseYear:O", title="Ano de Lançamento"),
            y=alt.Y("imdbAverageRating:Q", title="Nota Média no IMDB"),
        )
        .properties(height=320, title="Nota Média no IMDB por Ano de Lançamento")
    )

    # Gráfico de Nota Média no IMDB por Países Disponíveis
    df_avaliacao_disponibilidade = df_filtrado.groupby('availableCountries')['imdbAverageRating'].mean().reset_index()
    charts['available_countries'] = (
        alt.Chart(df_avaliacao_disponibilidade)
        .mark_bar()
        .encode(
            x=alt.X("availableCountries:N", title="Países Disponíveis"),
            y=alt.Y("imdbAverageRating:Q", title="Nota Média no IMDB"),
        )
        .properties(height=320, title="Nota Média no IMDB por Países Disponíveis")
    )

    return charts
