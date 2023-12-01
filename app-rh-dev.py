import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')

df = pd.read_csv ('base_rh.csv')

width = st.slider('Escolha o tamanho do gráfico:', min_value=300, max_value=550, value=400)

st.title ('Dashboard RH')

def control_grafico_barras ( variavel ):
    contagem = df[variavel].value_counts().reset_index()
    fig = px.bar (contagem, x=variavel, y="count", title="Qte de Funcionários por " + variavel, text_auto=True, color_discrete_sequence=px.colors.qualitative.T10)
    
    fig.update_layout (width=int(width))
    
    return fig

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
    
graf_1 = control_grafico_barras ("Estado_Civil")
col1.plotly_chart (graf_1)

graf_2 = control_grafico_barras ("Formacao")
col2.plotly_chart (graf_2)

graf_3 = control_grafico_barras ("Freq_Viagens")
col3.plotly_chart (graf_3)

st.sidebar.title('Navegação')
pagina_selecionada = st.sidebar.radio('Selecione uma página', ['Análise Univariada', 'Análise Bivariada'])

