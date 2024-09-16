'Itaipu Parquetec'
import math

from mafpll import MAF_PLL
from park_transform import ParkTransform

'Author: Gabriel Sgarbossa'
'Programa para implementação de um MAF-PLL para estimação de frequência e ângulo de fase'


import comtrade as ct
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

comtrade_path = "C:/Users/guilherme.zat/Downloads/"

Vbase = 500000 / math.sqrt(3) * math.sqrt(2)

rec = ct.load(comtrade_path + "TesteASCII_Caso_0001_S.cfg", comtrade_path + "TesteASCII_Caso_0001_S.dat")                  #Carrega o arquivo comtrade
df = rec.to_dataframe()                                                                                     #Cria um dataframe com os registros de todos os canais
Va = np.array(rec.analog[4]) / Vbase                                                                                   #Tensao Va
Vb = np.array(rec.analog[5]) / Vbase                                                                                      #Tensao Vb
Vc = np.array(rec.analog[6]) / Vbase                                                                                       #Tensao Vc
time = np.array(rec.time)

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

dt = time[1] - time[0]
print(dt)
pll = MAF_PLL(window_size=8, nominal_frequency=50, dt=dt)

Vd = np.zeros_like(time)
Vq = np.zeros_like(time)
Vz = np.zeros_like(time)
theta = np.zeros_like(time)
pll_omega_freq = np.zeros_like(time)

for i in range(len(time)):
    if i == 0:
        Vd[i], Vq[i], Vz[i] = ParkTransform.abc_to_dq0(Va[i], Vb[i], Vc[i], 0)
    else:
        Vd[i], Vq[i], Vz[i] = ParkTransform.abc_to_dq0(Va[i], Vb[i], Vc[i], theta[i-1])
    pll_omega_freq[i], theta[i] = pll.calculate(Vd[i], Vq[i])


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
