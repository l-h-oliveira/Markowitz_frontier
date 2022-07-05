# Otimização de Portfólios de Markowitz [problemas com LaTex e MarkDown]
## Objetivos
- Recolher dados históricos de dois índices (S&P500 e IBOV) para detectarmos períodos de movimentações abruptas;
- Escolher 4 ações de empresas pertencentes a cada um dos índices e calcular os retornos ao longo do tempo e as respectivas variâncias;
- Aplicar o processo de otimização às duas cestas de ativos; exibir o retorno do postifólio otimizado;
- Exibir a fronteira eficiente
- Calcular a curvatura da fronteira eficiente sobre o portifólio eficiente;
- A curvatura sobre o portifólio eficiente pode ser útil como indicativo de períodos de mudanças abrubtas?
- Apêndice A (detalhamento matemático): breve comentário sobre as duas implementações da otimização. A primeira fixa o retorno e minimiza a variância; e a segunda fixa a variância e maximiza o retorno;
- Apêndice B (detalhamento matemático): curvatura de uma hipérbole

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

onde $\Sigma$ é a **matriz de correlação** entre os ativos (nessa notação, $\vec{\alpha}$ é um vetor coluna e $\vec{\alpha}^t$ o seu transposto, um vetor linha). Ela é dada por

$$ \Sigma = \begin{pmatrix}\sigma_1^2 & \rho_{12} & \cdots & \rho_{1N} \\ \rho_{12} & \sigma_2^2 & \cdots & \rho_{2N} \\ \vdots & \vdots & \ddots & \vdots \\ \rho_{1N} & \rho_{2N} & \cdots & \sigma_N^2  \end{pmatrix}. $$

Os elementos na diagonal principal de $\Sigma$ são as variâncias dos ativos $(\sigma_i^2)$. Já os termos fora da diagonal $(\rho_{ij})$ representam correlações entre os ativos. Por exemplo, suponha que o preço do ativo $A_1$ sobe, se o preço do ativo $A_2$ também sobe, eles têm **correlação positiva** $(\rho_{12}>0)$, ao passo que se o preço ativo $A_2$ cai, eles têm **correlação negativa** $(\rho_{12}<0)$. 

Se os ativos não têm correlação, temos $\rho_{12} = 0$. E a variância do portfólio pode ser escrita de maneira muito simples

$$ \sigma^2 = \alpha_1^2\sigma_1^2 + \alpha_2^2\sigma_2^2 + \cdots + \alpha_N^2\sigma_N^2.$$

Podemos formular dois problemas de otimização. Nos dois casos, o intuito é encontrar as alocações $(\alpha_1, \alpha_2, ..., \alpha_N)$ que satisfazem as condições. São eles
1. Maximizar o retorno $ \alpha_1\mu_1 + \alpha_2\mu_2 + \cdots \alpha_N\mu_N $ e fixar a variância, ou seja, temos $\vec{\alpha}^t \Sigma \vec{\alpha} = \sigma_0^2 $;

2. Minimizar a variância $ \vec{\alpha}^t \Sigma \vec{\alpha} $ e fixar um retorno $ \alpha_1\mu_1 + \alpha_2\mu_2 + \cdots \alpha_N\mu_N = \mu_0 $.

Nos dois caso, ainda temos $\alpha_1~+~\alpha_2~+~\cdots~+~\alpha_N~=~1$.

Vamos nos concentrar no segundo caso. Vamos procurar os pontos extremos da seguinte lagrangiana

$$ \mathcal{L} = \frac{1}{2}\vec{\alpha}^t \Sigma \vec{\alpha} + \lambda_1 \left(\mu_0 - \vec{\alpha}^t\mu  \right) + \lambda_2\left(1 - \vec{\alpha}^t\vec{1}\right), $$

onde $\lambda_1$ está relacionado com o vínculo da variância fixada e $\lambda_2$ está relacionado com o vínculo de que as alocações somam $1$ e $\vec{1}$ é o vetor coluna com todos os elementos iguais a $1$. Para isso, calculamos a derivada em relação a $\alpha_k$ e igualamos a zero. A equação obtida é uma componente da seguinte equação vetorial
$$ \Sigma \vec{\alpha} - \lambda_1 \vec{\mu} - \lambda_2\vec{1} = 0.$$

De onde obtemos
$$  \vec{\alpha} =  \lambda_1 \Sigma^{-1}\vec{\mu} + \lambda_2\Sigma^{-1}\vec{1} = 0.$$

Resta determinar $\lambda_1$ e $\lambda_2$. Vamos utilizar as equações de vínculo para obter duas equações e resolver os sistema linear.

$$\mu_0 = \vec{\alpha}^t \vec{\mu} = \lambda_1\vec{\mu}^t\Sigma^{-1}\mu + \lambda_2 \vec{\mu}^t\Sigma^{-1}\vec{1} $$

$$1 = \vec{\alpha}^t\vec{1}= \lambda_1 \vec{\mu}^t\Sigma^{-1}\vec{1} + \lambda_2\vec{1}^t\Sigma^{-1}\vec{1}.$$

Na forma matricial,
$$ \begin{pmatrix}\vec{\mu}^t\Sigma^{-1}\mu & \vec{\mu}^t\Sigma^{-1}\vec{1} \\ \vec{\mu}^t\Sigma^{-1}\vec{1} & \vec{1}^t\Sigma^{-1}\vec{1} \end{pmatrix}\begin{pmatrix} \lambda_1 \\ \lambda_2 \end{pmatrix} = \begin{pmatrix} \mu_0 \\ 1 \end{pmatrix}.$$

Note que se conhecemos $\alpha$ podemos obter a variância do portifólio, $ \sigma^2 = \vec{\alpha}^t \Sigma \vec{\alpha}$, em função de um retorno $\mu_0$ fixado. Dessa forma, obtemos uma curva no plano $\mu \times \sigma$, a **fronteira eficiente**. Pode-se mostrar que essa curva é um hipérbole e que encapsula todos os pontos que representam os ativos que compõem o portfólio.

## Apêndice B: A Curvatura de uma Hipérbole

Conforme discutimos no Apêndice A, a fronteira eficiente tem a forma de uma hipérbole no plano $\mu \times \sigma$, que podemos expressar por

$$ \sigma^2 = a\mu^2 + b\mu + c, \textrm{com } a \neq 0.$$

Para obter a curvatura dessa curva, primeiro devemos obter uma **parametrização** da mesma. Ou seja, duas funções de um mesmo parâmetro, $t$, que fornecem um ponto da curva, $\left( \mu\left(t\right), \sigma\left(t\right)\right)$. Utilizando as funções trigonométricas, podemos definir

$$ \begin{cases} \mu(t) = \sqrt{\frac{c}{a} - \frac{b^2}{4a^2}}\sinh (t) - \frac{b}{2a} \\ \sigma(t) = \sqrt{c - \frac{b^2}{4a}}\cosh (t)\end{cases}.$$

Sabendo que $\cosh^2 (t) - \sinh^2 (t) = 1$, a equação da fronteira eficiente é naturalmente satisfeita. Temos portanto uma parametrização.

Nosso interesse é agora calcular a **curvatura** ao longo da curva. De forma geral, a expressão é um tanto extensa

$$k(t) = \frac{\mu^\prime\sigma^{\prime\prime} - \mu^{\prime\prime}\sigma^\prime}{\left(\left(\mu^\prime)^2 \right) + \left(\sigma^\prime \right)^2 \right)^{\frac{3}{2}}}, $$

onde $\mu^\prime$ é a primeira derivada de $\mu$ em relação a $t$ e $\mu^{\prime\prime}$ é a segunda derivada em relação a $t$, analogamente para $\sigma^\prime$ e $\sigma^{\prime\prime}$.

Felizmente as derivadas das funções trigonométricas hiperbólicas possuem relações recorrentes. Isto nos permite simplificar enormemente a expressão da curvatura

$$k(t)= \frac{a}{d} \left(\cosh^2(t) + a\sinh^2(t)\right)^{-\frac{3}{2}}.$$

Mais ainda, podemos expressar a curvatura em termos de $\mu$ e $\sigma$

$$k(\mu, \sigma) = \frac{c - \frac{b^2}{4a}}{\left(\sigma^2 + \left(a\mu + \frac{b}{2}\right)^2\right)^{\frac{3}{2}}}.$$