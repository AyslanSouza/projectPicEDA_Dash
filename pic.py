import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração do layout
st.set_page_config(layout="wide")

# Carregar os dados
arquivo = 'C:\\Users\\Citel\\Desktop\\Ayslan\\PIC_Dashboard\\dados_redcap_estruturados.xlsx'
planilhas = pd.read_excel(arquivo, sheet_name=None)

df_pacientes = planilhas['Pacientes']
df_diagnosticos = planilhas['Diagnósticos']

# 📌 Sidebar para seleção de filtros
sexo = st.sidebar.selectbox("Selecione o sexo:", ["Todos", "masculino", "feminino"])
# ✅ Esse código cria um menu lateral (sidebar) onde o usuário pode escolher entre "Todos", "masculino" e "feminino".
# ✅ Isso permite filtrar os pacientes pelo gênero antes de gerar o gráfico

df_pacientes_filtrado = df_pacientes.copy()

if sexo != "Todos":
    df_pacientes_filtrado = df_pacientes_filtrado[df_pacientes_filtrado["genero"] == sexo]
# ✅ Aqui, criamos uma cópia do dataframe df_pacientes para não alterar os dados originais.
# ✅ Se o usuário não escolheu "Todos", o código filtra apenas os pacientes do sexo selecionado.

df_sexo = df_pacientes_filtrado["genero"].value_counts().reset_index()
df_sexo.columns = ["Sexo", "Quantidade"]
fig_sexo = px.bar(df_sexo, x="Sexo", y="Quantidade", color="Sexo", title="Distribuição de Pacientes por Sexo")
# ✅ Transformamos os dados filtrados em um formato adequado para o gráfico.
# ✅ value_counts() conta quantos pacientes há para cada categoria (masculino/feminino).
# ✅ reset_index() converte a contagem em um DataFrame para ser usado pelo gráfico.
# ✅ O gráfico gerado é um gráfico de barras, onde cada barra representa um gênero e sua quantidade.

st.plotly_chart(fig_sexo, use_container_width=True)
# ✅ Esse comando exibe o gráfico interativamente na aplicação Streamlit.
# ✅ O parâmetro use_container_width=True faz o gráfico se ajustar ao tamanho da tela.

#--------------------------------------------------------------------------#

# 📌 Sidebar para seleção de faixa etária
idade = st.sidebar.selectbox("Selecione a faixa etária:", ["todos", "0-12 anos", "13-17 anos", "18-29 anos", "30-49 anos", "50+ anos"])

# 📌 Estratificação de pacientes com base na idade
df_idade_filtrado = df_pacientes.copy()

bins = [0, 12, 18, 30, 50, 100]
labels = ["0-12 anos", "13-17 anos", "18-29 anos", "30-49 anos", "50+ anos"]

# Criando a coluna faixa etária corretamente
df_idade_filtrado["faixa_etaria"] = pd.cut(df_idade_filtrado["idade"], bins=bins, labels=labels)

# 📌 Aplicar filtragem APÓS a criação da coluna
if idade != "todos":
    df_idade_filtrado = df_idade_filtrado[df_idade_filtrado["faixa_etaria"] == idade]

# 📌 Contagem correta das faixas etárias
df_faixa_etaria = df_idade_filtrado["faixa_etaria"].value_counts().reset_index()
df_faixa_etaria.columns = ["Faixa Etária", "Quantidade"]

# 📌 Criar gráfico com dados corretos
fig_idade = px.bar(df_faixa_etaria, x="Faixa Etária", y="Quantidade", color="Faixa Etária", title="Distribuição de Pacientes por Faixa Etária")

# 📌 Exibir gráfico no Streamlit
st.plotly_chart(fig_idade, use_container_width=True)

#-------------------------------------------------------------------------#

import pandas as pd
import streamlit as st
import plotly.express as px

# 📌 Criar cópia do dataframe para não modificar o original
df_ORPHA = df_diagnosticos.copy()

# 📌 Verificar nome correto da coluna ORPHA
coluna_orpha = "orpha_code" if "orpha_code" in df_ORPHA.columns else "ORPHA"
df_ORPHA[coluna_orpha] = df_ORPHA[coluna_orpha].astype(str)

# 📌 Agrupar códigos ORPHA com menos de 100 ocorrências como "outros"
contagem_orpha = df_ORPHA[coluna_orpha].value_counts()
codigos_menos_100 = contagem_orpha[contagem_orpha < 100].index
df_ORPHA[coluna_orpha] = df_ORPHA[coluna_orpha].replace(codigos_menos_100, "outros")

# 📌 Sidebar para seleção de código ORPHA
ORPHA = st.sidebar.selectbox("Selecione o código ORPHA:", ["Todos"] + df_ORPHA[coluna_orpha].unique().tolist())

# 📌 Filtrar ORPHA corretamente após a substituição dos valores
if ORPHA != "Todos":
    df_ORPHA = df_ORPHA[df_ORPHA[coluna_orpha] == ORPHA]  # Filtragem correta

# 📊 Contagem correta dos códigos ORPHA, incluindo "outros"
df_ORPHA_cod = df_ORPHA[coluna_orpha].value_counts().reset_index()
df_ORPHA_cod.columns = ["Código ORPHA", "Quantidade"]

# 📌 Criar gráfico com dados corretos
fig_orpha = px.bar(df_ORPHA_cod, x="Código ORPHA", y="Quantidade", color="Código ORPHA", 
                   title="Distribuição de Pacientes por Código ORPHA")

# 📌 Exibir gráfico no Streamlit
st.plotly_chart(fig_orpha, use_container_width=True)

