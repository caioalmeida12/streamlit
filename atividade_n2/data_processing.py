import pandas as pd

def load_and_process_data():
    # Carregar os dados dos arquivos CSV
    df1 = pd.read_csv('nf1.csv')
    df2 = pd.read_csv('nf2.csv')

    # Renomear colunas para garantir consistência
    df1.rename(columns={'genres': 'generos_nf1', 'type': 'tipo_nf1'}, inplace=True)
    df2.rename(columns={'genres': 'generos_nf2', 'type': 'tipo_nf2'}, inplace=True)

    # Mesclar os datasets na coluna 'title'
    df_merged = pd.merge(df1, df2, on='title')

    # Combinar as colunas de gêneros e tipo
    df_merged['generos'] = df_merged['generos_nf1'].combine_first(df_merged['generos_nf2'])
    df_merged['tipo'] = df_merged['tipo_nf1'].combine_first(df_merged['tipo_nf2'])

    # Expandir a coluna 'availableCountries' para que cada país tenha sua própria linha
    df_merged = df_merged.assign(availableCountries=df_merged['availableCountries'].str.split(',')).explode('availableCountries')
    df_merged['availableCountries'] = df_merged['availableCountries'].str.strip()

    # Verificar novamente se há múltiplos países em uma linha e expandir novamente
    df_merged = df_merged.assign(availableCountries=df_merged['availableCountries'].str.split(',')).explode('availableCountries')
    df_merged['availableCountries'] = df_merged['availableCountries'].str.strip()

    # Expandir a coluna 'generos' para que cada gênero tenha sua própria linha
    df_merged = df_merged.assign(generos=df_merged['generos'].str.split(',')).explode('generos')
    df_merged['generos'] = df_merged['generos'].str.strip()

    # Converter releaseYear para datetime
    df_merged['releaseYear'] = pd.to_datetime(df_merged['releaseYear'], format='%Y')

    return df_merged
