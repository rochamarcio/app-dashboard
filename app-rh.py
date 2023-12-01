
import streamlit as st
import plotly.express as px
import pandas as pd


# deixa o layout responsivo, ou seja, aproveita toda a tela
st.set_page_config(layout='wide')

# le a base de dados do dashboard
df = pd.read_csv('base_rh.csv', sep=',')

# cria um slider para que o usuário consiga alterar a largura do gráfico
width = st.slider('Escolha o tamanho do gráfico:', min_value=400, max_value=800, value=400)


##################################################################
# Funções para gerar gráficos da página da Análise Univariada
##################################################################

# Função que cria um gráfico de barras
def constroi_grafico_barras(variavel):
    contagem = df[variavel].value_counts().reset_index()
    contagem.columns = [variavel, 'Contagem']
    
    # Criando o gráfico de barras com o Plotly
    fig = px.bar(contagem, x=variavel, y='Contagem',text='Contagem', title='Contagem de ' + variavel , labels={'Contagem': 'Quantidade'})

    fig.update_layout(width=int(width))

    return fig

# Função que cria um gráfico de histograma
def constroi_grafico_hist(variavel):
    contagem = df[variavel].value_counts().reset_index()
    contagem.columns = [variavel, 'Contagem']
    
    # Criando o gráfico de barras com o Plotly
    fig = px.histogram(df[variavel], nbins=10, title='Histograma de ' + variavel, labels={'value': 'Valor', 'count': 'Contagem'})

    fig.update_layout(width=int(width))

    return fig


# Função que cria todos os gráficos da página da Análise Univariada
def pagina_univariada():

    
    st.title('Dashboard RH')
    st.text('Esse dashboard faz uma análise exploratória da base de RH de uma empresa de tecnologia.')


    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8 = st.columns(2)



    col1.plotly_chart(constroi_grafico_barras('Funcionario_Deixou_Empresa'))
    col2.plotly_chart(constroi_grafico_barras('Freq_Viagens'))
    col3.plotly_chart(constroi_grafico_barras('Formacao'))
    col4.plotly_chart(constroi_grafico_barras('Estado_Civil'))
    col5.plotly_chart(constroi_grafico_barras('Faz_hora_extras'))
    col6.plotly_chart(constroi_grafico_barras('Equilibrio_de_Vida'))
    col7.plotly_chart(constroi_grafico_hist('Idade'))
    col8.plotly_chart(constroi_grafico_hist('Tempo_de_empresa'))


##################################################################
# Funções para gerar gráficos da página da Análise Bivariada
##################################################################

# Função que cria um gráfico de barras bivariado
def constroi_grafico_barras_bivariado(variavel):

    tabela_contagem = pd.pivot_table(df, index=variavel, columns='Funcionario_Deixou_Empresa', aggfunc='size', fill_value=0).reset_index()
    fig = px.bar(tabela_contagem, x=variavel, y=['Não', 'Sim'],
                title='Impacto de ' + variavel + ' na Rotatividade de Funcionários',
                labels={'value': 'Qte', 'Funcionario_Deixou_Empresa': variavel},
                color_discrete_map={'Não': 'gray', 'Sim': 'red'}, 
                barmode='group')

    fig.update_layout(width=int(width))

    return fig


# Função que cria um gráfico box plot bivariado
def constroi_boxplot_bivariado(variavel):

    
    fig = px.box(df, x="Funcionario_Deixou_Empresa", y=variavel,title='Impacto de ' + variavel + ' na Rotatividade de Funcionários')

    fig.update_layout(width=int(width))

    return fig

# Função que cria todos os gráficos da página da Análise Bivariada
def pagina_bivariada():

    st.title('Dashboard RH')
    st.text('Esse dashboard faz uma análise exploratória da base de RH de uma empresa de tecnologia.')

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8 = st.columns(2)

    col1.plotly_chart(constroi_grafico_barras_bivariado('Freq_Viagens'))
    col2.plotly_chart(constroi_grafico_barras_bivariado('Formacao'))
    col3.plotly_chart(constroi_grafico_barras_bivariado('Estado_Civil'))
    col4.plotly_chart(constroi_grafico_barras_bivariado('Faz_hora_extras'))
    col5.plotly_chart(constroi_grafico_barras_bivariado('Equilibrio_de_Vida'))
    col6.plotly_chart(constroi_boxplot_bivariado('Idade'))
    col7.plotly_chart(constroi_boxplot_bivariado('Tempo_de_empresa'))


# Cria a barra lateral da aplicação
st.sidebar.title('Navegação')
pagina_selecionada = st.sidebar.radio('Selecione uma página', ['Análise Univariada', 'Análise Bivariada'])

if pagina_selecionada == 'Análise Univariada':
    pagina_univariada()
elif pagina_selecionada == 'Análise Bivariada':
    pagina_bivariada()
