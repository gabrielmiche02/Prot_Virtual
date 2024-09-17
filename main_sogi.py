'Itaipu Parquetec'
import math

from clark_transform import ClarkTransform
from mafpll import MAF_PLL
from park_transform import ParkTransform
from sogi_pll import DSOGI_QSG
from srf_pll import SRF_PLL

'Author: Gabriel Lavisch Michelom'
'Programa para implementação de um SOGI-PLL para estimação de frequência e ângulo de fase'


import comtrade as ct
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

comtrade_path = "C:/Users\gabri/OneDrive/Área de Trabalho/Bolsa_PTI/COMTRADE/"

Vbase = 500000 / math.sqrt(3) * math.sqrt(2)    #Tensão de base do sistema - 500 kV

rec = ct.load(comtrade_path + "TesteASCII_Caso_0001_S.cfg", comtrade_path + "TesteASCII_Caso_0001_S.dat")                  #Carrega o arquivo comtrade
df = rec.to_dataframe()                                                                                     #Cria um dataframe com os registros de todos os canais
Va = np.array(rec.analog[4]) / Vbase                                                                                   #Tensao Va em p.u
Vb = np.array(rec.analog[5]) / Vbase                                                                                      #Tensao Vb em p.u
Vc = np.array(rec.analog[6]) / Vbase                                                                                       #Tensao Vc em p.u
time = np.array(rec.time)

##plotagem das tensões Va, Vb e Vc
# plt.figure()
# plt.plot(time, Va, label="Va")
# plt.plot(time, Vb, label="Vb")
# plt.plot(time, Vc, label="Vc")
# plt.title('Tensões Va, Vb, Vc')
# plt.xlabel('Tempo [s]')
# plt.ylabel('Tensão [V]')
# plt.legend()
# plt.grid(True)
# plt.show()

dt = time[1] - time[0]  # Tempo de amostragem

# Inicialização dos objetos
sogi_alpha = DSOGI_QSG(dt) 
sogi_beta = DSOGI_QSG(dt)   
srf_pll = SRF_PLL(50, dt)   

# Inicialização das variáveis
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
    Valpha[i], Vbeta[i] = ClarkTransform.abc_to_alphabeta(Va[i], Vb[i], Vc[i])  # Transformação de abc para alfa beta
    if i == 0:
        sogi_alphal[i], sogi_qalphal[i] = sogi_alpha.calculate(Valpha[i], 314.15) # Passar frequência nominal
        sogi_betal[i], sogi_qbetal[i] = sogi_beta.calculate(Vbeta[i], 314.15) # Passar frequência nominal
    else:
        sogi_alphal[i], sogi_qalphal[i] = sogi_alpha.calculate(Valpha[i], omega[i-1])
        sogi_betal[i], sogi_qbetal[i] = sogi_beta.calculate(Vbeta[i], omega[i-1])

    Valpha_pos[i] = 1/2*(sogi_alphal[i] - sogi_qbetal[i])   #sequencia positiva de Valpha
    Vbeta_pos[i] = 1/2*(sogi_qalphal[i] + sogi_betal[i])    #sequencia positiva de Vbeta

    Vd[i], Vq[i] = ParkTransform.alphabeta_to_dq(Valpha_pos[i], Vbeta_pos[i], theta[i-1])   # Transformação de alfa beta para dq

    omega[i], theta[i] = srf_pll.calculate(Vq[i]) # Cálculo da frequência e do ângulo de fase


# plt.figure()
# plt.plot(time, Valpha, label="Valpha")
# plt.plot(time, Vbeta, label="Vbeta")
# plt.title('Tensões Valpha, Vbeta')
# plt.xlabel('Tempo [s]')
# plt.ylabel('Tensão [V]')
# plt.legend()
# plt.grid(True)
# plt.show()

# plt.figure()
# plt.plot(time, sogi_alphal, label="Valpha_l")
# plt.plot(time, sogi_qalphal, label="Vqbeta_ql")
# plt.title('Tensões Valpha\' e qValpha\' ')
# plt.xlabel('Tempo [s]')
# plt.ylabel('Tensão [V]')
# plt.legend()
# plt.grid(True)
# plt.show()


# plt.figure()
# plt.plot(time, Valpha_pos, label="Valpha_pos")
# plt.plot(time, Vbeta_pos, label="Vqbeta_pos")
# plt.title('Tensões Valpha Vbeta seq. positiva')
# plt.xlabel('Tempo [s]')
# plt.ylabel('Tensão [V]')
# plt.legend()
# plt.grid(True)
# plt.show()


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

# plt.figure()
# plt.plot(time, omega, label="omega")
# plt.title('Frequency')
# plt.xlabel('Tempo [s]')
# plt.ylabel('Frequency [rad/s]')
# plt.legend()
# plt.grid(True)
# plt.show()

# plt.figure()
# plt.plot(time, theta, label="Theta")
# plt.title('Theta')
# plt.xlabel('Tempo [s]')
# plt.ylabel('Theta [rad]')
# plt.legend()
# plt.grid(True)
# plt.show()
