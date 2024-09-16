import numpy as np


class SRF_PLL:
    def __init__(self, nominal_frequency, dt):
        self.nominal_omega_frequency = nominal_frequency * 2 * np.pi
        self.pll_omega_frequency = 0
        self.dt = dt
        self.proportional_gain = 50
        self.integrator_gain = 70
        self.output_proportional = 0
        self.output_integrator = 0
        self.theta = 0

    def calculate(self, vq_signal):
        self.output_proportional = self.proportional_gain * vq_signal
        self.output_integrator = self.output_integrator + (self.integrator_gain * self.dt * vq_signal)

        self.pll_omega_frequency = self.output_integrator + self.output_proportional + self.nominal_omega_frequency

        self.theta = self.theta + (self.dt * self.pll_omega_frequency)

        if self.theta >= np.pi:
            self.theta = self.theta - (2.0 * np.pi)

        return self.pll_omega_frequency, self.theta
