import streamlit as st
import pandas as pd
import numpy as np
import itertools
from sklearn.linear_model import LinearRegression
import altair as alt

# Define atributos do Conjoint
brands = ['Genérico', 'Atenta', 'Juneve', 'Venvanse']
dosages = ['30mg', '50mg', '70mg']
prices = ['R$100', 'R$150', 'R$200']
quantities = ['30 comprimidos', '60 comprimidos']

# Gerar combinações
profiles = list(itertools.product(brands, dosages, prices, quantities))

# Criar DataFrame de perfis
columns = ['Marca', 'Dosagem', 'Preço', 'Quantidade']
df_profiles = pd.DataFrame(profiles, columns=columns)
df_profiles['ID'] = range(1, len(df_profiles) + 1)

# Interface Streamlit
st.title("Simulador de Conjoint para Medicamentos TDAH")

st.write("Avalie diferentes combinações de medicamentos e veja o impacto nas preferências dos consumidores.")

st.subheader("1. Escolha os perfis que você prefere")

# Mostrar opções
selected_ids = []
for i, row in df_profiles.iterrows():
    with st.expander(f"Opção {row['ID']}: {row['Marca']}, {row['Dosagem']}, {row['Preço']}, {row['Quantidade']}"):
        if st.checkbox(f"Selecionar esta combinação", key=row['ID']):
            selected_ids.append(row['ID'])

# Rodar análise de regressão
if selected_ids:
    st.subheader("2. Resultados da Análise")
    df_profiles['Escolhido'] = df_profiles['ID'].apply(lambda x: 1 if x in selected_ids else 0)

    # One-hot encoding
    df_encoded = pd.get_dummies(df_profiles.drop(columns=['ID']), drop_first=True)

    X = df_encoded.drop(columns=['Escolhido'])
    y = df_encoded['Escolhido']

    model = LinearRegression()
    model.fit(X, y)
    importances = pd.DataFrame({
        'Atributo': X.columns,
        'Importância': model.coef_
    }).sort_values(by='Importância', ascending=False)

    chart = alt.Chart(importances).mark_bar().encode(
        x=alt.X('Importância:Q'),
        y=alt.Y('Atributo:N', sort='-x')
    ).properties(title="Importância dos Atributos na Escolha")

    st.altair_chart(chart, use_container_width=True)
    st.dataframe(importances)

else:
    st.info("Selecione pelo menos uma opção para ver os resultados.")
