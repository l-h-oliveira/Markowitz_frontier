# %%
from distutils.log import info
from matplotlib import ticker
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from datetime import datetime as dt

# Faz com que o terminal exiba as tabelas no estilo do Jupyther
from IPython.display import display 

# %%
# Datas de início e fim da análise
start_date = '2000-01-01'
end_date = dt.today().strftime('%Y-%m-%d')
# %%
#  Dados do IBOV e do S&P500 para contextualização
''' 
Lembrando que os códigos no Yahoo finance são 
^BVSP -> IBOV  e
^GSPC -> S&P500 
'''

index_data = yf.download(tickers = ['^BVSP', '^GSPC'] , start = start_date, end = end_date, interval = '1d')

# Vamos eliminar as colunas 'Adj Close' e 'Volume'
index_data = index_data.drop(columns = ['Adj Close', 'Volume'])

display(index_data.head())
display(index_data.info())

# %%
# Vamos selecionar um grupo de empresas para fazer a otimização de Markowitz
my_tickers_temp = ['PETR4', 'VALE3', 'BBAS3']

# Adicionando o sufixo '.SA' para o padrão Yahoo Finance
my_tickers = list(map(lambda x: x + '.SA', my_tickers_temp))

stocks_data = yf.download(tickers = my_tickers , start = start_date, end = end_date, interval = '1d')

# Eliminando as colunas 'Adj Close' e 'Volume'
stocks_data = stocks_data.drop(columns = ['Adj Close', 'Volume'])

# %%

# Um gráfico rápido 