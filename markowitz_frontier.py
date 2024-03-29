# %%
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
plt.rc('text', usetex = True)
plt.rc('font', **{'family' : "sans-serif"})
params= {'text.latex.preamble' : [r'\usepackage{amsmath}']}
plt.rcParams.update(params)


font1 = {'size': 24}

font2 = {'size': 18}

# %%
# Cálculo das fronteiras eficientes em cada janela de tempo

# Primeiramente, inicializamos três colunas no dataframe que irão armazenar os parâmetros a, b e c que definem a fronteira eficiente.

# importando dados
period = 50
stocks_data = pd.read_csv('stocks_data_br.csv')
#convertendo o índice no tipo datetime64
stocks_data['Date'] = pd.to_datetime(stocks_data['Date'], dayfirst= True, yearfirst=True)
stocks_data = stocks_data.set_index('Date')

index_data = pd.read_csv('index_data.csv')
index_data['Date'] = pd.to_datetime(index_data['Date'], dayfirst= True, yearfirst=True)
index_data = index_data.set_index('Date')

# %% 
# Para obtermos o portfólio otimizado em relação ao Sharpe-ratio, precisamos do valor da taxa livre de risco naquele período. Vamos utilizar como de costume, a taxa selic

# Obtendo dados da taxa livre de risco
full_data = pd.read_csv('consulta_selic_b3.txt', sep='	', decimal=',')

# Transformando as dadas de texto para datetime
full_data['Date'] = pd.to_datetime(full_data['Data'], dayfirst= True, yearfirst=True)

full_data = full_data.drop(columns= 'Data')
full_data = full_data.set_index('Date')

# queremos calcular o retorno da taxa selic ao longo da nossa janela de tempo. Para isso, vamos calcular o produto cumulativo de (1 + x/100) com x sendo o respectivo retorno diário da taxa selic 
full_data['SELIC_daylly'] = full_data['Taxa SELIC'].apply(lambda x: (1 + x/100)**(1/365))

# note que o retorno da taxa Selic está acrescido de 1, pois estamos trabalhando com a fórmula de juros compostos
full_data['r_SELIC'] = full_data['SELIC_daylly'].rolling(window = period).apply(np.prod) - 1

full_data[['a', 'b', 'c', 'aloc']] = pd.DataFrame({'a':[], 'b':[], 'c':[], 'aloc':[]})

# %%
#variáveis de configuração
my_tickers = list(filter(lambda x: 'r_' not in x, stocks_data.columns))

names = list(map(lambda x: 'r_' + x, my_tickers))

temp0 = stocks_data[my_tickers].rolling(period).corr().dropna()

mean_cols = list(map(lambda x: 'mean_' + x, names))
var_cols = list(map(lambda x: 'var_' + x, names))
vec_ones = np.ones((len(var_cols), 1))

print('\n' + 25*'=')
regs = 0
print('Registros com determinante nulo\n')
for x in stocks_data.index[period - 1:]:
    # Vetor com os retornos
    mu = np.matrix(stocks_data.loc[x, mean_cols].values).transpose()

    # Vamos obter a matriz de correlação entre os ativos em cada janela móvel. Entretanto, o método .corr() do pandas com janela móvel utiliza somente o coeficiente de Pearson ( https://en.wikipedia.org/wiki/Pearson_correlation_coefficient ). Para obter as corelações puras, devemos multiplicar pelos desvios-padrão de cada ativo.
    s = np.sqrt(np.matrix(stocks_data.loc[x, var_cols].values))
    S = np.dot(s.transpose(),s)

    try:
        inv_corr = inv(np.multiply(np.matrix(temp0.loc[x].values) ,S))

        # Obtendo os parâmetros da fronteira eficiente
        R11 = (mu.transpose()@inv_corr@mu)[0,0]
        R12 = (mu.transpose()@inv_corr@vec_ones)[0,0]
        R22 = (vec_ones.transpose()@inv_corr@vec_ones)[0,0]

        d = R11*R22 - R12**2

        full_data.loc[x, ['a', 'b', 'c']] = R22/d, -2*R12/d, R11/d

        # retorno do portfólio eficiente e multiplicadores de Lagrange
        r = full_data.loc[x, 'r_SELIC']
        m = -(r*full_data.loc[x, 'b'] + 2*full_data.loc[x, 'c'])/(2*r*full_data.loc[x, 'a'] + full_data.loc[x, 'b'])
        l1 = R22*m/d - R12/d
        l2 = -R12*m/d + R11/d

        # obtendo a alocação do portfólio eficiente
        alpha = l1*inv_corr@stocks_data.loc[x, mean_cols].values + l2*inv_corr@np.ones(len(my_tickers))

        # Salvaando alocações no DataFrame
        full_data.loc[x, 'aloc'] = str(alpha.round(2))

    except:
        # Examinando os registros em que a matriz de correlação é singular ou d = 0 (os únicos problemas que podem emergir aqui)
        print(x)
        regs += 1
        continue

print('\n{} registros com determinante nulo'.format(regs))
print(25*'=' + '\n')

# %%
# cálculo da cruvatura no vértice direito da hipérbole, t = 0

full_data['k1'] = full_data['a']/np.sqrt(full_data['c'] - full_data['b']**2/full_data['a']/4)

# cálculo da curvatura no ponto em que o retorno do ponto na fronteira eficiente é nulo, ou seja, ponto em que a hipérbole cruza o eixo do desvio-padrão

full_data['k3'] = (full_data['a']*full_data['c'] - full_data['b']**2/4)/((full_data['c'] +  full_data['b']**2/4)**(3/2))


