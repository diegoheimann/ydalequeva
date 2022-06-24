#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import interact
import warnings
warnings.filterwarnings('ignore')


# In[2]:


df = pd.read_excel('../Bolsas - Pasado 1-5 al 30-5.xlsx', sheet_name='Hoja2')


# In[3]:


lista = ['21CODSTO', '22ALDSTO', '43CEDSTO', '43CNDST1', '43CNDST2', '43CODSTO', '43CSDST1', '43CSDST2']


# In[4]:


df = df[~df.area.isin(lista)]


# In[ ]:





# In[5]:


capacidad = df.groupby(['fecha', 'area']).sum().reset_index().sort_values(['area', 'fecha'])


# In[6]:


capacidad = capacidad.reset_index()


# In[7]:


capacidad = capacidad.drop('index', axis=1).rename(columns={'cap_maxima':'minutos_totales_disponibles'})


# In[ ]:





# In[8]:


ingresos = pd.read_excel('../Ingresos por categoria -Actualizado 31-05.xlsx', sheet_name='BASE')


# In[9]:


ingresos = ingresos.groupby(['Fecha_Informe', 'route_criteria_cd', 'modelo_de_capacidad']).sum().reset_index()


# In[10]:


ingresos.rename(columns={'Fecha_Informe':'fecha', 'route_criteria_cd':'area', 
                         'COUNT_of__Cálculo1':'minutos_requeridos', 'modelo_de_capacidad':'categoria'}, inplace=True)


# In[11]:


ingresos.minutos_requeridos = ingresos.minutos_requeridos * 60


# In[12]:


ingresos.categoria = np.where(ingresos.categoria == 'DOM - SERVICE P', 'P', 'NP')


# In[13]:


ingresos = ingresos.set_index(['fecha','area', 'categoria'])['minutos_requeridos'].unstack().reset_index().sort_values(['area', 'fecha'])


# In[14]:


ingresos = ingresos.dropna(axis=0)


# In[ ]:





# In[15]:


porcentajes_actuales = pd.read_excel('../Porcentajes Actuales.xlsx')


# In[16]:


porcentajes_actuales = porcentajes_actuales.drop(porcentajes_actuales[porcentajes_actuales['CATEGORIAS'] == 'DOM - SERVICE T'].index).rename(columns={'ROUTE':'area'}).drop(['CATEGORIAS', '% Dist'], axis=1)


# In[ ]:





# In[17]:


tabla = capacidad.merge(ingresos, on=['fecha', 'area']).rename(columns={'NP':'minutos_requeridos_no_prioritario', 
                                                                        'P':'minutos_requeridos_prioritario'})


# In[18]:


resultados = {}
resultados_np = {}

for area in tabla.area.unique():
    
    data = tabla[tabla.area == area]
    residuos= []
    residuos_np = []
    
    # Porcentajes de 1 a 99
    for i in np.arange(1,100):
    
        porcentaje = i/100
    
        data['disponibles_prioritario'] = data.minutos_totales_disponibles * porcentaje
        data['disponibles_no_prioritario'] = data.minutos_totales_disponibles * (1 - porcentaje)
    
        data['residuo_prioritario'] = np.abs(data.disponibles_prioritario - data.minutos_requeridos_prioritario)
        data['residuo_no_prioritario'] = np.abs(data.disponibles_no_prioritario - data.minutos_requeridos_no_prioritario)
    
        residuo = round(data.residuo_prioritario.sum(),0)
        residuos.append(residuo)
        
        residuo_np = round(data.residuo_no_prioritario.sum(),0)
        residuos_np.append(residuo_np)
        
    resultados[area] = residuos
    resultados_np[area] = residuos_np


# In[19]:


resultados.keys()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[24]:


def grafico_variable(col):
        
    plt.figure(figsize=(14,8))
    plt.title('Residuo acumulado en funcion del porcentaje asignado a Prioritarios')
    sns.scatterplot(x=np.arange(1,100), y=resultados[col])
    sns.scatterplot(x=np.arange(1,100), y=resultados_np[col])
    
    valor = porcentajes_actuales[porcentajes_actuales.area==col]['Porcentaje']
    plt.scatter(valor, resultados[col][valor.values[0]], marker='o', s=200, color='red')
    
    print('Valor mínimo para un porcentaje de', resultados[col].index(min(resultados[col])))
    print('Valor actual', valor.values[0])


# In[25]:


interact(grafico_variable, col=tabla.area.unique());


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from plotly import tools


# In[ ]:


# fig = go.Figure()

# fig.add_trace(go.Scatter(x=np.arange(1,100), y=[resultados['11ZADSTO'], r, mode="markers"))

# #fig.add_trace(go.Scatter(x=np.arange(1,100), y=resultados_np['11ZADSTO'], mode="markers"))


# fig.update_layout(
#     font_family="Averta",
#     hoverlabel_font_family="Averta",
#     title_text="Basic Scatter Plot",
#     xaxis_title_text="x",
#     xaxis_title_font_size=18,
#     xaxis_tickfont_size=16,
#     yaxis_title_text="y",
#     yaxis_title_font_size=18,
#     yaxis_tickfont_size=16,
#     hoverlabel_font_size=16,
#     height=600, 
#     width=600
# )
# fig.show()


# In[ ]:


# fig = go.Figure()

# fig.add_trace(go.Scatter(x=np.arange(1,100), y=[resultados['11ZADSTO'],resultados_np['11ZADSTO']], mode="markers"))

# # fig.add_trace(go.Scatter(x=np.arange(1,100), y=resultados_np['11ZADSTO'], mode="markers"))

# # trace1 = go.Scatter(x=np.arange(1,100), y=resultados['11ZADSTO'], mode="markers")

# # trace2 = go.Scatter(x=np.arange(1,100), y=resultados_np['11ZADSTO'], mode="markers")

# cols = pd.DataFrame.from_dict(resultados).columns

# my_buttons = [dict(method = "restyle",
#                    args = [{'y': [ resultados[c], resultados_np[c] ]}],
#                    label = c) for k, c in enumerate(cols)]

# fig.update_layout(font_family="Averta",
#     hoverlabel_font_family="Averta",
#     title_text="Basic Scatter Plot",
#     xaxis_title_text="x",
#     xaxis_title_font_size=18,
#     xaxis_tickfont_size=16,
#     yaxis_title_text="y",
#     yaxis_title_font_size=18,
#     yaxis_tickfont_size=16,
#     hoverlabel_font_size=16,
#     height=600, 
#     width=600,
    
    
#                  updatemenus=[dict(active=0,
#                                    x= 1, y=1, 
#                                    xanchor='left', 
#                                    yanchor='top',
#                                    buttons=my_buttons)
#                               ])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




