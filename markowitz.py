# %%
from matplotlib import ticker
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from datetime import datetime as dt

# Faz com que o terminal exiba as tabelas no estilo do Jupyther
from IPython.display import display 

# Configurações matplotlib
# plt.rc('text', usetex = True)
# plt.rc('font', **{'family' : "sans-serif"})
# params= {'text.latex.preamble' : [r'\usepackage{amsmath}']}
# plt.rcParams.update(params)


# font1 = {'size': 24,}

# font2 = {'size': 18}

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

# Vamos utilizar apenas os preços de fechamento e eliminar as linhas com valores nulos
index_data = index_data['Close'].dropna(axis = 0)

# Renomeando as colunas
index_data.columns = ['IBOV', 'S&P500']

print("\n Primeira visualização dos dados crus ")
display(index_data.head())
display(index_data.info())

# %%
# Cálculo dos retornos
# Criamos duas novas colunas com os respectivos retornos dos índices. Usamos o método shift do pandas para deslocar os valores do DataFrame em 1 período (o índice se mantém), para calcular a razão entre p dia atual e o dia anterios, ou seja, o retorno diário
index_data[['r_IBOV', 'r_S&P500']] = index_data/index_data.shift(periods = 1)

# Algumas colunas vazias podem ser geradas, vamos eliminá-las
index_data = index_data.dropna(axis = 0)

print('\n Visualizando os dados filtrados')
display(index_data)

# %%
# Agora, vamos gerar os retornos acumulados. Já que nosso retorno é uma razão de preços, devemos calcular os produtos cumulativos (método cumprod do pandas)

fig, ax = plt.subplots(nrows = 2, ncols = 1, figsize = (12,6))
ax[0].plot(index_data['r_IBOV'].cumprod(), label = 'IBOV', color = 'blue')
ax[0].set_ylabel('IBOV (retornos)')
ax[0].set_xticks([])
ax[0].set_xlim([10900, 19250])
ax[0].set_yticks(list(range(9)))
ax[0].set_yticklabels(['0', '', '2', '', '4', '', '6', '',''])
ax[1].plot(index_data['r_S&P500'].cumprod(), label = 'S&P500', color = 'red')
ax[1].set_ylabel('S&P500 (retornos)')
ax[1].set_xlim([10900, 19250])
ax[1].set_yticks([0, 0.5, 1, 1.5, 2, 2.5, 3])
ax[1].set_yticklabels(['0', '','1', '','2', '','3'])
ax[1].set_xlabel('Ano')

# ax.secondary_yaxis('right', functions = (lambda x: 3*x/8, lambda x: 8*x/3)).set_ylabel('S&P500 (retornos)')
plt.subplots_adjust(wspace=0, hspace=0)
plt.show()
fig.savefig('indexes.png')

# %%
# Vamos selecionar um grupo de empresas para fazer a otimização de Markowitz
my_tickers_temp = ['PETR4', 'VALE3', 'BBAS3', 'BBDC4']

# Adicionando o sufixo '.SA' para o padrão Yahoo Finance
my_tickers = list(map(lambda x: x + '.SA', my_tickers_temp))

stocks_data = yf.download(tickers = my_tickers , start = start_date, end = end_date, interval = '1d')

# Eliminando as colunas 'Adj Close' e 'Volume'
stocks_data = stocks_data['Close'].dropna(axis = 0)

print("\n Primeira visualização dos dados crus (cesta de ações brasileiras)")
display(stocks_data.head())
display(stocks_data.info())

# %%
names = list(map(lambda x: 'r_' + x, my_tickers))
stocks_data[names] = stocks_data/stocks_data.shift(periods = 1)

# Algumas colunas vazias podem ser geradas, vamos eliminá-las
stocks_data = stocks_data.dropna(axis = 0)

print('\n Visualizando os dados filtrados (cesta de ações brasileiras)')
display(stocks_data)

# %%
# Gráfico dos retornos 
fig, ax = plt.subplots(nrows = 2, ncols = 1, figsize = (12,6))
ax[0].plot(index_data['r_IBOV'].cumprod(), label = 'IBOV', color = 'blue')
ax[0].set_ylabel('IBOV (retornos)')
ax[0].set_xticks([])
ax[0].set_xlim([10900, 19250])
ax[0].set_yticks(list(range(9)))
ax[0].set_yticklabels(['0', '', '2', '', '4', '', '6', '',''])
ax[1].plot(index_data['r_S&P500'].cumprod(), label = 'S&P500', color = 'red')
ax[1].set_ylabel('S&P500 (retornos)')
ax[1].set_xlim([10900, 19250])
ax[1].set_yticks([0, 0.5, 1, 1.5, 2, 2.5, 3])
ax[1].set_yticklabels(['0', '','1', '','2', '','3'])
ax[1].set_xlabel('Ano')

# ax.secondary_yaxis('right', functions = (lambda x: 3*x/8, lambda x: 8*x/3)).set_ylabel('S&P500 (retornos)')
plt.subplots_adjust(wspace=0, hspace=0)
plt.show()
fig.savefig('brasilian_bascket.png')