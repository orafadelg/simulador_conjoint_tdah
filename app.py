import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout="wide")

st.title("Simulador de Conjoint para Medicamentos TDAH")

st.write("Compare dois cenários de medicamentos e veja o impacto nas escolhas dos consumidores com base em um estudo fictício completo.")

# Dados simulados de coeficientes do estudo (valores fictícios)
marca_impact = {'Genérico': -0.2, 'Atenta': 0.1, 'Juneve': 0.15, 'Venvanse': 0.3}
dosagem_impact = {'30mg': -0.1, '50mg': 0.0, '70mg': 0.2}
preco_impact = {'R$100': 0.2, 'R$150': 0.0, 'R$200': -0.2}
quantidade_impact = {'30 comprimidos': -0.1, '60 comprimidos': 0.1}

st.subheader("1. Selecione as combinações a serem comparadas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Opção A**")
    marca_a = st.selectbox("Marca", list(marca_impact.keys()), key="a_marca")
    dosagem_a = st.selectbox("Dosagem", list(dosagem_impact.keys()), key="a_dosagem")
    preco_a = st.selectbox("Preço", list(preco_impact.keys()), key="a_preco")
    quantidade_a = st.selectbox("Quantidade", list(quantidade_impact.keys()), key="a_quantidade")

with col2:
    st.markdown("**Opção B**")
    marca_b = st.selectbox("Marca", list(marca_impact.keys()), key="b_marca")
    dosagem_b = st.selectbox("Dosagem", list(dosagem_impact.keys()), key="b_dosagem")
    preco_b = st.selectbox("Preço", list(preco_impact.keys()), key="b_preco")
    quantidade_b = st.selectbox("Quantidade", list(quantidade_impact.keys()), key="b_quantidade")

# Cálculo de score baseado no modelo fictício
score_a = sum([
    marca_impact[marca_a],
    dosagem_impact[dosagem_a],
    preco_impact[preco_a],
    quantidade_impact[quantidade_a]
])

score_b = sum([
    marca_impact[marca_b],
    dosagem_impact[dosagem_b],
    preco_impact[preco_b],
    quantidade_impact[quantidade_b]
])

# Resultado
st.subheader("2. Preferência Estimada")

result_df = pd.DataFrame({
    'Opção': ['A', 'B'],
    'Score Estimado': [score_a, score_b]
})

bar_chart = alt.Chart(result_df).mark_bar().encode(
    x='Opção:N',
    y='Score Estimado:Q',
    color='Opção:N'
).properties(title="Probabilidade Estimada de Escolha")

st.altair_chart(bar_chart, use_container_width=True)
st.dataframe(result_df)

# Simulação de curva de demanda
st.subheader("3. Curva de Preço Ideal (Simulada)")
precos = [100, 120, 140, 160, 180, 200, 220]
demanda = [95, 90, 80, 65, 50, 35, 20]

curva_df = pd.DataFrame({
    'Preço (R$)': precos,
    'Demanda Estimada (%)': demanda
})

curva_chart = alt.Chart(curva_df).mark_line(point=True).encode(
    x='Preço (R$):Q',
    y='Demanda Estimada (%):Q'
).properties(title="Curva de Demanda x Preço")

st.altair_chart(curva_chart, use_container_width=True)
