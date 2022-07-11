# %%
from matplotlib import ticker
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from datetime import datetime as dt
from datetime import timedelta

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
start_date = '2008-01-01'
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
ax[0].plot(index_data.index.values, index_data['IBOV']/index_data['IBOV'].max(), label = 'IBOV', color = 'blue')
ax[0].set_ylabel('IBOV (normalizado)')

# Aqui, estamos modificando os valores no eixo x. Queremos que o mínimo ocorra 50 dias antes do primeiro registro no dataframe e o máximo ocorra 50 dias dempois. O mesmo para os dois índices.
ax[0].set_xlim([np.datetime64(dt(int(str(index_data.index.values[0])[0:4]), int(str(index_data.index.values[0])[5:7]), int(str(index_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(index_data.index.values[- 1])[0:4]), int(str(index_data.index.values[-1])[5:7]), int(str(index_data.index.values[-1])[8:10])) + timedelta(days = 50))])


ax[1].plot(index_data.index.values, index_data['S&P500']/index_data['S&P500'].max(), label = 'S&P500', color = 'red')
ax[1].set_ylabel('S&P500 (normalizado)')
ax[1].set_xlim([np.datetime64(dt(int(str(index_data.index.values[0])[0:4]), int(str(index_data.index.values[0])[5:7]), int(str(index_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(index_data.index.values[- 1])[0:4]), int(str(index_data.index.values[-1])[5:7]), int(str(index_data.index.values[-1])[8:10])) + timedelta(days = 50))])
# ax[1].set_yticks([0, 0.5, 1, 1.5, 2, 2.5, 3])
# ax[1].set_yticklabels(['0', '','1', '','2', '','3'])
ax[1].set_xlabel('Ano')

# Plotando as áreas sombreadas com os períodos de interece

for i in [0,1]:
    for x in [2008, 2015, 2011, 2020]:
        ax[i].axvspan(index_data.index.values[np.where(index_data.index.year.values == x)[0][0]], index_data.index.values[np.where(index_data.index.year.values == x)[0][-1]], facecolor = 'gray')

# ax.secondary_yaxis('right', functions = (lambda x: 3*x/8, lambda x: 8*x/3)).set_ylabel('S&P500 (retornos)')
plt.subplots_adjust(wspace=0, hspace=0)
plt.show()
fig.savefig('indexes.png')

# %%
# Vamos selecionar um grupo de empresas brasileiras para fazer a otimização de Markowitz
my_tickers_temp = ['PETR4','VALE3', 'ITSA4', 'BBDC4']

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
# Gráficos dos preços das cestas de ações
# Cesta brasileira
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (12,6))
for x in my_tickers:
    ax.plot(stocks_data.index.values, stocks_data[x]/stocks_data[x].max(), label = x[:-3])#, color = 'blue')
ax.set_ylabel('Preços (retornos)')
# ax.set_xticks([])
ax.set_xlim([np.datetime64(dt(int(str(stocks_data.index.values[0])[0:4]), int(str(stocks_data.index.values[0])[5:7]), int(str(stocks_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(stocks_data.index.values[- 1])[0:4]), int(str(stocks_data.index.values[-1])[5:7]), int(str(stocks_data.index.values[-1])[8:10])) + timedelta(days = 50))])
# ax.axvspan(stocks_data.index.values[500], stocks_data.index.values[1200], facecolor='gray')
# ax[0].set_yticks(list(range(9)))
# ax[0].set_yticklabels(['0', '', '2', '', '4', '', '6', '',''])
ax.set_xlabel('Ano')
ax.legend()
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.show()
fig.savefig('brasilian_basket.png')

# %%

# Vamos selecionar um grupo de empresas norte americanas para fazer a otimização de Markowitz
my_tickers_temp = ['GOOG', 'MSFT', 'AMZN', 'COKE']

# Ativos norte americanos não necessitam do sufixo ".SA" para consulta pelo Yahoo Finance
# my_tickers = list(map(lambda x: x + '.SA', my_tickers_temp))

my_tickers= my_tickers_temp

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
# Cesta americana
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (12,6))
for x in my_tickers:
    ax.plot(stocks_data.index.values,stocks_data[x]/stocks_data[x].max(), label = x)#, color = 'blue')
ax.set_ylabel('Preços (retornos)')
ax.set_xlim([np.datetime64(dt(int(str(stocks_data.index.values[0])[0:4]), int(str(stocks_data.index.values[0])[5:7]), int(str(stocks_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(stocks_data.index.values[- 1])[0:4]), int(str(stocks_data.index.values[-1])[5:7]), int(str(stocks_data.index.values[-1])[8:10])) + timedelta(days = 50))])
# ax[0].set_yticks(list(range(9)))
# ax[0].set_yticklabels(['0', '', '2', '', '4', '', '6', '',''])
ax.set_xlabel('Ano')
ax.legend()
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.show()
fig.savefig('usa_basket.png')
