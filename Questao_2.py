#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import datetime, timedelta
import random

# Criar dados de exemplo
data_inicio = []
data_fim = []
categoria = []
local_inicio = []
local_fim = []
proposito = []
distancia = []

for _ in range(100): 
    data_inicio.append(datetime.now() - timedelta(days=random.randint(1, 30), hours=random.randint(1, 24)))
    data_fim.append(data_inicio[-1] + timedelta(hours=random.randint(1, 5)))
    categoria.append(random.choice(["Negócio", "Pessoal"]))
    local_inicio.append(f"Local_{random.randint(1, 10)}_Inicio")
    local_fim.append(f"Local_{random.randint(1, 10)}_Fim")
    proposito.append(random.choice(["Reunião", "Lazer", "Outro"]))
    distancia.append(round(random.uniform(1, 20), 2))

# Criar DataFrame
df = pd.DataFrame({
    'DATA_INICIO': data_inicio,
    'DATA_FIM': data_fim,
    'CATEGORIA': categoria,
    'LOCAL_INICIO': local_inicio,
    'LOCAL_FIM': local_fim,
    'PROPOSITO': proposito,
    'DISTANCIA': distancia
})

# Salvar o DataFrame em um arquivo CSV
df.to_csv('info_transportes.csv', index=False)

# Carregar o CSV para um DataFrame
df = pd.read_csv("info_transportes.csv", parse_dates=["DATA_INICIO", "DATA_FIM"])

# Formatar a coluna DATA_INICIO para yyyy-MM-dd
df["DT_REFE"] = df["DATA_INICIO"].dt.strftime("%Y-%m-%d")

# Agrupar e calcular as estatísticas
result_df = df.groupby("DT_REFE").agg(
    QT_CORR=("DATA_INICIO", "count"),
    QT_CORR_NEG=("CATEGORIA", lambda x: (x == "Negócio").sum()),
    QT_CORR_PESS=("CATEGORIA", lambda x: (x == "Pessoal").sum()),
    VL_MAX_DIST=("DISTANCIA", "max"),
    VL_MIN_DIST=("DISTANCIA", "min"),
    VL_AVG_DIST=("DISTANCIA", "mean"),
    QT_CORR_REUNI=("PROPOSITO", lambda x: (x == "Reunião").sum()),
    QT_CORR_NAO_REUNI=("PROPOSITO", lambda x: ((x != "Reunião") & x.notnull()).sum())
).reset_index()

# Exibir o DataFrame resultante
print(result_df)


# In[ ]:




