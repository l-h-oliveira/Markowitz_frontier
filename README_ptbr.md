<img src="https://render.githubusercontent.com/render/math?math=e^{i \pi} = -1">

# Otimização de Portifólios de Markowitz

## Objetivos
- Recolher dados históricos de dois índices (S&P500 e IBOV) para detectarmos períodos de movimentações abruptas;
- Escolher 4 ações de empresas pertencentes a cada um dos índices e calcular os retornos ao longo do tempo e as respectivas variâncias;
- Aplicar o processo de otimização às duas cestas de ativos; exibir o retorno do postifólio otimizado;
- Exibir a fronteira eficiente
- Calcular a curvatura da fronteira eficiente sobre o portifólio eficiente;
- A curvatura sobre o portifólio eficiente pode ser útil como indicativo de períodos de mudanças abrubtas?
- Apêndice A: breve comentário sobre as duas implementações da otimização. A primeira fixa o retorno e minimiza a variância; e a segunda fixa a variância e maximiza o retorno;
- Apêndice B: curvatura de uma hipérbole

## Dados Histórios S&P500 e IBOV

## Cestas de Ativos

### Google, Mycrosoft, Amazon, Meta

### Petrobrás, Vale, Itaú, Bradesco

## Portifólios Otimizados

## A Fronteira Eficiente e a Curvatura

## Apêndice A: Otimização de Portifólios de Markowitz
Um portfólio é definido através de um conjunto de ativos $A_1, A_2, ... , A_N$ e a respectiva alocação (percentual) $\alpha_1, \alpha_2, ... , \alpha_N$. Desse modo, $\alpha_1~+~\alpha_2~+~\cdots~+~\alpha_N~=~1$.

Então, **retorno do portfólio** $(\mu)$ é dado pela média ponderada dos retornos individuais

$$\mu = \alpha_1\mu_1 + \alpha_2\mu_2 + \cdots \alpha_N\mu_N,$$

onde $\mu_i$ é o retorno do ativo $A_i$. 

E a variância? A **variância do portfólio** $(\sigma^2)$ também pode ser escrita utilizando-se as variâncias dos ativos $(\sigma_i^2)$. Entretando, temos um momento de segunda ordem, por isso temos a influência de correlações entre os ativos. De forma geral, podemos escrever a variância do portfólio combinado como 

$$ \sigma^2 = \vec{\alpha}^t \Sigma \vec{\alpha},$$

onde $\Sigma$ é a **matriz de correlação** entre os ativos. Ela é dada por

$$ \Sigma = \begin{pmatrix}\sigma_1^2 & \rho_{12} & \cdots & \rho_{1N} \\ \rho_{12} & \sigma_2^2 & \cdots & \rho_{2N} \\ \vdots & \vdots & \ddots & \vdots \\ \rho_{1N} & \rho_{2N} & \cdots & \sigma_N^2  \end{pmatrix}. $$

Os elementos na diagonal principal de $\Sigma$ são as variâncias dos ativos $(\sigma_i^2)$. Já os termos fora da diagonal $(\rho_{ij})$ representam correlações entre os ativos. Por exemplo, suponha que o preço do ativo $A_1$ sobe, se o preço do ativo $A_2$ também sobe, eles têm **correlação positiva** $(\rho_{12}>0)$, ao passo que se o preço ativo $A_2$ cai, eles têm **correlação negativa** $(\rho_{12}<0)$. 

Se os ativos não têm correlação, temos $\rho_{12} = 0$. E a variância do portfólio pode ser escrita de maneira muito simples

$$ \sigma^2 = \alpha_1^2\sigma_1^2 + \alpha_2^2\sigma_2^2 + \cdots + \alpha_N^2\sigma_N^2.$$

Podemos formular dois problemas de otimização. Nos dois casos, o intuito é encontrar as alocações $(\alpha_1, \alpha_2, ..., \alpha_N)$ que satisfazem as condições. São eles
1. Maximizar o retorno $ \alpha_1\mu_1 + \alpha_2\mu_2 + \cdots \alpha_N\mu_N $ e fixar a variância, ou seja, temos $ \vec{\alpha}^t \Sigma \vec{\alpha} = \sigma_0^2 $;

2. Minimizar a variância $ \vec{\alpha}^t \Sigma \vec{\alpha} $ e fixar um retorno $ \alpha_1\mu_1 + \alpha_2\mu_2 + \cdots \alpha_N\mu_N = \mu_0 $.

Nos dois caso, ainda temos $`\alpha_1~+~\alpha_2~+~\cdots~+~\alpha_N~=~1`$.


## Apêndice B: A Curvatura de uma Hipérbole

$$\sum_{n = 0}^\infty $$