
from mafpll import MAF_PLL
from park_transform import ParkTransform

import comtrade as ct
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

#---------------------------------------------------------------------------------
# Aquisição dos sinais do comtrade	

comtrade_path = "D:/ARQUIVOS/Documents/Projeto_ProtVirtual/Comtrade/"                                                   #Caminho do arquivo comtrade

Vbase = 500000 / math.sqrt(3) * math.sqrt(2)                                                                            #Tensão base

rec = ct.load(comtrade_path + "TesteASCII_Caso_0001_S.cfg", comtrade_path + "TesteASCII_Caso_0001_S.dat")               #Carrega o arquivo comtrade
Va = np.array(rec.analog[4]) / Vbase                                                                                    #Tensao Va
Vb = np.array(rec.analog[5]) / Vbase                                                                                    #Tensao Vb
Vc = np.array(rec.analog[6]) / Vbase                                                                                    #Tensao Vc
time = np.array(rec.time)


#---------------------------------------------------------------------------------
# Plot dos sinais do comtrade

plt.figure()
plt.plot(time, Va, label="Va")
plt.plot(time, Vb, label="Vb")
plt.plot(time, Vc, label="Vc")
plt.title('Tensões Va, Vb, Vc')
plt.xlabel('Tempo [s]')
plt.ylabel('Tensão [V]')
plt.legend()
plt.grid(True)
plt.show()

#---------------------------------------------------------------------------------
# Cálculos do PLL

dt = time[1] - time[0]                                                                                                  #Calcula o intervalo de amostragem
print(dt)
pll = MAF_PLL(window_size=8, nominal_frequency=50, dt=dt)                                                               #Inicializa o objeto PLL

Vd = np.zeros_like(time)                                                                                                #Cria um array para componente d da tensão
Vq = np.zeros_like(time)                                                                                                #Cria um array para componente q da tensão
Vz = np.zeros_like(time)                                                                                                #Cria um array para componente z da tensão
theta = np.zeros_like(time)                                                                                             #Cria um array para o ângulo theta
pll_omega_freq = np.zeros_like(time)                                                                                    #Cria um array para a frequência do PLL

for i in range(len(time)):
    if i == 0:
        Vd[i], Vq[i], Vz[i] = ParkTransform.abc_to_dq0(Va[i], Vb[i], Vc[i], 0)                                          #Calcula as componentes dq0 da tensão
    else:
        Vd[i], Vq[i], Vz[i] = ParkTransform.abc_to_dq0(Va[i], Vb[i], Vc[i], theta[i-1])                                 #Calcula as componentes dq0 da tensão
    pll_omega_freq[i], theta[i] = pll.calculate(Vd[i], Vq[i])                                                           #Calcula a frequência e o ângulo do PLL


#---------------------------------------------------------------------------------
# Plot das variáveis do PLL

plt.figure()
plt.plot(time, Vd, label="Vd")
plt.plot(time, Vq, label="Vq")
plt.plot(time, Vz, label="Vz")
plt.title('Tensões Vd, Vq, Vz')
plt.xlabel('Tempo [s]')
plt.ylabel('Tensão [V]')
plt.legend()
plt.grid(True)
plt.show()

plt.figure()
plt.plot(time, pll_omega_freq, label="omega")
plt.title('Frequency')
plt.xlabel('Tempo [s]')
plt.ylabel('Frequency [rad/s]')
plt.legend()
plt.grid(True)
plt.show()

plt.figure()
plt.plot(time, theta, label="Theta")
plt.title('Theta')
plt.xlabel('Tempo [s]')
plt.ylabel('Theta [rad]')
plt.legend()
plt.grid(True)
plt.show()