# cálculo do retorno e variância do portfólio eficiente
full_data['r_ef'] = -(full_data['r_SELIC']*full_data['b'] + 2*full_data['c'])/(2*full_data['r_SELIC']*full_data['a'] + full_data['b'])

full_data['var_ef'] = (4*full_data['a']*full_data['c'] - full_data['b']**2)*(full_data['a']*full_data['r_SELIC']**2 + full_data['b']*full_data['r_SELIC'] + full_data['c'])/(2*full_data['r_SELIC']*full_data['a'] + full_data['b'])**2

# cálculo da curvatura da hipérbole no portfólio eficiente
full_data['k2'] = (full_data['a']*full_data['c'] - full_data['b']**2/4)/(full_data['var_ef'] + (full_data['a']*full_data['r_ef'] + full_data['b']/2)**2)**(3/2)

full_data = full_data.dropna()
full_data.to_csv('full_data.csv')

# %%
# Plot  curvatura, cesta brasileira
for y in ['k1', 'k2', 'k3']:
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (12,6))

    ax.plot(full_data.index.values, np.abs(full_data[y].values), color = 'blue')
    for x in [2008, 2015, 2011, 2020]:
            ax.axvspan(index_data.index.values[np.where(index_data.index.year.values == x)[0][0]], index_data.index.values[np.where(index_data.index.year.values == x)[0][-1]], facecolor = 'gray')
    # ax.axhline(0.4)
    ax.set_ylabel(r'Curvatura,  $k_' + y[1] + '(\sigma, \mu)$')
    ax.set_xlim()

    # ax.set_ylim([0, 1])
    ax.set_xlabel('Ano')
    # ax.legend()
    plt.subplots_adjust(wspace = 0, hspace = 0)
    plt.show()
    fig.savefig(y + '_br_basket.png')


# %%
# Exemplo de fronteira eficiente com ativos marcados no plano "Sharpe" (estamos realizando este cálculo aqui, para coletar o último valor válido das curvaturas)

# obtendo a alocação do portfólio eficiente no último dia do registro

# coletanto o índice do último registro válido das curvaturas
a = full_data.index[-1]

### obtendo a fronteira eficiente usando as parametrizações.

# Obtendo os valores extremos do parâmetro t
t_max = np.arccosh(np.sqrt(stocks_data.loc[a, var_cols].values).max()/np.sqrt(full_data.loc[a, 'c'] - full_data.loc[a, 'b']**2/4/full_data.loc[a, 'a']))

# definindo o parâmetro t
t = np.linspace(0, t_max, 100)

# calculando as componentes da fronteira eficiente (metade superior e inferior)
var = np.sqrt(full_data.loc[a, 'c'] - full_data.loc[a, 'b']**2/4/full_data.loc[a, 'a'])*np.cosh(t)

mu_p = np.sqrt(full_data.loc[a, 'c'] - full_data.loc[a, 'b']**2/4/full_data.loc[a, 'a'])/np.sqrt(full_data.loc[a, 'a'])*np.sinh(t) - full_data.loc[a, 'b']/2/full_data.loc[a, 'a']

mu_n = np.sqrt(full_data.loc[a, 'c'] - full_data.loc[a, 'b']**2/4/full_data.loc[a, 'a'])/np.sqrt(full_data.loc[a, 'a'])*np.sinh(-t) - full_data.loc[a, 'b']/2/full_data.loc[a, 'a']


# %%
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (12,6))

# Fronteira Eficiente
ax.plot(var, mu_n, color = 'black', linewidth = 3)
ax.plot(var, mu_p, color = 'black', linewidth = 3)
ax.fill_between(var, mu_n, mu_p, facecolor = 'lightgray')

#reta Sharpe
t2 = np.linspace(0,5, 100)
ax.plot(np.sqrt(full_data.loc[a, 'var_ef'])*t2, (full_data.loc[a, 'r_ef'] - full_data.loc[a, 'r_SELIC'])*t2 + full_data.loc[a, 'r_SELIC'], 'g', linestyle = 'dashed', linewidth = 4)


# ponto portfólio eficiente
ax.plot(np.sqrt(full_data.loc[a, 'var_ef']), full_data.loc[a, 'r_ef'], 'ok', markersize = 15)

# ativo livre de risco
ax.plot(0, full_data.loc[a, 'r_SELIC'], 'o', markersize = 15, color = 'purple')

# carregando alocação
aloc = list(map(float, filter(lambda x: x!= '', full_data.loc[a, 'aloc'][1:-1].split(' '))))
# ativos na cesta
u = ''
for i in range(len(my_tickers)):
    ax.plot(np.sqrt(stocks_data.loc[a, var_cols[i]]), stocks_data.loc[a, mean_cols[i]], 'o', markersize = 15, label = my_tickers[i][:-3])

    # Alocação
    u = u + '(' + str(aloc[i]) + ')' + my_tickers[i][:-3] + ' + '

ax.text(0.005, mu_n.min(), r'$\alpha \approx' + u[:-3] + '$', fontdict = {'size': 15})

# Data
ax.text(0.005, mu_n.min() + 0.3, r'$' + a.strftime('%d/%m/%Y') + '$', fontdict = {'size': 15})

ax.axhline(0, color = 'gray')
ax.set_xlabel(r'$\sigma$', fontdict = font1)
ax.set_ylabel(r'$\mu$', fontdict = font1)
ax.set_xlim(0, var.max() + 0.005)
ax.set_ylim(mu_n.min(), mu_p.max())
ax.spines['bottom'].set_position('zero') #colocando eixo x sobre 0
ax.legend()
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.show()
fig.savefig('ef_br.png')

# %%
