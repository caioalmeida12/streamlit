import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar o arquivo CSV
csv_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
if csv_file is not None:
    csv_file = pd.read_csv(csv_file, sep=';', encoding='latin1')
else:
    csv_file = pd.read_csv('consulta_cand_2024_CE.csv', sep=';', encoding='latin1')

# Inicializar estado da sessão
if 'nm_ue' not in st.session_state:
    st.session_state.nm_ue = None
if 'cargo' not in st.session_state:
    st.session_state.cargo = None

# Filtros na barra lateral
st.sidebar.title('Filtros')
st.sidebar.write('Link para a base de dados: https://dadosabertos.tse.jus.br/dataset/candidatos-2024/resource/af76c401-0972-4ddf-8ea8-00e310ae53b4?inner_span=True')
st.sidebar.write('Selecione uma unidade Eleitoral')
nm_ue = st.sidebar.selectbox('Unidade Eleitoral', [''] + list(csv_file['NM_UE'].unique()), index=0)
st.write(f'Unidade Eleitoral selecionada: {nm_ue}')

st.sidebar.write('Selecione um Cargo')
cargo = st.sidebar.selectbox('Cargo', [''] + list(csv_file['DS_CARGO'].unique()), index=0)
st.write(f'Cargo selecionado: {cargo}')

if st.sidebar.button('Limpar Filtros'):
    st.session_state.nm_ue = None
    st.session_state.cargo = None
    nm_ue = ''
    cargo = ''

# Aplicar filtros
filtered_df = csv_file
if nm_ue:
    filtered_df = filtered_df[filtered_df['NM_UE'] == nm_ue]
if cargo:
    filtered_df = filtered_df[filtered_df['DS_CARGO'] == cargo]

# Criar gráficos
st.title('Prévia dos dados')
st.write(filtered_df.head())

st.title('Distribuição do Grau de Instrução')
fig = px.histogram(filtered_df, x='DS_GRAU_INSTRUCAO')
st.plotly_chart(fig)

st.title('Relação entre Gênero e Grau de Instrução')
fig = px.histogram(filtered_df, x='DS_GRAU_INSTRUCAO', color='DS_GENERO', 
                   color_discrete_map={'MASCULINO': 'lightblue', 'FEMININO': 'orange'})
st.plotly_chart(fig)

st.title('Distribuição da Cor/Raça dos Candidatos')
fig_pie = px.pie(filtered_df, names='DS_COR_RACA')
st.plotly_chart(fig_pie)

st.title('Distribuição de Gênero dos Candidatos')
fig_pie = px.pie(filtered_df, names='DS_GENERO', 
                 color_discrete_map={'MASCULINO': 'lightblue', 'FEMININO': 'orange'})
st.plotly_chart(fig_pie)

feminino_df = filtered_df.query('DS_GENERO == "FEMININO"')
contagem_partido = feminino_df['SG_PARTIDO'].value_counts().reset_index()
contagem_partido.columns = ['SG_PARTIDO', 'count']
st.title('Quantidade de Candidatas femininas por Partido')
fig = px.bar(contagem_partido, x='SG_PARTIDO', y='count', color='count', 
             color_continuous_scale='Blues', title='Quantidade de Candidatas Femininas por Partido')
st.plotly_chart(fig)

masculino_df = filtered_df.query('DS_GENERO == "MASCULINO"')
contagem_partido = masculino_df['SG_PARTIDO'].value_counts().reset_index()
contagem_partido.columns = ['SG_PARTIDO', 'count']
st.title('Quantidade de Candidatos masculinos por Partido')
fig = px.bar(contagem_partido, x='SG_PARTIDO', y='count', color='count', 
             color_continuous_scale='Blues', title='Quantidade de Candidatos Masculinos por Partido')
st.plotly_chart(fig)

st.title('Proporção de Candidatos Masculinos e Femininos por Partido')
fig = px.histogram(filtered_df, x='SG_PARTIDO', color='DS_GENERO', 
                   color_discrete_map={'MASCULINO': 'lightblue', 'FEMININO': 'orange'})
fig.update_traces(texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig)