 # -*- coding: utf-8 -* -
"""
Created on Sun May  7 17:05:07 2023

@author: leona
"""

import yfinance as yf
import numpy as np
import matplotlib.pyplot as fig
import statistics as s
import matplotlib.mlab as m
import math 


# Definindo a ação desejada
ticker_symbol = "VALE3.SA"


# Baixando os dados do ativo
ticker = yf.Ticker(ticker_symbol)

# Baixando os dados históricos no intervalo desejado
df = ticker.history(start="2023-01-01", end="2024-02-15")

df=df.drop(['High','Low',"Open","Volume","Dividends", "Stock Splits"],axis =1)


#Calculo coluna retorno 
retorno= df['retorno']= df['Close'].pct_change(1)
print(retorno)
df['retorno']=retorno.tolist()

#Calculo coluna Close
df['Close']=df['Close'].values
print(df['Close'])

#Calculo coluna momento
x=df['Close'].values
dif= x[8:]-x[0:-8]

df=df.drop(df.index[0:8])
df['momento']=dif.tolist()
print(df['momento'])

#Calculo coluna momento(%)
dff= df['momento(%)']=df['momento'].rolling(window=3).mean()/df['Close']
print(df['momento(%)'])
df['momento(%)']=dff.tolist()
print(df['momento'])
df=df.dropna()
print(df)

#Gráficos 
df.plot.line(style=['-', '--'], color=['y', 'r', 'g', 'c'], title='Graficos',subplots=True, grid=True)


#Histograma
fig.figure()
df['retorno'].plot.hist(bins=10, color='blue',density=True)
fig.title('Histograma dos retornos')
fig.xlabel=('Classes')
fig.ylabel('frequencia')
xmin=min(retorno)
xmax=max(retorno)
xmin,xmax=fig.xlim()


print('###########ESTATISTICAS DA AÇÃO##########################')
minimo= min(x) 
maximo=max(x)
inmax=df['retorno'].argmax()
inmin=df['retorno'].argmin()


 
print('ULTIMO PREÇO DO FECH(R$):   ', x[-1])

print('PREÇO MÉDIO DO FECH(R$):', s.mean(x))

print('MINIMO PREÇO DO FECH(R$)', minimo)   

print('MAXIMO PREÇO DO FECH(R$)', maximo)  

print('MAXIMO RETORNO DO FECH(%)',df['retorno'].max())

print('DIA DO MAXIMO RETORNO DO FECH', df.index[inmax])

print('MINIMO RETORNO DO FECH(%)', df['retorno'].min())

print('DIA DO MINIMO RETORNO DO FECH', df.index[inmin])

print('VOLATILIDADE (desv.pad.pop) DOS PREÇOS DO FECH', x.std())

print('VOLATILIDADE (desv.pad.pop) DOS RETORNOS DO FECH(%)', df['retorno'].std())




#Calculo da tendencia 
print(' o número de pontos da reta é', len(x))
k = np.arange(len(x))
coef=np.polyfit(k,x,1)
print('O coeficiente angular é', coef[0], 'O coeficiente linear é', coef[1])
tend=coef[0]*k+coef[1]


#Calculo da filtragem da tendencia 
dif=m.detrend_linear(x)


#Simulações de Monte Carlo 
MC=[]

for i in range(1,51):
    mt=coef[0]*k+coef[1]+2*(s.pstdev(dif))*np.random.randn(len(x))
    MC.append(mt)
   
fig.figure() 
fig.subplot(311).plot(k,x,'-k',k,tend,'--r')
fig.subplot(312).plot(k,dif)   
fig.subplot(313).plot(MC)
fig.subplot(311).set_title('Gráfico de Tendência')
fig.subplot(312).set_title('Gráfico de Tendência Ajustada')
fig.subplot(313).set_title('Simulações de Monte Carlo')
fig.subplot(311).set_xlabel('dias')
fig.subplot(312).set_xlabel('dias')
fig.subplot(313).set_xlabel('dias')


##Cenario Otimista e Pessimista
for i in range(1,51):
    if i==50:
        mediamc=mt.mean()
        desviomc=mt.std()


pes=mediamc-2*desviomc/math.sqrt(93)
oti=mediamc+2*desviomc/math.sqrt(93)
print('+++++++++++++ previsão para os preços da ação +++++++++++++')
print('pessimista(95%) = ', pes) 
print('otimista(95%) = ', oti)




    

