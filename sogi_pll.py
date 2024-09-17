import math
import numpy as np


class DSOGI_QSG:
    def __init__(self, dt):
        self.dt = dt
        self.integrator_gain = 1
        self.proportional_gain = math.sqrt(2)
        self.signal_output = 0
        self.signal_output_q = 0
        self.integrator2 = 0

    #implementação da malha: v'/v = kws/(s^2 + ws + w^2) e qv'/v = kw^2/(s^2 + kws + w^2)
    def calculate(self, signal, omega):

        error = signal - self.signal_output

        output_proportional = self.proportional_gain * error

        error2 = output_proportional - self.signal_output_q

        output_proportional_2 = omega * error2

        self.signal_output = self.signal_output + (self.integrator_gain * self.dt * output_proportional_2)

        self.integrator2 = self.integrator2 + (self.integrator_gain * self.dt * self.signal_output)

        self.signal_output_q = omega * self.integrator2

        return self.signal_output, self.signal_output_q
