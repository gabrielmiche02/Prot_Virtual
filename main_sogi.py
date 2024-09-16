'Itaipu Parquetec'
import math

from clark_transform import ClarkTransform
from mafpll import MAF_PLL
from park_transform import ParkTransform
from sogi_pll import DSOGI_QSG
from srf_pll import SRF_PLL

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

sogi_alpha = DSOGI_QSG(dt)
sogi_beta = DSOGI_QSG(dt)
srf_pll = SRF_PLL(50, dt)

Valpha = np.zeros_like(time)
Vbeta = np.zeros_like(time)
Vd = np.zeros_like(time)
Vq = np.zeros_like(time)
Vz = np.zeros_like(time)
theta = np.zeros_like(time)
omega = np.zeros_like(time)

sogi_alphal = np.zeros_like(time)
sogi_qalphal = np.zeros_like(time)
sogi_betal = np.zeros_like(time)
sogi_qbetal = np.zeros_like(time)
Valpha_pos = np.zeros_like(time)
Vbeta_pos = np.zeros_like(time)

for i in range(len(time)):
    Valpha[i], Vbeta[i] = ClarkTransform.abc_to_alphabeta(Va[i], Vb[i], Vc[i])
    if i == 0:
        sogi_alphal[i], sogi_qalphal[i] = sogi_alpha.calculate(Valpha[i], 314.15) # Passar frequência nominal
        sogi_betal[i], sogi_qbetal[i] = sogi_beta.calculate(Vbeta[i], 314.15) # Passar frequência nominal
    else:
        sogi_alphal[i], sogi_qalphal[i] = sogi_alpha.calculate(Valpha[i], omega[i-1])
        sogi_betal[i], sogi_qbetal[i] = sogi_beta.calculate(Vbeta[i], omega[i-1])

    Valpha_pos[i] = sogi_alphal[i] - sogi_qbetal[i]
    Vbeta_pos[i] = sogi_qalphal[i] + sogi_betal[i]

    Vd[i], Vq[i] = ParkTransform.alphabeta_to_dq(Valpha_pos[i], Vbeta_pos[i], theta[i-1])

    omega[i], theta[i] = srf_pll.calculate(Vq[i])


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
plt.plot(time, omega, label="omega")
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
