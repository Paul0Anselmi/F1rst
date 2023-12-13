#!/usr/bin/env python
# coding: utf-8

# In[142]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
import scipy
import seaborn as sns
import statistics as st


# importando o base de dados
superheroes_data = pd.read_csv(r'C:\Users\Arthur Scheffer\Downloads\superheroes_nlp_dataset.csv')

superheroes_data.tail(30)


# In[143]:


# O intuito aqui é perceber se a variavel Overall_Score apresenta valores que dificultam a analise
non_numeric_values = superheroes_data[pd.to_numeric(superheroes_data['overall_score'], errors='coerce').isna()]

non_numeric_values_table = non_numeric_values[['name', 'overall_score']]

non_numeric_values_table.tail(270)

# como apresenta valores que dificultam a análise vamos entao criar uma nova variavel Overall Score


# In[144]:


# Distribuição da variavel score dada
superheroes_data['overall_score'] = pd.to_numeric(superheroes_data['overall_score'], errors='coerce')
plt.figure(figsize=(11, 7))
sns.histplot(superheroes_data['overall_score'].dropna(), kde=True)
plt.title('Distribution of Overall Scores')
plt.xlabel('Overall Score')
plt.ylabel('Frequency')



# In[145]:


# Entender a correlção dos Scores
all_scores = [
    'intelligence_score', 'strength_score', 'speed_score', 
    'durability_score', 'power_score', 'combat_score'
]
for col in all_scores:
    superheroes_data[col] = pd.to_numeric(superheroes_data[col], errors='coerce')

# MAtriz de correlação
corrected_scores_correlation_matrix = superheroes_data[all_scores].corr()

plt.figure(figsize=(12, 8))
sns.heatmap(corrected_scores_correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Matriz de Correlação dos Scores')
plt.show()


# In[147]:


#como o overall score tem alguns problemas como simbolos, traços entao criei uma nova variavel com o score_geral
#não esta sendo considerado pesos em cada score
superheroes_data["novo_ov_score"] = superheroes_data[all_scores].mean(axis = 1)

superheroes_data["novo_ov_score"] = pd.to_numeric(superheroes_data["novo_ov_score"], errors='coerce')
plt.figure(figsize=(11, 7))
sns.histplot(superheroes_data["novo_ov_score"].dropna(), kde=True)
plt.title('Histograma Novo Overall Score')
plt.xlabel('Overall Score')
plt.ylabel('Frequency')


# In[148]:


superheroes_data[superheroes_data["novo_ov_score"]== 0]

# Podemos ver pela tabela plota abaixo, vemos que tem varios herois que não foram preenchidos, podendo prejudicar a análise 
# causando algum tipo de tendencia


# In[149]:


# Separando Novo_overal Score em Quantil
# Vamos indicar a partir do novo score criado qual o nivel de força do heroi, dividindo por A, B, C, D
# Sendo o A o mais forte e D o mais fraco

quantil = st.quantiles(superheroes_data["novo_ov_score"], n = 4, method = 'exclusive')
quantil

qt_list = []
for i in range(len(superheroes_data)):
    if superheroes_data["novo_ov_score"][i] < quantil[0]:
        qt_list.append("D")
    elif superheroes_data["novo_ov_score"][i] < quantil[1]:
        qt_list.append("C")
    elif superheroes_data["novo_ov_score"][i] < quantil[2]:
        qt_list.append("B")
    else:
        qt_list.append("A")
superheroes_data["Classe_Heroi"]=qt_list



# In[150]:


# Filtrando os dados que estão não preenchidos

superheroes_data = superheroes_data[superheroes_data["novo_ov_score"] != 0 ]
superheroes_data[superheroes_data["Classe_Heroi"] != 'D' ]


# In[151]:


# Identificando a frencia que cada poder aparece 
power_columns = [col for col in superheroes_data.columns if col.startswith('has_')]

# Frenquencia
# Plotando a frequencia de todos os poderes
all_power_distribution = superheroes_data[power_columns].sum().sort_values(ascending=False)

plt.figure(figsize=(15, 8))
all_power_distribution.plot(kind='bar')
plt.title('Frequencia de todos os poderes')
plt.ylabel('Count')
plt.xlabel('Powers')
plt.xticks(rotation=90) 
plt.show()




# In[152]:


# A partir da classificação de cada heroi, podemos ver qual poder aparece com mais frequencia em cada classificação de Heroi
# Sera focado apresentar os Top 5 poderes em cada Classe 

top_powers_by_class = {}
for class_hero in ['A', 'B', 'C', 'D']:
    class_data = superheroes_data[superheroes_data["Classe_Heroi"] == class_hero]
    top_powers = class_data[power_columns].sum().sort_values(ascending=False).head(5)
    top_powers_by_class[class_hero] = top_powers

top_powers_by_class


fig, axes = plt.subplots(2, 2, figsize=(15, 10))
axes = axes.flatten()

for i, class_hero in enumerate(['A', 'B', 'C', 'D']):
    top_powers = top_powers_by_class[class_hero]
    axes[i].bar(top_powers.index, top_powers.values)
    axes[i].set_title(f'Class {class_hero} - Top 5 Poderes')
    axes[i].set_ylabel('Count')
    axes[i].set_xlabel('Poder')
    axes[i].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# Criando a tabela
top_powers_table = pd.DataFrame.from_dict(top_powers_by_class)
top_powers_table.columns = ['Class A', 'Class B', 'Class C', 'Class D']
top_powers_table.index.name = 'Power'

top_powers_table


# In[153]:


# Seria interessante para trazer uma informação mais aprofundada de cada calsse trazer um mapeamento de perfil

profile_columns = ['alignment', 'occupation', 'gender', 'type_race']

predominant_profiles_by_class = superheroes_data.groupby('Classe_Heroi')[profile_columns].agg(pd.Series.mode)

print(predominant_profiles_by_class)

# onde podemos ver que temos a predomincia de Alignment , gender, type_race iguais para cada classe
# se diferenciando na variavel occupation


# In[ ]:




