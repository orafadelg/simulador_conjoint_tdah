import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout="wide")

st.title("Simulador de Conjoint para Medicamentos TDAH")

# Filtros
st.subheader("Filtros de Perfil")
col_idade, col_regiao, col_classe = st.columns(3)
idade = col_idade.selectbox("Idade", ["18-30", "31-50", "50+"])
regiao = col_regiao.selectbox("Região", ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"])
classe = col_classe.selectbox("Classe Social", ["A", "B", "C", "DE"])

# Coeficientes básicos
base_marca_impact = {'Genérico': -0.2, 'Atenta': 0.1, 'Juneve': 0.15, 'Venvanse': 0.3}
base_dosagem_impact = {'30mg': -0.1, '50mg': 0.0, '70mg': 0.2}
base_preco_impact = {'R$100': 0.2, 'R$150': 0.0, 'R$200': -0.2}
base_quantidade_impact = {'30 comprimidos': -0.1, '60 comprimidos': 0.1}

# Função para aplicar pesos conforme filtros
def ajustar_pesos(base_dict, fator):
    return {k: round(v * fator, 3) for k, v in base_dict.items()}

# Define fator de ajuste com base nos filtros
fator_ajuste = 1.0
if idade == "18-30":
    fator_ajuste += 0.05
elif idade == "50+":
    fator_ajuste -= 0.05

if classe == "A":
    fator_ajuste += 0.05
elif classe == "DE":
    fator_ajuste -= 0.05

if regiao in ["Norte", "Nordeste"]:
    fator_ajuste -= 0.03
elif regiao in ["Sul", "Sudeste"]:
    fator_ajuste += 0.03

# Aplica ajuste
marca_impact = ajustar_pesos(base_marca_impact, fator_ajuste)
dosagem_impact = ajustar_pesos(base_dosagem_impact, fator_ajuste)
preco_impact = ajustar_pesos(base_preco_impact, fator_ajuste)
quantidade_impact = ajustar_pesos(base_quantidade_impact, fator_ajuste)

st.subheader("1. Escolha as opções de cada oferta")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Oferta A**")
    marca_a = st.selectbox("Marca", list(marca_impact.keys()), key="a_marca")
    dosagem_a = st.selectbox("Dosagem", list(dosagem_impact.keys()), key="a_dosagem")
    preco_a = st.selectbox("Preço", list(preco_impact.keys()), key="a_preco")
    quantidade_a = st.selectbox("Quantidade", list(quantidade_impact.keys()), key="a_quantidade")

with col2:
    st.markdown("**Oferta B**")
    marca_b = st.selectbox("Marca", list(marca_impact.keys()), key="b_marca")
    dosagem_b = st.selectbox("Dosagem", list(dosagem_impact.keys()), key="b_dosagem")
    preco_b = st.selectbox("Preço", list(preco_impact.keys()), key="b_preco")
    quantidade_b = st.selectbox("Quantidade", list(quantidade_impact.keys()), key="b_quantidade")

with col3:
    st.markdown("**Oferta C**")
    marca_c = st.selectbox("Marca", list(marca_impact.keys()), key="c_marca")
    dosagem_c = st.selectbox("Dosagem", list(dosagem_impact.keys()), key="c_dosagem")
    preco_c = st.selectbox("Preço", list(preco_impact.keys()), key="c_preco")
    quantidade_c = st.selectbox("Quantidade", list(quantidade_impact.keys()), key="c_quantidade")

# Cálculo dos scores
score_a = sum([marca_impact[marca_a], dosagem_impact[dosagem_a], preco_impact[preco_a], quantidade_impact[quantidade_a]])
score_b = sum([marca_impact[marca_b], dosagem_impact[dosagem_b], preco_impact[preco_b], quantidade_impact[quantidade_b]])
score_c = sum([marca_impact[marca_c], dosagem_impact[dosagem_c], preco_impact[preco_c], quantidade_impact[quantidade_c]])

scores = {'A': score_a, 'B': score_b, 'C': score_c}
vencedor = max(scores, key=scores.get)

# Exibição dos resultados
st.subheader("2. Preferência Estimada")

colr1, colr2, colr3 = st.columns(3)

def estilo_resultado(label, score, vencedor):
    cor = "background-color: #d4f4dd; padding: 10px; border-radius: 8px;" if label == vencedor else "padding: 10px; border-radius: 8px;"
    st.markdown(f"""
    <div style="{cor}; text-align: center;">
        <h4>Oferta {label}</h4>
        <p style='font-size:24px; font-weight:bold;'>{score:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

with colr1:
    estilo_resultado("A", score_a, vencedor)
with colr2:
    estilo_resultado("B", score_b, vencedor)
with colr3:
    estilo_resultado("C", score_c, vencedor)
