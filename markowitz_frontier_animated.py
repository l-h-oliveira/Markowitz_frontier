# %%
from matplotlib import ticker
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import yfinance as yf
from datetime import datetime as dt
from datetime import timedelta
from matplotlib.animation import FuncAnimation

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
# importando dados
full_data = pd.read_csv('full_data_br.csv')

#convertendo o índice no tipo datetime64
full_data['Date'] = pd.to_datetime(full_data['Date'], dayfirst= True, yearfirst=True)

full_data = full_data.set_index('Date')

# importando dados
stocks_data = pd.read_csv('stocks_data_br.csv')

#convertendo o índice no tipo datetime64
stocks_data['Date'] = pd.to_datetime(stocks_data['Date'], dayfirst= True, yearfirst=True)

stocks_data = stocks_data.set_index('Date')

# %%

# TODO fazer função que plot a fronteira eficiente
# TODO chamar a função dentro de um loop no dataframe fulldata
# TODO coletar na forma de um vídeo

# %%
# definições
my_tickers = list(filter(lambda x: 'r_' not in x, stocks_data.columns))
mean_cols = list(filter(lambda x: x[:4] == 'mean', stocks_data.columns))
var_cols = list(filter(lambda x: x[:3] == 'var', stocks_data.columns))

p = -1
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (12,6))
ax.set_xlabel(r'$\sigma$', fontdict = font1)
ax.set_ylabel(r'$\mu$', fontdict = font1)

def fronteira(p):
    a = full_data.index[p]

    ### obtendo a fronteira eficiente usando as parametrizações.

    # Obtendo os valores extremos do parâmetro t
    t_max = np.arccosh(np.sqrt(stocks_data.loc[a, var_cols].values).max()/np.sqrt(full_data.loc[a, 'c'] - full_data.loc[a, 'b']**2/4/full_data.loc[a, 'a']))

    # definindo o parâmetro t
    t = np.linspace(0, t_max, 100)

    # calculando as componentes da fronteira eficiente (metade superior e inferior)
    var = np.sqrt(full_data.loc[a, 'c'] - full_data.loc[a, 'b']**2/4/full_data.loc[a, 'a'])*np.cosh(t)

    mu_p = np.sqrt(full_data.loc[a, 'c'] - full_data.loc[a, 'b']**2/4/full_data.loc[a, 'a'])/np.sqrt(full_data.loc[a, 'a'])*np.sinh(t) - full_data.loc[a, 'b']/2/full_data.loc[a, 'a']

    mu_n = np.sqrt(full_data.loc[a, 'c'] - full_data.loc[a, 'b']**2/4/full_data.loc[a, 'a'])/np.sqrt(full_data.loc[a, 'a'])*np.sinh(-t) - full_data.loc[a, 'b']/2/full_data.loc[a, 'a']

    # Fronteira Eficiente
    ax.plot(var, mu_n, color = 'black', linewidth = 3)
    ax.plot(var, mu_p, color = 'black', linewidth = 3)
    # ax.fill_between(var, mu_n, mu_p, facecolor = 'lightgray')

    #reta Sharpe
    t2 = np.linspace(0, 5, 100)
    ax.cla()
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

    # ax.axhline(0, color = 'gray')
    ax.legend(loc = 'upper left')
    ax.set_xlim(0, var.max() + 0.005)
    ax.set_ylim(mu_n.min(), mu_p.max())
    ax.spines['bottom'].set_position('zero') #colocando eixo x sobre 0
    print(mu_n[0])
    return ax,

plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
plt.subplots_adjust(wspace = 0, hspace = 0)

animation = FuncAnimation(fig, func = fronteira, frames = range(20), interval = 500)
plt.show()
# animation.save('br_frontier.mp4')

# %%
