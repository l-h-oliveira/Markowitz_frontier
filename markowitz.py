# %%
from matplotlib import ticker
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import yfinance as yf
from datetime import datetime as dt
from datetime import timedelta

# Faz com que o terminal exiba as tabelas no estilo do Jupyther
from IPython.display import display 

# função para inverter matrizes
from scipy.linalg import inv

# Configurações matplotlib
# plt.rc('text', usetex = True)
# plt.rc('font', **{'family' : "sans-serif"})
# params= {'text.latex.preamble' : [r'\usepackage{amsmath}']}
# plt.rcParams.update(params)


# font1 = {'size': 24,}

# font2 = {'size': 18}

# cálculo a cruvatura da fronteira eficiente (curvatura de uma hipérbole  parametrizada por funções trigonométricas hiperbólicas)
def k(a, b, c, r):
    # 
    mu = -(r*b + 2*c)/(2*r*a)
    sigma = (4*a*c - b**2)*(a*r**2 + b*r + c)/(2*r*a + b)**2

    return (c - b**2/(4*a))(sigma**2 + (a*mu + b/2)**2)**(1.5)

# %%
# Datas de início e fim da análise
start_date = '2008-01-01'
end_date = '2022-05-31'
# Data de hoje: dt.today().strftime('%Y-%m-%d')
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
display(index_data.head())

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
# Agora, vamos calcular o retorno médio e a variância dos retornos de cada um dos índices. Para isso utilizamos as colunas dos retornos já definidas e calculamos o retorno acumulado médio numa janela móvel com período especificado.

period = 50

for x in ['IBOV', 'S&P500']:
    # Calculando a média dos retornos na janela especificada
    index_data['mean_r_' + x] = index_data['r_' + x].cumprod().rolling(period).mean()

    # Calculando a variância dos retornos na janela especificada
    index_data['var_r_' + x] = index_data['r_' + x].cumprod().rolling(period).var()

# %%
# Plots retornos médios e variâncias dos índices

fig, ax = plt.subplots(nrows = 2, ncols = 1, figsize = (12,6))
ax[0].plot(index_data.index.values, index_data['mean_r_IBOV'], label = 'IBOV', color = 'blue')
ax[0].plot(index_data.index.values, index_data['mean_r_S&P500'], label = 'S&P500', color = 'red')
ax[0].set_ylabel(r'$\mu$')
ax[0].legend(loc = 'upper left')
ax[0].set_ylim([0, 3.5])
ax[0].set_yticks(list(np.arange(0,3.5, 1)))

