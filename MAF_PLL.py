'Itaipu Parquetec'
'Author: Gabriel Sgarbossa'
'Programa para implementação de um MAF-PLL para estimação de frequência e ângulo de fase'


import comtrade as ct
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd




#___________________________________________________________________________________________
#Funções

# def abc_to_dq0 (a, b, c, omega, theta, t):
    
#     d = (2/3) * (a*np.cos(omega * t + theta) 
#                  + b*np.cos(omega * t - 2*np.pi/3 + theta) 
#                  + c*np.cos(omega * t + 2*np.pi/3 + theta))
    
#     q = (2/3) * (a*np.sin(omega * t + theta) 
#                  + b*np.sin(omega * t - 2*np.pi/3 + theta) 
#                  + c*np.sin(omega * t + 2*np.pi/3 + theta))
    
#     z = (2/3) * (a + b + c)/2

#     return d, q, z

# def abc_to_dq0 (a, b, c, omega, theta, t):
    
#     d = (2/3) * (a*np.cos(omega * t ) 
#                  + b*np.cos(omega * t - 2*np.pi/3 ) 
#                  + c*np.cos(omega * t + 2*np.pi/3 ))
    
#     q = (2/3) * (a*np.sin(omega * t + theta) 
#                  + b*np.sin(omega * t - 2*np.pi/3 ) 
#                  + c*np.sin(omega * t + 2*np.pi/3 ))
    
#     z = (2/3) * (a + b + c)/2

#     return d, q, z

def abc_to_dq0 (a, b, c, omega, theta, t):
    
    d = (2/3) * (a*np.cos( theta ) 
                 + b*np.cos( theta - 2*np.pi/3 ) 
                 + c*np.cos( theta + 2*np.pi/3 ))
    
    q = (2/3) * (-a*np.sin(theta) 
                 - b*np.sin( theta - 2*np.pi/3 ) 
                 - c*np.sin( theta + 2*np.pi/3 ))
    
    z = (2/3) * (a + b + c)/2

    return d, q, z



def maf_filter (u):
    if len(u) < 256:
        return u
    else:
        y = sum(u)/256
        u[-1] = y
    return u




#___________________________________________________________________________________________
#Constantes iniciais
theta = 0                                                                                                  #Ângulo de fase inicial
wf = w0 = 2*np.pi*50                                                                                       #Frequência de referência
VD = []
VQ = []
Int = 0

teste = []



rec = ct.load("Comtrade/TesteASCII_Caso_0001_S.cfg","Comtrade/TesteASCII_Caso_0001_S.dat")                  #Carrega o arquivo comtrade
df = rec.to_dataframe()                                                                                     #Cria um dataframe com os registros de todos os canais
Va = df['CA00 - VA00']                                                                                      #Tensao Va
Vb = df['CA01 - VB00']                                                                                      #Tensao Vb
Vc = df['CA02 - VC00']                                                                                      #Tensao Vc






for i in range(0, len(df)):

    Vd, Vq, Vz = abc_to_dq0(Va.iloc[i], Vb.iloc[i], Vc.iloc[i], w0, theta, Va.index[i])                      #Calcula as componentes dq0

    
    if len(VD) < 256:
            VD.append(Vd)
            VQ.append(Vq)
    else:
            VD.pop(0)
            VQ.pop(0)
            VD.append(Vd)
            VQ.append(Vq)

            Vd_maf = maf_filter(VD)                                                                           #Aplica o filtro MAF
            Vq_maf = maf_filter(VQ)                                                                           #Aplica o filtro MAF

            In_PI = Vq_maf[-1]                                                                     
            
            Prop = In_PI * 50
            Int = Int + In_PI * 20/(12800)

            w0 = wf + Int 
            

            theta = theta + w0 + Prop
            teste.append(Vq)

            print(theta, w0, Vq_maf[-1], VQ[-1], In_PI)
   
                                                                          












#___________________________________________________________________________
#extras - desconsiderar
# plt.plot(teste)
plt.plot(teste)

# # # plt.plot(Vz, label='Vz')
# Vd, Vq, Vz = abc_to_dq0(Va, Vb, Vc, wf, theta)                                                                           

# plt.plot(Vd)
# plt.plot(Vq)
# plt.legend(['Vd','Vq'])


# plt.xlim([0,0.1])