# Aqui, estamos modificando os valores no eixo x. Queremos que o mínimo ocorra 50 dias antes do primeiro registro no dataframe e o máximo ocorra 50 dias dempois. O mesmo para os dois índices.
ax[0].set_xlim([np.datetime64(dt(int(str(index_data.index.values[0])[0:4]), int(str(index_data.index.values[0])[5:7]), int(str(index_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(index_data.index.values[- 1])[0:4]), int(str(index_data.index.values[-1])[5:7]), int(str(index_data.index.values[-1])[8:10])) + timedelta(days = 50))])

ax[1].plot(index_data.index.values, index_data['var_r_IBOV'], label = 'S&P500', color = 'blue')
ax[1].plot(index_data.index.values, index_data['var_r_S&P500'], label = 'S&P500', color = 'red')
ax[1].set_ylabel(r'$\sigma^2$')
ax[1].set_xlim([np.datetime64(dt(int(str(index_data.index.values[0])[0:4]), int(str(index_data.index.values[0])[5:7]), int(str(index_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(index_data.index.values[- 1])[0:4]), int(str(index_data.index.values[-1])[5:7]), int(str(index_data.index.values[-1])[8:10])) + timedelta(days = 50))])
# ax[1].set_yticks([0, 0.5, 1, 1.5, 2, 2.5, 3])
# ax[1].set_yticklabels(['0', '','1', '','2', '','3'])
ax[1].set_xlabel('Ano')
ax[1].set_ylim([0,0.12])
ax[1].set_yticks(list(np.arange(0,0.12, 0.03)))

# # Plotando as áreas sombreadas com os períodos de interece

# for i in [0,1]:
#     for x in [2008, 2015, 2011, 2020]:
#         ax[i].axvspan(index_data.index.values[np.where(index_data.index.year.values == x)[0][0]], index_data.index.values[np.where(index_data.index.year.values == x)[0][-1]], facecolor = 'gray')

# ax.secondary_yaxis('right', functions = (lambda x: 3*x/8, lambda x: 8*x/3)).set_ylabel('S&P500 (retornos)')
ax[1].legend(loc = 'upper left')
plt.subplots_adjust(wspace=0, hspace=0)
plt.show()
fig.savefig('mean_and_var_indexes.png')

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
display(stocks_data.head())

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
# Vamos calcular os retornos e variâncias de cada uma das ações na cesta brasileira

period = 50

for x in my_tickers:
    # Calculando a média dos retornos na janela especificada
    stocks_data['mean_r_' + x] = stocks_data['r_' + x].cumprod().rolling(period).mean()

    # Calculando a variância dos retornos na janela especificada
    stocks_data['var_r_' + x] = stocks_data['r_' + x].cumprod().rolling(period).var()

# %%
# Plots dos retornos e variâncias das ações brasileiras

fig, ax = plt.subplots(nrows = 2, ncols = 1, figsize = (12,6))
for x in my_tickers:
    ax[0].plot(stocks_data.index.values, stocks_data['mean_r_' + x], label = x[:-3])
ax[0].set_ylabel(r'$\mu$')
# ax.set_xticks([])
ax[0].set_xlim([np.datetime64(dt(int(str(stocks_data.index.values[0])[0:4]), int(str(stocks_data.index.values[0])[5:7]), int(str(stocks_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(stocks_data.index.values[- 1])[0:4]), int(str(stocks_data.index.values[-1])[5:7]), int(str(stocks_data.index.values[-1])[8:10])) + timedelta(days = 50))])
# ax.axvspan(stocks_data.index.values[500], stocks_data.index.values[1200], facecolor='gray')
# ax[0].set_yticks(list(range(9)))
# ax[0].set_yticklabels(['0', '', '2', '', '4', '', '6', '',''])
# ax.set_xlabel('Ano')
ax[0].legend(loc = 'upper left')
ax[0].set_yticks(list(np.arange(0,2.5, 0.5)))

for x in my_tickers:
    ax[1].plot(stocks_data.index.values, stocks_data['var_r_' + x], label = x[:-3])
ax[1].set_ylabel(r'$\sigma^2$')
# ax.set_xticks([])
ax[1].set_xlim([np.datetime64(dt(int(str(stocks_data.index.values[0])[0:4]), int(str(stocks_data.index.values[0])[5:7]), int(str(stocks_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(stocks_data.index.values[- 1])[0:4]), int(str(stocks_data.index.values[-1])[5:7]), int(str(stocks_data.index.values[-1])[8:10])) + timedelta(days = 50))])
# ax.axvspan(stocks_data.index.values[500], stocks_data.index.values[1200], facecolor='gray')
# ax[0].set_yticks(list(range(9)))
# ax[0].set_yticklabels(['0', '', '2', '', '4', '', '6', '',''])
# ax.set_xlabel('Ano')
ax[1].set_yticks(list(np.arange(0,0.15, 0.03)))
ax[1].legend(loc = 'upper left')
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.show()
fig.savefig('mean_and_var_brasilian_basket.png')

# %% 
# O último dado relevante para a otimização de portfólios é a correlação entre as ações. A seguir, obtemos a correlação MÉDIA em todo o período entre as ações.

fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (6,5))
sns.heatmap(stocks_data[my_tickers].corr(), annot = True, cmap = 'viridis')
plt.savefig('corr_br.png')

# %%
# Cálculo das fronteiras eficientes em cada janela de tempo

# Primeiramente, inicializamos três colunas no dataframe que irão armazenar os parâmetros a, b e c que definem a fronteira eficiente.

stocks_data[['a', 'b', 'c']] = pd.DataFrame({'a':[], 'b':[], 'c':[]})

# Vamos obter a matriz de correlação entre os ativos em cada janela móvel. Entretanto, o método .corr() do pandas com janela móvel utiliza somente o coeficiente de Pearson ( https://en.wikipedia.org/wiki/Pearson_correlation_coefficient ). Para obter as corelações puras, devemos multiplicar pelos desvios-padrão de cada ativo.

temp0 = stocks_data[my_tickers].rolling(period).corr().dropna()

mean_cols = list(map(lambda x: 'mean_' + x, names))
var_cols = list(map(lambda x: 'var_' + x, names))
vec_ones = np.ones((len(var_cols), 1))

for x in stocks_data.index[period - 1:]:
    # Vetor com os retornos
    mu = np.matrix(stocks_data.loc[x, mean_cols].values).transpose()

    # Obtendo a matriz de correlações
    s = np.sqrt(np.matrix(stocks_data.loc[x, var_cols].values))
    S = np.dot(s.transpose(),s)

    try:
        inv_corr = inv(np.multiply(np.matrix(temp0.loc[x].values) ,S))

        # Obtendo os parâmetros da fronteira eficiente
        R11 = (mu.transpose()@inv_corr@mu)[0,0]
        R12 = (mu.transpose()@inv_corr@vec_ones)[0,0]
        R22 = (vec_ones.transpose()@inv_corr@vec_ones)[0,0]

        d = R11*R22 - R12**2

        stocks_data.loc[x, ['a', 'b', 'c']] = R22/d, -2*R12/d, R11/d
    except:
        # Examinando os registros em que a matriz de correlação é singular ou d = 0 (os únicos problemas que podem emergir aqui)
        print(x)
        continue

# Para obtermos o portfólio otimizado em relação ao Sharpe-ratio, precisamos do valor da taxa livre de risco naquele período. Vamos utilizar como de costume, a taxa selic

# %%
selic_data = pd.read_csv('consulta_selic_b3.txt', sep='	', decimal=',')

# Transformando as dadas de texto para datetime
selic_data['Date'] = pd.to_datetime(selic_data['Data'], dayfirst= True, yearfirst=True)

selic_data = selic_data.drop(columns= 'Data')

# Agora, vamos juntar os dados de preço de ações com os dados da taxa selic

full_data = pd.merge(stocks_data[['a', 'b', 'c']], selic_data, on = 'Date', how = 'left')

full_data = full_data.set_index('Date')

# queremos calcular o retorno da taxa selic ao longo da nossa janela de tempo. Para isso, vamos calcular o produto cumulativo de (1 + x/100) com x sendo o respectivo retorno diário da taxa selic 
full_data['SELIC_daylly'] = full_data['Taxa SELIC'].apply(lambda x: (1 + x/100)**(1/365))

full_data['r_SELIC'] = full_data['SELIC_daylly'].rolling(window = period).apply(np.prod)

# %%
# plot evolução da taxa selic anual
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (12,6))

ax.plot(full_data.index.values, full_data['Taxa SELIC'].values, color = 'blue', linewidth = 3)
# for x in [2008, 2015, 2011, 2020]:
#         ax.axvspan(index_data.index.values[np.where(index_data.index.year.values == x)[0][0]], index_data.index.values[np.where(index_data.index.year.values == x)[0][-1]], facecolor = 'gray')
ax.set_ylabel(r'$r (\%  \ Ano)$')
ax.set_xlim([np.datetime64(dt(int(str(full_data.index.values[0])[0:4]), int(str(full_data.index.values[0])[5:7]), int(str(full_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(full_data.index.values[- 1])[0:4]), int(str(full_data.index.values[-1])[5:7]), int(str(full_data.index.values[-1])[8:10])) + timedelta(days = 50))])
# ax.set_ylim([0, 1])
ax.set_xlabel('Ano')
# ax.legend()
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.show()
fig.savefig('selic_br.png')

# %%
# Exemplo de fronteira eficiente com ativos marcados no plano "Sharpe"

# obtendo a alocação do portfólio eficiente no último dia do registro
m = full_data.iloc[-1, 6]
l1 = R22*m/d - R12/d
l2 = -R12*m/d + R11/d

alpha = l1*inv_corr@stocks_data.loc[stocks_data.index[-1], mean_cols].values + l2*inv_corr@np.ones(len(my_tickers))

# plotando os ativos no plano e exibindo a fronteira eficiente




# %%
# cálculo da cruvatura no ponto inicial da parametrização, t = 0

full_data['k1'] = full_data['a']/np.sqrt(full_data['c'] - full_data['b']**2/full_data['a']/4)

# cálculo da curvatura no ponto em que o retorno do ponto na fronteira eficiente é nulo, vértice da hipérbole

full_data['k2'] = (full_data['a']*full_data['c'] - full_data['b']**2/4)/((4*full_data['a']*full_data['c'] + full_data['b']**2)/(4*full_data['a']) +  full_data['b']**2/4)


# cálculo do retorno e variância do portfólio eficiente
full_data['r_ef'] = -(full_data['r_SELIC']*full_data['b'] + 2*full_data['c'])/(2*full_data['r_SELIC']*full_data['a'] + full_data['b'])

full_data['var_ef'] = (4*full_data['a']*full_data['c'] - full_data['b']**2)*(full_data['a']*full_data['r_SELIC']**2 + full_data['b']*full_data['r_SELIC'] + full_data['c'])/(2*full_data['r_SELIC']*full_data['a'] + full_data['b'])**2

# cálculo da curvatura da hipérbole no portfólio eficiente
full_data['k3'] = (full_data['a']*full_data['c'] - full_data['b']**2/4)/(full_data['var_ef'] + (full_data['a']*full_data['r_ef'] + full_data['b']/2)**2)**(3/2)

full_data = full_data.dropna()
# %%
# Plot  curvatura, cesta brasileira
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (12,6))

ax.plot(full_data.index.values, np.abs(full_data['k'].values)/500, color = 'blue')
for x in [2008, 2015, 2011, 2020]:
        ax.axvspan(index_data.index.values[np.where(index_data.index.year.values == x)[0][0]], index_data.index.values[np.where(index_data.index.year.values == x)[0][-1]], facecolor = 'gray')
ax.axhline(0.4)
ax.set_ylabel(r'Curvatura,  $k(\sigma, \mu)$')
ax.set_xlim()
ax.set_ylim([0, 1])
ax.set_xlabel('Ano')
# ax.legend()
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.show()
fig.savefig('k_br_basket.png')













































































# %%

# Vamos selecionar um grupo de empresas norte americanas para fazer a otimização de Markowitz
my_tickers_temp = ['GOOG', 'MSFT', 'AMZN', 'COKE']

# Ativos norte americanos não necessitam do sufixo ".SA" para consulta pelo Yahoo Finance
# my_tickers = list(map(lambda x: x + '.SA', my_tickers_temp))

my_tickers = my_tickers_temp

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
display(stocks_data.head())



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


# %%
# Vamos calcular os retornos e variâncias de cada uma das ações na cesta brasileira

period = 50

for x in my_tickers:
    # Calculando a média dos retornos na janela especificada
    stocks_data['mean_r_' + x] = stocks_data['r_' + x].cumprod().rolling(period).mean()

    # Calculando a variância dos retornos na janela especificada
    stocks_data['var_r_' + x] = stocks_data['r_' + x].cumprod().rolling(period).var()

# %%
# Plots dos retornos e variâncias das ações americanas

fig, ax = plt.subplots(nrows = 2, ncols = 1, figsize = (12,6))
for x in my_tickers:
    ax[0].plot(stocks_data.index.values, stocks_data['mean_r_' + x], label = x)
ax[0].set_ylabel(r'$\mu$')
# ax.set_xticks([])
ax[0].set_xlim([np.datetime64(dt(int(str(stocks_data.index.values[0])[0:4]), int(str(stocks_data.index.values[0])[5:7]), int(str(stocks_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(stocks_data.index.values[- 1])[0:4]), int(str(stocks_data.index.values[-1])[5:7]), int(str(stocks_data.index.values[-1])[8:10])) + timedelta(days = 50))])
# ax.axvspan(stocks_data.index.values[500], stocks_data.index.values[1200], facecolor='gray')
# ax[0].set_yticks(list(range(9)))
# ax[0].set_yticklabels(['0', '', '2', '', '4', '', '6', '',''])
# ax.set_xlabel('Ano')
ax[0].legend(loc = 'upper left')
# ax[0].set_yticks(list(np.arange(0,2.5, 0.5)))

for x in my_tickers:
    ax[1].plot(stocks_data.index.values, stocks_data['var_r_' + x], label = x)
ax[1].set_ylabel(r'$\sigma^2$')
# ax.set_xticks([])
ax[1].set_xlim([np.datetime64(dt(int(str(stocks_data.index.values[0])[0:4]), int(str(stocks_data.index.values[0])[5:7]), int(str(stocks_data.index.values[0])[8:10])) - timedelta(days = 50)), np.datetime64(dt(int(str(stocks_data.index.values[- 1])[0:4]), int(str(stocks_data.index.values[-1])[5:7]), int(str(stocks_data.index.values[-1])[8:10])) + timedelta(days = 50))])
# ax.axvspan(stocks_data.index.values[500], stocks_data.index.values[1200], facecolor='gray')
# ax[0].set_yticks(list(range(9)))
# ax[0].set_yticklabels(['0', '', '2', '', '4', '', '6', '',''])
# ax.set_xlabel('Ano')
# ax[1].set_yticks(list(np.arange(0,0.15, 0.03)))
ax[1].legend(loc = 'upper left')
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.show()
fig.savefig('mean_and_var_usa_basket.png')

# %% 
# O último dado relevante para a otimização de portfólios é a correlação entre as ações. A seguir, obtemos a correlação MÉDIA em todo o período entre as ações.

fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (6,5))
sns.heatmap(stocks_data[my_tickers].corr(), annot = True, cmap = 'viridis')
plt.savefig('corr_us.png')

# %%
